# Validation corpus #11 — Passe 1 — Usufruitiers (46 fiches)

Checker MARS-prod, lecture seule. Contrôles : cotation `oui`/`non` fabriquée
dans `grille:` (note qui ne justifie pas la valeur) ; `nature_interet` cohérent
et sourcé ; forme juridique présumée vs réelle ; SIREN/RNA plausibles ; entités
HTML brutes ; cohérence avec les lieux qui les citent en `chaine.usufruitiers`.

Référentiels : `config/grilles.yml` (grille `usufruitier`), `config/concepts.yml`
(`nature_interet`, `montages`, pôles `integrite_montage`).

---

## Bloquantes

### B1 — `coop-du-tilleul` · forme juridique fabriquée (en-tête vs corps)
- **Critère** : forme juridique présumée vs réelle.
- **Problème** : l'en-tête affirme `forme_juridique: "Association loi 1901"`,
  alors que tout le corps de la fiche dit l'inverse. `personne_morale_civile:
  partiel` note « sa forme juridique précise (association ou société coopérative)
  n'est pas confirmée par les sources » ; `parts_non_cessibles: partiel` note
  « sa forme juridique exacte n'est pas confirmée » ; `pieces.statuts.note` :
  « Forme juridique exacte de la Coop du Tilleul non confirmée » ; `fiabilite`
  liste en non-confirmé « forme juridique précise de la Coop du Tilleul ».
- **Preuve** : l. 6 (`forme_juridique`) contre l. 49, 55, 119, 131.
- **Correction** : remplacer l'en-tête par une forme non affirmée, p. ex.
  `"Collectif d'usage (forme juridique non confirmée)"`, sur le modèle de
  `collectif-aubascule` / `exploitation-loiseliere` (`forme_juridique: null`).
  Le nom « Coop » dans l'intitulé n'autorise pas à trancher « association ».

### B2 — `exploitation-loiseliere` · `integrite_montage.niveau: mutualisme` incohérent avec une exploitation privée individuelle
- **Critère** : cohérence pôle / `nature_interet`.
- **Problème** : `nature_interet: privee_individuelle` (exploitant unique, forme
  juridique inconnue), mais le pôle est `mutualisme`. Le mutualisme (concepts.yml,
  rang 3) est le pôle d'une société de sociétaires (SCIC, coopérative) au bénéfice
  fermé — il suppose un collectif. Une exploitation a priori individuelle, dont
  la fiche elle-même note « exploitation a priori individuelle, sans gouvernance
  collective » et `une_voix: inconnu`, ne peut relever du mutualisme. Le commentaire
  de `integrite_montage` ne mentionne d'ailleurs aucun trait mutualiste : il décrit
  un exploitant individuel.
- **Preuve** : l. 7 (`privee_individuelle`) vs l. 42 (`niveau: mutualisme`) et
  l. 105 (fragilité « exploitation a priori individuelle »).
- **Correction** : aligner sur le pôle d'une propriété privée individuelle
  (`economie_marchande` ou `propriete_marchande` selon la lecture retenue pour les
  fermiers privés), ou au minimum sur `ig_institue` comme le fiche-sœur
  `exploitation-maraichere-la-chaudeau` (même `nature_interet: privee_individuelle`,
  pôle `ig_institue`). En l'état, deux fermiers individuels Terre de Liens reçoivent
  deux pôles différents (Chaudeau `ig_institue`, Oiselière `mutualisme`) : à trancher
  de façon homogène.

---

## Mineures

### M1 — `champs-des-possibles` · `personne_morale_civile: oui` en tension avec `nature_interet: commerciale_encadree`
- **Critère** : cotation `oui` fabriquée + cohérence avec la grille.
- **Problème** : `nature_interet: commerciale_encadree` (société anonyme
  coopérative, SCIC), mais `personne_morale_civile: oui` avec note « personne
  morale non lucrative ». La grille `usufruitier` définit ce critère ainsi : une
  SCIC se note **« partiel »** (« société commerciale, mais à lucrativité
  encadrée »). Toutes les autres SCIC du corpus (Domaine des Éveils, E3P,
  Semeurs de Graines, Keruzerh, Village Vertical) sont à juste titre notées
  `partiel` ; Champs des Possibles est le seul `oui`, et sa note le qualifie
  même de « non lucrative », ce que `commerciale_encadree` contredit.
- **Preuve** : `champs-des-possibles.yml` l. 8 + l. 38-40 vs `grilles.yml`
  l. 284-292 et la cotation des cinq autres coopératives du corpus.
- **Correction** : passer `personne_morale_civile` à `partiel` et reformuler la
  note (société coopérative à lucrativité encadrée).

### M2 — `champs-des-possibles` · `non_lucrativite_effective: partiel` avec note qui dit « non lucrative »
- **Critère** : note qui ne justifie pas la valeur.
- **Problème** : ailleurs (`personne_morale_civile`, `resume`) la fiche affirme
  le caractère « non lucratif » ; le critère `non_lucrativite_effective` est
  pourtant `partiel`. Incohérence interne sur la nature lucrative de la même
  entité. (Le `partiel` est correct ; c'est l'affirmation « non lucrative »
  ailleurs qui doit être retirée — voir M1.)
- **Preuve** : l. 40 (« personne morale non lucrative ») vs l. 44-46.

### M3 — `sctl` · `nature_interet: inconnu` discutable pour une structure ancienne et documentée
- **Critère** : `nature_interet` cohérent et sourcé.
- **Problème** : la SCTL est une société civile en activité depuis 1985, dont les
  associés sont les utilisateurs des terres et qui attribue l'usage par baux
  ruraux. `inconnu` (concepts.yml : « statuts non publiés, forme juridique
  ambiguë ») se justifie faute de statuts publiés, mais la fiche en sait assez
  (office foncier, associés = usagers, foncier de l'État) pour viser plutôt
  `commerciale_encadree` ou une catégorie d'exploitation/office. À noter : la
  note `non_lucrativite_effective: partiel` présuppose déjà un caractère
  sociétaire — ce qui cadre mal avec `inconnu`.
- **Preuve** : `sctl.yml` l. 7 vs corps l. 16-18, 42-44.
- **Correction** : soit assumer `inconnu` (statuts non publiés) et l'expliciter
  dans le commentaire, soit reclasser ; harmoniser avec `gfa-mutuels` et
  `societe-civile-bigotiere`, également `inconnu` pour des sociétés civiles.

### M4 — `gfa-mutuels` · `parts_non_cessibles: non` ferme sur une fiche « générique »
- **Critère** : cotation `non` fabriquée.
- **Problème** : la fiche est explicitement générique (« les statuts varient d'un
  GFA à l'autre », l. 111). La note du critère reconnaît elle-même que « le GFA
  mutuel ou solidaire peut les encadrer statutairement ». Coter `non` ferme (parts
  librement cessibles) sur une forme dont la fiche dit qu'elle peut verrouiller la
  cession est un jugement plus tranché que les sources ne le permettent — `partiel`
  serait plus prudent et cohérent avec `non_appropriation: partiel` juste au-dessus.
- **Preuve** : `gfa-mutuels.yml` l. 57-59 vs l. 54-56 et l. 111.
- **Correction** : `partiel` + note rappelant la variabilité statutaire, OU
  conserver `non` mais justifier que le défaut légal (cessibilité) prime tant
  qu'aucun verrou n'est documenté (à expliciter).

### M5 — `assemblee-des-usages-nddl` · `parts_non_cessibles: oui` et `non_appropriation: oui` sur un collectif sans personnalité juridique
- **Critère** : note qui ne justifie pas la valeur.
- **Problème** : la fiche décrit un « collectif sans personnalité juridique
  propre » qui ne porte aucun titre en son nom (`personne_morale_civile: partiel`,
  `devolution: inconnu` car « la question ne se pose pas »). Coter `oui` deux
  critères de verrouillage (parts non cessibles, non-appropriation) au motif
  qu'il n'y a « aucun titre cessible » revient à transformer une absence de
  structure en force : la non-existence de parts n'est pas un verrou anti-spéculatif,
  c'est une absence d'objet. Cohérence interne à revoir avec `devolution: inconnu`.
- **Preuve** : `assemblee-des-usages-nddl.yml` l. 50-52 vs l. 53-58.
- **Correction** : envisager `partiel`/`s.o.` ou expliciter que le verrou réel
  tient au fonds de dotation porteur (déjà dit), pas à l'assemblée elle-même.

### M6 — `association-keriskis` · `regime_usage_non_marchand: oui` appuyé sur une source au libellé fautif
- **Critère** : note qui ne justifie pas / qualité de preuve.
- **Problème** : la note cote `oui` en citant des activités « explicitement
  décrites comme "agricool non marchandes" ». « agricool » paraît être une coquille
  de citation (probablement « agricoles non marchandes »). Une cotation `oui` qui
  repose sur une citation visiblement déformée fragilise la preuve.
- **Preuve** : `association-keriskis.yml` l. 87-88.
- **Correction** : corriger la citation (vérifier le terme exact de la source) ou
  reformuler sans guillemets fautifs.

### M7 — `gaec-les-croquants` · pôle `ig_institue` divergent des autres GAEC Terre de Liens
- **Critère** : cohérence pôle / nature.
- **Problème** : `nature_interet: exploitation_agricole` comme tous les GAEC, mais
  pôle `ig_institue`, alors que les GAEC comparables (Durette, Bergers de la Sure,
  P'tites Berouettes, Riglanne `mutualisme`) sont en `mutualisme`. La Licorne et
  le Jointout sont aussi `ig_institue`. Trois GAEC `exploitation_agricole` se
  répartissent donc entre deux pôles sans critère explicite. La note du croquants
  (`non_lucrativite_effective: partiel`, « revenu agricole partagé entre associés »)
  décrit pourtant le trait mutualiste type.
- **Preuve** : `gaec-les-croquants.yml` l. 37 vs `gaec-ferme-la-durette.yml` l. 36,
  `gaec-de-la-licorne.yml` l. 35, `gaec-du-jointout.yml` l. 38.
- **Correction** : fixer une règle pôle↔GAEC (un GAEC `exploitation_agricole`
  = `mutualisme`, sauf justification) et harmoniser les 7 GAEC.

### M8 — `champs-des-possibles` · `localisation: null` malgré une adresse connue
- **Critère** : cohérence des données d'identité.
- **Problème** : `localisation: null` (l. 8) alors que `dossier.identite.adresse`
  donne « Hameau de Toussacq, 77480 Villenauxe-la-Petite » et que le lieu lié est
  `toussacq`. La localisation devrait au moins porter la Seine-et-Marne / Île-de-France.
- **Preuve** : `champs-des-possibles.yml` l. 8 vs l. 119.
- **Correction** : renseigner `localisation` à partir de l'adresse.

### M9 — `gaec-de-la-licorne` · SIREN 420321218 (immatriculation 1998) vs ferme « récente » (2024)
- **Critère** : SIREN plausible / cohérence.
- **Problème** : le SIREN 420321218 correspond à une racine d'immatriculation
  ancienne (séquence 42x = fin des années 1990), alors que la fiche présente une
  acquisition foncière « fin 2024 » et un GAEC dont la date de constitution est
  « non confirmée ». Le SIREN peut être exact (GAEC préexistant repreneur), mais
  l'écart mérite une note de cohérence : rien dans la fiche ne relie ce SIREN
  ancien au montage récent.
- **Preuve** : `gaec-de-la-licorne.yml` l. 121 vs l. 20-22, 116.
- **Correction** : ajouter une note d'identité expliquant l'antériorité du GAEC,
  ou re-vérifier le SIREN.

---

## RAS / points conformes

- **Entités HTML** : aucune entité brute (`&amp;`, `&#…`) dans les 46 fiches.
- **SIREN/RNA — format** : tous les SIREN sont à 9 chiffres, tous les RNA en
  W + 9 chiffres ; `association-moulinage-de-chirols` porte `siren: null` assumé
  (RNA seul, écart documenté dans la note). Formats plausibles.
