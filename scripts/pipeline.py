#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pipeline.py — Pipeline à zones Z0–Z3 de la veille « Terres Libérées ».

Module compagnon de watch.py qui implémente la qualification progressive
des candidats à promouvoir en fiches, sans déclenchement manuel.

Zones :
 Z0 — Capture brute    : discovery/raw/[source]/YYYY-MM-DD.jsonl
                         (archive intégrale, un item JSON par ligne)
 Z1 — Candidats scorés : discovery/candidats-YYYY-MM-DD.{md,json}
                         + discovery/candidates-YYYY-MM-DD.jsonl
 Z2 — Leads agrégés    : discovery/leads/[slug].md
                         (fiche frontmatter YAML par lieu pressenti)
 Z3 — Pré-fiches       : discovery/prefiches/[slug].yml
                         (schéma 1bis partiellement rempli, à arbitrer)

La promotion Z3 → Z4 (vers lieux/) reste MANUELLE — ce module ne touche
jamais à lieux/, porteurs/, usufruitiers/, etc.

Critères et seuils sont documentés dans discovery/PIPELINE.md et exposés
ici comme constantes paramétrables.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
DISCOVERY = ROOT / "discovery"
RAW_DIR = DISCOVERY / "raw"
LEADS_DIR = DISCOVERY / "leads"
PREFICHES_DIR = DISCOVERY / "prefiches"

# ─────────────────────────────────────────────────────────────────────────────
# Seuils et critères de promotion — paramétrables
# ─────────────────────────────────────────────────────────────────────────────
#
# Z2 → Z3 (lead → pré-fiche) :
#   • au moins 2 des 3 indices structurels parmi (nom_propre, localisation,
#     entite_juridique) doivent être à True ;
#   • le score cumulé doit dépasser SEUIL_SCORE_PROMOTION.
# Le seuil de 25 correspond à environ 2-3 passes positives avec un score
# pondéré moyen de 10-12 (cf. discovery/candidats-2026-05-26.md). Il est
# volontairement franchissable pour ne pas étouffer les candidats prometteurs,
# mais hors d'atteinte pour un signal isolé peu structurant.

SEUIL_SCORE_PROMOTION = 25
NB_INDICES_REQUIS = 2  # parmi (nom_propre, localisation, entite_juridique)

# Convention frequence: par source. Si absente du YAML, valeur par défaut.
FREQUENCES_VALIDES = {"hebdomadaire", "mensuelle", "trimestrielle", "sur_demande"}
FREQUENCE_DEFAUT = "hebdomadaire"
JOURS_PAR_FREQUENCE = {
    "hebdomadaire": 7,
    "mensuelle": 30,
    "trimestrielle": 90,
    "sur_demande": None,  # ne scanne jamais automatiquement
}

# Mots-outils à retirer du slug (articles, prépositions courtes).
SLUG_STOP_WORDS = {"le", "la", "les", "l", "de", "du", "des", "d", "un", "une",
                   "et", "a", "au", "aux", "en", "sur", "sous", "pour", "par",
                   "the"}

# Formes juridiques détectables (préfixées par leur identifiant ID).
FORMES_JURIDIQUES = [
    ("fondation_reconnue", r"\bfondation\s+(reconnue\s+d'?utilit[ée]\s+publique|de\s+france)\b"),
    ("fondation", r"\bfondation\b"),
    ("fonds_dotation", r"\bfonds\s+de\s+dotation\b"),
    ("scic", r"\bscic\b"),
    ("scop", r"\bscop\b"),
    ("sci", r"\bsci\b(?!.{0,40}familiale)"),
    ("gfa", r"\bg\.?f\.?a\.?\b"),
    ("gaec", r"\bgaec\b"),
    ("earl", r"\bearl\b"),
    ("bail_emphyteotique", r"\bbail\s+emphyt[ée]otique\b"),
    ("bail_reel_solidaire", r"\bbail\s+r[ée]el\s+solidaire\b|\bbrs\b"),
    ("bail_rural", r"\bbail\s+rural\b"),
    ("cooperative_habitants", r"\bcoop[ée]rative\s+d'?habitants?\b"),
    ("societe_civile", r"\bsoci[ée]t[ée]\s+civile\b"),
    ("fonciere", r"\bfonci[èe]re\b"),
    ("association_1901", r"\bassociation\s+(?:loi\s+)?1901\b"),
    ("association", r"\bassociation\b"),
    ("collectivite", r"\b(commune|communaut[ée]\s+de\s+communes|m[ée]tropole|d[ée]partement|r[ée]gion|conservatoire\s+du\s+littoral)\b"),
]

