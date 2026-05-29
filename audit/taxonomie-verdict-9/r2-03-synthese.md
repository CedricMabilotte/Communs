# Synthèse round 2 — la finalité de l'usage (intérêt général / non-lucratif)

*Session #9, 29 mai 2026. Deuxième passe MARS-strat (5 voix : économie
solidaire/don, théoricien·ne des communs, juriste-économiste, méthodologue,
éditoriale-réception), cycle 2 en réactions croisées. Rouverte par l'opérateur
sur le constat que « économie paysanne » (round 1) amalgame deux finalités
distinctes. À lire après `03-synthese.md` (round 1).*

---

## 1. Verdict d'ensemble

Convergence très forte, et plus économe que prévu. Le round 1 graduait la
captation du **fonds** (le stock — à qui appartient le sol). Le round 2 traite la
finalité du **fruit** (le flux — comment circule ce que la terre produit, au
profit de qui). Découverte centrale, indépendamment trouvée par les cinq voix :
**cette distinction est déjà saisie dans la grille** — `usage_interet_general`
(axe 4) et `usage_non_marchand` (axe 5, gradué marchand/partagé/gratuit), tous
deux pondérés sur l'Indice. Sur Pommiers : « oui » et « partiel ». Mais ces
critères **ne remontent pas au verdict**.

Conséquence : le besoin de l'opérateur n'appelle **ni nouvel axe, ni re-division
de `nature_interet`, ni verdict bidimensionnel, ni champ saisi**. C'est un
**re-câblage** — faire lire au verdict des critères déjà là, exactement comme
`compute_verdict` lit déjà `vivant_finalite` + `place_au_vivant` pour distinguer
sanctuaire de hybride. Estimation : ~8 lignes.

---

## 2. La convergence (les cinq voix)

1. **Gate doux, au sommet seulement.** Le foncier commande le *plancher et le
   tranchant* (`marchand` / `hybride`), irréversiblement. La finalité d'usage ne
   peut **jamais faire descendre** un commun foncier vers `marchand` — elle peut
   seulement **conditionner la montée au sommet** (`sanctuaire`). Le paysan qui
   vend reste `hybride` plein, jamais `marchand` (anti-criminalisation — ligne
   rouge partagée par les cinq).

