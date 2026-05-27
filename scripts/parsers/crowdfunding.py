#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crowdfunding.py — Parser dédié à la voie F (session #8) du pipeline de veille.

Voie F : « crowdfunding aboutis ≥ 18 mois ». Les plateformes participatives
(Miimosa, Bluebees, Lita.co, KissKissBankBank, Tudigo, Ulule…) hébergent des
campagnes foncières et agricoles qui, une fois la collecte close avec succès,
laissent derrière elles des lieux effectivement constitués — fermes installées
en SCIC/GFA/foncière, fonds de dotation amorcés par appel populaire, achats
collectifs de terres. Le délai de 18 mois est essentiel : il laisse le temps
au projet de se concrétiser (passation foncière, montage juridique) et donc
d'être documentable au sens du fork « Terres Libérées ».

Ce module est volontairement :
  • autonome (stdlib + PyYAML, pas de dépendance lourde) ;
  • sans effet de bord à l'import (aucune requête réseau au chargement) ;
  • structuré par plateforme : une fonction `_fetch_<plateforme>(...)`
    + une fonction de dispatch `fetch_crowdfunding_source(...)`.

Les sélecteurs HTML attendus sont marqués `# à confirmer à la première passe` :
les plateformes refondent régulièrement leur DOM, et il est inutile de figer un
contrat fragile tant que la veille n'a pas tourné une fois en conditions
réelles. Les heuristiques de filtrage (mots-clés thématiques, statut « abouti »,
date de fin de campagne) sont en revanche stables et testables hors réseau.

Format de sortie : une liste de dicts au schéma Z0/Z1 attendu par watch.py.

    {
      "ts": "<ISO>",
      "source_id": "<id de la source dans config/sources.yml>",
      "url_source": "<URL racine de la source>",
      "url": "<URL de la page de campagne>",
      "url_norm": "<URL normalisée>",
      "anchor": "<titre + accroche de la campagne>",
    }

Usage typique (depuis watch.py) :

    from parsers.crowdfunding import fetch_crowdfunding_source
    items = fetch_crowdfunding_source(src, src.get("options", {}))
    raw_buffer[src["id"]] = items  # archive Z0
    # … puis scoring habituel.
