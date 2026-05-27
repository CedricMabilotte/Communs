#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebond.py — Voie B du pipeline de veille : rebond depuis le corpus.

Le corpus actuel (lieux/, porteurs/, usufruitiers/, reseaux/, modeles/)
mentionne en prose, dans des champs descriptifs (notes, résumés,
articulations, analyses…), des entités qui n'ont pas encore leur propre
fiche : foncières, fondations, lieux, collectifs, baux particuliers,
fondateurs, etc. Ces noms cités-non-fichés sont des candidats à fort
signal — ils émergent de sources que le projet juge déjà fiables.

Ce script :

1. charge toutes les fiches YAML du corpus ;
2. indexe les uid + noms + noms_courts existants pour pouvoir rapprocher
   un nom détecté d'une fiche connue ;
3. parcourt les champs de prose de chaque fiche et y détecte les
   séquences de mots à majuscule (2+ tokens) qui ressemblent à des noms
   propres ;
4. élague les faux positifs courants à l'aide d'une liste de mots-stop
   (toponymes administratifs, noms de mois, formes juridiques nues, etc.) ;
5. agrège les noms candidats par occurrence et écrit un rapport Markdown
   dans discovery/rebonds.md : noms à fréquence ≥ 2 en tête (avec
   citations et extraits), noms à fréquence 1 en queue.

Heuristique pure — pas de LLM, pas d'API externe, stdlib + PyYAML.
Lecture seule des fiches : aucune écriture dans lieux/, porteurs/, etc.

