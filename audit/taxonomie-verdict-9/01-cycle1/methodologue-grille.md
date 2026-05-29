# Cycle 1 — voix méthodologue / gardien·ne de la cohérence

*MARS-strat, passe « refonte de l'axe `nature_interet` ». Perspective
indépendante. Critère propre : cohérence interne du système d'évaluation et
faisabilité de migration. Je ne tranche ni le politique ni le juridique fin.*

---

## 1. Diagnostic de cohérence — ce que le bug Pommiers révèle

La Ferme de Pommiers a une chaîne propre : porteur `fondation-terre-de-liens`
(`non_lucrative`), usufruitier `gaec-bergers-de-la-sure` (`commerciale`). Le
foncier est irréversiblement hors-marché, porté par une fondation RUP. Et
pourtant : `compute_verdict` voit un maillon `commerciale` dans la chaîne, et
renvoie `marchand` (l. 1304). En parallèle, `apply_lieu_plafond_chaine` lit le
pire maillon (`_pire_nature_chaine`, ordre l. 358-361 : `commerciale` arrive en
2ᵉ position, juste après `privee_individuelle`) et écrase l'axe 2 à 20
(`ax2_par_nature.commerciale: 20`).

Le bug n'est pas une erreur d'implémentation — les deux mécaniques font
exactement ce que la table leur dit. Le bug est **dans la granularité de la
valeur `commerciale` elle-même**. Elle agrège deux objets que le projet veut
désormais distinguer : la société commerciale spéculative à parts cessibles
(SARL, SAS, propriété=actif) et la société civile d'exploitation agricole
(GAEC, EARL, SCEA) dont les associé·es vivent du produit de leur travail sans
détenir ni pouvoir spéculer sur le foncier (qui appartient ici à la fondation).
La définition actuelle (concepts.yml l. 401-412) le reconnaît d'ailleurs
explicitement — elle range les deux dans le même `id` tout en les décrivant
comme distincts (« société de marché, **ou** une exploitation agricole »). C'est
le symptôme L14 à l'état pur : **un seul label porte deux réalités que la
mécanique traite identiquement, donc le calcul ment sur l'une des deux.**

Conséquence chiffrée pour la refonte : sur les 13 fiches `commerciale`, le
grep en montre une nette majorité de GAEC/EARL exploitants
(`gaec-bergers-de-la-sure`, `gaec-eyssal`, `gaec-les-ptites-berouettes`,
`gaec-ferme-la-durette`, `earl-ferme-de-magnantru`, `gaec-ferme-du-plaisir`,
`gaec-de-la-licorne`, `gaec-du-jointout`, `gaec-de-riglanne`,
`gaec-les-croquants`…) face à de vraies sociétés commerciales / SCI lucratives
(`sci-terres-ecolectif`, `le-temps-des-possibles`). **L'écrasante majorité du
bucket `commerciale` est de l'agriculture paysanne**, pas du capital spéculatif.
La refonte n'est donc pas cosmétique : elle touche le verdict et le plafond de
~10 lieux d'un coup.

---

## 2. Contraintes dures

**C1 — Le principe L11 est intouchable.** Le verdict se *calcule* sur la chaîne,
ne se saisit jamais. Toute proposition qui réintroduirait un champ `verdict:` ou
`niveau_lucrativite:` saisi à la main est rejetée d'office. Le seul levier
admissible est : (a) changer la valeur `nature_interet` saisie sur les maillons
(donnée élémentaire, légitime), et (b) recâbler les *tables* (`ax2_par_nature`,
règle de verdict) qui dérivent le jugement.

**C2 — Une seule source de vérité par fait.** Verdict et plafond ax2 lisent
**la même** donnée (le pire maillon). Tout nouveau cran doit être inséré
*simultanément* dans `_NATURE_ORDRE_PIRE_AU_MIEUX`, dans `ax2_par_nature`, et
dans la règle `compute_verdict`. Oublier l'un des trois recrée un L14.

