# Cycle 1 — voix méthodologue / gardien·ne de la cohérence du système

*Passe MARS-strat comparative #9 (modèle renforcé vs modèle actuel), cycle 1,
divergence isolée. Voix : méthodologue de la grille. Écrit pour le mainteneur du
générateur. Perspective indépendante — n'a pas lu les autres voix de cette passe.
Aucun fichier modifié.*

---

## Préambule — ce que je mesure, ici

Je ne tranche ni le politique (faut-il un sommet aussi exigeant ?) ni le
doctrinal (Polanyi vaut-il mieux qu'Ostrom ?). Je mesure une seule chose : ce
que coûte, en encodage, le passage du modèle actuel au modèle renforcé, et si ce
passage casse ou non les invariants du système d'évaluation — L11 (« le verdict
se calcule, ne se saisit pas »), source unique de vérité (la chaîne), `inconnu`
sacré, label mobile / `id` figé (L2). Je travaille sur le code et la config
réellement lus, pas sur l'intention.

---

## 1. Cartographie de la taxonomie ACTUELLE

Inventaire différencié de ce qui existe — c'est la base pour le cadre exhaustif.

### 1.1 Les cinq axes de l'Indice (`ranking.yml`, `grilles.yml`)

Chaque axe a un **domicile** (le maillon de chaîne où il se joue) et agrège des
critères pondérés (`score_axe = Σ(poids × facteur)/Σ(poids) × 100`).

| Axe | Label | Domicile | Critères (grille `lieu`) |
|---|---|---|---|
| 1 | Le sol | porteur (face juridique) + lieu (face matérielle) | `foncier_hors_marche` (3), `montage_documente` (2), `irreversibilite` (3), `origine_non_speculative` (2), `parts_non_cessibles` (3), `milieu_protege` (2) |
| 2 | La structure | `chaine_min` (pire maillon) | `non_lucratif_global` (3), `montage_non_commercial` (3) |
| 3 | Le pouvoir | usufruitier | `gouvernance_collective` (3), `tripartisme` (2), `perennite_gouvernance` (2) |
| 4 | La finalité | `chaine_min` | `usage_interet_general` (3), `ancrage_territorial` (2), `vivant_finalite` (2) |
| 5 | L'usage | convention + lieu | `usage_non_marchand` (3), `loyer_non_rentier` (2), `securite_jouissance` (3), `usage_non_degradant` (3), `place_au_vivant` (3) |

Les grilles `porteur` et `usufruitier` ont leurs propres critères par axe — dont,
notable pour le renforcé : `autogestion_usagers` (porteur, axe 3, poids 3 — voix
DÉLIBÉRATIVE des usager·es), `usagers_decident` + `une_voix` (usufruitier, axe 3),
`non_lucrativite_effective` (porteur ET usufruitier, axe 2), `regime_usage_offert`
/ `regime_usage_non_marchand` (axe 5).

### 1.2 L'axe `nature_interet` (`concepts.yml` l. 370-431)

Axe **descriptif orthogonal**, *saisi* sur chaque porteur/usufruitier (jamais sur
le lieu). 6 crans, du plus pur au moins : `non_lucrative` → `commerciale_desactivee`
→ `commerciale_encadree` → `commerciale` → `privee_individuelle` → `inconnu`.
C'est la **seule donnée saisie** qui alimente le verdict — tout le reste se calcule.

### 1.3 Le verdict (`compute_verdict`, l. 1290-1314)

Calculé, jamais saisi. 3 niveaux. Algorithme réel :
1. maillon `commerciale` ou `privee_individuelle` → `marchand` ;
2. sinon maillon `commerciale_encadree` → `hybride` ;
3. sinon maillon `inconnu` → `None` (« à établir ») ;
4. sinon (chaîne entièrement `non_lucrative`/`commerciale_desactivee`) →
   `sanctuaire` **si** `foncier_hors_marche==oui ET irreversibilite==oui ET
   vivant_finalite==oui ET place_au_vivant==oui`, sinon `hybride`.

