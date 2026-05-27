# Pipeline de veille à zones — Z0 → Z3

Ce document décrit le pipeline de qualification progressive des candidats
issus de la veille (`scripts/watch.py` + `scripts/pipeline.py`). Le but
est de **séparer la moisson brute de la qualification éditoriale** :
un candidat repéré une fois sans suite ne pollue pas l'inventaire ; un
candidat vu plusieurs fois et structurellement étayé monte
automatiquement d'étage, jusqu'au stade « pré-fiche » qui appelle un
arbitrage humain.

La promotion finale Z3 → Z4 (pré-fiche → fiche dans `lieux/`) reste
**strictement manuelle** : le code n'écrit jamais dans `lieux/`,
`porteurs/`, `usufruitiers/`, `reseaux/`, `modeles/`.

---

## Vue d'ensemble

```
              moisson web
                  │
                  ▼
   Z0 — discovery/raw/<source>/YYYY-MM-DD.jsonl
        (capture brute, archive intégrale)
                  │   scoring pondéré + anti-bruit
                  ▼
   Z1 — discovery/candidats-YYYY-MM-DD.{md,json}
        discovery/candidates-YYYY-MM-DD.jsonl
        (candidats scorés, regardés une passe à la fois)
                  │   détection d'indices structurels
                  ▼   + fusion par slug
   Z2 — discovery/leads/<slug>.md
        (un lead par lieu pressenti, agrégé dans le temps)
                  │   critères de promotion
                  ▼   (cf. § Seuils)
   Z3 — discovery/prefiches/<slug>.yml
        (schéma 1bis partiellement rempli)
                  │   ARBITRAGE MANUEL
                  ▼
   Z4 — lieux/<slug>.yml   (hors-pipeline, à la main)
```

---

## Convention de fréquence par source

Chaque source de `config/sources.yml` peut porter un champ `frequence:`
parmi quatre valeurs reconnues :

| Valeur            | Délai minimum entre deux scans automatiques |
|-------------------|--------------------------------------------|
| `hebdomadaire`    | 7 jours (valeur par défaut)                |
| `mensuelle`       | 30 jours                                    |
| `trimestrielle`   | 90 jours                                    |
| `sur_demande`     | jamais (scan manuel via `--force`)         |

Le champ est **tolérant** : si absent ou invalide, la veille retombe sur
`hebdomadaire`. Pour l'ajouter à une source, modifier `config/sources.yml` :

```yaml
- id: ma-source
  url: "https://example.org/"
  frequence: mensuelle        # ← ajouter cette ligne
  mots_cles: [foncier, …]
```

L'historique des passes est tenu dans `discovery/_freq.json` (un dict
`<source_id> → {dernier_scan, dernier_statut}`). Pour forcer un scan
même si la fenêtre n'est pas écoulée : `python3 scripts/watch.py --force`.

---

## Zones — formats et critères

### Z0 — Capture brute

**Emplacement** : `discovery/raw/<source_id>/YYYY-MM-DD.jsonl`.

Une ligne JSON par item capturé. Mode **append** : plusieurs runs dans
la même journée s'accumulent dans le même fichier. Schéma d'une ligne :

```json
{
  "ts": "2026-05-27T13:42:11",
  "source_id": "terre-de-liens",
  "url_source": "https://terredeliens.org/",
  "url": "https://terredeliens.org/national/transmettre-des-terres/",
  "url_norm": "terredeliens.org/national/transmettre-des-terres",
  "anchor": "Transmettre des terres — Terre de Liens"
}
```

