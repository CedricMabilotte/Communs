---
name: communs-veille-prefiche
description: Promeut un lead qualifié Communs en pré-fiche Z3 (schéma 1bis partiel). Usage : /communs-veille-prefiche <slug>
argument-hint: <slug>
allowed-tools: [Bash, Read, Write, Edit]
---
# communs-veille-prefiche — Promotion Z2 → Z3

Étape 3 (cf. `discovery/PIPELINE.md`). Écrit `discovery/prefiches/<slug>.yml` à
partir d'un lead qualifié « dans le périmètre » (ou retenu par l'opérateur malgré
une réserve — alors documenter la réserve). N'écrit pas dans `lieux/` (→ carver).

## Schéma (modèle : `discovery/prefiches/terre-liens.yml`)
```yaml
categorie: lieu
slug: <slug>
nom: "<nom>"
statut_fiche: prefiche
_source_lead: discovery/leads/<slug>.md
_genere_le: 'AAAA-MM-JJ'
_indices_structurels: {...}
_reserve_eligibilite: >   # si lead hors-périmètre mais retenu par l'opérateur
localisation: {commune, departement, region, code_postal}
entites_pressenties: [{nom, forme, siren, role}]
montage: {type: <silhouette ou null si à arbitrer>, articulations: []}
chaine: {porteurs: [_a_qualifier_<forme>], usufruitiers: [_a_qualifier_<forme>]}
sources_veille: [...]
note_genese: >
```
- Les `_a_qualifier_<forme>` sont **volontairement invalides** : ils DOIVENT être
  réécrits à la main au carvage Z3→Z4.
- Passer le `statut:` du lead à `pre_fiche`.
- Conserver les réserves « à confirmer » ; ne rien fabriquer.