**C3 — Nombre de crans soutenable.** L'axe a aujourd'hui 6 valeurs (dont
`inconnu`, qui est un non-cran : valeur par défaut, plafond `null`, bloque le
sanctuaire). Soit **5 crans lucratifs effectifs** : `non_lucrative`,
`commerciale_desactivee`, `commerciale_encadree`, `commerciale`,
`privee_individuelle`. Mon jugement de faisabilité : **6 crans effectifs est le
plafond raisonnable, 7 le maximum absolu**. Au-delà, trois choses cassent : (a)
l'opérateur ne peut plus *calibrer de tête* l'ordre du pire-au-mieux quand il
classe une fiche neuve ; (b) la table `ax2_par_nature` devient une rampe de
valeurs si serrées (20, 30, 35, 40, 50…) que l'écart perd tout sens
qualitatif ; (c) le badge de verdict et les étiquettes de chaîne (UI) deviennent
illisibles. **La refonte doit donc ajouter UN cran, pas deux.**

**C4 — Non-régression des garde-fous.** `verifier_uids`, `verifier_chaines`,
`verifier_entites_html` doivent rester verts. `verifier_chaines` contient déjà
(l. 4910-4920) une règle qui couple `montage.type: propriete_privee*` à la
`nature_interet` attendue du porteur (`privee_individuelle` ou `commerciale`).
**Tout nouveau cran qui sortirait les GAEC de `commerciale` doit être répercuté
ici**, sinon le garde-fou avertira à tort (ou laissera passer une incohérence).

---

## 3. Options d'architecture

Le besoin : distinguer, *à l'intérieur de l'actuel `commerciale`*, la société
spéculative (intérêt privé captable sur le foncier) de la société d'exploitation
agricole (intérêt collectif lucratif des associé·es, mais foncier non détenu /
non spéculé). J'appelle le nouveau cran **`exploitation_agricole`** (nom
provisoire, le naming fin relève d'une autre voix) — à insérer entre
`commerciale_encadree` et `commerciale` dans l'ordre du pire-au-mieux.

### Option A — nouveau cran `nature_interet` mappant sur les 3 verdicts existants

On ajoute `exploitation_agricole` à l'axe. On l'insère dans
`_NATURE_ORDRE_PIRE_AU_MIEUX` entre `commerciale` et `commerciale_encadree`. On
lui donne un plafond ax2 **entre 20 et 50** (voir §3bis). Et — c'est le point
de bascule — on décide à quel verdict il mappe dans `compute_verdict` :

- **A1** : `exploitation_agricole` reste dans la branche `marchand` (l. 1304).
  Le verdict de Pommiers ne change pas (`marchand`), mais le plafond ax2 remonte
  (de 20 à p. ex. 40). Effet : on nuance le *score* sans nuancer le *verdict*.
- **A2** : `exploitation_agricole` bascule dans la branche `hybride` (avec
  `commerciale_encadree`). Pommiers devient `hybride`. Effet : on requalifie
  ~10 lieux de `marchand` à `hybride`.

A2 est le choix cohérent avec l'intention affichée (ne pas criminaliser
l'agriculture paysanne) : laisser Pommiers en `marchand` alors que son foncier
est irréversiblement chez une fondation RUP, c'est précisément le mensonge que
la refonte veut corriger. **Coût mécanique de A : trois lignes** —
un `id` de plus dans concepts.yml, une entrée dans `ax2_par_nature`, une
position dans `_NATURE_ORDRE_PIRE_AU_MIEUX`, et le déplacement de
`exploitation_agricole` d'une branche à l'autre dans `compute_verdict`. **Le
verdict reste à 3 niveaux.**

### Option B — verdict à 4 niveaux (cran intermédiaire nommé entre hybride et marchand)

On ajoute un 4ᵉ degré de verdict, p. ex. `productif` ou `marchand_encadre`,
entre `hybride` et `marchand`. La règle `compute_verdict` gagne une branche :
`exploitation_agricole` → ce nouveau verdict.

Conséquences en cascade, toutes à payer :
- **Le couplage palier×verdict (L16).** `palier_for` (l. 325-347) et
  `apply_palier_verdict_constraint` (l. 429-444) ne testent qu'une égalité
  (`verdict == req`). Un 4ᵉ verdict n'y casse rien *mécaniquement* (aucun palier
  ne le requiert), mais oblige à rouvrir la question : un palier doit-il
  désormais distinguer ce 4ᵉ niveau ? Question politique, hors mon périmètre —
  mais je signale qu'elle s'ouvre obligatoirement.
- **Le badge** (`verdict_badge`, l. 1317) itère sur `concepts.verdict.degres` :
  il faut un 4ᵉ `degre` (label, définition, couleur, classe CSS
  `.verdict-<id>`). **C'est une modification de rendu → garde-fou L9 : aperçu
  HTML autonome obligatoire.**