Rôle : audit (qu'est-ce que la veille a vraiment vu ?) et possibilité de
**rejouer** un scoring sur l'archive sans refaire les requêtes.

### Z1 — Candidats scorés

**Emplacement** : `discovery/candidats-YYYY-MM-DD.md` (rétrocompatible,
lisible par l'humain) + `discovery/candidats-YYYY-MM-DD.json` +
`discovery/candidates-YYYY-MM-DD.jsonl` (structuré, consommé par les
passes automatiques).

Le scoring est inchangé par rapport à la version précédente (pondéré
par mot-clé + bonus angle mort - signaux négatifs anti-bruit). Le seuil
de production reste **score ≥ 3** après enrichissement.

### Z2 — Leads agrégés

**Emplacement** : `discovery/leads/<slug>.md`.

Un fichier Markdown par **lieu pressenti**, avec frontmatter YAML. Le
slug est forgé à partir du nom du lieu détecté (cf. `slugify` dans
`scripts/pipeline.py`).

```yaml
---
slug: ferme-de-la-coccinelle
nom: Ferme de la Coccinelle
cree: 2026-05-23
dernier_repere: 2026-05-27
score_cumule: 27
sources_vues:
  - source: terre-de-liens
    date: 2026-05-23
    url: https://fermes.terredeliens.org/alsace/.../ferme-de-la-coccinelle/
    titre: "Ferme de la Coccinelle — Terre de Liens"
    score: 14
  - source: terre-de-liens
    date: 2026-05-27
    url: https://terredeliens.org/national/actu/…
    titre: "Campagne de don pour la Ferme de la Coccinelle"
    score: 13
indices_structurels:
  nom_propre: true
  localisation: true
  entite_juridique: true
  montage_explicite: false
  siren: false
  geoportail_localisable: true
extracted:
  nom: "Ferme de la Coccinelle"
  localisation:
    region: "Grand Est"
    departement: "Bas-Rhin"
  formes: [association, fondation, bail_rural]
statut: actif
---

# Lead — Ferme de la Coccinelle

Notes libres pour qualification manuelle…
```

**Mécanique de fusion** :

- recherche d'un lead existant par slug normalisé (sans accents, sans
  articles, en kebab-case) ;
- si trouvé : ajout de la source à `sources_vues` (si l'URL n'y est pas
  déjà), mise à jour de `dernier_repere`, incrément de `score_cumule` ;
- les indices structurels acquis ne sont jamais perdus (OR booléen) ;
- les listes de `extracted` (formes juridiques, sirens) fusionnent ;
  les dicts (localisation) prennent la première valeur non vide.

### Z3 — Pré-fiches

**Emplacement** : `discovery/prefiches/<slug>.yml`.

Schéma 1bis partiellement rempli à partir d'un lead promu. Le fichier
contient explicitement un pointeur `_source_lead:` vers le lead qui l'a
généré, pour traçabilité.

```yaml
categorie: lieu
slug: ferme-de-la-coccinelle
nom: "Ferme de la Coccinelle"
statut_fiche: prefiche
_source_lead: discovery/leads/ferme-de-la-coccinelle.md
_genere_le: 2026-05-27
_score_cumule: 27
_indices_structurels:
  nom_propre: true
  localisation: true
  entite_juridique: true
  …
localisation:
  commune: null
  departement: "Bas-Rhin"
  region: "Grand Est"
montage:
  type: null            # à arbitrer
  articulations: []
chaine:
  porteurs:    [_a_qualifier_fondation, _a_qualifier_fonds_dotation]
  usufruitiers: [_a_qualifier_association]
sources_veille:
  - source: terre-de-liens
    url: https://fermes.terredeliens.org/.../ferme-de-la-coccinelle/
    date: 2026-05-23
    score: 14
note_genese: "Premier signal détecté par la veille via la source `terre-de-liens`."
```

Les chaînes `_a_qualifier_<forme>` sont délibérément non valides comme
identifiants : elles **doivent** être réécrites à la main lors de la
promotion Z3 → Z4 (qui restera manuelle).

---

## Seuils de promotion (Z2 → Z3)

Un lead est promu en pré-fiche automatiquement si **les deux conditions
sont vraies** :

1. **Au moins 2 des 3 indices structurels** suivants sont à `true` :
   - `nom_propre` (nom de lieu reconnaissable) ;
   - `localisation` (région ou département détecté) ;
   - `entite_juridique` (au moins une forme juridique attendue).
2. **Score cumulé** ≥ **25**.

Ces deux constantes sont exposées dans `scripts/pipeline.py` :
`SEUIL_SCORE_PROMOTION` et `NB_INDICES_REQUIS`. Justification du seuil
de 25 : c'est environ 2 à 3 passes positives à score pondéré
10-12 — l'historique des candidats récents (voir
`discovery/candidats-2026-05-26.md`) montre que la plupart des
candidats à fort score atteignent ce seuil au bout de 2 semaines de
récurrence, ce qui filtre les signaux isolés sans étouffer ceux qui
reviennent.

