#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
watch.py — Veille automatisée du projet « Communs / Terres Libérées ».

Lit config/sources.yml, interroge chaque source web, repère les liens qui
évoquent la libération des terres, approfondit les meilleurs candidats en
analysant la page pointée, écarte ce qui est déjà référencé, et écrit une
liste de CANDIDATS à examiner dans discovery/.

Améliorations cycle D (audit veille) :
 - P1 : analyse de la page candidate (titre, meta, corps), pas que l'ancre ;
 - P2 : scoring pondéré + signaux négatifs anti-bruit ;
 - P3 : détecteur d'angles morts (régions / montages sous-représentés) ;
 - P4 : mémoire des passes (discovery/_seen.json) + dédup par URL normalisée ;
 - P7 : statut « ignore » durable, tenu à la main (discovery/ignore.txt) ;
        dédup d'URL préservant les paramètres signifiants (session #2).

Cycle E (pipeline à zones, lot 2 de la refonte #6) :
 - Z0 : capture brute en JSONL par source — discovery/raw/<source>/YYYY-MM-DD.jsonl
 - Z1 : candidats scorés (Markdown rétrocompatible + candidates-*.jsonl)
 - Z2 : leads agrégés par lieu pressenti — discovery/leads/<slug>.md
 - Z3 : pré-fiches au schéma 1bis — discovery/prefiches/<slug>.yml
 - Fréquence par source (frequence: hebdomadaire | mensuelle | trimestrielle |
   sur_demande) — fenêtre tracée dans discovery/_freq.json.
 - Mode --dry-run : pas de requêtes externes, replay sur les JSONL de Z0
   existants pour valider la traversée Z1 → Z2 → Z3.

Volontairement sans dépendance lourde (urllib + html.parser de la stdlib ;
PyYAML pour la config). Aucune clé d'API requise. La promotion d'un candidat
en fiche reste une décision humaine — la veille ne fait que défricher.

Usage : python3 scripts/watch.py [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.request
import urllib.error
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qsl, urlencode

import yaml

# Pipeline à zones Z0–Z3 — module compagnon.
from pipeline import (
    DISCOVERY as PIPELINE_DISCOVERY,
    RAW_DIR, LEADS_DIR, PREFICHES_DIR,
    SEUIL_SCORE_PROMOTION, NB_INDICES_REQUIS, FREQUENCE_DEFAUT,
    lire_frequence, fenetre_autorise_scan, marquer_scan,
    load_freq_log, save_freq_log,
    ecrire_raw, ecrire_candidates_jsonl,
    traiter_candidats_pipeline,
)

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
DISCOVERY = ROOT / "discovery"
UA = "CommunsVeilleBot/1.0 (+https://communs.actitude.org ; veille documentaire)"
TIMEOUT = 20
POLITE_DELAY = 2.0          # secondes entre deux requêtes
MAX_DEEP_FETCH = 40         # plafond de pages candidates approfondies par passe

# Mots-clés « forts » par défaut — surchargés par sources.yml:mots_cles_forts.
STRONG_KW_DEFAULT = ["libération des terres", "nue-propriété", "usufruit",
                     "fonds de dotation", "démembrement"]

# Formes juridiques attendues — leur présence qualifie un candidat.
FORMES = ["fondation", "fonds de dotation", "scic", "gfa",
          "bail emphytéotique", "bail réel solidaire", "coopérative d'habitants",
          "société civile", "foncière", "association"]

# Signaux négatifs — bruit financier / marchand : retranchent des points.
NEGATIFS = ["faire un don", "objectif de financement", "collecte de fonds",
            "à vendre", "investissez", "rendement", "sci familiale",
            "défiscalisation", "souscription de parts"]

# Treize régions métropolitaines — référence pour le détecteur d'angles morts.
REGIONS_FR = [
    "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Bretagne",
    "Centre-Val de Loire", "Corse", "Grand Est", "Hauts-de-France",
    "Île-de-France", "Normandie", "Nouvelle-Aquitaine", "Occitanie",
    "Pays de la Loire", "Provence-Alpes-Côte d'Azur",
]


# ─────────────────────────────────────────────────────────────────────────────
# Extraction des liens d'une page
# ─────────────────────────────────────────────────────────────────────────────

class LinkHarvester(HTMLParser):
    """Collecte (href, texte) de chaque <a> de la page."""

    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._buf = []
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
                if txt:
                    self.links.append((self._href, txt))
                self._href = None
                self._buf = []
                self._depth = 0
            else:
                self._depth -= 1

    def handle_data(self, data):
        if self._href is not None:
            self._buf.append(data)


class TextExtractor(HTMLParser):
    """Récupère <title>, meta description et le texte visible (hors
    script/style) de la page candidate (audit veille P1)."""

    SKIP = {"script", "style", "noscript", "svg"}

    def __init__(self):
        super().__init__()
        self.title, self.meta_desc = "", ""
        self._chunks, self._skip, self._in_title = [], 0, False

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            a = {k.lower(): (v or "") for k, v in attrs}
            name = (a.get("name", "") or a.get("property", "")).lower()
            if name in ("description", "og:description"):
                self.meta_desc = a.get("content", "")

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

    def text(self, limit=2000):
        body = re.sub(r"\s+", " ", " ".join(self._chunks)).strip()
        return f"{self.title} {self.meta_desc} {body[:limit]}"


def fetch(url: str) -> str | None:
    """Récupère le HTML d'une URL ; renvoie None en cas d'échec (sans planter)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "fr,en;q=0.7"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "html" not in ctype and "xml" not in ctype and ctype:
                return None
            raw = resp.read(2_500_000)  # plafond de sécurité
        return raw.decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            ConnectionError, ValueError) as exc:
        print(f"  ! échec {url} : {exc}", file=sys.stderr)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Normalisation et déduplication par URL (audit veille P4)
# ─────────────────────────────────────────────────────────────────────────────

def normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


# Paramètres de requête purement publicitaires / analytiques : retirés de
# l'URL normalisée. Tout préfixe « utm_ » est également retiré (voir norm_url).
TRACKING_PARAMS = {"fbclid", "gclid", "gbraid", "wbraid", "msclkid", "yclid",
                   "dclid", "mc_cid", "mc_eid", "igshid", "ref_src",
                   "_hsenc", "_hsmi", "vero_id", "oly_enc_id", "oly_anon_id"}


def norm_url(u: str) -> str:
    """URL normalisée pour la déduplication : sans schéma, sans www., sans
    fragment, sans barre oblique finale, et sans paramètres de tracking
    (utm_*, fbclid, gclid…). Les paramètres porteurs de sens — identifiant
    d'article, numéro de page — sont CONSERVÉS : deux pages distinguées par
    un tel paramètre ne sont pas fusionnées à tort en doublon."""
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


# ─────────────────────────────────────────────────────────────────────────────
# Scoring pondéré (audit veille P2)
# ─────────────────────────────────────────────────────────────────────────────

def score_candidate(text: str, source_kw, transverse_kw, strong_kw):
    """Score pondéré : mot-clé de source = 1, transverse = 2, fort = 3,
    forme juridique attendue = 2 ; signaux négatifs = -2 chacun."""
    t = normalise(text)
    score, hits = 0, []
    for kw in source_kw or []:
        if normalise(kw) in t:
            score += 1
            hits.append(kw)
    for kw in transverse_kw or []:
        if normalise(kw) in t:
            score += 2
            hits.append(kw)
    for kw in strong_kw or []:
        if normalise(kw) in t:
            score += 3
            hits.append(kw)
    for f in FORMES:
        if f in t:
            score += 2
            hits.append(f)
    for n in NEGATIFS:
        if n in t:
            score -= 2
    return score, sorted(set(hits))


# ─────────────────────────────────────────────────────────────────────────────
# Connaissance de l'existant — dédup contre les fiches (audit veille P4)
# ─────────────────────────────────────────────────────────────────────────────

def known_urls():
    """Renvoie (urls_exactes_normalisées, domaines). Indexe le champ url: ET
    le bloc sources: de chaque fiche, pas seulement url:."""
    exact, domains = set(), set()
    for folder in ("lieux", "porteurs", "usufruitiers", "modeles"):
        d = ROOT / folder
        if not d.exists():
            continue
        for fp in d.glob("*.yml"):
            try:
                data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            urls = [data.get("url")]
            for s in (data.get("sources") or []):
                if isinstance(s, dict) and s.get("url"):
                    urls.append(s["url"])
            for u in filter(None, urls):
                exact.add(norm_url(str(u)))
                net = urlparse(str(u)).netloc.lower()
                domains.add(net[4:] if net.startswith("www.") else net)
    return exact, domains


# ─────────────────────────────────────────────────────────────────────────────
# Détecteur d'angles morts (audit veille P3)
# ─────────────────────────────────────────────────────────────────────────────

def corpus_profile():
    """Compte la couverture du corpus par région et par type de montage."""
    regions, montages = Counter(), Counter()
    for folder in ("lieux", "porteurs", "usufruitiers"):
        d = ROOT / folder
        if not d.exists():
            continue
        for fp in d.glob("*.yml"):
            try:
                data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            loc = data.get("localisation") or {}
            if loc.get("region"):
                regions[loc["region"]] += 1
            m = data.get("montage") or {}
            if m.get("type"):
                montages[m["type"]] += 1
    return regions, montages


def montage_labels():
    """Libellés des types de montage, lus depuis concepts.yml."""
    try:
        cc = yaml.safe_load((CONFIG / "concepts.yml").read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError):
        return {}
    return {m["id"]: m.get("label", m["id"])
            for m in (cc.get("montages") or [])}


def blind_spots(regions, montages, mont_labels):
    """Régions et montages absents ou faiblement couverts (≤ 1 fiche)."""
    faibles_r = [r for r in REGIONS_FR if regions.get(r, 0) <= 1]
    faibles_m = [m for m in mont_labels if montages.get(m, 0) <= 1]
    return faibles_r, faibles_m


def angle_mort_bonus(text, faibles_r, faibles_m, mont_labels):
    """Bonus de score si la page candidate touche un angle mort du corpus."""
    t = normalise(text)
    touched = []
    for r in faibles_r:
        if normalise(r) in t:
            touched.append(r)
    for m in faibles_m:
        lab = mont_labels.get(m, m)
        # on teste le label et l'id ; un mot du label suffit s'il est distinctif
        if normalise(m) in t or normalise(lab) in t:
            touched.append(lab)
    bonus = 2 if touched else 0
    return bonus, touched


# ─────────────────────────────────────────────────────────────────────────────
# Mémoire des passes (audit veille P4)
# ─────────────────────────────────────────────────────────────────────────────

def load_seen():
    fp = DISCOVERY / "_seen.json"
    if not fp.exists():
        return {}
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_seen(seen):
    (DISCOVERY / "_seen.json").write_text(
        json.dumps(seen, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8")


def load_ignore():
    """URLs à écarter durablement de la veille — liste tenue à la main.

    Fichier `discovery/ignore.txt` : une URL par ligne, « # » pour un
    commentaire. Chaque ligne est passée par norm_url, donc on peut y coller
    une URL brute (avec schéma, www., paramètres) : elle sera reconnue. C'est
    le moyen propre de dire « ne me re-propose plus jamais ce candidat »,
    sans éditer _seen.json à la main."""
    fp = DISCOVERY / "ignore.txt"
    if not fp.exists():
        return set()
    out = set()
    for line in fp.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.add(norm_url(line))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────────────────────────────────────────

# Échantillons synthétiques pour --dry-run. On évite toute requête externe :
# les candidats simulent ce que produirait la veille sur quelques pages réelles
# (ferme TDL en Hauts-de-France, bail emphytéotique Larzac, simple bruit
# financier qui doit être filtré).
_DRY_RUN_CANDIDATES = [
    {
        "titre_page": "Ferme de la Coccinelle — Terre de Liens",
        "texte": "Ferme de la Coccinelle à Witternheim, Bas-Rhin. "
                 "Acquisition par la Foncière Terre de Liens, bail rural "
                 "environnemental confié à une association. Hauts-de-France. "
                 "Siren : 453 985 731. Société civile dédiée.",
        "url": "https://example.test/coccinelle",
        "source_id": "terre-de-liens",
        "categorie_probable": ["lieu", "porteur"],
        "score": 14,
        "mots_cles": ["ferme", "foncière", "association", "fonds de dotation"],
        "angle_mort": ["Hauts-de-France"],
        "fiche_existante": False, "domaine_connu": True, "statut": "nouveau",
    },
    {
        "titre_page": "Ferme de la Coccinelle — page d'actualité",
        "texte": "Nouvelle campagne de don pour la Ferme de la Coccinelle "
                 "à Witternheim. Bail rural environnemental, association "
                 "porteuse, propriété de la Fondation Terre de Liens "
                 "reconnue d'utilité publique.",
        "url": "https://example.test/coccinelle-don",
        "source_id": "terre-de-liens",
        "categorie_probable": ["lieu"],
        "score": 13,
        "mots_cles": ["fondation", "association", "bail"],
        "angle_mort": [],
        "fiche_existante": False, "domaine_connu": True, "statut": "revu",
    },
    {
        "titre_page": "Plafonds d'éligibilité au BRS pour 2026",
        "texte": "Plafonds d'éligibilité — OFS — bail réel solidaire.",
        "url": "https://example.test/brs",
        "source_id": "foncier-solidaire",
        "categorie_probable": ["porteur"],
        "score": 5,
        "mots_cles": ["BRS", "OFS", "bail réel solidaire"],
        "angle_mort": [],
        "fiche_existante": False, "domaine_connu": False, "statut": "nouveau",
    },
]


def run_dry() -> int:
    """Mode --dry-run : exerce Z1 → Z2 → Z3 sans requête externe.

    On teste : (a) la fusion d'un lead à partir de deux candidats référant
    le même lieu ; (b) le franchissement du seuil de promotion Z2 → Z3 ;
    (c) l'absence de pré-fiche sur un candidat structurellement faible."""
    print("Mode dry-run : aucune requête réseau. Test du pipeline Z1 → Z2 → Z3.")
    DISCOVERY.mkdir(exist_ok=True)
    today_d = dt.date.today()

    # Z0 — on archive aussi les candidats simulés pour vérifier la mécanique.
    by_src: dict[str, list[dict]] = {}
    for c in _DRY_RUN_CANDIDATES:
        by_src.setdefault(c["source_id"], []).append({
            "ts": dt.datetime.now().isoformat(timespec="seconds"),
            "source_id": c["source_id"],
            "url": c["url"],
            "anchor": c["texte"][:300],
            "dry_run": True,
        })
    for sid, items in by_src.items():
        ecrire_raw(sid, today_d, items)

    # Z1 — JSONL structuré.
    ecrire_candidates_jsonl(today_d, _DRY_RUN_CANDIDATES)

    # Z2 → Z3.
    resultat = traiter_candidats_pipeline(_DRY_RUN_CANDIDATES, today_d)

    print("\nRésumé dry-run :")
    print(f"  leads actifs       : {resultat['leads_actifs']}")
    print(f"  leads modifiés     : {resultat['leads_modifies']}")
    print(f"  pré-fiches créées  : {resultat['prefiches_creees']}")
    print(f"\nFichiers attendus dans :")
    print(f"  {RAW_DIR}")
    print(f"  {LEADS_DIR}")
    print(f"  {PREFICHES_DIR}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="Pas de requêtes externes ; rejoue depuis Z0 "
                             "(discovery/raw/<source>/*.jsonl) si présent et "
                             "exerce la traversée Z1 → Z2 → Z3.")
    parser.add_argument("--force", action="store_true",
                        help="Ignore la fenêtre de fréquence (scanne toutes "
                             "les sources même si elles ne sont pas dues).")
    args = parser.parse_args()

    if args.dry_run:
        return run_dry()

    cfg = yaml.safe_load((CONFIG / "sources.yml").read_text(encoding="utf-8"))
    sources = cfg.get("sources", [])
    transverse = cfg.get("mots_cles_transverses", [])
    strong_kw = cfg.get("mots_cles_forts", STRONG_KW_DEFAULT)
    DISCOVERY.mkdir(exist_ok=True)

    known_exact, known_domains = known_urls()
    regions, montages = corpus_profile()
    mont_labels = montage_labels()
    faibles_r, faibles_m = blind_spots(regions, montages, mont_labels)
    seen = load_seen()
    ignored = load_ignore()
    freq_log = load_freq_log()
    today_d = dt.date.today()
    today = today_d.isoformat()

    # Fenêtres de fréquence (Z-pipeline) — sources éligibles vs hors fenêtre.
    sources_eligibles: list[dict] = []
    sources_hors_fenetre: list[tuple[str, str]] = []
    for src in sources:
        sid = src.get("id", "?")
        freq = lire_frequence(src)
        src["_frequence_resolue"] = freq
        if args.force or fenetre_autorise_scan(sid, freq, freq_log, today_d):
            sources_eligibles.append(src)
        else:
            sources_hors_fenetre.append((sid, freq))

    # ── 1. moisson des liens, premier filtre sur l'ancre ─────────────────────
    prelim = []          # liens passant le filtre faible sur l'ancre
    seen_links = set()
    sources_sante = []
    raw_buffer: dict[str, list[dict]] = {}  # Z0 — par source
    for src in sources_eligibles:
        sid = src.get("id", "?")
        url = src.get("url")
        if not url:
            continue
        parser_type = src.get("parser", "html_static")

        # Parser dédié — voie F crowdfunding (session #8). Le dispatcher
        # produit directement des items au format Z0 ; on saute la moisson
        # HTML classique pour cette source.
        if parser_type == "crowdfunding":
            print(f"· {sid} — {url}  [{src.get('_frequence_resolue')}] (parser: crowdfunding)")
            try:
                from parsers.crowdfunding import fetch_crowdfunding_source
                items = fetch_crowdfunding_source(src, src.get("options", {}))
            except Exception as exc:
                print(f"  ! parser crowdfunding {sid} : {exc}",
                      file=sys.stderr)
                sources_sante.append((sid, f"parser KO", 0))
                marquer_scan(sid, freq_log, today_d, status="parser KO")
                continue
            n_src = 0
            src_raw: list[dict] = []
            for item in items:
                nu = item.get("url_norm") or norm_url(item.get("url", ""))
                if nu in seen_links:
                    continue
                seen_links.add(nu)
                src_raw.append(item)
                anchor = item.get("anchor", "")
                anchor_score, _ = score_candidate(
                    anchor, src.get("mots_cles", []), transverse, strong_kw)
                if anchor_score >= 1:
                    prelim.append({
                        "link": item.get("url"), "norm": nu,
                        "anchor": anchor[:200],
                        "anchor_score": anchor_score, "src": src,
                    })
                    n_src += 1
            if src_raw:
                raw_buffer[sid] = src_raw
            sources_sante.append((sid, "ok", n_src))
            marquer_scan(sid, freq_log, today_d, status="ok")
            continue

        print(f"· {sid} — {url}  [{src.get('_frequence_resolue')}]")
        html_doc = fetch(url)
        time.sleep(POLITE_DELAY)
        n_src = 0
        if not html_doc:
            sources_sante.append((src.get("id"), "échec", 0))
            marquer_scan(src.get("id"), freq_log, today_d, status="échec")
            continue
        harvester = LinkHarvester()
        try:
            harvester.feed(html_doc)
        except Exception as exc:  # parsing best-effort
            print(f"  ! parsing {url} : {exc}", file=sys.stderr)
            sources_sante.append((src.get("id"), "parsing KO", 0))
            marquer_scan(src.get("id"), freq_log, today_d, status="parsing KO")
            continue
        src_kw = src.get("mots_cles", [])
        src_raw: list[dict] = []
        for href, text in harvester.links:
            link = urljoin(url, href)
            if not link.startswith(("http://", "https://")):
                continue
            nu = norm_url(link)
            if nu in seen_links or len(text) < 8:
                continue
            seen_links.add(nu)
            # Z0 — capture brute : on archive TOUT (avant filtrage),
            # avec un snippet de l'ancre.
            src_raw.append({
                "ts": dt.datetime.now().isoformat(timespec="seconds"),
                "source_id": src.get("id"),
                "url_source": url,
                "url": link,
                "url_norm": nu,
                "anchor": text[:300],
            })
            anchor_score, _ = score_candidate(text, src_kw, transverse, strong_kw)
            # premier filtre faible : on approfondit dès le moindre signal
            if anchor_score >= 1:
                prelim.append({
                    "link": link, "norm": nu, "anchor": text[:200],
                    "anchor_score": anchor_score, "src": src,
                })
                n_src += 1
        if src_raw:
            raw_buffer[src.get("id")] = src_raw
        sources_sante.append((src.get("id"), "ok", n_src))
        marquer_scan(src.get("id"), freq_log, today_d, status="ok")

    # Écriture Z0 — un fichier par source/jour, append.
    for sid, items in raw_buffer.items():
        ecrire_raw(sid, today_d, items)

    # ── 2. approfondissement : analyse de la page candidate (P1) ─────────────
    # priorité aux meilleurs scores d'ancre, plafonné pour garder le run court.
    prelim.sort(key=lambda c: c["anchor_score"], reverse=True)
    candidates = []
    n_ignores = 0
    for c in prelim[:MAX_DEEP_FETCH]:
        src = c["src"]
        page_html = fetch(c["link"])
        time.sleep(POLITE_DELAY)
        page_text = c["anchor"]
        title = ""
        if page_html:
            extractor = TextExtractor()
            try:
                extractor.feed(page_html)
                page_text = c["anchor"] + " " + extractor.text()
                title = re.sub(r"\s+", " ", extractor.title).strip()
            except Exception:
                pass
        score, hits = score_candidate(page_text, src.get("mots_cles", []),
                                      transverse, strong_kw)
        bonus, angles = angle_mort_bonus(page_text, faibles_r, faibles_m,
                                         mont_labels)
        score += bonus
        if score < 3:                       # seuil sur le score enrichi
            continue
        net = urlparse(c["link"]).netloc.lower()
        net = net[4:] if net.startswith("www.") else net
        deja = c["norm"] in known_exact
        # mémoire : nouveauté, récurrence, ou candidat écarté durablement
        mem = seen.get(c["norm"])
        ecarte = c["norm"] in ignored or (mem is not None
                                          and mem.get("statut") == "ignore")
        statut = "ignore" if ecarte else ("revu" if mem else "nouveau")
        # la mémoire suit TOUT — y compris les candidats écartés, pour que le
        # statut « ignore » colle une fois posé.
        prev = seen.get(c["norm"], {})
        seen[c["norm"]] = {
            "premiere_detection": prev.get("premiere_detection", today),
            "derniere_detection": today,
            "dernier_score": score,
            "statut": "ignore" if ecarte else prev.get("statut", "nouveau"),
        }
        if ecarte:                          # écarté : hors des candidats produits
            n_ignores += 1
            continue
        candidates.append({
            "titre_page": title[:200],
            "texte": c["anchor"],
            "url": c["link"],
            "source_id": src.get("id"),
            "categorie_probable": src.get("categorie_probable", []),
            "score": score,
            "mots_cles": hits,
            "angle_mort": angles,
            "fiche_existante": deja,
            "domaine_connu": net in known_domains,
            "statut": statut,
        })

    # tri : score décroissant, nouveautés (jamais vues) et angles morts d'abord
    candidates.sort(
        key=lambda c: (c["statut"] == "nouveau", bool(c["angle_mort"]),
                       not c["fiche_existante"], c["score"]),
        reverse=True)

    save_seen(seen)
    save_freq_log(freq_log)

    # ── 2bis. Pipeline Z2 → Z3 (leads agrégés, pré-fiches) ───────────────────
    pipeline_resultat = traiter_candidats_pipeline(candidates, today_d)

    # ── 3. sorties ───────────────────────────────────────────────────────────
    out_json = DISCOVERY / f"candidats-{today}.json"
    out_md = DISCOVERY / f"candidats-{today}.md"
    out_json.write_text(json.dumps(candidates, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    # Z1 — variante JSONL structurée, consommée par les passes automatiques.
    ecrire_candidates_jsonl(today_d, candidates)

    nouveaux = [c for c in candidates if not c["fiche_existante"]]
    am = [c for c in candidates if c["angle_mort"]]
    lines = [f"# Veille — candidats du {today}", "",
             f"{len(candidates)} candidat·s repéré·s sur "
             f"{len(sources_eligibles)} sources scannées "
             f"({len(sources_hors_fenetre)} hors fenêtre de fréquence, "
             f"{len(sources)} sources au total) — "
             f"{len(nouveaux)} hors fiches existantes, {len(am)} sur un angle "
             f"mort ; {n_ignores} écarté·s via discovery/ignore.txt. Score "
             "pondéré ; à examiner et promouvoir manuellement.", "",
             f"**Pipeline** — {pipeline_resultat['leads_actifs']} leads actifs ; "
             f"{len(pipeline_resultat['leads_modifies'])} leads touchés cette "
             f"passe ; {len(pipeline_resultat['prefiches_creees'])} pré-fiches "
             f"générées (Z2 → Z3, seuil {SEUIL_SCORE_PROMOTION}, "
             f"{NB_INDICES_REQUIS} indices min).", ""]
    if pipeline_resultat["prefiches_creees"]:
        lines.append("### Pré-fiches générées dans cette passe — à arbitrer\n")
        for slug in pipeline_resultat["prefiches_creees"]:
            lines.append(f"- `discovery/prefiches/{slug}.yml`")
        lines.append("")
    if sources_hors_fenetre:
        lines.append(
            f"### Sources hors fenêtre ({len(sources_hors_fenetre)})\n")
        for sid, freq in sources_hors_fenetre:
            lines.append(f"- {sid} — fréquence {freq}")
        lines.append("")
    lines.append(f"## Nouveautés possibles ({len(nouveaux)})\n")
    for c in nouveaux[:60]:
        tag = " · ANGLE MORT" if c["angle_mort"] else ""
        titre = c["titre_page"] or c["texte"]
        lines.append(f"- **[{c['score']}{tag}]** [{titre}]({c['url']}) "
                     f"— source : {c['source_id']} — statut : {c['statut']} — "
                     f"mots-clés : {', '.join(c['mots_cles'])}")
    deja = [c for c in candidates if c["fiche_existante"]]
    if deja:
        lines.append(f"\n## Déjà référencés ({len(deja)})\n")
        for c in deja[:30]:
            lines.append(f"- [{c['score']}] [{c['titre_page'] or c['texte']}]"
                         f"({c['url']}) — {c['source_id']}")
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # rapport d'angles morts — outil de pilotage éditorial (P3)
    am_lines = [f"# Angles morts du corpus — {today}", "",
                "Régions et types de montage absents ou faiblement couverts "
                "(≤ 1 fiche). Les candidats touchant ces dimensions sont "
                "bonifiés au scoring de veille.", "",
                "## Régions sous-représentées\n"]
    for r in faibles_r:
        am_lines.append(f"- {r} — {regions.get(r, 0)} fiche·s")
    am_lines.append("\n## Types de montage sous-représentés\n")
    for m in faibles_m:
        am_lines.append(f"- {mont_labels.get(m, m)} — {montages.get(m, 0)} fiche·s")
    (DISCOVERY / "angles-morts.md").write_text("\n".join(am_lines) + "\n",
                                               encoding="utf-8")

    # santé des sources (P5, version légère)
    ss_lines = [f"# Santé des sources — {today}", "",
                "Par source : état du dernier scan et nombre de liens retenus "
                "pour approfondissement.", ""]
    for sid, etat, n in sources_sante:
        flag = " ⚠" if etat != "ok" else ""
        ss_lines.append(f"- {sid} — {etat}{flag} — {n} lien·s pré-retenu·s")
    (DISCOVERY / "sources-sante.md").write_text("\n".join(ss_lines) + "\n",
                                                encoding="utf-8")

    # index consolidé (P6)
    (DISCOVERY / "index.md").write_text(
        f"# Veille — index\n\nDerniere passe : {today}\n\n"
        f"- [Candidats du {today}](candidats-{today}.md)\n"
        f"- [Angles morts du corpus](angles-morts.md)\n"
        f"- [Santé des sources](sources-sante.md)\n"
        f"- [Pipeline — spec et conventions](PIPELINE.md)\n"
        f"\nPipeline en cours : "
        f"{pipeline_resultat['leads_actifs']} leads actifs ; "
        f"{len(pipeline_resultat['prefiches_creees'])} pré-fiches générées "
        f"aujourd'hui.\n",
        encoding="utf-8")

    print(f"\nVeille terminée : {len(candidates)} candidats "
          f"({len(nouveaux)} hors fiches, {len(am)} sur angle mort, "
          f"{n_ignores} écartés).")
    print(f"Pipeline : {pipeline_resultat['leads_actifs']} leads actifs · "
          f"{len(pipeline_resultat['leads_modifies'])} leads touchés · "
          f"{len(pipeline_resultat['prefiches_creees'])} pré-fiches créées.")
    print(f"→ {out_md}")


if __name__ == "__main__":
    main()