- **Toute la prose** (concepts.yml l. 440-483, ranking.yml, pages méthode/régimes
  /glossaire) qui présente le verdict comme un triptyque doit être réécrite.

**Verdict de faisabilité : A2 ≫ B.** A2 obtient le résultat éditorial visé
(Pommiers cesse d'être `marchand`) au prix de trois lignes, sans toucher au
nombre de verdicts, sans rouvrir le couplage palier×verdict, sans refonte CSS.
B est un chantier conceptuel lourd (4ᵉ niveau de verdict = nouvelle catégorie
publique à défendre) qui n'achète rien de plus que A2 sur le plan du calcul. Je
ne recommande B que si une autre voix démontre qu'un 4ᵉ verdict *public nommé*
est éditorialement nécessaire — auquel cas il faut l'assumer comme décision
politique, pas comme contrainte technique.

### 3bis — valeurs numériques du nouveau cran dans `ax2_par_nature`

La rampe actuelle : `non_lucrative` 100 · `commerciale_desactivee` 80 ·
`commerciale_encadree` 50 · `commerciale` 20 · `privee_individuelle` 10. Le
trou entre 50 et 20 est large (30 points) — c'est là qu'on insère. Mon
calibrage : **`exploitation_agricole` à 40**. Justification de cohérence : il
doit rester *sous* `commerciale_encadree` (50) — une SCIC à lucrativité
statutairement bornée et verrou d'actif est structurellement plus protectrice
qu'un GAEC sans bornage de plus-value — et nettement *au-dessus* de
`commerciale` ouverte (20), qu'on garde pour la vraie société spéculative. 40
laisse l'écart 50→40→20 lisible (10 puis 20). Je déconseille 35 (trop collé à
50, frontière floue) et 45 (trop collé à 50 aussi). **40 est la valeur qui
préserve la lisibilité de la rampe.**

