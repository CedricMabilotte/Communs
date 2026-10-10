#!/usr/bin/env python3
"""Export transverse de la section Enjeux vers l'agora (session #12).

Deux exports, pour que les autres projets (wikomons, libres, communautes,
biblio) partagent ce que les études ont établi :

1. Références — `resources/shared/references/foncier-agricole.yaml` :
   sources citées par les études (dédoublonnées, typées, avec les études qui
   les citent) et ouvrages de fond par auteur·ice. Source unique : le
   front-matter des études (`enjeux/etudes/*.md`). Le fichier exporté est
   régénéré à chaque passage — ne pas l'éditer à la main.

2. Glossaire — `resources/shared/concepts/glossaire-commun.yaml` : ajoute
   les termes de `config/concepts.yml#glossaire` absents du glossaire commun
   (comparaison insensible à la casse et aux accents), avec
   `statut: en discussion` et `projets: [Projet Communs]`. N'écrase jamais
   une définition existante ; les écarts sont listés à l'écran.

Usage : python3 scripts/export_enjeux_transverse.py [--agora CHEMIN] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
AGORA = Path.home() / "Documents/Ced_Cabinet/Activities/agents"


def _fm(path):
    t = path.read_text(encoding="utf-8")
    if t.startswith("---"):
        end = t.find("\n---", 3)
        return yaml.safe_load(t[3:end]) or {}
    return {}


def _norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def etudes():
    out = []
    for p in sorted((ROOT / "enjeux" / "etudes").glob("*.md")):
        m = _fm(p)
        n = int(m.get("numero") or 0)
        out.append((f"E{n:02d}", f"{n:02d}-{m.get('slug')}", m))
    return out


def export_references(agora, dry):
    sources, ouvrages = {}, {}
    for code, url, m in etudes():
        for s in m.get("sources") or []:
            if not isinstance(s, dict):
                continue
            key = s.get("url") or _norm(s.get("titre", ""))
            ent = sources.setdefault(key, {
                "type": s.get("type"), "auteur": s.get("auteur"),
                "titre": s.get("titre"), "annee": s.get("annee"),
                "url": s.get("url"), "etudes": []})
            if code not in ent["etudes"]:
                ent["etudes"].append(code)
        for o in m.get("ouvrages") or []:
            if not isinstance(o, dict):
                continue
            key = (_norm(o.get("auteur", "")), _norm(o.get("titre", "")))
            ent = ouvrages.setdefault(key, {
                "auteur": o.get("auteur"), "titre": o.get("titre"),
                "annee": o.get("annee"), "editeur": o.get("editeur"),
                "etudes": []})
            if code not in ent["etudes"]:
                ent["etudes"].append(code)
    doc = {
        "version": 1,
        "description": ("Références du foncier agricole et des communs fonciers "
                        "en France — sources citées par les analyses « Enjeux » "
                        "de communs.actitude.org et ouvrages de fond. Partagé "
                        "avec wikomons, libres, communautes, biblio."),
        "genere_par": "Communs/scripts/export_enjeux_transverse.py — ne pas éditer à la main",
        "source_unique": "Communs/enjeux/etudes/*.md (front-matter sources: et ouvrages:)",
        "regle_sources": ("Sources officielles, recherche, académiques, presse "
                          "d'enquête ; opérateurs (SAFER, chambres) signalés ; "
                          "ONG françaises exclues comme sources."),
        "mis_a_jour": datetime.date.today().isoformat(),
        "etudes_url": "https://communs.actitude.org/enjeux/",
        "ouvrages": sorted(ouvrages.values(), key=lambda o: (_norm(o["auteur"] or ""), o.get("annee") or 0)),
        "sources": sorted(sources.values(), key=lambda s: (s.get("type") or "", _norm(s.get("auteur") or ""))),
    }
    dest = agora / "resources/shared/references/foncier-agricole.yaml"
    print(f"Références : {len(sources)} sources, {len(ouvrages)} ouvrages → {dest}")
    if not dry:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
                        encoding="utf-8")


def export_glossaire(agora, dry):
    cfg = yaml.safe_load((ROOT / "config/concepts.yml").read_text(encoding="utf-8"))
    termes = [g for g in (cfg.get("glossaire") or []) if isinstance(g, dict)]
    dest = agora / "resources/shared/concepts/glossaire-commun.yaml"
    gc = yaml.safe_load(dest.read_text(encoding="utf-8"))
    deja = {_norm(c.get("terme", "")): c for c in gc.get("concepts", [])}
    for c in gc.get("concepts", []):
        for a in c.get("alias") or []:
            deja.setdefault(_norm(a), c)
    ajouts, ecarts = [], []
    for g in termes:
        k = _norm(g["terme"])
        if k in deja:
            ecarts.append(g["terme"])
            continue
        ajouts.append({
            "terme": g["terme"], "definition": g.get("definition", ""),
            "registre": g.get("registre", "juridique"),
            "statut": "en discussion", "projets": ["Projet Communs"],
            "source": "communs.actitude.org/enjeux — " + ", ".join(g.get("etudes") or []),
            "fiche": "https://communs.actitude.org/glossaire.html#g-" + re.sub(r"\s+", "-", _norm(g["terme"])),
        })
    print(f"Glossaire commun : {len(ajouts)} terme(s) ajouté(s), "
          f"{len(ecarts)} déjà présent(s) (définition commune conservée) : "
          + ", ".join(ecarts))
    if ajouts and not dry:
        gc.setdefault("concepts", []).extend(ajouts)
        gc["updated"] = datetime.date.today().isoformat()
        dest.write_text(yaml.safe_dump(gc, allow_unicode=True, sort_keys=False, width=120),
                        encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--agora", type=Path, default=AGORA)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    export_references(a.agora, a.dry_run)
    export_glossaire(a.agora, a.dry_run)
