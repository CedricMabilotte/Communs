---
name: communs-veille-lead
description: Crée ou normalise un lead de veille Communs (Z2) à partir d'un nom de lieu ou d'une graine opérateur. Usage : /communs-veille-lead <nom-ou-slug>
argument-hint: <nom-ou-slug>
allowed-tools: [Bash, Read, Write, Edit, WebSearch]
---
# communs-veille-lead — Amorcer un lead (Z2)

Étape 1 du pipeline (cf. `discovery/PIPELINE.md`). Crée `discovery/leads/<slug>.md`
pour un lieu pressenti (graine opérateur, rebond, ou détection veille). Ne qualifie
pas (→ `/communs-veille-qualifier`).

## Schéma du lead (frontmatter YAML + corps)
```yaml
---
slug: <kebab-case>
nom: "<nom du lieu>"
cree: 'AAAA-MM-JJ'
dernier_repere: 'AAAA-MM-JJ'
score_cumule: 0
sources_vues: []          # source/date/url/titre/score si déjà repérées
indices_structurels: {nom_propre: true, localisation: false, entite_juridique: false,
  montage_explicite: false, siren: false, geoportail_localisable: false}
extracted: {nom: "<nom>"}  # + localisation si connue
origine: "graine-operateur-AAAA-MM-JJ" | "rebond" | "veille-<source>"
statut: actif
---
# Lead — <nom>
## À instruire
<contexte minimal ; ce qu'il reste à rechercher : entité juridique, localisation,
montage foncier, éligibilité>
```

## Règles
- **Aucune invention** : une piste non vérifiée est marquée « à confirmer ».
- Slug en kebab-case ; vérifier qu'il n'existe pas déjà (`ls discovery/leads/`).
- Si plusieurs lieux d'un même réseau/écosystème : un lead par lieu, et une note
  d'arbitrage commune si utile (`discovery/leads-arbitrage-<lot>.md`).