Effet sur Pommiers : ax2 plafonné à 40 au lieu de 20 → l'IdL remonte
mécaniquement (l'axe 2 entre en moyenne géométrique avec les 4 autres) ; reste à
recalculer après régénération.

---

## 4. Plan de migration des fiches + garde-fous à ajouter

**Étape 1 — figer la frontière de tri.** Critère opérationnel pour reclasser une
fiche actuellement `commerciale` : *les associé·es détiennent-ils/elles le
foncier ou seulement l'exploitent-ils/elles ?* Si la chaîne du lieu confie le
foncier à un porteur non lucratif et l'usage au GAEC par bail → le GAEC est
`exploitation_agricole`. Si le GAEC/la SCI **détient** le foncier (porteur ET
usufruitier confondus, ou SCI propriétaire spéculative) → reste `commerciale`.
Ce critère se lit sur la chaîne déjà déclarée — pas de nouvelle donnée à
chercher.

**Étape 2 — reclasser les ~13 fiches.** Sur la base du grep, sont candidates au
basculement vers `exploitation_agricole` les GAEC/EARL **usufruitiers**
(`gaec-bergers-de-la-sure`, `gaec-eyssal`, `gaec-les-ptites-berouettes`,
`gaec-ferme-la-durette`, `earl-ferme-de-magnantru`, `gaec-ferme-du-plaisir`,
`gaec-de-la-licorne`, `gaec-du-jointout`, `gaec-de-riglanne`,
`gaec-les-croquants`). Restent `commerciale` les porteurs/structures
spéculatives (`sci-terres-ecolectif`, `le-temps-des-possibles`) — à confirmer au
cas par cas. **Chaque bascule = un seul champ `nature_interet:` modifié sur la
fiche du maillon.** Migration triviale, atomique, réversible : c'est exactement
le profil de churn minimal de la leçon L2.

**Étape 3 — méthode parallèle (L7/L12).** ~13 fiches sur des fichiers disjoints
(un maillon par fichier, aucun partagé) → délégable à 2-3 sous-agents
partitionnés, intégration centralisée. Mais le volume est si faible (~13 éditions
d'un champ) que **je recommande la migration à la main** : le coût d'un brief de
sous-agent dépasse le coût de l'édition (cf. L24, le 4ᵉ lot mécanique repris à
la main).

**Étape 4 — garde-fou à ajouter (`verifier_natures` ou extension de
`verifier_chaines`).** Risque L14 résiduel : rien n'empêche une fiche neuve de
déclarer `exploitation_agricole` sur une SCI purement spéculative, ou
`commerciale` sur un GAEC exploitant. Je recommande **un avertissement** (pas un
blocage — la nature reste un jugement) dans `verifier_chaines` : si une fiche
porte une `forme_juridique` de type société civile agricole (GAEC/EARL/SCEA) et
`nature_interet: commerciale`, signaler « GAEC/EARL classé `commerciale` —
vérifier si `exploitation_agricole` est attendu ». Symétriquement pour une SCI/
SARL classée `exploitation_agricole`. **Et ne pas oublier** : la règle existante
de `verifier_chaines` l. 4913-4920 (`montage propriete_privee` → nature attendue)
doit intégrer le nouveau cran dans son test `want`.

**Étape 5 — régénération + recalcul.** Après migration : régénérer, vérifier que
les garde-fous sont verts, recalculer verdicts et paliers. Plusieurs lieux
basculeront de `marchand` à `hybride` (option A2). **Contrôler la cohérence
palier↔verdict** : aucun de ces lieux requalifiés ne doit indûment atteindre le
palier `abouti` (réservé `sanctuaire` — le couplage L16 les protège déjà
mécaniquement, mais vérifier). Et — L9 — **aperçu HTML autonome de la fiche
Pommiers** livré pour revue, puisque son badge de verdict et son panneau de
score changent visuellement.

---

## 5. Désaccords prévisibles avec les autres angles

- **Avec l'angle juridique** : la voix juridique voudra probablement une
  définition fine distinguant GAEC, EARL, SCEA, SCI agricole, SCEA à associé
  unique… Je m'y opposerai si elle multiplie les crans : un cran par forme
  juridique ferait exploser C3 (≥ 8 valeurs, table illisible). Ma position : la
  forme juridique est une *donnée d'entrée* (champ `forme_juridique:`) qui
  *informe* le classement, mais l'axe `nature_interet` ne doit pas la dupliquer
  cran par cran. Un seul cran `exploitation_agricole` regroupe toutes les
  sociétés civiles d'exploitation ; la nuance fine vit dans la prose de la
  fiche, pas dans l'énuméré.
- **Avec l'angle politique** : la voix politique voudra peut-être un verdict à 4
  niveaux (option B) pour *nommer publiquement* la posture critique
  (« productif mais pas libéré »). Je signalerai le coût (refonte CSS, prose,
  réouverture palier×verdict) et demanderai que ce soit assumé comme décision
  éditoriale, pas justifié par la mécanique — la mécanique, elle, est satisfaite
  par A2.
- **Avec l'angle éditorial** : risque que le nom du cran porte une charge
  (`exploitation_agricole` est neutre, mais une autre voix pourrait proposer
  `paysan` / `productif` / `lucratif_collectif`). Je ne tranche pas le nom ;
  je pose seulement que l'`id` interne doit rester stable une fois figé (L2) et
  que le slug/label public ne reprenne pas un qualificatif interne polémique
  (L32).

---

## 6. Mes lignes rouges (ce qui casserait la cohérence du système)

1. **Réintroduire un verdict ou un degré de lucrativité saisi à la main.**
   Violation directe de L11. Rejet absolu.
2. **Ajouter plus d'un cran `nature_interet` dans cette passe.** Au-delà de 6
   crans effectifs, la table devient incalibrable et l'UI illisible (C3).
3. **Toucher `ax2_par_nature`, `_NATURE_ORDRE_PIRE_AU_MIEUX` ou la règle de
   verdict isolément.** Les trois dérivent du *même* pire-maillon : modifier
   l'un sans les deux autres recrée un L14 immédiat.
4. **Bricoler le verdict de Pommiers sur la fiche** (forcer un champ) au lieu de
   corriger la `nature_interet` du GAEC. Le bug est dans la donnée du maillon,
   il se corrige là — pas par une exception au calcul.
5. **Modifier le rendu (badge, panneau, étiquettes de chaîne) sans aperçu HTML
   autonome.** L9 : aucun garde-fou ne voit la mise en page.
6. **Laisser un GAEC exploitant en `commerciale` après la refonte sans garde-fou
   d'alerte.** Sans le `verifier_*` de l'étape 4, la frontière dérivera au fil du
   peuplement (L31 : les calibrages manquants ne surgissent qu'à la
   confrontation au réel).
