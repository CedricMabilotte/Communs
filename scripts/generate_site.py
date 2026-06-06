#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_site.py — Génère le site public « Terres Libérées ».

Fork de Résidence. À partir des fiches YAML (lieux/ porteurs/ usufruitiers/
modeles/) et de la configuration (config/), produit un site statique :
accueil, catalogues par catégorie, fiches détaillées, classement par l'Indice
de libération, pages grilles / modèles / méthode.

Aucune dépendance hors PyYAML. Usage : python3 scripts/generate_site.py
"""
from __future__ import annotations
import datetime
import html
import json
import math
import re
import shutil
import unicodedata
from pathlib import Path

import yaml

try:
    import weasyprint as _weasyprint  # noqa: F401
    HAS_WEASYPRINT = True
except Exception:
    HAS_WEASYPRINT = False

# Date de génération du site — affichée en pied de page et dans le sitemap.
BUILD_DATE = datetime.date.today().isoformat()

# Variante française lisible de la date de génération (pied de page public).
_MOIS_FR = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
            "août", "septembre", "octobre", "novembre", "décembre")
_today = datetime.date.today()
BUILD_DATE_FR = f"{_today.day} {_MOIS_FR[_today.month - 1]} {_today.year}"

# Version publique du site — affichée discrètement en pied de page et reprise
# dans le journal des versions (changelog.html). Version majeure 2.0 = modèle
# d'évaluation renforcé.
SITE_VERSION = "3.1"
SITE_VERSION_DATE = "juin 2026"

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
SITE = ROOT / "site"
ASSETS = SITE / "assets"

CAT_DIR = {"lieu": "lieux", "porteur": "porteurs",
           "usufruitier": "usufruitiers", "modele": "modeles",
           "reseau": "reseaux"}
CAT_SLUG = {"lieu": "l", "porteur": "p", "usufruitier": "u", "modele": "m",
            "reseau": "r"}
CAT_PAGE = {"lieu": "lieux.html", "porteur": "porteurs.html",
            "usufruitier": "usufruitiers.html", "modele": "modeles.html",
            "reseau": "reseaux.html"}
# Libellé court de chaque catégorie — source unique, réutilisée partout.
CAT_LABEL = {"lieu": "Lieu", "porteur": "Porteur de nue-propriété",
             "usufruitier": "Organisme usufruitier", "modele": "Modèle voisin",
             "reseau": "Réseau"}

# ─────────────────────────────────────────────────────────────────────────────
# Chargement
# ─────────────────────────────────────────────────────────────────────────────

def load_yaml(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_config():
    return {
        "concepts": load_yaml(CONFIG / "concepts.yml"),
        "grilles": load_yaml(CONFIG / "grilles.yml"),
        "ranking": load_yaml(CONFIG / "ranking.yml"),
    }


def load_fiches():
    fiches = []
    for cat, d in CAT_DIR.items():
        folder = ROOT / d
        if not folder.exists():
            continue
        for fp in sorted(folder.glob("*.yml")):
            data = load_yaml(fp)
            if not data:
                continue
            data.setdefault("categorie", cat)
            data["_file"] = fp.name
            fiches.append(data)
    return fiches


def verifier_uids(fiches):
    """Garde-fou (leçon session #2) : aucun uid ne doit désigner deux fiches.
    L'index by_uid est plat — un uid en doublon écraserait silencieusement une
    fiche, et les chaînes pointant vers cet uid deviendraient ambiguës. Tout
    doublon fait échouer la génération."""
    vus = {}
    fautes = []
    for f in fiches:
        u = f.get("uid")
        loc = f"{f.get('categorie','?')}/{f.get('_file','?')}"
        if u in vus:
            fautes.append(f"{u} — {vus[u]} ET {loc}")
        else:
            vus[u] = loc
    return fautes


# ─────────────────────────────────────────────────────────────────────────────
# Scoring — l'Indice de libération
# ─────────────────────────────────────────────────────────────────────────────

def grille_index(grilles_cfg):
    """Renvoie {categorie: {critere_id: {axe, poids, label, definition}}}."""
    idx = {}
    for cat, gril in grilles_cfg["grilles"].items():
        cmap = {}
        for fam in gril["familles"]:
            for cr in fam["criteres"]:
                cmap[cr["id"]] = {"axe": cr["axe"], "poids": cr["poids"],
                                  "label": cr["label"], "definition": cr["definition"],
                                  "famille": fam["label"]}
        idx[cat] = cmap
    return idx


def axes_ids(ranking):
    """Liste ordonnée des identifiants d'axes (entiers 1..5)."""
    return [a["id"] for a in ranking["axes"]]


# Plancher d'axe pour l'agrégation géométrique. Un axe à 0 (dimension
# entièrement échouée) doit faire chuter l'Indice très bas — c'est le principe
# non compensatoire — mais sans l'annuler purement : un montage fort sur quatre
# axes et nul sur un cinquième vaut « éloigné », pas « rien ». On plancher donc
# chaque axe à 0,5 dans le PRODUIT seulement ; le profil affiché garde le 0
# réel. Session #5 : passage de 1 à 0,5 pour redonner du tranchant à
# l'agrégation non compensatoire — un axe écrasé pèse désormais plus.
AXE_PLANCHER_GEO = 0.5


def geometric_idl(axes_scores):
    """Moyenne géométrique des scores d'axes renseignés (agrégation NON
    compensatoire). Chaque axe est planché à AXE_PLANCHER_GEO dans le produit
    pour qu'un axe nul écrase fortement l'Indice sans l'annihiler. Aucun axe
    renseigné → None."""
    known = [v for v in axes_scores.values() if v is not None]
    k = len(known)
    if k == 0:
        return None
    produit = 1.0
    for v in known:
        produit *= max(v, AXE_PLANCHER_GEO)
    return round(produit ** (1.0 / k))


def score_fiche(fiche, gidx, ranking):
    """Calcule les cinq axes (1..5, 0-100), l'Indice global (moyenne
    géométrique non compensatoire), le palier et la complétude."""
    valeurs = ranking["valeurs"]
    cat = fiche["categorie"]
    aids = axes_ids(ranking)

    if cat == "reseau":
        # un réseau n'est pas une chaîne : il ne porte pas d'Indice (cf. R1).
        # Sa fiche est un hub qui présente l'entité et relie ses membres.
        return {"axes": {aid: None for aid in aids}, "idl": None,
                "idl_brut": None, "palier": None, "completude": None,
                "estime": False, "score_type": "reseau", "criteres_evalues": {}}

    if cat == "modele":
        ax = fiche.get("axes_estimes", {}) or {}
        # Les fiches modeles utilisent les clés entières 1..5. Tolérance de
        # repli sur l'ancien jeu A/B/C → 1..3 si une fiche n'a pas encore
        # migré, pour ne jamais planter la génération.
        legacy = {"A": 1, "B": 2, "C": 3}
        axes = {}
        for aid in aids:
            v = ax.get(aid)
            if v is None:
                # repli : clé string de l'entier, ou ancienne lettre A/B/C
                v = ax.get(str(aid))
            if v is None:
                for old, new in legacy.items():
                    if new == aid and ax.get(old) is not None:
                        v = ax.get(old)
                        break
            axes[aid] = round(float(v)) if v is not None else None
        idl_brut = geometric_idl(axes)
        # Session #5 — pénalité d'estimation. Les modèles voisins, notés par
        # `axes_estimes` plutôt que par grille sur sources, recevaient
        # jusque-là un IdL sans pénalité, ce qui les hissait au-dessus des
        # lieux peuplés (CLT Bruxelles à 87, devant le Domaine du Rayol —
        # seul sanctuaire — à 77). Une fiche estimée est par construction
        # moins fiable qu'une fiche sourcée : on lui applique la même formule
        # de pénalité de complétude qu'à une fiche moyennement renseignée
        # (complétude forfaitaire 0,7), pour qu'un modèle voisin atteigne au
        # mieux le bas du palier « montage solide ».
        PENALITE_MODELE = 0.5 + 0.5 * 0.7  # = 0,85
        idl = round(idl_brut * PENALITE_MODELE) if idl_brut is not None else None
        return {"axes": axes, "idl": idl, "idl_brut": idl_brut,
                "palier": palier_for(idl, ranking),
                "completude": None, "estime": True,
                "score_type": "estime", "criteres_evalues": {}}

    cmap = gidx.get(cat, {})
    acc = {aid: [0.0, 0.0] for aid in aids}  # axe → [poids_total, poids_obtenu]
    n_total = len(cmap)
    n_known = 0
    criteres_evalues = {}
    for entry in fiche.get("grille", []) or []:
        cid = entry.get("critere")
        if cid not in cmap:
            continue
        meta = cmap[cid]
        val = entry.get("valeur", "inconnu")
        criteres_evalues[cid] = {"valeur": val, "note": entry.get("note", ""),
                                 **meta}
        factor = valeurs.get(val)
        if factor is None:  # inconnu → exclu
            continue
        n_known += 1
        axe = meta["axe"]
        if axe in acc:
            acc[axe][0] += meta["poids"]
            acc[axe][1] += meta["poids"] * factor

    axes = {}
    for axe in aids:
        wtot, wobt = acc[axe]
        axes[axe] = round(wobt / wtot * 100) if wtot > 0 else None

    # Indice brut : moyenne géométrique non compensatoire des axes renseignés.
    idl_brut = geometric_idl(axes)
    completude = (n_known / n_total) if n_total else 0.0
    # Pénalité de complétude : l'indice affiché est l'indice brut pondéré par la
    # complétude, pour ne pas surnoter les fiches lacunaires (cf. ranking.yml).
    if idl_brut is not None:
        idl = round(idl_brut * (0.5 + 0.5 * completude))
    else:
        idl = None
    return {"axes": axes, "idl": idl, "idl_brut": idl_brut,
            "palier": palier_for(idl, ranking),
            "completude": completude, "estime": False,
            "score_type": "calcule", "criteres_evalues": criteres_evalues}


def _median(values):
    """Médiane d'une liste non vide de nombres."""
    s = sorted(values)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2.0


# Axes « contaminables » par la chaîne : la structure (2), la finalité (4) et
# l'usage (5). L'axe 1 (le sol) reste intrinsèque au porteur, l'axe 3 (le
# pouvoir) intrinsèque à l'usufruitier. Cf. ranking.yml § option_a.
CHAINE_AXES_CONTAMINABLES = (2, 4, 5)


def chained_uids(fiche, by_uid):
    """Renvoie les uid des LIEUX reliés à une fiche par une CHAÎNE.

    Le lieu est la source unique de vérité : il déclare `chaine.porteurs` et
    `chaine.usufruitiers`. Un porteur ou un usufruitier reçoit ses lieux par
    rétro-référence (les lieux dont la chaîne le citent). Les liens `voir_aussi`
    sont éditoriaux et n'entrent jamais dans la chaîne ni dans le scoring."""
    me = fiche["uid"]
    lieux = set()
    for other_uid, other in by_uid.items():
        if other_uid == me or other.get("categorie") != "lieu":
            continue
        ch = other.get("chaine", {}) or {}
        if me in (ch.get("porteurs") or []) or me in (ch.get("usufruitiers") or []):
            lieux.add(other_uid)
    return sorted(lieux)


def apply_chaine(all_sc, by_uid, ranking):
    """Calcule l'indice EFFECTIF des porteurs et usufruitiers : relit l'indice
    intrinsèque à travers les chaînes (lieux reliés).

    Pour les axes contaminables (2, 4, 5), l'axe effectif = min(axe
    intrinsèque, médiane de cet axe sur les lieux reliés). Les axes 1 et 3
    restent intrinsèques. L'indice effectif = moyenne géométrique des axes
    effectifs, puis pénalité de complétude. Sans lieu relié, effectif =
    intrinsèque. Les lieux et les modèles ne sont pas recalculés.

    Mute chaque dict de score en place : ajoute `axes_intr`, `idl_intr`,
    `idl_brut_intr` (valeurs intrinsèques conservées) et remplace `axes`,
    `idl`, `idl_brut`, `palier` par les valeurs effectives."""
    sc_by_uid = {f["uid"]: sc for f, sc in all_sc}
    for fiche, sc in all_sc:
        cat = fiche["categorie"]
        # valeurs intrinsèques toujours conservées pour affichage
        sc["axes_intr"] = dict(sc["axes"])
        sc["idl_intr"] = sc["idl"]
        sc["idl_brut_intr"] = sc.get("idl_brut")
        sc["chaine_uids"] = []
        if cat not in ("porteur", "usufruitier"):
            continue
        lieux = chained_uids(fiche, by_uid)
        sc["chaine_uids"] = lieux
        if not lieux:
            continue
        eff = dict(sc["axes"])
        for axe in CHAINE_AXES_CONTAMINABLES:
            vals = []
            for luid in lieux:
                lsc = sc_by_uid.get(luid)
                if lsc and lsc["axes"].get(axe) is not None:
                    vals.append(lsc["axes"][axe])
            intr = sc["axes"].get(axe)
            if vals and intr is not None:
                eff[axe] = round(min(intr, _median(vals)))
        sc["axes"] = eff
        idl_brut = geometric_idl(eff)
        sc["idl_brut"] = idl_brut
        comp = sc.get("completude")
        if idl_brut is not None and comp is not None:
            sc["idl"] = round(idl_brut * (0.5 + 0.5 * comp))
        elif idl_brut is not None:
            sc["idl"] = idl_brut
        else:
            sc["idl"] = None
        sc["palier"] = palier_for(sc["idl"], ranking)


def palier_for(idl, ranking, verdict=None):
    """Palier (tier) correspondant à l'IdL. Session #5 : un palier portant
    `requiert_verdict` n'est accessible qu'aux lieux dont le verdict est
    exactement celui demandé. Sinon, le palier est dégradé d'un cran (le
    suivant dans la liste). Le verdict est ignoré pour les fiches non-lieu
    (porteur, usufruitier, modele) — leur palier ne dépend que de l'IdL."""
    if idl is None:
        return None
    paliers = ranking["paliers"]
    for i, p in enumerate(paliers):  # ordonnés du plus haut au plus bas
        if idl >= p["min"]:
            req = p.get("requiert_verdict")
            if req and verdict != req:
                # Verdict ne satisfait pas l'exigence : on dégrade au palier suivant.
                # Si le palier suivant a lui-même une exigence, on continue.
                for j in range(i + 1, len(paliers)):
                    q = paliers[j]
                    if q.get("requiert_verdict") and verdict != q.get("requiert_verdict"):
                        continue
                    return q
                return paliers[-1]
            return p
    return paliers[-1]


# ── Plafond de chaîne sur l'axe 2 des LIEUX (session #5) ─────────────────────
# Le score d'axe 2 d'un lieu est plafonné selon le pire `nature_interet` de sa
# chaîne (porteurs + usufruitiers). Cf. ranking.yml § plafonds_chaine. Le score
# intrinsèque est conservé pour information ; l'écart est restitué sur la
# fiche. Source unique de vérité : la chaîne — comme pour le verdict.

# Ordre du « pire au mieux » des natures, du plus restrictif au moins.
# Sert à choisir le maillon décisif quand la chaîne en mélange plusieurs.
_NATURE_ORDRE_PIRE_AU_MIEUX = [
    "privee_individuelle", "commerciale", "exploitation_agricole",
    "commerciale_encadree", "commerciale_desactivee", "non_lucrative", "inconnu",
]


def _pire_nature_chaine(fiche, by_uid):
    """Renvoie le `nature_interet` du maillon le plus restrictif de la chaîne
    d'un lieu (porteurs + usufruitiers). Renvoie None si chaîne vide."""
    ch = fiche.get("chaine", {}) or {}
    maillons = list(ch.get("porteurs") or []) + list(ch.get("usufruitiers") or [])
    if not maillons:
        return None
    natures = []
    for u in maillons:
        ent = by_uid.get(u) or {}
        natures.append(ent.get("nature_interet") or "inconnu")
    for n in _NATURE_ORDRE_PIRE_AU_MIEUX:
        if n in natures:
            return n
    return None


def apply_lieu_plafond_chaine(all_sc, by_uid, ranking):
    """Pour chaque lieu, plafonne le score d'axe 2 (la structure) selon le pire
    maillon de sa chaîne. Le mécanisme parallèle au verdict — calculé sur la
    même donnée — garantit que la grille saisie ne peut pas afficher un axe 2
    plus haut que la chaîne ne le permet (session #5, faille structurelle :
    grille saisie et nature_interet pouvaient se contredire, ex. GAEC coté
    'non commercial').

    Conserve `sc['axes_intr']` (axes pré-plafond) et ajoute `sc['ax2_plafond']`
    (la valeur du plafond appliqué, ou None si non appliqué). Recalcule IdL,
    palier et axes effectifs. À appeler APRÈS apply_chaine (mais celle-ci ne
    touche pas les lieux ; donc l'ordre n'a pas d'importance sur les lieux)."""
    plafonds = ((ranking.get("plafonds_chaine") or {})
                .get("ax2_par_nature") or {})
    if not plafonds:
        return
    for fiche, sc in all_sc:
        if fiche.get("categorie") != "lieu":
            continue
        # axes_intr est posé par apply_chaine pour porteur/usufruitier ; pour
        # un lieu, apply_chaine ne fait rien — on l'initialise ici pour cohérence.
        sc.setdefault("axes_intr", dict(sc["axes"]))
        sc["ax2_plafond"] = None
        ax2 = sc["axes"].get(2)
        if ax2 is None:
            continue
        pire = _pire_nature_chaine(fiche, by_uid)
        if not pire:
            continue
        plafond = plafonds.get(pire)
        if plafond is None:
            continue  # inconnu : pas de plafond (par défaut prudent)
        if ax2 > plafond:
            sc["ax2_plafond"] = plafond
            sc["ax2_intrinseque"] = ax2  # conservé pour l'affichage
            sc["ax2_nature_pire"] = pire
            new_axes = dict(sc["axes"])
            new_axes[2] = plafond
            sc["axes"] = new_axes
            idl_brut = geometric_idl(new_axes)
            sc["idl_brut"] = idl_brut
            comp = sc.get("completude")
            if idl_brut is not None and comp is not None:
                sc["idl"] = round(idl_brut * (0.5 + 0.5 * comp))
            elif idl_brut is not None:
                sc["idl"] = idl_brut


def apply_palier_verdict_constraint(all_sc, by_uid, ranking):
    """Recalcule les paliers en tenant compte du verdict du lieu. Les paliers
    portant `requiert_verdict: sanctuaire` ne sont accessibles qu'aux lieux
    verdict==sanctuaire. À appeler APRÈS apply_lieu_plafond_chaine (qui peut
    avoir modifié l'IdL). Les fiches non-lieu ne sont pas re-paliérées (mais
    leurs paliers déjà calculés sont relus via palier_for — si la définition
    d'un palier exige un verdict, une porteur/usufruitier ne peut pas y entrer
    parce qu'ils n'ont pas de verdict)."""
    for fiche, sc in all_sc:
        if sc.get("idl") is None:
            continue
        if fiche.get("categorie") == "lieu":
            v = compute_verdict(fiche, by_uid)
        else:
            v = None
        sc["palier"] = palier_for(sc["idl"], ranking, verdict=v)
        sc["verdict"] = v  # mémorise pour l'affichage


def fiabilite_label(completude, ranking):
    if completude is None:
        return ("Estimation comparative", "faint")
    seuils = ranking["fiabilite"]
    if completude >= seuils["seuil_completude_bon"]:
        return ("Fiche bien renseignée", "ok")
    if completude >= seuils["seuil_completude_moyen"]:
        return ("Fiche fiable avec réserves", "gold")
    return ("Fiche à compléter", "faint")


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires HTML
# ─────────────────────────────────────────────────────────────────────────────

def e(x):
    return html.escape(str(x)) if x is not None else ""


def clean(text):
    """Replie les textes YAML multi-lignes."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


# Espace fine insécable (U+202F) — typographie française.
_NNBSP = " "


def typo(text):
    """Applique la typographie française au texte VISIBLE uniquement : espace
    fine insécable devant ; ? ! et :, et à l'intérieur des guillemets « ».

    À n'appliquer qu'à du texte destiné à l'affichage, jamais à du HTML brut,
    à des URL, du JSON-LD ou des fichiers .js/.xml — l'insécable y serait un
    caractère parasite. Idempotent : ne double pas une insécable déjà posée."""
    if not text:
        return ""
    t = str(text)
    # espace fine insécable devant la ponctuation double — on remplace une
    # éventuelle espace ordinaire, ou on insère si la ponctuation est collée.
    t = re.sub(r"[   ]*([;?!:])", _NNBSP + r"\1", t)
    # intérieur des guillemets : après « , avant »
    t = re.sub(r"«[   ]*", "«" + _NNBSP, t)
    t = re.sub(r"[   ]*»", _NNBSP + "»", t)
    return t


def slugify(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "x"


def meta_desc(text, limit=155):
    """Tronque une description à ~155 caractères sur une frontière de mot."""
    t = clean(text)
    if len(t) <= limit:
        return t
    cut = t[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.")
    return cut + "…"


# ─────────────────────────────────────────────────────────────────────────────
# Liage du glossaire — première occurrence par page des termes pivots
# ─────────────────────────────────────────────────────────────────────────────

# Termes pivots reliés, du plus long au plus court (pour éviter qu'un terme
# court masque un terme long). Le slug doit correspondre à une ancre du
# glossaire (id="g-…"), cf. GLOSSAIRE / slugify().
GLOSS_TERMS = [
    ("agrégation non compensatoire", "agregation-non-compensatoire"),
    ("libération des terres", "liberation-des-terres"),
    ("indice de libération", "indice-de-liberation"),
    ("intégrité du montage", "integrite-du-montage"),
    ("bail emphytéotique", "bail-emphyteotique"),
    ("fonds de dotation", "fonds-de-dotation"),
    ("utilité publique", "utilite-publique"),
    ("commun libre et vivant", "commun"),
    ("intérêt général", "interet-general"),
    ("fondation RUP", "fondation-rup"),
    ("nue-propriété", "nue-propriete"),
    ("démembrement", "demembrement"),
    ("bail rural", "bail-rural"),
    ("faux ami", "faux-ami"),
    ("usufruit", "usufruit"),
    ("chaîne", "chaine"),
]


def link_glossary(body, up):
    """Lie sobrement la première occurrence par page de chaque terme pivot vers
    son ancre du glossaire. Opère sur le HTML déjà assemblé ; ne touche ni à
    l'intérieur des balises, ni aux liens existants, ni aux titres, pour ne pas
    surligner tout le texte (audit pédagogie C, C1)."""
    # segmente le HTML : on ne modifie que les segments de texte hors balise,
    # et on saute entièrement les zones <a …>…</a>, <h1>…</h6>, <script>, <svg>.
    skip_pat = re.compile(
        r'<a\b[^>]*>.*?</a>|<h[1-6]\b[^>]*>.*?</h[1-6]>'
        r'|<select\b[^>]*>.*?</select>'
        r'|<script\b[^>]*>.*?</script>|<svg\b[^>]*>.*?</svg>'
        r'|<style\b[^>]*>.*?</style>|<[^>]+>',
        re.S)
    done = set()
    out = []
    pos = 0
    for m in skip_pat.finditer(body):
        # texte brut entre deux éléments à sauter
        out.append(_link_text_chunk(body[pos:m.start()], up, done))
        out.append(m.group(0))
        pos = m.end()
    out.append(_link_text_chunk(body[pos:], up, done))
    return "".join(out)


def apply_typo(body):
    """Applique typo() aux seuls nœuds de texte visibles du HTML assemblé.

    Saute l'intérieur des balises, des <script> (donc le JSON-LD, ajouté plus
    tard de toute façon), <style> et <svg> — où l'espace fine insécable serait
    un caractère parasite. Les URL et attributs vivent dans les balises : ils
    ne sont jamais touchés."""
    # On saute aussi les entités HTML (&#x27; &amp; &quot; …) : leur point-virgule
    # final ne doit pas recevoir d'espace fine insécable, qui casserait l'entité.
    skip_pat = re.compile(
        r'<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>'
        r'|<svg\b[^>]*>.*?</svg>|<[^>]+>|&#?[0-9A-Za-z]+;',
        re.S)
    out, pos = [], 0
    for m in skip_pat.finditer(body):
        out.append(typo(body[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(typo(body[pos:]))
    return "".join(out)


def _link_text_chunk(text, up, done):
    if not text:
        return text
    for term, slug in GLOSS_TERMS:
        if slug in done:
            continue
        # première occurrence, frontière de mot, insensible à la casse
        pat = re.compile(r'(?<![\w-])(' + re.escape(term) + r')(?![\w-])',
                         re.IGNORECASE)
        m = pat.search(text)
        if not m:
            continue
        done.add(slug)
        link = (f'<a class="gloss-link" href="{up}glossaire.html#g-{slug}">'
                f'{m.group(1)}</a>')
        text = text[:m.start()] + link + text[m.end():]
    return text


# ─────────────────────────────────────────────────────────────────────────────
# Gabarit de page
# ─────────────────────────────────────────────────────────────────────────────

# NAV principal — 6 entrées de parcours (faire / comprendre). Les pages de
# référence documentaire (Trois régimes, Grilles, Modèles voisins, Glossaire)
# restent en accès secondaire : footer + renvois depuis Méthode et les pages
# concernées (cf. cycle B — audit UX, I1/I2).
# Navigation par intentions (5 entrées) : les catalogues d'acteurs (porteurs,
# usufruitiers, réseaux, modèles), le classement et les revues sont accessibles
# via le hub « Annuaire » et le pied de page — ils ne saturent plus l'en-tête.
NAV = [
    ("index.html", "Accueil"),
    ("carte.html", "Carte"),
    ("dossiers/index.html", "Dossiers"),
    ("classement.html", "Classement"),
    ("methode.html", "Méthode"),
]
# Pages-catalogues dont l'onglet actif est « Classement » (le classement réunit
# toutes les entrées ; les catalogues par rôle restent accessibles via le pied
# de page). L'ancien hub « Annuaire » a été retiré (#11).
CATALOGUE_PAGES = {"lieux.html", "porteurs.html", "usufruitiers.html",
                   "modeles.html", "reseaux.html", "classement.html"}

# URL canonique de base (sans barre oblique finale). Lue depuis concepts.yml.
BASE_URL = "https://communs.actitude.org"


def canonical_url(path):
    """URL absolue d'une page. L'accueil canonicalise vers la racine."""
    if path in ("", "index.html"):
        return BASE_URL + "/"
    return BASE_URL + "/" + path.lstrip("/")


def page(title, body, active, depth=0, project=None, description="",
         path="", jsonld=None, og_type="website", robots=None,
         link_gloss=True, extra_css=None):
    up = "../" * depth
    # liage du glossaire : première occurrence par page des termes pivots
    # (audit pédagogie C, C1). Désactivé sur le glossaire lui-même.
    if link_gloss:
        body = link_glossary(body, up)
    # une page-catalogue (lieux, porteurs…) allume l'onglet « Classement »
    active_nav = "classement.html" if active in CATALOGUE_PAGES else active
    nav_items = []
    for href, label in NAV:
        classes = []
        if href == active_nav:
            classes.append("active")
        if href == "methode.html":      # la référence, mise un peu à part
            classes.append("nav-ref")
        cls = f' class="{" ".join(classes)}"' if classes else ""
        aria = ' aria-current="page"' if href == active_nav else ""
        nav_items.append(f'<a href="{up}{href}"{cls}{aria}>{e(label)}</a>')
    nav = "".join(nav_items)
    pname = project["display_name"] if project else "Terres Libérées"
    mark = project["logo_mark"] if project else "TL"
    base = project["tagline"] if project else ""
    desc = e(meta_desc(description or base))
    canon = canonical_url(path)
    og_img = BASE_URL + "/assets/og-default.svg"
    full_title = f"{title} — {pname}"

    # données structurées JSON-LD
    ld = ""
    for block in (jsonld or []):
        ld += ('\n<script type="application/ld+json">'
               + json.dumps(block, ensure_ascii=False) + "</script>")

    robots_tag = f'\n<meta name="robots" content="{e(robots)}">' if robots else ""

    doc = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#221f1a">{robots_tag}
<link rel="canonical" href="{e(canon)}">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{e(og_type)}">
<meta property="og:site_name" content="{e(pname)}">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{e(canon)}">
<meta property="og:image" content="{e(og_img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(full_title)}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{e(og_img)}">
<link rel="stylesheet" href="{up}assets/style.css">{("".join(chr(10) + '<link rel="stylesheet" href="' + up + 'assets/' + c + '">' for c in (extra_css or [])))}{ld}
</head>
<body>
<a class="skiplink" href="#contenu">Aller au contenu</a>
<header class="masthead">
  <div class="wrap">
    <a class="brand" href="{up}index.html">
      <span class="logo-mark">{e(mark)}</span>
      <span class="brand-txt"><span class="brand-name">{e(pname)}</span>
      <span class="baseline">{e(base)}</span></span>
    </a>
    <nav class="topnav">{nav}</nav>
  </div>
</header>
<main class="wrap" id="contenu">
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <p>{e(pname)} — annuaire critique des montages de libération des terres en
    France. Une évaluation selon un cadre assumé, <a href="{up}methode.html">non un
    label</a>.</p>
    <p class="foot-links"><strong>Découvrir</strong> ·
    <a href="{up}dossiers/index.html">Dossiers</a> ·
    <a href="{up}revues/index.html">Revues</a> ·
    <a href="{up}regimes.html">Régimes et pôles</a> ·
    <a href="{up}glossaire.html">Glossaire</a> ·
    <a href="{up}themes.html">Thèmes</a></p>
    <p class="foot-links"><strong>Explorer</strong> ·
    <a href="{up}carte.html">Carte</a> ·
    <a href="{up}lieux.html">Lieux</a> ·
    <a href="{up}porteurs.html">Porteurs</a> ·
    <a href="{up}usufruitiers.html">Usufruitiers</a> ·
    <a href="{up}reseaux.html">Réseaux</a> ·
    <a href="{up}modeles.html">Modèles voisins</a> ·
    <a href="{up}classement.html">Classement</a> ·
    <a href="{up}comparer.html">Comparer</a></p>
    <p class="foot-links"><strong>Comprendre la note</strong> ·
    <a href="{up}methode.html">Méthode</a> ·
    <a href="{up}ce-que-la-note-ne-dit-pas.html">Ce qu'elle ne dit pas</a> ·
    <a href="{up}faq.html">FAQ</a> ·
    <a href="{up}exemples.html">Exemples calculés</a> ·
    <a href="{up}droit-de-reponse.html">Droit de réponse</a></p>
    <p class="foot-links"><strong>Citer &amp; contribuer</strong> ·
    <a href="{up}methode.html">Méthode</a> ·
    <a href="{up}grilles.html">Grilles d'analyse</a> ·
    <a href="{up}data.json">Données ouvertes (JSON)</a> ·
    <a href="{up}changelog.html">Journal des versions</a> ·
    <a href="{up}suggerer.html">Proposer un lieu</a></p>
    <p>Terres Libérées · v{SITE_VERSION} · {SITE_VERSION_DATE}</p>
    <p>Site statique, généré automatiquement le {e(BUILD_DATE_FR)}.</p>
  </div>
</footer>
</body>
</html>
"""
    # passe typographique française : espaces fines insécables sur le seul
    # texte visible (audit copywriting D, D1). N'affecte ni les balises, ni
    # les URL, ni le JSON-LD (dans <script>), ni les SVG.
    return apply_typo(doc)


# ─────────────────────────────────────────────────────────────────────────────
# Composants
# ─────────────────────────────────────────────────────────────────────────────

def montage_label(mid, concepts):
    if not mid:
        return "—"
    for m in concepts["montages"]:
        if m["id"] == mid:
            return m["label"]
    return mid


def titre_label(tid, concepts):
    """Libellé d'un titre d'articulation (vocabulaire `titres` de concepts.yml)."""
    if not tid:
        return "—"
    for t in concepts.get("titres", []) or []:
        if t["id"] == tid:
            return t["label"]
    return tid


def _entite_lien(uid, by_uid):
    """Nom d'une entité lié à sa fiche, suivi de sa forme juridique si connue."""
    ent = by_uid.get(uid)
    if not ent:
        return e(uid)
    slug = CAT_SLUG.get(ent.get("categorie", ""), "l")
    lien = f'<a href="../{slug}/{uid}.html">{e(ent.get("nom", uid))}</a>'
    fj = clean(ent.get("forme_juridique") or "")
    return f"{lien} ({e(fj)})" if fj else lien


def montage_section(fiche, concepts, by_uid):
    """Section « Le montage » d'une fiche de lieu : silhouette typologique +
    chaîne réelle (porteur, articulations typées, usufruitiers) + liants.
    Dégradation gracieuse si `articulations:` est absent."""
    mont = fiche.get("montage", {}) or {}
    ch = fiche.get("chaine", {}) or {}
    if fiche.get("categorie") != "lieu":
        if mont.get("description"):
            return ('<section><h2 class="sec">Le montage</h2><p class="prose">'
                    + e(clean(mont["description"])) + "</p></section>")
        return ""
    if not mont and not ch:
        return ""
    blocs = []
    # 1 — silhouette typologique
    sil = next((m for m in concepts.get("montages", []) or []
                if m["id"] == mont.get("type")), None)
    if sil:
        if sil.get("en_clair"):
            blocs.append('<p class="enclair">' + e(clean(sil["en_clair"])) + "</p>")
        blocs.append('<p class="prose"><strong>' + e(clean(sil["label"]))
                     + ".</strong> " + e(clean(sil.get("definition", ""))) + "</p>")
    # 2 — la chaîne réelle
    porteurs = ch.get("porteurs") or []
    usufs = ch.get("usufruitiers") or []
    phr = []
    if porteurs:
        phr.append("Le foncier est porté par "
                   + ", ".join(_entite_lien(u, by_uid) for u in porteurs) + ".")
    arts = mont.get("articulations") or []
    if arts:
        for a in arts:
            seg = ("L'usage est confié à "
                   + _entite_lien(a.get("usufruitier"), by_uid)
                   + " par un titre de type « "
                   + e(titre_label(a.get("titre"), concepts)) + " »")
            duree = clean(a.get("duree") or "")
            if duree:
                seg += " (" + e(duree) + ")"
            note = clean(a.get("note") or "")
            seg += (" — " + e(note)) if note else "."
            phr.append(seg)
    elif usufs:
        phr.append("L'usage est confié à "
                   + ", ".join(_entite_lien(u, by_uid) for u in usufs)
                   + " — le titre précis de l'articulation reste à documenter.")
    if phr:
        blocs.append('<p class="prose">' + " ".join(phr) + "</p>")
    # chaîne intégrée
    if set(porteurs) & set(usufs):
        blocs.append('<p class="chaine-note"><strong>Chaîne intégrée :</strong> '
                     "le porteur et l'usufruitier sont une seule et même entité. "
                     "La propriété et l'usage ne sont pas dissociés : le collectif "
                     "n'est pas un locataire précaire, mais il est aussi juge et "
                     "partie, sans contre-pouvoir externe entre les deux rôles.</p>")
    # 3 — liants
    liants = mont.get("liants") or []
    if liants:
        lis = []
        for l in liants:
            txt = "<strong>" + e(clean(l.get("intitule", ""))) + "</strong>"
            niv = clean(l.get("niveau") or "")
            if niv:
                txt += " — niveau " + e(niv)
            portee = clean(l.get("portee") or "")
            if portee:
                txt += ", portée " + e(portee)
            desc = clean(l.get("description") or "")
            if desc:
                txt += " : " + e(desc)
            lis.append("<li>" + txt + "</li>")
        blocs.append('<p class="prose">Éléments qui lient le montage :</p>'
                     '<ul class="prose">' + "".join(lis) + "</ul>")
    # 4 — description libre, en complément
    if mont.get("description"):
        blocs.append('<p class="prose">' + e(clean(mont["description"])) + "</p>")
    if not blocs:
        return ""
    return '<section><h2 class="sec">Le montage</h2>' + "".join(blocs) + "</section>"


def dossier_section(fiche):
    """Section « Dossier » d'une fiche de porteur ou d'usufruitier : les pièces
    du montage et leur statut de publicité (public / non public / inconnu).
    Bloc documentaire de transparence — non noté."""
    if fiche.get("categorie") not in ("porteur", "usufruitier"):
        return ""
    dossier = fiche.get("dossier", {}) or {}
    pieces = dossier.get("pieces") or []
    if not pieces:
        return ""
    types = [("statuts", "Statuts"),
             ("reglement_interieur", "Règlement intérieur"),
             ("charte", "Charte"),
             ("acte_montage", "Acte de montage"),
             ("rapport_financier", "Rapport financier / comptes"),
             ("bail", "Bail / convention d'usage")]
    by_type = {p.get("type"): p for p in pieces if p.get("type")}
    smap = {"public": ("Public", "crit-oui"),
            "non_public": ("Non public", "crit-non"),
            "inconnu": ("Inconnu", "crit-inconnu")}
    trs = []
    for tid, tlabel in types:
        p = by_type.get(tid) or {}
        statut = p.get("statut", "inconnu")
        slab, scls = smap.get(statut, smap["inconnu"])
        cell = slab
        if statut == "public" and p.get("lien"):
            cell += (' — <a href="' + e(p["lien"]) + '" rel="noopener" '
                     'target="_blank">consulter</a>')
        note = clean(p.get("note") or "")
        if note:
            cell += ' <span class="note">(' + e(note) + ')</span>'
        trs.append('<tr><th scope="row">' + e(tlabel) + '</th>'
                   '<td class="' + scls + '">' + cell + "</td></tr>")
    return ('<section><h2 class="sec">Dossier</h2>'
            '<p class="prose">Les pièces du montage et leur accessibilité '
            "publique. Le statut de chaque pièce — publique, non publique ou "
            "inconnu — est lui-même une information.</p>"
            '<div class="table-scroll" tabindex="0" role="region" '
            'aria-label="Dossier — pièces et statut de publicité">'
            '<table class="rank-tbl small">'
            '<thead><tr><th scope="col">Pièce</th>'
            '<th scope="col">Statut</th></tr></thead>'
            "<tbody>" + "".join(trs) + "</tbody></table></div></section>")


def _fmtnum(val):
    """Affiche un nombre sans décimale parasite (90.0 → 90)."""
    if val is None:
        return "—"
    if isinstance(val, float) and val == int(val):
        return str(int(val))
    return str(val)


def axe_legend(axes_cfg, prefix=""):
    """Légende des axes : une pastille colorée + numéro + libellé par axe.
    Itère ranking["axes"] — aucun axe codé en dur."""
    items = "".join(
        f'<span class="axe-dot axe-{ax["id"]}"></span> {ax["id"]} — {e(ax["label"])}'
        for ax in axes_cfg)
    return prefix + items


def axis_bar(axes_cfg, axes_scores, compact=False):
    """Barres horizontales des cinq axes — lecture chiffrée précise."""
    rows = []
    for ax in axes_cfg:
        aid = ax["id"]
        val = axes_scores.get(aid)
        col = ax["couleur"]
        if val is None:
            w, txt, cls = 0, "n.r.", "axis-na"
        else:
            w, txt, cls = _fmtnum(val), _fmtnum(val), ""
        rows.append(f"""<div class="axis-row">
  <span class="axis-label">{e(ax['id'])} · {e(ax['label'])}</span>
  <span class="axis-track"><span class="axis-fill {cls}" style="width:{w}%;background:{col}"></span></span>
  <span class="axis-val">{e(txt)}</span>
</div>""")
    cls = "axis-block compact" if compact else "axis-block"
    return f'<div class="{cls}">' + "".join(rows) + "</div>"


# ── Pentagone de profil à cinq axes (radar SVG inline) ───────────────────────

_TRI_SIZE = 120  # taille de référence du SVG pentagone (viewBox)


def _penta_geom(axes_cfg, size=_TRI_SIZE):
    """Sommets du radar : un par axe, répartis régulièrement sur un cercle,
    l'axe 1 en haut. Renvoie (centre, {axe_id: (x, y)})."""
    cx, cy = size / 2, size / 2
    r = size * 0.40
    n = len(axes_cfg)
    verts = {}
    for i, ax in enumerate(axes_cfg):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        verts[ax["id"]] = (cx + r * math.cos(ang), cy + r * math.sin(ang))
    return (cx, cy), verts


def _penta_profile_points(axes_cfg, axes_scores, size=_TRI_SIZE):
    """Renvoie (points du polygone de profil, liste des axes manquants)."""
    (gx, gy), verts = _penta_geom(axes_cfg, size)
    pts, missing = [], []
    for ax in axes_cfg:
        aid = ax["id"]
        v = axes_scores.get(aid)
        vx, vy = verts[aid]
        if v is None:
            missing.append(aid)
            f = 0.0
        else:
            f = max(0.0, min(1.0, v / 100))
        pts.append(f"{gx + (vx - gx) * f:.1f},{gy + (vy - gy) * f:.1f}")
    return pts, missing


def tri_defs(axes_cfg, size=_TRI_SIZE):
    """Bloc <defs> commun à tous les pentagones compacts d'une page : cadre,
    grille intermédiaire, sommets et numéros d'axes — la seule part qui varie
    ensuite est le polygone de profil (factorisation, audit performance B-1)."""
    (gx, gy), verts = _penta_geom(axes_cfg, size)
    col = {ax["id"]: ax["couleur"] for ax in axes_cfg}
    frame = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts.values())
    mid = " ".join(f"{gx + (x - gx) * 0.5:.1f},{gy + (y - gy) * 0.5:.1f}"
                   for x, y in verts.values())
    dots = ""
    for ax in axes_cfg:
        aid = ax["id"]
        vx, vy = verts[aid]
        # léger décalage radial du numéro pour le sortir du sommet
        lx = gx + (vx - gx) * 1.16
        ly = gy + (vy - gy) * 1.16
        dots += (f'<circle class="tri-vtx" cx="{vx:.1f}" cy="{vy:.1f}" '
                 f'r="3" fill="{col[aid]}"/>'
                 f'<text class="tri-lab" x="{lx:.1f}" y="{ly:.1f}">{aid}</text>')
    return (f'<svg width="0" height="0" aria-hidden="true" '
            f'style="position:absolute" focusable="false"><defs>'
            f'<g id="tri-base">'
            f'<polygon class="tri-frame" points="{frame}"/>'
            f'<polygon class="tri-grid" points="{mid}"/>'
            f'{dots}</g></defs></svg>')


def axis_triangle(axes_cfg, axes_scores, size=_TRI_SIZE, compact=False):
    """SVG pentagone de profil à cinq axes (radar).

    En mode `compact` (cartes / chips) : ne rend que le polygone variable et
    référence le cadre commun via <use href="#tri-base"> — la part fixe est
    factorisée par `tri_defs()` une fois par page.
    En pleine taille (fiche) : SVG autonome avec cadre, repère d'échelle et
    aria-label — seule source accessible du profil chiffré.
    """
    (gx, gy), verts = _penta_geom(axes_cfg, size)
    col = {ax["id"]: ax["couleur"] for ax in axes_cfg}
    pts, missing = _penta_profile_points(axes_cfg, axes_scores, size)
    label = "Profil des six questions — " + ", ".join(
        f"{ax['label']} "
        f"{_fmtnum(axes_scores.get(ax['id'])) if axes_scores.get(ax['id']) is not None else 'non renseigné'}"
        for ax in axes_cfg)
    vb = f"0 0 {size} {size}"

    # profil dégénéré : à partir de 2 axes non renseignés, plusieurs sommets se
    # confondent au centre et le polygone devient auto-sécant. On ne trace alors
    # pas la zone remplie — seulement le cadre et une mention « profil
    # incomplet ». Les barres d'axe chiffrées, elles, restent inchangées.
    degenere = (len(axes_cfg) - len(missing)) < 3

    # arêtes du polygone : hachurer celles qui touchent un sommet absent (None)
    # pour signaler une donnée indéterminée plutôt qu'un score nul.
    edge_lines = ""
    if missing and not degenere:
        n = len(axes_cfg)
        for i, ax in enumerate(axes_cfg):
            a = ax["id"]
            b = axes_cfg[(i + 1) % n]["id"]
            if a in missing or b in missing:
                pa, pb = pts[i], pts[(i + 1) % n]
                edge_lines += (f'<line class="tri-edge-na" x1="{pa.split(",")[0]}" '
                               f'y1="{pa.split(",")[1]}" x2="{pb.split(",")[0]}" '
                               f'y2="{pb.split(",")[1]}"/>')

    if compact:
        # décoratif : la carte porte nom + palier + anneau ; le détail chiffré
        # est sur la fiche liée. <use> du cadre commun, polygone variable seul.
        # Profil dégénéré : cadre seul + libellé « profil incomplet ».
        if degenere:
            return (f'<svg class="tri compact tri-incomplet" viewBox="{vb}" '
                    f'role="img" focusable="false" aria-label="{e(label)} '
                    f'— profil incomplet">'
                    f'<use href="#tri-base"/>'
                    f'<text class="tri-incomplet-txt" x="{gx:.1f}" y="{gy:.1f}">'
                    f'profil incomplet</text></svg>')
        return (f'<svg class="tri compact" viewBox="{vb}" '
                f'role="img" focusable="false" aria-label="{e(label)}">'
                f'<use href="#tri-base"/>'
                f'<polygon class="tri-fill" points="{" ".join(pts)}"/>'
                f'{edge_lines}</svg>')

    # pleine taille (fiche) — SVG autonome avec cadre + repère d'échelle.
    frame = " ".join(f"{x:.1f},{y:.1f}" for x, y in verts.values())
    mid = " ".join(f"{gx + (x - gx) * 0.5:.1f},{gy + (y - gy) * 0.5:.1f}"
                   for x, y in verts.values())
    dots = ""
    for ax in axes_cfg:
        aid = ax["id"]
        vx, vy = verts[aid]
        na = " tri-na" if aid in missing else ""
        lx = gx + (vx - gx) * 1.17
        ly = gy + (vy - gy) * 1.17
        dots += (f'<circle class="tri-vtx{na}" cx="{vx:.1f}" cy="{vy:.1f}" '
                 f'r="4" fill="{col[aid]}"/>'
                 f'<text class="tri-lab" x="{lx:.1f}" y="{ly:.1f}">{aid}</text>')
    # repère d'échelle : « 100 » au sommet de l'axe 1, « 0 » au centre.
    a1x, a1y = verts[axes_cfg[0]["id"]]
    scale = (f'<text class="tri-scale" x="{a1x:.1f}" y="{a1y - 6:.1f}">100</text>'
             f'<text class="tri-scale" x="{gx:.1f}" y="{gy + 9:.1f}">0</text>')
    # profil dégénéré : cadre + sommets + repère, mais ni zone remplie ni
    # arêtes hachurées — le polygone serait auto-sécant. Mention explicite.
    fill = ("" if degenere
            else f'<polygon class="tri-fill" points="{" ".join(pts)}"/>')
    incomplet = ""
    if degenere:
        incomplet = (f'<text class="tri-incomplet-txt" x="{gx:.1f}" '
                     f'y="{gy:.1f}">profil incomplet</text>')
    aria = e(label) + (" — profil incomplet" if degenere else "")
    return (f'<svg class="tri" viewBox="{vb}" '
            f'role="img" aria-label="{aria}">'
            f'<polygon class="tri-frame" points="{frame}"/>'
            f'<polygon class="tri-grid" points="{mid}"/>'
            f'{fill}'
            f'{edge_lines}{dots}{scale}{incomplet}</svg>')


# ── Badge d'Indice : anneau de progression SVG ───────────────────────────────

def idl_badge(sc, big=False):
    """Anneau de progression. Le SVG est décoratif (aria-hidden) : l'indice et le
    palier sont déjà disponibles en texte, doublés d'un libellé masqué accessible."""
    idl = sc["idl"]
    pal = sc["palier"]
    if idl is None or pal is None:
        return ('<span class="idl-badge idl-na">n.r.'
                '<span class="visually-hidden">Note non renseignée</span></span>')
    estime = sc.get("score_type") == "estime"
    r, sw = (34, 7) if big else (16, 4)
    c = 2 * math.pi * r
    off = c * (1 - idl / 100)
    box = (r + sw) * 2
    cls = "idl-badge big" if big else "idl-badge"
    if estime:
        cls += " idl-estime"
    pal_lab = e(pal["label"]) + (" · estimé" if estime else "")
    num_sz = "1.6rem" if big else ".82rem"
    sr = (f'<span class="visually-hidden">Note de libération {idl} sur 100, '
          f'{e(pal["label"])}{" (estimé)" if estime else ""}.</span>')
    return (
        f'<span class="{cls}" style="--pal:{pal["couleur"]}">'
        f'<svg class="idl-ring" viewBox="0 0 {box} {box}" aria-hidden="true" '
        f'focusable="false">'
        f'<circle class="idl-track" cx="{box / 2}" cy="{box / 2}" r="{r}" '
        f'stroke-width="{sw}"/>'
        f'<circle class="idl-arc" cx="{box / 2}" cy="{box / 2}" r="{r}" '
        f'stroke-width="{sw}" stroke-dasharray="{c:.1f}" '
        f'stroke-dashoffset="{off:.1f}" '
        f'transform="rotate(-90 {box / 2} {box / 2})"/>'
        f'<text class="idl-num" x="{box / 2}" y="{box / 2}" '
        f'style="font-size:{num_sz}">{idl}</text>'
        f'</svg>{sr}'
        f'<span class="idl-pal">{pal_lab}</span></span>')


def idl_scale(sc, ranking):
    """Jauge linéaire 0-100 avec bandes de palier et curseur (panneau de score)."""
    idl = sc["idl"]
    if idl is None:
        return ""
    paliers = sorted(ranking["paliers"], key=lambda p: p["min"])
    segs = ""
    for i, p in enumerate(paliers):
        left = p["min"]
        right = paliers[i + 1]["min"] if i + 1 < len(paliers) else 100
        segs += (f'<span class="idl-seg" style="left:{left}%;'
                 f'width:{right - left}%;background:{p["couleur"]}" '
                 f'title="{e(p["label"])} (≥ {p["min"]})"></span>')
    brut = sc.get("idl_brut")
    ghost = ""
    if brut is not None and brut != idl:
        ghost = (f'<span class="idl-ghost" style="left:{brut}%" '
                 f'title="Indice brut {brut}, avant pénalité de complétude"></span>')
    # curseur et marqueur « indice brut » placés HORS de la piste (qui est en
    # overflow:hidden) pour ne pas être rognés — chantier 7.
    return (f'<div class="idl-scale" aria-hidden="true">'
            f'<span class="idl-scale-track">{segs}</span>'
            f'{ghost}'
            f'<span class="idl-cursor" style="left:{idl}%"></span>'
            f'<span class="idl-scale-ends"><span>0</span><span>100</span></span>'
            f'</div>')


def corpus_histogram(all_sc, ranking=None):
    """Histogramme de la distribution des entrées par palier de libération (v3.1)."""
    order=["marchand","en_transition","sorti_du_marche","autogere","usage_decommodifie","commun_vivant"]
    short={"marchand":"marchand","en_transition":"transition","sorti_du_marche":"sorti","autogere":"autogéré","usage_decommodifie":"usage","commun_vivant":"commun"}
    counts={b:0 for b in order}
    for f, s in all_sc:
        if f.get("categorie")=="modele":
            continue
        pal=s.get("palier")
        if pal and pal.get("id") in counts:
            counts[pal["id"]]+=1
    total=sum(counts.values()); mx=max(counts.values()) or 1
    susp_n=sum(1 for f,s in all_sc if f.get("categorie")!="modele" and (s.get("palier")) and s.get("idl") is None)
    W,H,pad=480,180,30
    bw=(W-2*pad)/len(order)
    bars=""
    for i,b in enumerate(order):
        n=counts[b]
        bh=(H-2*pad-14)*n/mx
        x=pad+i*bw; y=H-pad-bh
        bars+=(f'<rect class="hg-bar" x="{x+8:.1f}" y="{y:.1f}" '
               f'width="{bw-16:.1f}" height="{max(bh,0.5):.1f}" fill="{FB_HEX[b]}" rx="2"/>'
               f'<text class="hg-n" x="{x+bw/2:.1f}" y="{y-5:.1f}">{n}</text>'
               f'<text class="hg-l" x="{x+bw/2:.1f}" y="{H-pad+13:.1f}">{e(short[b])}</text>')
    return (f'<figure class="corpus-hist"><svg viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Répartition des {total} entrées situées sur l\'échelle de libération">{bars}</svg>'
            f'<figcaption>Répartition des {total} entrées situées sur l\'échelle, par palier '
            f'(dont {susp_n} suspendues, sans note chiffrée ; modèles voisins exclus).</figcaption></figure>')
def grille_recap(criteres_evalues, gril, axes_cfg):
    """Bandeau récapitulatif : part de oui/partiel/non/inconnu par axe."""
    order = ["oui", "partiel", "non", "inconnu"]
    olab = {"oui": "oui", "partiel": "partiel", "non": "non", "inconnu": "inconnu"}
    seg_col = {"oui": "var(--green)", "partiel": "var(--gold)",
               "non": "var(--terra)", "inconnu": "#cfc6b0"}
    rows = ""
    for ax in axes_cfg:
        crit_ids = [cr["id"] for fam in gril.get("familles", [])
                    for cr in fam["criteres"] if cr["axe"] == ax["id"]]
        if not crit_ids:
            continue
        tally = {k: 0 for k in order}
        for cid in crit_ids:
            ev = criteres_evalues.get(cid)
            tally[ev["valeur"] if ev else "inconnu"] += 1
        tot = sum(tally.values()) or 1
        segs, txt = "", []
        for k in order:
            if not tally[k]:
                continue
            segs += (f'<span class="rk-seg" style="width:{tally[k] / tot * 100:.1f}%;'
                     f'background:{seg_col[k]}" title="{tally[k]} {olab[k]}"></span>')
            txt.append(f"{tally[k]} {olab[k]}")
        rows += (f'<div class="rk-row"><span class="rk-ax">'
                 f'<span class="axe-dot axe-{ax["id"]}" aria-hidden="true"></span>'
                 f'{ax["id"]} · {e(ax["label"])}</span>'
                 f'<span class="rk-bar" aria-hidden="true">{segs}</span>'
                 f'<span class="rk-txt">{e(" · ".join(txt))}</span></div>')
    return f'<div class="grille-recap">{rows}</div>'


def card(fiche, sc, axes_cfg, depth=0, concepts=None):
    up = "../" * depth
    cat = fiche["categorie"]
    href = f'{up}{CAT_SLUG[cat]}/{fiche["uid"]}.html'
    loc = ""
    region = ""
    if fiche.get("localisation"):
        l = fiche["localisation"]
        loc = " · ".join(x for x in [l.get("commune"), l.get("departement")] if x)
        region = l.get("region", "") or ""
    elif fiche.get("forme_juridique"):
        loc = clean(fiche["forme_juridique"])
    if not loc:
        loc = "Réseau national" if cat in ("lieu", "reseau") \
            else (fiche.get("pays") or "—")
    catlabel = {"lieu": "Lieu", "porteur": "Porteur",
                "usufruitier": "Usufruitier", "modele": "Modèle voisin",
                "reseau": "Réseau"}.get(cat, cat)
    # attributs data-* pour tri / filtres
    mont = fiche.get("montage", {}) or {}
    montage_id = mont.get("type", "") or ""
    montage_lab = montage_label(montage_id, concepts) if (montage_id and concepts) else ""
    pal_id = sc["palier"]["id"] if sc["palier"] else ""
    ax = sc["axes"]
    ax_attrs = " ".join(f'data-ax{aid}="{ax.get(aid) or 0}"' for aid in ax)
    data = (f'data-idl="{sc["idl"] or 0}" data-nom="{e(fiche["nom"])}" '
            f'data-palier="{e(pal_id)}" data-region="{e(region)}" '
            f'data-montage="{e(montage_id)}" {ax_attrs}')
    return f"""<li class="card" {data}>
  <div class="card-head">
    <span class="tag tag-{cat}">{catlabel}</span>
    {idl_badge(sc)}
  </div>
  <h3><a class="card-link" href="{href}">{e(fiche['nom'])}</a>{ctx_labels_html(fiche, up)}</h3>
  <p class="card-sub">{e(clean(fiche.get('sous_titre','')))}</p>
  <p class="card-meta">{e(loc)}{(' · ' + e(montage_lab)) if montage_lab else ''}</p>
  {f'<div class="card-viz">{axis_triangle(Q6_CFG, sc["q6"], compact=True)}</div>' if sc.get("q6") else ''}
</li>"""


def cards_grid(fiches_sc, axes_cfg, depth=0, concepts=None, grid_id=""):
    items = "".join(card(f, sc, axes_cfg, depth, concepts) for f, sc in fiches_sc)
    attr = f' id="{grid_id}"' if grid_id else ""
    return f'<ul class="cards"{attr}>{items}</ul>'


# ─────────────────────────────────────────────────────────────────────────────
# Pages — fiche détaillée
# ─────────────────────────────────────────────────────────────────────────────

def integrite_label(niv, ranking):
    """Libellé et sens d'un niveau d'intégrité du montage. Lit la nouvelle
    section `integrite_montage` ; tolère l'absence de niveau."""
    im = ranking.get("integrite_montage", {}) or {}
    for n in im.get("niveaux", []) or []:
        if n["id"] == niv:
            return n["label"], n.get("sens", "")
    return niv or "—", ""


# Repli compatibilité : ancien nom de fonction.
def purete_label(niv, ranking):
    return integrite_label(niv, ranking)


def nature_label(nid, concepts):
    """Libellé de l'axe de lucrativité `nature_interet` (chantier 1bis)."""
    if not nid:
        return "—"
    for n in concepts.get("nature_interet", []) or []:
        if n["id"] == nid:
            return n["label"]
    return nid


# ── Dérivation relationnelle de la nature agricole (A1, session #10) ─────────
# Un maillon `exploitation_agricole` (GAEC/EARL/SCEA exploitante) ne capte pas
# le fonds — donc plafonne à `hybride` — UNIQUEMENT s'il est PRENEUR d'un bail
# sécurisé SOUS un (ou des) porteur(s) hors-marché et n'est pas intégré à la
# propriété. Sinon (détient, intègre, sans bail, ou porteur non hors-marché), il
# capte le fonds et se lit `commerciale` → `marchand`. Cf. taf/spec-A1-implementation.md §3.
_BAIL_TITRES_SECURISES = {
    "bail_rural", "bail_emphyteotique", "bail_reel_solidaire", "bail_a_construction",
    # commodat (prêt à usage, gratuit par nature — art. 1875 C. civ.) : créditant
    # SOUS porteur hors-marché — la gratuité + un porteur hors-marché l'emportent
    # sur la précarité du titre (décision #11, cas Villarceaux/FPH). La condition
    # `porteurs_hors_marche` reste exigée plus bas, donc un commodat sous porteur
    # marchand resterait, lui, non créditant.
    "commodat",
}
# `convention` (titre générique vague) = usage précaire, non créditant.
_PORTEUR_HORS_MARCHE = {
    "non_lucrative", "commerciale_desactivee", "commerciale_encadree",
}


def compute_verdict(fiche, by_uid):
    """Verdict calculé d'un lieu — `marchand` / `hybride` / `sanctuaire`, ou None
    si la chaîne comporte un maillon de nature non établie. Jamais saisi (L11) : il
    se déduit de la nature_interet de chaque maillon (dérivée relationnellement pour
    l'exploitation agricole), de l'irréversibilité du foncier et des co-gates du
    sommet. Cf. conception-refonte-3.md §13 et taf/spec-A1-implementation.md."""
    if fiche.get("categorie") != "lieu":
        return None
    ch = fiche.get("chaine", {}) or {}
    porteurs = list(ch.get("porteurs") or [])
    usufs = list(ch.get("usufruitiers") or [])
    maillons = porteurs + usufs
    if not maillons:
        return None
    # titre d'articulation par usufruitier (seconde couche du montage)
    titre_par_usuf = {}
    for a in (fiche.get("montage", {}) or {}).get("articulations") or []:
        u = a.get("usufruitier")
        if u:
            titre_par_usuf[u] = a.get("titre")
    integ = set(porteurs) & set(usufs)
    porteurs_natures = [((by_uid.get(p) or {}).get("nature_interet") or "inconnu")
                        for p in porteurs]
    porteurs_hors_marche = bool(porteurs) and all(
        n in _PORTEUR_HORS_MARCHE for n in porteurs_natures)
    # nature EFFECTIVE de chaque maillon (dérivation relationnelle de l'agricole)
    effectives = []
    for u in maillons:
        nat = (by_uid.get(u) or {}).get("nature_interet") or "inconnu"
        if nat == "exploitation_agricole":
            titre = titre_par_usuf.get(u)
            preneur_securise = (u not in integ
                                and titre in _BAIL_TITRES_SECURISES
                                and porteurs_hors_marche)
            # défaut prudent : sans bail sécurisé sous porteur hors-marché, le
            # maillon capte le fonds → commerciale (décision #10).
            nat = "exploitation_agricole" if preneur_securise else "commerciale"
        effectives.append(nat)
    if any(n in ("commerciale", "privee_individuelle") for n in effectives):
        return "marchand"
    # exploitation_agricole et commerciale_encadree plafonnent à hybride : jamais
    # le sommet (appropriation du bénéfice / intérêt privé encadré — décision #9).
    if any(n in ("commerciale_encadree", "exploitation_agricole") for n in effectives):
        return "hybride"
    if any(n == "inconnu" for n in effectives):
        return None  # chaîne non entièrement établie — verdict à établir
    # chaîne entièrement non_lucrative / commerciale_desactivee → candidate au
    # sommet : les co-gates observables doivent TOUS être au vert (sinon hybride).
    g = {c.get("critere"): c.get("valeur") for c in (fiche.get("grille") or [])}
    foncier = (g.get("foncier_hors_marche") == "oui"
               and g.get("irreversibilite") == "oui")
    vivant = (g.get("vivant_finalite") == "oui"
              and g.get("place_au_vivant") == "oui")
    regeneration = g.get("milieu_protege") == "oui"          # face opposable (option a)
    finalite = (g.get("usage_non_marchand") in ("oui", "partiel")
                and g.get("usage_interet_general") == "oui")
    # travail décommodifié — proxy UNIDIRECTIONNEL (mini-strats #10) : seul un
    # salariat de marché CONSTATÉ sur le travail-cœur (`non`) ferme le sommet ;
    # `oui`/`partiel`/`inconnu`/absent sont neutres — on ne bloque jamais le
    # sommet par le seul silence d'un critère peu peuplé. Teste la FORME salariale
    # (marchandise-travail, Polanyi), pas la subordination ni la propriété du
    # capital : une SCOP qui salarie reste « non » ; le don/troc/GAEC reste « oui ».
    travail_non_march = g.get("travail_non_marchandise") != "non"
    sommet = foncier and vivant and regeneration and finalite and travail_non_march
    return "sanctuaire" if sommet else "hybride"


def verdict_badge(vid, concepts):
    """Badge du verdict d'un lieu. vid None → verdict non encore établi."""
    if not vid:
        return ('<span class="verdict verdict-na" title="Verdict suspendu : il '
                'manque une pièce — la nature d\'au moins un maillon de la chaîne '
                'n\'est pas encore documentée.">Verdict suspendu</span>')
    for d in (concepts.get("verdict", {}) or {}).get("degres", []) or []:
        if d["id"] == vid:
            # infobulle : version « en clair » (claire et préserve les cas) ;
            # `definition` reste le texte canonique long affiché sur Méthode/Glossaire.
            tip = d.get("en_clair") or d.get("definition", "")
            return (f'<span class="verdict verdict-{e(vid)}" '
                    f'title="{e(clean(tip))}">'
                    f'{e(d["label"])}</span>')
    return ""


def compute_chain_context(fiches, by_uid):
    """Attache à chaque fiche un champ `_ctx` — la liste des entités de contexte
    de chaîne à montrer en étiquettes grisées (session #4, UI). Un lieu montre
    ses porteurs ; un usufruitier, les porteurs des lieux où il intervient ; un
    porteur, les réseaux dont il est membre."""
    usuf_porteurs = {}
    for f in fiches:
        if f["categorie"] != "lieu":
            continue
        ch = f.get("chaine", {}) or {}
        ports = ch.get("porteurs") or []
        for u in (ch.get("usufruitiers") or []):
            lst = usuf_porteurs.setdefault(u, [])
            for p in ports:
                if p not in lst:
                    lst.append(p)
    membre_reseaux = {}
    for f in fiches:
        if f["categorie"] != "reseau":
            continue
        for m in (f.get("membres") or []):
            lst = membre_reseaux.setdefault(m, [])
            if f["uid"] not in lst:
                lst.append(f["uid"])

    def lab(uid, kind, owner):
        ent = by_uid.get(uid)
        if not ent or uid == owner:
            return None
        return {"kind": kind, "uid": uid, "nom": ent.get("nom", uid),
                "slug": CAT_SLUG.get(ent.get("categorie", ""), "l")}

    for f in fiches:
        cat, uid = f["categorie"], f["uid"]
        ctx = []
        if cat == "lieu":
            for p in ((f.get("chaine", {}) or {}).get("porteurs") or []):
                x = lab(p, "porteur", uid)
                if x and x not in ctx:
                    ctx.append(x)
        elif cat == "usufruitier":
            for p in usuf_porteurs.get(uid, []):
                x = lab(p, "porteur", uid)
                if x and x not in ctx:
                    ctx.append(x)
        elif cat == "porteur":
            for r in membre_reseaux.get(uid, []):
                x = lab(r, "reseau", uid)
                if x and x not in ctx:
                    ctx.append(x)
        f["_ctx"] = ctx


def ctx_labels_html(fiche, up=""):
    """Étiquettes grisées de contexte de chaîne (porteur, réseau)."""
    ctx = fiche.get("_ctx") or []
    if not ctx:
        return ""
    pre = {"porteur": "Porteur", "reseau": "Réseau"}
    parts = []
    for c in ctx:
        p = pre.get(c["kind"], "")
        parts.append(
            f'<a class="ctx-lab ctx-{e(c["kind"])}" '
            f'href="{up}{c["slug"]}/{e(c["uid"])}.html" '
            f'title="{p} : {e(c["nom"])}">'
            f'<span class="ctx-k">{p}</span>&nbsp;{e(c["nom"])}</a>')
    return '<span class="ctx-labs">' + "".join(parts) + "</span>"


def render_fiche(fiche, sc, cfg, by_uid, sc_by_uid):
    concepts = cfg["concepts"]["concept_central"]
    project = cfg["concepts"]["project"]
    ranking = cfg["ranking"]
    axes_cfg = ranking["axes"]
    grilles = cfg["grilles"]["grilles"]
    cat = fiche["categorie"]
    catlabel = {"lieu": "Lieu", "porteur": "Porteur de nue-propriété",
                "usufruitier": "Organisme usufruitier",
                "modele": "Modèle voisin"}[cat]

    # verdict calculé du lieu — badge dans l'entête (chantier 1bis)
    verdict_html = ""
    if cat == "lieu":
        verdict_html = "\n  " + verdict_badge(compute_verdict(fiche, by_uid),
                                              cfg["concepts"])
    # --- v3.1 : si le lieu porte un bloc evaluation, on réalimente les composants existants ---
    _ev_lieu = fiche.get("evaluation") if cat == "lieu" else (porteur_eval(fiche, by_uid) if cat in ("porteur","usufruitier","reseau") else None)
    _is_porteur = (cat == "porteur" and _ev_lieu is not None)
    _is_group = (cat in ("porteur","usufruitier","reseau") and _ev_lieu is not None)
    _BAND_COL = {"marchand":"#9a9a9a","en_transition":"#a86a4a","sorti_du_marche":"#b08a3e",
                 "autogere":"#3d7a4e","usage_decommodifie":"#2f6e8f","commun_vivant":"#224477"}
    if _ev_lieu:
        _band,_susp,_pf,_badge,_num = _fsc_derive(_ev_lieu)
        _bcol = _BAND_COL[_band]
        _sc_v3 = {"idl": (None if _susp else _num),
                  "palier": {"label": FB_LABEL[_band], "couleur": _bcol},
                  "idl_brut": None, "score_type": "calcule"}
        _ranking_v3 = {"paliers":[
            {"min":0,"couleur":_BAND_COL["marchand"],"label":"marchand"},
            {"min":20,"couleur":_BAND_COL["sorti_du_marche"],"label":"sorti du marché"},
            {"min":50,"couleur":_BAND_COL["autogere"],"label":"autogéré"},
            {"min":75,"couleur":_BAND_COL["usage_decommodifie"],"label":"usage libéré"},
            {"min":90,"couleur":_BAND_COL["commun_vivant"],"label":"commun vivant"}]}
        _NUMS=["1","2","3","4","5","6"]
        _QCOL={"milieu":"#6b8f71","vivant":"#3d7a4e","ouverture":"#4a6b8a","don":"#b08a3e","duree":"#8a6db0","voix":"#bc5d3a"}
        _qv={"oui":100,"partiel":50,"non":0}
        _q_cfg=[{"id":_NUMS[i],"label":Q_LABEL[i][1],"couleur":_QCOL[Q_LABEL[i][0]]} for i in range(6)]
        _q_scores={_NUMS[i]: _qv.get(_ev_lieu["questions"][Q_LABEL[i][0]]["valeur"]) for i in range(6)}
        _mtype = (fiche.get("montage") or {}).get("type")
        verdict_html = ('\n  <span class="tag tag-montage">'
                        + e(montage_label(_mtype, cfg["concepts"])) + '</span>') if _mtype else ""
        if _is_porteur:
            _pctx = porteur_porte_context(fiche)
            verdict_html = '\n  <span class="tag tag-montage">' + e(_pctx["label"]) + '</span>'



    # fil d'Ariane complet : Accueil › Catégorie › Fiche
    head = f"""<nav class="crumb" aria-label="Fil d'Ariane">
  <a href="../index.html">Accueil</a> ›
  <a href="../{CAT_PAGE[cat]}">{e(catlabel)}</a> ›
  <span aria-current="page">{e(fiche['nom'])}</span>
</nav>
<div class="fiche-head">
  <span class="tag tag-{cat}">{e(catlabel)}</span>{verdict_html}
  <h1>{e(fiche['nom'])}{ctx_labels_html(fiche, "../")}</h1>
  <p class="fiche-sub">{e(clean(fiche.get('sous_titre', '')))}</p>
</div>"""
    sub = clean(fiche.get("sous_titre", ""))

    # bloc score — triangle de profil + barres chiffrées + jauge linéaire
    flabel, fcls = fiabilite_label(sc["completude"], ranking)
    # écart indice intrinsèque / effectif — chaîne (porteurs et usufruitiers).
    axe_name = {a["id"]: a["label"] for a in axes_cfg}
    idl_intr = sc.get("idl_intr")
    n_chaine = len(sc.get("chaine_uids", []) or [])
    # une chaîne contamine si elle abaisse au moins un axe (intrinsèque → effectif)
    contamine = (cat in ("porteur", "usufruitier") and idl_intr is not None
                 and sc["idl"] is not None and n_chaine > 0
                 and sc["idl"] != idl_intr)

    def _lien_pluriel(n):
        return f"{n} lieu relié" if n == 1 else f"{n} lieux reliés"

    # 1.4 — les annotations de plafond (note de chaîne, indice brut « ghost »,
    # pénalité de complétude) sont collectées ici puis regroupées sous une seule
    # ligne repliable « Plafonds appliqués » (voir plus bas). Le contenu et les
    # valeurs sont inchangés : on ne fusionne que la zone d'affichage.
    # `comp` reste la ligne de complétude factuelle, toujours visible.
    plafonds = []  # phrases de plafonnement collectées
    comp = ""
    if sc["completude"] is not None:
        comp = (f'<p class="completude">Grille renseignée à '
                f'{round(sc["completude"] * 100)} %.</p>')
        if not contamine and sc.get("idl_brut") is not None \
                and sc["idl_brut"] != sc["idl"]:
            plafonds.append(
                f'<strong>Complétude.</strong> Indice brut {sc["idl_brut"]}, '
                f'ramené à {sc["idl"]} après pénalité de complétude.')

    # note de chaîne — une seule chaîne causale : intrinsèque → axes contaminés
    # par les lieux reliés → effectif (la pénalité de complétude mentionnée une
    # fois ici en cas de contamination).
    if cat in ("porteur", "usufruitier") and idl_intr is not None \
            and sc["idl"] is not None:
        renvoi = (' <a class="chaine-renvoi" href="../methode.html#chaine">'
                  'Comment la chaîne entre dans la note →</a>')
        if n_chaine == 0:
            plafonds.append('<strong>Chaîne.</strong> Aucun lieu relié dans '
                            'l\'annuaire : la note replacée dans les chaînes égale '
                            'la note propre.' + renvoi)
        elif not contamine:
            plafonds.append(f'<strong>Chaîne.</strong> Note propre et note '
                            f'replacée dans les chaînes identiques ({sc["idl"]}) : '
                            f'les {_lien_pluriel(n_chaine)} n\'abaissent aucun '
                            f'axe.{renvoi}')
        else:
            # axes réellement abaissés : comparaison intrinsèque / effectif
            axes_intr = sc.get("axes_intr", {}) or {}
            baisses = []
            for aid in (a["id"] for a in axes_cfg):
                vi = axes_intr.get(aid)
                ve = sc["axes"].get(aid)
                if vi is not None and ve is not None and ve < vi:
                    baisses.append(f"l'axe {aid} ({axe_name[aid].lower()}) "
                                   f"est ramené de {vi} à {ve}")
            if len(baisses) == 1:
                axes_phrase = baisses[0]
            elif baisses:
                axes_phrase = (", ".join(baisses[:-1]) + " et " + baisses[-1])
            else:
                axes_phrase = ""
            comp_phrase = ""
            if sc.get("idl_brut") is not None and sc["idl_brut"] != sc["idl"]:
                comp_phrase = (" La note replacée intègre aussi la pénalité de "
                               "complétude.")
            plafonds.append(f'<strong>Chaîne.</strong> Note propre '
                            f'{idl_intr}, ramenée à <strong>{sc["idl"]}</strong> '
                            f'une fois replacée dans ses chaînes : par les '
                            f'{_lien_pluriel(n_chaine)}, '
                            f'{axes_phrase}.{comp_phrase}{renvoi}')

    # plafond de chaîne sur l'axe 2 d'un lieu (session #5) — annotation visible
    # pour rendre lisible la sanction du verdict marchand ou hybride sur l'axe
    # 2 du lieu (L11 : un calcul n'est utile que si son écart à la saisie est
    # affiché et expliqué).
    if cat == "lieu" and sc.get("ax2_plafond") is not None:
        nat = sc.get("ax2_nature_pire") or "inconnu"
        nat_lbl = nature_label(nat, cfg["concepts"]).lower()
        plafonds.append(
            f'<strong>Maillon limitant.</strong> La structure ne peut être notée '
            f'plus haut que <strong>{sc["ax2_plafond"]}</strong> : un maillon de '
            f'la chaîne — « {e(nat_lbl)} » — l\'en empêche, quels que soient les '
            f'critères cochés. '
            f'<a class="chaine-renvoi" href="../methode.html#chaine">'
            f'Comment la chaîne entre dans la note →</a>')

    # pour un lieu sans contamination de chaîne mais avec pénalité de complétude :
    # la phrase de complétude est déjà dans `plafonds` (cas `not contamine` ci-dessus).
    if _ev_lieu or sc.get("idl") is None:
        comp = ""
    plafonds_html = ""
    if plafonds and not _ev_lieu and sc.get("idl") is not None:
        items = "".join(f"<li>{p}</li>" for p in plafonds)
        plafonds_html = (
            '<details class="plafonds-fold"><summary>Plafonds appliqués '
            f'({len(plafonds)})</summary><ul class="plafonds-list">{items}</ul>'
            '</details>')

    # nombre d'axes effectivement renseignés : l'Indice est leur moyenne
    # géométrique. En deçà de 5, on le signale — information distincte de la
    # complétude des critères.
    n_axes = len(axes_cfg)
    n_axes_calc = sum(1 for a in axes_cfg if sc["axes"].get(a["id"]) is not None)
    axes_note = ""
    if 0 < n_axes_calc < n_axes:
        axes_note = (f'<p class="axes-calc">Indice calculé sur {n_axes_calc} '
                     f'axes sur {n_axes} — les autres sont entièrement '
                     f'« inconnu ».</p>')

    # « Repères » — construits ici pour être intégrés au panneau de score comme
    # 3e colonne compacte (chantier 7, TAF 3).
    rows = []
    if fiche.get("forme_juridique"):
        rows.append(("Forme juridique", e(clean(fiche["forme_juridique"]))))
    if fiche.get("nature_interet") and cat in ("porteur", "usufruitier"):
        rows.append(("Nature de l'intérêt",
                     e(nature_label(fiche["nature_interet"], cfg["concepts"]))))
    if cat == "porteur":
        n_lieux_p = len(sc.get("chaine_uids", []) or [])
        if n_lieux_p:
            rows.append(("Lieux reliés", e(f"{n_lieux_p} dans l'annuaire")))
    if fiche.get("localisation"):
        l = fiche["localisation"]
        loc = ", ".join(x for x in [l.get("commune"), l.get("departement"),
                                    l.get("region")] if x)
        rows.append(("Localisation", e(loc)))
    if fiche.get("pays"):
        rows.append(("Pays", e(fiche["pays"])))
    if fiche.get("annee"):
        rows.append(("Année", e(fiche["annee"])))
    mont = fiche.get("montage", {}) or {}
    if mont.get("type"):
        rows.append(("Type de montage",
                     e(montage_label(mont["type"], cfg["concepts"]))))
    # intégrité du montage : nouvelle clé `integrite_montage`, repli sur
    # l'ancienne clé `purete_juridique` pour ne pas planter sur une fiche non
    # encore migrée.
    im = fiche.get("integrite_montage", {}) or fiche.get("purete_juridique", {}) or {}
    if im.get("niveau"):
        plab, psens = integrite_label(im["niveau"], ranking)
        rows.append(("Intégrité du montage",
                     f'<span title="{e(psens)}">'
                     f'<a href="../regimes.html#poles">{e(plab)}</a></span>'))
    if fiche.get("url"):
        rows.append(("Site", f'<a href="{e(fiche["url"])}" rel="noopener" '
                             f'target="_blank">Voir le site</a>'))
    # géoportail (lieu) et bloc dossier — identité, échelle — chantier 6
    loc6 = fiche.get("localisation", {}) or {}
    if loc6.get("geoportail"):
        rows.append(("Géoportail", f'<a href="{e(loc6["geoportail"])}" '
                     f'rel="noopener" target="_blank">Voir la parcelle</a>'))
    dossier = fiche.get("dossier", {}) or {}
    ident = dossier.get("identite", {}) or {}
    if ident.get("siren"):
        rows.append(("SIREN / SIRET", e(clean(str(ident["siren"])))))
    if ident.get("rna"):
        rows.append(("N° RNA", e(clean(str(ident["rna"])))))
    if ident.get("adresse"):
        rows.append(("Siège", e(clean(ident["adresse"]))))
    ech = dossier.get("echelle", {}) or {}
    if ech.get("personnes"):
        rows.append(("Collectif", f'{e(ech["personnes"])} personnes'))
    if ech.get("lieux"):
        rows.append(("Lieux portés", e(str(ech["lieux"]))))
    if ech.get("surface"):
        rows.append(("Surface", e(clean(str(ech["surface"])))))
    bref_compact = "".join(
        f'<div class="sb-item"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in rows)
    if _ev_lieu and sc.get("idl_v2") is not None:
        rows.append(("Ancienne note (v2)", f'{sc["idl_v2"]}/100 · archivée'))
        bref_compact = "".join(f'<div class="sb-item"><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    bref_col = (f'<div class="score-bref"><p class="score-cap">Repères</p>'
                f'<dl>{bref_compact}</dl></div>') if rows else ""

    pal_col = _bcol if _ev_lieu else (sc["palier"]["couleur"] if sc["palier"] else "var(--green)")

    # 1.5 — objet-verdict composite : verdict · Indice · palier rapprochés sur une
    # ligne en tête de panneau, trois libellés typographiquement distincts (badge
    # coloré · nombre /100 · étiquette de palier) + un renvoi unique. On rapproche
    # la zone d'affichage, jamais les concepts ni les valeurs. Lieux seulement
    # (eux seuls portent un verdict).
    composite_html = ""
    if cat == "lieu" and sc.get("idl") is not None and sc.get("palier"):
        vid = compute_verdict(fiche, by_uid)
        composite_html = (
            '<div class="verdict-composite">'
            '<span class="vco-line">'
            f'{verdict_badge(vid, cfg["concepts"])}'
            f'<span class="vco-sep">·</span>'
            f'<span class="vco-idl"><b>{sc["idl"]}</b><span class="vco-unit">/100</span></span>'
            f'<span class="vco-sep">·</span>'
            f'<span class="vco-pal" style="--pal:{pal_col}">{e(sc["palier"]["label"])}</span>'
            '</span>'
            '<a class="vco-renvoi" href="../methode.html#verdict">'
            'Pourquoi ces trois ? → Méthode</a>'
            '</div>')
    if _ev_lieu:
        _nd = ('<span class="vco-idl"><b>suspendue</b></span>' if _susp
               else f'<span class="vco-idl"><b>{_num}</b><span class="vco-unit">/100</span></span>')
        composite_html = (
            '<div class="verdict-composite"><span class="vco-line">'
            f'{_nd}<span class="vco-sep">·</span>'
            f'<span class="vco-pal" style="--pal:{_bcol}">{e(FB_LABEL[_band])}</span>'
            '</span><a class="vco-renvoi" href="../methode.html">La méthode →</a></div>')

    _sc_b = _sc_v3 if _ev_lieu else sc
    _axc = _q_cfg if _ev_lieu else axes_cfg
    _axs = _q_scores if _ev_lieu else sc['axes']
    _rk = _ranking_v3 if _ev_lieu else ranking
    if _ev_lieu:
        _tr = axis_triangle(_q_cfg, _q_scores).replace("Profil à cinq axes", "Profil des six questions")
        _triangle = re.sub(r'<text class="tri-scale"[^>]*>[^<]*</text>', '', _tr)
    else:
        _triangle = ""
    _axbar = axis_bar(_axc, _axs) if _ev_lieu else ""
    _scale = idl_scale(_sc_b, _rk) if _ev_lieu else ""
    _axesnote = "" if (_ev_lieu or sc.get("idl") is None) else axes_note
    _scorecap = ('<p class="score-cap"><a href="../methode.html">Note de libération</a></p>'
                 if _ev_lieu else
                 '<p class="score-cap"><a href="../methode.html">Note de libération</a></p>')
    score_block = f"""<section class="score-panel" style="--pal:{pal_col}">
  {composite_html}
  <div class="score-main">
    {_scorecap}
    {idl_badge(_sc_b, big=True)}
    {_axesnote}
    {_triangle}
  </div>
  <div class="score-axes">
    {_axbar}
    {_scale}
    <p class="fiab fiab-{fcls}">{e(flabel)}</p>
    {comp}
    {plafonds_html}
  </div>
  {bref_col}
</section>"""

    # clé de lecture compacte de la fiche — repliée par défaut, sobre
    # (audit pédagogie C, I1/I3).
    grille_line = ("</li>\n  <li><strong>Grille détaillée</strong> — chaque "
                   "critère est évalué oui · partiel · non ; le score en "
                   "découle.") if (cat != "modele" and sc["criteres_evalues"]) else ""
    axes_enum = ", ".join(f"{a['id']} {a['label']}" for a in axes_cfg)
    # encart A3 — verdict × palier × Indice (lieux seulement) : lève l'apparente
    # contradiction entre un Indice élevé et un palier qui n'est pas « abouti ».
    # Bandeau de lecture A3 — TOUJOURS visible (déplié), au-dessus de la ligne de
    # flottaison : un·e lecteur·rice doit pouvoir citer le sens des trois chiffres
    # sans rien dérouler. Lieux seulement (eux seuls portent un verdict).
    # 1.1 — une seule phrase + lien Méthode, placée SOUS le panneau de score
    # (l'encart à puces « Trois lectures » est supprimé ; la distinction est
    # désormais portée par l'objet-verdict composite en tête de panneau).
    if _ev_lieu and cat == "lieu":
        verdict_cle = ("""<p class="verdict-cle">La note et le palier situent un <strong>degré de """
            """sortie du marché</strong>, pas la valeur d'un lieu ; on lit au <strong>point le plus """
            """faible</strong>, et le badge écologique est <em>à côté</em> de la note. """
            """<a href="../methode.html#indice">Comment les lire → Méthode</a></p>""")
    elif cat == "lieu":
        verdict_cle = ("""<p class="verdict-cle">Verdict, Indice et palier ne disent pas
la même chose : un Indice élevé peut rester « solide » sans être « abouti ».
<a href="../methode.html#verdict">Comment les lire → Méthode</a></p>""")
    else:
        verdict_cle = ""
    # 1.2 — version courte et accessible : on décrit ce que MONTRENT les visuels
    # (pentagone, barres, badge), sans ré-expliquer la règle d'agrégation (qui vit
    # sur la Méthode, vers laquelle on renvoie).
    lecture = f"""<details class="fiche-key">
  <summary>Comment lire les visuels de cette fiche</summary>
  <ul>
  <li><strong>Badge Indice</strong> — note de synthèse de 0 à 100 ; sa couleur
  indique le palier.</li>
  <li><strong>Pentagone à cinq axes</strong> — un sommet par axe ({axes_enum}),
  l'axe 1 en haut. Plus la zone colorée s'étend vers un sommet, plus le montage
  est noté sur cet axe.</li>
  <li><strong>Barres d'axe</strong> — le détail chiffré des cinq axes.{grille_line}</li>
  </ul>
  <p class="fiche-key-more"><a href="../methode.html#indice">Comment l'Indice est
  calculé → Méthode</a></p>
</details>"""
    if _ev_lieu:
        lecture = ("""<details class="fiche-key"><summary>Comment lire les visuels de cette fiche</summary><ul>"""
          """<li><strong>Anneau de note</strong> — la note de libération de 0 à 100 ; sa couleur indique le palier.</li>"""
          """<li><strong>Étoile à six branches</strong> — un sommet par question (1 Le milieu, 2 Le vivant, 3 L'ouverture, 4 Le don, 5 La durée, 6 La voix), numérotées comme les barres.</li>"""
          """<li><strong>Barres</strong> — les six questions chiffrées (● tenu 100 · ◐ partiel 50 · ○ absent 0 · n.r. non établi).</li>"""
          """<li><strong>Échelle</strong> — du marchand au commun vivant ; le curseur situe la note.</li>"""
          """<li><strong>Badge « Sanctuaire »</strong> — distinction écologique, <i>à part</i> de la note.</li></ul>"""
          """<p class="fiche-key-more"><a href="../methode.html">Comment la note est calculée → Méthode</a></p></details>""")
    elif cat != "lieu":
        lecture = ""

    # (les « Repères » sont désormais construits plus haut et intégrés au
    # panneau de score comme 3e colonne — chantier 7, TAF 3.)

    # résumé
    resume = ""
    if fiche.get("resume"):
        resume = (f'<section><h2 class="sec">Présentation</h2>'
                  f'<p class="prose">{e(clean(fiche["resume"]))}</p></section>')

    # montage — silhouette typologique + chaîne réelle (porteur, articulations
    # typées, usufruitiers, liants). Cf. chantier 5, conception-refonte-3.md §8.
    montage_html = montage_section(fiche, cfg["concepts"], by_uid)
    dossier_html = dossier_section(fiche)

    # grille détaillée + récapitulatif par axe
    grille_html = ""
    if _ev_lieu:
        grille_html = _v3_grille_fold(_ev_lieu)
    elif cat != "modele" and sc["criteres_evalues"]:
        gril = grilles.get(cat, {})
        vmap = {"oui": ("Oui", "crit-oui"), "partiel": ("Partiel", "crit-partiel"),
                "non": ("Non", "crit-non"), "inconnu": ("Inconnu", "crit-inconnu")}
        fam_rows = []
        for fam in gril.get("familles", []):
            trs = []
            for cr in fam["criteres"]:
                ev = sc["criteres_evalues"].get(cr["id"])
                if not ev:
                    val, note = "inconnu", ""
                else:
                    val, note = ev["valeur"], ev["note"]
                vlab, vcls = vmap.get(val, vmap["inconnu"])
                trs.append(f"""<tr>
  <td class="crit-name"><span class="axe-dot axe-{cr['axe']}" title="Axe {cr['axe']}"></span>
      {e(cr['label'])}</td>
  <td class="num">{cr['poids']}</td>
  <td class="{vcls}">{e(vlab)}</td>
  <td class="crit-note">{e(clean(note))}</td>
</tr>""")
            fam_rows.append(f'<tr class="fam-row"><th colspan="4" scope="colgroup">{e(fam["label"])}</th></tr>'
                            + "".join(trs))
        recap = grille_recap(sc["criteres_evalues"], gril, axes_cfg)
        grille_html = f"""<section class="grille-section"><details class="grille-fold">
<summary class="sec">Grille de lecture <span class="fold-hint">— déplier / replier</span></summary>
<p class="grille-intro">{e(clean(gril.get('objet','')))}
<a href="../grilles.html#grille-{cat}">Comprendre la grille →</a></p>
{recap}
<div class="table-scroll" tabindex="0" role="region" aria-label="Grille de lecture détaillée de la fiche"><table class="grille-tbl">
<caption class="visually-hidden">Grille de lecture de la fiche : critère, poids, évaluation et lecture.</caption>
<thead><tr><th scope="col">Critère</th><th scope="col" class="num">Poids</th><th scope="col">Évaluation</th><th scope="col">Lecture</th></tr></thead>
<tbody>{''.join(fam_rows)}</tbody></table></div>
<p class="axe-legend">{axe_legend(axes_cfg)}</p>
</details></section>"""

    # analyse stratégique
    an = fiche.get("analyse", {}) or {}
    def lst(items):
        return "".join(f"<li>{e(clean(x))}</li>" for x in (items or []))
    analyse_html = ""
    if an:
        synth = (f'<p class="prose synthese">{e(clean(an.get("synthese","")))}</p>'
                 if an.get("synthese") else "")
        analyse_html = f"""<section><h2 class="sec">Analyse stratégique</h2>
{synth}
<div class="analyse-grid">
  <div class="an-col an-forces"><h3>Forces</h3><ul>{lst(an.get('forces'))}</ul></div>
  <div class="an-col an-frag"><h3>Fragilités</h3><ul>{lst(an.get('fragilites'))}</ul></div>
  <div class="an-col an-lev"><h3>Leviers</h3><ul>{lst(an.get('leviers'))}</ul></div>
</div></section>"""

    # Droit de réponse du porteur (réversibilité du verdict) — rendu si la fiche
    # porte un bloc `reponse_porteur: {texte, date, auteur}`. Voix distincte de
    # celle de l'annuaire, clairement attribuée : l'évaluation est contestable et
    # le porteur peut faire valoir sa lecture.
    reponse_html = ""
    rp = fiche.get("reponse_porteur") or {}
    if rp.get("texte"):
        meta_rp = " · ".join(x for x in [clean(rp.get("auteur") or ""),
                                         clean(rp.get("date") or "")] if x)
        reponse_html = (
            '<section class="reponse-porteur"><h2 class="sec">Droit de réponse</h2>'
            '<p class="rp-chapeau">L\'évaluation ci-dessus est une lecture au regard '
            'd\'un cadre explicite et contestable. Le porteur ou l\'usufruitier peut '
            'y répondre ; sa réponse est reproduite ici sans retouche.</p>'
            f'<blockquote class="rp-texte">{e(clean(rp["texte"]))}</blockquote>'
            + (f'<p class="rp-meta">— {e(meta_rp)}</p>' if meta_rp else "")
            + '</section>')

    # reliés — la chaîne (déclarée par le lieu) et les liens voir_aussi, dans
    # les deux sens (liens déclarés + rétro-liens des fiches qui citent celle-ci).
    liens_html = ""
    rel_uids = set()
    me = fiche["uid"]
    if cat == "lieu":
        ch = fiche.get("chaine", {}) or {}
        rel_uids |= set(ch.get("porteurs") or [])
        rel_uids |= set(ch.get("usufruitiers") or [])
    rel_uids |= set(fiche.get("voir_aussi", []) or [])
    for other_uid, other in by_uid.items():
        if other_uid == me:
            continue
        och = other.get("chaine", {}) or {}
        if me in (och.get("porteurs") or []) or me in (och.get("usufruitiers") or []):
            rel_uids.add(other_uid)
        if me in (other.get("voir_aussi", []) or []):
            rel_uids.add(other_uid)
    rel_uids.discard(me)
    chips_par_cat = {}
    for uid in sorted(rel_uids):
        tgt = by_uid.get(uid)
        if not tgt:
            continue
        tcat = tgt["categorie"]
        _tsc = sc_by_uid.get(uid)
        _tri = (axis_triangle(Q6_CFG, _tsc["q6"], compact=True)
                if _tsc and _tsc.get("q6") else "")
        chip = (f'<a class="chip chip-rel" href="../{CAT_SLUG[tcat]}/{uid}.html">'
                f'{_tri}<span class="chip-txt">{e(tgt["nom"])}'
                f'<span class="chip-cat">{e(tcat)}</span></span></a>')
        chips_par_cat.setdefault(tcat, []).append(chip)
    if chips_par_cat:
        # reliés groupés par nature plutôt que mélangés (chantier 7, TAF 5)
        ordre_grp = [("lieu", "Lieux"),
                     ("porteur", "Porteurs de nue-propriété"),
                     ("usufruitier", "Organismes usufruitiers"),
                     ("reseau", "Réseaux"),
                     ("modele", "Modèles voisins")]
        groupes = []
        for gid, gtitre in ordre_grp:
            lot = chips_par_cat.get(gid)
            if lot:
                groupes.append(f'<h3 class="rel-grp">{e(gtitre)}</h3>'
                               f'<div class="chips">{"".join(lot)}</div>')
        liens_html = ('<section><h2 class="sec">Reliés dans l\'annuaire</h2>'
                      '<p class="lead">Montages directement reliés à cette '
                      'fiche, regroupés par nature.</p>'
                      + "".join(groupes) + '</section>')

    # fiabilité + sources
    fiab = ""
    if fiche.get("fiabilite"):
        fiab = (f'<section class="fiab-box"><h3>Fiabilité des informations</h3>'
                f'<p>{e(clean(fiche["fiabilite"]))}</p></section>')
    src_items = "".join(
        f'<li><a href="{e(s.get("url",""))}" target="_blank" rel="noopener">'
        f'{e(clean(s.get("titre","")))}</a></li>'
        for s in (fiche.get("sources", []) or []))
    sources_html = (f'<section><h2 class="sec">Sources</h2>'
                    f'<ul class="src-list">{src_items}</ul></section>'
                    if src_items else "")

    retlabel = {"lieu": "aux lieux", "porteur": "aux porteurs",
                "usufruitier": "aux usufruitiers",
                "modele": "aux modèles voisins"}[cat]
    backlink = (f'<p class="backlink">'
                f'<a href="../{CAT_PAGE[cat]}">← Retour {retlabel}</a>'
                f' · <a href="../classement.html">Voir le classement</a></p>')
    # le <defs> tri-base n'est utile que si la fiche rend au moins un triangle
    # compact, c'est-à-dire si elle a des chips reliés (audit fonctionnel C, M2).
    defs = tri_defs(Q6_CFG) if chips_par_cat else ""
    # ordre de lecture (session #3) : le récit avant la preuve — les « Repères »
    # sont intégrés au panneau de score (chantier 7) ; puis présentation,
    # montage, analyse, chaîne, dossier, et la grille reléguée en fin.
    # lien vers le dossier (magazine) qui raconte ce lieu, s'il existe
    dossier_slug = (cfg.get("_dossier_for") or {}).get(fiche["uid"])
    dossier_lien = (f'<p class="fiche-dossier-lien"><a href="../dossiers/'
                    f'{e(dossier_slug)}.html">Lire le dossier — le récit de ce '
                    f'lieu →</a></p>' if dossier_slug else "")
    _group_extra = ""
    if _is_group:
        _GH={"porteur":("Les lieux qu'il tient","Sa note de libération est la synthèse de ces lieux — un porteur se juge à ce qu'il libère."),
             "usufruitier":("Les lieux qu'il anime","Sa note de libération est la synthèse des lieux dont il a l'usage."),
             "reseau":("Les lieux de son réseau","Sa note de libération est la synthèse des lieux que son réseau fédère.")}
        _h,_l=_GH[cat]
        if _is_porteur:
            _pctx=porteur_porte_context(fiche)
            _ctx=(f'<p class="verdict-cle"><b>Démarche / modèle.</b> Portage de type <b>{e(_pctx["label"])}</b> : '
                  f'la solidité de la porte que ce porteur apporte à la chaîne conditionne ce que ses lieux peuvent '
                  f'atteindre. La note ci-dessus est la <b>synthèse de libération</b> de ces lieux. <a href="../methode.html">Méthode →</a></p>')
        else:
            _kind={"usufruitier":"Collectif usager","reseau":"Réseau"}[cat]
            _ctx=(f'<p class="verdict-cle"><b>{_kind}.</b> Évalué sur la <b>même grille</b> que les lieux, '
                  f'sa note est la <b>synthèse de libération</b> des lieux qu\'il {"anime" if cat=="usufruitier" else "fédère"}. '
                  f'<a href="../methode.html">Méthode →</a></p>')
        _group_extra = _ctx + (_member_lieux(fiche, by_uid, _h, _l) if cat != "usufruitier" else "")
    body = (defs + head + dossier_lien + score_block + verdict_cle + lecture + _group_extra + resume
            + montage_html + analyse_html + reponse_html + liens_html + grille_html
            + dossier_html + fiab + sources_html + backlink)

    # données structurées : fil d'Ariane + entité principale
    fpath = f"{CAT_SLUG[cat]}/{fiche['uid']}.html"
    fdesc = meta_desc(fiche.get("resume", "") or sub, 250)
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil",
             "item": canonical_url("index.html")},
            {"@type": "ListItem", "position": 2, "name": catlabel,
             "item": canonical_url(CAT_PAGE[cat])},
            {"@type": "ListItem", "position": 3, "name": fiche["nom"]},
        ],
    }
    if cat == "lieu":
        entity = {"@context": "https://schema.org", "@type": "Place",
                  "name": fiche["nom"], "description": fdesc,
                  "url": canonical_url(fpath)}
        loc = fiche.get("localisation") or {}
        if loc:
            addr = {"@type": "PostalAddress", "addressCountry": "FR"}
            if loc.get("commune"):
                addr["addressLocality"] = loc["commune"]
            if loc.get("region"):
                addr["addressRegion"] = loc["region"]
            entity["address"] = addr
    else:
        entity = {"@context": "https://schema.org", "@type": "Organization",
                  "name": fiche["nom"], "description": fdesc,
                  "mainEntityOfPage": canonical_url(fpath)}
        if fiche.get("url"):
            entity["url"] = fiche["url"]
            entity["sameAs"] = [fiche["url"]]
    ogt = "article" if cat != "modele" else "website"
    # titre_court : <title> abrégé optionnel, pour ne pas dépasser ~60 car. une
    # fois suffixé « — Terres Libérées » (audit SEO C, M1). Le H1 reste le nom
    # complet.
    page_title = clean(fiche.get("titre_court", "")) or fiche["nom"]
    return page(page_title, body, CAT_PAGE[cat], depth=1, project=project,
                description=clean(fiche.get("resume", "")) or sub,
                path=fpath, jsonld=[breadcrumb, entity], og_type=ogt)


# ─────────────────────────────────────────────────────────────────────────────
# Pages — catalogues
# ─────────────────────────────────────────────────────────────────────────────

QCOL_V3={"milieu":"#6b8f71","vivant":"#3d7a4e","ouverture":"#4a6b8a","don":"#b08a3e","duree":"#8a6db0","voix":"#bc5d3a"}
RANKING_V3={"paliers":[{"min":0,"couleur":"#9a9a9a","label":"marchand"},
    {"min":20,"couleur":"#b08a3e","label":"sorti du marché"},
    {"min":50,"couleur":"#3d7a4e","label":"autogéré"},
    {"min":75,"couleur":"#2f6e8f","label":"usage libéré"},
    {"min":90,"couleur":"#224477","label":"commun vivant"}]}

def _v3_score_panel_standalone(ev):
    """Panneau de score v3 (anneau + étoile six branches + barres + échelle) à partir d'un eval — réutilisé hors render_fiche (réseaux)."""
    band,susp,pf,badge,num=_fsc_derive(ev)
    bcol=FB_HEX[band]
    sc_v3={"idl":(None if susp else num),"palier":{"label":FB_LABEL[band],"couleur":bcol},"idl_brut":None,"score_type":"calcule"}
    NUMS=["1","2","3","4","5","6"]; qv={"oui":100,"partiel":50,"non":0}
    q_cfg=[{"id":NUMS[i],"label":Q_LABEL[i][1],"couleur":QCOL_V3[Q_LABEL[i][0]]} for i in range(6)]
    q_scores={NUMS[i]:qv.get(ev["questions"][Q_LABEL[i][0]]["valeur"]) for i in range(6)}
    tri=re.sub(r'<text class="tri-scale"[^>]*>[^<]*</text>','',axis_triangle(q_cfg,q_scores).replace("Profil à cinq axes","Profil des six questions"))
    nd=('<b>suspendue</b>' if susp else f'<b>{num}</b><span class="vco-unit">/100</span>')
    composite=(f'<div class="verdict-composite"><span class="vco-line"><span class="vco-idl">{nd}</span>'
               f'<span class="vco-sep">·</span><span class="vco-pal" style="--pal:{bcol}">{e(FB_LABEL[band])}</span></span>'
               f'<a class="vco-renvoi" href="../methode.html">La méthode →</a></div>')
    return (f'<section class="score-panel" style="--pal:{bcol}">{composite}'
            f'<div class="score-main"><p class="score-cap">Note de libération</p>{idl_badge(sc_v3,big=True)}{tri}</div>'
            f'<div class="score-axes">{axis_bar(q_cfg,q_scores)}{idl_scale(sc_v3,RANKING_V3)}</div></section>')

def render_reseau(fiche, cfg, by_uid, sc_by_uid):
    """Rend la fiche d'un RÉSEAU : un hub non noté (cf. décision R1). Il
    présente l'entité-réseau, relie ses membres documentés et donnera la
    distribution de ses lieux concrets à mesure qu'ils sont carvés."""
    project = cfg["concepts"]["project"]
    axes_cfg = cfg["ranking"]["axes"]
    uid = fiche["uid"]

    head = f"""<nav class="crumb" aria-label="Fil d'Ariane">
  <a href="../index.html">Accueil</a> ›
  <a href="../reseaux.html">Réseaux</a> ›
  <span aria-current="page">{e(fiche['nom'])}</span>
</nav>
<div class="fiche-head">
  <span class="tag tag-reseau">Réseau</span>
  <h1>{e(fiche['nom'])}</h1>
  <p class="fiche-sub">{e(clean(fiche.get('sous_titre', '')))}</p>
</div>"""

    intro = ('<section><p class="lead"><strong>Réseau.</strong> Cette entité '
             'fédère ou démultiplie plusieurs lieux : elle n\'est pas une chaîne '
             'unique : sa note de libération agrège les lieux qu\'elle fédère. Sa fiche est '
             'un hub — elle présente l\'entité, relie ses membres documentés et '
             'donnera la distribution de ses lieux concrets à mesure qu\'ils '
             'sont détaillés. <a href="../methode.html#chaine">La chaîne, et où '
             'se lit chaque axe →</a></p></section>')

    resume = ""
    if fiche.get("resume"):
        resume = (f'<section><h2 class="sec">Présentation</h2>'
                  f'<p class="prose">{e(clean(fiche["resume"]))}</p></section>')

    montage_html = ""
    mont = fiche.get("montage", {}) or {}
    if mont.get("description"):
        montage_html = (f'<section><h2 class="sec">Le montage</h2>'
                        f'<p class="prose">{e(clean(mont["description"]))}</p>'
                        f'</section>')

    chips, lieux_membres = [], []
    for muid in (fiche.get("membres", []) or []):
        tgt = by_uid.get(muid)
        if not tgt:
            continue
        tcat = tgt["categorie"]
        tsc = sc_by_uid.get(muid)
        if tcat == "lieu":
            lieux_membres.append((tgt, tsc))
        _tri = (axis_triangle(Q6_CFG, tsc["q6"], compact=True)
                if tsc and tsc.get("q6") else "")
        chips.append(
            f'<a class="chip chip-rel" href="../{CAT_SLUG[tcat]}/{muid}.html">'
            f'{_tri}<span class="chip-txt">{e(tgt["nom"])}'
            f'<span class="chip-cat">{e(CAT_LABEL.get(tcat, tcat))}</span>'
            f'</span></a>')
    # Repères du réseau — nombre de porteurs et de lieux (session #4)
    n_porteurs_res = sum(
        1 for m in (fiche.get("membres") or [])
        if (by_uid.get(m) or {}).get("categorie") == "porteur")
    lieux_res = set(t["uid"] for t, _ in lieux_membres)
    for m in (fiche.get("membres") or []):
        msc = sc_by_uid.get(m)
        if msc:
            lieux_res |= set(msc.get("chaine_uids", []) or [])
    rep_items = []
    if n_porteurs_res:
        rep_items.append(("Porteurs du réseau", str(n_porteurs_res)))
    if lieux_res:
        rep_items.append(("Lieux du réseau", str(len(lieux_res))))
    reperes_html = ""
    if rep_items:
        dl = "".join(f'<div class="sb-item"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>'
                     for k, v in rep_items)
        reperes_html = (f'<section><div class="score-bref reseau-reperes">'
                        f'<p class="score-cap">Repères</p><dl>{dl}</dl>'
                        f'</div></section>')

    membres_html = ""
    if chips:
        membres_html = (f'<section><h2 class="sec">Membres dans l\'annuaire</h2>'
                        f'<p class="lead">Entités de ce réseau déjà documentées '
                        f'par l\'annuaire.</p>'
                        f'<div class="chips">{"".join(chips)}</div></section>')

    if lieux_membres:
        rep = {}
        for _, tsc in lieux_membres:
            lab = tsc["palier"]["label"] if (tsc and tsc["palier"]) else "Non noté"
            rep[lab] = rep.get(lab, 0) + 1
        rows = "".join(f"<li>{e(k)} — {v}</li>" for k, v in rep.items())
        distrib_html = (f'<section><h2 class="sec">Distribution des lieux</h2>'
                        f'<p class="lead">{len(lieux_membres)} lieu·x concret·s '
                        f'détaillé·s, répartis par palier de libération :</p>'
                        f'<ul>{rows}</ul></section>')
    else:
        distrib_html = ('<section><h2 class="sec">Distribution des lieux</h2>'
                        '<p class="prose">Aucun lieu concret de ce réseau n\'est '
                        'encore détaillé dans l\'annuaire. Les chaînes réelles '
                        'sont carvées progressivement, fiche par fiche.</p>'
                        '</section>')

    an = fiche.get("analyse", {}) or {}
    analyse_html = ""
    if an:
        def lst(items):
            return "".join(f"<li>{e(clean(x))}</li>" for x in (items or []))
        synth = (f'<p class="prose synthese">{e(clean(an.get("synthese","")))}</p>'
                 if an.get("synthese") else "")
        analyse_html = (
            f'<section><h2 class="sec">Analyse stratégique</h2>{synth}'
            f'<div class="analyse-grid">'
            f'<div class="an-col an-forces"><h3>Forces</h3><ul>{lst(an.get("forces"))}</ul></div>'
            f'<div class="an-col an-frag"><h3>Fragilités</h3><ul>{lst(an.get("fragilites"))}</ul></div>'
            f'<div class="an-col an-lev"><h3>Leviers</h3><ul>{lst(an.get("leviers"))}</ul></div>'
            f'</div></section>')

    fiab = ""
    if fiche.get("fiabilite"):
        fiab = (f'<section class="fiab-box"><h3>Fiabilité des informations</h3>'
                f'<p>{e(clean(fiche["fiabilite"]))}</p></section>')
    src_items = "".join(
        f'<li><a href="{e(s.get("url",""))}" target="_blank" rel="noopener">'
        f'{e(clean(s.get("titre","")))}</a></li>'
        for s in (fiche.get("sources", []) or []))
    sources_html = (f'<section><h2 class="sec">Sources</h2>'
                    f'<ul class="src-list">{src_items}</ul></section>'
                    if src_items else "")
    backlink = ('<p class="backlink"><a href="../reseaux.html">← Retour aux '
                'réseaux</a></p>')

    _rev = porteur_eval(fiche, by_uid)
    _rev_panel = ""
    if _rev:
        _rev_panel = (_v3_score_panel_standalone(_rev)
            + '<p class="verdict-cle"><b>Réseau.</b> Évalué sur la même grille que les lieux, sa note est la '
              '<b>synthèse de libération</b> des lieux que son réseau fédère. <a href="../methode.html">Méthode →</a></p>')
    defs = tri_defs(Q6_CFG) if chips else ""
    body = (defs + head + _rev_panel + intro + reperes_html + resume + montage_html
            + membres_html + distrib_html + analyse_html + fiab + sources_html
            + backlink)
    fdesc = meta_desc(fiche.get("resume", "") or fiche.get("sous_titre", ""), 250)
    return page(fiche["nom"], body, "reseaux.html", depth=1, project=project,
                description=fdesc, path=f"r/{uid}.html", og_type="website")


def render_reseaux(reseaux_sc, cfg):
    """Page catalogue des réseaux — liste simple, sans tri ni filtre par note :
    les réseaux ne sont pas notés."""
    project = cfg["concepts"]["project"]
    axes_cfg = cfg["ranking"]["axes"]
    concepts = cfg["concepts"]
    fiches = sorted((f for f, _ in reseaux_sc), key=lambda f: f["nom"])
    cards = cards_grid([(f, {"idl": None, "palier": None,
                             "axes": {a["id"]: None for a in axes_cfg}})
                        for f in fiches], axes_cfg, depth=0, concepts=concepts)
    body = f"""<h1>Réseaux</h1>
<p class="lead">Les réseaux fédèrent ou démultiplient plusieurs lieux —
mouvements, foncières multi-sites, dispositifs de financement. Ils ne portent
une note agrégée de leurs lieux : ce sont des hubs qui relient leurs membres et
dont les lieux concrets sont détaillés un à un. {len(fiches)} réseau·x
recensé·s.</p>
{cards}"""
    return page("Réseaux", body, "reseaux.html", depth=0, project=project,
                description="Les réseaux de la libération des terres recensés "
                            "par l'annuaire.", path="reseaux.html")


def render_catalogue(cat, fiches_sc, cfg):
    project = cfg["concepts"]["project"]
    concepts = cfg["concepts"]
    axes_cfg = cfg["ranking"]["axes"]
    ranking = cfg["ranking"]
    catdef = next(c for c in concepts["categories"] if c["id"] == cat) \
        if cat != "modele" else None
    if cat == "modele":
        title = "Modèles voisins"
        intro = clean(concepts["modeles_voisins"]["description"])
        modeles_note = (
            '<div class="callout callout-note"><p><strong>Hors classement '
            'principal.</strong> Les modèles voisins ne sont pas notés par les '
            'grilles de l\'annuaire : leur note est <em>estimée</em> '
            '(hors grille) et signalé par un anneau en pointillé. '
            'Ils servent de points de comparaison et n\'apparaissent pas dans '
            'le classement.</p></div>')
    else:
        title = catdef["label_pluriel"]
        intro = clean(catdef["definition"])
        modeles_note = ""
    fiches_sc = sorted(fiches_sc, key=lambda x: x[1]["idl"] or 0, reverse=True)
    n = len(fiches_sc)

    # filtres par palier — n'émettre que les paliers présents dans le
    # sous-ensemble, pour éviter des boutons morts (audit fonctionnel C, M1).
    present_pal = []
    for f, s in fiches_sc:
        pid = s["palier"]["id"] if s["palier"] else None
        if pid and pid not in present_pal:
            present_pal.append(pid)
    pal_order = [p for p in ranking["paliers"] if p["id"] in present_pal]
    pal_btns = "".join(
        f'<button class="fbtn" data-fk="palier" data-fv="{p["id"]}" '
        f'aria-pressed="false">{e(p["label"])}</button>' for p in pal_order)
    # filtres par montage (montages présents dans le sous-ensemble)
    present_mont = []
    for f, _ in fiches_sc:
        m = (f.get("montage", {}) or {}).get("type")
        if m and m not in present_mont:
            present_mont.append(m)
    mont_btns = "".join(
        f'<button class="fbtn" data-fk="montage" data-fv="{m}" '
        f'aria-pressed="false">{e(montage_label(m, concepts))}</button>'
        for m in present_mont)
    # filtres par région (lieux uniquement)
    region_block = ""
    if cat == "lieu":
        regions = []
        for f, _ in fiches_sc:
            r = (f.get("localisation", {}) or {}).get("region")
            if r and r not in regions:
                regions.append(r)
        if regions:
            reg_btns = "".join(
                f'<button class="fbtn" data-fk="region" data-fv="{e(r)}" '
                f'aria-pressed="false">{e(r)}</button>' for r in sorted(regions))
            region_block = (
                f'<div class="filter-row" role="group" '
                f'aria-label="Filtrer par région">'
                f'<span class="filter-lab">Région</span>'
                f'<button class="fbtn active" data-fk="region" data-fv="all" '
                f'aria-pressed="true">Toutes</button>{reg_btns}</div>')

    carte_lien = ('\n<a href="carte.html">Voir les lieux sur la carte →</a>'
                  if cat == "lieu" else "")
    body = f"""{tri_defs(Q6_CFG)}<h1>{e(title)}</h1>
<p class="lead">{e(intro)}
<a href="methode.html">Comprendre la note et les six questions →</a>{carte_lien}</p>
{modeles_note}
<div class="toolbar">
  <input type="search" id="q" placeholder="Rechercher un nom…" aria-label="Rechercher par nom" aria-controls="resultats">
  <label class="sort-lab" for="sort">Trier :</label>
  <select id="sort">
    <option value="idl">Par note (décroissant)</option>
    <option value="nom">Par nom (A→Z)</option>
    {"".join(f'<option value="ax{a["id"]}">Par axe {a["id"]} — {e(a["court"])}</option>' for a in axes_cfg)}
  </select>
  <span class="count" id="cnt" aria-live="polite"><b id="cntn">{n}</b><span id="cntl"> entrée{'s' if n > 1 else ''} affichée{'s' if n > 1 else ''}</span></span>
</div>
<p id="sort-status" role="status" class="visually-hidden"></p>
<details class="filter-details">
  <summary>Filtres avancés</summary>
  <div class="filter-bar">
    <div class="filter-row" role="group" aria-label="Filtrer par palier"><span class="filter-lab">Palier</span>
      <button class="fbtn active" data-fk="palier" data-fv="all" aria-pressed="true">Tous</button>
      {pal_btns}</div>
    {f'<div class="filter-row" role="group" aria-label="Filtrer par montage"><span class="filter-lab">Montage</span><button class="fbtn active" data-fk="montage" data-fv="all" aria-pressed="true">Tous</button>{mont_btns}</div>' if mont_btns else ''}
    {region_block}
  </div>
</details>
{bands_legend()}
{cards_grid(fiches_sc, axes_cfg, concepts=concepts, grid_id="resultats")}
<p class="no-result" id="noresult" role="status" hidden>Aucune entrée ne correspond à ces filtres. Élargissez la sélection.</p>
<p class="cat-foot"><a href="suggerer.html">Un lieu manque ou une fiche est incomplète ? Signalez-le →</a></p>
<script defer src="assets/list.js"></script>"""
    active = CAT_PAGE[cat]
    return page(title, body, active, depth=0, project=project, description=intro,
                path=CAT_PAGE[cat])


# ─────────────────────────────────────────────────────────────────────────────
# Pages — classement
# ─────────────────────────────────────────────────────────────────────────────

def render_classement(all_sc, cfg):
    project = cfg["concepts"]["project"]
    by_uid = {f["uid"]: f for f, _ in all_sc}
    entries=[]
    for f, s in all_sc:
        if f.get("categorie")=="modele": continue
        v=fiche_v3(f, by_uid)
        if not v: continue
        entries.append((f, v))
    entries.sort(key=lambda x:(x[1]["note"] if x[1]["note"] is not None else -1), reverse=True)
    catlabel={"lieu":"Lieu","porteur":"Porteur","usufruitier":"Usufruitier","reseau":"Réseau"}
    rows=[]
    for i,(f,v) in enumerate(entries,1):
        cat=f["categorie"]; href=f'{CAT_SLUG[cat]}/{f["uid"]}.html'
        note=("suspendue" if v["susp"] else (v["note"] if v["note"] is not None else "—"))
        rows.append(f"""<tr data-cat="{cat}">
  <td class="rank">{i}</td>
  <td class="name"><a href="{href}">{e(f['nom'])}</a>
      {ctx_labels_html(f, "")}
      <span class="row-sub">{e(clean(f.get('sous_titre','')))}</span></td>
  <td><span class="tag tag-{cat}">{catlabel.get(cat,cat)}</span></td>
  <td><span class="pal-chip" style="--pal:{v['bcol']}">{e(v['label'])}</span></td>
  <td class="num idl-cell" style="--pal:{v['bcol']}"><b>{note}</b></td>
</tr>""")
    bands=[("commun_vivant","commun vivant"),("usage_decommodifie","usage libéré"),
           ("autogere","autogéré"),("sorti_du_marche","sorti du marché"),
           ("en_transition","en transition"),("marchand","marchand")]
    legend="".join(f'<span class="pal-chip" style="--pal:{FB_HEX[b]}">{e(lab)}</span>' for b,lab in bands)
    body=f"""<h1>Classement par la note de libération</h1>
<p class="lead">Chaque entrée — lieu, porteur, usufruitier, réseau — est notée de 0 à 100 sur la
<a href="methode.html">même grille</a> (le faisceau libéré), lue au point le plus faible. Porteurs,
usufruitiers et réseaux sont notés par <strong>agrégation des lieux</strong> qu'ils tiennent, animent ou
fédèrent. <a href="methode.html">Méthode →</a></p>
<div class="paliers-legend">{legend}</div>
<div class="toolbar" role="group" aria-label="Filtrer par catégorie">
  <span class="sort-lab">Filtrer&nbsp;: </span>
  <button class="fbtn active" data-f="all" aria-pressed="true">Tout</button>
  <button class="fbtn" data-f="lieu" aria-pressed="false">Lieux</button>
  <button class="fbtn" data-f="porteur" aria-pressed="false">Porteurs</button>
  <button class="fbtn" data-f="usufruitier" aria-pressed="false">Usufruitiers</button>
  <button class="fbtn" data-f="reseau" aria-pressed="false">Réseaux</button>
</div>
<div class="table-scroll" tabindex="0" role="region" aria-label="Tableau du classement">
<table class="rank-tbl"><thead><tr>
  <th scope="col">#</th><th scope="col">Entrée</th><th scope="col">Catégorie</th>
  <th scope="col">Palier</th><th scope="col" class="num">Note</th>
</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p class="note">Note « suspendue » : une question décisive n'est pas documentée. La note se lit avec le
profil des six questions sur chaque fiche.</p>
<script defer src="assets/list.js"></script>"""
    return page("Classement", body, "classement.html", project=project,
                description="Classement par la note de libération (le faisceau libéré).",
                path="classement.html")


# ─────────────────────────────────────────────────────────────────────────────
# Pages — carte
# ─────────────────────────────────────────────────────────────────────────────

# Couleurs des marqueurs par verdict — alignées sur les badges verdict du CSS
# (.verdict-sanctuaire / -hybride / -marchand) et la charte (variables --green-dk,
# --gold-dk, --terra-dk). `None` (verdict à établir) → gris (--faint).
CARTE_VERDICT_COULEURS = {
    "marchand": "#8f3f25",    # --terra-dk
    "hybride": "#8a6420",     # --gold-dk
    "sanctuaire": "#356026",  # --green-dk
    None: "#6e6655",          # --faint
}
CARTE_VERDICT_LABELS = {
    "marchand": "Montage marchand",
    "hybride": "Montage hybride",
    "sanctuaire": "Sanctuaire",
    None: "Verdict suspendu",
}

# Extraction lon,lat depuis l'URL geoportail (paramètre c=LON,LAT).
_GEOPORTAIL_C = re.compile(r"[?&]c=(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")


def _coords_from_geoportail(url):
    """Renvoie (lon, lat) extraits d'une URL geoportail, ou None si absente
    ou non conforme. Ne fabrique jamais de coordonnées."""
    if not url:
        return None
    m = _GEOPORTAIL_C.search(str(url))
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def carte_markers(all_sc, by_uid):
    """Construit (markers, omis) pour la carte des lieux.

    Un marqueur par lieu géolocalisé : {lat, lon, nom, uid, verdict,
    verdict_label, idl, palier, commune}. Les lieux sans coordonnées valides
    sont renvoyés à part (liste de (uid, nom)) pour le compte-rendu."""
    markers, omis = [], []
    for f, sc in all_sc:
        if f.get("categorie") != "lieu":
            continue
        loc = f.get("localisation", {}) or {}
        coords = _coords_from_geoportail(loc.get("geoportail"))
        if coords is None:
            omis.append((f["uid"], f.get("nom", f["uid"])))
            continue
        lon, lat = coords
        verdict = compute_verdict(f, by_uid)
        palier = sc.get("palier")
        commune = clean(loc.get("commune") or "")
        dept = clean(loc.get("departement") or "")
        commune_dept = " — ".join(x for x in (commune, dept) if x)
        _v3m = lieu_v3(f)
        markers.append({
            "lat": lat, "lon": lon,
            "nom": f.get("nom", f["uid"]), "uid": f["uid"],
            "idl": sc.get("idl"),
            "band": (_v3m["band"] if _v3m else ""),
            "bcol": (_v3m["bcol"] if _v3m else ""),
            "band_label": (_v3m["label"] if _v3m else ""),
            "v3note": (_v3m["note"] if _v3m else None),
            "v3susp": (bool(_v3m["susp"]) if _v3m else False),
            "commune": commune_dept,
        })
    return markers, omis


def render_carte(all_sc, cfg, by_uid):
    project = cfg["concepts"]["project"]
    markers, omis = carte_markers(all_sc, by_uid)
    n = len(markers)

    # données des marqueurs en JSON inline — pas de dépendance externe hors
    # Leaflet + tuiles OSM. json.dumps n'émet pas de balise </script> littérale.
    data_js = json.dumps(markers, ensure_ascii=False)
    couleurs_js = json.dumps(
        {k or "": v for k, v in CARTE_VERDICT_COULEURS.items()},
        ensure_ascii=False)

    # légende des couleurs de verdict (ordre : sanctuaire → hybride → marchand →
    # à établir). Symétrique : une pastille de même taille par verdict.
    leg_order = [("commun_vivant","commun vivant"),("usage_decommodifie","usage libéré"),
                 ("autogere","autogéré"),("sorti_du_marche","sorti du marché"),
                 ("en_transition","en transition"),("marchand","marchand")]
    legende = "".join(
        f'<span class="carte-leg-item">'
        f'<span class="carte-leg-dot" style="background:{FB_HEX[b]}"></span>'
        f'{e(lab)}</span>'
        for b,lab in leg_order)

    body = f"""<h1>Carte des lieux</h1>
<p class="lead">Un marqueur par lieu de l'annuaire, géolocalisé et coloré selon
son palier de libération (la nouvelle grille). Cliquez un marqueur pour ouvrir sa fiche.
<a href="lieux.html">Voir le catalogue des lieux →</a></p>
<div class="carte-legende" role="group" aria-label="Légende des paliers de libération">{legende}</div>
<div id="carte" class="carte-map" role="application"
  aria-label="Carte interactive des lieux de l'annuaire"></div>
<p class="note">{n} lieu{'x' if n > 1 else ''} géolocalisé{'s' if n > 1 else ''}.
Fond de carte&nbsp;: OpenStreetMap. Les couleurs reprennent le verdict calculé de
chaque lieu — le catalogue ne hiérarchise pas&nbsp;: tous les marqueurs sont de
même taille.</p>
<noscript><p class="callout callout-warn">La carte interactive nécessite
JavaScript. <a href="lieux.html">Consultez le catalogue des lieux →</a></p></noscript>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
<script>
(function () {{
  var LIEUX = {data_js};
  var COULEURS = {couleurs_js};
  function colorFor(v) {{ return COULEURS[v || ""] || COULEURS[""]; }}
  function esc(s) {{
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {{
      return {{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}}[c];
    }});
  }}
  var map = L.map("carte", {{ scrollWheelZoom: false }}).setView([46.6, 2.5], 6);
  map.on("focus", function () {{ map.scrollWheelZoom.enable(); }});
  map.on("blur", function () {{ map.scrollWheelZoom.disable(); }});
  L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }}).addTo(map);
  LIEUX.forEach(function (d) {{
    var marker = L.circleMarker([d.lat, d.lon], {{
      radius: 8, weight: 2, color: "#fffdf6",
      fillColor: d.bcol || colorFor(d.verdict), fillOpacity: 0.95
    }}).addTo(map);
    var url = "l/" + encodeURIComponent(d.uid) + ".html";
    var lines = [];
    lines.push('<a class="carte-pop-nom" href="' + url + '">' + esc(d.nom) + '</a>');
    var vl = d.band_label;
    var vc = d.bcol || colorFor(d.verdict);
    if (vl) {{
      lines.push('<span class="carte-pop-verdict" style="color:' + vc + '">' + esc(vl) + '</span>');
    }}
    var meta = [];
    if (d.v3susp) meta.push("note suspendue");
    else if (d.v3note != null) meta.push("libération " + esc(d.v3note) + "/100");
    if (meta.length) lines.push('<span class="carte-pop-meta">' + meta.join(" · ") + '</span>');
    if (d.commune) lines.push('<span class="carte-pop-lieu">' + esc(d.commune) + '</span>');
    lines.push('<a class="carte-pop-link" href="' + url + '">Voir la fiche →</a>');
    marker.bindPopup('<div class="carte-pop">' + lines.join("") + '</div>');
    marker.bindTooltip(esc(d.nom));
  }});
}})();
</script>"""
    return page("Carte", body, "carte.html", project=project,
                description="Carte interactive des lieux de l'annuaire des montages de libération des terres en France.",
                path="carte.html", link_gloss=False)


# ─────────────────────────────────────────────────────────────────────────────
# Pages — grilles
# ─────────────────────────────────────────────────────────────────────────────

def render_grilles(cfg):
    project = cfg["concepts"]["project"]
    grilles = cfg["grilles"]["grilles"]
    axes_cfg = cfg["ranking"]["axes"]
    axe_name = {a["id"]: a["label"] for a in axes_cfg}

    blocks = []
    catorder = [("porteur", "Porteurs de nue-propriété"),
                ("usufruitier", "Organismes usufruitiers"),
                ("lieu", "Lieux")]
    for cat, lab in catorder:
        g = grilles[cat]
        fam_html = []
        for fam in g["familles"]:
            crit = []
            for cr in fam["criteres"]:
                crit.append(f"""<tr>
  <td class="crit-name"><span class="axe-dot axe-{cr['axe']}"></span>{e(cr['label'])}</td>
  <td class="crit-axe">{e(axe_name[cr['axe']])}</td>
  <td class="num">{cr['poids']}</td>
  <td class="crit-def">{e(clean(cr['definition']))}</td>
</tr>""")
            fam_html.append(f'<tr class="fam-row"><th colspan="4" scope="colgroup">{e(fam["label"])}</th></tr>'
                            + "".join(crit))
        ls = g["lecture_strategique"]
        def lst(x):
            return "".join(f"<li>{e(clean(i))}</li>" for i in x)
        blocks.append(f"""<section class="grille-block" id="grille-{cat}">
<h2 class="sec">{e(lab)}</h2>
<p class="prose">{e(clean(g['objet']))}</p>
<div class="table-scroll" tabindex="0" role="region" aria-label="Critères de la grille {e(lab)}"><table class="grille-tbl">
<caption class="visually-hidden">Critères de lecture de la grille {e(lab)} : axe, poids et définition.</caption>
<thead><tr><th scope="col">Critère de lecture</th><th scope="col">Axe</th><th scope="col">Poids</th><th scope="col">Définition</th></tr></thead>
<tbody>{''.join(fam_html)}</tbody></table></div>
<div class="strat">
  <h3>Lecture stratégique</h3>
  <p class="prose"><strong>Enjeu.</strong> {e(clean(ls['enjeu']))}</p>
  <div class="analyse-grid">
    <div class="an-col an-forces"><h3>Forces typiques</h3><ul>{lst(ls['forces_typiques'])}</ul></div>
    <div class="an-col an-frag"><h3>Fragilités typiques</h3><ul>{lst(ls['fragilites_typiques'])}</ul></div>
    <div class="an-col an-lev"><h3>Leviers</h3><ul>{lst(ls['leviers'])}</ul></div>
  </div>
</div>
</section>""")

    body = f"""<h1>Grilles de lecture et d'analyse stratégique</h1>
<div class="callout callout-warn"><p><strong>Grille héritée (v2).</strong> Cette page détaille la grille d'analyse à cinq axes (sol · structure · pouvoir · finalité · usage) qui a précédé <a href="methode.html">le faisceau libéré</a>. L'annuaire note désormais chaque montage selon <strong>la porte et les six questions</strong> du faisceau ; cette page est conservée comme <em>matériau de référence et d'archive</em>, non comme la grille courante.</p></div>
<p class="lead">Chaque catégorie de l'annuaire est lue à travers une grille
dédiée. Une grille combine des <strong>critères de lecture</strong> — chacun
rattaché à un axe du classement et pondéré — et une <strong>lecture
stratégique</strong> qui cadre les enjeux, forces, fragilités et leviers
propres à la catégorie. Toute fiche évalue ces critères (oui · partiel · non ·
inconnu) ; le score en découle directement.
<a href="regimes.html">Le cadre des régimes et des pôles du sol →</a></p>
<p class="axe-legend">{axe_legend(axes_cfg, "Cinq axes : ")}</p>
{''.join(blocks)}
<p class="linkrow"><a href="methode.html">La méthode et le calcul de la note →</a> ·
<a href="regimes.html">Régimes et pôles du sol →</a> ·
<a href="glossaire.html">Glossaire des termes →</a></p>"""
    return page("Grilles", body, "grilles.html", project=project,
                description="Les trois grilles de lecture et d'analyse stratégique de l'annuaire.",
                path="grilles.html")


# ─────────────────────────────────────────────────────────────────────────────
# Page — trois régimes du sol
# ─────────────────────────────────────────────────────────────────────────────

def render_regimes(cfg):
    project = cfg["concepts"]["project"]
    reg = cfg["concepts"].get("regimes", {}) or {}
    anti = cfg["concepts"].get("anti_concepts", []) or []
    liste = reg.get("liste", []) or []

    # trois blocs courts, un par régime
    cards = ""
    for r in liste:
        cards += f"""<div class="regime-card">
  <h3>{e(clean(r.get('label','')))}</h3>
  <p class="regime-outils"><strong>Outils.</strong> {e(clean(r.get('outils','')))}</p>
  <p class="regime-but"><strong>Finalité.</strong> {e(clean(r.get('but','')))}</p>
  <p class="regime-role">{e(clean(r.get('role','')))}</p>
</div>"""

    # tableau comparatif — structure stable, en dur
    tbl_rows = [
        ("Outil juridique type",
         "Démembrement, fondation, fonds de dotation, bail long, association, SCIC",
         "Société commerciale, parts ou actions cessibles",
         "Pleine propriété individuelle (art. 544 C. civ.)"),
        ("Finalité",
         "Usage collectif d'intérêt général",
         "Profit, valorisation du capital",
         "Jouissance et transmission privées"),
        ("Lucrativité",
         "Non lucratif, gestion désintéressée",
         "Lucratif par construction",
         "Indifférente (usage privé)"),
        ("Cessibilité du foncier",
         "Verrouillée (inaliénabilité, dévolution)",
         "Libre — parts cessibles, revente",
         "Libre"),
        ("Rapport au marché",
         "Soustrait durablement",
         "Soumis, voire spéculatif",
         "Soumis, sans visée spéculative"),
        ("Gouvernance",
         "Collective, ouverte, « une voix par personne »",
         "Proportionnelle au capital",
         "Individuelle"),
        ("Place dans l'annuaire",
         "Régime de référence (noté)",
         "Repoussoir — sauf si neutralisé",
         "Point de départ, non référencé"),
    ]
    trs = "".join(
        f"<tr><th scope=\"row\">{e(c)}</th><td>{e(a)}</td><td>{e(b)}</td>"
        f"<td>{e(d)}</td></tr>"
        for c, a, b, d in tbl_rows)
    table = f"""<div class="table-scroll" tabindex="0" role="region" aria-label="Tableau comparatif des trois régimes du sol"><table class="rank-tbl regimes-tbl">
<caption class="visually-hidden">Comparaison des trois régimes du sol selon
sept critères.</caption>
<thead><tr><th scope="col">Critère</th>
<th scope="col">Droit civil / intérêt général</th>
<th scope="col">Droit commercial</th>
<th scope="col">Propriété privée classique</th></tr></thead>
<tbody>{trs}</tbody></table></div>"""

    anti_html = ""
    if anti:
        items = "".join(f"<li>{e(clean(x))}</li>" for x in anti)
        anti_html = f"""<section><h2 class="sec">Aux frontières du modèle</h2>
<p class="prose">L'annuaire se définit aussi par contraste. Ne sont
<strong>pas</strong> référencés :</p>
<ul class="prose">{items}</ul></section>"""

    paradoxe = ""
    if reg.get("paradoxe"):
        paradoxe = (f'<div class="callout callout-note"><p>'
                    f'<strong>Un régime n\'est pas une fatalité.</strong> '
                    f'{e(clean(reg["paradoxe"]))}</p></div>')

    # triptyque usus / fructus / abusus — ossature, lu depuis concepts["triptyque"].
    tri = cfg["concepts"].get("triptyque", {}) or {}
    triptyque_html = ""
    if tri.get("droits"):
        droit_cards = "".join(
            f"""<div class="regime-card">
  <h3>{e(clean(d.get('label','')))}</h3>
  <p class="enclair">{e(clean(d.get('en_clair','')))}</p>
  <p class="regime-but"><strong>Au sens du droit.</strong> {e(clean(d.get('definition','')))}</p>
  <p class="regime-role">{e(clean(d.get('portee_modele','')))}</p>
</div>""" for d in tri["droits"])
        verif = ""
        if tri.get("verification"):
            verif = (f'<p class="prose"><strong>Vérifier la posture par la '
                     f'nature.</strong> {e(clean(tri["verification"]))}</p>')
        triptyque_html = f"""<section><h2 class="sec" id="triptyque">Les trois pouvoirs du propriétaire : usus, fructus, abusus</h2>
<p class="lead">{e(clean(tri.get('en_clair','')))}</p>
<p class="prose">{e(clean(tri.get('chapeau','')))}</p>
<div class="regime-grid">{droit_cards}</div>
{verif}
</section>"""

    # cinq pôles — profils de référence sur le triptyque, lus depuis concepts["poles"].
    poles = cfg["concepts"].get("poles", {}) or {}
    poles_liste = poles.get("liste", []) or []
    poles_html = ""
    if poles_liste:
        pole_cards = "".join(
            f"""<div class="pole-card">
  <p class="pole-rang">Pôle {p.get('rang','')}</p>
  <h3>{e(clean(p.get('label','')))}</h3>
  <p class="enclair">{e(clean(p.get('en_clair','')))}</p>
  <p class="pole-role">{e(clean(p.get('role','')))}</p>
  <p class="pole-line"><strong>Usus.</strong> {e(clean(p.get('usus','')))}</p>
  <p class="pole-line"><strong>Fructus.</strong> {e(clean(p.get('fructus','')))}</p>
  <p class="pole-line"><strong>Abusus.</strong> {e(clean(p.get('abusus','')))}</p>
  <p class="pole-line"><strong>En un mot.</strong> {e(clean(p.get('logique','')))}</p>
</div>""" for p in poles_liste)
        registres = poles.get("registres", {}) or {}
        reg_html = ""
        if registres.get("chapeau"):
            reg_html = f"""<p class="prose">{e(clean(registres.get('chapeau','')))}</p>"""
        poles_html = f"""<section><h2 class="sec" id="poles">Les cinq pôles</h2>
<p class="lead">{e(clean(poles.get('en_clair','')))}</p>
<p class="prose">Ces trois régimes se précisent en cinq pôles : cinq profils de
référence sur le triptyque. Ils dédoublent les deux régimes où la qualification
se joue — le droit civil d'intérêt général se scinde entre le commun libre et
vivant et l'intérêt général institué, le droit commercial entre le mutualisme
d'usagers et l'économie sociale marchande — la propriété privée demeurant un
pôle unique.</p>
<p class="prose">{e(clean(poles.get('chapeau','')))}</p>
<div class="pole-grid">{pole_cards}</div>
{reg_html}
</section>"""

    body = f"""<h1>Régimes et pôles du sol</h1>
<p class="lead">{e(clean(reg.get('chapeau','')))}</p>

<section><h2 class="sec">Les trois régimes</h2>
<div class="regime-grid">{cards}</div>
{paradoxe}
</section>

<section><h2 class="sec">Tableau comparatif</h2>
{table}
</section>

{triptyque_html}

{poles_html}

{anti_html}

<p class="prose">La grille de notation traduit ce cadre par <strong>la porte et six
questions</strong> : voir les <a href="grilles.html">grilles d'analyse</a>. Le calcul
de la note est détaillé dans la <a href="methode.html">méthode</a> ; les termes
pivots sont définis au <a href="glossaire.html">glossaire</a>.</p>"""
    # données structurées : les trois régimes en DefinedTermSet, bâti depuis la
    # même source que le HTML (audit SEO C, I1).
    termset = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Régimes et pôles du sol",
        "description": meta_desc(reg.get("chapeau", "")),
        "inLanguage": "fr",
        "url": canonical_url("regimes.html"),
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": clean(r.get("label", "")),
             "description": clean(r.get("but", "")),
             "inDefinedTermSet": canonical_url("regimes.html")}
            for r in liste
        ],
    }
    return page("Régimes et pôles du sol", body, "regimes.html", project=project,
                description="Les trois régimes juridiques du foncier et les cinq "
                            "pôles : droit civil d'intérêt général, droit "
                            "commercial, propriété privée classique.",
                path="regimes.html", jsonld=[termset])


# ─────────────────────────────────────────────────────────────────────────────
# Pages — méthode
# ─────────────────────────────────────────────────────────────────────────────

def render_methode(cfg, n_by_cat, all_sc):
    project = cfg["concepts"]["project"]
    ranking = cfg["ranking"]
    cc = cfg["concepts"]["concept_central"]
    n_total_fiches = len(all_sc)
    notees = [(f, sc) for f, sc in all_sc
              if f["categorie"] != "modele" and sc.get("idl") is not None]
    n_notees = len(notees)
    n_susp = sum(1 for f, sc in all_sc
                 if f["categorie"] != "modele" and sc.get("palier") and sc.get("idl") is None)
    n_sur_echelle = n_notees + n_susp
    Q_CARDS_CFG = [
        ("1", "Le milieu", "#7a5230", "Le sol, l'eau, la terre sont-ils ménagés plutôt qu'exploités ?",
         "Ce qui est fait au vivant non-humain du lieu : sol vivant, eau, haies, pratiques de soin."),
        ("2", "Le vivant", "#3d7a4e", "Le non-humain a-t-il une place faite pour lui ?",
         "Habitat partagé avec le vivant : espaces rendus, biodiversité, place effective au-delà de l'usage humain."),
        ("3", "L'ouverture", "#2f6e8f", "Le lieu est-il ouvert au-dela de ceux qui l'habitent ?",
         "Hospitalité, vocation d'intérêt général, accueil — par opposition à l'entre-soi clos."),
        ("4", "Le don", "#8a5a8a", "L'accès relève-t-il du don plutôt que du paiement ?",
         "L'usage se gagne-t-il par l'appartenance et l'entraide, ou reste-t-il une redevance, un loyer, un billet ?"),
        ("5", "La durée", "#b08a3e", "Les usagers peuvent-ils rester — le titre d'usage est-il solide et long ?",
         "La sécurité d'usage dans le temps : bail long, statut stable, impossibilité d'être délogé du jour au lendemain."),
        ("6", "La voix", "#225588", "Ceux qui vivent le lieu décident-ils vraiment ?",
         "Autogouvernance réelle des usagers — par opposition à une gestion descendante, d'en haut."),
    ]
    Q_CARDS = "".join(
        f'<div class="axe-card" style="--c:{c}"><h3>{i} &middot; {e(lab)}</h3>'
        f'<p class="axe-q">{e(q)}</p><p>{e(d)}</p></div>'
        for i, lab, c, q, d in Q_CARDS_CFG)
    BANDS_V3 = [
        ("marchand", "#9a9a9a", "0-20", "Rien n'est sorti du marché — la porte n'est pas franchie."),
        ("en transition", "#a86a4a", "20", "La porte n'est que partielle : la valeur n'est pas pleinement soustraite."),
        ("sorti du marché", "#b08a3e", "20-50", "Le foncier est hors-marché, mais l'usage n'est pas encore rendu à un collectif."),
        ("autogéré", "#3d7a4e", "50-75", "Porte franchie, et les usagers décident et peuvent rester (voix + durée tenues)."),
        ("usage libéré", "#2f6e8f", "75-90", "En plus, l'accès relève du don plus que du paiement."),
        ("commun vivant", "#224477", "90-100", "Le faisceau est entier, et la place du vivant est tenue."),
    ]
    bands_html = "".join(
        f'<tr><td><span class="pal-chip" style="--pal:{col}">{e(lab)}</span></td>'
        f'<td class="num">{seuil}</td><td>{e(sens)}</td></tr>'
        for lab, col, seuil, sens in BANDS_V3)
    tri = cfg["concepts"].get("triptyque", {}) or {}
    triptyque_html = f"""<section id="triptyque"><h2 class="sec">Les trois pouvoirs du propriétaire : usus, fructus, abusus</h2>
<p class="enclair">{e(clean(tri.get('en_clair','')))}</p>
<p class="prose"><strong>La formule.</strong> {e(clean(cc.get('formule','')))}</p>
<p class="prose">Usus (utiliser), fructus (en tirer un revenu), abusus (en disposer
jusqu'à détruire) : libérer une terre, c'est ré-agencer collectivement ces trois
pouvoirs — au fond, ce que teste <em>la porte</em>. Le détail des trois droits,
avec les pôles et la typologie de montage, est sur la page
<a href="regimes.html#triptyque">Régimes et pôles du sol</a>.</p>
</section>"""
    verdict_html = """<section id="verdict"><h2 class="sec">Statut de l'évaluation</h2>
<p class="prose"><strong>Ce qu'est la note — et ce qu'elle n'est pas.</strong> La note de
libération est une <strong>lecture argumentée à partir d'informations publiques</strong>,
pas une mesure objective ni une vérité sur le lieu ou ses acteurs. On note
<strong>un degré de sortie du marché, pas un lieu</strong> ; la critique porte sur le
<em>montage</em>, jamais sur les personnes. Comme tout indice, le faisceau agrège des
critères choisis selon un cadre assumé — celui d'une économie citoyenne, non lucrative et
d'intérêt général. Ce cadre est <strong>daté, signé, contestable</strong> et appelle la
critique.</p>
<p class="prose"><strong>Le chiffre est calculé, jamais saisi.</strong> Ce qui est renseigné,
ce sont seulement les faits — la porte et les six questions ; la bande, la suspension, le
point faible et le badge en sont <em>dérivés</em> à la publication. Un pseudo-portage ne peut
donc pas afficher une bande haute : la porte le bloque, quoi qu'on saisisse ailleurs.</p>
<p class="prose"><strong>Droit de réponse.</strong> Parce que c'est une lecture et non un
arrêt, tout porteur, usufruitier ou collectif peut répondre : sa réponse est reproduite sur la
fiche concernée, sans retouche. <a href="droit-de-reponse.html">La page droit de réponse →</a></p>
</section>"""
    body = f"""<h1>Méthode</h1>
<p class="lead">Comment l'annuaire recense, lit et note les montages de
libération des terres — selon <strong>le faisceau libéré</strong> : une porte, six questions,
une échelle lue au point le plus faible.</p>
<nav class="page-toc" aria-label="Sommaire de la page">
  <a href="#corpus">Ce que recense l'annuaire</a>
  <a href="#triptyque">Les trois pouvoirs du propriétaire</a>
  <a href="#indice">La note de libération</a>
  <a href="#chaine">La chaîne, et la note d'un groupe</a>
  <a href="#verdict">Statut de l'évaluation</a>
  <a href="#integrite">L'intégrité du montage</a>
  <a href="#limites">Limites</a>
  <a href="#etat">État du corpus</a>
</nav>
<section id="corpus"><h2 class="sec">Ce que recense l'annuaire</h2>
<p class="enclair">{e(clean(cc.get('en_clair','')))}</p>
<p class="prose">« Terres Libérées » recense des lieux français où le foncier a
été soustrait au marché spéculatif par dissociation de la propriété et de
l'usage : <strong>l'un possède la terre sans s'en servir</strong> (le porteur de
nue-propriété), <strong>l'autre s'en sert sans la posséder</strong> (l'organisme
usufruitier). {e(clean(cc['definition']))}</p>
<p class="prose"><strong>Ressort juridique.</strong> {e(clean(cc['ressort_juridique']))}</p>
<p class="prose"><strong>Verrou central.</strong> {e(clean(cc['verrou_cle']))}</p>
</section>
{triptyque_html}
<section id="indice"><h2 class="sec">La note de libération — la porte et les six questions</h2>
<p class="prose"><strong>D'abord, la porte.</strong> Avant toute note, une question
préalable : la valeur du lieu est-elle <strong>soustraite au marché</strong> ? Si rien n'en
est sorti, le montage reste <em>marchand</em> et n'entre pas sur l'échelle. La porte franchie
— partiellement, ou pour toujours quand le bien est rendu inaliénable — on lit alors six
questions, du lieu vers le groupe.</p>
<div class="axe-cards">{Q_CARDS}</div>
<p class="prose"><strong>Quatre réponses possibles.</strong> Chaque question se lit
<strong>&#9679; tenu</strong>, <strong>&#9680; partiel</strong>, <strong>&#9675; absent</strong>, ou
<strong>non établi</strong> quand nos sources ne permettent pas de trancher. Le « non établi »
n'est jamais compté comme un zéro, ni au désavantage du lieu : il appelle une pièce, pas un
jugement.</p>
<p class="prose"><strong>L'échelle monte par paliers — sans sauter de marche.</strong>
On part du bas et l'on franchit chaque palier à condition de tenir le précédent : porte &#9679; →
plancher <em>sorti du marché</em> ; puis <em>voix</em> &#9679; et <em>durée</em> &#9679; → <em>autogéré</em> ;
puis <em>don</em> &#9679; → <em>usage libéré</em> ; enfin la place du vivant (le badge) → <em>commun
vivant</em>.</p>
<table class="rank-tbl small">
<caption class="visually-hidden">Paliers de la note de libération : seuil et sens.</caption>
<thead><tr><th scope="col">Palier</th><th scope="col" class="num">Seuil</th><th scope="col">Sens</th></tr></thead>
<tbody>{bands_html}</tbody></table>
<p class="prose"><strong>On lit au point le plus faible du chemin — une force ne rachète pas
une faille.</strong> La position dans la bande suit la plus faible des questions <em>du
chemin</em> (porte, voix, durée, don). Un lieu solide partout mais où l'on ne décide pas reste
bas : la faiblesse commande, elle ne se moyenne pas avec les forces.</p>
<p class="prose"><strong>Le chiffre est indicatif ; la bande fait foi.</strong> Le nombre
(0-100) situe à l'intérieur de la bande, donné en <strong>fourchette</strong> « du sûr à
l'estimé ». Ce qui est robuste, c'est la <strong>bande</strong>, le <strong>profil des six
questions</strong> et le <strong>point faible</strong> — pas la décimale.</p>
<p class="prose"><strong>Ne pas savoir suspend la note.</strong> Si une question
<em>décisive</em> (la porte, la voix, la durée) est non établie, on <strong>suspend</strong> :
pas de chiffre, seulement le palier atteint avec certitude, et la pièce manquante marquée comme
une dette datée. Suspendre est une honnêteté, pas une faiblesse — un lieu remarquable peut
rester suspendu si la pièce manque de notre côté.</p>
<p class="prose"><strong>Le badge « Sanctuaire » est à côté de la note, jamais dedans.</strong>
Le milieu et le vivant nourrissent un <strong>badge écologique</strong> (🌿 / 🌿🌿) qui dit le
soin du lieu pour le vivant, <em>séparément</em> du chiffre. Un domaine de conservation peut
ainsi être écologiquement exemplaire <em>et</em> avoir une note de libération basse parce que
l'usage n'y est pas encore rendu : les deux informations cohabitent sans s'effacer.</p>
</section>
<section id="chaine"><h2 class="sec">La chaîne, et la note d'un groupe</h2>
<p class="prose">Le faisceau n'évalue pas un lieu isolé mais toute la <strong>chaîne</strong>,
réparti entre ses maillons : la <strong>porte</strong> → le porteur ; le <strong>milieu</strong>
et le <strong>vivant</strong> → le lieu ; l'<strong>ouverture</strong> et le <strong>don</strong>
→ la chaîne ; la <strong>durée</strong> et la <strong>voix</strong> → l'usufruitier. Le lieu est
l'assemblage où tout converge — d'où son <strong>étoile complète à six branches</strong>.</p>
<p class="prose"><strong>Noter un porteur, un usufruitier, un réseau.</strong> Pas de grille à
part : on les note sur les <strong>six mêmes questions</strong>, par <strong>agrégation des
lieux</strong> qu'ils tiennent, animent ou fédèrent — on juge un porteur par ce qu'il libère
réellement. Un pseudo-portage tire ses lieux vers le bas : l'agrégat le contient. Sous l'étoile,
le <strong>type de portage</strong> (verrou pour toujours · portage solide · partiel ·
pseudo-portage) éclaire la note sans s'y substituer. Un groupe sans lieu agrégeable dans
l'annuaire reste <strong>non noté</strong>.</p>
</section>
{verdict_html}
<section id="integrite"><h2 class="sec">L'intégrité du montage</h2>
<p class="prose">{e(clean(ranking['integrite_montage']['question']))}</p>
<p class="prose">{e(clean(ranking['integrite_montage']['note_lecture']))}
Cet indicateur complémentaire n'entre pas dans la note : il
<strong>situe</strong> le montage parmi les cinq pôles sans les hiérarchiser.
Le cadre des régimes et des cinq pôles est sur la
page <a href="regimes.html#poles">Régimes et pôles du sol</a>.</p>
</section>
<section id="limites"><h2 class="sec">Limites</h2>
<ul class="prose">
<li>Les fiches reposent sur des <strong>sources publiques</strong> ; les montages réels peuvent
être plus précis ou avoir évolué. Chaque fiche distingue les faits vérifiés des
points non confirmés, et tout acteur dispose d'un droit de réponse.</li>
<li>La note est une lecture au regard d'un cadre explicite, reproductible et
contestable — non un label.</li>
<li>Ce qu'on ne peut établir reste « non établi » et peut suspendre la note ; on ne devine pas.</li>
<li>Le « montage de référence » (nue-propriété d'intérêt général + usufruit
associatif) est un idéal-type ; peu de lieux réels le réalisent à la lettre.</li>
<li>Le corpus est construit et non exhaustif ; sa composition — sous-représentation
de l'habitat et de l'Outre-mer notamment — est détaillée dans l'<a href="#etat">État
du corpus</a>.</li>
</ul>
</section>
<section id="etat"><h2 class="sec">État du corpus</h2>
<p class="prose">{n_by_cat['lieu']} lieux · {n_by_cat['porteur']} porteurs de
nue-propriété · {n_by_cat['usufruitier']} organismes usufruitiers ·
{n_by_cat['modele']} modèles voisins de comparaison. Les {n_total_fiches}
fiches sont publiées ; le corpus est construit, non exhaustif. <strong>{n_sur_echelle}</strong>
entrées sont situées sur l'échelle du faisceau : <strong>{n_notees}</strong> portent une note
chiffrée et <strong>{n_susp}</strong> sont <strong>suspendues</strong> (une question décisive
n'est pas documentée — on n'affiche alors que le palier atteint avec certitude, jamais un chiffre
deviné). Les autres entrées (groupes sans lieu agrégeable, modèles voisins) restent non situées.</p>
{corpus_histogram(all_sc, ranking)}
<p class="prose"><strong>Posture du recensement.</strong> Le projet regarde le
sujet depuis la tradition de l'<strong>éducation populaire</strong> et des
<strong>mouvements citoyens non-commerciaux</strong>. Il cherche les formes les
plus pleinement non-marchandes ; les lieux qui s'en écartent — par la nature
commerciale d'un maillon, une logique locative rentière, une gouvernance
descendante — sont décrits avec la <strong>même grille</strong> que les autres, et
leur palier en rend compte.</p>
<p class="prose"><strong>Ce que le corpus ne couvre pas encore.</strong> Le
recensement est très majoritairement rural et agricole ; l'habitat coopératif,
le foncier solidaire urbain et le périurbain restent peu représentés.
Géographiquement, les lieux se concentrent sur la moitié sud et est de la
métropole ; plusieurs régions et l'ensemble de l'Outre-mer ne sont pas couverts.
Ces manques sont des pistes d'enrichissement, non des choix d'exclusion.</p>
</section>
<section><h2 class="sec">Aller plus loin</h2>
<p class="prose">Pour le détail du cadre et des grilles : la page
<a href="regimes.html">Régimes et pôles du sol</a> expose l'opposition droit
civil d'intérêt général / droit commercial / propriété privée ; les
<a href="grilles.html">grilles d'analyse</a> détaillent les critères de chaque
catégorie ; le <a href="glossaire.html">glossaire</a> définit les termes
pivots ; les <a href="modeles.html">modèles voisins</a> servent de points de
comparaison hors classement.</p>
<p class="prose"><strong>Accompagnement.</strong> <a href="ce-que-la-note-ne-dit-pas.html">Ce que la note ne dit pas</a> · <a href="faq.html">Questions fréquentes</a> · <a href="exemples.html">Trois exemples calculés pas à pas</a> · <a href="droit-de-reponse.html">Droit de réponse</a>.</p>
</section>"""
    return page("Méthode", body, "methode.html", project=project,
                description="Méthode de l'annuaire : le faisceau libéré — la porte, les six questions, l'échelle de libération.",
                path="methode.html")


# ─────────────────────────────────────────────────────────────────────────────
# Page — glossaire
# ─────────────────────────────────────────────────────────────────────────────

GLOSSAIRE = [
    ("Libération des terres",
     "Ensemble de pratiques visant à soustraire durablement un foncier à la "
     "logique spéculative et marchande, pour le placer au service d'un usage "
     "défini collectivement et d'intérêt général. Le terme n'est pas un "
     "concept juridique codifié."),
    ("Décommodifié / décommodification",
     "Retirer un bien du commerce : il ne peut plus être acheté, vendu ni loué "
     "pour le profit. Une terre décommodifiée est sortie du marché — elle cesse "
     "d'être une marchandise. Terme savant pour ce que l'annuaire appelle, en "
     "clair, « retirer la terre du marché »."),
    ("Démembrement",
     "Division du droit de propriété (article 544 du Code civil) en deux "
     "droits distincts confiés à des titulaires différents : la nue-propriété "
     "et l'usufruit. On parle aussi de dissociation de la propriété et de "
     "l'usage : dans l'annuaire, les deux termes désignent la même opération."),
    ("Nue-propriété",
     "Droit de propriété privé de l'usage et des revenus du bien : le "
     "nu-propriétaire détient le bien mais n'en a ni l'usage ni la jouissance. "
     "Dans l'annuaire, elle est portée par un organisme d'intérêt général."),
    ("Usufruit",
     "Droit d'user d'un bien et d'en percevoir les revenus sans en être "
     "propriétaire (articles 578 et suivants du Code civil). Constitué au "
     "profit d'une personne morale, il ne peut excéder 30 ans."),
    ("Bail rural",
     "Contrat par lequel un propriétaire confie l'exploitation d'un fonds "
     "agricole à un preneur. D'une durée minimale de neuf ans, il ouvre un "
     "droit au renouvellement d'ordre public."),
    ("Bail emphytéotique",
     "Bail de très longue durée — de 18 à 99 ans — qui confère au preneur un "
     "droit réel sur le bien, proche de la propriété pour la durée du contrat, "
     "en échange d'une redevance modique."),
    ("Fonds de dotation",
     "Personne morale de droit privé à but non lucratif (loi du 4 août 2008) "
     "qui reçoit et gère des biens pour réaliser une œuvre d'intérêt général "
     "ou les redistribuer à un organisme poursuivant un tel but."),
    ("Dotation consomptible / non consomptible",
     "Une dotation est dite non consomptible lorsque les biens qui la "
     "composent ne peuvent pas être vendus ou dépensés : seuls leurs revenus "
     "sont utilisés. La dotation est consomptible lorsque le fonds peut "
     "entamer le capital lui-même. Pour un fonds de dotation portant du "
     "foncier, le caractère non consomptible rend la terre juridiquement très "
     "difficile à sortir : c'est un verrou central des montages de l'annuaire."),
    ("Bail réel solidaire",
     "Bail de longue durée (le BRS) par lequel un organisme de foncier "
     "solidaire dissocie durablement la propriété du terrain, qu'il conserve, "
     "de la propriété du bâti, cédée au ménage. Il encadre les prix de "
     "revente pour maintenir des logements abordables sur le long terme."),
    ("Fondation RUP",
     "Fondation reconnue d'utilité publique : organisme sans but lucratif "
     "doté de la personnalité morale par décret, voué à une mission d'intérêt "
     "général et soumis à un contrôle de l'État."),
    ("Intérêt général",
     "Catégorie juridique octroyée par l'État : reconnaissance d'utilité "
     "publique, agrément, qualification fiscale. Caractère d'une activité non "
     "lucrative, à gestion désintéressée, ouverte, qui ne profite pas à un "
     "cercle restreint. Condition centrale de plusieurs montages de l'annuaire — "
     "mais à distinguer du commun : l'intérêt général est institué par l'État, "
     "le commun se définit par la gouvernance citoyenne, ni étatique ni "
     "marchande."),
    ("Intérêt général d'initiative citoyenne",
     "Finalité d'intérêt général affirmée par la nature et la posture d'un "
     "collectif citoyen, avant et indépendamment de toute reconnaissance "
     "étatique. C'est le repère du projet : non l'intérêt général institué par "
     "l'État, mais la gouvernance citoyenne tournée vers le bien commun."),
    ("Commun",
     "Mode d'organisation d'une ressource qui n'est ni étatique ni marchand : "
     "gouvernance collective des usagers, finalité ouverte. Troisième pôle, "
     "distinct de l'intérêt général institué comme de la propriété privée."),
    ("Agrégation non compensatoire",
     "En clair : l'axe le plus faible commande — une force ne rachète pas une "
     "faiblesse. C'est le principe du faisceau : on lit la note au point le plus "
     "faible du chemin (la porte, la voix, la durée, le don). Un montage solide "
     "partout mais effondré sur une question décisive ne peut afficher une note "
     "élevée. « Lecture non compensatoire » "
     "est l'étiquette technique de cette règle."),
    ("Chaîne",
     "Un montage de libération des terres n'est pas une entité isolée mais une "
     "chaîne : un lieu, son porteur de nue-propriété, son organisme "
     "usufruitier. La qualité d'un porteur ou d'un usufruitier se lit à travers "
     "les montages qu'il noue effectivement."),
    ("Palier de libération",
     "La bande où se situe une entrée sur l'échelle du faisceau : marchand, en "
     "transition, sorti du marché, autogéré, usage libéré, commun vivant. Elle "
     "ne se saisit pas : elle découle de la porte et des six questions, lues au "
     "point le plus faible. Du marchand (rien n'est sorti du marché) au commun "
     "vivant (le faisceau entier, la place du vivant tenue)."),
    ("Condition du sommet (commun vivant)",
     "Le palier le plus haut — commun vivant — n'est atteint que si le faisceau "
     "est entier : porte franchie, usage rendu (voix et durée tenues), accès "
     "relevant du don, et la place du vivant tenue (le badge écologique). Il "
     "suffit qu'une marche manque pour rester en deçà. Rare — un horizon plus "
     "qu'une case à remplir."),
    ("Les maillons du faisceau",
     "Le faisceau n'évalue pas un lieu isolé mais toute la chaîne, réparti entre "
     "ses maillons : la porte au porteur ; le milieu et le vivant au lieu ; "
     "l'ouverture et le don à la chaîne ; la durée et la voix à l'usufruitier. "
     "Le lieu est l'assemblage où tout converge."),
    ("Note d'un groupe (agrégation)",
     "Un porteur, un usufruitier ou un réseau n'a pas de grille à part : sa note "
     "agrège les six questions des lieux qu'il tient, anime ou fédère — on juge un "
     "groupe par ce qu'il libère réellement. Un pseudo-portage tire ses lieux vers "
     "le bas, et l'agrégat le contient ; un groupe sans lieu agrégeable reste non "
     "noté."),
    ("Faux ami",
     "Entité qui mobilise le vocabulaire du commun et de l'utilité sociale tout "
     "en étant structurellement commerciale et lucrative au profit d'un cercle "
     "fermé. On parle aussi de « communs-washing ». Cas-type : la société "
     "coopérative dont le bénéficiaire réel est le seul sociétariat."),
    ("Les trois pouvoirs du propriétaire (triptyque usus / fructus / abusus)",
     "Les trois droits que le droit civil reconnaît sur une chose : l'usus — "
     "s'en servir —, le fructus — en percevoir les revenus —, l'abusus — en "
     "disposer, jusqu'à vendre, transformer ou épuiser. Le commun n'invente pas "
     "un quatrième droit : il ré-agence les trois — fructus supprimé ou "
     "réinvesti, abusus neutralisé dans ses deux faces, usus partagé, y compris "
     "avec le vivant non-humain. C'est l'ossature du cadre d'évaluation."),
    ("Cinq pôles",
     "À l'intérieur et au travers des trois régimes du sol, le cadre situe cinq "
     "pôles — cinq profils de référence sur le triptyque usus/fructus/abusus : "
     "le commun libre et vivant, l'intérêt général institué, le mutualisme "
     "d'usagers, l'économie sociale marchande, la propriété marchande. Ce sont "
     "des profils de référence, non des cases."),
    ("Verrou d'actif (asset-lock)",
     "Clause statutaire interdisant que l'actif d'une structure soit capté à "
     "titre privé, y compris en cas de dissolution. Verrou central des montages "
     "qui neutralisent durablement la cessibilité du foncier."),
    ("Réserves impartageables",
     "Part des excédents d'une structure qui ne peut être distribuée aux "
     "membres et reste affectée à l'objet de la structure. Clause qui, comme le "
     "verrou d'actif, tempère ou neutralise la lucrativité."),
    ("Complétude",
     "Part des éléments d'une fiche effectivement documentés par nos sources. "
     "Une faible complétude signale les angles morts du recensement ; quand un "
     "point décisif manque, la note n'est pas devinée mais suspendue."),
    ("Utilité publique",
     "Reconnaissance officielle, par l'État, qu'un organisme ou un projet "
     "sert l'intérêt de la collectivité. Elle conditionne notamment le statut "
     "de fondation reconnue d'utilité publique."),
    ("Droit civil",
     "Branche du droit qui régit les rapports entre les personnes privées et "
     "leurs biens : propriété, démembrement, baux, associations, sociétés "
     "civiles. La libération des terres réemploie ces outils de droit civil, "
     "dans leur version non lucrative, pour soustraire le foncier au marché."),
    ("Droit commercial",
     "Branche du droit qui régit les commerçants et les sociétés "
     "commerciales. Une société commerciale poursuit en principe un but "
     "lucratif et ses parts ou actions sont, sauf clause contraire, librement "
     "cessibles. C'est le régime que l'annuaire prend pour repoussoir — sauf "
     "lorsque ses statuts en neutralisent la lucrativité."),
    ("Propriété privée",
     "Droit d'user, de jouir et de disposer d'un bien de la manière la plus "
     "absolue (article 544 du Code civil). La pleine propriété individuelle "
     "est le régime ordinaire du foncier : ni libération, ni spéculation, mais "
     "le point de départ que la libération des terres entend dépasser."),
    ("Spéculation foncière",
     "Acquisition d'un foncier dans l'attente d'une plus-value à la revente, "
     "plutôt que pour son usage. Les montages de l'annuaire visent à "
     "neutraliser cette logique, en verrouillant la cessibilité du foncier ou "
     "des parts qui en portent la valeur."),
    ("Note de libération",
     "Note de synthèse de 0 à 100 attribuée à chaque entrée de l'annuaire. "
     "Elle découle de la porte et des six questions du faisceau — le milieu, le "
     "vivant, l'ouverture, le don, la durée, la voix, "
     "l'usage — et résume la solidité du montage. L'axe le plus faible commande "
     "le résultat (voir « Agrégation non compensatoire »). Voir la page Méthode."),
    ("Intégrité du montage",
     "Indicateur complémentaire, non noté et non hiérarchique : il situe la "
     "chaîne du montage parmi cinq pôles, du commun libre et vivant à la "
     "propriété marchande, sans les classer. La protection effective du foncier est "
     "lue à part, par la porte du faisceau (le bien est-il soustrait au marché ?) "
     "et le profil des six questions."),
    ("Modèle voisin",
     "Montage de référence — français ou étranger — proche de l'idéal de "
     "libération des terres, recensé à titre de comparaison. Les modèles "
     "voisins ne sont pas notés par la grille de l'annuaire : ils restent "
     "descriptifs et hors du classement "
     "principal."),
    ("Idéal-type",
     "Construction de référence qui décrit un montage sous sa forme la plus "
     "pure, pour servir de point de comparaison. L'idéal-type n'a pas "
     "vocation à exister tel quel : peu de lieux réels le réalisent à la "
     "lettre, mais il aide à situer chaque cas concret."),
]


def render_glossaire(cfg):
    project = cfg["concepts"]["project"]
    items = "".join(
        f'<div class="gloss-item" id="g-{slugify(term)}">'
        f'<dt>{e(term)}</dt><dd>{e(defn)}</dd></div>'
        for term, defn in GLOSSAIRE)
    body = f"""<h1>Glossaire</h1>
<p class="lead">Définitions simples des termes pivots employés dans l'annuaire.
Pour le détail du calcul de la note, voir la <a href="methode.html">Méthode</a>.</p>
<dl class="glossaire">{items}</dl>
<p class="linkrow"><a href="methode.html">La méthode et le calcul de la note →</a> ·
<a href="regimes.html">Régimes et pôles du sol →</a> ·
<a href="grilles.html">Grilles d'analyse →</a></p>
<p class="backlink"><a href="index.html">← Retour à l'accueil</a></p>"""
    termset = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Glossaire — Terres Libérées",
        "url": canonical_url("glossaire.html"),
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": term, "description": defn,
             "url": canonical_url("glossaire.html") + f"#g-{slugify(term)}"}
            for term, defn in GLOSSAIRE
        ],
    }
    return page("Glossaire", body, "glossaire.html", project=project,
                description="Glossaire des termes de la libération des terres : "
                            "nue-propriété, usufruit, démembrement, intérêt général.",
                path="glossaire.html", jsonld=[termset], link_gloss=False)


# ─────────────────────────────────────────────────────────────────────────────
# Page — thèmes transversaux
# ─────────────────────────────────────────────────────────────────────────────

# Cinq thèmes transversaux : porte d'entrée par sujet, absente des catalogues
# (qui entrent par rôle) et du classement (qui entre par note). Répartition
# codée en dur — aucun champ ajouté aux YAML. Un uid peut figurer dans deux
# thèmes (recoupement assumé, cf. audit cycle D — thèmes).
THEMES = [
    ("foncier-agricole", "Foncier agricole et installation paysanne",
     "Terres cultivées sorties du marché pour installer ou maintenir des "
     "paysan·nes.",
     ["reseau-terre-de-liens", "lurzaindia", "larzac", "villarceaux", "nddl",
      "fondation-terre-de-liens", "fonciere-terre-de-liens", "lurzaindia-sca",
      "feve", "sctl", "gfa-mutuels", "champs-des-possibles", "reneta"]),
    ("habitat", "Habitat et logement non spéculatif",
     "Immeubles et écolieux dont la propriété du logement est déconnectée du "
     "marché.",
     ["village-vertical", "hameau-des-buis", "longo-mai", "habicoop",
      "fonciere-chenelet", "cooperative-oasis", "cooperatives-longo-mai",
      "cooperative-habitants-alur", "ofs-brs", "clt-bruxelles",
      "stiftung-trias", "mietshauser-syndikat"]),
    ("espaces-naturels", "Espaces naturels et protection de l'eau",
     "Foncier naturel ou sensible protégé pour des raisons écologiques.",
     ["conservatoire-littoral", "federation-cen", "scic-terres-de-sources",
      "nddl"]),
    ("portage-public", "Portage public et collectivités",
     "Montages où une personne publique détient ou sécurise le foncier.",
     ["larzac", "conservatoire-littoral", "scic-terres-de-sources",
      "federation-cen", "ofs-brs"]),
    ("portage-citoyen", "Portage citoyen et fondations",
     "Foncier sécurisé par l'épargne, les dons ou une fondation, hors "
     "puissance publique.",
     ["fondation-terre-de-liens", "fonciere-terre-de-liens",
      "fonds-la-terre-en-commun", "fonds-terre-europeenne", "fonciere-antidote",
      "fondation-fph", "lurzaindia-sca", "feve", "stiftung-trias"]),
]


def render_themes(all_sc, cfg):
    """Page « Thèmes » statique : 5 sections, une par thème transversal.
    Réutilise le composant de cartes existant ; aucun JS, aucun filtre."""
    project = cfg["concepts"]["project"]
    concepts = cfg["concepts"]
    axes_cfg = cfg["ranking"]["axes"]
    sc_by_uid = {f["uid"]: (f, sc) for f, sc in all_sc}

    toc = "".join(f'<a href="#theme-{tid}">{e(titre)}</a>'
                  for tid, titre, _, _ in THEMES)

    sections = []
    for tid, titre, cadrage, uids in THEMES:
        fiches_sc = [sc_by_uid[u] for u in uids if u in sc_by_uid]
        fiches_sc.sort(key=lambda x: x[1]["idl"] or 0, reverse=True)
        grid = cards_grid(fiches_sc, axes_cfg, concepts=concepts)
        sections.append(f"""<section id="theme-{tid}">
<h2 class="sec">{e(titre)}</h2>
<p class="lead">{e(cadrage)}</p>
{grid}
</section>""")

    body = f"""{tri_defs(Q6_CFG)}<h1>Thèmes transversaux</h1>
<p class="lead">Les catalogues classent l'annuaire par rôle dans le montage ;
le classement, par la note de libération. Cette page propose une troisième lecture, par
sujet : à quoi sert la terre, et qui la porte. Un même montage peut relever de
deux thèmes. <a href="methode.html">Comprendre la note et les six questions →</a></p>
<nav class="page-toc" aria-label="Sommaire des thèmes">{toc}</nav>
{bands_legend()}
{''.join(sections)}
<p class="backlink"><a href="index.html">← Retour à l'accueil</a></p>"""
    return page("Thèmes", body, "themes.html", project=project,
                description="Cinq thèmes transversaux pour explorer l'annuaire "
                            "par sujet : foncier agricole, habitat, espaces "
                            "naturels, portage public et citoyen.",
                path="themes.html")


# ─────────────────────────────────────────────────────────────────────────────
# Page — comparateur
# ─────────────────────────────────────────────────────────────────────────────

def render_comparer(all_sc, cfg):
    """Page « Comparer » : deux sélecteurs, rendu en deux colonnes côté client
    depuis data.json. Le HTML est quasi vide ; compare.js fait le rendu.
    Réutilise les styles de carte / axes existants."""
    project = cfg["concepts"]["project"]
    groups = {"lieu": [], "porteur": [], "usufruitier": [], "modele": []}
    for f, _ in all_sc:
        if f["categorie"] == "reseau":
            continue  # les réseaux ne sont pas notés : hors comparateur
        groups[f["categorie"]].append((f["uid"], f["nom"]))
    catlab = {"lieu": "Lieux", "porteur": "Porteurs",
              "usufruitier": "Usufruitiers", "modele": "Modèles voisins"}

    def opts():
        out = '<option value="">— Choisir —</option>'
        for cat, lab in catlab.items():
            items = sorted(groups[cat], key=lambda x: x[1])
            if not items:
                continue
            out += f'<optgroup label="{e(lab)}">'
            out += "".join(f'<option value="{e(u)}">{e(n)}</option>'
                            for u, n in items)
            out += '</optgroup>'
        return out

    selects = opts()
    body = f"""<h1>Comparer deux montages</h1>
<p class="lead">Choisissez deux entrées de l'annuaire pour voir leurs notes,
profils des six questions et caractéristiques en vis-à-vis.
<a href="methode.html">Comprendre la note →</a></p>
<p class="note">Comparer ce qui est comparable : la comparaison critère à
critère n'a de sens qu'entre entrées de même catégorie.
<a href="classement.html">Pourquoi ? →</a></p>
<div class="cmp-pickers">
  <label>Montage A <select id="cmp-a">{selects}</select></label>
  <label>Montage B <select id="cmp-b">{selects}</select></label>
</div>
<p id="cmp-warn" class="note" role="status" hidden></p>
<div class="cmp-grid" id="cmp-grid"></div>
<noscript><p class="no-result">La comparaison nécessite JavaScript. Vous pouvez
consulter chaque fiche depuis le <a href="classement.html">classement</a> ou
les <a href="lieux.html">catalogues</a>.</p></noscript>
<p class="backlink"><a href="classement.html">← Voir le classement complet</a></p>
<script defer src="assets/compare.js"></script>"""
    return page("Comparer", body, "comparer.html", project=project,
                description="Comparer deux montages de libération des terres : "
                            "indices, axes et caractéristiques en vis-à-vis.",
                path="comparer.html")


# ─────────────────────────────────────────────────────────────────────────────
# Page — accueil
# ─────────────────────────────────────────────────────────────────────────────

def render_index(all_sc, cfg, n_by_cat):
    project = cfg["concepts"]["project"]
    concepts = cfg["concepts"]
    ranking = cfg["ranking"]
    axes_cfg = ranking["axes"]
    core = sorted([(f, s) for f, s in all_sc
                   if f["categorie"] not in ("modele", "reseau")],
                  key=lambda x: x[1]["idl"] or 0, reverse=True)

    # 1.10 — meilleures entrées par catégorie (réutilise le tri de `core`, même
    # logique que render_classement) : 2 lieux, 2 porteurs, 2 usufruitiers.
    def _best(cat, n=2):
        return [(f, s) for f, s in core
                if f["categorie"] == cat and s.get("idl") is not None][:n]
    best_groups = [("lieu", "Lieux", _best("lieu")),
                   ("porteur", "Porteurs de nue-propriété", _best("porteur")),
                   ("usufruitier", "Organismes usufruitiers", _best("usufruitier"))]

    # chiffres-clés — verdicts déjà calculés sur les scores des lieux
    from collections import Counter as _Counter
    _verd = _Counter((s.get("verdict") or "a_etablir")
                     for f, s in all_sc if f["categorie"] == "lieu")
    n_lieux = n_by_cat["lieu"]
    n_hybride = _verd.get("hybride", 0)

    def _intention(titre, texte, liens):
        ls = " · ".join(f'<a href="{h}">{e(t)}</a>' for t, h in liens)
        return (f'<div class="intent-card"><h3>{e(titre)}</h3>'
                f'<p>{e(texte)}</p><p class="intent-links">{ls}</p></div>')
    intentions = "".join([
        _intention("Je découvre",
                   "Ce que « libérer une terre » veut dire, et le cadre qui le mesure.",
                   [("Le concept", "glossaire.html"), ("Régimes du sol", "regimes.html"),
                    ("La méthode", "methode.html")]),
        _intention("Je cherche un lieu",
                   "Parcourir les lieux recensés, sur la carte ou dans le catalogue.",
                   [("La carte", "carte.html"), ("Les lieux", "lieux.html"),
                    ("Le classement", "classement.html")]),
        _intention("Je veux la méthode",
                   "Comment chaque montage est lu, noté et situé — la grille de lecture.",
                   [("La méthode", "methode.html"), ("Les grilles", "grilles.html")]),
        _intention("Je suis chercheur·euse ou journaliste",
                   "Un référentiel citable : cadre explicite, statut du chiffre, versions datées.",
                   [("Statut de l'évaluation", "methode.html#verdict"),
                    ("Journal des versions", "changelog.html")]),
    ])

    hist = corpus_histogram(all_sc, ranking)

    # bandeau « À lire » — 3 récits du magazine, donnés à voir dès l'accueil
    _doss = load_dossiers()
    _by_uid = {f["uid"]: f for f, _ in all_sc}
    _dcards = []
    for d in _doss[:3]:
        m = d["meta"]
        slug = m.get("slug", "")
        lu = m.get("lieu")
        vb = (band_chip(_by_uid[lu], _by_uid) if lu and _by_uid.get(lu) else "")
        _dcards.append(
            f'<a class="dossier-vignette" href="dossiers/{e(slug)}.html">'
            f'<h3>{e(clean(m.get("titre","")))}</h3>'
            f'<p>{e(clean(m.get("sous_titre","")))}</p>'
            f'<span class="dv-meta">{vb}Lire le récit →</span></a>')
    doss_section = (
        '<section class="accueil-dossiers"><h2 class="sec">À lire — les récits</h2>'
        '<p class="lead">Certains lieux portent un enseignement que la fiche-tableau '
        'ne transmet pas. On les raconte.</p>'
        '<div class="dossier-vignettes">' + "".join(_dcards) + '</div>'
        '<p class="linkrow"><a href="dossiers/index.html">Tous les dossiers →</a></p>'
        '</section>') if _dcards else ""
    # aperçu de carte vivant — la carte est le réflexe n°1 d'un annuaire
    # géographique : on la MONTRE (points réels colorés par verdict) plutôt que de
    # la promettre. Carte non interactive (pointer-events désactivés en CSS) : un
    # clic n'importe où ouvre la carte complète.
    _cm, _ = carte_markers(all_sc, _by_uid)
    _cm_js = json.dumps(_cm, ensure_ascii=False)
    _cc_js = json.dumps({k or "": v for k, v in CARTE_VERDICT_COULEURS.items()},
                        ensure_ascii=False)
    carte_teaser = f"""<section class="carte-teaser">
  <h2 class="sec">La France des terres libérées</h2>
  <p class="lead">{n_lieux} lieux géolocalisés, colorés selon leur palier de libération — du
  gris marchand au bleu du commun vivant. Un aperçu : cliquez pour plonger dans la carte.</p>
  <a class="carte-home-link" href="carte.html" aria-label="Explorer la carte des {n_lieux} lieux">
    <div id="carte-home" class="carte-home-map" aria-hidden="true"></div>
    <span class="carte-home-cta">Explorer la carte →</span>
  </a>
</section>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
<script>
(function () {{
  var el = document.getElementById("carte-home");
  if (!el || typeof L === "undefined") return;
  var LIEUX = {_cm_js};
  var COULEURS = {_cc_js};
  function colorFor(v) {{ return COULEURS[v || ""] || COULEURS[""]; }}
  var map = L.map("carte-home", {{
    zoomControl: false, dragging: false, scrollWheelZoom: false,
    doubleClickZoom: false, touchZoom: false, keyboard: false, boxZoom: false,
    tap: false
  }}).setView([46.7, 2.4], 5);
  L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }}).addTo(map);
  LIEUX.forEach(function (d) {{
    L.circleMarker([d.lat, d.lon], {{
      radius: 6, weight: 1.5, color: "#fffdf6",
      fillColor: d.bcol || colorFor(d.verdict), fillOpacity: 0.95, interactive: false
    }}).addTo(map);
  }});
}})();
</script>"""

    # 1.10 — section « En vue » : les meilleures entrées par catégorie, en cartes,
    # avec lien direct vers le classement complet.
    best_blocks = []
    for cat, glabel, lot in best_groups:
        if not lot:
            continue
        best_blocks.append(
            f'<h3 class="best-grp">{e(glabel)}</h3>'
            + cards_grid(lot, axes_cfg, concepts=concepts))
    best_section = (
        '<section class="accueil-best"><h2 class="sec">En vue — les montages '
        'les mieux notés</h2>'
        '<p class="lead">Par catégorie, les entrées dont la note de libération '
        'est la plus élevée. <a href="classement.html">Voir le classement complet '
        '→</a></p>'
        + "".join(best_blocks) + '</section>') if best_blocks else ""

    body = f"""{tri_defs(Q6_CFG)}<section class="hero">
  <div class="hero-grid">
    <div class="hero-intro">
      <p class="hero-kicker">Annuaire critique · libération des terres</p>
      <h1>La terre n'est pas une marchandise.</h1>
      <p class="hero-lead">Pourtant elle se vend, se loue, s'épuise. Partout en
      France, des collectifs l'en soustraient — et la rendent à un usage commun,
      vivant et durable. Cet annuaire les recense sans complaisance : il distingue
      les libérations réelles des montages qui en empruntent le vocabulaire, au
      regard d'un cadre explicite et assumé — celui d'une économie citoyenne, non
      lucrative, qui retire la terre du marché. C'est une prise de position, défendable et
      contestable, non une mesure neutre.</p>
      <p class="hero-cta">
        <a class="cta" href="carte.html">Voir la carte</a>
        <a class="cta cta-ghost" href="methode.html">Comprendre la méthode</a>
      </p>
    </div>
    <div class="hero-entry">
      <h2 class="sec">Par où entrer</h2>
      <div class="intent-cards intent-cards-hero">{intentions}</div>
    </div>
  </div>
</section>

<section class="chiffres corpus">
  <h2 class="sec">État du corpus</h2>
  <div class="stat-grid">
    <a class="stat" href="lieux.html"><span class="stat-n">{n_by_cat['lieu']}</span>
      <span class="stat-l">lieux recensés</span></a>
    <a class="stat" href="usufruitiers.html"><span class="stat-n">{n_by_cat['usufruitier']}</span>
      <span class="stat-l">organismes usufruitiers</span></a>
    <a class="stat" href="porteurs.html"><span class="stat-n">{n_by_cat['porteur']}</span>
      <span class="stat-l">porteurs de nue-propriété</span></a>
    <a class="stat" href="reseaux.html"><span class="stat-n">{n_by_cat['reseau']}</span>
      <span class="stat-l">réseaux</span></a>
  </div>
  <p class="lead">La plupart des lieux sont des montages <strong>hybrides</strong>
  ({n_hybride}) : des communs juridiquement solides, mais qu'un maillon, un usage
  rémunéré ou une condition encore non établie tient à distance du sommet — un
  horizon, non une case à remplir. Répartition de toutes les entrées notées par
  palier de libération :</p>
  {hist}
</section>

{carte_teaser}

{doss_section}

{best_section}

<section>
  <h2 class="sec">Modèles voisins de référence</h2>
  <p class="lead">Des modèles proches — français et étrangers — recensés à titre
  de comparaison. Hors classement principal, leur note est <em>estimée</em>.
  <a href="modeles.html">Voir les modèles voisins →</a></p>
</section>"""
    site_desc = meta_desc(concepts["project"]["description"])
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": project["display_name"],
        "alternateName": "Annuaire critique des montages de libération des terres en France",
        "url": canonical_url("index.html"),
        "inLanguage": "fr",
        "description": site_desc,
    }
    return page("Accueil", body, "index.html", project=project,
                description=site_desc, path="index.html", jsonld=[website])


def render_suggerer(cfg):
    project = cfg["concepts"]["project"]
    body = """<h1>Proposer un lieu</h1>
<p class="lead">« Terres Libérées » est un annuaire évolutif au corpus volontairement
restreint et exigeant. Si vous connaissez un lieu, un porteur ou un montage réel de
libération des terres qui n'y figure pas encore, vous pouvez le signaler.</p>

<section><h2 class="sec">Ce que recense l'annuaire</h2>
<p class="prose">Sont référencés les lieux français dont le foncier a été
soustrait au marché spéculatif par dissociation de la propriété et de l'usage :
la propriété est portée par un organisme d'intérêt général ou d'utilité publique
et l'usage confié à une personne morale non lucrative. La page
<a href="methode.html">Méthode</a> détaille les critères ; les
<a href="grilles.html">grilles</a> précisent ce qui est analysé.</p></section>

<section><h2 class="sec">Comment signaler un lieu ou un montage</h2>
<p class="prose">Écrivez à l'adresse ci-dessous en indiquant, autant que possible :</p>
<ul class="prose">
  <li>le nom du lieu, du porteur de nue-propriété et de l'usufruitier ;</li>
  <li>la commune et la région ;</li>
  <li>le type de montage juridique (démembrement, bail emphytéotique, propriété
  publique, propriété collective verrouillée…) ;</li>
  <li>des sources publiques vérifiables (site officiel, presse, rapports) ;</li>
  <li>l'année de création ou d'acquisition, si elle est connue.</li>
</ul>
<p class="prose">Chaque proposition est vérifiée avant publication : seules les
informations sourcées et confirmées sont retenues ; les points non confirmés
sont signalés comme tels dans la fiche.</p>
<p class="prose"><strong>Contact :</strong>
<a href="mailto:cedric.mabilotte@gmail.com">cedric.mabilotte@gmail.com</a></p></section>

<section><h2 class="sec">Limites assumées du corpus</h2>
<p class="prose">L'annuaire reste lacunaire sur certains angles — habitat partagé,
foncier périurbain, outre-mer, espaces naturels concrets. Les signalements
portant sur ces angles morts sont particulièrement bienvenus.</p></section>

<p class="backlink"><a href="index.html">← Retour à l'accueil</a></p>"""
    return page("Proposer un lieu", body, "suggerer.html", project=project,
                description="Comment signaler un lieu ou un montage réel de "
                            "libération des terres à référencer dans l'annuaire.",
                path="suggerer.html")


# ─────────────────────────────────────────────────────────────────────────────
# Page — Journal des versions (changelog)
# ─────────────────────────────────────────────────────────────────────────────

def render_changelog(cfg):
    """Journal public des versions : les évolutions majeures de l'annuaire et de
    sa méthode, en langage public, sans détail interne de fabrication."""
    project = cfg["concepts"]["project"]
    body = f"""<h1>Journal des versions</h1>
<p class="lead">Les évolutions majeures de l'annuaire et de sa méthode. Le site
est révisé en continu ; seules les étapes structurantes sont consignées ici.</p>

<section><h2 class="sec">v{SITE_VERSION} — {SITE_VERSION_DATE}</h2>
<p class="prose">Modèle d'évaluation renforcé. Chaque lieu reçoit désormais un
<strong>verdict</strong> en trois niveaux — marchand, hybride, sanctuaire — à
côté de l'Indice chiffré. La chaîne lieu / porteur / usufruitier est lue de
façon relationnelle : la nature d'un maillon se juge à sa place dans la chaîne,
pas en soi. Le statut épistémique de chaque fiche — ce qui est vérifié, ce qui
reste à confirmer — est affiché explicitement.</p></section>

<section><h2 class="sec">v1.x — {SITE_VERSION_DATE}</h2>
<p class="prose">Première publication de l'annuaire et de la méthode : recensement
des montages réels de libération des terres en France, note de libération (le
faisceau : la porte et six questions), grilles d'analyse et glossaire.</p></section>

<p class="backlink"><a href="index.html">← Retour à l'accueil</a></p>"""
    return page("Journal des versions", body, "", project=project,
                description="Les évolutions majeures de l'annuaire « Terres "
                            "Libérées » et de sa méthode d'évaluation.",
                path="changelog.html")


# ─────────────────────────────────────────────────────────────────────────────
# Page — 404
# ─────────────────────────────────────────────────────────────────────────────

def render_404(cfg):
    project = cfg["concepts"]["project"]
    body = """<h1>Page introuvable</h1>
<p class="lead">La page demandée n'existe pas ou a été déplacée. Le site est un
annuaire au corpus restreint : la page que vous cherchez n'a peut-être jamais
existé.</p>
<p class="prose">Vous pouvez repartir de l'une de ces pages :</p>
<ul class="prose">
  <li><a href="/index.html">Accueil de l'annuaire</a></li>
  <li><a href="/classement.html">Classement par la note de libération</a></li>
  <li><a href="/lieux.html">Catalogue des lieux</a></li>
  <li><a href="/porteurs.html">Catalogue des porteurs de nue-propriété</a></li>
  <li><a href="/usufruitiers.html">Catalogue des organismes usufruitiers</a></li>
  <li><a href="/glossaire.html">Glossaire</a></li>
</ul>"""
    return page("Page introuvable", body, "", project=project,
                description="Page introuvable — Terres Libérées.",
                path="404.html", robots="noindex")


# ─────────────────────────────────────────────────────────────────────────────
# Revues — pensée publique éditoriale (session #7)
# ─────────────────────────────────────────────────────────────────────────────
#
# Chaque revue vit dans `revues/[slug]/` avec un `index.md` (manifeste) et
# un dossier `articles/` contenant des fichiers `YYYY-MM-DD_slug.md`. Le
# générateur en tire :
#   /revues/                        page d'accueil (liste des revues)
#   /revues/[slug]/                 index d'une revue (manifeste + articles)
#   /revues/[slug]/[article-slug]/  un article
#   /revues/[slug]/[slug]-edition-YYYYMMDD.pdf
#
# Markdown supporté : titres `#`/`##`/`###`, paragraphes, gras `**`,
# italique `*`, listes `-`, liens `[txt](url)`, code inline `` ` ``,
# citations `>` — via la bibliothèque `markdown` (extensions: extra,
# sane_lists, smarty).

REVUES_DIR = ROOT / "revues"
DOSSIERS_DIR = ROOT / "dossiers"
PDF_MOIS_FR = ("janvier", "février", "mars", "avril", "mai", "juin", "juillet",
               "août", "septembre", "octobre", "novembre", "décembre")


def _parse_md_frontmatter(text):
    """Lecture d'un fichier Markdown au format :
       ---
       <YAML>
       ---
       <corps Markdown>
    Renvoie (meta_dict, body_str). Si pas de frontmatter, meta={}."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            head = text[3:end].lstrip("\n")
            meta = yaml.safe_load(head) or {}
            body = text[end + 4:].lstrip("\n")
            return meta, body
    return {}, text


def _md_to_html(md_text):
    """Convertit un corps Markdown en HTML via la bibliothèque markdown.
    Extensions : extra (tables, footnotes), sane_lists, smarty (typographie)."""
    try:
        import markdown as _md
    except ImportError:
        # repli minimal — paragraphes seulement.
        return "".join(f"<p>{e(p.strip())}</p>"
                       for p in md_text.split("\n\n") if p.strip())
    return _md.markdown(md_text or "",
                        extensions=["extra", "sane_lists", "smarty"],
                        output_format="html5")


def _date_fr(iso_str):
    """« 2026-05-27 » → « 27 mai 2026 ». Accepte aussi un objet date."""
    if not iso_str:
        return ""
    try:
        if isinstance(iso_str, datetime.date):
            d = iso_str
        else:
            d = datetime.date.fromisoformat(str(iso_str))
        return f"{d.day} {PDF_MOIS_FR[d.month - 1]} {d.year}"
    except (ValueError, TypeError):
        return str(iso_str)


def _statut_chip(statut):
    """Badge HTML pour un statut (vivant, stabilisé/stabilisée, archivé)."""
    statut = (statut or "").strip().lower()
    label_map = {"vivant": "Vivant", "vivante": "Vivant",
                 "stabilise": "Stabilisé", "stabilisé": "Stabilisé",
                 "stabilisee": "Stabilisée", "stabilisée": "Stabilisée",
                 "archive": "Archivé", "archivé": "Archivé",
                 "archivee": "Archivée", "archivée": "Archivée"}
    label = label_map.get(statut, statut.capitalize() or "—")
    cls_norm = {"vivante": "vivant", "stabilisé": "stabilise",
                "stabilisée": "stabilisee", "archivé": "archive",
                "archivée": "archivee"}.get(statut, statut)
    return (f'<span class="statut-chip statut-{e(cls_norm or "inconnu")}">'
            f'{e(label)}</span>')


def load_revues():
    """Charge depuis `revues/` toutes les revues et leurs articles.
    Renvoie une liste de dicts {meta, body_md, articles:[{meta,body_md}]}.
    Trie les articles par date `created` décroissante (plus récent d'abord).
    """
    if not REVUES_DIR.exists():
        return []
    out = []
    for revue_dir in sorted(REVUES_DIR.iterdir()):
        if not revue_dir.is_dir():
            continue
        if revue_dir.name.startswith("."):
            continue
        index_md = revue_dir / "index.md"
        if not index_md.exists():
            continue
        meta, body = _parse_md_frontmatter(
            index_md.read_text(encoding="utf-8"))
        meta.setdefault("slug", revue_dir.name)
        articles = []
        articles_dir = revue_dir / "articles"
        if articles_dir.exists():
            for art_path in sorted(articles_dir.glob("*.md")):
                ameta, abody = _parse_md_frontmatter(
                    art_path.read_text(encoding="utf-8"))
                # slug par défaut : nom de fichier sans la date et l'extension
                nm = art_path.stem
                m = re.match(r"^(\d{4}-\d{2}-\d{2})_(.+)$", nm)
                default_slug = m.group(2) if m else nm
                default_date = m.group(1) if m else None
                ameta.setdefault("slug", default_slug)
                if default_date and not ameta.get("created"):
                    ameta["created"] = default_date
                articles.append({"meta": ameta, "body_md": abody,
                                  "_file": art_path.name})
        # tri : created décroissant, puis slug
        def _key(a):
            c = a["meta"].get("created") or ""
            return (str(c), a["meta"].get("slug", ""))
        articles.sort(key=_key, reverse=True)
        out.append({"meta": meta, "body_md": body, "articles": articles,
                    "_dir": revue_dir.name})
    return out


def _article_url_part(article):
    """Slug court d'un article (pour la route /revues/[slug]/[article-slug]/)."""
    return article["meta"].get("slug") or article["_file"].replace(".md", "")


def _archetype_label(slug, cfg):
    """Libellé lisible d'un slug d'archétype. Cherche dans
    `cfg["concepts"]["archetypes"]` si existant, sinon repli sur le slug."""
    if not slug:
        return ""
    archs = (cfg.get("concepts", {}) or {}).get("archetypes", []) or []
    for a in archs:
        if a.get("id") == slug or a.get("slug") == slug:
            return a.get("label") or a.get("nom") or slug
    return slug.replace("-", " ")


def render_revue(revue, articles, cfg):
    """Page d'index d'une revue : manifeste, archétypes-pivot, liste des
    articles, lien PDF si ≥ 2 articles."""
    project = cfg["concepts"]["project"]
    meta = revue["meta"]
    slug = meta.get("slug", revue["_dir"])
    titre = clean(meta.get("titre", "") or slug)
    sous_titre = clean(meta.get("sous_titre", ""))
    voix = clean(meta.get("voix", "Eozen"))
    co_eds = meta.get("co_editeurs") or []
    perim = clean(meta.get("perimetre", ""))
    posture = clean(meta.get("posture", ""))
    archs = meta.get("archetypes_pivot") or []
    statut = meta.get("statut", "vivant")
    created = _date_fr(meta.get("created"))
    updated = _date_fr(meta.get("updated"))
    version = meta.get("version", 1)

    archs_html = ""
    if archs:
        archs_html = ("<p class=\"revue-meta\"><strong>Archétypes pivots :</strong> "
                      + ", ".join(e(_archetype_label(a, cfg)) for a in archs)
                      + "</p>")
    co_html = ""
    if co_eds:
        co_html = ("<p class=\"revue-meta\"><strong>Co-éditeur·rice·s :</strong> "
                   + ", ".join(e(clean(str(c))) for c in co_eds) + "</p>")

    # bouton PDF — dès le premier article publié (session #8)
    pdf_html = ""
    if len(articles) >= 1 and HAS_WEASYPRINT:
        today_compact = datetime.date.today().strftime("%Y%m%d")
        pdf_name = f"{slug}-edition-{today_compact}.pdf"
        if len(articles) >= 2:
            pdf_desc = (
                "Une édition PDF reprend l'ensemble des articles de cette "
                "revue, mis en pages comme un livre de lecture (couverture, "
                "table des matières, articles à la suite, demi-format A5).")
            pdf_label = "Télécharger l'édition"
        else:
            pdf_desc = (
                "Le premier article de cette revue est disponible en PDF, "
                "mis en pages comme un livre de lecture (couverture, "
                "demi-format A5).")
            pdf_label = "Télécharger le PDF"
        pdf_html = f"""<aside class="revue-pdf">
  <h4>Édition imprimable</h4>
  <p>{pdf_desc}</p>
  <p><a class="cta-pdf" href="{e(pdf_name)}" download>{pdf_label} du
  {e(_date_fr(datetime.date.today().isoformat()))} (PDF)</a></p>
</aside>"""

    # liste des articles
    if articles:
        items = []
        for a in articles:
            am = a["meta"]
            art_slug = _article_url_part(a)
            art_titre = clean(am.get("titre", "") or art_slug)
            art_sous = clean(am.get("sous_titre", ""))
            art_resume = clean(am.get("resume", ""))
            art_statut = am.get("statut", "vivant")
            art_date = _date_fr(am.get("created"))
            art_updated = am.get("updated")
            art_version = am.get("version", 1)
            auteur = clean(am.get("auteur", voix))
            meta_parts = []
            if art_date:
                meta_parts.append(f'<time datetime="{e(am.get("created",""))}">'
                                  f'{e(art_date)}</time>')
            if auteur:
                meta_parts.append(f"par {e(auteur)}")
            meta_parts.append(_statut_chip(art_statut))
            if art_version and int(art_version) > 1:
                meta_parts.append(f"version {e(art_version)}")
            if art_updated and str(art_updated) != str(am.get("created", "")):
                meta_parts.append(f"mis à jour le {e(_date_fr(art_updated))}")
            meta_line = '<span class="sep">·</span>'.join(meta_parts)
            sous_html = (f'<p class="article-resume"><em>{e(art_sous)}</em></p>'
                         if art_sous else "")
            resume_html = (f'<p class="article-resume">{e(art_resume)}</p>'
                           if art_resume else "")
            items.append(f"""<li class="article-item">
  <h3><a href="{e(art_slug)}/">{e(art_titre)}</a></h3>
  <p class="article-meta">{meta_line}</p>
  {sous_html}{resume_html}
</li>""")
        articles_html = (f'<ol class="articles-liste">{"".join(items)}</ol>')
    else:
        articles_html = ('<p class="prose"><em>Aucun article publié pour '
                         "l'instant. La revue est ouverte ; les premiers "
                         "articles paraîtront prochainement.</em></p>")

    # manifeste — corps Markdown de l'index.md
    manifeste_html = _md_to_html(revue.get("body_md", ""))

    body = f"""<section class="revue-hero">
  <p class="hero-kicker"><a href="../index.html">Revues</a></p>
  <h1>{e(titre)}</h1>
  {f'<p class="revue-soustitre">{e(sous_titre)}</p>' if sous_titre else ""}
  <p class="revue-meta">{_statut_chip(statut)}
  <span class="sep">·</span> Voix : <strong>{e(voix)}</strong>
  {f'<span class="sep">·</span> Créée le {e(created)}' if created else ""}
  {f'<span class="sep">·</span> Mise à jour le {e(updated)}' if updated and updated != created else ""}
  </p>
  {co_html}
  {f'<p class="revue-meta"><strong>Périmètre :</strong> {e(perim)}</p>' if perim else ""}
  {f'<p class="revue-meta"><strong>Posture :</strong> {e(posture)}</p>' if posture else ""}
  {archs_html}
</section>

<section class="revue-prose">
  <h2>Manifeste</h2>
  {manifeste_html}
</section>

{pdf_html}

<section>
  <h2 class="sec">Articles</h2>
  {articles_html}
</section>"""

    desc = meta_desc(sous_titre or perim or titre)
    return page(titre, body, "revues/index.html", depth=2, project=project,
                description=desc,
                path=f"revues/{slug}/index.html",
                extra_css=["style-revue.css"])


def render_article(revue, article, cfg):
    """Page d'un article : titre, sous-titre, auteur·s, dates, version,
    statut, archétypes traversés, cas illustratifs (liens vers les fiches),
    corps Markdown converti, changelog en pied."""
    project = cfg["concepts"]["project"]
    rmeta = revue["meta"]
    rslug = rmeta.get("slug", revue["_dir"])
    rtitre = clean(rmeta.get("titre", "") or rslug)
    am = article["meta"]
    art_slug = _article_url_part(article)
    titre = clean(am.get("titre", "") or art_slug)
    sous_titre = clean(am.get("sous_titre", ""))
    auteur = clean(am.get("auteur", rmeta.get("voix", "Eozen")))
    co_auteurs = am.get("co_auteurs") or []
    created = _date_fr(am.get("created"))
    updated = _date_fr(am.get("updated"))
    version = am.get("version", 1)
    statut = am.get("statut", "vivant")
    changelog = am.get("changelog") or []
    archs = am.get("archetypes") or []
    cas = am.get("cas_illustratifs") or []

    # archétypes traversés — lien retour vers la revue (manifeste les liste)
    archs_html = ""
    if archs:
        items = ", ".join(e(_archetype_label(a, cfg)) for a in archs)
        archs_html = f"""<div class="article-relations">
  <h4>Archétypes traversés</h4>
  <p>{items} <span class="sep">·</span>
  <a href="../index.html#archetypes">voir le manifeste</a></p>
</div>"""

    # cas illustratifs — uid de fiches Communs, liens absolus vers /l/<uid>.html etc.
    cas_html = ""
    if cas:
        # on essaie le préfixe CAT_SLUG ; on tente l→p→u→m→r pour résoudre
        liens = []
        for uid in cas:
            uid = str(uid).strip()
            if not uid:
                continue
            # cherche le fichier qui existe
            href = None
            for slugd in ("l", "p", "u", "m", "r"):
                cible = SITE / slugd / f"{uid}.html"
                if cible.exists():
                    href = f"../../../{slugd}/{uid}.html"  # article = prof. 3
                    break
            if href is None:
                # fallback raisonnable : lieux
                href = f"../../../l/{uid}.html"
            liens.append(f'<li><a href="{e(href)}">{e(uid)}</a></li>')
        if liens:
            cas_html = f"""<div class="article-relations">
  <h4>Cas illustratifs</h4>
  <ul>{"".join(liens)}</ul>
</div>"""

    # changelog
    cl_html = ""
    if changelog:
        items = []
        for entry in changelog:
            if not isinstance(entry, dict):
                continue
            d = _date_fr(entry.get("date"))
            v = entry.get("version")
            note = clean(entry.get("note", ""))
            items.append(
                f'<li><span class="ch-date">{e(d)}</span>'
                f'{f"<span class=\"ch-version\">v{e(v)}</span>" if v else ""}'
                f'<span>{e(note)}</span></li>')
        if items:
            cl_html = f"""<section class="article-changelog">
  <h2>Journal des modifications</h2>
  <ol>{"".join(items)}</ol>
</section>"""

    # corps Markdown
    body_html = _md_to_html(article.get("body_md", ""))

    # méta-ligne d'en-tête
    meta_parts = []
    if created:
        meta_parts.append(f'Écrit le <strong>{e(created)}</strong>')
    auteurs_full = auteur
    if co_auteurs:
        auteurs_full = auteur + ", " + ", ".join(
            e(clean(str(c))) for c in co_auteurs)
    meta_parts.append(f'par <strong>{auteurs_full}</strong>')
    meta_parts.append(_statut_chip(statut))
    if version and int(version) > 1:
        meta_parts.append(f'version <strong>{e(version)}</strong>')
    if updated and str(am.get("updated")) != str(am.get("created", "")):
        meta_parts.append(f'mis à jour le <strong>{e(updated)}</strong>')
    meta_line = '<span class="sep">·</span>'.join(meta_parts)

    body = f"""<header class="article-head">
  <p class="article-kicker"><a href="../index.html">{e(rtitre)}</a></p>
  <h1>{e(titre)}</h1>
  {f'<p class="article-soustitre">{e(sous_titre)}</p>' if sous_titre else ""}
  <p class="article-meta">{meta_line}</p>
</header>

<article class="article-prose">
  {body_html}
</article>

{archs_html}
{cas_html}
{cl_html}"""

    desc = meta_desc(sous_titre or clean(am.get("resume", "")) or titre)
    return page(titre, body, "revues/index.html", depth=3, project=project,
                description=desc,
                path=f"revues/{rslug}/{art_slug}/index.html",
                extra_css=["style-revue.css"],
                og_type="article")


def render_revues_index(revues, cfg):
    """Page principale `/revues/` — présente l'ensemble des revues."""
    project = cfg["concepts"]["project"]
    cards = []
    for r in revues:
        m = r["meta"]
        slug = m.get("slug", r["_dir"])
        titre = clean(m.get("titre", "") or slug)
        sous = clean(m.get("sous_titre", ""))
        voix = clean(m.get("voix", "Eozen"))
        statut = m.get("statut", "vivant")
        n_art = len(r["articles"])
        n_label = (f"{n_art} article" + ("s" if n_art > 1 else "")) if n_art \
            else "aucun article publié"
        cards.append(f"""<a class="revue-card" href="{e(slug)}/">
  <h3>{e(titre)}</h3>
  {f'<p class="revue-card-sous">{e(sous)}</p>' if sous else ""}
  <p class="revue-card-meta">{_statut_chip(statut)}
    <span class="sep">·</span> Voix : <strong>{e(voix)}</strong>
    <span class="sep">·</span> {e(n_label)}</p>
</a>""")
    grid = ('<div class="revues-grid">' + "".join(cards) + "</div>"
            if cards else
            '<p class="prose"><em>Aucune revue publiée pour l\'instant.</em></p>')
    body = f"""<section class="revue-hero">
  <p class="hero-kicker">Pensée publique éditoriale</p>
  <h1>Revues</h1>
  <p class="revue-soustitre">Quatre revues vivantes, éditées en continu, qui
  prolongent l'annuaire en écriture. Chaque revue tient un fil — un mécanisme,
  une posture, un type de cas — et l'instruit article par article. Les textes
  sont versionnés : l'écrit n'est jamais figé, il s'épaissit.</p>
  <p class="revue-meta">Direction éditoriale : <strong>Eozen</strong>.</p>
</section>

{grid}

<section class="revue-meta-regles">
  <h2 class="sec">Comment ces revues s'écrivent</h2>
  <p class="prose"><strong>Édition vivante.</strong> Les revues s'écrivent au fil
  de l'eau : un article peut être révisé, complété, restructuré, et porte sa date
  de mise à jour. L'écrit n'est jamais figé, il s'épaissit.</p>
  <p class="prose"><strong>Des archétypes, pas des noms.</strong> Les revues
  parlent de mécanismes et d'archétypes plutôt que de cibles nommées : un mécanisme
  nommé se reconnaît partout, une cible nommée enferme le débat dans un cas
  particulier. Un cas concret n'est nommé que lorsqu'il éclaire l'archétype — ou,
  pour les récits, lorsque raconter un lieu exige de le nommer.</p>
</section>

<p class="prose">Les revues sont éditoriales, l'annuaire est documentaire :
ce qui se discute dans les revues s'appuie sur ce que recense l'annuaire,
et inversement. <a href="../methode.html">Lire la méthode →</a></p>"""
    return page("Revues", body, "revues/index.html", depth=1, project=project,
                description="Les quatre revues vivantes de Terres Libérées — "
                            "pensée publique sur la libération des terres.",
                path="revues/index.html",
                extra_css=["style-revue.css"])


# ─────────────────────────────────────────────────────────────────────────────
# Dossiers — le magazine : fiches-récit longues sur des cas-pivot du corpus.
# Chaque dossier porte un lieu (`lieu:` uid) qu'il raconte ; lien bidirectionnel
# avec la fiche-catalogue. Voix incarnée dominante. Format Markdown + frontmatter.
# ─────────────────────────────────────────────────────────────────────────────
def load_dossiers():
    """Charge `dossiers/*.md` → liste de {meta, body_md, _file}, triés par date
    décroissante puis titre."""
    if not DOSSIERS_DIR.exists():
        return []
    out = []
    for p in sorted(DOSSIERS_DIR.glob("*.md")):
        if p.name.startswith("."):
            continue
        meta, body = _parse_md_frontmatter(p.read_text(encoding="utf-8"))
        meta.setdefault("slug", p.stem)
        out.append({"meta": meta, "body_md": body, "_file": p.name})
    out.sort(key=lambda d: (str(d["meta"].get("date") or ""),
                            d["meta"].get("titre", "")), reverse=True)
    return out


def dossier_map(dossiers):
    """uid de lieu → slug de dossier (pour le lien retour depuis la fiche)."""
    m = {}
    for d in dossiers:
        lu = d["meta"].get("lieu")
        if lu:
            m[lu] = d["meta"].get("slug", d["_file"].replace(".md", ""))
    return m


def render_dossiers_index(dossiers, cfg, sc_by_uid, by_uid):
    project = cfg["concepts"]["project"]
    cards = []
    for d in dossiers:
        m = d["meta"]
        slug = m.get("slug")
        titre = clean(m.get("titre", "") or slug)
        sous = clean(m.get("sous_titre", ""))
        lu = m.get("lieu")
        vbadge = ""
        if lu and by_uid.get(lu):
            vbadge = band_chip(by_uid[lu], by_uid)
        cards.append(f"""<a class="revue-card" href="{e(slug)}.html">
  <h3>{e(titre)}</h3>
  {f'<p class="revue-card-sous">{e(sous)}</p>' if sous else ""}
  <p class="revue-card-meta">{vbadge}</p>
</a>""")
    grid = ('<div class="revues-grid">' + "".join(cards) + "</div>" if cards else
            '<p class="prose"><em>Aucun dossier publié pour l\'instant.</em></p>')
    body = f"""<section class="revue-hero">
  <p class="hero-kicker">Le magazine · récits de cas</p>
  <h1>Dossiers</h1>
  <p class="revue-soustitre">Certains lieux portent un enseignement que la
  fiche-tableau ne transmet pas. Les dossiers les racontent — en récit, au plus
  près de ce qui s'y vit — sans rien retrancher à l'analyse du catalogue, qu'ils
  prolongent et vers lequel ils renvoient.</p>
  <p class="revue-meta">Direction éditoriale : <strong>Eozen</strong>.</p>
</section>

{grid}

<p class="prose">Les dossiers sont éditoriaux, l'annuaire est documentaire : le
récit éclaire un cas, la fiche le situe à barème égal avec tous les autres.
<a href="../lieux.html">Le catalogue des lieux →</a></p>"""
    return page("Dossiers", body, "dossiers/index.html", depth=1, project=project,
                description="Le magazine de Terres Libérées — récits de cas-pivot "
                            "de la libération des terres.",
                path="dossiers/index.html", extra_css=["style-revue.css"])


def render_dossier(dossier, cfg, by_uid, sc_by_uid):
    project = cfg["concepts"]["project"]
    m = dossier["meta"]
    titre = clean(m.get("titre", "") or m.get("slug", ""))
    sous = clean(m.get("sous_titre", ""))
    chapeau = clean(m.get("chapeau", ""))
    date_fr = _date_fr(m.get("date"))
    lu = m.get("lieu")
    # lien vers la fiche-catalogue + badge verdict
    fiche_lien = ""
    if lu and by_uid.get(lu):
        v = band_chip(by_uid[lu], by_uid)
        sc = sc_by_uid.get(lu)
        idl = f" · note {sc['idl']}" if sc and sc.get("idl") is not None else ""
        fiche_lien = (f'<aside class="dossier-fiche">{v}'
                      f'<span class="df-txt">Ce lieu est aussi analysé, à barème '
                      f'égal avec les autres, dans le catalogue{idl}. '
                      f'<a href="../l/{e(lu)}.html">Voir la fiche → </a></span></aside>')
    corps = _md_to_html(dossier["body_md"])
    meta_line = " · ".join(x for x in [date_fr, "Voix : Eozen"] if x)
    body = f"""<article class="dossier">
<p class="crumb"><a href="index.html">← Tous les dossiers</a></p>
<header class="dossier-head">
  <h1>{e(titre)}</h1>
  {f'<p class="dossier-sous">{e(sous)}</p>' if sous else ""}
  <p class="dossier-meta">{e(meta_line)}</p>
</header>
{f'<p class="dossier-chapeau">{e(chapeau)}</p>' if chapeau else ""}
{fiche_lien}
<div class="dossier-corps prose-long">
{corps}
</div>
{fiche_lien}
<p class="backlink"><a href="index.html">← Tous les dossiers</a>
 · <a href="../lieux.html">Le catalogue des lieux</a></p>
</article>"""
    return page(titre, body, "dossiers/index.html", depth=1, project=project,
                description=meta_desc(sous or chapeau or titre, 250),
                path=f"dossiers/{m.get('slug')}.html", extra_css=["style-revue.css"])


def build_revue_pdf(revue, articles, cfg):
    """Génère un PDF format livre (demi-A5) via WeasyPrint.

    Mise en page : couverture pleine page (titre, sous-titre, voix, date
    d'édition, nombre d'articles), table des matières, articles à la suite
    avec saut de page entre chacun. Style sobre, typographie de lecture.
    """
    try:
        from weasyprint import HTML, CSS as _WCSS
    except ImportError:
        print(f"  PDF non généré pour {revue['_dir']} : weasyprint absent.")
        return None
    meta = revue["meta"]
    slug = meta.get("slug", revue["_dir"])
    titre = clean(meta.get("titre", "") or slug)
    sous_titre = clean(meta.get("sous_titre", ""))
    voix = clean(meta.get("voix", "Eozen"))
    today = datetime.date.today()
    today_compact = today.strftime("%Y%m%d")
    today_fr = _date_fr(today.isoformat())
    n_art = len(articles)
    n_label = f"{n_art} article" + ("s" if n_art > 1 else "")
    manifeste_html = _md_to_html(revue.get("body_md", ""))

    # table des matières + articles
    toc_items, art_blocks = [], []
    for i, a in enumerate(articles, 1):
        am = a["meta"]
        atitre = clean(am.get("titre", "") or _article_url_part(a))
        asous = clean(am.get("sous_titre", ""))
        adate = _date_fr(am.get("created"))
        auteur = clean(am.get("auteur", voix))
        anchor = f"art-{i}"
        toc_items.append(
            f'<li><a href="#{anchor}"><span class="toc-num">{i}.</span> '
            f'<span class="toc-title">{e(atitre)}</span>'
            f'<span class="toc-date">{e(adate)}</span></a></li>')
        body_html = _md_to_html(a.get("body_md", ""))
        sous_html = (f'<p class="pdf-soustitre">{e(asous)}</p>' if asous else "")
        meta_html = (f'<p class="pdf-meta">{e(adate)}'
                     f'{f" · par {e(auteur)}" if auteur else ""}</p>')
        art_blocks.append(f"""<section class="pdf-article" id="{anchor}">
  <h1 class="pdf-art-titre">{e(atitre)}</h1>
  {sous_html}{meta_html}
  <div class="pdf-art-corps">{body_html}</div>
</section>""")

    pdf_html_doc = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>{e(titre)}</title></head>
<body>
<section class="pdf-cover">
  <p class="pdf-cover-kicker">Revue · Terres Libérées</p>
  <h1 class="pdf-cover-titre">{e(titre)}</h1>
  {f'<p class="pdf-cover-sous">{e(sous_titre)}</p>' if sous_titre else ""}
  <p class="pdf-cover-voix">par {e(voix)}</p>
  <p class="pdf-cover-date">édition du {e(today_fr)}</p>
  <p class="pdf-cover-n">{e(n_label)}</p>
</section>
<section class="pdf-toc">
  <h2>Table des matières</h2>
  <ol>{"".join(toc_items)}</ol>
</section>
<section class="pdf-manifeste">
  <h2>Manifeste</h2>
  {manifeste_html}
</section>
{"".join(art_blocks)}
</body></html>"""

    pdf_css = """
    @page {
      size: 148mm 210mm; /* demi-A5 / A5 portrait */
      margin: 18mm 16mm 18mm 16mm;
      @bottom-center {
        content: counter(page);
        font-family: Georgia, serif; font-size: 9pt; color: #666;
      }
      @top-center {
        content: string(art-title);
        font-family: Georgia, serif; font-size: 8.5pt; color: #888;
        font-style: italic;
      }
    }
    @page :first { @top-center { content: none; } @bottom-center { content: none; } }
    @page cover { margin: 0; @top-center { content: none; } @bottom-center { content: none; } }
    html, body {
      font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
      color: #221f1a; font-size: 10.5pt; line-height: 1.55;
    }
    .pdf-cover {
      page: cover; height: 210mm; width: 148mm;
      padding: 28mm 18mm; box-sizing: border-box;
      display: flex; flex-direction: column; justify-content: center;
      background: #f5f2e9; page-break-after: always;
    }
    .pdf-cover-kicker {
      font-size: 9pt; text-transform: uppercase; letter-spacing: .15em;
      color: #8f3f25; font-family: "Helvetica Neue", Helvetica, sans-serif;
      margin: 0 0 16mm 0;
    }
    .pdf-cover-titre {
      font-size: 26pt; line-height: 1.18; margin: 0 0 6mm 0;
      font-weight: 700; max-width: 100mm; color: #221f1a;
    }
    .pdf-cover-sous {
      font-size: 13pt; font-style: italic; color: #5f5849;
      margin: 0 0 14mm 0; max-width: 100mm;
    }
    .pdf-cover-voix { font-size: 11pt; margin: 8mm 0 1mm 0; color: #221f1a; }
    .pdf-cover-date { font-size: 10pt; color: #5f5849; margin: 0 0 3mm 0; }
    .pdf-cover-n {
      font-size: 9pt; color: #888; margin: 0;
      font-family: "Helvetica Neue", Helvetica, sans-serif;
    }
    .pdf-toc { page-break-after: always; }
    .pdf-toc h2, .pdf-manifeste h2 {
      font-size: 16pt; margin: 0 0 6mm 0; font-weight: 600;
      border-bottom: 1px solid #ddd4bf; padding-bottom: 2mm;
    }
    .pdf-toc ol { list-style: none; padding: 0; margin: 0; }
    .pdf-toc li { margin: 1.4mm 0; }
    .pdf-toc a {
      color: #221f1a; text-decoration: none; display: flex; gap: 3mm;
    }
    .pdf-toc .toc-num { color: #8f3f25; font-weight: 600; min-width: 6mm; }
    .pdf-toc .toc-title { flex: 1; }
    .pdf-toc .toc-date {
      color: #888; font-size: 9pt; font-style: italic;
    }
    .pdf-manifeste { page-break-after: always; }
    .pdf-article { page-break-before: always; string-set: art-title content(); }
    .pdf-art-titre {
      font-size: 18pt; line-height: 1.22; margin: 0 0 3mm 0; font-weight: 700;
      string-set: art-title content();
    }
    .pdf-soustitre {
      font-size: 12pt; font-style: italic; color: #5f5849; margin: 0 0 4mm 0;
    }
    .pdf-meta {
      font-size: 9pt; color: #888; margin: 0 0 8mm 0;
      font-family: "Helvetica Neue", Helvetica, sans-serif;
    }
    .pdf-art-corps p { margin: 2mm 0; text-align: justify; hyphens: auto; }
    .pdf-art-corps h2 {
      font-size: 13pt; font-weight: 600; margin: 6mm 0 2mm 0;
    }
    .pdf-art-corps h3 {
      font-size: 11.5pt; font-weight: 600; margin: 5mm 0 1.5mm 0;
    }
    .pdf-art-corps blockquote {
      border-left: 2px solid #bc5d3a; padding-left: 4mm; margin: 3mm 0;
      color: #5f5849; font-style: italic;
    }
    .pdf-art-corps ul, .pdf-art-corps ol {
      margin: 2mm 0 2mm 5mm; padding-left: 4mm;
    }
    .pdf-art-corps code {
      font-family: "Menlo", "Consolas", monospace; font-size: 9.5pt;
      background: #efe9d8; padding: 0 1mm; border-radius: 1mm;
    }
    """
    out_dir = SITE / "revues" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}-edition-{today_compact}.pdf"
    try:
        HTML(string=pdf_html_doc).write_pdf(
            target=str(out_path), stylesheets=[_WCSS(string=pdf_css)])
        return out_path
    except Exception as exc:  # pragma: no cover — diagnostic
        print(f"  PDF non généré pour {slug} : {exc}")
        return None


def verifier_revues(revues):
    """Garde-fou des revues : cohérence des dates, archétypes, cas illustratifs.

    Avertit sans bloquer (les revues vivantes peuvent avoir des cas en
    cours de documentation). Sort la liste des messages."""
    avert = []
    for r in revues:
        m = r["meta"]
        slug = m.get("slug", r["_dir"])
        # date created ≤ updated si les deux sont fournies
        c, u = m.get("created"), m.get("updated")
        if c and u and str(c) > str(u):
            avert.append(f"  revue {slug} — updated < created "
                         f"({u} < {c})")
        for a in r["articles"]:
            am = a["meta"]
            aslug = am.get("slug") or a["_file"]
            ac, au = am.get("created"), am.get("updated")
            if ac and au and str(ac) > str(au):
                avert.append(f"  revue {slug}/{aslug} — updated < created "
                             f"({au} < {ac})")
    if avert:
        print(f"Contrôle des revues : {len(avert)} signalement·s —")
        for a in avert:
            print(a)
    else:
        print("Contrôle des revues : cohérence des dates OK.")
    return avert


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
:root{
 --ink:#221f1a;--muted:#5f5849;--faint:#6e6655;--paper:#f5f2e9;--card:#fffdf6;
 --line:#ddd4bf;--green:#4a7a3a;--green-dk:#356026;--terra:#bc5d3a;
 --terra-dk:#8f3f25;--blue:#36748a;--blue-dk:#2a5566;--gold:#b0843a;
 --gold-dk:#8a6420;--beige:#efe9d8;--beige-dk:#e6ddc6;
 --axe-1:#bc5d3a;--axe-2:#4a6b8a;--axe-3:#36748a;--axe-4:#4a7a3a;--axe-5:#b0822f;
 --radius:8px;--radius-sm:4px;--radius-pill:999px;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
 color:var(--ink);background:var(--paper);line-height:1.58;-webkit-font-smoothing:antialiased;}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.3rem;}
a{color:var(--green-dk);}
a:hover{color:var(--green);}
:focus-visible{outline:2px solid var(--ink);outline-offset:2px;border-radius:var(--radius-sm);}

/* utilitaire : visuellement masqué mais lisible par lecteur d'écran */
.visually-hidden{position:absolute;width:1px;height:1px;padding:0;margin:-1px;
 overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0;}
.skiplink{position:absolute;left:-999px;top:0;background:var(--ink);
 color:var(--paper);padding:.6rem 1rem;z-index:100;border-radius:0 0 var(--radius) 0;
 font-family:-apple-system,system-ui,sans-serif;font-size:.9rem;}
.skiplink:focus{left:0;color:var(--paper);}

/* échelle typographique */
h1{font-size:2.6rem;line-height:1.15;letter-spacing:-.018em;margin:1.4rem 0 .6rem;}
h2.sec{font-size:1.7rem;font-family:inherit;text-transform:none;
 letter-spacing:-.01em;color:var(--ink);font-weight:600;
 border-bottom:1px solid var(--line);padding-bottom:.4rem;margin:2.4rem 0 1.2rem;}
h2.sec::before{content:"";display:inline-block;width:1.5rem;height:3px;
 background:var(--terra);vertical-align:.35em;margin-right:.55rem;border-radius:2px;}
h3{font-size:1.28rem;font-weight:600;letter-spacing:-.005em;margin:1.2rem 0 .4rem;}
p{font-size:1.05rem;}
.sans,.topnav,.toolbar,.tag,.axis-block,.card-meta,.enbref,.idl-badge,.fiab,
.completude,.note,.crumb,.foot-links,.score-cap,.pal-chip,.fbtn,.count,
.cat-n,.row-sub,table,.chip,.axe-legend,.crit-axe,.hero-kicker,.step-n,
.sort-lab,.filter-lab,select,.no-result,.gloss-item dt{
 font-family:-apple-system,system-ui,"Segoe UI",sans-serif;}

/* masthead */
.masthead{border-bottom:2px solid var(--ink);background:var(--paper);}
.masthead .wrap{display:flex;flex-wrap:wrap;align-items:center;
 justify-content:space-between;gap:.6rem 1.4rem;padding-top:1.1rem;padding-bottom:.6rem;}
.brand{display:flex;align-items:center;gap:.7rem;text-decoration:none;color:var(--ink);}
.logo-mark{font-family:-apple-system,system-ui,sans-serif;font-size:1.2rem;font-weight:800;
 letter-spacing:0;background:var(--green-dk);color:var(--paper);
 padding:.32rem .5rem;border-radius:var(--radius);line-height:1;}
.brand-name{font-size:1.4rem;font-weight:700;letter-spacing:-.01em;display:block;}
.baseline{font-size:.76rem;color:var(--muted);font-family:-apple-system,system-ui,sans-serif;}
@media (max-width:480px){.baseline{display:none;}}
.topnav{display:flex;gap:1.05rem;flex-wrap:wrap;font-size:.88rem;}
.topnav a{text-decoration:none;color:var(--muted);padding:.45rem .2rem;
 display:inline-block;min-height:24px;
 border-bottom:2px solid transparent;transition:color .15s,border-color .15s;}
.topnav a:hover{color:var(--green-dk);border-bottom-color:var(--line);}
.topnav a.active{color:var(--ink);font-weight:600;border-bottom-color:var(--terra);}
/* la Méthode est la référence : un peu détachée des destinations */
.topnav a.nav-ref{margin-left:auto;color:var(--faint);}
@media (max-width:640px){.topnav a.nav-ref{margin-left:0;}}

/* hub Annuaire — bloc « Commencer ici » (entrées dominantes) */
.start-grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin:.6rem 0 .4rem;}
.start-card{display:block;background:var(--beige);border:1px solid transparent;
 border-radius:var(--radius);padding:1.3rem 1.4rem;text-decoration:none;color:var(--ink);
 transition:border-color .15s,box-shadow .15s;}
.start-card:hover{border-color:var(--green);box-shadow:0 6px 20px rgba(33,29,24,.10);}
.start-card h3{margin:0 0 .35rem;font-size:1.25rem;}
.start-card p{font-size:.92rem;color:var(--muted);margin:.2rem 0 .6rem;}
.acteurs-fold>summary.sec{cursor:pointer;width:fit-content;}
.acteurs-fold>summary.sec .fold-hint{font-weight:400;font-size:.8rem;color:var(--muted);text-transform:none;letter-spacing:0;}

main.wrap{padding-bottom:4rem;}

/* hero */
.hero{padding:3.4rem 0 2.6rem;border-bottom:1px solid var(--line);}
.hero-kicker{font-size:.8rem;text-transform:uppercase;letter-spacing:.12em;
 color:var(--terra-dk);font-weight:700;margin:0 0 .4rem;}
.hero h1{font-size:2.9rem;max-width:18ch;margin:.1rem 0 .7rem;}
.hero-lead{font-size:1.22rem;line-height:1.5;color:var(--ink);max-width:46ch;}
.hero-cta{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.4rem;}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.62fr) minmax(0,1.7fr);gap:2.4rem;align-items:start;}
.hero-entry .sec{margin:.2rem 0 .6rem;}
/* la colonne de droite tient elle-même 2 colonnes d'encarts (→ 3 colonnes au total).
   Double classe pour l'emporter sur la règle .intent-cards auto-fit déclarée plus bas. */
.intent-cards.intent-cards-hero{grid-template-columns:1fr 1fr;gap:.7rem;margin:0;}
.intent-cards-hero .intent-card{padding:.8rem .9rem;}
.intent-cards-hero .intent-card h3{font-size:1rem;}
.intent-cards-hero .intent-card p{font-size:.82rem;}
@media (max-width:880px){.hero-grid{grid-template-columns:1fr;gap:1.6rem;}}
@media (max-width:520px){.intent-cards.intent-cards-hero{grid-template-columns:1fr;}}
.cta{display:inline-block;background:var(--green-dk);color:var(--paper)!important;
 text-decoration:none;padding:.6rem 1.2rem;border-radius:var(--radius);font-weight:600;
 font-family:-apple-system,system-ui,sans-serif;font-size:.92rem;
 transition:background .15s,box-shadow .15s;}
.cta:hover{background:var(--green);}
.cta:focus-visible{outline-color:var(--ink);}
.cta-ghost{background:transparent;color:var(--green-dk)!important;border:1.5px solid var(--green);}
.cta-ghost:hover{background:var(--card);}
.lead{font-size:1.05rem;color:var(--muted);max-width:70ch;}
.lead a,.prose a,.grille-intro a,.linkrow a{text-decoration:underline;
 text-underline-offset:2px;text-decoration-thickness:1px;}

/* fil de liens secondaires — dégradé par rapport au chapô .lead */
.linkrow{font-family:-apple-system,system-ui,sans-serif;font-size:.9rem;
 color:var(--faint);margin:.9rem 0 .2rem;}

/* sommaire ancré de page de référence */
.page-toc{display:flex;flex-wrap:wrap;gap:.4rem 1.1rem;margin:1rem 0 .4rem;
 font-family:-apple-system,system-ui,sans-serif;font-size:.88rem;}
.page-toc a{color:var(--green-dk);text-decoration:none;}
.page-toc a:hover{text-decoration:underline;}

/* comment lire — étapes */
.steps{list-style:none;padding:0;margin:1.2rem 0;display:grid;gap:1rem;
 grid-template-columns:repeat(auto-fit,minmax(240px,1fr));}
.step{background:var(--card);border:1px solid transparent;
 border-radius:var(--radius);padding:1.1rem 1.2rem 1.2rem;position:relative;}
.step-n{display:inline-flex;align-items:center;justify-content:center;
 width:1.9rem;height:1.9rem;border-radius:50%;background:var(--terra-dk);
 color:var(--paper);font-weight:700;font-size:.95rem;}
.step h3{margin:.6rem 0 .3rem;}
.step p{font-size:.95rem;color:var(--muted);}

/* explain */
/* chiffres-clés (accueil) */
.chiffres{margin:1.4rem 0;}
.stat-grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));margin:.6rem 0 1rem;}
.stat{background:var(--beige);border-radius:var(--radius);padding:1rem 1.1rem;text-align:center;}
.stat-n{display:block;font-size:2.4rem;line-height:1;font-weight:700;color:var(--green-dk);}
.stat-l{display:block;margin-top:.4rem;font-size:.86rem;color:var(--muted);
 font-family:-apple-system,system-ui,sans-serif;}
a.stat{color:inherit;text-decoration:none;transition:box-shadow .15s,transform .15s;}
a.stat:hover,a.stat:focus-visible{box-shadow:0 2px 10px rgba(0,0,0,.10);transform:translateY(-1px);}
/* entrées par intention (accueil) */
.intent-cards{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin:.6rem 0;}
.intent-card{background:var(--card);border:1px solid transparent;border-radius:var(--radius);
 padding:1.1rem 1.2rem;transition:border-color .15s,box-shadow .15s;}
.intent-card:hover{border-color:var(--green);box-shadow:0 4px 16px rgba(33,29,24,.08);}
.intent-card h3{margin-top:0;}
.intent-card p{font-size:.92rem;color:var(--muted);}
.intent-links{font-family:-apple-system,system-ui,sans-serif;font-size:.85rem;}
/* bandeau « À lire » — vignettes de récits sur l'accueil */
.accueil-dossiers{margin:1.6rem 0;}
/* 1.10 — section « En vue » : meilleures entrées par catégorie */
.accueil-best{margin:1.6rem 0;}
.accueil-best .best-grp{font-size:.92rem;text-transform:uppercase;
 letter-spacing:.06em;color:var(--muted);margin:1.2rem 0 .2rem;}
.dossier-vignettes{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));margin:.6rem 0;}
.dossier-vignette{display:block;background:var(--card);border:1px solid transparent;
 border-radius:var(--radius);padding:1.1rem 1.2rem;text-decoration:none;color:var(--ink);
 transition:border-color .15s,box-shadow .15s;}
.dossier-vignette:hover{border-color:var(--terra-dk);box-shadow:0 4px 16px rgba(33,29,24,.08);}
.dossier-vignette h3{margin:0 0 .35rem;font-size:1.12rem;line-height:1.3;}
.dossier-vignette p{font-size:.9rem;color:var(--muted);margin:.2rem 0 .6rem;}
.dossier-vignette .dv-meta{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;
 font-family:-apple-system,system-ui,sans-serif;font-size:.82rem;font-weight:600;color:var(--terra-dk);}
/* aperçu de carte vivant sur l'accueil */
.carte-teaser{margin:1.6rem 0;}
.carte-teaser .sec{margin-top:0;}
.carte-teaser .lead{max-width:60ch;}
.carte-home-link{display:block;position:relative;border-radius:var(--radius);
 overflow:hidden;text-decoration:none;border:1px solid var(--line);}
.carte-home-map{height:340px;width:100%;pointer-events:none;background:#e8efe6;}
.carte-home-cta{position:absolute;bottom:1.1rem;left:50%;transform:translateX(-50%);
 z-index:1001;background:var(--ink);color:#fff;padding:.6rem 1.3rem;border-radius:999px;
 font-weight:600;font-size:.95rem;box-shadow:0 4px 18px rgba(0,0,0,.3);
 font-family:-apple-system,system-ui,sans-serif;}
.carte-home-link:hover .carte-home-cta{background:var(--green-dk);}
@media (max-width:480px){.carte-home-map{height:260px;}}

.explain-grid,.cat-cards{display:grid;gap:1rem;}
.explain-grid{grid-template-columns:repeat(auto-fit,minmax(220px,1fr));}
.explain-grid h3{margin-top:0;}
.explain-grid p{font-size:.95rem;color:var(--muted);}
.cat-cards{grid-template-columns:repeat(auto-fit,minmax(260px,1fr));}
.cat-card{display:block;background:var(--card);border:1px solid transparent;
 border-radius:var(--radius);padding:1.1rem 1.2rem;text-decoration:none;
 color:var(--ink);transition:border-color .15s,box-shadow .15s;}
.cat-card:hover{border-color:var(--green);box-shadow:0 4px 16px rgba(33,29,24,.08);}
.cat-card h3{margin-top:0;}
.cat-card p{font-size:.92rem;color:var(--muted);}
.cat-n{font-family:-apple-system,system-ui,sans-serif;font-size:.83rem;
 font-weight:600;color:var(--green-dk);}

/* cards */
.cards{list-style:none;padding:0;margin:1.2rem 0;display:grid;gap:.9rem;
 grid-template-columns:repeat(auto-fill,minmax(300px,1fr));}
.card{position:relative;background:var(--card);border:1px solid var(--line);
 border-radius:var(--radius);padding:1rem 1.15rem;
 transition:border-color .15s,box-shadow .15s;}
.card:hover{border-color:var(--green);box-shadow:0 4px 16px rgba(33,29,24,.07);}
/* stretched-link : l'indicateur de focus porte sur la carte entière, pas sur
   le seul titre, pour refléter la cible cliquable réelle (audit a11y C, I5). */
.card:focus-within{border-color:var(--green);
 outline:2px solid var(--ink);outline-offset:2px;}
.card-link:focus-visible{outline:none;}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:.5rem;}
.card h3{margin:.5rem 0 .2rem;font-size:1.16rem;line-height:1.3;}
.card h3 a{text-decoration:none;color:var(--ink);}
.card h3 a:hover{color:var(--green-dk);}
/* stretched link : toute la carte est cliquable, zéro JS */
.card-link::after{content:"";position:absolute;inset:0;border-radius:var(--radius);}
.card-sub{font-size:.9rem;color:var(--muted);margin:.1rem 0;}
.card-meta{font-size:.8rem;color:var(--faint);margin:.2rem 0 .5rem;}
.card-viz{display:flex;justify-content:center;}

/* tags */
.tag{font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700;
 padding:.2rem .5rem;border-radius:var(--radius-sm);color:var(--paper);white-space:nowrap;}
.tag-lieu{background:var(--green-dk);}
.tag-porteur{background:var(--terra-dk);}
.tag-usufruitier{background:var(--blue-dk);}
.tag-modele{background:var(--gold-dk);}
.tag-reseau{background:var(--ink);}.tag-montage{background:#7a6a52;}
/* verdict calculé du lieu */
.verdict{font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;
 font-weight:700;padding:.18rem .55rem;border-radius:var(--radius-pill);
 white-space:nowrap;border:1.5px solid currentColor;}
.verdict-sanctuaire{color:var(--green-dk);background:rgba(53,96,38,.10);}
.verdict-hybride{color:var(--gold-dk);background:rgba(138,100,32,.10);}
.verdict-marchand{color:var(--terra-dk);background:rgba(143,63,37,.10);}
.verdict-na{color:var(--faint);background:transparent;font-weight:600;}
/* carte des lieux (Leaflet) */
.carte-map{height:70vh;min-height:400px;width:100%;border-radius:var(--radius);
 border:1px solid var(--line);margin:.5rem 0 1rem;z-index:0;}
.carte-legende{display:flex;flex-wrap:wrap;gap:.4rem 1.1rem;margin:.6rem 0;}
.carte-leg-item{display:inline-flex;align-items:center;gap:.4rem;
 font-size:.82rem;color:var(--muted);}
.carte-leg-dot{display:inline-block;width:.85rem;height:.85rem;border-radius:50%;
 border:1.5px solid var(--paper);box-shadow:0 0 0 1px var(--line);}
.carte-pop{display:flex;flex-direction:column;gap:.3rem;min-width:9rem;}
.carte-pop-nom{font-weight:700;font-size:.98rem;color:var(--green-dk);}
.carte-pop-verdict{font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;
 font-weight:700;}
.carte-pop-meta{font-size:.82rem;color:var(--muted);}
.carte-pop-lieu{font-size:.8rem;color:var(--faint);}
.carte-pop-link{font-size:.85rem;font-weight:600;}
/* étiquettes de contexte de chaîne — porteur / réseau */
.ctx-labs{display:inline;}
.ctx-lab{display:inline-block;vertical-align:middle;white-space:nowrap;
 margin:.1rem 0 .1rem .4rem;font-size:.68rem;font-weight:400;
 padding:.13rem .5rem;border-radius:var(--radius-pill);background:var(--beige);
 color:var(--muted)!important;border:1px solid var(--line);
 text-decoration:none;line-height:1.4;}
.ctx-lab:hover{border-color:var(--muted);color:var(--ink)!important;}
.ctx-k{font-size:.58rem;text-transform:uppercase;letter-spacing:.05em;
 font-weight:700;color:var(--faint);}

/* pentagone radar de profil à cinq axes */
.tri{width:118px;height:auto;display:block;flex:0 0 auto;}
.tri.compact{width:100px;}
.score-main .tri{width:160px;margin:.6rem auto 0;}
.tri-frame{fill:none;stroke:var(--line);stroke-width:1;}
.tri-grid{fill:none;stroke:var(--line);stroke-width:1;stroke-dasharray:2 2;}
/* remplissage neutre, découplé des couleurs d'axe (audit dataviz B, M5) */
.tri-fill{fill:rgba(34,31,26,.10);stroke:var(--ink);stroke-width:1.6;
 stroke-linejoin:round;}
/* arête vers un axe non renseigné : hachurée, signale une donnée indéterminée */
.tri-edge-na{stroke:var(--faint);stroke-width:1.6;stroke-dasharray:3 2;}
.tri-vtx.tri-na{fill:var(--paper);stroke:var(--faint);stroke-width:1;
 stroke-dasharray:2 1.5;}
/* numéro d'axe : posé hors du sommet, donc en encre foncée et non en blanc */
.tri-lab{font:700 8px -apple-system,system-ui,sans-serif;fill:var(--muted);
 text-anchor:middle;dominant-baseline:central;}
.tri-scale{font:6px -apple-system,system-ui,sans-serif;fill:var(--faint);
 text-anchor:middle;}

/* note de chaîne : écart indice intrinsèque / effectif sur la fiche */
.chaine-note{font-size:.82rem;color:var(--faint);margin:.5rem 0 0;
 font-family:-apple-system,system-ui,sans-serif;}

/* cinq pôles (page régimes) */
.pole-grid{display:grid;gap:1rem;margin:1.1rem 0;
 grid-template-columns:repeat(auto-fit,minmax(220px,1fr));}
.pole-card{border:1px solid var(--line);border-top:3px solid var(--terra);
 border-radius:var(--radius);padding:.5rem 1.1rem 1rem;background:var(--card);}
.pole-card:nth-child(1){border-top-color:var(--green-dk);}
.pole-card:nth-child(2){border-top-color:var(--green);}
.pole-card:nth-child(3){border-top-color:var(--gold);}
.pole-card:nth-child(4){border-top-color:var(--terra);}
.pole-card:nth-child(5){border-top-color:var(--terra-dk);}
.pole-rang{font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;
 color:var(--faint);font-weight:700;margin:.2rem 0 0;
 font-family:-apple-system,system-ui,sans-serif;}
.pole-card h3{font-size:1.05rem;margin:.2rem 0 .3rem;}
.pole-role{color:var(--faint);font-style:italic;font-size:.86rem;}
.pole-line{font-size:.88rem;color:var(--muted);margin:.35rem 0;}

/* idl badge — anneau */
.idl-badge{display:inline-flex;flex-direction:column;align-items:center;
 gap:.15rem;line-height:1.1;}
.idl-ring{width:46px;height:46px;}
.idl-badge.big .idl-ring{width:92px;height:92px;}
.idl-track{fill:none;stroke:var(--beige-dk);}
.idl-arc{fill:none;stroke:var(--pal,#999);stroke-linecap:round;}
/* le chiffre de l'Indice est porté par var(--ink) : contraste > 12:1, la
   couleur du palier restant sur l'anneau (audit a11y C, I1). */
.idl-num{fill:var(--ink);font-weight:800;text-anchor:middle;
 dominant-baseline:central;font-family:-apple-system,system-ui,sans-serif;}
.idl-pal{font-size:.62rem;text-transform:uppercase;letter-spacing:.04em;
 color:var(--muted);text-align:center;max-width:9rem;}
/* sur la carte, le palier est déjà porté par la couleur de l'anneau et le
   classement ; on masque le libellé répété pour alléger la grille (design B, M8) */
.card .idl-pal{display:none;}
.idl-badge.big .idl-pal{font-size:.78rem;letter-spacing:.06em;}
.idl-estime .idl-arc{stroke-dasharray:4 3;}
.idl-estime .idl-num{font-style:italic;}
.idl-na{display:inline-block;border:2px solid var(--faint);color:var(--faint);
 border-radius:var(--radius);padding:.3rem .6rem;font-family:-apple-system,system-ui,sans-serif;
 font-size:.8rem;}

/* jauge linéaire idl */
.idl-scale{position:relative;margin:.8rem 0 .2rem;}
.idl-scale-track{position:relative;display:block;height:12px;border-radius:6px;
 overflow:hidden;background:var(--beige-dk);}
.idl-seg{position:absolute;top:0;height:100%;}
.idl-cursor{position:absolute;top:-3px;width:5px;height:18px;background:var(--ink);
 border-radius:2px;box-shadow:0 0 0 1.6px #fff,0 1px 3px rgba(0,0,0,.4);
 transform:translateX(-50%);}
.idl-ghost{position:absolute;top:-6px;width:0;height:0;
 border-left:3.5px solid transparent;border-right:3.5px solid transparent;
 border-top:5px solid rgba(34,31,26,.34);transform:translateX(-50%);}
.idl-scale-ends{display:flex;justify-content:space-between;font-size:.68rem;
 color:var(--faint);font-family:-apple-system,system-ui,sans-serif;margin-top:.15rem;}

/* axis bars */
.axis-block{margin:.6rem 0;}
.axis-row{display:flex;align-items:center;gap:.5rem;margin:.3rem 0;font-size:.82rem;}
.axis-label{flex:0 0 8.4rem;color:var(--muted);overflow:hidden;text-overflow:ellipsis;
 white-space:nowrap;}
.axis-track{flex:1;height:.5rem;background:var(--beige-dk);
 border-radius:var(--radius-sm);overflow:hidden;}
/* liseré 1px var(--ink) : garantit le 3:1 de délimitation de la jauge
   quelle que soit la couleur d'axe (audit a11y C, I2). */
.axis-fill{display:block;height:100%;border-radius:var(--radius-sm);
 box-shadow:inset 0 0 0 1px rgba(34,31,26,.55);}
.axis-fill.axis-na{box-shadow:none;}
.axis-fill.axis-na{background:repeating-linear-gradient(45deg,#ddd,#ddd 3px,#eee 3px,#eee 6px)!important;}
.axis-val{flex:0 0 2.1rem;text-align:right;font-weight:700;font-variant-numeric:tabular-nums;}
.axis-block.compact .axis-label{flex-basis:5.6rem;font-size:.72rem;}
.axis-block.compact .axis-row{font-size:.72rem;margin:.22rem 0;}

/* toolbar / filtres */
.toolbar{display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin:1.3rem 0 .7rem;}
.toolbar input[type=search]{flex:1;min-width:180px;font:inherit;font-size:.9rem;
 padding:.45rem .65rem;border:1px solid var(--line);border-radius:var(--radius);
 background:var(--card);font-family:-apple-system,system-ui,sans-serif;
 transition:border-color .15s,box-shadow .15s;}
.toolbar input[type=search]:focus{border-color:var(--green);
 box-shadow:0 0 0 3px rgba(74,122,58,.15);outline:none;}
.sort-lab{font-size:.85rem;color:var(--muted);}
select{font:inherit;font-family:-apple-system,system-ui,sans-serif;font-size:.85rem;
 padding:.4rem .6rem;border:1px solid var(--line);border-radius:var(--radius);
 background:var(--card);color:var(--ink);cursor:pointer;}
.count{margin-left:auto;color:var(--faint);font-size:.85rem;}
.count b{color:var(--green-dk);}
/* filtres avancés repliés — n'occupent pas de hauteur avant les cartes */
.filter-details{margin:.4rem 0 .8rem;}
.filter-details summary{font-family:-apple-system,system-ui,sans-serif;
 font-size:.84rem;color:var(--muted);cursor:pointer;padding:.3rem 0;
 width:fit-content;}
.filter-details summary:hover{color:var(--green-dk);}
.filter-details[open] summary{margin-bottom:.3rem;}
.filter-bar{display:flex;flex-direction:column;gap:.5rem;margin:.2rem 0 1.2rem;}
.filter-row{display:flex;gap:.4rem;flex-wrap:wrap;align-items:center;}
.filter-lab{font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;
 color:var(--faint);font-weight:700;flex:0 0 4.4rem;}
.fbtn{font:inherit;font-family:-apple-system,system-ui,sans-serif;font-size:.83rem;
 min-height:32px;padding:.4rem .8rem;border:1px solid var(--line);
 border-radius:var(--radius-pill);
 background:var(--card);color:var(--muted);cursor:pointer;
 transition:background .15s,color .15s,border-color .15s;}
.fbtn:hover{border-color:var(--green);color:var(--ink);}
.fbtn.active{background:var(--green-dk);color:var(--paper);border-color:var(--green-dk);}
.fbtn:focus-visible{outline-color:var(--ink);}
.no-result{background:var(--beige);
 padding:.7rem 1rem;border-radius:var(--radius);font-size:.92rem;color:var(--muted);}
.cat-foot{font-family:-apple-system,system-ui,sans-serif;font-size:.86rem;
 margin:1.6rem 0 .4rem;}

/* fiche */
.crumb{font-size:.85rem;font-family:-apple-system,system-ui,sans-serif;
 margin:1.2rem 0 0;color:var(--muted);}
.crumb a{text-decoration:none;}
.crumb a:hover{text-decoration:underline;}
.crumb [aria-current]{color:var(--faint);}
.fiche-head{margin:.5rem 0 1rem;}
.fiche-head h1{margin:.3rem 0 .15rem;}
.fiche-sub{color:var(--muted);font-size:1.08rem;line-height:1.45;margin:0;}

/* score panel — composant primaire */
.score-panel{display:flex;gap:1.6rem;flex-wrap:wrap;align-items:flex-start;
 background:var(--card);border:1px solid var(--line);
 border-left:3px solid var(--pal,var(--green));border-radius:var(--radius);
 padding:1.6rem 1.8rem;margin:1.4rem 0;box-shadow:0 3px 14px rgba(33,29,24,.06);}
.score-main{text-align:center;flex:0 0 12rem;max-width:12rem;}
.score-main .axes-calc{font-size:.78rem;color:var(--muted);margin:.3rem 0 0;
 line-height:1.35;overflow-wrap:break-word;word-break:normal;hyphens:auto;}
.score-cap{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;
 color:var(--muted);margin:0 0 .35rem;}
/* un seul séparateur : le gap suffit, le filet gauche est retiré (design B, M5) */
/* un peu moins de largeur au centre (axes), un peu plus à Repères :
   évite que Repères saute à la ligne quand axes-calc a un texte long. */
.score-axes{flex:1;min-width:200px;}
/* 3e colonne du panneau de score — repères compacts */
.score-bref{flex:0 0 21rem;font-size:.8rem;}
.score-bref dl{margin:.1rem 0 0;}
.sb-item{display:flex;justify-content:space-between;gap:.7rem;
 padding:.26rem 0;border-bottom:1px solid var(--line);}
.sb-item:last-child{border-bottom:none;}
.sb-item dt{color:var(--faint);}
.sb-item dd{margin:0;text-align:right;overflow-wrap:anywhere;}
.fiab{font-size:.82rem;margin:.6rem 0 0;font-weight:600;}
.fiab-ok{color:var(--green-dk);}
.fiab-gold{color:var(--gold-dk);}
.fiab-faint{color:var(--faint);}
.completude{font-size:.8rem;color:var(--faint);margin:.2rem 0 0;}

/* 1.5 — objet-verdict composite : ligne en tête du panneau de score, pleine
   largeur (force un retour avant les colonnes flex). Trois libellés distincts :
   badge verdict coloré · nombre /100 · étiquette de palier. */
.verdict-composite{flex:0 0 100%;display:flex;flex-wrap:wrap;align-items:center;
 gap:.6rem 1rem;padding-bottom:1rem;margin-bottom:.3rem;
 border-bottom:1px solid var(--line);}
.vco-line{display:flex;align-items:center;gap:.55rem;flex-wrap:wrap;
 font-size:1.05rem;}
.vco-sep{color:var(--faint);font-weight:400;}
.vco-idl b{font-size:1.25rem;font-variant-numeric:tabular-nums;}
.vco-idl .vco-unit{font-size:.78rem;color:var(--faint);margin-left:.1rem;}
.vco-pal{font-size:.82rem;font-weight:600;color:var(--pal,var(--green-dk));
 background:color-mix(in srgb,var(--pal,var(--green)) 14%,transparent);
 border-radius:999px;padding:.12rem .6rem;}
.vco-renvoi{font-size:.8rem;color:var(--muted);margin-left:auto;white-space:nowrap;}
.vco-renvoi:hover{color:var(--green-dk);}

/* 1.4 — « Plafonds appliqués » : une seule ligne repliable regroupant les
   annotations de plafonnement (chaîne, maillon limitant, complétude). */
.plafonds-fold{margin:.6rem 0 0;font-family:-apple-system,system-ui,sans-serif;}
.plafonds-fold>summary{font-size:.82rem;color:var(--muted);cursor:pointer;
 width:fit-content;}
.plafonds-fold>summary:hover{color:var(--green-dk);}
.plafonds-list{margin:.4rem 0 .2rem;padding-left:1.05rem;}
.plafonds-list li{font-size:.82rem;color:var(--faint);margin:.35rem 0;
 max-width:70ch;line-height:1.45;}
.plafonds-list .chaine-renvoi{color:var(--muted);}

/* clé de lecture de la fiche — repliée, sobre (audit pédagogie C, I1/I3) */
.fiche-key{margin:-.4rem 0 1.2rem;font-family:-apple-system,system-ui,sans-serif;}
.fiche-key summary{font-size:.84rem;color:var(--muted);cursor:pointer;
 padding:.3rem 0;width:fit-content;}
.fiche-key summary:hover{color:var(--green-dk);}
.fiche-key ul{margin:.4rem 0 .2rem;padding-left:1.1rem;}
.fiche-key li{font-size:.88rem;color:var(--muted);margin:.3rem 0;max-width:68ch;}

/* 1.1 — rappel court sous le panneau de score (une phrase + lien Méthode) */
.verdict-cle{font-size:.84rem;color:var(--muted);margin:-.6rem 0 1.2rem;
 max-width:74ch;line-height:1.5;
 font-family:-apple-system,system-ui,sans-serif;}
.verdict-cle a{font-weight:600;}
.fiche-dossier-lien{margin:.2rem 0 1rem;font-family:-apple-system,system-ui,sans-serif;
 font-size:.92rem;font-weight:600;}

/* grille repliable */
.grille-fold>summary.sec{cursor:pointer;width:fit-content;}
.grille-fold>summary.sec .fold-hint{font-weight:400;font-size:.8rem;color:var(--muted);
 text-transform:none;letter-spacing:0;}

/* droit de réponse du porteur (réversibilité) */
.reponse-porteur{background:var(--paper,#fff);border:1px solid var(--line,#e0d9cc);
 border-radius:var(--radius);padding:.8rem 1.1rem;margin:1.2rem 0;}
.reponse-porteur .rp-chapeau{font-size:.85rem;color:var(--muted);
 font-family:-apple-system,system-ui,sans-serif;margin:.2rem 0 .6rem;}
.reponse-porteur .rp-texte{margin:.4rem 0;padding-left:.9rem;
 border-left:3px solid var(--muted);font-style:italic;color:var(--ink);}
.reponse-porteur .rp-meta{font-size:.82rem;color:var(--muted);text-align:right;margin:.3rem 0 0;}

/* en bref — composant tertiaire (info) */
.enbref{background:var(--beige);border-radius:var(--radius);
 padding:1rem 1.3rem;margin:1.2rem 0;font-size:.92rem;}
.enbref .bref-titre{font-size:.95rem;margin:0 0 .8rem;color:var(--muted);
 font-weight:700;text-transform:uppercase;letter-spacing:.04em;}
.enbref dl{display:grid;grid-template-columns:1fr 1fr;gap:.5rem 2.2rem;margin:0;}
.enbref .bref-item{display:grid;grid-template-columns:max-content 1fr;
 gap:.55rem 1rem;align-content:start;}
.enbref dt{color:var(--muted);font-weight:600;}
.enbref dd{margin:0;word-break:break-word;}
.prose{font-size:1.05rem;max-width:68ch;}
.prose.synthese{background:var(--beige);border-left:3px solid var(--green);
 padding:.8rem 1.1rem;border-radius:var(--radius);max-width:none;}
.grille-intro{font-size:.9rem;color:var(--muted);font-family:-apple-system,system-ui,sans-serif;}

/* callouts */
.callout{border-radius:var(--radius);padding:.8rem 1.1rem;margin:1.2rem 0;
 background:var(--beige);}
.callout p{font-size:.95rem;margin:.3rem 0;}
.callout-note{border-left:3px solid var(--gold);}
.callout-warn{border-left:3px solid var(--terra);}

/* récap grille par axe */
.grille-recap{margin:.8rem 0 1rem;display:flex;flex-direction:column;gap:.4rem;}
.rk-row{display:flex;align-items:center;gap:.6rem;font-size:.82rem;
 font-family:-apple-system,system-ui,sans-serif;}
.rk-ax{flex:0 0 11rem;color:var(--muted);}
.rk-bar{flex:0 0 130px;display:flex;height:.7rem;border-radius:var(--radius-sm);
 overflow:hidden;background:var(--beige-dk);}
.rk-seg{display:block;height:100%;}
.rk-txt{color:var(--faint);font-size:.78rem;}

/* corpus histogram */
.corpus-hist{margin:1rem 0;}
.corpus-hist svg{width:100%;max-width:420px;height:auto;}
.corpus-hist figcaption{font-size:.82rem;color:var(--faint);
 font-family:-apple-system,system-ui,sans-serif;margin-top:.3rem;}
.hg-n{font:700 12px -apple-system,system-ui,sans-serif;text-anchor:middle;fill:var(--ink);}
.hg-l{font:9px -apple-system,system-ui,sans-serif;text-anchor:middle;fill:var(--muted);}

/* tables */
.table-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:.6rem 0;}
table{width:100%;border-collapse:collapse;font-size:.9rem;margin:.6rem 0;}
table th,table td{border-bottom:1px solid var(--line);padding:.5rem .55rem;
 text-align:left;vertical-align:top;}
table th{color:var(--muted);font-weight:700;font-size:.72rem;text-transform:uppercase;
 letter-spacing:.04em;border-bottom:1px solid var(--ink);}
.fam-row td,.fam-row th{background:var(--beige);font-weight:700;font-size:.8rem;
 text-transform:uppercase;letter-spacing:.04em;color:var(--muted);
 border-top:2px solid var(--line);text-align:left;}
.crit-name{font-weight:600;}
.crit-note,.crit-def{color:var(--muted);font-size:.86rem;}
.crit-oui{color:var(--green-dk);font-weight:700;}
.crit-partiel{color:var(--gold-dk);font-weight:700;}
.crit-non{color:var(--terra-dk);font-weight:700;}
.crit-inconnu{color:var(--faint);font-style:italic;}
.num{text-align:right;font-variant-numeric:tabular-nums;}
.axe-dot{display:inline-block;width:.62rem;height:.62rem;border-radius:50%;
 margin-right:.35rem;vertical-align:baseline;}
.axe-1{background:var(--axe-1);}
.axe-2{background:var(--axe-2);}
.axe-3{background:var(--axe-3);}
.axe-4{background:var(--axe-4);}
.axe-5{background:var(--axe-5);}
.axe-legend{font-size:.82rem;color:var(--muted);}
.axe-legend .axe-dot{margin-left:.8rem;}
.cat-legend{margin:.4rem 0 1rem;}

/* classement — tri + mini-barres */
.rank-tbl tbody tr:nth-child(even) td{background:rgba(221,212,191,.18);}
.rank-tbl tbody tr:hover td{background:var(--beige);}
.rank-tbl .rank{color:var(--faint);font-weight:700;font-variant-numeric:tabular-nums;}
.rank-tbl .name a{font-weight:700;text-decoration:none;}
.rank-tbl .name a:hover{text-decoration:underline;}
.row-sub{display:block;font-size:.78rem;color:var(--faint);font-weight:400;}
.rank-tbl td.idl-cell,.rank-tbl th.idl-cell{border-left:1px solid var(--line);}
.idl-cell b{color:var(--ink);font-size:1.05rem;font-variant-numeric:tabular-nums;}
.rank-tbl.small{max-width:640px;}
th.sortable{white-space:nowrap;padding:0;}
.th-sort{font:inherit;font-family:-apple-system,system-ui,sans-serif;
 font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;
 color:var(--muted);background:none;border:0;cursor:pointer;width:100%;
 text-align:inherit;padding:.5rem .55rem;}
th.num.sortable .th-sort{text-align:right;}
.th-sort:hover{color:var(--terra-dk);}
th.sortable::after{content:" \\2195";opacity:.4;font-size:.8em;
 display:inline-block;padding-right:.4rem;}
th.sortable[aria-sort=ascending]::after{content:" \\25B2";opacity:1;}
th.sortable[aria-sort=descending]::after{content:" \\25BC";opacity:1;}
.sort-hint{margin:.4rem 0;}
.axc{position:relative;}
.axc .cbar{position:absolute;left:0;bottom:0;height:3px;width:var(--w,0);
 background:var(--ac,#999);opacity:.85;}
.axc .cv{position:relative;font-variant-numeric:tabular-nums;}
.cbar-na{color:var(--faint);}

/* analyse */
.analyse-grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
 margin:1rem 0;}
.an-col{border-radius:var(--radius);padding:.4rem 1rem 1rem;background:var(--card);}
.an-col h3{font-size:.82rem;text-transform:uppercase;letter-spacing:.05em;}
.an-col ul{margin:.3rem 0;padding-left:1.1rem;font-size:.92rem;}
.an-col li{margin:.35rem 0;}
.an-forces{border-top:3px solid var(--axe-4);}
.an-frag{border-top:3px solid var(--axe-1);}
.an-lev{border-top:3px solid var(--axe-3);}

/* strat (grilles page) */
.strat{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
 padding:.6rem 1.2rem 1.2rem;margin:1rem 0 2rem;}

/* chips — montages reliés avec profil */
.chips{display:flex;flex-wrap:wrap;gap:.6rem;margin:.6rem 0;}
.rel-grp{font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;
 color:var(--faint);font-weight:700;margin:1.1rem 0 .1rem;
 font-family:-apple-system,system-ui,sans-serif;}
.chip{display:inline-block;background:var(--card);border:1px solid var(--line);
 border-radius:var(--radius-pill);padding:.3rem .8rem;font-size:.85rem;
 text-decoration:none;color:var(--ink);
 font-family:-apple-system,system-ui,sans-serif;
 transition:background .15s,border-color .15s,color .15s;}
.chip:hover{border-color:var(--green);color:var(--ink);}
.chip-rel{display:flex;align-items:center;gap:.55rem;border-radius:var(--radius);
 padding:.5rem .8rem;}
.chip-rel .tri.compact{flex:0 0 auto;width:54px;}
.chip-txt{display:flex;flex-direction:column;line-height:1.25;}
.chip-cat{font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;
 color:var(--faint);}

/* fiab box / sources — tertiaire */
.fiab-box{background:var(--beige);border-radius:var(--radius);
 padding:.7rem 1.2rem;margin:1.4rem 0;}
.fiab-box h3{margin:.3rem 0;font-size:.85rem;text-transform:uppercase;letter-spacing:.05em;
 font-family:-apple-system,system-ui,sans-serif;color:var(--muted);}
.fiab-box p{font-size:.9rem;margin:.3rem 0;}
.src-list{font-size:.9rem;}
.backlink{font-family:-apple-system,system-ui,sans-serif;font-size:.88rem;margin-top:2rem;}

/* classement legend */
.paliers-legend{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0;}
.pal-chip{font-size:.78rem;font-weight:600;border-left:3px solid var(--pal,#999);
 background:var(--card);padding:.25rem .6rem;border-radius:var(--radius-sm);}
.pal-chip em{color:var(--faint);font-style:normal;}

/* axe cards (methode) — élargis d'un tiers */
.axe-cards{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(307px,1fr));
 margin:1.1rem 0;}
.axe-card{border:1px solid var(--line);border-top:3px solid var(--c,#999);
 border-radius:var(--radius);padding:.4rem 1.1rem 1rem;background:var(--card);}
.axe-card h3{font-size:1.05rem;}
.axe-q{font-style:italic;color:var(--muted);font-size:.92rem;}
.axe-card p{font-size:.9rem;}
/* voix incarnée du double registre — glose en clair d'un concept */
.enclair{color:var(--ink);border-left:3px solid var(--gold);padding-left:.75rem;
 margin:.55rem 0;}
code{background:var(--beige);padding:.1rem .35rem;border-radius:var(--radius-sm);font-size:.86rem;}
.note{font-size:.83rem;color:var(--faint);}

/* trois régimes du sol */
.regime-grid{display:grid;gap:1rem;margin:1.1rem 0;
 grid-template-columns:repeat(auto-fit,minmax(240px,1fr));}
.regime-card{border:1px solid var(--line);border-top:3px solid var(--green);
 border-radius:var(--radius);padding:.5rem 1.1rem 1rem;background:var(--card);}
.regime-card:nth-child(2){border-top-color:var(--terra);}
.regime-card:nth-child(3){border-top-color:var(--gold);}
.regime-card h3{font-size:1.05rem;}
.regime-card p{font-size:.9rem;margin:.45rem 0;}
.regime-outils,.regime-but{color:var(--muted);}
.regime-role{color:var(--faint);font-style:italic;font-size:.85rem!important;}
.regimes-tbl th[scope=row]{font-weight:600;color:var(--ink);text-transform:none;
 letter-spacing:0;font-size:.86rem;border-bottom:1px solid var(--line);}

/* liens vers le glossaire — sobres : soulignement pointillé discret, pas de
   couleur vive, pour ne pas surcharger la prose (audit pédagogie C, C1) */
a.gloss-link{color:inherit;text-decoration:underline;
 text-decoration-style:dotted;text-decoration-thickness:1px;
 text-underline-offset:2px;text-decoration-color:var(--faint);}
a.gloss-link:hover{color:var(--green-dk);text-decoration-color:var(--green-dk);}

/* glossaire */
.glossaire{margin:1.4rem 0;display:flex;flex-direction:column;gap:0;}
.gloss-item{border-bottom:1px solid var(--line);padding:.9rem 0;}
.gloss-item dt{font-size:1.05rem;font-weight:700;color:var(--ink);
 margin-bottom:.2rem;}
.gloss-item dd{margin:0;font-size:1.02rem;color:var(--muted);max-width:70ch;}

/* comparateur — deux colonnes, réutilise les styles de carte et d'axes */
.cmp-pickers{display:flex;gap:1rem;flex-wrap:wrap;margin:1.3rem 0 .6rem;}
.cmp-pickers label{display:flex;flex-direction:column;gap:.25rem;flex:1 1 220px;
 font-family:-apple-system,system-ui,sans-serif;font-size:.82rem;
 color:var(--muted);font-weight:600;}
.cmp-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0;}
.cmp-col{background:var(--card);border:1px solid var(--line);
 border-radius:var(--radius);padding:1rem 1.15rem;}
.cmp-col.cmp-empty{display:flex;align-items:center;justify-content:center;
 min-height:8rem;border-style:dashed;}
.cmp-col-head{display:flex;justify-content:space-between;align-items:flex-start;
 gap:.5rem;}
.cmp-idl{display:inline-flex;flex-direction:column;align-items:flex-end;
 line-height:1.1;border-right:3px solid var(--pal,#999);padding-right:.5rem;}
.cmp-idl b{font-size:1.2rem;font-variant-numeric:tabular-nums;color:var(--ink);
 font-family:-apple-system,system-ui,sans-serif;}
.cmp-name{font-size:1.2rem;margin:.6rem 0 .15rem;border:0;padding:0;}
.cmp-name::before{display:none;}
.cmp-sub{font-size:.88rem;color:var(--muted);margin:.1rem 0 .6rem;
 font-family:-apple-system,system-ui,sans-serif;}
.cmp-dl{display:grid;grid-template-columns:max-content 1fr;gap:.4rem 1rem;
 margin:.8rem 0 .4rem;font-size:.86rem;
 font-family:-apple-system,system-ui,sans-serif;}
.cmp-dl dt{color:var(--muted);font-weight:600;}
.cmp-dl dd{margin:0;}
.cmp-link{font-family:-apple-system,system-ui,sans-serif;font-size:.86rem;
 margin:.6rem 0 0;}
@media(max-width:560px){.cmp-grid{grid-template-columns:1fr;}}

/* footer */
.footer{border-top:2px solid var(--ink);margin-top:3rem;background:var(--paper);}
.footer .wrap{padding:1.6rem 1.3rem 2.2rem;}
.footer p{font-size:.86rem;color:var(--muted);margin:.4rem 0;
 font-family:-apple-system,system-ui,sans-serif;}
.foot-links a{color:var(--green-dk);}

/* tablette */
@media(max-width:880px){
 h1{font-size:2.1rem;}
 .hero h1{font-size:2.2rem;}
 h2.sec{font-size:1.45rem;}
 .score-panel{flex-direction:column;}
 .score-axes{border-left:none;border-top:1px solid var(--line);
  padding-left:0;padding-top:1rem;}
 .rk-ax{flex-basis:8rem;}
}

/* mobile */
@media(max-width:620px){
 h1{font-size:1.85rem;}
 .hero{padding:2.4rem 0 1.8rem;}
 .hero h1{font-size:1.95rem;}
 .hero-lead{font-size:1.08rem;}
 .enbref dl{grid-template-columns:1fr;}
 .count{margin-left:0;}
 .rk-row{flex-wrap:wrap;}
 .rk-ax{flex-basis:100%;}
 .rk-bar{flex:1 1 auto;}

 /* nav — pleine largeur sous la marque, cibles tactiles 44px */
 .masthead .wrap{padding-bottom:.3rem;}
 .topnav{gap:.15rem .55rem;width:100%;margin-top:.4rem;
  padding-top:.5rem;border-top:1px solid var(--line);font-size:.82rem;}
 .topnav a{padding:.5rem .55rem;min-height:44px;
  display:flex;align-items:center;}

 /* classement — libellés contraints, sous-titre sur plusieurs lignes */
 .rank-tbl{font-size:.82rem;}
 .rank-tbl td,.rank-tbl th{padding:.4rem .4rem;}
 .rank-tbl .name{min-width:11rem;max-width:13rem;}
 .rank-tbl .row-sub{white-space:normal;line-height:1.25;}
 .th-sort{padding:.45rem .4rem;}

 /* régimes — le tableau déborde proprement, colonne critère figée */
 .regimes-tbl{min-width:34rem;font-size:.82rem;}
 .regimes-tbl th,.regimes-tbl td{padding:.45rem .5rem;}
 .regimes-tbl th[scope=row]{position:sticky;left:0;
  background:var(--card);z-index:1;}

 /* toolbar / filtres — label pleine ligne, boutons et recherche élargis */
 .toolbar{gap:.45rem;}
 .toolbar > label{flex:0 0 100%;font-size:.8rem;
  color:var(--muted);margin-bottom:.1rem;
  font-family:-apple-system,system-ui,sans-serif;}
 .fbtn{min-height:40px;padding:.5rem 1rem;}
 .toolbar input[type=search]{flex:1 1 100%;min-width:0;}

 /* fiche — score panel et axes empilés */
 .score-panel{padding:1.1rem 1rem;}
 .axis-row{flex-wrap:wrap;}
 .axis-label{flex:1 1 100%;white-space:normal;
  overflow:visible;margin-bottom:.1rem;}
 .axis-track{flex:1 1 auto;}

 /* cartes — colonne unique, triangle réduit */
 .cards{grid-template-columns:1fr;}
 .tri.compact{width:78px;}
}

/* très petit écran — hero resserré, CTA pleine largeur */
@media(max-width:400px){
 .hero{padding:1.9rem 0 1.4rem;}
 .hero h1{font-size:1.7rem;}
 .hero-lead{font-size:1rem;}
 .hero-cta{gap:.5rem;}
 .hero-cta .cta{flex:1 1 100%;text-align:center;}
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────────────────────────────────────────

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ── Ressources statiques générées ────────────────────────────────────────────

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="12" fill="#356026"/>
<text x="32" y="44" font-family="-apple-system,system-ui,Segoe UI,sans-serif"
 font-size="34" font-weight="800" fill="#f5f2e9" text-anchor="middle">TL</text>
</svg>
"""

LIST_JS = """/* list.js — filtre, tri et recherche des catalogues.
   Fichier unique mis en cache, partagé par lieux/porteurs/usufruitiers/modeles
   (cf. cycle B — audit performance, B-2). Vanilla JS, aucune dépendance. */
(function(){
 var q=document.getElementById('q'),sort=document.getElementById('sort'),
   cntn=document.getElementById('cntn'),cntl=document.getElementById('cntl'),
   nores=document.getElementById('noresult'),
   sstatus=document.getElementById('sort-status'),
   grid=document.querySelector('.cards');
 if(!grid) return;
 var cards=[].slice.call(document.querySelectorAll('.card')),
   fbtns=[].slice.call(document.querySelectorAll('.fbtn'));
 var active={};
 fbtns.forEach(function(b){
  var k=b.dataset.fk;
  if(b.classList.contains('active')) active[k]=b.dataset.fv;
 });
 function apply(){
  var v=q?q.value.toLowerCase().trim():'',n=0;
  cards.forEach(function(c){
   var ok=c.dataset.nom.toLowerCase().indexOf(v)!==-1;
   for(var k in active){
    if(active[k]&&active[k]!=='all'&&c.dataset[k]!==active[k]) ok=false;
   }
   c.style.display=ok?'':'none';
   if(ok) n++;
  });
  /* on n'écrit que du texte dans la région live (audit a11y C, I3). */
  if(cntn) cntn.textContent=n;
  if(cntl) cntl.textContent=' entrée'+(n>1?'s':'')+' affichée'+(n>1?'s':'');
  if(nores) nores.hidden=n!==0;
 }
 function doSort(){
  var key=sort.value;
  var vis=cards.slice().sort(function(a,b){
   if(key==='nom') return a.dataset.nom.localeCompare(b.dataset.nom,'fr');
   return (parseFloat(b.dataset[key])||0)-(parseFloat(a.dataset[key])||0);
  });
  vis.forEach(function(c){grid.appendChild(c);});
  /* annonce du tri pour les lecteurs d'écran (audit a11y C, C1). */
  if(sstatus) sstatus.textContent='Liste triée : '
   +sort.options[sort.selectedIndex].text+'.';
 }
 if(q) q.addEventListener('input',apply);
 if(sort) sort.addEventListener('change',doSort);
 fbtns.forEach(function(b){
  b.addEventListener('click',function(){
   var k=b.dataset.fk;
   document.querySelectorAll('.fbtn[data-fk="'+k+'"]').forEach(function(x){
    x.classList.remove('active');x.setAttribute('aria-pressed','false');
   });
   b.classList.add('active');b.setAttribute('aria-pressed','true');
   active[k]=b.dataset.fv;apply();
  });
 });
})();

/* Classement — tri de colonnes + filtre par catégorie (page classement.html). */
(function(){
 var tbl=document.querySelector('.rank-tbl');
 if(!tbl||!tbl.tBodies.length||!tbl.tHead) return;
 var tb=tbl.tBodies[0],
   ths=[].slice.call(tbl.tHead.rows[0].cells),
   btns=[].slice.call(document.querySelectorAll('.fbtn[data-f]')),
   status=document.getElementById('sort-status');
 function reindex(){
  var i=0;
  [].slice.call(tb.rows).forEach(function(t){
   if(t.style.display!=='none'){i++;t.querySelector('.rank').textContent=i;}
  });
 }
 btns.forEach(function(b){
  b.addEventListener('click',function(){
   btns.forEach(function(x){
    x.classList.remove('active');x.setAttribute('aria-pressed','false');
   });
   b.classList.add('active');b.setAttribute('aria-pressed','true');
   var f=b.dataset.f;
   [].slice.call(tb.rows).forEach(function(t){
    t.style.display=(f==='all'||t.dataset.cat===f)?'':'none';
   });
   reindex();
  });
 });
 function cellVal(tr,i,type){
  var t=tr.cells[i].innerText.trim();
  if(type==='num') return t==='—'?-1:(parseFloat(t)||0);
  return t.toLowerCase();
 }
 function sortBy(th){
  var i=ths.indexOf(th),type=th.dataset.sort;
  var dir=th.getAttribute('aria-sort')==='ascending'?-1:1;
  ths.forEach(function(x){
   if(x.classList.contains('sortable')) x.setAttribute('aria-sort','none');
  });
  th.setAttribute('aria-sort',dir===1?'descending':'ascending');
  [].slice.call(tb.rows).sort(function(a,b){
   var va=cellVal(a,i,type),vb=cellVal(b,i,type);
   if(va<vb) return dir;
   if(va>vb) return -dir;
   return 0;
  }).forEach(function(r){tb.appendChild(r);});
  reindex();
  if(status){
   var lab=(th.querySelector('.th-sort')||th).innerText.trim();
   status.textContent='Tableau trié par '+lab+', ordre '
    +(dir===1?'décroissant':'croissant')+'.';
  }
 }
 ths.forEach(function(th){
  if(!th.classList.contains('sortable')) return;
  var btn=th.querySelector('.th-sort');
  (btn||th).addEventListener('click',function(){sortBy(th);});
 });
})();
"""

COMPARE_JS = """/* compare.js — comparateur de deux montages, page comparer.html.
   Rendu côté client depuis data.json. Vanilla JS, aucune dépendance.
   N'est chargé que par comparer.html ; list.js n'est pas touché. */
(function(){
 var selA=document.getElementById('cmp-a'),selB=document.getElementById('cmp-b'),
   grid=document.getElementById('cmp-grid'),warn=document.getElementById('cmp-warn');
 if(!selA||!selB||!grid) return;
 var byUid={};
 function esc(s){
  return String(s==null?'':s).replace(/[&<>"]/g,function(c){
   return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];
  });
 }
 /* Les cinq axes du modèle, injectés depuis ranking.yml à la génération. */
 var AXES=__AXES__;
 var CATLAB={lieu:'Lieu',porteur:'Porteur',usufruitier:'Usufruitier',
   modele:'Modèle voisin'};
 var SLUG={lieu:'l',porteur:'p',usufruitier:'u',modele:'m'};
 function bar(label,col,val){
  var w=(val==null?0:Math.max(0,Math.min(100,val)));
  var txt=(val==null?'n.r.':val);
  return '<div class="axis-row"><span class="axis-label">'+esc(label)
   +'</span><span class="axis-track"><span class="axis-fill'
   +(val==null?' axis-na':'')+'" style="width:'+w+'%;background:'+col
   +'"></span></span><span class="axis-val">'+esc(txt)+'</span></div>';
 }
 function col(d){
  if(!d) return '<div class="cmp-col cmp-empty"><p class="note">'
   +'Choisissez une entrée.</p></div>';
  var bars='';
  for(var i=0;i<AXES.length;i++){
   var av=d.axes?(d.axes[AXES[i][0]]!=null?d.axes[AXES[i][0]]
     :d.axes[String(AXES[i][0])]):null;
   bars+=bar(AXES[i][0]+' · '+AXES[i][1],AXES[i][2],av);
  }
  var estime=d.score_type==='estime';
  var idl=(d.idl==null?'n.r.':d.idl)+(estime?' · estimé':'');
  var pal=d.palier_label?esc(d.palier_label):'—';
  var palCol=d.palier_couleur||'#999';
  var rows='';
  function row(k,v){
   if(!v) return '';
   return '<dt>'+esc(k)+'</dt><dd>'+esc(v)+'</dd>';
  }
  rows+=row('Catégorie',CATLAB[d.categorie]||d.categorie);
  rows+=row('Forme juridique',d.forme_juridique);
  rows+=row('Type de montage',d.montage_label);
  rows+=row('Nature juridique',d.nature_juridique);
  if(d.completude!=null){
   rows+=row('Complétude',Math.round(d.completude*100)+' %');
  }
  var href=SLUG[d.categorie]+'/'+d.uid+'.html';
  return '<div class="cmp-col"><div class="cmp-col-head">'
   +'<span class="tag tag-'+esc(d.categorie)+'">'
   +esc(CATLAB[d.categorie]||d.categorie)+'</span>'
   +'<span class="cmp-idl" style="--pal:'+esc(palCol)+'">'
   +'<b>'+esc(idl)+'</b><span class="idl-pal">'+pal+'</span></span></div>'
   +'<h2 class="cmp-name">'+esc(d.nom)+'</h2>'
   +'<p class="cmp-sub">'+esc(d.sous_titre||'')+'</p>'
   +'<div class="axis-block">'+bars+'</div>'
   +'<dl class="cmp-dl">'+rows+'</dl>'
   +'<p class="cmp-link"><a href="'+esc(href)+'">Fiche complète →</a></p>'
   +'</div>';
 }
 function render(){
  var a=byUid[selA.value],b=byUid[selB.value];
  grid.innerHTML=col(a)+col(b);
  if(a&&b&&a.categorie!==b.categorie){
   warn.textContent='Ces deux entrées relèvent de catégories différentes, '
    +'notées par des grilles distinctes : la comparaison est indicative.';
   warn.hidden=false;
  }else{ warn.hidden=true; }
  var p=new URLSearchParams();
  if(selA.value) p.set('a',selA.value);
  if(selB.value) p.set('b',selB.value);
  var qs=p.toString();
  history.replaceState(null,'',qs?('?'+qs):location.pathname);
 }
 fetch('data.json').then(function(r){return r.json();}).then(function(list){
  list.forEach(function(d){byUid[d.uid]=d;});
  var q=new URLSearchParams(location.search);
  if(q.get('a')&&byUid[q.get('a')]) selA.value=q.get('a');
  if(q.get('b')&&byUid[q.get('b')]) selB.value=q.get('b');
  render();
 }).catch(function(){
  grid.innerHTML='<p class="no-result">Données indisponibles. '
   +'Consultez le <a href="classement.html">classement</a>.</p>';
 });
 selA.addEventListener('change',render);
 selB.addEventListener('change',render);
})();
"""

OG_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#f5f2e9"/>
<rect x="0" y="0" width="1200" height="14" fill="#221f1a"/>
<rect x="80" y="118" width="64" height="64" rx="10" fill="#356026"/>
<text x="112" y="164" font-family="-apple-system,system-ui,Segoe UI,sans-serif"
 font-size="32" font-weight="800" fill="#f5f2e9" text-anchor="middle">TL</text>
<text x="168" y="164" font-family="-apple-system,system-ui,Segoe UI,sans-serif"
 font-size="40" font-weight="700" fill="#221f1a">Terres Libérées</text>
<text x="80" y="320" font-family="Georgia,serif" font-size="76"
 font-weight="700" fill="#221f1a">La terre, soustraite</text>
<text x="80" y="408" font-family="Georgia,serif" font-size="76"
 font-weight="700" fill="#221f1a">au marché.</text>
<rect x="80" y="452" width="60" height="8" fill="#8f3f25"/>
<text x="80" y="520" font-family="-apple-system,system-ui,Segoe UI,sans-serif"
 font-size="30" fill="#5f5849">Annuaire critique des montages de libération des terres en France</text>
</svg>
"""


# CSS additionnel pour les pages /revues/* — typographie de lecture longue,
# colonne étroite, interlignage généreux. Inclus en plus de style.css par
# `extra_css=["style-revue.css"]` dans page() pour les routes revue/article.
CSS_REVUE = """
/* style-revue.css — typographie de lecture longue pour les revues.
   Colonne unique, largeur de lecture confortable, interlignage généreux.
   Inclus en plus de style.css sur les pages /revues/* uniquement. */

main.wrap{max-width:1080px;}
.revue-wrap,main:has(.revue-hero),main:has(.article-head),main:has(.dossier){max-width:42rem;}

/* dossiers — récits de cas (magazine) */
.dossier .crumb{font-family:-apple-system,system-ui,sans-serif;font-size:.85rem;margin:.2rem 0 1rem;}
.dossier-head{margin:.4rem 0 1.2rem;}
.dossier-head h1{font-size:2.3rem;line-height:1.18;margin:.1rem 0 .4rem;}
.dossier-sous{font-size:1.2rem;color:var(--muted);font-style:italic;line-height:1.5;margin:.2rem 0;}
.dossier-meta{font-family:-apple-system,system-ui,sans-serif;font-size:.85rem;color:var(--faint);margin:.3rem 0;}
.dossier-chapeau{font-size:1.25rem;line-height:1.55;color:var(--ink);
 border-left:3px solid var(--terra-dk);padding-left:1rem;margin:1.2rem 0;font-weight:500;}
.dossier-fiche{background:var(--beige);border-radius:var(--radius);padding:.7rem 1rem;
 margin:1.2rem 0;display:flex;gap:.6rem;align-items:baseline;flex-wrap:wrap;
 font-family:-apple-system,system-ui,sans-serif;font-size:.9rem;}
.dossier-fiche .df-txt{color:var(--muted);}
.dossier-corps.prose-long{font-size:1.08rem;line-height:1.72;}
.dossier-corps.prose-long p{margin:1rem 0;}
.dossier-corps.prose-long h2{font-size:1.5rem;margin:2rem 0 .6rem;}
.dossier-corps.prose-long h3{font-size:1.2rem;margin:1.5rem 0 .4rem;}
.dossier-corps.prose-long blockquote{border-left:3px solid var(--muted);
 padding-left:1rem;font-style:italic;color:var(--muted);margin:1.2rem 0;}

.revue-hero{padding:2.6rem 0 1.6rem;border-bottom:1px solid var(--line);
 margin-bottom:1.6rem;}
.revue-hero .hero-kicker{font-size:.78rem;text-transform:uppercase;
 letter-spacing:.14em;color:var(--terra-dk);font-weight:700;margin:0 0 .5rem;
 font-family:-apple-system,system-ui,"Segoe UI",sans-serif;}
.revue-hero h1{font-size:2.4rem;line-height:1.18;max-width:22ch;
 margin:.2rem 0 .5rem;}
.revue-hero .revue-soustitre{font-size:1.18rem;color:var(--muted);
 max-width:46ch;margin:.2rem 0 .8rem;line-height:1.5;font-style:italic;}
.revue-hero .revue-meta{font-family:-apple-system,system-ui,"Segoe UI",sans-serif;
 font-size:.88rem;color:var(--faint);margin:.2rem 0;}
.revue-hero .revue-meta strong{color:var(--ink);font-weight:600;}

.statut-chip{display:inline-block;padding:.12rem .55rem;border-radius:var(--radius-pill);
 font-family:-apple-system,system-ui,"Segoe UI",sans-serif;font-size:.74rem;
 font-weight:600;text-transform:uppercase;letter-spacing:.06em;
 background:var(--beige);color:var(--muted);border:1px solid var(--line);}
.statut-chip.statut-vivant{background:#e7f0dc;color:var(--green-dk);
 border-color:#bcd29c;}
.statut-chip.statut-stabilise,.statut-chip.statut-stabilisee{background:#dfe9ee;
 color:var(--blue-dk);border-color:#a8c4cf;}
.statut-chip.statut-archive,.statut-chip.statut-archivee{background:var(--beige-dk);
 color:var(--faint);}

.revue-prose,.article-prose{font-size:1.08rem;line-height:1.72;color:var(--ink);}
.revue-prose p,.article-prose p{margin:.95rem 0;max-width:42rem;}
.revue-prose h2,.article-prose h2{font-size:1.5rem;font-family:inherit;
 font-weight:600;letter-spacing:-.005em;margin:2.2rem 0 .6rem;
 border-bottom:none;padding-bottom:0;color:var(--ink);}
.revue-prose h2::before,.article-prose h2::before{content:none;}
.revue-prose h3,.article-prose h3{font-size:1.18rem;font-weight:600;
 margin:1.6rem 0 .3rem;color:var(--ink);}
.revue-prose blockquote,.article-prose blockquote{border-left:3px solid var(--terra);
 padding:.3rem 0 .3rem 1rem;margin:1.1rem 0;color:var(--muted);font-style:italic;}
.revue-prose ul,.article-prose ul,.revue-prose ol,.article-prose ol{margin:.8rem 0;
 padding-left:1.5rem;}
.revue-prose li,.article-prose li{margin:.3rem 0;line-height:1.65;}
.revue-prose code,.article-prose code{font-family:"SFMono-Regular",Menlo,Consolas,
 monospace;font-size:.94em;background:var(--beige);padding:.05rem .3rem;
 border-radius:var(--radius-sm);}

.articles-liste{list-style:none;padding:0;margin:1.8rem 0;display:grid;gap:1.4rem;}
.articles-liste .article-item{border-top:1px solid var(--line);padding-top:1.2rem;}
.articles-liste .article-item:first-child{border-top:none;padding-top:0;}
.articles-liste h3{font-size:1.32rem;margin:0 0 .25rem;}
.articles-liste h3 a{color:var(--ink);text-decoration:none;}
.articles-liste h3 a:hover{color:var(--green-dk);text-decoration:underline;}
.articles-liste .article-meta{font-family:-apple-system,system-ui,"Segoe UI",sans-serif;
 font-size:.84rem;color:var(--faint);margin:.1rem 0 .4rem;}
.articles-liste .article-meta .sep{margin:0 .4rem;color:var(--line);}
.articles-liste .article-resume{margin:.3rem 0 0;color:var(--muted);
 line-height:1.55;}

.article-head{padding:1.6rem 0 1rem;border-bottom:1px solid var(--line);
 margin-bottom:1.4rem;}
.article-head .article-kicker{font-size:.78rem;text-transform:uppercase;
 letter-spacing:.12em;color:var(--terra-dk);font-weight:700;
 font-family:-apple-system,system-ui,"Segoe UI",sans-serif;margin:0 0 .4rem;}
.article-head .article-kicker a{color:var(--terra-dk);text-decoration:none;}
.article-head .article-kicker a:hover{text-decoration:underline;}
.article-head h1{font-size:2.2rem;line-height:1.18;max-width:24ch;
 margin:.2rem 0 .4rem;}
.article-head .article-soustitre{font-size:1.14rem;color:var(--muted);
 font-style:italic;line-height:1.5;margin:.2rem 0 .8rem;max-width:46ch;}
.article-head .article-meta{font-family:-apple-system,system-ui,"Segoe UI",sans-serif;
 font-size:.86rem;color:var(--faint);margin:.4rem 0;}
.article-head .article-meta .sep{margin:0 .4rem;color:var(--line);}
.article-head .article-meta strong{color:var(--ink);font-weight:600;}

.article-relations{margin:1.6rem 0;padding:.9rem 1rem;background:var(--card);
 border-left:3px solid var(--blue);border-radius:0 var(--radius) var(--radius) 0;}
.article-relations h4{font-family:-apple-system,system-ui,"Segoe UI",sans-serif;
 font-size:.82rem;text-transform:uppercase;letter-spacing:.08em;
 color:var(--blue-dk);margin:0 0 .3rem;font-weight:700;}
.article-relations ul{list-style:none;padding:0;margin:0;display:flex;
 flex-wrap:wrap;gap:.3rem .7rem;font-family:-apple-system,system-ui,sans-serif;
 font-size:.9rem;}
.article-relations li{margin:0;}

.article-changelog{margin:2.4rem 0 1rem;border-top:1px solid var(--line);
 padding-top:1.2rem;}
.article-changelog h2{font-family:-apple-system,system-ui,"Segoe UI",sans-serif!important;
 font-size:.9rem!important;text-transform:uppercase;letter-spacing:.1em;
 color:var(--faint);font-weight:600;margin:0 0 .6rem!important;}
.article-changelog ol{list-style:none;padding:0;margin:0;
 font-family:-apple-system,system-ui,"Segoe UI",sans-serif;font-size:.88rem;
 color:var(--muted);}
.article-changelog li{margin:.35rem 0;line-height:1.55;}
.article-changelog .ch-date{color:var(--ink);font-weight:600;margin-right:.5rem;}
.article-changelog .ch-version{color:var(--terra-dk);font-weight:600;
 margin-right:.5rem;}

.revue-pdf{margin:2rem 0;padding:1.1rem 1.2rem;background:var(--card);
 border:1px solid var(--line);border-radius:var(--radius);}
.revue-pdf h4{font-family:-apple-system,system-ui,"Segoe UI",sans-serif;
 font-size:.82rem;text-transform:uppercase;letter-spacing:.08em;
 color:var(--terra-dk);margin:0 0 .5rem;font-weight:700;}
.revue-pdf p{margin:.2rem 0;font-size:.95rem;color:var(--muted);}
.revue-pdf .cta-pdf{display:inline-block;margin-top:.6rem;
 background:var(--ink);color:var(--paper)!important;text-decoration:none;
 padding:.5rem 1rem;border-radius:var(--radius);font-weight:600;
 font-family:-apple-system,system-ui,"Segoe UI",sans-serif;font-size:.88rem;}
.revue-pdf .cta-pdf:hover{background:var(--green-dk);}

.revues-grid{display:grid;gap:1.6rem;
 grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin:1.6rem 0;}
.revue-card{background:var(--card);border:1px solid var(--line);
 border-radius:var(--radius);padding:1.4rem 1.5rem;text-decoration:none;
 color:var(--ink);display:flex;flex-direction:column;gap:.4rem;
 transition:border-color .15s,box-shadow .15s;}
.revue-card:hover{border-color:var(--green);
 box-shadow:0 2px 8px rgba(0,0,0,.06);color:var(--ink);}
.revue-card h3{margin:0;font-size:1.32rem;line-height:1.22;color:var(--ink);}
.revue-card .revue-card-sous{color:var(--muted);font-style:italic;
 font-size:1rem;line-height:1.5;margin:.1rem 0 .4rem;}
.revue-card .revue-card-meta{font-family:-apple-system,system-ui,"Segoe UI",sans-serif;
 font-size:.82rem;color:var(--faint);margin-top:auto;}
.revue-card .revue-card-meta .sep{margin:0 .4rem;color:var(--line);}
"""


def build_robots():
    return (f"User-agent: *\nAllow: /\n\n"
            f"Sitemap: {BASE_URL}/sitemap.xml\n")


def build_sitemap(paths):
    """paths : liste de (chemin_relatif, priorité)."""
    urls = ""
    for path, prio in paths:
        urls += (f"  <url>\n    <loc>{canonical_url(path)}</loc>\n"
                 f"    <lastmod>{BUILD_DATE}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n"
                 f"    <priority>{prio}</priority>\n  </url>\n")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "</urlset>\n")


def verifier_entites_html():
    """Garde-fou (leçon du 2026-05-24) : la passe typographique ne doit jamais
    insérer d'espace avant le point-virgule d'une entité HTML — « &#x27 ; » au
    lieu de « &#x27; » casse l'entité à l'affichage. On scanne le site produit ;
    toute entité malformée fait échouer la génération."""
    pat = re.compile(r"&#?[0-9A-Za-z]+[   ]+;")
    fautes = []
    for fp in sorted(SITE.rglob("*.html")):
        for m in pat.finditer(fp.read_text(encoding="utf-8")):
            fautes.append(f"{fp.relative_to(SITE)} : {m.group(0)!r}")
    return fautes


def verifier_liens():
    """Garde-fou (leçon L54, session #11) : tout lien interne relatif d'une page
    produite doit résoudre vers un fichier existant. Le corps Markdown d'un article
    de revue n'est PAS réécrit selon la profondeur de la page (seul le chrome l'est
    via `up`), si bien qu'un lien `../../methode.html` correct au manifeste (prof. 2)
    pointe vers un 404 dans un article (prof. 3). Ce contrôle scanne les `href`
    relatifs du site produit et fait échouer la génération si l'un ne résout pas.
    On ignore les liens externes (http, //, mailto, tel, javascript, data),
    les ancres pures (`#…`) et les href vides."""
    href_pat = re.compile(r'href="([^"]*)"')
    script_pat = re.compile(r"<script\b.*?</script>", re.DOTALL | re.IGNORECASE)
    skip_pref = ("http://", "https://", "//", "mailto:", "tel:", "javascript:",
                 "data:", "#")
    casses = []
    racine = SITE.resolve()
    for fp in sorted(SITE.rglob("*.html")):
        base = fp.parent
        # on retire les blocs <script> : un href construit en JS n'est pas un lien statique
        contenu = script_pat.sub("", fp.read_text(encoding="utf-8"))
        for href in href_pat.findall(contenu):
            h = href.strip()
            if not h or h.startswith(skip_pref):
                continue
            h = h.split("#", 1)[0].split("?", 1)[0]   # retirer fragment et query
            if not h:
                continue
            start = racine if h.startswith("/") else base
            cible = (start / h.lstrip("/")).resolve()
            if cible.is_dir() or h.endswith("/"):
                cible = cible / "index.html"
            try:
                cible.relative_to(racine)
                hors = False
            except ValueError:
                hors = True
            if hors or not cible.exists():
                casses.append(f"{fp.relative_to(SITE)} : href=\"{href}\""
                              + ("  (hors site)" if hors else "  (cible absente)"))
    return casses


def verifier_chaines(fiches):
    """Contrôle de cohérence des chaînes (chantier A, session #3).

    Une chaîne est déclarée par le LIEU, qui nomme ses porteurs et ses
    usufruitiers. Le contrôle vérifie que tout lieu déclare une chaîne complète
    (au moins un porteur ET un usufruitier) et que tout porteur ou usufruitier
    est cité par au moins une chaîne. Les modèles voisins en sont exemptés.
    Avertit sans bloquer la génération : les manques relèvent de la recherche
    (chantier D), pas d'une erreur de code."""
    cites = set()
    for f in fiches:
        if f["categorie"] == "lieu":
            ch = f.get("chaine", {}) or {}
            cites.update(ch.get("porteurs") or [])
            cites.update(ch.get("usufruitiers") or [])
        elif f["categorie"] == "reseau":
            # une entité membre d'un réseau est couverte : elle n'est pas
            # orpheline, elle attend que les lieux du réseau soient carvés.
            cites.update(f.get("membres") or [])
    nature = {f["uid"]: f.get("nature_interet") for f in fiches}
    avert = []
    for f in sorted(fiches, key=lambda x: (x["categorie"], x["uid"])):
        cat, uid = f["categorie"], f["uid"]
        if cat == "lieu":
            ch = f.get("chaine", {}) or {}
            if not (ch.get("porteurs") or []):
                avert.append(f"  lieu {uid} — aucun porteur dans la chaîne")
            if not (ch.get("usufruitiers") or []):
                avert.append(f"  lieu {uid} — aucun usufruitier dans la chaîne")
            # articulations : tout usufruitier articulé doit figurer dans la chaîne
            usufs_ch = set(ch.get("usufruitiers") or [])
            for art in ((f.get("montage", {}) or {}).get("articulations") or []):
                au = art.get("usufruitier")
                if au and au not in usufs_ch:
                    avert.append(f"  lieu {uid} — articulation vers «{au}», "
                                 f"absent de la chaîne")
            # garde-fou chantier 1bis : un montage privé doit s'accorder avec
            # la nature_interet de son porteur.
            mtype = ((f.get("montage", {}) or {}).get("type") or "")
            if mtype.startswith("propriete_privee"):
                want = ("privee_individuelle" if mtype.endswith("individuelle")
                        else "commerciale")
                for p in (ch.get("porteurs") or []):
                    if nature.get(p) not in (want, None):
                        avert.append(f"  lieu {uid} — montage «{mtype}» mais "
                                     f"porteur «{p}» de nature «{nature.get(p)}» "
                                     f"(attendu «{want}»)")
        elif cat in ("porteur", "usufruitier"):
            if uid not in cites:
                avert.append(f"  {cat} {uid} — orphelin : cité par aucune chaîne")
    if avert:
        print(f"Contrôle des chaînes : {len(avert)} signalement·s "
              f"(worklist du chantier D) —")
        for a in avert:
            print(a)
    else:
        print("Contrôle des chaînes : toutes les entités sont reliées.")
    return avert


# Cohérence pôle (integrite_montage.niveau) ↔ verdict calculé du lieu (garde-fou
# souple ajouté en #11 — avertit, ne bloque pas). Le pôle « situe » et peut être
# une aspiration (≠ verdict, cf. L3) ; on ne flague donc QUE les incohérences
# nettes : un pôle élevé sur une chaîne marchande ou non établie, ou
# `economie_marchande` sur un sanctuaire.
_POLES_ELEVES = {"commun_citoyen", "mutualisme", "ig_institue"}


def verifier_poles(fiches, by_uid):
    avert = []
    for f in fiches:
        if f.get("categorie") != "lieu":
            continue
        niveau = (f.get("integrite_montage") or {}).get("niveau")
        if not niveau:
            continue
        v = compute_verdict(f, by_uid)
        uid = f.get("uid")
        if v == "marchand" and niveau in _POLES_ELEVES:
            avert.append(f"  lieu {uid} — pôle «{niveau}» sur chaîne marchande "
                         f"(verdict marchand)")
        elif v is None and niveau in _POLES_ELEVES:
            avert.append(f"  lieu {uid} — pôle «{niveau}» sur chaîne non établie "
                         f"(verdict à établir)")
        elif niveau == "economie_marchande" and v == "sanctuaire":
            avert.append(f"  lieu {uid} — pôle «economie_marchande» sur un "
                         f"sanctuaire (contradiction)")
    if avert:
        print(f"Contrôle des pôles : {len(avert)} signalement·s —")
        for a in avert:
            print(a)
    else:
        print("Contrôle des pôles : cohérence pôle↔verdict OK.")
    return avert


# ─────────────────────────────────────────────────────────────────────────────
# Le faisceau libéré (v3.1) — PILOTE (grille + 3 fiches revues). Additif : ne
# touche pas au rendu des 52 fiches v2. Migration en cours (cf. SEQUENCE).
# ─────────────────────────────────────────────────────────────────────────────
FAISCEAU_CSS = """
.fsc-intro{background:#f4f1ea;border-left:4px solid #6b8f71;padding:12px 16px;border-radius:6px;font-size:.96rem;margin:14px 0}
.fsc-card{border:1px solid #d8d3c6;border-radius:10px;padding:18px 20px;margin:22px 0}
.fsc-hd{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1px solid #eee;padding-bottom:6px}
.fsc-hd h3{margin:0;font-size:1.25rem} .fsc-loc{color:#777;font-size:.85rem}
.fsc-porteur{font-size:.85rem;color:#555;margin:6px 0 10px}
.fsc-score{margin:8px 0 12px} .fsc-band{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.8rem;font-weight:bold;color:#fff;margin-right:6px}
.fb-autogere{background:#3d7a4e}.fb-sorti{background:#b08a3e}.fb-transition{background:#a86a4a}.fb-marchand{background:#9a9a9a}.fb-usage{background:#2f6e8f}.fb-commun{background:#274}
.fsc-q{width:100%;border-collapse:collapse;margin:8px 0;font-size:.9rem}
.fsc-q td,.fsc-q th{padding:5px 8px;border-bottom:1px solid #f0ece2;vertical-align:top;text-align:left}
.fsc-q th{font-weight:bold;width:90px}
.fsc-sym{text-align:center;width:38px;font-size:1.1rem}.s-ok{color:#3d7a4e}.s-mid{color:#b08a3e}.s-no{color:#b04a4a}.s-na{color:#999;font-size:.75rem}
.fsc-nt{color:#555;font-size:.85rem}.fsc-pf{margin-top:6px;font-weight:bold}
.fsc-dr{margin-top:10px;font-size:.8rem;color:#666;background:#faf8f3;padding:8px 10px;border-radius:6px}
.fsc-note{font-size:.8rem;color:#999;margin-top:26px}
.fsc-src{font-size:.72rem;color:#884488;background:#f3eef5;padding:1px 6px;border-radius:8px}.fsc-src.ok{color:#3d7a4e;background:#eef5ef}
"""

def _fsc_card(nom, loc, porteur, band_cls, band_lbl, note, badge, pf, rows, src=""):
    qr = "".join(
        f'<tr><td>{q}</td><td class="fsc-sym {c}">{s}</td><td class="fsc-nt">{n}</td></tr>'
        for q, s, c, n in rows)
    return f"""<div class="fsc-card">
  <div class="fsc-hd"><h3>{nom}</h3><span class="fsc-loc">{loc}</span></div>
  <div class="fsc-porteur">{porteur}</div>
  <div class="fsc-score"><span class="fsc-band {band_cls}">{band_lbl}</span> libération {note} · {badge}{src}</div>
  <table class="fsc-q"><tr><th>la porte</th><td class="fsc-sym s-ok">●</td><td class="fsc-nt">Sortie du marché, pour toujours (préalable franchi).</td></tr>{qr}</table>
  <div class="fsc-pf">Point faible nommé : <b>{pf}</b>.</div>
  <div class="fsc-dr">Vous représentez ce lieu ? <b>Droit de réponse</b> : correction sur pièce, levée d'un « non établi » sur témoignage, réponse libre sans retouche — contact avant toute publication.</div>
</div>"""

FB_CLASS={"marchand":"fb-marchand","en_transition":"fb-transition","sorti_du_marche":"fb-sorti","autogere":"fb-autogere","usage_decommodifie":"fb-usage","commun_vivant":"fb-commun"}
FB_LABEL={"marchand":"marchand","en_transition":"en transition","sorti_du_marche":"sorti du marché","autogere":"autogéré","usage_decommodifie":"usage libéré","commun_vivant":"commun vivant"}
FB_ORDER=["commun_vivant","usage_decommodifie","autogere","sorti_du_marche","en_transition","marchand"]
Q_LABEL=[("milieu","Le milieu"),("vivant","Le vivant"),("ouverture","L'ouverture"),("don","Le don"),("duree","La durée"),("voix","La voix")]
Q6_AXES=[("1","Le milieu","#7a5230"),("2","Le vivant","#3d7a4e"),("3","L'ouverture","#2f6e8f"),("4","Le don","#8a5a8a"),("5","La durée","#b08a3e"),("6","La voix","#225588")]
Q6_CFG=[{"id":a,"label":l,"court":l,"couleur":c} for a,l,c in Q6_AXES]
def _q_scores_from_ev(ev):
    out={}
    for _i,(_k,_l) in enumerate(Q_LABEL,1):
        _v=(ev.get("questions",{}).get(_k,{}) or {}).get("valeur")
        out[str(_i)]=(None if (_v in _FB_UNK or _v is None) else round(_FB_S.get(_v,0.0)*100))
    return out
PF_LABEL={"milieu":"le milieu","vivant":"le vivant","ouverture":"l'ouverture","don":"le don","duree":"la durée","voix":"la voix","porte":"la porte"}
_FB_SYM={"oui":("●","s-ok"),"partiel":("◐","s-mid"),"non":("○","s-no"),"non_etabli":("non établi","s-na"),"projete":("projeté","s-na")}
_FB_BADGE={0:"<span style=\'color:#999;font-size:.85rem\'>pas de badge</span>",1:"🌿 <b>Sanctuaire</b>",2:"🌿🌿 <b>Sanctuaire</b>","non_etabli":"<span style=\'color:#999;font-size:.85rem\'>badge non évalué</span>"}
_FB_S={"oui":1.0,"partiel":0.5,"non":0.0}
_FB_UNK={"non_etabli","projete"}
_FB_BANDS={"marchand":(0,20),"en_transition":(20,40),"sorti_du_marche":(20,50),"autogere":(50,75),"usage_decommodifie":(75,90),"commun_vivant":(90,100)}

def _fsc_derive(ev):
    """Tient l'invariant : bande/suspension/point faible/badge calculés, jamais saisis."""
    porte=ev["porte"]["valeur"]; q=ev["questions"]
    v=lambda n:q[n]["valeur"]; sc=lambda n:_FB_S.get(v(n))
    susp=(porte=="non_etabli") or any(v(n)=="non_etabli" for n in ("voix","duree"))
    if porte=="non": band="marchand"
    elif porte=="partiel": band="en_transition"
    elif susp: band="sorti_du_marche"
    elif sc("voix")==1.0 and sc("duree")==1.0: band="usage_decommodifie" if sc("don")==1.0 else "autogere"
    else: band="sorti_du_marche"
    mil,viv=v("milieu"),v("vivant")
    badge="non_etabli" if (mil in _FB_UNK or viv in _FB_UNK) else (2 if _FB_S[mil]==1 and _FB_S[viv]==1 else (1 if _FB_S[mil]+_FB_S[viv]>=1 else 0))
    if band=="usage_decommodifie" and isinstance(badge,int) and badge>=1: band="commun_vivant"
    chemin=("voix","duree","don","ouverture")
    rank=lambda n:(0 if n in ("voix","duree") and v(n)=="non_etabli" else 1, 9 if v(n) in _FB_UNK else _FB_S[v(n)])
    pf=min(chemin,key=rank); lo,hi=_FB_BANDS[band]
    if susp: num=None
    elif band=="sorti_du_marche": num=round(lo+(hi-lo)*(((1.0 if porte=="oui" else .5)+(sc("ouverture") or 0)+(sc("duree") or 0))/3))
    elif band=="autogere": num=round(lo+(hi-lo)*(sc("don") or 0))
    elif band=="usage_decommodifie": num=round(lo+(hi-lo)*(1.0 if badge!="non_etabli" and badge>=1 else .3))
    else: num=round((lo+hi)/2)
    return band,susp,pf,badge,num

def _v3_grille_fold(ev):
    vmap={"oui":("●","crit-oui"),"partiel":("◐","crit-partiel"),"non":("○","crit-non"),
          "non_etabli":("non établi","crit-inconnu"),"projete":("projeté","crit-inconnu")}
    p=ev.get("porte",{})
    pst={"oui":("franchie","crit-oui"),"partiel":("partielle","crit-partiel"),
         "non":("non franchie","crit-non")}.get(p.get("valeur"),("?","crit-inconnu"))
    trs='<tr class="fam-row"><th colspan="3" scope="colgroup">La porte — préalable (sortir du marché)</th></tr>'
    trs+=f'<tr><td class="crit-name">Sortir du marché</td><td class="{pst[1]}">{pst[0]}</td><td class="crit-note">{e(clean(p.get("note","")))}</td></tr>'
    trs+='<tr class="fam-row"><th colspan="3" scope="colgroup">Les six questions — du lieu vers le groupe</th></tr>'
    for k,lab in Q_LABEL:
        q=ev["questions"][k]; sym,cls=vmap.get(q["valeur"],vmap["non_etabli"])
        trs+=f'<tr><td class="crit-name">{lab}</td><td class="{cls}">{sym}</td><td class="crit-note">{e(clean(q.get("note","")))}</td></tr>'
    return ('<section class="grille-section"><details class="grille-fold">'
      '<summary class="sec">Grille de lecture <span class="fold-hint">— déplier / replier</span></summary>'
      '<p class="grille-intro">La porte (sortir du marché), puis six questions du lieu vers le groupe ; '
      'la note se lit au point le plus faible du chemin. <a href="../methode.html">Comprendre la grille →</a></p>'
      '<div class="table-scroll" tabindex="0" role="region" aria-label="Grille de lecture (faisceau v3.1)">'
      '<table class="grille-tbl"><thead><tr><th scope="col">Critère</th><th scope="col">Évaluation</th>'
      '<th scope="col">Lecture</th></tr></thead><tbody>'+trs+'</tbody></table></div></details></section>')

def _v3_hexstar(ev):
    """Étoile à six branches dédiée v3.1 — SVG autonome (styles inline), lisible :
    labels en toutes lettres, grille concentrique, remplissage teinté palier, point coloré par question."""
    import math as _m
    band,susp,pf,badge,num=_fsc_derive(ev)
    BC={"marchand":"#9a9a9a","en_transition":"#a86a4a","sorti_du_marche":"#b08a3e",
        "autogere":"#3d7a4e","usage_decommodifie":"#2f6e8f","commun_vivant":"#224477"}
    col=BC[band]
    QS=[("milieu","Milieu"),("vivant","Vivant"),("ouverture","Ouverture"),
        ("don","Don"),("duree","Durée"),("voix","Voix")]
    F={"oui":1.0,"partiel":0.55,"non":0.0}
    DOT={"oui":"#3d7a4e","partiel":"#b08a3e","non":"#b04a4a"}
    cx,cy,R=130.0,104.0,66.0
    ang=[-90+i*60 for i in range(6)]
    rad=[a*_m.pi/180 for a in ang]
    vx=[cx+R*_m.cos(r) for r in rad]; vy=[cy+R*_m.sin(r) for r in rad]
    # grille concentrique (3 anneaux) + rayons
    grid=""
    for ring in (0.34,0.67,1.0):
        pts=" ".join(f"{cx+R*ring*_m.cos(r):.1f},{cy+R*ring*_m.sin(r):.1f}" for r in rad)
        grid+=f'<polygon points="{pts}" fill="none" stroke="#e3ded2" stroke-width="1"/>'
    for i in range(6):
        grid+=f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{vx[i]:.1f}" y2="{vy[i]:.1f}" stroke="#ece8de" stroke-width="1"/>'
    # polygone de profil + points colorés
    poly=[]; dots=""
    miss=0
    for i,(k,_) in enumerate(QS):
        val=ev["questions"][k]["valeur"]
        if val in ("non_etabli","projete"):
            f=0.0; miss+=1; dcol="#fff"; dstroke="#bbb"
        else:
            f=F.get(val,0.0); dcol=DOT.get(val,"#b04a4a"); dstroke=dcol
        px=cx+(vx[i]-cx)*f; py=cy+(vy[i]-cy)*f
        poly.append(f"{px:.1f},{py:.1f}")
        dots+=f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.3" fill="{dcol}" stroke="{dstroke}" stroke-width="1.5"/>'
    fill = "" if miss>=3 else f'<polygon points="{" ".join(poly)}" fill="{col}" fill-opacity="0.18" stroke="{col}" stroke-width="2" stroke-linejoin="round"/>'
    # labels en toutes lettres
    labs=""
    for i,(k,lab) in enumerate(QS):
        val=ev["questions"][k]["valeur"]
        lx=cx+(vx[i]-cx)*1.34; ly=cy+(vy[i]-cy)*1.34
        anchor="middle"
        if lx-cx>10: anchor="start"
        elif lx-cx<-10: anchor="end"
        dy=-3 if (ly<cy-2) else (11 if ly>cy+2 else 4)
        gcl="#999" if val in ("non_etabli","projete") else "#3a3a32"
        labs+=f'<text x="{lx:.1f}" y="{ly+dy:.1f}" text-anchor="{anchor}" font-size="11" font-weight="600" fill="{gcl}">{lab}</text>'
    aria="Profil des six questions : "+", ".join(f"{lab} {ev['questions'][k]['valeur']}" for k,lab in QS)
    return (f'<svg class="v3-star" viewBox="0 0 260 208" role="img" aria-label="{e(aria)}" '
            f'style="width:100%;max-width:300px;height:auto;display:block;margin:0 auto">'
            f'{grid}{fill}{dots}{labs}'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.6" fill="#bbb"/></svg>')

def _v3_chaine(ev):
    """Colonne-chaîne (reco @graphiste) : six maillons ●◐○ étiquetés, maillon faible désigné.
    Dit la doctrine — une chaîne casse au maillon faible — sans aire de moyenne. Labels 14px non rognables."""
    band,susp,pf,badge,num=_fsc_derive(ev)
    BC={"marchand":"#9a9a9a","en_transition":"#a86a4a","sorti_du_marche":"#b08a3e",
        "autogere":"#3d7a4e","usage_decommodifie":"#2f6e8f","commun_vivant":"#224477"}
    col=BC[band]
    SYM={"oui":"#3d7a4e","partiel":"#b08a3e","non":"#b04a4a"}
    QS=[("milieu","Le milieu"),("vivant","Le vivant"),("ouverture","L'ouverture"),
        ("don","Le don"),("duree","La durée"),("voix","La voix")]
    y0=30; STEP=37; cx=30
    pfval=ev["questions"].get(pf,{}).get("valeur") if pf in ev["questions"] else None
    weak_lab="suspend la note" if (susp and pfval in ("non_etabli","projete")) else "maillon faible"
    bg=""; body=""
    for i,(k,lab) in enumerate(QS):
        cy=y0+i*STEP; val=ev["questions"][k]["valeur"]; weak=(k==pf)
        if weak:
            bg=f'<rect x="6" y="{cy-15}" width="288" height="30" rx="6" fill="{col}" opacity="0.10"/>'
        if val=="oui":
            g=f'<circle cx="{cx}" cy="{cy}" r="9" fill="{SYM["oui"]}"/>'
        elif val=="partiel":
            g=(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#fcfbf8" stroke="{SYM["partiel"]}" stroke-width="1.5"/>'
               f'<path d="M{cx} {cy-9} A9 9 0 0 1 {cx} {cy+9} Z" fill="{SYM["partiel"]}"/>')
        elif val=="non":
            g=f'<circle cx="{cx}" cy="{cy}" r="9" fill="#fcfbf8" stroke="{SYM["non"]}" stroke-width="2"/>'
        else:
            g=(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#fcfbf8" stroke="#9a9a9a" stroke-width="1.5"/>'
               f'<text x="{cx}" y="{cy+3}" text-anchor="middle" font-size="9" fill="#9a9a9a">n.é.</text>')
        tag=(f' <tspan fill="{col}" font-size="11" font-weight="bold">· {weak_lab}</tspan>') if weak else ""
        fw=' font-weight="bold"' if weak else ""
        body+=g+f'<text x="50" y="{cy+5}" font-size="14" fill="#221f1a"{fw}>{e(lab)}{tag}</text>'
    H=y0+5*STEP+22
    line=f'<line x1="{cx}" y1="{y0-2}" x2="{cx}" y2="{y0+5*STEP+2}" stroke="#e3ded2" stroke-width="2"/>'
    aria=f"Le faisceau libéré, lu au maillon faible : {PF_LABEL.get(pf,pf)}"
    return (f'<svg class="v3-chaine" viewBox="0 0 300 {H}" role="img" aria-label="{e(aria)}" '
            f'style="width:100%;max-width:300px;height:auto;font-family:Georgia,serif">'
            f'{bg}{line}{body}</svg>')

def bands_legend():
    _b=[("marchand","#9a9a9a"),("transition","#a86a4a"),("sorti du marché","#b08a3e"),("autogéré","#3d7a4e"),("usage libéré","#2f6e8f"),("commun vivant","#224477")]
    return '<p class="paliers-legend cat-legend">'+"".join(f'<span class="pal-chip" style="--pal:{c}">{l}</span>' for l,c in _b)+'</p>'
FB_HEX={"marchand":"#9a9a9a","en_transition":"#a86a4a","sorti_du_marche":"#b08a3e",
        "autogere":"#3d7a4e","usage_decommodifie":"#2f6e8f","commun_vivant":"#224477"}
def lieu_v3(f):
    """Profil v3.1 réutilisable d'un lieu (bande, couleur, libellé, note) — None si pas d'evaluation."""
    ev=f.get("evaluation")
    if not ev: return None
    band,susp,pf,badge,num=_fsc_derive(ev)
    return {"band":band,"bcol":FB_HEX[band],"label":FB_LABEL[band],
            "note":(None if susp else num),"susp":susp,"badge":badge,"pf":pf}

def _member_lieu_uids(f, by_uid):
    """Lieux rattachés à un maillon-groupe : via `membres` (réseau) ou la chaîne (porteur/usufruitier).
    Un membre porteur/usufruitier est étendu à ses propres lieux."""
    seed = list(f.get("membres") or []) or list(chained_uids(f, by_uid))
    lieux=set()
    for u in seed:
        g=by_uid.get(u)
        if not g: continue
        if g.get("categorie")=="lieu": lieux.add(u)
        elif g.get("categorie") in ("porteur","usufruitier"):
            for v in chained_uids(g, by_uid):
                if (by_uid.get(v) or {}).get("categorie")=="lieu": lieux.add(v)
    return list(lieux)

def porteur_eval(f, by_uid):
    """Synthèse six-questions d'un maillon-groupe, AGRÉGÉE sur ses lieux (son travail de libération)."""
    uids=_member_lieu_uids(f, by_uid)
    evs=[by_uid[u]["evaluation"] for u in uids if (by_uid.get(u) or {}).get("evaluation")]
    if not evs: return None
    S={"oui":1.0,"partiel":0.5,"non":0.0}
    QK=["milieu","vivant","ouverture","don","duree","voix"]
    MA={"milieu":"lieu","vivant":"lieu","ouverture":"chaine","don":"chaine","duree":"usage","voix":"usage"}
    def agg(getter):
        vals=[S[getter(ev)] for ev in evs if getter(ev) in S]
        if not vals: return "non_etabli"
        m=sum(vals)/len(vals)
        return "oui" if m>=0.84 else ("non" if m<=0.16 else "partiel")
    porte=agg(lambda ev: ev["porte"]["valeur"])
    qs={}
    for k in QK:
        d={"valeur":agg(lambda ev,k=k: ev["questions"][k]["valeur"]),"maillon":MA[k],
           "note":f"Agrégé sur {len(evs)} lieu·x porté·s."}
        if k in ("duree","voix"): d["decisive"]=True
        qs[k]=d
    return {"porte":{"valeur":porte,"cran":"pour_toujours","voie":"nature_porteur",
            "note":f"Synthèse sur {len(evs)} lieu·x."},"questions":qs,"_n":len(evs)}

def porteur_porte_context(f):
    """Démarche/modèle du porteur : type de portage (solidité de SA porte), en contexte de l'éval agrégée."""
    G={e["critere"]:e.get("valeur") for e in (f.get("grille") or [])}
    S={"oui":1.0,"partiel":0.5,"non":0.0}
    def lv(cs):
        v=[S[G[c]] for c in cs if c in G and G[c] in S]; return min(v) if v else None
    inal=lv(["inalienabilite"]); cap=lv(["non_lucrativite_effective","independance_rendement"])
    core=[x for x in (inal,cap) if x is not None]
    allv=[lv([c]) for c in ["inalienabilite","parts_non_cessibles","nature_protectrice","clause_devolution"]]+[cap]
    estab=[x for x in allv if x is not None]
    if core and min(core)==0.0: lab="pseudo-portage"
    elif estab and min(estab)==1.0: lab="verrou pour toujours"
    elif estab and min(estab)>=0.5: lab="portage solide"
    elif estab: lab="portage partiel"
    else: lab="à établir"
    return {"label":lab}

def _member_lieux(f, by_uid, heading, lead):
    uids=_member_lieu_uids(f, by_uid)
    items=[]
    for u in sorted(uids):
        g=by_uid.get(u)
        if not g or g.get("categorie")!="lieu": continue
        v=lieu_v3(g)
        if not v: continue
        note=("suspendue" if v["susp"] else f'{v["note"]}/100')
        items.append(f'<a class="pl-item" href="../l/{e(u)}.html" style="border-left:4px solid {v["bcol"]}">'
                     f'<span class="pl-nom">{e(g.get("nom",u))}</span>'
                     f'<span class="pl-band" style="color:{v["bcol"]}">{e(v["label"])} · {note}</span></a>')
    if not items: return ""
    return (f'<section class="porteur-lieux"><h2 class="sec">{e(heading)}</h2>'
      f'<p class="lead">{e(lead)}</p>'
      '<style>.pl-item{display:flex;justify-content:space-between;gap:10px;padding:8px 12px;margin:6px 0;background:#fcfbf8;border:1px solid #e3ded2;border-radius:6px;text-decoration:none;color:#221f1a}.pl-band{font-size:.85rem;font-weight:600;white-space:nowrap}</style>'
      '<div>'+''.join(items)+'</div></section>')

def fiche_v3(f, by_uid):
    """Profil v3.1 (note, bande, couleur, libellé, scores par question) de n'importe quelle entité."""
    cat=f.get("categorie")
    if cat=="lieu":
        ev=f.get("evaluation")
        if not ev: return None
    elif cat in ("porteur","usufruitier","reseau"):
        ev=porteur_eval(f, by_uid)
        if not ev: return None
    else:
        return None
    band,susp,pf,badge,num=_fsc_derive(ev)
    return {"band":band,"bcol":FB_HEX[band],"label":FB_LABEL[band],
            "note":(None if susp else num),"susp":susp,"pf":pf,"badge":badge,
            "qscores":_q_scores_from_ev(ev)}

def band_chip(f, by_uid):
    """Petite puce de palier v3.1 (remplace l'ancien badge de verdict v2)."""
    v=fiche_v3(f, by_uid)
    if not v: return ""
    return f'<span class="pal-chip" style="--pal:{v["bcol"]}">{e(v["label"])}</span>'
def render_faisceau(fiches, cfg, project=None):
    project = project or cfg["concepts"]["project"]
    body = """<h1>Le faisceau libéré</h1>
<p class="lead">La nouvelle grille de lecture — une porte, six questions, une échelle lue au
point le plus faible — n'est plus une page à part : elle est désormais la grille de
<strong>tout l'annuaire</strong>.</p>
<p class="prose">Chaque lieu, porteur, usufruitier et réseau est lu selon ce cadre ; chaque
fiche porte son <strong>étoile à six branches</strong>, sa <strong>note de libération</strong>
et son <strong>point faible</strong>, et le badge écologique « Sanctuaire » se lit à côté de la
note, jamais dedans.</p>
<ul class="prose">
  <li><a href="methode.html">La méthode en détail</a> — la porte, les six questions, l'échelle, la suspension.</li>
  <li><a href="classement.html">Le classement</a> — toutes les entrées notées sur la même échelle.</li>
  <li><a href="carte.html">La carte</a> — les lieux colorés par palier de libération.</li>
</ul>
<p class="prose note">Le cadre est daté, signé, contestable ; chaque chiffre est calculé,
jamais saisi. <a href="suggerer.html">Nous écrire / droit de réponse →</a></p>"""
    return page("Le faisceau libéré", body, "methode.html", depth=0,
                project=project, description="Le faisceau libéré — la grille de libération des terres, désormais appliquée à tout l'annuaire.",
                path="faisceau.html", link_gloss=False)


def render_comms_pages(cfg):
    """Pages d'accompagnement public (réserve @lumen #3) : ce que la note ne dit pas,
    FAQ, exemples calculés, droit de réponse. HTML autonome (aucune dépendance markdown)."""
    project = cfg["concepts"]["project"]
    pages = []

    # 1 — Ce que la note ne dit pas
    b1 = """<h1>Ce que la note ne dit pas</h1>
<p class="lead"><em>Une note tient sur un axe. Pour qu'elle serve sans tromper, il faut dire
franchement tout ce qu'elle <strong>ne</strong> mesure pas.</em></p>
<p class="prose"><strong>Elle ne dit pas si le lieu est réussi.</strong> Beau, accueillant, vivant,
bien tenu au quotidien, utile à son territoire : rien de tout cela n'entre dans la note de libération.
Un lieu admirable peut être à mi-chemin de la sortie du marché.</p>
<p class="prose"><strong>Elle ne dit pas si le lieu est écologique.</strong> Ça, c'est le badge
« Sanctuaire » 🌿, affiché <em>à côté</em> — exprès. Un lieu peut être un sanctuaire du vivant
<strong>et</strong> avoir une note de libération basse (son usage n'est pas encore rendu) ; ou être très
libéré <strong>sans</strong> badge (en ville, rien à agir pour le non-humain).</p>
<p class="prose"><strong>Elle ne dit pas si le lieu est viable économiquement.</strong> La fragilité
financière — pouvoir ne pas survivre — est un drapeau à part, jamais un point qui pénalise. On ne note
pas la pauvreté.</p>
<p class="prose"><strong>Elle ne classe pas des personnes.</strong> Elle situe un montage juridique.
Derrière une note basse il n'y a pas des gens « moins bien » : il y a une architecture de droits qui
n'a pas (encore) franchi telle marche.</p>
<p class="prose"><strong>Elle ne compare pas les lieux en valeur.</strong> Deux lieux à la même note
peuvent être deux réussites différentes — un commun de conservation et un commun habité ne se ressemblent
pas. La note <em>situe</em> sur une échelle commune ; le profil et le point faible nommé disent le reste.</p>
<p class="prose"><strong>Elle ne prétend pas être neutre.</strong> C'est une lecture argumentée selon un
parti pris assumé (économie citoyenne, non lucrative, du vivant), avec des seuils datés et contestables
— pas une mesure de laboratoire.</p>
<p class="prose"><strong>Et quand elle ne sait pas, elle le dit.</strong> Un point non documenté reste
« non établi », jamais comblé à votre désavantage ; si un point décisif manque, la note est
<strong>suspendue</strong> plutôt que devinée.</p>
<blockquote class="prose"><p>En une phrase : <strong>on note un degré de sortie du marché, pas un
lieu.</strong></p></blockquote>
<p class="prose backlink"><a href="methode.html">← La méthode</a> · <a href="faq.html">Questions
fréquentes</a> · <a href="exemples.html">Trois exemples calculés</a></p>"""
    pages.append(("ce-que-la-note-ne-dit-pas.html", "Ce que la note ne dit pas", b1,
                  "Les limites assumées de la note de libération : ce qu'elle ne mesure pas."))

    # 2 — FAQ
    _faq = [
        ("« Que mesure exactement votre note ? »",
         "Une seule chose, nommée : <em>à quel point une terre est sortie du marché et rendue à celles et ceux qui l'usent.</em> C'est une coordonnée sur un axe — la libération — pas un jugement de valeur du lieu."),
        ("« Pourquoi un lieu que j'aime a-t-il une note basse ? »",
         "Parce que la note ne juge pas le lieu, mais <em>le degré de sortie du marché et de retour aux usagers</em>. Un lieu précieux, beau, utile, peut être à mi-chemin sur cet axe — et porter par ailleurs le badge « Sanctuaire », ou être un modèle de conservation. La note basse dit « le chemin n'est pas fini », pas « ce lieu vaut peu »."),
        ("« Pourquoi un grand jardin protégé (le Conservatoire…) n'est-il pas tout en haut ? »",
         "Parce qu'il protège la terre sans (encore) en rendre l'usage à un collectif autogéré. C'est une autre réussite, que nous signalons par le badge écologique « Sanctuaire », pas par la note de libération. Les deux s'affichent côte à côte exprès."),
        ("« Vous comparez des lieux qui n'ont rien à voir — est-ce juste ? »",
         "On ne dresse pas un palmarès qui dit « ce lieu est meilleur que celui-là ». On situe chaque montage sur une même échelle de libération, avec son profil et son point faible nommé. Deux lieux à la même note peuvent être deux réussites différentes ; la note les situe, elle ne les classe pas en valeur."),
        ("« La note est-elle objective ? »",
         "Non, et nous l'assumons. C'est une lecture argumentée selon un cadre explicite — une économie citoyenne, non lucrative, attentive au vivant — pas une mesure neutre. Les seuils sont datés, signés, contestables, et nous appelons la critique (voir la <a href=\"methode.html\">note de méthode</a>)."),
        ("« Pourquoi certains lieux n'ont-ils pas de note du tout ? »",
         "Parce qu'un point décisif (la sortie du marché, la durée d'usage, ou qui décide) est resté non établi — non documenté de notre côté. Dans ce cas nous suspendons la note plutôt que de deviner : nous affichons le palier atteint avec certitude et signalons le reste comme « non établi (en cours d'évaluation) ». Ce n'est pas un mauvais score — c'est un manque de pièces, jamais retenu à votre désavantage."),
        ("« Vous risquez de décourager des porteurs de bonne foi. »",
         "Notre but est l'inverse : montrer <em>où</em> le chemin de libération se poursuit, pas distribuer des mauvaises notes. Le point faible nommé est une indication de progression, pas une sanction ; et le badge honore ce qui est déjà accompli pour le vivant."),
        ("« De quel droit notez-vous notre lieu sans nous demander ? »",
         "Nous évaluons des montages juridiques et des faits publics — comment une terre est tenue en droit — pas des personnes ni des vies privées, à partir des informations publiquement disponibles. C'est une lecture documentaire, faillible, qui ne prétend pas détenir une vérité ; sa contrepartie est ferme : contact <strong>avant</strong> publication d'une fiche nommée, <a href=\"droit-de-reponse.html\">droit de réponse</a> sans retouche, et tout « non établi » levable sur pièce ou témoignage."),
        ("« Qui produit ces évaluations — une IA ? »",
         "Une lecture humaine, assumée et signée, aidée d'outils d'analyse (dont l'IA). La grille et chaque fiche engagent une responsabilité éditoriale nommée, pas un algorithme anonyme."),
        ("« Et si vous vous trompez sur notre lieu ? »",
         "Écrivez-nous : vous avez un <a href=\"droit-de-reponse.html\">droit de réponse</a>. On corrige tout fait prouvé, on lève un « non établi » sur pièce ou sur témoignage, et votre réponse libre est reproduite sans retouche, en tête de la fiche. Avant toute publication d'une fiche nommée, le lieu est contacté d'abord."),
        ("« Vos seuils peuvent-ils changer ? »",
         "Oui. Ce sont une convention publique datée (2026), révisable ; tout amendement argumenté est versé au <a href=\"changelog.html\">journal des versions</a>. La grille évolue au grand jour, pas en douce."),
    ]
    b2 = '<h1>Questions fréquentes sur la note</h1>\n<p class="lead">On note un degré de sortie du marché, pas un lieu. Voici les questions qui reviennent — et nos réponses, fermes et faillibles.</p>\n'
    b2 += "".join(f'<section class="faq-q"><h3>{q}</h3><p class="prose">{a}</p></section>\n' for q, a in _faq)
    b2 += '<p class="prose backlink"><a href="methode.html">← La méthode</a> · <a href="ce-que-la-note-ne-dit-pas.html">Ce que la note ne dit pas</a> · <a href="droit-de-reponse.html">Droit de réponse</a></p>'
    pages.append(("faq.html", "Questions fréquentes", b2,
                  "Questions fréquentes sur la note de libération."))

    # 3 — Exemples calculés
    def _qrow(q, sym, why):
        return f'<tr><td>{q}</td><td class="num">{sym}</td><td>{why}</td></tr>'
    t1 = "".join([
        _qrow("Le milieu", "○", "Immeuble urbain ; rien d'agi sur le sol / l'eau."),
        _qrow("Le vivant", "○", "Rien d'aménagé pour le non-humain."),
        _qrow("L'ouverture", "◐", "Coopérative ouverte sur le quartier, mais d'abord pour ses habitants."),
        _qrow("Le don", "◐", "<strong>Point faible.</strong> L'accès reste une redevance ; le logement n'est pas « donné »."),
        _qrow("La durée", "●", "Les habitants peuvent rester (bail coopératif stable)."),
        _qrow("La voix", "●", "Une voix par personne ; ils décident vraiment."),
    ])
    t2 = "".join([
        _qrow("Le milieu", "●", "Remarquablement préservé (jardin de conservation)."),
        _qrow("Le vivant", "●", "Biodiversité protégée, gestion écologique attestée."),
        _qrow("L'ouverture", "●", "Lieu ouvert au public, vocation pédagogique."),
        _qrow("Le don", "○", "L'accès est payant (billet d'entrée)."),
        _qrow("La durée", "◐", "Personnel et gestionnaires, pas une communauté d'usagers qui « reste »."),
        _qrow("La voix", "○", "<strong>Point faible.</strong> Géré d'en haut (établissement), pas par ses usagers."),
    ])
    t3 = "".join([
        _qrow("Le milieu", "●", "Obligation Réelle Environnementale signée fin 2024."),
        _qrow("Le vivant", "●", "Démarche Oasis de Biodiversité ; place effective au vivant."),
        _qrow("L'ouverture", "●", "Écolieu intergénérationnel ouvert, à vocation d'intérêt général."),
        _qrow("Le don", "?", "Régime d'accès et d'usage non documenté par nos sources."),
        _qrow("La durée", "?", "<strong>Décisive.</strong> La nature et la durée du titre d'usage ne sont pas attestées."),
        _qrow("La voix", "●", "<strong>Décisive.</strong> Collectif intergénérationnel autogéré ; gouvernance réelle."),
    ])
    _thead = '<thead><tr><th>Question</th><th class="num"></th><th>Pourquoi</th></tr></thead>'
    b3 = f"""<h1>Comment on arrive à une note — trois exemples, pas à pas</h1>
<p class="lead"><em>On ne demande pas de nous croire sur parole. Voici, déroulée, la lecture de trois lieux
très différents. À chaque fois la même marche : la porte (sortir du marché ? sinon, rien ne commence),
puis six questions du lieu vers le groupe, puis on se place sur l'échelle au point le plus faible, et on
dit ce qu'on n'a pas pu vérifier.</em></p>
<blockquote class="prose"><p>marchand (0-20) → sorti du marché (20-50) → autogéré (50-75) → usage libéré
(75-90) → commun vivant (90-100)</p></blockquote>
<p class="prose">Et le badge « Sanctuaire » 🌿 (l'écologie) est à côté de la note, jamais dedans.</p>
<h2 class="sec">Exemple 1 — un lieu haut : Le Village Vertical <span class="enclair">(coopérative d'habitants, Villeurbanne)</span></h2>
<p class="prose"><strong>La porte — franchie.</strong> Les parts sont au nominal, sans plus-value à la
revente ; personne ne capte la valeur du bâti. → <em>on entre sur l'échelle.</em></p>
<table class="rank-tbl small">{_thead}<tbody>{t1}</tbody></table>
<p class="prose"><strong>On se place.</strong> Porte ● + voix ● + durée ● → palier <strong>autogéré</strong>
(50-75). Le don n'est que ◐ → on ne franchit pas <em>usage libéré</em>. Le milieu ○ et le vivant ○ ne
situent pas dans le palier : ils ne font que fermer le badge. La position suit la plus faible des
questions du chemin — ici le don (◐). → <strong>Libération 60-66 · commun autogéré · pas de badge.</strong>
Point faible : le don. <em>Un lieu où l'on décide et où l'on reste, mais où habiter se paie encore.</em></p>
<h2 class="sec">Exemple 2 — l'écologie n'est pas la note : Le Domaine du Rayol <span class="enclair">(Conservatoire du littoral)</span></h2>
<p class="prose"><strong>La porte — franchie, pour toujours.</strong> Domaine public inaliénable : la
valeur est soustraite à toute revente, définitivement. → <em>on entre sur l'échelle.</em></p>
<table class="rank-tbl small">{_thead}<tbody>{t2}</tbody></table>
<p class="prose"><strong>On se place.</strong> Porte ● mais la voix est ○ : l'usage n'est pas rendu à un
collectif. On reste au palier <strong>sorti du marché</strong> (20-50). → <strong>Libération ≈ 45 · commun
institué · 🌿🌿 Sanctuaire.</strong> Point faible : la voix. <em>Le lieu est écologiquement exemplaire — d'où
le badge fort — et sa note de libération est basse, parce que l'usage n'est pas encore rendu. Les deux
informations cohabitent ; aucune n'efface l'autre.</em></p>
<h2 class="sec">Exemple 3 — quand on ne sait pas : on suspend, on n'invente pas <span class="enclair">(cas type : L'Aube)</span></h2>
<p class="prose"><strong>La porte — franchie.</strong> Donation à un fonds de dotation : la valeur est
soustraite au marché. → <em>on entre sur l'échelle.</em></p>
<table class="rank-tbl small">{_thead}<tbody>{t3}</tbody></table>
<p class="prose"><strong>On se place — et on s'arrête.</strong> La durée (le titre d'usage) est une question
décisive, et elle est non établie. La règle : on ne devine pas une décisive. → la note est
<strong>suspendue</strong>. On affiche seulement le palier atteint avec certitude (sorti du marché) et on
marque les « ? » comme une dette datée. → <strong>Type : sorti du marché — sommet non attesté · note
suspendue · 🌿🌿 Sanctuaire.</strong></p>
<blockquote class="prose"><p><strong>La suspension est une honnêteté, pas une faiblesse.</strong> Mieux
vaut dire « nous n'avons pas la pièce » que prêter une note que les sources ne fondent pas — appliqué sans
exception, au plus connu comme au plus discret.</p></blockquote>
<p class="prose"><em>Les chiffres ci-dessus sont des illustrations de méthode ; chaque fiche réelle est
calculée et sourcée pièce par pièce, et ouverte au <a href="droit-de-reponse.html">droit de réponse</a>.</em></p>
<p class="prose backlink"><a href="methode.html">← La méthode</a> · <a href="ce-que-la-note-ne-dit-pas.html">Ce que la note ne dit pas</a></p>"""
    pages.append(("exemples.html", "Trois exemples calculés", b3,
                  "Trois exemples déroulés pas à pas : comment on arrive à une note de libération."))

    # 4 — Droit de réponse
    b4 = """<h1>Droit de réponse</h1>
<p class="lead"><em>Nous évaluons des montages juridiques, sur des faits publics, selon un cadre explicite.
Nous pouvons nous tromper, ou manquer une pièce. Cette page vous donne les moyens de corriger, compléter
ou répondre — et nous engage sur la manière dont nous traitons votre demande.</em></p>
<h2 class="sec">Avant toute publication d'une fiche nommée</h2>
<p class="prose"><strong>Tout lieu nommé est contacté avant la mise en ligne de sa fiche</strong> — pas
seulement ceux dont l'évaluation évolue à la baisse. Vous disposez d'un délai pour répondre, corriger ou
compléter <strong>avant</strong> publication ; la fiche n'est pas mise en ligne pendant cette fenêtre.
<em>(Nous ne parlons pas de « classe » ni de « niveau » : une évaluation qui change est une lecture qui
s'affine sur pièces, pas un bulletin.)</em></p>
<h2 class="sec">Ce que vous pouvez demander</h2>
<ol class="prose">
<li><strong>La correction d'un fait.</strong> Apportez la preuve (statuts, bail, acte, délibération…) :
nous rectifions et datons la correction, visible dans l'historique de la fiche.</li>
<li><strong>L'ajout d'une pièce qui lève un « non établi ».</strong> Un point que nos sources ne
documentaient pas peut être attesté par écrit <em>ou</em> par témoignage / visite — pour ne pas pénaliser
les lieux discrets, qui ne communiquent pas mais existent. La case passe de « non établi » à sa valeur
réelle.</li>
<li><strong>Une réponse libre.</strong> Jusqu'à un format court, reproduite sans retouche, en tête de
votre fiche — que vous soyez d'accord ou non avec notre lecture. <em>(Seule réserve : nous ne pouvons pas
mettre en ligne un contenu manifestement illégal ; nous vous le signalerions pour reformulation.)</em></li>
</ol>
<h2 class="sec">Ce que nous ne ferons pas</h2>
<ul class="prose">
<li>Retirer une évaluation fondée sur des faits publics au seul motif qu'elle déplaît (mais votre réponse
libre est toujours affichée à côté).</li>
<li>Modifier une note sans pièce : un désaccord d'appréciation se discute, un fait se prouve.</li>
<li>Réécrire votre réponse : elle paraît telle quelle.</li>
</ul>
<h2 class="sec">Comment nous écrire</h2>
<p class="prose">Indiquez : le <strong>lieu concerné</strong>, le <strong>point visé</strong> (la porte,
l'une des six questions, le badge, ou un fait descriptif), <strong>ce que vous demandez</strong>
(correction / ajout de pièce / réponse libre), et la <strong>pièce ou le témoignage</strong> s'il y en a
un. → <a href="mailto:cedric.mabilotte@gmail.com?subject=Droit%20de%20r%C3%A9ponse%20Terres%20Lib%C3%A9r%C3%A9es">cedric.mabilotte@gmail.com</a> — un·e responsable éditorial·e traite chaque demande.</p>
<h2 class="sec">Notre engagement de délai</h2>
<p class="prose">Accusé de réception sous quelques jours ouvrés ; instruction d'une correction factuelle
prouvée <strong>avant</strong> toute (re)publication de la fiche concernée ; réponse libre mise en ligne
rapidement après vérification (légalité uniquement, pas le fond).</p>
<p class="prose backlink"><a href="methode.html">← La méthode</a> · <a href="faq.html">Questions fréquentes</a></p>"""
    pages.append(("droit-de-reponse.html", "Droit de réponse", b4,
                  "Droit de réponse : corriger un fait, lever un « non établi », répondre sans retouche."))

    out = []
    for fname, title, body, desc in pages:
        out.append((fname, page(title, body, "methode.html", depth=0, project=project,
                                 description=desc, path=fname)))
    return out

def main():
    global BASE_URL
    cfg = load_config()
    # URL canonique centralisée depuis concepts.yml
    cfg_url = (cfg["concepts"].get("project", {}) or {}).get("url")
    if cfg_url:
        BASE_URL = cfg_url.rstrip("/")
    fiches = load_fiches()
    doublons = verifier_uids(fiches)
    if doublons:
        print(f"ÉCHEC — {len(doublons)} uid en doublon (un uid = une fiche) :")
        for d in doublons:
            print(f"  {d}")
        raise SystemExit(1)
    gidx = grille_index(cfg["grilles"])
    ranking = cfg["ranking"]

    all_sc = []
    by_uid = {}
    for f in fiches:
        sc = score_fiche(f, gidx, ranking)
        all_sc.append((f, sc))
        by_uid[f["uid"]] = f

    # contexte de chaîne — étiquettes grisées porteur / réseau (session #4, UI)
    compute_chain_context(fiches, by_uid)

    # chaîne / Option A : relit l'indice des porteurs et usufruitiers à
    # travers leurs lieux reliés (indice intrinsèque → indice effectif).
    # À faire après le scoring de TOUTES les fiches (besoin des axes des lieux).
    apply_chaine(all_sc, by_uid, ranking)


    # session #5 — plafond ax2 sur les LIEUX selon le pire nature_interet de la
    # chaîne. Doit précéder apply_palier_verdict_constraint (qui relit l'IdL).
    apply_lieu_plafond_chaine(all_sc, by_uid, ranking)

    # session #5 — paliers contraints par verdict (« libération aboutie »
    # réservée aux lieux verdict==sanctuaire).
    apply_palier_verdict_constraint(all_sc, by_uid, ranking)

    # contrôle de cohérence des chaînes (chantier A) — avertit, ne bloque pas.
    verifier_chaines(fiches)
    # contrôle de cohérence pôle↔verdict (#11) — avertit, ne bloque pas.
    verifier_poles(fiches, by_uid)
    # --- bascule v3.1 (APRÈS toutes les passes v2 : chaine, plafond, contrainte verdict) ---
    for _f, _s in all_sc:
        if _f.get("categorie") == "modele":
            # modèle voisin : descriptif, sans note de libération (doctrine)
            _s["idl_v2"] = _s.get("idl"); _s["palier_v2"] = _s.get("palier")
            _s["idl"] = None; _s["palier"] = None
            continue
        _v = fiche_v3(_f, by_uid)
        if not _v:
            # groupe sans lieu agrégeable → non noté en v3 (n'hérite pas d'un score v2)
            if _f.get("categorie") in ("porteur", "usufruitier", "reseau"):
                _s["idl_v2"] = _s.get("idl")
                _s["palier_v2"] = _s.get("palier")
                _s["idl"] = None
                _s["palier"] = None
            continue
        _s["idl_v2"] = _s.get("idl")
        _s["palier_v2"] = _s.get("palier")
        _s["idl"] = _v["note"]                      # None si suspendue
        _s["palier"] = {"id": _v["band"], "label": _v["label"], "couleur": _v["bcol"]}
        _s["susp_v3"] = _v["susp"]
        _s["q6"] = _v.get("qscores")
        _s["score_type"] = "vrai"

    sc_by_uid = {f["uid"]: sc for f, sc in all_sc}

    # nettoyage du site
    if SITE.exists():
        for child in SITE.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            elif child.name != "CNAME":
                child.unlink()
    SITE.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    write(ASSETS / "style.css", CSS)
    write(ASSETS / "list.js", LIST_JS)
    # compare.js : on injecte les cinq axes (id, libellé, couleur) lus depuis
    # ranking.yml — aucun axe codé en dur dans le JavaScript.
    axes_js = json.dumps([[a, l, c] for a, l, c in Q6_AXES], ensure_ascii=False)
    write(ASSETS / "compare.js", COMPARE_JS.replace("__AXES__", axes_js))
    write(ASSETS / "favicon.svg", FAVICON_SVG)
    write(ASSETS / "og-default.svg", OG_SVG)
    write(SITE / "favicon.svg", FAVICON_SVG)
    # CSS additionnel — pages /revues/* (typographie de lecture longue).
    write(ASSETS / "style-revue.css", CSS_REVUE)

    n_by_cat = {c: sum(1 for f in fiches if f["categorie"] == c)
                for c in ("lieu", "porteur", "usufruitier", "modele", "reseau")}

    # Dossiers (magazine) — chargés avant les fiches pour le lien retour fiche↔dossier
    dossiers = load_dossiers()
    cfg["_dossier_for"] = dossier_map(dossiers)

    # fiches individuelles
    for f, sc in all_sc:
        cat = f["categorie"]
        if cat == "reseau":
            html_doc = render_reseau(f, cfg, by_uid, sc_by_uid)
        else:
            html_doc = render_fiche(f, sc, cfg, by_uid, sc_by_uid)
        write(SITE / CAT_SLUG[cat] / f'{f["uid"]}.html', html_doc)

    # catalogues
    for cat in ("lieu", "porteur", "usufruitier", "modele"):
        subset = [(f, sc) for f, sc in all_sc if f["categorie"] == cat]
        write(SITE / CAT_PAGE[cat], render_catalogue(cat, subset, cfg))
    write(SITE / "reseaux.html", render_reseaux(
        [(f, sc) for f, sc in all_sc if f["categorie"] == "reseau"], cfg))

    # pages transverses
    write(SITE / "index.html", render_index(all_sc, cfg, n_by_cat))
    write(SITE / "classement.html", render_classement(all_sc, cfg))
    write(SITE / "carte.html", render_carte(all_sc, cfg, by_uid))
    write(SITE / "regimes.html", render_regimes(cfg))
    write(SITE / "grilles.html", render_grilles(cfg))
    write(SITE / "glossaire.html", render_glossaire(cfg))
    write(SITE / "methode.html", render_methode(cfg, n_by_cat, all_sc))
    for _cfn, _chtml in render_comms_pages(cfg):
        write(SITE / _cfn, _chtml)
    write(SITE / "faisceau.html", render_faisceau(fiches, cfg, project=None))
    write(SITE / "themes.html", render_themes(all_sc, cfg))
    write(SITE / "comparer.html", render_comparer(all_sc, cfg))
    write(SITE / "suggerer.html", render_suggerer(cfg))
    write(SITE / "changelog.html", render_changelog(cfg))
    write(SITE / "404.html", render_404(cfg))

    # Revues — pensée publique éditoriale (session #7)
    revues = load_revues()
    verifier_revues(revues)
    if revues:
        write(SITE / "revues" / "index.html",
              render_revues_index(revues, cfg))
        for r in revues:
            rslug = r["meta"].get("slug", r["_dir"])
            write(SITE / "revues" / rslug / "index.html",
                  render_revue(r, r["articles"], cfg))
            for art in r["articles"]:
                art_slug = _article_url_part(art)
                write(SITE / "revues" / rslug / art_slug / "index.html",
                      render_article(r, art, cfg))
            # PDF — dès le premier article publié (session #8)
            if len(r["articles"]) >= 1:
                build_revue_pdf(r, r["articles"], cfg)
        print(f"Revues : {len(revues)} revue(s) générée(s), "
              f"{sum(len(r['articles']) for r in revues)} article(s).")

    # Dossiers — le magazine (récits de cas-pivot)
    if dossiers:
        write(SITE / "dossiers" / "index.html",
              render_dossiers_index(dossiers, cfg, sc_by_uid, by_uid))
        for d in dossiers:
            write(SITE / "dossiers" / f'{d["meta"].get("slug")}.html',
                  render_dossier(d, cfg, by_uid, sc_by_uid))
        print(f"Dossiers : {len(dossiers)} dossier(s) généré(s).")

    # CNAME — domaine personnalisé GitHub Pages
    write(SITE / "CNAME", BASE_URL.split("//")[-1] + "\n")

    # robots.txt + sitemap.xml
    sitemap_paths = [("index.html", "1.0")]
    for cat in ("lieu", "porteur", "usufruitier", "modele", "reseau"):
        sitemap_paths.append((CAT_PAGE[cat], "0.8"))
    for p in ("classement.html", "carte.html", "regimes.html",
              "grilles.html", "methode.html", "themes.html", "comparer.html",
              "glossaire.html", "suggerer.html", "faisceau.html"):
        sitemap_paths.append((p, "0.6"))
    for f, sc in all_sc:
        sitemap_paths.append((f'{CAT_SLUG[f["categorie"]]}/{f["uid"]}.html', "0.7"))
    # dossiers — index + récits
    if dossiers:
        sitemap_paths.append(("dossiers/index.html", "0.7"))
        for d in dossiers:
            sitemap_paths.append((f'dossiers/{d["meta"].get("slug")}.html', "0.6"))
    # revues — index + manifestes + articles (PDF non listés dans le sitemap)
    if revues:
        sitemap_paths.append(("revues/index.html", "0.7"))
        for r in revues:
            rslug = r["meta"].get("slug", r["_dir"])
            sitemap_paths.append((f"revues/{rslug}/index.html", "0.6"))
            for art in r["articles"]:
                art_slug = _article_url_part(art)
                sitemap_paths.append(
                    (f"revues/{rslug}/{art_slug}/index.html", "0.5"))
    write(SITE / "robots.txt", build_robots())
    write(SITE / "sitemap.xml", build_sitemap(sitemap_paths))

    # data.json (export ouvert) — enrichi de champs descriptifs pour le
    # comparateur (sous-titre, forme juridique, type de montage, nature). Champs
    # ajoutés, aucun retiré : l'export reste rétro-compatible.
    data = []
    for f, sc in all_sc:
        if f["categorie"] == "reseau":
            continue  # un réseau n'est pas une entité notée : hors export data
        mont = f.get("montage", {}) or {}
        # intégrité du montage : nouvelle clé, repli sur l'ancienne.
        im = f.get("integrite_montage", {}) or f.get("purete_juridique", {}) or {}
        montage_id = mont.get("type", "") or ""
        im_niv = im.get("niveau", "") or ""
        im_lab = integrite_label(im_niv, ranking)[0] if im_niv else ""
        # axes exportés avec les clés entières 1..5 (sérialisées en chaînes).
        _v3e = fiche_v3(f, by_uid)
        data.append({"uid": f["uid"], "nom": f["nom"], "categorie": f["categorie"],
                      "sous_titre": clean(f.get("sous_titre", "")),
                      "idl": sc["idl"],
                      "suspendue": bool(_v3e["susp"]) if _v3e else None,
                      "point_faible": (PF_LABEL.get(_v3e["pf"], _v3e["pf"]) if _v3e else None),
                      "badge": (_v3e["badge"] if _v3e else None),
                      "score_type": sc.get("score_type"),
                      "completude": (round(sc["completude"], 3)
                                     if sc.get("completude") is not None else None),
                      "axes": (_v3e["qscores"] if _v3e else {}),
                      "palier": sc["palier"]["id"] if sc["palier"] else None,
                      "palier_label": (sc["palier"]["label"]
                                       if sc["palier"] else None),
                      "palier_couleur": (sc["palier"]["couleur"]
                                         if sc["palier"] else None),
                      "forme_juridique": clean(f.get("forme_juridique", "")),
                      "montage_type": montage_id,
                      "montage_label": (montage_label(montage_id, cfg["concepts"])
                                        if montage_id else ""),
                      "nature_juridique": im_lab})
    write(SITE / "data.json", json.dumps(data, ensure_ascii=False, indent=2))

    total = len(fiches)
    print(f"Site généré : {total} fiches, "
          f"{n_by_cat['lieu']} lieux / {n_by_cat['porteur']} porteurs / "
          f"{n_by_cat['usufruitier']} usufruitiers / {n_by_cat['reseau']} réseaux "
          f"/ {n_by_cat['modele']} modèles.")
    print(f"→ {SITE}")

    # garde-fou — aucune entité HTML ne doit avoir été cassée par la typographie
    fautes = verifier_entites_html()
    if fautes:
        print(f"ÉCHEC — {len(fautes)} entité(s) HTML malformée(s) détectée(s) :")
        for f in fautes[:20]:
            print(f"  {f}")
        raise SystemExit(1)
    print("Contrôle des entités HTML : aucune anomalie.")

    # garde-fou — tout lien interne relatif doit résoudre vers un fichier existant
    liens_casses = verifier_liens()
    if liens_casses:
        print(f"ÉCHEC — {len(liens_casses)} lien(s) interne(s) cassé(s) :")
        for l in liens_casses[:20]:
            print(f"  {l}")
        raise SystemExit(1)
    print("Contrôle des liens internes : aucun lien cassé.")


if __name__ == "__main__":
    main()