Le verdict croise donc déjà **deux sources** : la nature des maillons (saisie) et
quatre critères de grille du lieu (D-B + irréversibilité). C'est le précédent
décisif pour le renforcé : *on sait déjà faire remonter des critères de grille au
verdict* (round 2 l'a même formalisé comme « re-câblage », ~8 lignes).

### 1.4 Paliers, plafonds, silhouettes

- **Paliers** (5, l. 279-317) : `abouti` (min 70, `requiert_verdict: sanctuaire`),
  `solide` (64), `engage` (50), `partiel` (35), `eloigne` (0). Le palier `abouti`
  est couplé au verdict via `palier_for` (l. 325-347) : un non-sanctuaire est
  dégradé d'un cran. **Couplage palier×verdict déjà actif et fragile** — tout
  ajout de verdict le rouvre.
- **Plafonds chaîne** (`ax2_par_nature`, l. 327-334) : l'axe 2 d'un lieu est
  plafonné par le pire `nature_interet` (`non_lucrative` 100 … `commerciale` 20,
  `privee_individuelle` 10, `inconnu` null). Mécanisme parallèle au verdict, même
  source (`_pire_nature_chaine`, l. 364-378).
- **Silhouettes de montage** (`concepts.yml`, `montages`) : DESCRIPTIVES
  (démembrement, propriété protégée…) — ne portent aucun jugement. Le jugement
  vit dans `nature_interet` + verdict.

### 1.5 Acquis rounds 1-2 (déjà dans la grille)

- **Round 1 (foncier-captation)** : la captation se lit sur la chaîne via
  `nature_interet × titre` (le `titre` — bail rural, emphytéotique — vit déjà dans
  les articulations, `concepts.yml` l. 524-532). Un cran neuf `commerciale`
  exploitation-agricole-sur-bail, dérivation relationnelle ~15-25 lignes. **Aucun
  champ saisi neuf.**
- **Round 2 (finalité-glose)** : `usage_interet_general` (axe 4) et
  `usage_non_marchand` (axe 5) **existent déjà**, gradués. Le besoin est un
  re-câblage (co-gate du sommet + glose), pas un axe. **Aucun champ saisi neuf.**

**Le fil rouge des rounds 1-2 : tout besoin nouveau a été satisfait par re-câblage
de données existantes, jamais par saisie. C'est l'étalon que le renforcé doit
égaler.**

---

## 2. Ce que la grille capture DÉJÀ du modèle renforcé

Le §3 du cadre renforcé liste 7 conditions cumulatives du sommet. Je les confronte
à la grille réelle :

| Condition renforcée | Déjà capturé ? | Par quoi |
|---|---|---|
| 1. Foncier hors-marché irréversible | **Oui, pleinement** | axe 1 (`foncier_hors_marche`, `irreversibilite`, `parts_non_cessibles`) — déjà gate du sommet |
| 2. Gouvernance collective sans hiérarchie | **Partiellement** | `gouvernance_collective`, `usagers_decident`, `une_voix`, **`autogestion_usagers`** (déjà le critère qui sépare autogestion / IG institué) — mais « sans hiérarchie/salariat » n'est pas isolé |
| 3. Non-appropriation actifs ET bénéfices | **Partiellement** | actifs : `non_appropriation`, `parts_non_cessibles`, `clause_devolution` (axe 1) ; bénéfices : `non_lucrativite_effective` (axe 2) — mais lus sur la *structure*, pas sur la *répartition aux travailleur·ses* |
| 4. Économie décommodifiée (don/troc) | **Partiellement** | `usage_non_marchand` / `regime_usage_non_marchand` gradués (oui = gratuité/don/troc) — capture le mode de circulation du *fruit*, pas la prise en charge collective des *besoins monétaires* |
| 5. Usage doux et régénératif | **Oui, largement** | `usage_non_degradant` (axe 5, déjà « laisser le lieu aussi vivant qu'on l'a reçu »), `milieu_protege` (axe 1, ORE opposable), `place_au_vivant` |
| 6. Intérêt général | **Oui** | `usage_interet_general`, `objet_ig`, `public_non_restreint` (axe 4) |
| 7. Habitat du vivant | **Oui, pleinement** | `vivant_finalite` + `place_au_vivant` — déjà D-B, déjà gate du sommet |

**Constat fort : 4 des 7 conditions sont déjà gérées (1, 5, 6, 7) et deux le sont
en gros (2, 3).** Le modèle renforcé n'est pas un système neuf : c'est un
**resserrement du gate du sommet** sur des critères majoritairement présents, plus
**l'introduction d'un objet réellement neuf** : les *rapports de production*
(salariat / partage du travail) et la *prise en charge collective des besoins
monétaires*, que rien dans la grille ne voit aujourd'hui.

---

## 3. Ce qu'il faudrait AJOUTER — coût et risque `inconnu`

### 3.1 Les critères vraiment neufs

Trois choses ne sont capturées par aucun critère existant :

- **a. Non-salariat / non-subordination du travail.** L'axe 2 (`ranking.yml`
  l. 88-92) *évoque* déjà « la subordination d'un travail salarié à une autorité
  de marché » comme lecture de la nature commerciale — mais c'est une glose
  d'intention, **aucun critère saisi ne la porte**. Critère neuf : `travail_non_salarie`
  (les personnes qui font vivre le lieu n'y sont pas en rapport de subordination
  salariale).
