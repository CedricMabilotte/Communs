---
name: communs-veille-valider
description: Passe Checker MARS-prod de validation d'une fiche ou d'un lot du corpus Communs — traque cotation fabriquée, chaîne cassée, désync factuelle, écart de schéma. Usage : /communs-veille-valider <slug|lot>
argument-hint: <slug | "lieux" | "porteurs" | "all">
allowed-tools: [Bash, Read, Grep, WebSearch, mcp__workspace__web_fetch]
---
# communs-veille-valider — Validation adversariale (Checker MARS-prod)

Étape 6 (transversale). Relit une fiche ou un lot **en cherchant la faille**
(chapeau Checker). Ne modifie rien : produit un rapport d'objections classées
**bloquantes / mineures / RAS**. Pour de gros lots : partitionner en sous-agents
disjoints, intégration centralisée.

## Ce qu'on traque
1. **Cotation fabriquée** : tout `oui`/`non` dans `grille:` dont la `note:` ne
   justifie pas par un fait sourcé — surtout sur milieu_protege, vivant_finalite,
   place_au_vivant, usage_non_degradant, travail_non_marchandise, inalienabilite,
   irreversibilite. Au moindre doute → devrait être `inconnu`.
2. **Chaîne / garde-fous** : `articulations[].usufruitier` ⊆ `chaine.usufruitiers` ;
   uid de chaîne existants ; pas de doublon d'uid ; `titre`/`nature_interet` dans
   le canon (`config/concepts.yml`) ; `integre` réservé au cas entité-unique.
3. **Désync factuelle** : verdict/Indice/palier d'une prose qui contredit la fiche
   live (cf. cas Pommiers) ; libellés faux (forme juridique présumée vs registre,
   cf. SCIC/SCOP→SAS de Chirols) ; SIREN/RNA erronés (vérifier au registre) ;
   entités HTML brutes.
4. **Réserves honnêtes** : un lieu fragile (achat non prouvé, résidence non
   confirmée) ne doit PAS afficher de `oui` sur le sol/usage non établis ; réserves
   présentes en `fiabilite`.
5. **Schéma** : écarts par rapport au modèle (blocs manquants, clés inventées).

## Méthode
Vérifier ce qui est vérifiable (grep, comptage oui/non/inconnu, recoupement
registre). Ne pas faire confiance aux notes — juger si la note JUSTIFIE la valeur.
Régénérer et lire les garde-fous. Pour les faits, WebSearch→web_fetch (provenance).

## Sortie
Rapport d'objections (bloquante/mineure/RAS) : fiche · critère · problème · preuve
· correction suggérée. Les corrections sont appliquées par les skills d'édition,
pas ici.

## Contrôles ajoutés — passe 1 corpus (méthode améliorée, 2026-06-01)
La 1re passe a montré que les contrôles « cotation » et « entités HTML » ne
suffisent pas. Ajouter systématiquement :
1. **Complétude de la chaîne** : greper dans les `note:`/`description` les formes
   de structures (EARL, GAEC, SAS, SCI, SCIC, SCOP, fondation, fonds de dotation,
   commune, foncière) et recouper avec `chaine`/`articulations` — un maillon
   décisif cité en prose mais absent de la chaîne fausse le verdict (cas
   Villarceaux : EARL exploitante manquante).
2. **Articulations présentes sur tout montage dissocié** (`demembrement`,
   `propriete_protegee`, `propriete_publique`) : un montage dissocié sans bloc
   `articulations` est une anomalie (cas Flocques).
3. **Rôles ↔ prose** : qui *possède* (porteur) vs qui *use* (usufruitier) doit
   correspondre à la prose — vérifier les inversions (cas Flocques : commune
   propriétaire rangée en usufruitier).
4. **Cohérence pôle (`integrite_montage.niveau`) ↔ `nature_interet`/verdict** :
   pas de `commun_citoyen`/`mutualisme` sur une chaîne `inconnu` ou
   `privee_individuelle`. (Manque structurel : il faudrait une table
   `nature_interet → pôles admissibles` dans `config/`, contrôlée au générateur.)
5. **Intégrité référentielle du graphe** : tout uid cité (`chaine`, `membres`,
   `voir_aussi`) existe ; `membres:` d'un réseau ne mélange pas doublons
   lieu+porteur du même site ; signaler les orphelins (entité citée par personne).
6. **note ↔ valeur** : une `note:` qui dit « non lucrative » sous une `valeur`
   `partiel`/`oui` d'un maillon `commerciale_encadree` est une incohérence.
7. **uid trompeur** : un uid encodant une forme fausse (`scic-…` pour une SAS,
   `fonciere-…` pour un fonds de dotation) est cosmétique mais à signaler.