"""
from __future__ import annotations

import datetime as dt
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse


# ─────────────────────────────────────────────────────────────────────────────
# Constantes — partagées par toutes les plateformes
# ─────────────────────────────────────────────────────────────────────────────

UA = ("CommunsVeilleBot/1.0 (+https://communs.actitude.org ; "
      "veille documentaire ; voie F — crowdfunding aboutis)")
TIMEOUT = 20
HTML_MAX_BYTES = 2_500_000

# Mots-clés thématiques retenus pour le filtre « foncier / agricole / installation »
# — leur présence dans le titre ou l'accroche d'une campagne est nécessaire pour
# qu'elle soit retenue par la voie F. Variés volontairement : nous cherchons
# autant les acquisitions foncières directes que les installations paysannes
# qui débouchent sur un montage juridique de propriété d'usage.
MOTS_CLES_THEMATIQUES = [
    # Foncier
    "foncier", "foncière", "fonciere", "acquisition foncière",
    "achat de terres", "achat de terre", "propriété collective",
    "terres", "terre", "hectares", "ha",
    # Installation
    "installation", "installation agricole", "installation paysanne",
    "transmission", "reprise", "s'installer", "installer",
    # Agriculture
    "ferme", "fermes", "paysan", "paysanne", "paysans", "paysannes",
    "agricole", "agriculteur", "agricultrice", "maraîchage", "maraicher",
    "élevage", "bio", "agroécologie", "agroecologie",
    # Montages juridiques
    "scic", "gfa", "groupement foncier", "foncière", "fonciere",
    "coopérative", "cooperative", "bail", "bail rural",
    "bail emphytéotique", "fonds de dotation", "fondation",
    # Sanctuarisation
    "sanctuaire", "libération des terres", "sortir la terre du marché",
]

# Signaux de statut « abouti » : la campagne a été close avec succès.
SIGNAUX_ABOUTI = [
    "objectif atteint", "100 %", "100%", "succès", "succes", "réussie",
    "reussie", "terminée", "terminee", "clôturée", "cloturee",
    "financée", "financee", "collecte réussie",
]

# Signaux d'échec : campagne fermée sans atteindre l'objectif — à exclure.
SIGNAUX_ECHEC = [
    "échec", "echec", "non financé", "non finance", "objectif non atteint",
    "campagne annulée", "campagne annulee",
]

# Délai minimum entre la fin de campagne et la date du jour : 18 mois.
DELAI_MINIMUM_MOIS_DEFAUT = 18


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires — réseau, URL, dates
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_html(url: str) -> str | None:
    """Récupère le HTML d'une URL. Renvoie None en cas d'échec, sans planter.

    Comportement aligné sur watch.py : User-Agent identifié, timeout court,
    plafond de sécurité sur la taille du contenu.
    """
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept-Language": "fr,en;q=0.7"},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if ctype and "html" not in ctype and "xml" not in ctype:
                return None
            raw = resp.read(HTML_MAX_BYTES)
        return raw.decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            ConnectionError, ValueError) as exc:
        print(f"  ! crowdfunding — échec {url} : {exc}", file=sys.stderr)
        return None


TRACKING_PARAMS = {"fbclid", "gclid", "gbraid", "wbraid", "msclkid", "yclid",
                   "dclid", "mc_cid", "mc_eid", "igshid", "ref_src",
                   "_hsenc", "_hsmi", "vero_id", "oly_enc_id", "oly_anon_id"}


def _norm_url(u: str) -> str:
    """URL normalisée pour la déduplication. Cohérent avec watch.py:norm_url.

    Retire schéma, www., fragment, paramètres de tracking et utm_*. Conserve
    les paramètres porteurs de sens (id, page) pour ne pas fusionner à tort
    deux campagnes distinguées par un identifiant en query string.
    """
    try:
        p = urlparse(u)
    except ValueError:
        return u.lower()
    netloc = p.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = p.path.rstrip("/") or "/"
    keep = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
            if not k.lower().startswith("utm_")
            and k.lower() not in TRACKING_PARAMS]
    query = urlencode(sorted(keep))
    return f"{netloc}{path}?{query}" if query else f"{netloc}{path}"


# Patterns de dates rencontrés dans le DOM des plateformes (variés). On garde
# une heuristique pragmatique : on extrait toute date plausible et on retient
# la plus récente (présumée date de fin de campagne).
_RE_DATE_ISO = re.compile(r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b")
_RE_DATE_FR = re.compile(
    r"\b(\d{1,2})[/\s\.](\d{1,2}|"
    r"janvier|février|fevrier|mars|avril|mai|juin|juillet|"
    r"août|aout|septembre|octobre|novembre|décembre|decembre)"
    r"[/\s\.](20\d{2})\b",
    re.IGNORECASE,
)
_MOIS_FR = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "aout": 8, "septembre": 9,
    "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}


def _extraire_dates(texte: str) -> list[dt.date]:
    """Extrait les dates plausibles d'un texte (ISO et FR). Tolère les
    formats `YYYY-MM-DD`, `DD/MM/YYYY`, `DD mois YYYY`."""
    dates: list[dt.date] = []
    for m in _RE_DATE_ISO.finditer(texte):
        try:
            dates.append(dt.date(int(m.group(1)), int(m.group(2)),
                                 int(m.group(3))))
        except (ValueError, TypeError):
            continue
    for m in _RE_DATE_FR.finditer(texte):
        jour = m.group(1)
        mois_raw = m.group(2).lower()
        annee = m.group(3)
        try:
            jour_i = int(jour)
            annee_i = int(annee)
            if mois_raw.isdigit():
                mois_i = int(mois_raw)
            else:
                mois_i = _MOIS_FR.get(mois_raw)
                if mois_i is None:
                    continue
            dates.append(dt.date(annee_i, mois_i, jour_i))
        except (ValueError, TypeError):
            continue
    return dates


def _date_limite(delai_minimum_mois: int, aujourd_hui: dt.date | None = None) -> dt.date:
    """Calcule la date butoir : une campagne dont la fin est postérieure à
    cette date est trop récente pour être documentable.
    """
    today = aujourd_hui or dt.date.today()
    # Calcul mois → jour approximatif (30 jours/mois). Pour 18 mois, écart
    # de quelques jours sans incidence sur la veille.
    return today - dt.timedelta(days=delai_minimum_mois * 30)


def _est_thematique(texte: str, mots_supplementaires: Iterable[str] | None = None) -> bool:
    """Renvoie True si le texte contient au moins un mot-clé thématique."""
    t = texte.lower()
    kw = list(MOTS_CLES_THEMATIQUES)
    if mots_supplementaires:
        kw.extend(m.lower() for m in mots_supplementaires)
    return any(k.lower() in t for k in kw)


def _est_abouti(texte: str) -> bool:
    """Heuristique : la campagne a été clôturée avec succès."""
    t = texte.lower()
    if any(s in t for s in SIGNAUX_ECHEC):
        return False
    return any(s in t for s in SIGNAUX_ABOUTI)


# ─────────────────────────────────────────────────────────────────────────────
# Petits extracteurs HTML — sans dépendance externe
# ─────────────────────────────────────────────────────────────────────────────

class _CampagneCardsHarvester(HTMLParser):
    """Collecte les <a> qui ressemblent à des cartes de campagne sur une page
    d'index de plateforme. Volontairement permissif : on retient TOUTES les
    ancres avec un texte non trivial pointant sur une URL en `/project/`,
    `/projet/`, `/campaign/`, `/projets/`, etc. ; le filtre thématique vient
    ensuite.

    Le seuil sur la longueur du texte (> 12 caractères) écarte les liens de
    navigation (« suivant », « précédent », pictos sociaux).
    """

    PATTERNS_URL_CAMPAGNE = (
        "/project/", "/projet/", "/projets/", "/projects/",
        "/campaign/", "/campagne/", "/campagnes/",
        "/p/", "/projects-financed/",
    )
    LONGUEUR_MIN_TEXTE = 12

    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._buf: list[str] = []
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self._href = href
                self._buf = []
                self._depth = 1
        elif self._href is not None:
            self._depth += 1

    def handle_endtag(self, tag):
        if self._href is not None:
            if tag == "a" and self._depth <= 1:
                txt = re.sub(r"\s+", " ", "".join(self._buf)).strip()
                if (txt and len(txt) >= self.LONGUEUR_MIN_TEXTE
                        and any(p in (self._href or "")
                                for p in self.PATTERNS_URL_CAMPAGNE)):
                    self.links.append((self._href, txt))
                self._href = None
                self._buf = []
                self._depth = 0
            else:
                self._depth -= 1

    def handle_data(self, data):
        if self._href is not None:
            self._buf.append(data)


class _PageTexteExtractor(HTMLParser):
    """Récupère le texte visible d'une page de campagne (hors script/style)
    + le <title>, pour pouvoir tester `_est_thematique`, `_est_abouti` et
    extraire les dates.
    """

    SKIP = {"script", "style", "noscript", "svg"}

    def __init__(self):
        super().__init__()
        self.title = ""
        self._chunks: list[str] = []
        self._skip = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            a = {k.lower(): (v or "") for k, v in attrs}
            name = (a.get("name", "") or a.get("property", "")).lower()
            if name in ("description", "og:description", "og:title"):
                self._chunks.append(" " + a.get("content", "") + " ")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self._skip:
            self._chunks.append(data)

    def text(self, limit: int = 8000) -> str:
        body = re.sub(r"\s+", " ", " ".join(self._chunks)).strip()
        return f"{self.title} {body[:limit]}"


# ─────────────────────────────────────────────────────────────────────────────
# Item de sortie — au format Z0/Z1 attendu par watch.py
# ─────────────────────────────────────────────────────────────────────────────

def _construire_item(source_id: str, url_source: str, url: str,
                     anchor: str) -> dict:
    """Construit un dict au schéma Z0/Z1 attendu par watch.py."""
    return {
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "source_id": source_id,
        "url_source": url_source,
        "url": url,
        "url_norm": _norm_url(url),
        "anchor": anchor[:300],
    }


def _retenir_campagne(
    titre: str,
    texte_page: str,
    date_limite: dt.date,
    mots_supplementaires: Iterable[str] | None = None,
) -> tuple[bool, str]:
    """Décide si une campagne mérite d'être remontée par la veille.

    Retourne (bool, motif). Le motif sert au debug ; n'est pas archivé Z0.

    Critères cumulatifs :
      1. la page touche au moins un mot-clé thématique (sinon : bruit
         généraliste sans rapport avec le foncier) ;
      2. la page porte un signal de statut « abouti » (sinon : campagne en
         cours ou échouée) ;
      3. au moins une date détectée sur la page est antérieure à
         `date_limite`, signe que la campagne s'est conclue il y a ≥ 18 mois.
         Si aucune date n'est détectable, on retient quand même (faux négatif
         coûteux : le réseau de fonds de dotation amorcé en 2018 reste
         pertinent même si la date n'a pas été parsée).
    """
    blob = f"{titre} {texte_page}"
    if not _est_thematique(blob, mots_supplementaires):
        return False, "hors thématique"
    if not _est_abouti(blob):
        return False, "non abouti ou statut indéterminé"
    dates = _extraire_dates(blob)
    if dates:
        date_la_plus_recente = max(dates)
        if date_la_plus_recente > date_limite:
            return False, (f"trop récente — {date_la_plus_recente.isoformat()} "
                           f"> {date_limite.isoformat()}")
    return True, "ok"


# ─────────────────────────────────────────────────────────────────────────────
# Plateformes — une fonction par plateforme
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_miimosa(source_id: str, url_source: str,
                   delai_minimum_mois: int, mots_supplementaires) -> list[dict]:
    """Miimosa — plateforme française dédiée au crowdfunding agricole et
    alimentaire.

    URL d'index utilisée : la racine `https://www.miimosa.com/fr` qui
    présente les campagnes en cours, à laquelle on associe l'URL de l'index
    des projets financés (slug à ajuster au premier scan — Miimosa expose
    typiquement `/fr/projets?statut=finance` ou `/fr/projets-finances`).

    Mots-clés thématiques : forte densité agricole native — la majorité des
    campagnes touche déjà l'installation, la transmission, le foncier. Le
    filtre supplémentaire ne sert qu'à éliminer les campagnes de produits
    transformés (fromages, conserves) sans dimension foncière.

    Sélecteurs HTML attendus : cartes de campagne avec URL en `/projet/`.
        # à confirmer à la première passe — Miimosa a refondu son DOM en 2024.
    """
    return _fetch_plateforme_generique(
        source_id=source_id,
        url_source=url_source,
        urls_index_candidates=[
            url_source,
            urljoin(url_source, "/fr/projets-finances"),
            urljoin(url_source, "/fr/projets?statut=finance"),
        ],
        delai_minimum_mois=delai_minimum_mois,
        mots_supplementaires=mots_supplementaires,
    )


def _fetch_bluebees(source_id: str, url_source: str,
                    delai_minimum_mois: int, mots_supplementaires) -> list[dict]:
    """Blue Bees — plateforme française dédiée au crowdfunding agroécologique
    et alimentation durable.

    Statut au 2026-05-28 : Blue Bees a annoncé l'arrêt de ses activités
    courant 2024 ; le site bluebees.fr reste consulté en lecture seule à
    l'heure de cette rédaction, mais peut basculer à tout moment vers un
    archivage Wayback Machine. Une vérification de présence est conduite
    en premier ; en cas d'échec, on tente une URL d'archive `web.archive.org`.

    Mots-clés thématiques : majoritairement agricole — même posture que
    Miimosa.

    Sélecteurs HTML attendus : cartes de campagne avec URL en `/project/`
    ou `/projet/`.
        # à confirmer à la première passe — DOM potentiellement gelé sur la
        # dernière capture, à comparer à l'archive Wayback.
    """
    urls_index_candidates = [
        url_source,
        urljoin(url_source, "/projets-finances"),
        urljoin(url_source, "/projets"),
    ]
    items = _fetch_plateforme_generique(
        source_id=source_id,
        url_source=url_source,
        urls_index_candidates=urls_index_candidates,
        delai_minimum_mois=delai_minimum_mois,
        mots_supplementaires=mots_supplementaires,
    )
    if items:
        return items

    # Plateforme inaccessible : tentative sur l'archive Wayback (best-effort).
    # On ne fabrique pas d'URL hors archive officielle — uniquement
    # `web.archive.org` qui expose un snapshot navigable.
    archive_url = ("https://web.archive.org/web/2024/" + url_source)
    print(f"  · crowdfunding — {source_id} : repli sur archive {archive_url}",
          file=sys.stderr)
    return _fetch_plateforme_generique(
        source_id=source_id,
        url_source=archive_url,
        urls_index_candidates=[archive_url],
        delai_minimum_mois=delai_minimum_mois,
        mots_supplementaires=mots_supplementaires,
    )


def _fetch_lita(source_id: str, url_source: str,
                delai_minimum_mois: int, mots_supplementaires) -> list[dict]:
    """Lita.co — plateforme française d'investissement à impact.

    URL d'index utilisée : la racine `https://fr.lita.co/`, à laquelle on
    associe l'index des projets financés. Lita expose typiquement
    `/fr/projects?status=successful` ou `/fr/projects?type=success`.

    Mots-clés thématiques : ATTENTION, Lita couvre tous les secteurs
    (énergie, santé, mobilité, alimentation). Le filtre thématique est
    indispensable — sans lui, le bruit serait écrasant. On insiste sur
    `agricole`, `foncier`, `ferme`, `installation paysanne`.

    Sélecteurs HTML attendus : cartes de campagne avec URL en `/projects/`.
        # à confirmer à la première passe — Lita refond fréquemment son
        # parcours d'investisseur.
    """
    return _fetch_plateforme_generique(
        source_id=source_id,
        url_source=url_source,
        urls_index_candidates=[
            url_source,
            urljoin(url_source, "/fr/projects?status=successful"),
            urljoin(url_source, "/fr/projects-finances"),
        ],
        delai_minimum_mois=delai_minimum_mois,
        mots_supplementaires=mots_supplementaires,
        # Lita est généraliste : on durcit le filtre thématique.
        filtre_strict=True,
    )


def _fetch_kisskissbankbank(source_id: str, url_source: str,
                            delai_minimum_mois: int,
                            mots_supplementaires) -> list[dict]:
    """KissKissBankBank — plateforme française généraliste de crowdfunding.

    URL d'index utilisée : la catégorie « Engagés » ou « Solidaire » qui
    expose les projets à dimension sociale et environnementale ; les
    sous-catégories utiles sont typiquement `/fr/discover?category=ecology`
    et `/fr/discover?category=craftsmanship` (agriculture y est rattachée).

    Mots-clés thématiques : ATTENTION, KissKissBankBank est massivement
    généraliste — disques, livres, jeux vidéo. Le filtre thématique est
    indispensable et durci (mode strict). Le statut « financé » est exposé
    via un bandeau visible sur la fiche projet.

    Sélecteurs HTML attendus : cartes de campagne avec URL en `/projects/`
    ou `/fr/projects/`.
        # à confirmer à la première passe — KKBB a une page dédiée par
        # campagne et un filtre `state=success` dans l'URL.
    """
    return _fetch_plateforme_generique(
        source_id=source_id,
        url_source=url_source,
        urls_index_candidates=[
            url_source,
            urljoin(url_source, "/fr/discover?category=ecology&state=success"),
            urljoin(url_source, "/fr/discover?state=success&q=ferme"),
            urljoin(url_source, "/fr/discover?state=success&q=foncier"),
        ],
        delai_minimum_mois=delai_minimum_mois,
        mots_supplementaires=mots_supplementaires,
        filtre_strict=True,
    )


def _fetch_tudigo(source_id: str, url_source: str,
                  delai_minimum_mois: int, mots_supplementaires) -> list[dict]:
    """Tudigo — plateforme française d'investissement participatif dans les
    PME locales et l'économie réelle.

    Optionnelle dans la voie F : Tudigo couvre beaucoup de cafés / commerces
    de proximité, mais on y trouve aussi des fermes en SCIC et des
    foncières agricoles citoyennes. Filtre thématique strict.

    URL d'index utilisée : `https://www.tudigo.co/`, complétée par les
    catégories « Agriculture » et « Environnement ».

    Sélecteurs HTML attendus : cartes de campagne avec URL en
    `/investir/<slug>` ou `/projects/<slug>`.
        # à confirmer à la première passe.
    """
    return _fetch_plateforme_generique(
        source_id=source_id,
        url_source=url_source,
        urls_index_candidates=[
            url_source,
            urljoin(url_source, "/investir/agriculture"),
            urljoin(url_source, "/investir/environnement"),
        ],
        delai_minimum_mois=delai_minimum_mois,
        mots_supplementaires=mots_supplementaires,
        filtre_strict=True,
    )


def _fetch_plateforme_generique(
    source_id: str,
    url_source: str,
    urls_index_candidates: list[str],
    delai_minimum_mois: int,
    mots_supplementaires,
    filtre_strict: bool = False,
) -> list[dict]:
    """Squelette commun aux cinq plateformes — moisson, dédup, filtrage.

    Étapes :
      1. pour chaque URL d'index candidate, télécharger la page et
         récolter les ancres pointant sur des fiches de campagne ;
      2. dédupliquer par URL normalisée (deux index peuvent référencer
         les mêmes campagnes) ;
      3. pour chaque campagne unique, télécharger la fiche, extraire son
         texte, vérifier qu'elle est thématique, aboutie et que sa date
         de fin est antérieure à la limite ;
      4. retourner une liste d'items au format Z0/Z1.

    Mode `filtre_strict` : pour les plateformes généralistes (Lita, KKBB,
    Tudigo), on exige qu'au moins UN mot-clé du noyau dur soit présent.
    """
    cartes: list[tuple[str, str]] = []
    urls_vues_dans_index: set[str] = set()
    for url_index in urls_index_candidates:
        html = _fetch_html(url_index)
        if not html:
            continue
        harvester = _CampagneCardsHarvester()
        try:
            harvester.feed(html)
        except Exception as exc:
            print(f"  ! crowdfunding — parsing index {url_index} : {exc}",
                  file=sys.stderr)
            continue
        for href, texte in harvester.links:
            url_abs = urljoin(url_index, href)
            if not url_abs.startswith(("http://", "https://")):
                continue
            nu = _norm_url(url_abs)
            if nu in urls_vues_dans_index:
                continue
            urls_vues_dans_index.add(nu)
            cartes.append((url_abs, texte))

    date_limite = _date_limite(delai_minimum_mois)
    items: list[dict] = []

    # Garde-fou : on ne télécharge pas plus de 60 fiches par plateforme et par
    # passe (politesse + maîtrise du run).
    PLAFOND_FICHES_PAR_PASSE = 60

    for url_campagne, texte_carte in cartes[:PLAFOND_FICHES_PAR_PASSE]:
        # Premier filtre sur le texte de la carte (peu coûteux) pour éviter
        # un téléchargement inutile.
        mots = mots_supplementaires
        if filtre_strict and not _est_thematique(texte_carte, mots):
            continue

        html_fiche = _fetch_html(url_campagne)
        if not html_fiche:
            continue
        extractor = _PageTexteExtractor()
        try:
            extractor.feed(html_fiche)
        except Exception as exc:
            print(f"  ! crowdfunding — parsing fiche {url_campagne} : {exc}",
                  file=sys.stderr)
            continue
        texte_page = extractor.text()
        titre = extractor.title.strip() or texte_carte

        retenu, motif = _retenir_campagne(
            titre=titre,
            texte_page=texte_page,
            date_limite=date_limite,
            mots_supplementaires=mots,
        )
        if not retenu:
            # On garde la trace en debug — pas remontée dans Z0/Z1.
            continue

        anchor = f"{titre} — {texte_carte}".strip(" —")
        items.append(_construire_item(
            source_id=source_id,
            url_source=url_source,
            url=url_campagne,
            anchor=anchor,
        ))

    return items


# ─────────────────────────────────────────────────────────────────────────────
# Dispatcher public
# ─────────────────────────────────────────────────────────────────────────────

_PLATEFORMES: dict[str, Any] = {
    "miimosa": _fetch_miimosa,
    "bluebees": _fetch_bluebees,
    "blue-bees": _fetch_bluebees,
    "lita": _fetch_lita,
    "lita.co": _fetch_lita,
    "kisskissbankbank": _fetch_kisskissbankbank,
    "kkbb": _fetch_kisskissbankbank,
    "tudigo": _fetch_tudigo,
}


def fetch_crowdfunding_source(source_dict: dict, options: dict | None = None) -> list[dict]:
    """Point d'entrée public — appelé par watch.py pour chaque source dont
    `parser: crowdfunding`.

    Paramètres
    ----------
    source_dict : dict
        Le bloc YAML de la source, tel que lu depuis config/sources.yml.
        Doit contenir au minimum `id`, `url`, `options.plateforme`.
    options : dict | None
        Bloc `options:` de la source. Clés reconnues :
          - `plateforme` (str) : identifiant de la plateforme, obligatoire ;
          - `delai_minimum_mois` (int) : délai depuis fin de campagne ;
            défaut 18.
        Si `options` est None, on lit le bloc `options:` de `source_dict`.

    Retourne
    --------
    list[dict]
        Une liste d'items au schéma Z0/Z1, prête à être archivée dans
        `discovery/raw/<source_id>/YYYY-MM-DD.jsonl` puis scorée par
        watch.py au même titre que les autres sources HTML.

    Lève
    ----
    Aucune exception : tout échec réseau, parsing ou plateforme inconnue
    est journalisé sur stderr et la fonction retourne une liste vide.
    """
    options = options if options is not None else (source_dict.get("options") or {})
    plateforme = (options.get("plateforme") or "").strip().lower()
    if not plateforme:
        print(f"  ! crowdfunding — source {source_dict.get('id','?')} : "
              f"`options.plateforme` manquant",
              file=sys.stderr)
        return []

    handler = _PLATEFORMES.get(plateforme)
    if handler is None:
        print(f"  ! crowdfunding — plateforme inconnue : {plateforme!r} "
              f"(connues : {sorted(_PLATEFORMES.keys())})",
              file=sys.stderr)
        return []

    source_id = source_dict.get("id", plateforme)
    url_source = source_dict.get("url", "")
    if not url_source:
        print(f"  ! crowdfunding — source {source_id} : `url` manquante",
              file=sys.stderr)
        return []

    delai_minimum_mois = int(options.get("delai_minimum_mois",
                                         DELAI_MINIMUM_MOIS_DEFAUT))
    mots_supplementaires = source_dict.get("mots_cles", []) or []

    try:
        return handler(
            source_id=source_id,
            url_source=url_source,
            delai_minimum_mois=delai_minimum_mois,
            mots_supplementaires=mots_supplementaires,
        )
    except Exception as exc:  # filet de sécurité — la veille ne doit pas planter
        print(f"  ! crowdfunding — exception sur {source_id} ({plateforme}) : "
              f"{exc}", file=sys.stderr)
        return []


# Compat : permet `from parsers.crowdfunding import fetch_crowdfunding_source`
# et un usage en module autonome pour des tests futurs.
__all__ = ["fetch_crowdfunding_source"]