- **b. Non-appropriation individuelle du bénéfice d'exploitation.** Distinct de
  `non_lucrativite_effective` (qui regarde le capital, pas le revenu du travail).
  C'est le cœur du « piège GAEC » du cadre renforcé : un GAEC bio sur bail dont les
  associé·es s'approprient le bénéfice. Critère neuf : `benefice_non_approprie`.
- **c. Prise en charge collective des besoins monétaires (Polanyi/Illich).**
  Vraiment neuf, et le plus difficile. Critère : `besoins_pris_en_charge_collectivement`.

La régénération active (compensation des prélèvements) est, elle, **largement
absorbable** par `usage_non_degradant` + `milieu_protege` — au pire un raffinement
de définition (« régénère » comme palier au-dessus de « maintient »), pas un axe.

### 3.2 Combien d'axes / critères ? Deux scénarios.

- **Scénario minimal (re-câblage, recommandé)** : on N'ajoute PAS d'axe.
  Les 5 axes restent. On ajoute **2 à 3 critères neufs** (`travail_non_salarie`,
  `benefice_non_approprie`, éventuellement `besoins_pris_en_charge_collectivement`)
  logés dans l'axe **2** (la structure — nature des rapports) ou **3** (le pouvoir
  — rapports de production), et on les fait **co-gater le sommet** comme round 2 l'a
  fait pour la finalité. Coût d'encodage : ~3 critères en `grilles.yml` + ~10-15
  lignes dans `compute_verdict` (étendre la condition `sanctuaire`). Le verdict
  reste à 3 niveaux.
- **Scénario maximal (axe « rapports économiques »)** : un 6ᵉ axe. Je le
  **déconseille fermement**. Un 6ᵉ axe touche la moyenne géométrique (l. 175-182),
  le radar (5 branches → 6), la pondération `chaine_min`, l'ensemble de l'UI et la
  prose des axes. C'est le churn que round 2 a explicitement écarté (« ni nouvel
  axe, ni verdict bidimensionnel »). Aucun gain de calcul par rapport au scénario
  minimal.

### 3.3 Le risque `inconnu` — le point dur

C'est ma plus grosse réserve, et elle est **structurelle**, pas idéologique.
`inconnu` est sacré (round 1 §3.5 : on ne classe pas par marqueurs qui exigeraient
des champs absents). Or les 3 critères neufs sont **quasi-inobservables sur sources
publiques** :

- `travail_non_salarie` : exige de connaître les contrats de travail internes.
- `benefice_non_approprie` : exige les comptes / la répartition du résultat.
- `besoins_pris_en_charge_collectivement` : exige une enquête de terrain.

Si ces critères **co-gatent le sommet**, et qu'ils sont presque toujours `inconnu`,
alors par la règle « `sanctuaire` ne s'allume jamais tant qu'un critère D-B est
`inconnu` » (l. 450), **le sommet devient inatteignable pour presque tout le
corpus**. Ce n'est pas un bug d'encodage : c'est la mécanique `inconnu`-bloque-sommet
qui transforme un idéal exigeant en sommet vide. Le cadre renforcé pose lui-même la
question (§6, observabilité) ; ma réponse de méthodologue est : **techniquement,
le sommet sera vide ou quasi**, sauf à (i) accepter que `partiel`/`inconnu` ne
bloque pas (mais alors on blanchit), ou (ii) renoncer au gate dur et n'en faire
qu'une **glose** (comme l'option β du round 2). Je penche pour la glose — mais
c'est l'empiriste/agroécologue qui doit dire si la donnée existe ; moi je dis
seulement : *gate dur sur donnée inobservable = sommet vide, par construction.*

---

## 4. Articulation avec rounds 1-2 + verdict 3 niveaux

### 4.1 Le renforcé ABSORBE les rounds 1-2, il ne les refond pas

C'est la bonne nouvelle. Le renforcé **conserve** le plancher foncier (round 1 :
captation lue sur la chaîne, cran exploitation-agricole, plafond ax2) tel quel — il
le qualifie même de « plancher irréversible conservé » (§5). Et il **prolonge** le
re-câblage du round 2 : là où round 2 faisait co-gater le sommet par
`usage_interet_general` (+ option α sur `usage_non_marchand`), le renforcé ajoute
2-3 critères de rapports au même co-gate. **Même mécanique, mêmes lignes de code,
mêmes invariants.** Le renforcé est l'**extension** du re-câblage round 2, pas une
architecture rivale.