2. **Gradation, pas binaire.** `usage_non_marchand` est déjà gradué
   (oui/partiel/non) ; `partiel` est accepté pour le sommet, donc Pommiers
   n'est pas exclu. Un gate binaire viderait la catégorie et estampillerait
   « lucratif » ~80 % du corpus (constat d'observabilité du juriste : le
   non-lucratif d'intérêt général strict ≈ 10-20 % du corpus).

3. **Affichage : un verdict + une glose.** Pas deux jauges égales (le lecteur
   ferait la synthèse à la place du site). La glose **s'allume au positif** (elle
   marque le don, l'intérêt général, la gouvernance collective) et **se tait sur
   le banal** (la vente directe ordinaire n'est pas glosée). Le mot « marchand »
   est **banni de l'affichage de maillon/glose** ; il ne vit qu'au verdict de
   lieu, quand le fonds est captable.

4. **Deux critères distincts, jamais fusionnés.** « Intérêt général » (axe 4 —
   nourrir, servir, soigner) ≠ « non-marchand » (axe 5 — mode de circulation).
   Un GAEC bio est d'intérêt général ET marchand : les coller serait une faute
   (juriste). Le re-câblage lit deux mentions indépendantes.

5. **B et C sont morts par consensus.** B (champ `finalite_usage` saisi sur
   l'entité) viole L11 et refait la faille de la session #5. C (verdict 2D)
   casse `palier_for`, le couplage palier×verdict, déclenche L9 et multiplie
   les `inconnu`.

---

## 3. La décision résiduelle — ce que l'opérateur doit trancher

Une seule vraie divergence subsiste, et elle touche directement la posture du
site. **Qu'est-ce qui co-gate le sommet (`sanctuaire`), au-delà du foncier
irréversible et de l'habitat du vivant ?**

- **Option α — le non-marchand compte au sommet** (méthodologue « affirmatif »,
  économie-solidaire). Le sommet exige `usage_interet_general == oui` ET
  `usage_non_marchand ∈ {oui, partiel}`. *La non-lucrativité de l'usage est
  valorisée jusque dans le verdict.* C'est la lecture qui affirme le plus
  fortement la contre-culture non-lucrative — au cœur du jugement, pas seulement
  à l'affichage. Coût : un lieu d'intérêt général à gouvernance collective mais
  pleinement marchand (`usage_non_marchand: non`) est recalé du sommet.

- **Option β — seul l'intérêt général + la gouvernance co-gatent le sommet**
  (théoricien·ne des communs, soutenu par le juriste). `usage_non_marchand`
  reste un *score + glose*, jamais un gate. Argument (Ostrom) : un commun peut
  vendre et rester un commun ; la gouvernance collective d'un bien d'intérêt
  général **est** la définition du commun, le mode de circulation du fruit est
  second. Argument du juriste : le non-marchand est gradué, *réversible* et
  quasi-inobservable sur sources publiques — trop fragile pour gater un verdict
  irréversible. *La posture reste affirmée par la glose* (qui marque le don au
  positif), sans surcharger le verdict d'un critère réversible.

**Le point de bascule entre α et β** : un lieu à gouvernance collective, d'intérêt
général, mais qui **vend tout au marché** (`usage_non_marchand: non`). Sous α, il
n'atteint pas le sommet. Sous β, il le peut. (Pommiers, lui, est `partiel` : il
passe dans les deux options — la divergence ne le concerne pas.)

Ta posture déclarée — *soutenir une contre-culture citoyenne non-lucrative
d'intérêt général, assumée comme décalée du marché* — penche vers **α** (la
non-lucrativité valorisée jusqu'au verdict). Mais **β** affirme cette même
posture dans la **glose visible**, tout en gardant le verdict conceptuellement
pur (un commun se définit par la gouvernance, pas par la gratuité) et
empiriquement robuste (pas de gate sur une donnée réversible). Les deux servent
ta posture ; ils diffèrent sur *où* elle s'inscrit — dans le calcul du sommet
(α) ou dans l'affichage qui le commente (β).

---

## 4. Le wording de la glose (acquis, quelle que soit α/β)

La glose s'adosse aux critères déjà calculés, s'allume au positif :

- Pommiers : *Terre libérée · ferme nourricière en circuit court* (l'éditorial),
  ou *bien commun d'intérêt général · vente en circuit court* (le théoricien
  insiste pour nommer l'intérêt général et la gouvernance, pas le seul
  mode marchand).
- Cas de don/gratuité : *Terre libérée · économie du don et du partage*.
- Phrase de posture (accueil/méthode) : « Tous ces lieux servent un intérêt qui
  les dépasse — nourrir, abriter, soigner le vivant. Certains vont plus loin :
  ils font vivre une économie du don et du partage, décalée du marché. »

---

## 5. Conséquence consolidée (round 1 + round 2)

Le modèle final à deux dimensions, sans nouvel axe saisi :

- **Dimension foncier (round 1)** — captation du fonds, lue sur la chaîne
  (`nature_interet` du maillon × titre de l'articulation), un cran nouveau
  « exploitation agricole » → `hybride`. Commande le tranchant
  `marchand`/`hybride`/`sanctuaire`.
- **Dimension finalité d'usage (round 2)** — déjà dans la grille (axes 4 et 5),
  remontée au verdict en **co-gate du sommet** (α ou β) + **glose positive**.

**Pommiers** : foncier libéré (Fondation TDL, bail rural) → quitte `marchand`
pour `hybride` (round 1) ; usage `partiel` + intérêt général `oui` → reste
`hybride` (n'accède pas au sommet sanctuaire, qu'il ne revendique pas), avec
glose *ferme nourricière en circuit court*. Le bandeau « marchand » disparaît
dans les deux rounds, pour deux raisons cumulées.

---

## 6. Position de l'orchestrateur (à valider) et minorité

Je propose **β**, pour trois raisons : (a) elle affirme la posture là où le
lecteur la voit (la glose), sans charger le verdict irréversible d'un critère
réversible ; (b) elle respecte la définition du commun (gouvernance d'un bien
d'intérêt général) sans la réduire à la gratuité ; (c) elle est plus robuste à
l'observabilité (le juriste). **Mais c'est une décision de posture, pas
technique** : si tu veux que la non-lucrativité de l'usage pèse jusque dans le
verdict — affirmation maximale de la contre-culture — **α** est le bon choix, et
il est pleinement défendable.

**Minorité documentée** : l'économie-solidaire portait le mode de circulation
(don/troc) comme bien suprême ; le théoricien l'a contestée (« le don est une
qualité, pas le sommet ; le maraîcher en circuit court sous gouvernance
collective est plus pleinement un commun que le propriétaire qui donne sa
récolte »). Cette position minoritaire reste cohérente et alimente α — c'est
pourquoi α n'est pas écarté mais soumis à l'arbitrage.

---

*Fin de la synthèse round 2. La conclusion opérateur (α ou β + décisions
résiduelles du round 1) clôt l'Étape 0 et ouvre l'exécution de A1.*
