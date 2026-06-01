# Validation du corpus — Passe 1 (synthèse)
*4 Checkers parallèles (lecture seule), 1er juin 2026. Rapports détaillés :
`pass1-lieux-a-l.md`, `pass1-lieux-m-z.md`, `pass1-porteurs-reseaux.md`,
`pass1-usufruitiers.md`.*

## Bloquantes (6) — corpus à corriger
1. **logements-chenelet-flocques** : bloc `articulations` absent (bail
   emphytéotique 99 ans non structuré) ; rôles porteur/usufruitier inversés
   (commune propriétaire rangée en usufruitier, Foncière Chênelet en porteur).
2. **villarceaux** : l'EARL du Chemin Neuf (maillon exploitant qui *fait* le
   verdict) est citée en prose mais absente de `chaine`/`articulations`/entités →
   verdict faux ; + note contradictoire (société commerciale vs civile).
3. **coop-du-tilleul** (usufruitier) : en-tête « Association loi 1901 » contredit
   par le corps (forme non confirmée) — forme fabriquée.
4. **exploitation-loiseliere** (usufruitier) : pôle `mutualisme` sur une
   exploitation `privee_individuelle` à exploitant unique.
*(2 et 1 affectent un verdict calculé — priorité haute.)*

## Récurrences (mineures, systémiques)
- Pôle `integrite_montage.niveau` mal calibré vs nature de la chaîne (GAEC
  répartis mutualisme/ig_institue sans critère ; TDL fermiers individuels
  divergents). → manque d'une table `nature_interet → pôles admissibles`.
- `reseaux/clip.yml` `membres:` mélange lieux + porteurs → chaque site compté
  deux fois.
- Orphelins de graphe : terre-de-liens-auvergne, terre-de-liens-pays-de-la-loire,
  lurzaindia-sca.
- uid encodant une forme fausse : `scic-moulinage-de-chirols` (SAS),
  `fonciere-antidote` (fonds de dotation).
- Oasis Coq à l'Âme : `propriete_collective` vs `propriete_protegee` (bail).
- Cotations dont la note contredit la valeur (Champs des Possibles).

## Acquis
Aucun `oui`/`non` fabriqué sur les axes sensibles (vivant/usage) ; `inconnu` posé
honnêtement partout ; pas d'entité HTML brute ; SIREN/RNA plausibles ; **désync
Pommiers résolue** (article et fiche = hybride 65) ; SCIC habitat (Coq à l'Âme,
Keruzerh) confirmées au registre ; Chirols SAS≠SCOP corrigée.

## Amélioration de méthode (passe 1 → 2)
7 contrôles ajoutés au skill `communs-veille-valider` (complétude de chaîne par
grep des formes ; articulations sur montage dissocié ; rôles↔prose ; cohérence
pôle↔nature ; intégrité référentielle du graphe ; note↔valeur ; uid trompeur).
**Passe 2** : appliquer ces contrôles, corriger les 6 bloquantes, et envisager
un garde-fou générateur d'intégrité référentielle + table nature→pôle.
