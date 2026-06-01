# Validation corpus #11 — Passe 1 — Lieux m → z

**Checker MARS-prod (lecture seule).** Lot : 12 fiches `lieux/[m-z]*.yml` —
magnantru, maison-blanche-antre-toit, mas-de-granier, moulinage-de-chirols,
nddl, oasis-coq-a-lame, riglanne, tera, toussacq, treynas, village-vertical,
villarceaux.

Contrôles appliqués (skill `communs-veille-valider` + `config/grilles.yml` +
`config/concepts.yml`) : cotation `oui`/`non` fabriquée (axes vivant/usage) ;
chaîne valide (articulations ⊆ chaine, uid existants, titres/natures du canon,
`integre` réservé à l'entité-unique) ; désync verdict/prose ; libellés de forme
juridique présumés vs registre ; entités HTML brutes ; réserves honnêtes.

Tous les uid de chaîne référencés (porteurs + usufruitiers) existent comme
fichiers d'entité. Aucune entité HTML brute dans le lot. `integre` employé une
seule fois (village-vertical) et à bon droit (porteur = usufruitier =
`le-village-vertical`).

---

## BLOQUANTES

### B1 — villarceaux · chaîne incomplète : le maillon qui fait le verdict est absent de la chaîne
- **Problème.** `chaine.usufruitiers: [ecosite-villarceaux]` et
  `montage.articulations[].usufruitier: ecosite-villarceaux` ne déclarent que
  l'**association Écosite** (loi 1901, `nature_interet: non_lucrative`). Or la
  fiche elle-même établit que l'**exploitant réel** est l'**EARL du Chemin Neuf**
  (société civile d'exploitation agricole, exploitant Olivier Ranke). C'est ce
  maillon — `exploitation_agricole`, voire `commerciale` s'il détient/exploite
  sans bail sécurisé — qui plafonne le verdict. Il n'a **pas de fiche d'entité**
  (absent de `usufruitiers/`) et ne figure **ni dans `chaine` ni dans
  `articulations`**.
- **Preuve.** `lieux/villarceaux.yml` l.74-76 (`montage_non_commercial: non` —
  « L'usufruitier inclut l'EARL du Chemin Neuf, société commerciale
  d'exploitation agricole ») ; l.98-100 (`travail_non_marchandise: oui` —
  « EARL du Chemin Neuf, société civile d'exploitation ») ; l.125-127
  (`chaine.usufruitiers: [ecosite-villarceaux]`). Entité `ecosite-villarceaux`
  l.21 : « Titulaire de l'usage : association Écosite … et EARL du Chemin Neuf ».
- **Correction.** Créer l'entité `usufruitiers/earl-du-chemin-neuf.yml`
  (`nature_interet` à trancher : `exploitation_agricole` si bail sécurisé sous la
  FPH, sinon `commerciale`) et l'ajouter à `chaine.usufruitiers` + à une
  `articulation`. Tant que le maillon exploitant est hors chaîne, le verdict
  calculé est faux (sous-estime la lucrativité de la chaîne).

### B2 — villarceaux · cotation contradictoire sur la forme de l'EARL (société commerciale vs société civile)
- **Problème.** Deux notes de la même grille qualifient l'EARL du Chemin Neuf de
  façon **opposée** : `montage_non_commercial: non` la dit « société commerciale
  d'exploitation agricole », `travail_non_marchandise: oui` la dit « société
  civile d'exploitation ». Le canon (`concepts.yml`, `nature_interet:
  exploitation_agricole`) tranche : une EARL est une **société civile**
  d'exploitation, lucrative pour ses associé·es mais non commerciale au sens du
  marché. La note de `montage_non_commercial` retient le mauvais libellé, et la
  valeur `non` (« un maillon commercial à lucrativité ouverte ») au lieu de
  `partiel` (intérêt privé encadré / bénéfice d'exploitation approprié →
  plafond `hybride`) en découle.
- **Preuve.** `lieux/villarceaux.yml` l.75-76 vs l.99-100.
- **Correction.** Aligner les deux notes sur la lecture canonique (EARL =
  société civile d'exploitation). Trancher `montage_non_commercial` en fonction
  du titre réel : si l'EARL est preneuse d'un bail sécurisé sous la FPH →
  `partiel` (hybride) ; si elle détient/exploite sans bail → `non` (marchand).
  La nature exacte du titre est notée « non documentée » : à défaut, la
  prudence impose `partiel` avec réserve, pas `non` fabriqué sur un libellé faux.

---

## MINEURES

### M1 — moulinage-de-chirols · uid de chaîne portant une forme juridique fausse (`scic-` pour une SAS)
- **Problème.** `chaine.porteurs: [scic-moulinage-de-chirols]` et l'entité
  `porteurs/scic-moulinage-de-chirols.yml` portent un **uid préfixé `scic-`**,
  alors que le contenu (vérifié au registre) établit une **SAS** constituée
  comme société commerciale (NAF 6820B), **sans statut SCIC/SCOP certifié**. Le
  contenu est entièrement corrigé (nom « SAS Le Moulinage de Chirols »,
  forme_juridique, « POINT DE FORME RÉSOLU » dans `fiabilite`) ; **seule la
  chaîne de caractères de l'uid** conserve le libellé faux. C'est exactement le
  cas SCIC/SCOP→SAS que le skill nomme — résolu sur le fond, résiduel sur l'uid.
- **Preuve.** `porteurs/scic-moulinage-de-chirols.yml` l.1 (`uid: scic-…`) vs
  l.3 (`nom: "SAS Le Moulinage de Chirols"`), l.161-169 (POINT DE FORME RÉSOLU) ;
  `lieux/moulinage-de-chirols.yml` l.202.
- **Correction.** Renommer l'entité en `sas-moulinage-de-chirols` (ou neutre
  `porteur-moulinage-de-chirols`) et propager dans `chaine.porteurs`. Impact
  cosmétique sur le rendu (l'uid n'est pas affiché), mais un uid mensonger est un
  piège pour le prochain carveur. Priorité basse car le fond est juste.

### M2 — maison-blanche-antre-toit · uid de chaîne `fonciere-antidote` pour un fonds de dotation
- **Problème.** `chaine.porteurs: [fonciere-antidote]` : l'uid embarque
  « foncière », mais l'entité est un **fonds de dotation** (loi du 4 août 2008),
  comme le confirment sa `forme_juridique`, son `sous_titre` et toutes les notes
  de sa grille — et comme le dit d'ailleurs la prose du lieu (« le fonds de
  dotation Antidote »). Libellé de forme présumé/faux dans l'uid, fond correct.
- **Preuve.** `porteurs/fonciere-antidote.yml` l.4-6 (sous_titre + forme_juridique
  « Fonds de dotation ») ; `lieux/maison-blanche-antre-toit.yml` l.21-22, 34, 44
  (prose « fonds de dotation Antidote ») vs l.138 (`chaine.porteurs:
  [fonciere-antidote]`).
- **Correction.** Renommer en `fonds-antidote` et propager. Là encore, fond juste,
  uid trompeur.

### M3 — nddl · usufruitier de chaîne sans articulation correspondante (chaîne pendante)
- **Problème.** `chaine.usufruitiers: [assemblee-des-usages-nddl]` est déclaré,
  mais le bloc `montage` ne comporte **aucune `articulations:`** (seul `type` +
  `description`). Le contrôle « articulations ⊆ chaine » passe (ensemble vide),
  mais l'inverse échoue : un usufruitier annoncé dans la chaîne n'est relié au
  porteur par aucun acte (titre). La prose assume ce flou (« les détails des
  montages d'usage parcelle par parcelle ne sont pas confirmés »), mais la
  chaîne affirme tout de même un usufruitier identifié.
- **Preuve.** `lieux/nddl.yml` l.21-28 (montage sans articulations) vs l.116-118
  (`chaine.usufruitiers: [assemblee-des-usages-nddl]`).
- **Correction.** Soit ajouter une `articulation` honnête
  (`titre: convention`, `note:` « titre non documenté »), soit, si l'usage
  parcelle par parcelle n'est pas établi, retirer l'usufruitier de la chaîne et
  documenter l'état « usage non formalisé ». Vérifier que le générateur ne casse
  pas le rendu de la chaîne quand un usufruitier déclaré n'a pas d'articulation.

### M4 — oasis-coq-a-lame · `montage.type` discutable (propriete_collective vs propriete_protegee)
- **Problème.** `type: propriete_collective` alors que la fiche décrit un
  **porteur distinct de l'usufruitier** (SCIC propriétaire → bail emphytéotique
  à une association d'habitant·es tierce). Le canon réserve `propriete_collective`
  à la chaîne intégrée (« souvent le collectif qui détient est aussi celui qui
  use ») ; ici la dissociation porteur/usufruitier par bail relève plutôt de
  `propriete_protegee` (« propriété conservée + bail de long terme »). Cas
  limite : la SCIC est de sociétariat habitant, ce qui justifie en partie
  `collective`, mais la silhouette décrite est une dissociation par bail.
- **Preuve.** `lieux/oasis-coq-a-lame.yml` l.28 (`type: propriete_collective`),
  l.30-32 (bail_emphyteotique à `habitants-echoisy`), l.44-45 (« La SCIC confie
  l'usage … par un bail emphytéotique »). À comparer à Magnantru/Toussacq
  (porteur ≠ usufruitier, bail) classés `propriete_protegee`.
- **Correction.** Trancher : si la dissociation par bail prime → `propriete_protegee` ;
  si le sociétariat habitant prime → garder `propriete_collective` mais l'assumer
  explicitement. À harmoniser avec TERA, classée `propriete_collective` sur une
  logique voisine (fonds + SCI), pour cohérence du lot.

### M5 — magnantru · `forme_juridique: null` sur une fiche par ailleurs très documentée
- **Problème.** Le champ `forme_juridique` est `null` alors que la chaîne est
  parfaitement identifiée (foncière FEVE = SCA à actionnariat solidaire ; EARL
  La Ferme de Magnantru). Le `null` est la convention du lot pour les fiches-lieu
  (toutes les fiches sauf chirols ont `forme_juridique: null`, la forme étant
  portée par les entités) — donc **conforme à la convention**, mais asymétrique
  avec moulinage-de-chirols qui, lui, renseigne `forme_juridique`. Signalé pour
  cohérence éditoriale, non comme erreur.
- **Preuve.** `lieux/magnantru.yml` l.6 vs `lieux/moulinage-de-chirols.yml` l.6.
- **Correction.** Décider d'une règle : `forme_juridique` au niveau du lieu
  réservé aux montages mono-structure (Chirols), `null` sinon. Documenter la
  convention pour éviter l'asymétrie perçue.

---

## RAS (cotation et chaîne tenues)

- **mas-de-granier**, **treynas** (Longo Maï / Fonds de Terre Européenne) :
  chaîne cohérente (`propriete_protegee`, `convention` avec note « titre non
  documenté »), cotations vivant/usage honnêtes et largement en `partiel`/`non`
  avec réserves explicites. Aucun `oui` fabriqué. Verdict implicite `hybride`
  cohérent (usage marchand partiel, milieu non protégé).
- **riglanne** (Terre de Liens / GAEC) : chaîne saine, `travail_non_marchandise:
  oui` justifié (GAEC = société civile d'exploitation, paysannes non salariées) ;
  `vivant_finalite`/`place_au_vivant: non` honnêtes ; foncier `partiel` (moitié
  des terres). Bonne tenue des réserves.
- **toussacq** (Terre de Liens / Champs des Possibles SCIC) : cotations cohérentes,
  `milieu_protege: inconnu` honnête (bail non lu). Verdict `hybride` cohérent
  (SCA + SCIC = deux maillons à intérêt privé encadré).
- **tera** (fonds SDH / SCI Le Tilleul / Coop) : chaîne simplifiée au porteur
  dominant (fonds SDH) alors que le foncier transite par une SCI à usage locatif
  « lucratif » — assumé en prose et en notes (`montage_non_commercial: partiel`),
  donc honnête ; cotations vivant en `partiel` justifiées.
- **village-vertical** : `integre` correctement employé (entité-unique),
  cotations urbaines honnêtes (`milieu_protege`/`vivant_finalite`/`place_au_vivant:
  non` argumentés à l'échelle d'un immeuble), `loyer_non_rentier: oui` justifié
  par le verrou statutaire au nominal.
- **moulinage-de-chirols** (fiche-lieu) : cotations solidement sourcées
  (registre, BODACC), `oui` sur vivant (`vivant_finalite`, `place_au_vivant`)
  justifiés par faits concrets (~2 000 m² faysses bio, ruches, poules, fruitiers).
  Réserves honnêtes (statuts PDF non lus). Seul l'uid de chaîne reste fautif (M1).

**Note de méthode sur les `oui` vivant/usage du lot.** Les `oui` les plus
exposés (Oasis Coq à l'Âme `place_au_vivant`, Villarceaux `vivant_finalite`/
`place_au_vivant`, NDDL `usage_non_degradant`/`place_au_vivant`) sont tous
**adossés à un fait sourcé** (ORE signée 28/08/2025 ; 5 + 8 km de haies et
650 arbres ; bocage humide à espèces protégées). Aucun `oui` fabriqué détecté
sur les axes vivant/usage dans ce lot — la discipline du `inconnu` par défaut
est respectée.

---

## Manques de méthode (contrôles à ajouter au skill `communs-veille-valider`)

1. **Contrôle « chaîne complète » (le plus important).** Le skill vérifie
   `articulations[].usufruitier ⊆ chaine.usufruitiers` mais **pas l'inverse, ni
   l'exhaustivité réelle des maillons**. Villarceaux (B1) le montre : un
   exploitant (EARL) qui FAIT le verdict peut être nommé dans la prose et les
   notes sans figurer ni dans `chaine` ni dans `articulations` ni même comme
   entité. Ajouter : (a) tout usufruitier de `chaine` doit avoir une
   `articulation` correspondante (M3, NDDL) ; (b) **grep des notes de grille
   pour les noms de structures (EARL, SAS, SCI, SCIC, GAEC, association…) et
   recoupement avec `chaine`** — toute structure citée dans une note comme
   maillon du montage doit être dans la chaîne et avoir une entité.

2. **Contrôle « uid ≠ forme réelle ».** Détecter les uid préfixés par une forme
   juridique (`scic-`, `scop-`, `fonciere-`, `sci-`, `fonds-`, `fondation-`,
   `gaec-`, `earl-`, `association-`) et **comparer le préfixe à la
   `forme_juridique`/`nature_interet` de l'entité**. M1 (scic-→SAS) et M2
   (fonciere-→fonds de dotation) sont invisibles aux contrôles actuels parce
   que le fond a été corrigé sans renommer l'uid. Un uid mensonger survit aux
   corrections de contenu et piège le carveur suivant.

3. **Contrôle de cohérence interne des notes d'une même fiche.** B2 (EARL dite
   « société commerciale » dans une note et « société civile » dans une autre)
   passe tous les contrôles actuels. Ajouter une passe qui repère, dans les
   `note:` d'une même fiche, **deux qualifications juridiques contradictoires de
   la même structure** (recherche du nom de structure + termes de forme
   incompatibles : « commerciale » vs « civile », « SCIC » vs « SAS »…).