# Départements français (numéro → nom court) — utilisé pour la détection de
# localisation. Liste réduite aux noms les plus discriminants.
DEPARTEMENTS_FR = [
    "Ain", "Aisne", "Allier", "Alpes-de-Haute-Provence", "Hautes-Alpes",
    "Alpes-Maritimes", "Ardèche", "Ardennes", "Ariège", "Aube", "Aude",
    "Aveyron", "Bouches-du-Rhône", "Calvados", "Cantal", "Charente",
    "Charente-Maritime", "Cher", "Corrèze", "Corse-du-Sud", "Haute-Corse",
    "Côte-d'Or", "Côtes-d'Armor", "Creuse", "Dordogne", "Doubs", "Drôme",
    "Eure", "Eure-et-Loir", "Finistère", "Gard", "Haute-Garonne", "Gers",
    "Gironde", "Hérault", "Ille-et-Vilaine", "Indre", "Indre-et-Loire",
    "Isère", "Jura", "Landes", "Loir-et-Cher", "Loire", "Haute-Loire",
    "Loire-Atlantique", "Loiret", "Lot", "Lot-et-Garonne", "Lozère",
    "Maine-et-Loire", "Manche", "Marne", "Haute-Marne", "Mayenne",
    "Meurthe-et-Moselle", "Meuse", "Morbihan", "Moselle", "Nièvre", "Nord",
    "Oise", "Orne", "Pas-de-Calais", "Puy-de-Dôme", "Pyrénées-Atlantiques",
    "Hautes-Pyrénées", "Pyrénées-Orientales", "Bas-Rhin", "Haut-Rhin",
    "Rhône", "Haute-Saône", "Saône-et-Loire", "Sarthe", "Savoie", "Haute-Savoie",
    "Paris", "Seine-Maritime", "Seine-et-Marne", "Yvelines", "Deux-Sèvres",
    "Somme", "Tarn", "Tarn-et-Garonne", "Var", "Vaucluse", "Vendée", "Vienne",
    "Haute-Vienne", "Vosges", "Yonne", "Territoire de Belfort", "Essonne",
    "Hauts-de-Seine", "Seine-Saint-Denis", "Val-de-Marne", "Val-d'Oise",
]

REGIONS_FR = [
    "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Bretagne",
    "Centre-Val de Loire", "Corse", "Grand Est", "Hauts-de-France",
    "Île-de-France", "Normandie", "Nouvelle-Aquitaine", "Occitanie",
    "Pays de la Loire", "Provence-Alpes-Côte d'Azur",
]