- **Cohérence chaîne lieu↔usufruitier** : les 46 fiches sont chacune citée par
  au moins un lieu en `chaine.usufruitiers` ; les noms concordent. `cooperatives-longo-mai`
  est partagé par 5 lieux (Limans, Chantemerle, Mas de Granier, Treynas, La Cabrery),
  cohérent avec la fiche « réseau ». Aucun renvoi orphelin détecté.
- **`la-deviation`** : cas exemplaire — la disambiguation SIREN 789457306
  (En Devenir) vs 833981731 (En Devenir 2) est sourcée et argumentée ; cotations
  `partiel` prudentes là où le titre d'usage n'est pas publié. Modèle à suivre.
- **Cotations `non` justifiées** : les `non` sur `regime_usage_non_marchand`,
  `non_lucrativite_effective`, `vivant_finalite` des GAEC et exploitations
  (production vendue, revenu approprié, pas de finalité biodiversité) sont
  cohérentes avec la grille et bien argumentées.
- **`commune-flocques`** : `personne_morale_civile: partiel` pour une commune
  (droit public, hors droit civil strict) — lecture fine et correcte de la grille.

---

## Manques de méthode

1. **Règle pôle `integrite_montage` ↔ `nature_interet` absente.** Le défaut le
   plus structurant : aucune table de correspondance ne fixe quel pôle un
   `nature_interet` donné autorise. D'où B2 (privée individuelle → mutualisme),
   M7 (deux GAEC `exploitation_agricole` en `ig_institue`, quatre en `mutualisme`),
   et les deux fermiers individuels Terre de Liens classés différemment (Chaudeau
   `ig_institue` / Oiselière `mutualisme`). Une grille de cohérence
   `nature_interet → pôles admissibles` (analogue à la règle de calcul du `verdict`
   des lieux dans concepts.yml) supprimerait toute cette classe d'écarts et
   pourrait être contrôlée mécaniquement par le générateur.

2. **`forme_juridique` (en-tête) non contraint par le corps.** B1 montre qu'un
   en-tête peut affirmer une forme que la fiche déclare partout ailleurs inconnue.
   Garde-fou simple : si `personne_morale_civile` ou les pièces signalent une forme
   « non confirmée », `forme_juridique` ne doit pas l'affirmer sèchement (mot
   « présumée / non confirmée » requis, comme `association-keriskis`).

3. **Pas de contrôle de cohérence interne valeur↔note dans `grille:`.** M2, M5, M6
   relèvent de notes qui contredisent leur propre valeur (note « non lucrative »
   sous un `partiel` ; `oui` de verrouillage justifié par une absence de structure ;
   citation fautive sous un `oui`). Un Checker systématique « la note justifie-t-elle
   la valeur ? » devrait être passé critère par critère, pas seulement sur les `oui`/`non`.