Une nuance de cohérence : le renforcé **déplace le GAEC bio sur bail du milieu vers
le bas du sommet** (§4 : appropriation individuelle du bénéfice → milieu, pas
sommet). Or round 1 venait de le **monter** de `marchand` à `hybride`. Ces deux
mouvements ne se contredisent PAS : round 1 agit sur le *verdict* (marchand →
hybride, via la chaîne), le renforcé agit sur l'*accès au sommet* (hybride →
pas sanctuaire, via `benefice_non_approprie`). Le GAEC bio sur bail finit
`hybride` dans les deux modèles — exactement le résultat de Pommiers. **Le renforcé
ne casse rien des acquis ; il ajoute une marche au-dessus.**

### 4.2 Verdict 3 niveaux : tenable

Oui, tenable, et il FAUT le tenir. Les rounds 1-2 ont écarté à l'unanimité tout 4ᵉ
verdict (coût de rendu, réouverture `palier×verdict`, prose à réécrire, zéro gain
de calcul). Le renforcé n'introduit **aucun besoin d'un 4ᵉ niveau** : ses critères
neufs raffinent la *condition d'accès* à `sanctuaire`, ils ne créent pas une
catégorie ontologique nouvelle. `sanctuaire`/`hybride`/`marchand` suffisent — on
durcit simplement le test qui sépare `sanctuaire` de `hybride`. **3 niveaux,
maintenus.**

---

## 5. Coût comparé d'encodage des deux modèles

| | Modèle actuel (rounds 1-2 implémentés) | Modèle renforcé |
|---|---|---|
| Nouveaux axes | 0 | **0** (scénario minimal) ou 1 (déconseillé) |
| Champs saisis neufs | 0 (round 1 : un cran `nature_interet` ; round 2 : 0) | **2-3 critères de grille saisis** |
| Lignes `compute_verdict` | ~8 (round 2) + ~15-25 (dérivation round 1) | + ~10-15 (étendre condition `sanctuaire`) |
| Verdict | 3 niveaux | **3 niveaux** |
| Couplage palier×verdict | inchangé | inchangé |
| Risque `inconnu` | maîtrisé (données existantes) | **ÉLEVÉ** (3 critères quasi-inobservables) |
| Risque sommet vide | faible | **élevé si gate dur ; nul si glose** |

**Verdict de coût : le renforcé est PEU coûteux en architecture (3 critères, ~15
lignes, 3 niveaux conservés) — il est conforme aux invariants L11 / source unique /
L2. Son seul vrai coût n'est pas le code, c'est l'OBSERVABILITÉ des 3 critères
neufs, qui décide si le sommet est habitable ou vide.** Le choix gate-dur vs glose
est doctrinal (où s'inscrit la posture — calcul ou affichage), exactement comme
α/β au round 2 ; moi je ne le tranche pas, je dis seulement qu'il commande tout le
risque.

---

## 6. Désaccords prévisibles (cycle 2)

- **Avec la voix pro-renforcé** : elle voudra **gater dur** sur les 3 critères
  (« la posture doit peser dans le calcul, pas seulement l'affichage »). Je
  répondrai : gate dur sur donnée inobservable = sommet vide *par construction* de
  la règle `inconnu`-bloque. Tension réelle, pas de faux accord possible : c'est le
  même crux que α/β, et il faut le poser à l'opérateur.
- **Avec l'empiriste / `inconnu`** : accord probable sur le diagnostic
  (inobservabilité), désaccord possible sur la conclusion — l'empiriste pourrait
  vouloir **renoncer aux 3 critères** ; moi je veux les **encoder mais en glose**
  (ils existent dans la grille, alimentent l'Indice, mais ne gatent pas), pour que
  la posture soit *visible* sans rendre le corpus non-jugeable.
- **Avec l'agroécologue** : friction sur la régénération. Je soutiens qu'elle est
  **déjà absorbée** par `usage_non_degradant` + `milieu_protege` ; l'agroécologue
  réclamera sans doute un critère `regeneration_active` distinct (rendre plus que
  prélever ≠ ne pas dégrader). Désaccord sur le grain : un raffinement de définition
  (mon camp) vs un critère neuf (le sien). Observable sur sources publiques ? J'en
  doute — d'où, encore, le risque `inconnu`.

---

*Fin du cycle 1 — voix méthodologue. Position synthétique : le renforcé est
encodable à coût architectural faible et sans casser un invariant ; le verrou
n'est pas le code mais l'observabilité de 3 critères de rapports, qui décide
gate-dur (sommet vide) vs glose (sommet habitable, posture visible).*