Exécution : `python3 scripts/rebond.py` depuis la racine du projet.
"""
from __future__ import annotations

import datetime as dt
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable

import yaml

# ─────────────────────────────────────────────────────────────────────────────
# Repères de chemins
# ─────────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
DOSSIERS_FICHES = ["lieux", "porteurs", "usufruitiers", "reseaux", "modeles"]
DISCOVERY = ROOT / "discovery"
SORTIE = DISCOVERY / "rebonds.md"

# ─────────────────────────────────────────────────────────────────────────────
# Champs de prose explorés
# ─────────────────────────────────────────────────────────────────────────────
#
# Une fiche YAML mêle données structurées (chaînes, grille, dossier…) et
# prose libre (résumé, notes, descriptions, analyses…). On veut détecter
# les noms propres en prose seulement — pas dans les uid ni les chaînes
# d'identifiants. Les champs ci-dessous sont ceux où l'on s'attend à
# trouver des mentions de tierces entités.

CHAMPS_PROSE_RACINE = (
    "resume", "sous_titre", "synthese", "fiabilite", "note_genese",
)

CHAMPS_PROSE_OBJETS = {
    # bloc -> sous-champs textuels
    "montage": ("description", "nu_proprietaire", "usufruitier"),
    "integrite_montage": ("commentaire",),
    "analyse": ("synthese",),  # forces/fragilites/leviers traités à part (listes)
    "dossier": (),  # rien de prose direct ; pieces[].note traité à part
}

# Listes de prose à parcourir au niveau racine
LISTES_PROSE_RACINE = {
    "analyse": ("forces", "fragilites", "leviers"),  # listes de strings
}

# ─────────────────────────────────────────────────────────────────────────────
# Mots-stop : faux positifs systématiques à exclure
# ─────────────────────────────────────────────────────────────────────────────
#
# On retire les noms qui sont en réalité des toponymes administratifs,
# des noms de mois ou de jours, des formes juridiques nues, des étiquettes
# de pays, ou des entités françaises courantes sans valeur de signal.

STOP_WORDS = {
    # pays et grands ensembles géographiques
    "France", "Espagne", "Allemagne", "Italie", "Belgique", "Suisse",
    "Autriche", "Portugal", "Pays-Bas", "Royaume-Uni", "Luxembourg",
    "Europe", "Union Européenne", "Union Europeenne",
    "Maroc", "Algérie", "Algerie", "Tunisie", "Ukraine", "Russie",
    "Canada", "Brésil", "Bresil", "Chine", "Japon", "Inde", "Mexique",
    "États-Unis", "Etats-Unis", "Amérique", "Amerique",
    "Afrique", "Asie", "Océanie", "Oceanie",
    "Méditerranée", "Mediterranee",

    # régions administratives françaises
    "Bretagne", "Normandie", "Bourgogne-Franche-Comté", "Bourgogne",
    "Franche-Comté", "Franche-Comte", "Occitanie", "Nouvelle-Aquitaine",
    "Aquitaine", "Provence", "Provence-Alpes-Côte", "Côte d'Azur",
    "Auvergne", "Auvergne-Rhône-Alpes", "Rhône-Alpes", "Île-de-France",
    "Ile-de-France", "Pays de la Loire", "Pays-de-la-Loire",
    "Centre-Val de Loire", "Hauts-de-France", "Grand Est",
    "Languedoc-Roussillon", "Midi-Pyrénées", "Midi-Pyrenees",
    "Poitou-Charentes", "Limousin", "Alsace", "Lorraine",
    "Champagne-Ardenne", "Picardie", "Nord-Pas-de-Calais",
    "Corse", "Outre-Mer", "Outre-mer", "Massif Central",
    "Vallée du Rhône", "Vallee du Rhone",

    # grandes villes et préfectures
    "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes",
    "Strasbourg", "Montpellier", "Bordeaux", "Lille", "Rennes",
    "Reims", "Saint-Étienne", "Saint-Etienne", "Le Havre", "Toulon",
    "Grenoble", "Dijon", "Angers", "Nîmes", "Nimes", "Villeurbanne",
    "Clermont-Ferrand", "Aix-en-Provence", "Brest", "Limoges",
    "Tours", "Amiens", "Perpignan", "Metz", "Besançon", "Besancon",
    "Orléans", "Orleans", "Mulhouse", "Rouen", "Caen", "Nancy",
    "Argenteuil", "Saint-Denis", "Roubaix", "Tourcoing", "Avignon",
    "Poitiers", "Versailles", "Pau", "La Rochelle", "Calais",
    "Cannes", "Antibes", "Annecy", "Bourges", "Vannes", "Quimper",
    "Lorient", "Niort", "Chambéry", "Chambery", "Beauvais",
    "Bayonne", "Cherbourg", "Boulogne-Billancourt",
    "Saint-Nazaire", "Valence", "Troyes", "Lourdes", "Vichy",

    # mois et jours
    "Janvier", "Février", "Fevrier", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Aout", "Septembre", "Octobre", "Novembre",
    "Décembre", "Decembre",
    "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi",
    "Dimanche",

    # formes juridiques nues (à exclure seules — quand suivies d'un nom propre
    # la séquence complète passe)
    "Association", "Fondation", "Société", "Societe",
    "Coopérative", "Cooperative", "Collectif",
    "SCI", "SCIC", "GFA", "SCEA", "SAS", "SARL", "SA", "EARL", "GAEC",
    "GAEC EARL", "SCA", "EURL", "SASU", "SCP", "SELARL", "SCM",
    "GIE", "GAB", "OFS", "BRS", "CLT", "ORE",
    "FRUP", "RUP", "ESS", "FPS", "FDS",

    # institutions et entités françaises génériques
    "État", "Etat", "République", "Republique",
    "République Française", "Republique Francaise",
    "Conseil d'État", "Conseil d'Etat", "Sénat", "Senat",
    "Assemblée Nationale", "Assemblee Nationale",
    "INSEE", "DREAL", "DDT", "DRAF", "MSA",
    "Crédit Agricole", "Credit Agricole",
    "Banque Populaire", "Caisse d'Épargne", "Caisse d'Epargne",
    "Code Rural", "Code Civil", "Code Général",
    "Bulletin Officiel", "Journal Officiel",

    # divisions de fiche / sections de prose qui pourraient apparaître
    "Voir Aussi", "Voir Également", "Voir Egalement",
    "Sources", "Références", "References",

    # connecteurs et locutions courantes qui peuvent émerger en milieu
    # de phrase capitalisées (rare mais possible)
    "Cf",
}

# Normalisation : on stocke aussi la version normalisée (sans accents,
# minuscules) pour comparaison souple avec les uid et noms des fiches.
STOP_WORDS_NORM = {None}  # placeholder, rempli plus bas

# ─────────────────────────────────────────────────────────────────────────────
# Détection des noms propres
# ─────────────────────────────────────────────────────────────────────────────
#
# On cherche les séquences d'au moins 2 mots commençant par une
# majuscule (≥ 2 caractères, pour éviter les initiales). On accepte
# les liaisons par espace, tiret ou apostrophe, et les « petits mots »
# en minuscules entre deux capitalisés (de, du, des, le, la, les, et,
# à, en, sur, pour) pour capturer « Fonds de Terre Européenne »,
# « Domaine du Rayol », etc.

# Un « gros mot » capitalisé : majuscule + au moins une lettre ensuite
GROS_MOT = r"[A-ZÀ-Ý][a-zà-ÿ´'\-]+"
# Un « petit mot » de liaison admis au milieu
PETIT_MOT = r"(?:de|du|des|le|la|les|et|à|en|sur|au|aux|d'|l'|pour)"

# Séquence : un gros mot, suivi d'au moins un (petit mot OU gros mot),
# où le dernier token doit être un gros mot.
PATTERN_NOM_PROPRE = re.compile(
    r"(?<![A-Za-zÀ-ÿ])"  # bord gauche : pas de lettre collée
    r"(?:" + GROS_MOT + r")"
    r"(?:[ \-]+(?:" + PETIT_MOT + r"|" + GROS_MOT + r"))+"
)

# Pour identifier le « début de phrase » (où une majuscule est attendue
# pour des raisons purement grammaticales), on repère les positions
# précédées de . ! ? : ; ou de début de chaîne.
SEPARATEURS_PHRASE = re.compile(r"(?:^|[.!?:;\n]\s+)")

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def normaliser(s: str) -> str:
    """Retire accents, met en minuscules, supprime articles courants
    et ponctuation, pour rapprochement souple avec les uid."""
    if not s:
        return ""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    # remplace tirets/apostrophes/espaces par un seul espace pour comparer
    s = re.sub(r"[\-'’\s]+", " ", s)
    # retire articles et petits mots
    tokens = [
        t for t in s.split()
        if t not in {"le", "la", "les", "de", "du", "des",
                     "l", "d", "et", "a", "au", "aux", "en", "sur"}
    ]
    return " ".join(tokens).strip()


def charger_fiches() -> list[dict[str, Any]]:
    """Charge toutes les fiches YAML des dossiers du corpus.

    Renvoie une liste de dicts enrichis d'un champ `_path` (Path) et
    `_categorie` (str dérivée du dossier)."""
    fiches = []
    for dossier in DOSSIERS_FICHES:
        chemin_dossier = ROOT / dossier
        if not chemin_dossier.is_dir():
            continue
        for fichier in sorted(chemin_dossier.glob("*.yml")):
            try:
                with fichier.open("r", encoding="utf-8") as fh:
                    data = yaml.safe_load(fh) or {}
            except yaml.YAMLError as exc:
                print(f"[rebond] YAML invalide : {fichier} ({exc})")
                continue
            if not isinstance(data, dict):
                continue
            data["_path"] = fichier
            data["_categorie"] = dossier
            fiches.append(data)
    return fiches


def collecter_index_fiches(fiches: list[dict[str, Any]]) -> set[str]:
    """Construit l'index des noms/uid normalisés correspondant à des
    fiches existantes (pour exclure ces noms des candidats)."""
    index: set[str] = set()
    for fiche in fiches:
        for cle in ("uid", "nom", "nom_court", "slug"):
            val = fiche.get(cle)
            if isinstance(val, str) and val.strip():
                norme = normaliser(val)
                if norme:
                    index.add(norme)
    return index


def extraire_textes_prose(fiche: dict[str, Any]) -> list[str]:
    """Extrait toutes les chaînes de prose d'une fiche, en suivant
    quelques chemins canoniques (résumé, montage.description, notes
    d'articulations, notes de grille, analyse, etc.)."""
    textes: list[str] = []

    # 1. Champs prose directs à la racine
    for cle in CHAMPS_PROSE_RACINE:
        val = fiche.get(cle)
        if isinstance(val, str) and val.strip():
            textes.append(val)

    # 2. Champs prose dans des objets imbriqués
    for cle_obj, sous_cles in CHAMPS_PROSE_OBJETS.items():
        bloc = fiche.get(cle_obj)
        if not isinstance(bloc, dict):
            continue
        for sc in sous_cles:
            val = bloc.get(sc)
            if isinstance(val, str) and val.strip():
                textes.append(val)

    # 3. Articulations du montage : montage.articulations[].note
    montage = fiche.get("montage")
    if isinstance(montage, dict):
        articulations = montage.get("articulations")
        if isinstance(articulations, list):
            for art in articulations:
                if isinstance(art, dict):
                    note = art.get("note")
                    if isinstance(note, str) and note.strip():
                        textes.append(note)

    # 4. Grille[].note (les notes peuvent mentionner des entités)
    grille = fiche.get("grille")
    if isinstance(grille, list):
        for crit in grille:
            if isinstance(crit, dict):
                note = crit.get("note")
                if isinstance(note, str) and note.strip():
                    textes.append(note)

    # 5. Analyse : listes (forces, fragilites, leviers)
    analyse = fiche.get("analyse")
    if isinstance(analyse, dict):
        for cle_liste in LISTES_PROSE_RACINE.get("analyse", ()):
            liste = analyse.get(cle_liste)
            if isinstance(liste, list):
                for item in liste:
                    if isinstance(item, str) and item.strip():
                        textes.append(item)

    # 6. Dossier.pieces[].note
    dossier = fiche.get("dossier")
    if isinstance(dossier, dict):
        pieces = dossier.get("pieces")
        if isinstance(pieces, list):
            for piece in pieces:
                if isinstance(piece, dict):
                    note = piece.get("note")
                    if isinstance(note, str) and note.strip():
                        textes.append(note)

    # 7. Sources[].titre (souvent porteur de noms d'entités)
    sources = fiche.get("sources")
    if isinstance(sources, list):
        for src in sources:
            if isinstance(src, dict):
                titre = src.get("titre")
                if isinstance(titre, str) and titre.strip():
                    textes.append(titre)

    return textes


def segmenter_phrases(texte: str) -> list[tuple[int, str]]:
    """Découpe le texte en phrases. Renvoie une liste de (offset, phrase)
    où offset est l'indice de début de la phrase dans le texte d'origine.

    On segmente sur . ! ? : ; ainsi que sur les sauts de ligne. Les puces
    et les énumérations comptent comme des phrases distinctes. C'est
    grossier mais suffisant pour identifier les majuscules de début de
    phrase à neutraliser."""
    if not texte:
        return []
    phrases: list[tuple[int, str]] = []
    debut = 0
    # On itère sur les séparateurs : un séparateur + espace(s)/sauts marque
    # la fin d'une phrase.
    for m in re.finditer(r"[.!?:;\n]+\s+", texte):
        fin = m.start()
        if fin > debut:
            phrases.append((debut, texte[debut:fin]))
        debut = m.end()
    if debut < len(texte):
        phrases.append((debut, texte[debut:]))
    return phrases


# Liaisons en minuscules autorisées entre deux tokens capitalisés
PETITS_MOTS_LIAISON = {
    "de", "du", "des", "le", "la", "les", "et", "à", "en", "sur",
    "au", "aux", "d'", "l'", "pour", "ou",
}


def detecter_noms_propres(texte: str) -> list[str]:
    """Détecte les séquences de mots à majuscule (≥ 2 tokens) dans le
    texte.

    Stratégie : on découpe d'abord le texte en phrases, et dans chaque
    phrase on neutralise la première position (la majuscule du premier
    mot est grammaticale, pas un signal de nom propre). Cela élimine les
    faux positifs massifs créés par les listes `forces`/`fragilites`/
    `leviers` dont chaque entrée commence par un verbe à l'infinitif
    capitalisé (« Documenter le … », « Inscrire des … »).

    Pour récupérer quand même les noms propres qui se trouvent en
    *début* d'item de liste (par ex. « Statuts du GAEC… » où c'est bien
    « Statuts » qui démarre, mais aussi « Eau du Bassin Rennais y mène… »),
    on fait un compromis : on saute uniquement le **premier mot
    capitalisé seul** ; si la phrase commence par un nom propre composé
    de plusieurs gros mots collés (sans liaison minuscule entre les deux
    premiers), on le garde. Cela perd des occurrences en tête de phrase
    pour les noms à structure « Mot + de/du + Mot » — mais la voie B est
    un détecteur par accumulation : ce qui compte est qu'au moins une
    citation passe, et celles-là seront généralement en milieu de phrase
    dans d'autres fiches.
    """
    if not texte:
        return []
    noms: list[str] = []
    for offset_phrase, phrase in segmenter_phrases(texte):
        if not phrase.strip():
            continue
        # Repère la fin du premier token : si ce qui suit immédiatement
        # est un petit mot de liaison, on doit le garder dans la zone
        # neutralisée (la séquence entière « Documenter le » est suspecte).
        # Sinon, la première position est neutralisée tant que les deux
        # premiers gros mots ne sont pas adjacents.
        offset_neutralisation = 0
        m_premier = re.match(r"\s*(" + GROS_MOT + r")", phrase)
        if m_premier:
            fin_premier = m_premier.end()
            # Examine ce qui suit le premier gros mot : si c'est un petit
            # mot de liaison (de/du/le/…), on neutralise jusqu'à la fin
            # du second token (gros mot ou liaison). Sinon, on neutralise
            # juste le premier mot (et donc si le 2e mot est aussi un gros
            # mot directement collé, le pattern le rattrapera quand même).
            suite = phrase[fin_premier:]
            m_liaison = re.match(
                r"[ \-]+(" + "|".join(PETITS_MOTS_LIAISON) + r")\b",
                suite, flags=re.IGNORECASE,
            )
            if m_liaison:
                # Neutralise jusqu'à la fin de la liaison
                offset_neutralisation = fin_premier + m_liaison.end()
            else:
                offset_neutralisation = fin_premier

        for m in PATTERN_NOM_PROPRE.finditer(phrase):
            # Si la mention démarre dans la zone neutralisée du début de
            # phrase, on la saute. (Note : si elle démarre au début mais
            # déborde, on saute aussi — pour ne pas piéger un nom propre
            # qui inclurait le verbe à l'infinitif.)
            if m.start() < offset_neutralisation:
                continue
            candidat = m.group(0).strip()
            candidat = re.sub(r"\s+", " ", candidat)
            # Post-traitement : élague les liaisons en fin de séquence
            # (« Code de l' », « Cercle d' », « Crau en »). On retire
            # itérativement le ou les derniers tokens s'ils sont de
            # petits mots, jusqu'à ce que le dernier soit capitalisé.
            tokens = candidat.split()
            while tokens and tokens[-1].lower().rstrip("'") in (
                {p.rstrip("'") for p in PETITS_MOTS_LIAISON}
            ):
                tokens.pop()
            # Idem en tête : si la séquence commence par un petit mot
            # (cas rare mais possible avec « De Bonelli » détecté…), on
            # l'élague aussi.
            while tokens and tokens[0].lower().rstrip("'") in (
                {p.rstrip("'") for p in PETITS_MOTS_LIAISON}
            ):
                tokens.pop(0)
            candidat = " ".join(tokens)
            if len(tokens) < 2:
                continue
            mots_significatifs = [
                t for t in tokens
                if t.lower() not in PETITS_MOTS_LIAISON
            ]
            if not mots_significatifs:
                continue
            if all(mot in STOP_WORDS for mot in mots_significatifs):
                continue
            if candidat in STOP_WORDS:
                continue
            noms.append(candidat)
    return noms


def contexte_autour(texte: str, mention: str, marge: int = 80) -> str:
    """Renvoie un extrait du texte autour de la mention, pour donner
    une amorce de contexte."""
    idx = texte.find(mention)
    if idx < 0:
        return mention
    debut = max(0, idx - marge)
    fin = min(len(texte), idx + len(mention) + marge)
    extrait = texte[debut:fin].strip()
    # Nettoyer les sauts de ligne
    extrait = re.sub(r"\s+", " ", extrait)
    if debut > 0:
        extrait = "…" + extrait
    if fin < len(texte):
        extrait = extrait + "…"
    return extrait


# ─────────────────────────────────────────────────────────────────────────────
# Cœur du traitement
# ─────────────────────────────────────────────────────────────────────────────


def collecter_mentions(
    fiches: list[dict[str, Any]],
    index_fiches: set[str],
) -> dict[str, list[tuple[str, str, str]]]:
    """Parcourt toutes les fiches et collecte les mentions de noms
    propres qui ne correspondent PAS à une fiche existante.

    Renvoie : { nom_propre : [ (uid_citant, categorie, extrait), ... ] }
    """
    # On regroupe par version normalisée du nom (pour fusionner les
    # variantes d'accentuation/casse), mais on garde une « forme
    # canonique » lisible (la plus fréquente, ou la première rencontrée).

    # nom_normalise -> { "formes": Counter, "citations": [...] }
    accumulateur: dict[str, dict[str, Any]] = {}

    for fiche in fiches:
        uid = fiche.get("uid") or fiche["_path"].stem
        categorie = fiche["_categorie"]
        textes = extraire_textes_prose(fiche)
        for texte in textes:
            noms = detecter_noms_propres(texte)
            for nom in noms:
                norme = normaliser(nom)
                if not norme:
                    continue
                # Skip si correspond à une fiche existante (uid/nom)
                if norme in index_fiches:
                    continue
                # Skip si inclusion partielle dans un uid (slug forme
                # « domaine-du-rayol » contient « rayol »).
                # On vérifie l'inclusion bidirectionnelle pour limiter
                # les faux rapprochements ; le seuil est volontairement
                # large pour favoriser la précision (peu de bruit).
                rapproche = False
                for ref in index_fiches:
                    if not ref:
                        continue
                    # Le nom détecté est inclus dans une réf existante
                    # (et fait au moins 4 caractères pour éviter les
                    # collisions sur fragments trop courts)
                    if len(norme) >= 5 and norme in ref:
                        rapproche = True
                        break
                    # Ou la réf est incluse dans le nom détecté
                    if len(ref) >= 5 and ref in norme:
                        rapproche = True
                        break
                if rapproche:
                    continue
                # On enregistre la citation
                slot = accumulateur.setdefault(
                    norme, {"formes": {}, "citations": []}
                )
                slot["formes"][nom] = slot["formes"].get(nom, 0) + 1
                extrait = contexte_autour(texte, nom)
                slot["citations"].append((uid, categorie, extrait))

    # Convertit en dict { forme_canonique : citations }
    final: dict[str, list[tuple[str, str, str]]] = {}
    for norme, slot in accumulateur.items():
        # Forme canonique = celle la plus fréquente
        forme_canonique = max(slot["formes"].items(), key=lambda x: x[1])[0]
        final[forme_canonique] = slot["citations"]
    return final


def construire_rapport(mentions: dict[str, list[tuple[str, str, str]]]) -> str:
    """Construit le contenu du rapport Markdown à partir des mentions."""
    aujourd_hui = dt.date.today().isoformat()

    # Trier par fréquence décroissante, puis nom alphabétique
    classement = sorted(
        mentions.items(),
        key=lambda kv: (-len(kv[1]), kv[0].lower()),
    )

    # Séparer fréquence >= 2 et fréquence == 1
    forts = [(n, cits) for n, cits in classement if len(cits) >= 2]
    faibles = [(n, cits) for n, cits in classement if len(cits) == 1]

    lignes: list[str] = []
    lignes.append("# Rebonds — entités citées par le corpus mais non-fichées")
    lignes.append("")
    lignes.append(
        f"*Généré le {aujourd_hui} par `scripts/rebond.py`. "
        "Liste à arbitrer en ouverture de session de veille — "
        "heuristique pure, faux positifs attendus.*"
    )
    lignes.append("")
    lignes.append(
        f"Totaux : {len(mentions)} entités candidates "
        f"({len(forts)} à fréquence ≥ 2, {len(faibles)} à fréquence 1)."
    )
    lignes.append("")

    # Top — fréquence >= 2
    lignes.append("## Top des entités citées (fréquence ≥ 2)")
    lignes.append("")
    if not forts:
        lignes.append("*(Aucune entité citée plus d'une fois.)*")
        lignes.append("")
    else:
        for nom, citations in forts:
            lignes.append(f"### {nom}")
            lignes.append(f"- Citations : {len(citations)}")
            lignes.append("- Fiches citantes :")
            # Limiter à une citation par fiche (le même nom peut être
            # mentionné plusieurs fois dans une même fiche)
            vues = set()
            for uid, categorie, extrait in citations:
                cle = (uid, categorie)
                if cle in vues:
                    continue
                vues.add(cle)
                # Échapper les pipes éventuels qui casseraient les
                # listes Markdown (peu probable mais possible)
                extrait_md = extrait.replace("|", "\\|")
                lignes.append(
                    f"  - `{categorie}/{uid}.yml` — \"{extrait_md}\""
                )
            lignes.append("")

    # Signaux faibles — fréquence == 1
    lignes.append("## Entités citées une fois (signaux faibles)")
    lignes.append("")
    if not faibles:
        lignes.append("*(Aucun signal faible.)*")
        lignes.append("")
    else:
        lignes.append(
            "Liste à plat — un signal faible peut être un nom détecté "
            "par erreur ou une mention isolée à creuser au cas par cas."
        )
        lignes.append("")
        for nom, citations in faibles:
            uid, categorie, _ = citations[0]
            lignes.append(f"- **{nom}** — `{categorie}/{uid}.yml`")
        lignes.append("")

    return "\n".join(lignes) + "\n"


def main() -> None:
    fiches = charger_fiches()
    if not fiches:
        print("[rebond] Aucune fiche chargée — vérifie les dossiers du corpus.")
        return
    index = collecter_index_fiches(fiches)
    print(f"[rebond] {len(fiches)} fiches chargées, "
          f"{len(index)} identifiants/noms indexés.")
    mentions = collecter_mentions(fiches, index)
    print(f"[rebond] {len(mentions)} entités candidates détectées.")
    rapport = construire_rapport(mentions)
    DISCOVERY.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(rapport, encoding="utf-8")
    print(f"[rebond] Rapport écrit : {SORTIE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