# Mots indicatifs d'un montage de libération — pour pré-remplir montage.type.
INDICES_MONTAGE_TYPE = [
    ("propriete_publique", r"\bbail\s+emphyt[ée]otique\b.*(état|commune|conservatoire|département|département|région)|\bdomanialit[ée]\b|\bpropri[ée]t[ée]\s+publique\b"),
    ("demembrement", r"\bnue[- ]propri[ée]t[ée]\b|\busufruit\b|\bd[ée]membrement\b"),
    ("propriete_collective", r"\bcoop[ée]rative\s+d'?habitants?\b|\bscic\b|\bg\.?f\.?a\.?\b|\bpropri[ée]t[ée]\s+collective\b"),
    ("propriete_protegee", r"\bfonds\s+de\s+dotation\b|\bfondation\s+(reconnue|d'?utilit[ée])\b"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Normalisation et slugification
# ─────────────────────────────────────────────────────────────────────────────

def deaccent(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def slugify(label: str) -> str:
    """Forge un slug à partir d'un nom de lieu. Retire accents, ponctuation,
    articles courts, longueur bornée."""
    s = deaccent(label.lower())
    s = re.sub(r"[^a-z0-9]+", " ", s)
    parts = [p for p in s.split() if p and p not in SLUG_STOP_WORDS]
    slug = "-".join(parts)[:80].strip("-")
    return slug or "lead-sans-nom"


def slug_lookup_key(label: str) -> str:
    """Clé de recherche pour fusion de leads (plus tolérante que slugify)."""
    return slugify(label)


# ─────────────────────────────────────────────────────────────────────────────
# Détecteurs d'indices structurels
# ─────────────────────────────────────────────────────────────────────────────

def detecter_nom_propre(texte: str, titre: str = "") -> tuple[bool, str | None]:
    """Heuristique nom de lieu : groupes de mots à majuscule dans le titre,
    précédés ou suivis d'un terme de lieu (ferme, domaine, hameau, écolieu,
    château…). Retourne (présent, nom_extrait_si_possible)."""
    # On privilégie le titre — plus stable que le corps.
    base = titre or texte[:300]
    if not base:
        return False, None
    motifs = [
        r"(?:Ferme|Domaine|Hameau|Écolieu|Ecolieu|Château|Chateau|Mas|Bergerie|"
        r"Oasis|Village|Ferme\s+de|Ferme\s+du|Ferme\s+des|Maison|Jardin|"
        r"Eco-lieu|Lieu-dit|Bastide|Manoir|Domaine\s+de|Domaine\s+du)\s+"
        r"(?:de\s+|du\s+|des\s+|de\s+la\s+|de\s+l['']\s*|d['']\s*)?"
        r"([A-ZÉÈÊÀÂÔÎÏÇŒÆ][\w\-'']{2,}(?:[\s-][A-ZÉÈÊÀÂÔÎÏÇŒÆ][\w\-'']{2,})*)",
        r"\b([A-ZÉÈÊÀÂÔÎÏÇŒÆ][\w\-'']{3,}(?:[\s-][A-ZÉÈÊÀÂÔÎÏÇŒÆ][\w\-'']{2,}){0,3})\s+"
        r"(?:ferme|domaine|hameau|écolieu|château|mas)",
    ]
    for motif in motifs:
        m = re.search(motif, base)
        if m:
            return True, m.group(0).strip()
    # Cas dégradé : un titre court entièrement en Titlecase, hors mots vides.
    mots = [w for w in re.findall(r"\b[\w'-]+\b", base[:80]) if w]
    if mots:
        cap = [w for w in mots if w[:1].isupper() and len(w) > 2
               and w.lower() not in SLUG_STOP_WORDS]
        if len(cap) >= 2 and len(cap) <= 5:
            return True, " ".join(cap[:4])
    return False, None


def detecter_localisation(texte: str) -> tuple[bool, dict[str, str]]:
    """Recherche région et/ou département. Retourne (présent, info)."""
    t = texte
    info: dict[str, str] = {}
    for r in REGIONS_FR:
        if re.search(r"\b" + re.escape(r) + r"\b", t, re.IGNORECASE):
            info["region"] = r
            break
    for d in DEPARTEMENTS_FR:
        if re.search(r"\b" + re.escape(d) + r"\b", t):
            info["departement"] = d
            break
    # Indices de commune : « à <Nom> » ou « (xxxxx) » (code postal).
    m_cp = re.search(r"\b(\d{5})\b", t)
    if m_cp:
        info["code_postal"] = m_cp.group(1)
    m_commune = re.search(r"\b(?:à|a)\s+([A-ZÉÈÊÀÂÔÎÏÇŒÆ][\w\-'']{2,}"
                          r"(?:[\s-][A-ZÉÈÊÀÂÔÎÏÇŒÆ][\w\-'']{2,}){0,3})", texte)
    if m_commune:
        info["commune_indice"] = m_commune.group(1)
    return bool(info), info


def detecter_entite_juridique(texte: str) -> tuple[bool, list[str]]:
    """FORMES_JURIDIQUES — retourne (présent, liste des formes détectées)."""
    found: list[str] = []
    for fid, motif in FORMES_JURIDIQUES:
        if re.search(motif, texte, re.IGNORECASE):
            found.append(fid)
    return bool(found), sorted(set(found))


def detecter_siren(texte: str) -> tuple[bool, dict[str, list[str]]]:
    """Repère un SIREN (9 chiffres) ou SIRET (14 chiffres) en évitant les
    faux positifs courants (codes postaux 5 chiffres, années 4 chiffres,
    téléphones avec espaces)."""
    # SIREN/SIRET vivent dans un contexte « Siren : 123 456 789 ».
    info: dict[str, list[str]] = {"siren": [], "siret": []}
    for m in re.finditer(r"\bsiren[\s:]*((?:\d[\s.]?){9})\b",
                         texte, re.IGNORECASE):
        s = re.sub(r"\D", "", m.group(1))
        if len(s) == 9:
            info["siren"].append(s)
    for m in re.finditer(r"\bsiret[\s:]*((?:\d[\s.]?){14})\b",
                         texte, re.IGNORECASE):
        s = re.sub(r"\D", "", m.group(1))
        if len(s) == 14:
            info["siret"].append(s)
    info["siren"] = sorted(set(info["siren"]))
    info["siret"] = sorted(set(info["siret"]))
    return bool(info["siren"] or info["siret"]), info


def detecter_montage_explicite(texte: str) -> tuple[bool, str | None]:
    """Présence explicite d'un type de montage parmi ceux de concepts.yml."""
    for type_id, motif in INDICES_MONTAGE_TYPE:
        if re.search(motif, texte, re.IGNORECASE):
            return True, type_id
    return False, None


def detecter_geoportail(loc_info: dict[str, str]) -> tuple[bool, str | None]:
    """Peut-on construire un lien Géoportail à partir de la localisation ?"""
    if loc_info.get("commune_indice") or loc_info.get("code_postal"):
        # Pas de coordonnées : l'opérateur devra confirmer la commune.
        return True, None
    return False, None


def calcul_indices_structurels(texte: str, titre: str = "") -> dict[str, Any]:
    """Renvoie le dict complet des indices structurels pour un texte."""
    nom_propre, nom = detecter_nom_propre(texte, titre)
    loc, loc_info = detecter_localisation(texte)
    ent, formes = detecter_entite_juridique(texte)
    siren_ok, siren_info = detecter_siren(texte)
    montage_ok, montage_type = detecter_montage_explicite(texte)
    geo_ok, _ = detecter_geoportail(loc_info)
    return {
        "indices": {
            "nom_propre": nom_propre,
            "localisation": loc,
            "entite_juridique": ent,
            "montage_explicite": montage_ok,
            "siren": siren_ok,
            "geoportail_localisable": geo_ok,
        },
        "extracted": {
            "nom": nom,
            "localisation": loc_info,
            "formes": formes,
            "siren": siren_info,
            "montage_type": montage_type,
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# Fréquence des sources — fenêtre de scan
# ─────────────────────────────────────────────────────────────────────────────

def lire_frequence(src: dict) -> str:
    """Normalise la valeur du champ `frequence:` d'une source."""
    f = (src.get("frequence") or "").strip().lower()
    if f in FREQUENCES_VALIDES:
        return f
    return FREQUENCE_DEFAUT


def fenetre_autorise_scan(src_id: str, frequence: str,
                          freq_log: dict, today: dt.date) -> bool:
    """Renvoie True si la fenêtre courante autorise un scan de la source."""
    if frequence == "sur_demande":
        return False  # ne scanne jamais automatiquement
    jours = JOURS_PAR_FREQUENCE.get(frequence)
    if jours is None:
        return False
    entry = freq_log.get(src_id) or {}
    last = entry.get("dernier_scan")
    if not last:
        return True
    try:
        last_d = dt.date.fromisoformat(last)
    except ValueError:
        return True
    return (today - last_d).days >= jours


def marquer_scan(src_id: str, freq_log: dict, today: dt.date,
                 status: str = "ok") -> None:
    freq_log[src_id] = {
        "dernier_scan": today.isoformat(),
        "dernier_statut": status,
    }


def load_freq_log() -> dict:
    fp = DISCOVERY / "_freq.json"
    if not fp.exists():
        return {}
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_freq_log(freq_log: dict) -> None:
    (DISCOVERY / "_freq.json").write_text(
        json.dumps(freq_log, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# Z0 — Capture brute
# ─────────────────────────────────────────────────────────────────────────────

def ecrire_raw(source_id: str, today: dt.date, items: Iterable[dict]) -> Path:
    """Écrit une ligne JSONL par item dans discovery/raw/<source>/YYYY-MM-DD.jsonl.
    Mode append — plusieurs runs dans la journée s'accumulent."""
    src_dir = RAW_DIR / source_id
    src_dir.mkdir(parents=True, exist_ok=True)
    fp = src_dir / f"{today.isoformat()}.jsonl"
    with fp.open("a", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    return fp


# ─────────────────────────────────────────────────────────────────────────────
# Z1 — Candidats scorés (JSONL structuré, complément du Markdown)
# ─────────────────────────────────────────────────────────────────────────────

def ecrire_candidates_jsonl(today: dt.date, candidates: list[dict]) -> Path:
    """Variante JSONL d'un fichier candidats — utilisée par les passes auto."""
    fp = DISCOVERY / f"candidates-{today.isoformat()}.jsonl"
    with fp.open("w", encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return fp


# ─────────────────────────────────────────────────────────────────────────────
# Z2 — Leads agrégés (fichier par lieu pressenti)
# ─────────────────────────────────────────────────────────────────────────────

# Limite de longueur pour les snippets stockés dans un lead (titre, texte).
MAX_TITRE_LEAD = 200
MAX_NOTE_LEAD = 600

# Délimiteur frontmatter YAML pour les fichiers .md de leads.
FM_DELIM = "---"


def lire_lead(slug: str) -> dict | None:
    """Charge un lead existant. Retourne None s'il n'existe pas."""
    fp = LEADS_DIR / f"{slug}.md"
    if not fp.exists():
        return None
    raw = fp.read_text(encoding="utf-8")
    fm, body = _split_frontmatter(raw)
    if fm is None:
        return None
    try:
        data = yaml.safe_load(fm) or {}
    except yaml.YAMLError:
        return None
    data["_body"] = body
    return data


def _split_frontmatter(raw: str) -> tuple[str | None, str]:
    if not raw.startswith(FM_DELIM):
        return None, raw
    parts = raw.split(FM_DELIM, 2)
    if len(parts) < 3:
        return None, raw
    return parts[1].strip(), parts[2].lstrip("\n")


def ecrire_lead(slug: str, data: dict) -> Path:
    """Écrit un lead — frontmatter YAML + corps Markdown libre."""
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    body = data.pop("_body", "")
    fp = LEADS_DIR / f"{slug}.md"
    fm_text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False,
                             default_flow_style=False).strip()
    fp.write_text(f"{FM_DELIM}\n{fm_text}\n{FM_DELIM}\n\n{body}",
                  encoding="utf-8")
    return fp


def fusionner_lead(slug: str, candidat: dict, indices: dict, today: dt.date,
                   nom_detecte: str | None = None) -> dict:
    """Fusionne un candidat dans un lead existant (ou crée le lead).

    candidat : dict produit par watch.py (clés : url, source_id, titre_page,
               texte, score, mots_cles, …).
    indices  : sortie de calcul_indices_structurels.
    """
    existing = lire_lead(slug)
    today_s = today.isoformat()

    extracted = indices.get("extracted", {})
    nom = (nom_detecte
           or (existing or {}).get("nom")
           or extracted.get("nom")
           or candidat.get("titre_page")
           or slug)

    source_entry = {
        "source": candidat.get("source_id"),
        "date": today_s,
        "url": candidat.get("url"),
        "titre": (candidat.get("titre_page") or "")[:MAX_TITRE_LEAD],
        "score": int(candidat.get("score", 0)),
    }

    if existing is None:
        data = {
            "slug": slug,
            "nom": nom,
            "cree": today_s,
            "dernier_repere": today_s,
            "score_cumule": int(candidat.get("score", 0)),
            "sources_vues": [source_entry],
            "indices_structurels": dict(indices["indices"]),
            "extracted": extracted,
            "statut": "actif",
        }
        data["_body"] = _body_initial(nom, candidat)
        return data

    # Fusion : on ajoute la source si l'URL n'y est pas déjà.
    body = existing.pop("_body", "")
    urls_vues = {s.get("url") for s in (existing.get("sources_vues") or [])}
    sources = list(existing.get("sources_vues") or [])
    if source_entry["url"] not in urls_vues:
        sources.append(source_entry)
        existing["score_cumule"] = int(existing.get("score_cumule", 0)) + \
            int(candidat.get("score", 0))
    existing["sources_vues"] = sources
    existing["dernier_repere"] = today_s

    # Indices : on conserve les True acquis, et on enregistre les nouveaux.
    indices_courants = dict(existing.get("indices_structurels") or {})
    for k, v in indices["indices"].items():
        indices_courants[k] = bool(indices_courants.get(k)) or bool(v)
    existing["indices_structurels"] = indices_courants

    # Extracted : fusion par concaténation des listes / mise à jour des dicts.
    merged_ext = dict(existing.get("extracted") or {})
    for k, v in extracted.items():
        if v is None or v == [] or v == {}:
            continue
        if isinstance(v, list):
            cur = set(merged_ext.get(k) or [])
            merged_ext[k] = sorted(cur | set(v))
        elif isinstance(v, dict):
            base = dict(merged_ext.get(k) or {})
            for kk, vv in v.items():
                if vv and not base.get(kk):
                    base[kk] = vv
            merged_ext[k] = base
        else:
            if not merged_ext.get(k):
                merged_ext[k] = v
    existing["extracted"] = merged_ext

    existing.setdefault("statut", "actif")
    existing["_body"] = body
    existing["slug"] = slug
    if not existing.get("nom"):
        existing["nom"] = nom
    return existing


def _body_initial(nom: str, candidat: dict) -> str:
    """Corps initial d'un lead (Markdown libre pour qualification manuelle)."""
    return (
        f"# Lead — {nom}\n\n"
        f"Premier signal détecté par la veille via la source "
        f"`{candidat.get('source_id', '?')}`. URL pivot : "
        f"{candidat.get('url', '?')}.\n\n"
        f"## Notes\n\n"
        f"_(à compléter à la main — éléments d'enquête, doutes, contacts)_\n"
    )


def lead_est_promouvable(lead: dict,
                         seuil_score: int = SEUIL_SCORE_PROMOTION,
                         nb_indices_min: int = NB_INDICES_REQUIS) -> bool:
    """Critère Z2 → Z3 : ≥ nb_indices_min parmi (nom_propre, localisation,
    entite_juridique) ET score cumulé ≥ seuil_score."""
    ind = lead.get("indices_structurels") or {}
    cles = ("nom_propre", "localisation", "entite_juridique")
    nb_ok = sum(1 for k in cles if bool(ind.get(k)))
    if nb_ok < nb_indices_min:
        return False
    return int(lead.get("score_cumule") or 0) >= seuil_score


# ─────────────────────────────────────────────────────────────────────────────
# Z3 — Pré-fiches (schéma 1bis partiellement rempli)
# ─────────────────────────────────────────────────────────────────────────────

def ecrire_prefiche(slug: str, lead: dict) -> Path:
    """Écrit une pré-fiche YAML au schéma 1bis à partir d'un lead. La
    pré-fiche est ensuite arbitrée manuellement et promue en lieux/<slug>.yml
    par l'opérateur (Z3 → Z4 MANUELLE)."""
    PREFICHES_DIR.mkdir(parents=True, exist_ok=True)
    fp = PREFICHES_DIR / f"{slug}.yml"
    extracted = lead.get("extracted") or {}
    loc = dict(extracted.get("localisation") or {})
    formes = list(extracted.get("formes") or [])

    porteurs: list[str] = []
    usufruitiers: list[str] = []
    # Heuristique simple : si une forme « porteur » est repérée, on la met
    # côté porteurs (fondation, fonds_dotation, collectivite). Le reste va
    # côté usufruitiers.
    portage = {"fondation", "fondation_reconnue", "fonds_dotation",
               "collectivite", "fonciere"}
    for f in formes:
        if f in portage:
            porteurs.append(f"_a_qualifier_{f}")
        else:
            usufruitiers.append(f"_a_qualifier_{f}")

    note = (lead.get("_body", "") or "").strip()
    if note:
        # On garde seulement la première ligne descriptive.
        first = next((l for l in note.splitlines() if l.strip()
                      and not l.startswith("#")), "")
        note_genese = first[:MAX_NOTE_LEAD]
    else:
        note_genese = f"Lead repéré par la veille — {lead.get('nom', slug)}."

    prefiche = {
        "categorie": "lieu",
        "slug": slug,
        "nom": lead.get("nom") or slug,
        "statut_fiche": "prefiche",
        "_source_lead": str((LEADS_DIR / f"{slug}.md").relative_to(ROOT)),
        "_genere_le": dt.date.today().isoformat(),
        "_score_cumule": int(lead.get("score_cumule") or 0),
        "_indices_structurels": dict(lead.get("indices_structurels") or {}),
        "localisation": {
            "commune": loc.get("commune_indice"),
            "departement": loc.get("departement"),
            "region": loc.get("region"),
            "code_postal": loc.get("code_postal"),
        },
        "montage": {
            "type": extracted.get("montage_type"),
            "articulations": [],
        },
        "chaine": {
            "porteurs": porteurs,
            "usufruitiers": usufruitiers,
        },
        "sources_veille": [
            {"source": s.get("source"), "url": s.get("url"),
             "date": s.get("date"), "score": s.get("score")}
            for s in (lead.get("sources_vues") or [])
        ],
        "note_genese": note_genese,
    }
    fp.write_text(yaml.safe_dump(prefiche, allow_unicode=True, sort_keys=False,
                                 default_flow_style=False),
                  encoding="utf-8")
    return fp


# ─────────────────────────────────────────────────────────────────────────────
# Orchestration des zones — fonction principale exposée à watch.py
# ─────────────────────────────────────────────────────────────────────────────

def traiter_candidats_pipeline(candidates: list[dict], today: dt.date,
                               seuil_score: int = SEUIL_SCORE_PROMOTION,
                               nb_indices_min: int = NB_INDICES_REQUIS
                               ) -> dict:
    """Traverse Z1 → Z2 → Z3 pour la liste de candidats fournis.

    Renvoie un dict avec :
      - leads_actifs     : nombre de leads en statut actif après la passe
      - leads_modifies   : slugs touchés dans la passe
      - prefiches_creees : slugs promus en Z3 dans la passe
    """
    leads_modifies: list[str] = []
    prefiches_creees: list[str] = []

    for c in candidates:
        texte_total = " ".join([
            c.get("titre_page") or "",
            c.get("texte") or "",
            " ".join(c.get("mots_cles") or []),
        ])
        analyse = calcul_indices_structurels(texte_total,
                                             c.get("titre_page") or "")
        nom = (analyse["extracted"].get("nom")
               or c.get("titre_page") or c.get("texte") or "")
        if not nom:
            continue
        slug = slug_lookup_key(nom)
        if not slug:
            continue
        lead = fusionner_lead(slug, c, analyse, today, nom_detecte=nom)
        ecrire_lead(slug, lead)
        leads_modifies.append(slug)

        # Re-lecture (ecrire_lead a popé _body) pour critère de promotion.
        lead_check = lire_lead(slug) or {}
        if (lead_check.get("statut") in (None, "actif")
                and lead_est_promouvable(lead_check, seuil_score,
                                         nb_indices_min)):
            ecrire_prefiche(slug, lead_check)
            # Statut promu enregistré dans le lead pour ne pas re-générer.
            lead_check["statut"] = "pre_fiche"
            ecrire_lead(slug, lead_check)
            prefiches_creees.append(slug)

    leads_actifs = _compter_leads_actifs()
    return {
        "leads_actifs": leads_actifs,
        "leads_modifies": sorted(set(leads_modifies)),
        "prefiches_creees": prefiches_creees,
    }


def _compter_leads_actifs() -> int:
    if not LEADS_DIR.exists():
        return 0
    n = 0
    for fp in LEADS_DIR.glob("*.md"):
        raw = fp.read_text(encoding="utf-8")
        fm, _ = _split_frontmatter(raw)
        if not fm:
            continue
        try:
            d = yaml.safe_load(fm) or {}
        except yaml.YAMLError:
            continue
        if d.get("statut") in (None, "actif"):
            n += 1
    return n