Pour ajuster : modifier les deux constantes dans `pipeline.py` ; le
nouveau seuil prend effet à la passe suivante (ne ré-évalue pas les
leads déjà promus).

---

## Cycle de vie d'un lead

```
        première détection
              │
              ▼
        statut: actif  ◀────┐
              │              │ nouvelles passes — enrichissement
              ▼              │
        critère promo OK ────┘
              │
              ▼
        statut: pre_fiche  (pré-fiche écrite dans Z3)
              │
              ▼  arbitrage humain
        ┌──────────┐
        │          │
        ▼          ▼
   statut: promu   statut: rejete
   (la fiche       (le lead reste,
   existe dans     la pré-fiche peut
   lieux/)         être supprimée)
```

**Statuts possibles** dans le frontmatter d'un lead :

| Statut       | Sens                                                       |
|--------------|------------------------------------------------------------|
| `actif`      | défaut — lead en cours d'enrichissement                    |
| `pre_fiche`  | a déjà généré une pré-fiche en Z3, en attente d'arbitrage  |
| `promu`      | arbitré et passé en `lieux/` (à poser à la main)           |
| `rejete`     | arbitré et écarté (à poser à la main)                      |

Un lead en statut `pre_fiche`, `promu` ou `rejete` **n'est plus
re-promu** automatiquement, même si son score continue de monter.

---

## Fichiers à ignorer / convention

- `discovery/raw/.gitkeep`, `discovery/leads/.gitkeep`,
  `discovery/prefiches/.gitkeep` : marqueurs de présence du dossier dans
  le repo (les dossiers nus ne se commitent pas en git).
- `discovery/_seen.json` : mémoire des URLs vues (cf. P4) — automatique.
- `discovery/_freq.json` : historique des scans par fréquence —
  automatique.
- `discovery/ignore.txt` : URLs durablement écartées, **tenu à la
  main** (une URL par ligne, `#` pour les commentaires).

---

## Mode `--dry-run`

`python3 scripts/watch.py --dry-run` exerce la traversée Z1 → Z2 → Z3
sur des candidats synthétiques **sans aucune requête réseau**. Sert à
vérifier le format des leads et des pré-fiches après une modification
du pipeline. Les fichiers générés (raw + leads + pré-fiches) sont
écrits aux mêmes emplacements que les passes réelles — penser à les
nettoyer si nécessaire avant un commit.

---

## Décisions et points de vigilance

- **Conservation de la rétrocompatibilité** : `candidats-YYYY-MM-DD.{md,json}`
  restent produits à l'identique. Le JSONL est un **complément**.
- **Slugification** : suffisamment large pour fusionner « Ferme de la
  Coccinelle » et « Ferme de la Coccinelle — Terre de Liens » (qui
  partagent les mots significatifs après nettoyage des articles). Mais
  deux lieux distincts portant le même nom seraient fusionnés à tort :
  un déballonnage manuel est attendu lors de la promotion Z3 → Z4.
- **Détection d'indices** : heuristique, pas exhaustive. Un faux négatif
  sur `nom_propre` reporte la promotion ; un faux positif n'enclenche
  rien sans le score cumulé.
- **Seuil de promotion** : la première fois qu'on tournera sur l'archive
  réelle, il faudra observer combien de leads passent et ajuster.
  L'historique cumulé de mai 2026 suggère que `terre-de-liens` produit
  des leads très étoffés qui franchiront vite le seuil — c'est attendu.
