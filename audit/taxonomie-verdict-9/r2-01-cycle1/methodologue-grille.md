# Round 2 — Cycle 1 (divergence isolée) — voix méthodologue de la grille

*MARS-strat round 2, projet Communs / Terres Libérées. Crux du round 2 : la
**finalité d'usage** (non-lucrative d'intérêt général vs lucrative d'intérêt
individuel) est-elle un SECOND AXE orthogonal au foncier, une re-division du cran
`nature_interet`, ou — l'hypothèse que je vais défendre — un re-câblage de
critères de grille DÉJÀ présents vers le verdict ? Je tiens mon créneau :
faisabilité, cohérence de calcul, L11, source unique, parcimonie. Je ne tranche
ni le politique ni le juridique fin. Lecture faite de `config/grilles.yml`,
`lieux/ferme-de-pommiers.yml`, et de `compute_verdict` / `score_fiche` /
`palier_for` / `_pire_nature_chaine` dans `generate_site.py`.*

---

## 1. Inventaire — ce que la grille capture DÉJÀ sur la finalité d'usage

J'ai lu la grille `lieu` ligne à ligne. La finalité d'usage que l'opérateur
veut distinguer **est déjà saisie**, et pas par un seul critère — par plusieurs,
répartis sur deux axes :

**Axe 4 — La finalité (intérêt général)** :
- `usage_interet_general` (poids **3**) — « L'activité du lieu […] sert un
  intérêt qui dépasse ses occupants. » (grilles.yml l. 552-559)
- `ancrage_territorial` (poids 2) — utilité au territoire, ouverture au-delà des
  résidents.
- `vivant_finalite` (poids 2) — le vivant non-humain dans la finalité.

**Axe 5 — L'usage (régime non marchand)** :
- `usage_non_marchand` (poids **3**) — « gratuité, le don, le troc ou une
  contribution modique. *partiel* si une part marchande coexiste avec une
  logique de partage ; *non* si l'accès est tarifé au prix du marché. »
  (grilles.yml l. 582-590)
- `loyer_non_rentier` (poids 2), `securite_jouissance` (poids 3),
  `usage_non_degradant` (poids 3), `place_au_vivant` (poids 3).

La distinction même que le brief décrit — (1) don/troc/gratuité/redistribution/
soin du vivant vs (2) commerce/bénéfice réparti/patrimoine — est **exactement**
le contenu de `usage_non_marchand` (gradation marchand/partagé/gratuit) croisé
avec `usage_interet_general` (au service de qui ?). Le cas-test du brief — un
GAEC bio sur bail qui vend au marché — est précisément ce que la fiche Pommiers
encode aujourd'hui : `usage_non_marchand: partiel` (« vente fromagère en circuit
court », l. 83-85) et `usage_interet_general: oui` (« vocation agricole et
sociale », l. 77-79).

**Donc : la finalité d'usage n'est pas une donnée manquante. C'est une donnée
saisie, pondérée, qui alimente le calcul — mais seulement l'Indice, pas le
verdict.** C'est le point décisif de mon diagnostic.

**Où elle va dans le calcul (vérifié).** `score_fiche` (l. 200-224) agrège
chaque critère par son axe via `acc[axe]`, et l'Indice est la moyenne
**géométrique** des cinq axes (`geometric_idl`, non compensatoire). Donc un
`usage_non_marchand: non` (facteur de pénalité sur l'axe 5) **fait déjà
chuter l'Indice** d'un lieu — d'autant plus que la moyenne géométrique pénalise
les axes bas sans qu'un axe haut puisse compenser. La finalité lucrative est
**déjà sanctionnée dans l'Indice**. Ce qu'elle ne touche pas, c'est le
**verdict**.

---

## 2. Le besoin du round 2 est-il neuf, ou un re-câblage de l'existant ?

Re-câblage, à 90 %. Voici la démonstration.

`compute_verdict` (l. 1290-1314) procède en deux temps :
1. **Tranche sur la chaîne (foncier)** : si un maillon est `commerciale`/
   `privee_individuelle` → `marchand` ; si `commerciale_encadree` → `hybride` ;
   si `inconnu` → `None`.
2. **Pour une chaîne entièrement non-lucrative**, il lit **DÉJÀ des critères de
   grille** (l. 1311-1314) :
   ```python
   g = {c["critere"]: c["valeur"] for c in fiche.get("grille") or []}
   irrev   = g.get("foncier_hors_marche")=="oui" and g.get("irreversibilite")=="oui"
   db_vert = g.get("vivant_finalite")=="oui"   and g.get("place_au_vivant")=="oui"
   return "sanctuaire" if (irrev and db_vert) else "hybride"
   ```

**Le précédent est là, dans le code, déjà voté.** Le verdict lit *déjà* des
critères de grille (`vivant_finalite`, `place_au_vivant`, `foncier_hors_marche`,
`irreversibilite`) pour distinguer sanctuaire de hybride. Faire remonter
`usage_non_marchand` / `usage_interet_general` dans cette même clause **n'invente
aucun mécanisme** : c'est strictement la même opération que celle qui existe
pour les critères « habitat du vivant » (D-B). On étend une lecture existante,
on n'en crée pas une.

Ce qui est neuf, ce n'est donc pas un *besoin de données* ni un *besoin de
mécanisme*. C'est un **choix de pondération éditorial** : aujourd'hui une chaîne
hors-marché irréversible **mais marchande à l'usage** (Pommiers : GAEC qui vend
au marché) atterrit en `hybride` faute de remplir le test D-B vivant. Le round 2
demande : un usage lucratif d'intérêt individuel doit-il **bloquer** la montée,
ou **être tranché** explicitement, plutôt que de rester invisible au verdict et
de ne peser que dans l'Indice ? C'est une question de seuil, pas d'architecture.

**Conclusion de §2 : le besoin du round 2 est, pour l'essentiel, le re-câblage
de deux critères de grille déjà saisis vers la clause finale de
`compute_verdict` — le mécanisme exact que le code emploie déjà pour D-B.**

---

## 3. Les trois options — coût et risque

### Option A — Ne rien ajouter ; faire remonter `usage_non_marchand` / `usage_interet_general` au verdict

**Mécanique.** Étendre la clause finale de `compute_verdict` (l. 1311-1314). La
sanctuaire exige déjà foncier irréversible + habitat du vivant ; on ajoute une
condition de finalité d'usage. Exemple minimal, cohérent avec la posture du
site (contre-culture non-lucrative d'intérêt général) :
```python
usage_ng = g.get("usage_non_marchand") in ("oui","partiel") \
           and g.get("usage_interet_general") == "oui"
return "sanctuaire" if (irrev and db_vert and usage_ng) else "hybride"
```
Et, si l'on veut que l'usage purement marchand soit *visiblement* tranché au
sein d'une chaîne par ailleurs non-lucrative, on peut faire basculer
`usage_non_marchand == "non"` (accès tarifé au prix du marché) sur `hybride`
explicite plutôt que de le laisser au silence.

**Coût** : ~3-8 lignes dans une fonction unique. Aucun nouveau champ
(`usage_non_marchand`/`usage_interet_general` existent dans toutes les fiches
lieu). Aucune nouvelle clé `id`, aucune table de plafonds touchée, aucun
nouveau verdict. `palier_for` / `apply_palier_verdict_constraint` inchangés (le
verdict reste à 3 valeurs). Pas de churn de migration. Pas de risque d'`inconnu`
nouveau : ces critères sont déjà renseignés ou déjà `inconnu` (et un `inconnu`
sur eux ferait simplement échouer le test sanctuaire → `hybride`, dégradation
gracieuse, exactement comme le test D-B aujourd'hui).
**L9** : aucune modification de rendu (mêmes 3 verdicts, mêmes classes CSS) —
pas d'aperçu HTML requis pour la mécanique. (Si l'on retouche la *prose* qui
explique le verdict, oui, mais c'est un autre chantier.)

**Risque** : faible. Le seul vrai risque est de **durcir le seuil sanctuaire**
au point de vider la catégorie (combien de lieux ont `usage_non_marchand: oui`
ET `usage_interet_general: oui` ET D-B vivant ET foncier irréversible ? très
peu). Mais ce risque est **paramétrable** : `partiel` accepté ou non, et la
règle peut ne porter que sur le **blocage du marchand pur** plutôt que sur
l'**exigence du non-marchand pour la sanctuaire**. À calibrer empiriquement à la
régénération, comme le plafond ax2=40 du round 1 (décision D2).

### Option B — Un descripteur orthogonal sur l'usufruitier (`finalite_usage` saisi par entité)

**Mécanique.** Nouveau champ `finalite_usage: ig_non_lucratif | individuel_lucratif`
sur les fiches usufruitier, lu par le verdict.

**Coût et risque** : c'est la solution que la grille rend **inutile et
dangereuse**. (a) Nouveau champ saisi = nouvelle source de vérité à tenir et à
garde-fouder — **violation directe de L11** (« le verdict se calcule, ne se
saisit pas ») et de la source unique. (b) **Redondance** avec
`usage_non_marchand`/`usage_interet_general` déjà saisis : deux faits encodant
la même chose, qui peuvent se contredire (exactement la faille de session #5,
grille vs nature_interet, qui a motivé `apply_lieu_plafond_chaine`). (c) Surtout :
la finalité d'usage est **relationnelle et locale au lieu**, pas une propriété
de l'entité — c'est l'enseignement du round 1 répliqué. Un même GAEC peut vendre
au marché sur un lieu et faire de la distribution gratuite sur un autre. Mettre
`finalite_usage` sur l'usufruitier referait l'erreur que le round 1 a corrigée
pour `nature_interet` (le théoricien avait retiré sa demande d'un
`nature_interet` relationnel saisi). **B est l'anti-pattern.** À écarter.

### Option C — Un verdict bidimensionnel (foncier × finalité d'usage)

**Mécanique.** Le verdict cesse d'être un scalaire à 3 valeurs et devient un
couple `(captation_foncier, finalite_usage)`, ex. 3×3 = 9 cases.

**Coût** : massif et systémique.
- `compute_verdict` renvoie un tuple → tous ses appelants cassent
  (`apply_palier_verdict_constraint` l. 441, `verdict_badge` l. 1317,
  l'export JS, le filtre de cartes).
- `palier_for` (l. 325-347) teste `verdict != req` sur un **scalaire** ; le
  couplage palier×verdict (`requiert_verdict: sanctuaire`) devrait être réécrit
  pour un couple, et la question politique « quel palier requiert quelle
  case ? » s'ouvre sur 9 cases au lieu de 3.
- **L9** : nouveau rendu (badge composite, légende, couleurs, classes CSS pour
  N cases) → aperçu HTML autonome obligatoire.
- Prose : tout le triptyque verdict (concepts.yml, ranking.yml, pages
  méthode/régimes/glossaire) à réécrire pour une matrice.
- **Risque d'`inconnu`** : une 2ᵉ dimension dérivée de critères qui peuvent être
  `inconnu` (Pommiers a `loyer_non_rentier: inconnu`) multiplie les cases
  partiellement indéterminées → explosion des « à établir ».

**Pour quel gain ?** Aucun gain de *calcul* : la finalité d'usage est déjà dans
l'Indice (axes 4 et 5), et son report au verdict est obtenu par l'option A en
8 lignes. C reconstruit une cathédrale pour ce qu'un linteau porte déjà. À
écarter sauf démonstration éditoriale qu'un **affichage matriciel public** est
indispensable — ce qui serait une décision politique assumée, pas une contrainte
technique (parallèle exact avec le 4ᵉ verdict écarté au round 1, T-c).

---

## 4. Recommandation de cohérence

**Option A.** La finalité d'usage n'est ni un second axe à créer, ni une
re-division de `nature_interet` : c'est une donnée **déjà capturée par la grille
sur deux axes** (4 et 5) qui pèse **déjà sur l'Indice** mais ne **remonte pas au
verdict**. Le correctif juste et parcimonieux est de la faire remonter, en
réutilisant le mécanisme **exact** que `compute_verdict` emploie déjà pour les
critères « habitat du vivant » (D-B).

Deux niveaux de report, à arbitrer par l'éditorial/l'opérateur (pas par moi) :
- **Minimal** : `usage_non_marchand: non` (accès au prix du marché) sur une
  chaîne par ailleurs non-lucrative bascule explicitement le verdict en
  `hybride` au lieu de rester silencieux. Rend visible le « lucratif d'intérêt
  individuel » sans nouvelle case.
- **Affirmatif** : la `sanctuaire` exige en outre `usage_non_marchand ∈
  {oui, partiel}` ET `usage_interet_general: oui`. Cale le sommet du verdict sur
  la posture non-lucrative d'intérêt général du site.

Je recommande le **minimal d'abord** (réversible, peu d'effet de bord, calibrage
visible à la régénération), l'affirmatif en second temps si la passe montre que
des lieux marchands d'intérêt individuel atteignent encore la sanctuaire. C'est
la même discipline empirique que le plafond ax2=40 (D2 du round 1).

**Articulation avec le round 1.** Le round 1 a tranché la captation du
**foncier** (chaîne × titre). Le round 2 tranche la finalité de l'**usage**
(critères de grille du lieu). Les deux vivent **dans le même `compute_verdict`**,
sur deux blocs successifs : d'abord la chaîne (foncier), puis la grille
(habitat du vivant + finalité d'usage). C'est une stratification, pas une
seconde dimension — le verdict reste **un scalaire à 3 valeurs**.

---

## 5. Désaccords prévisibles

- **Le théoricien / l'éditorial voudront un verdict 2D** (option C) pour rendre
  la finalité d'usage *visible comme telle*. Je répondrai : la visibilité est un
  problème d'affichage (badge, prose d'explication du lieu), pas de structure de
  verdict ; et l'Indice + les axes 4/5 affichent déjà la finalité. Reproduit le
  débat 3-vs-4-niveaux du round 1.
- **Le juriste voudra un descripteur d'entité** (option B) pour « ancrer » la
  finalité dans la forme. Je maintiens : relationnel, donc dans le lieu, pas
  dans l'entité — sinon on refait la faille session #5.
- **On me dira « A enfouit la finalité dans le calcul, c'est implicite ».** Non :
  l'Indice la chiffre (géométrique, non-compensatoire), et le report A la rend
  *tranchante* au verdict. L'implicite devient explicite sans nouvelle donnée.
- **Calibrage** : combien de lieux perd la sanctuaire avec l'option affirmative ?
  Inconnu avant régénération. Je refuse de chiffrer un seuil sans la passe.

---

## 6. Lignes rouges

- **L11 — le verdict se calcule, ne se saisit pas.** L'option A est la seule des
  trois qui respecte L11 sans réserve : zéro nouveau champ. B le viole
  frontalement. C l'amplifie (plus de cases dérivées d'`inconnu`).
- **Source unique de vérité.** La finalité d'usage est déjà saisie une fois
  (`usage_non_marchand`, `usage_interet_general`). En créer une deuxième (B)
  rouvre la contradiction grille↔donnée que session #5 a fermée.
- **Parcimonie.** Le mécanisme de report existe déjà (D-B). Ne pas inventer de
  table, de clé, de verdict, de dimension pour ce qu'une clause de 8 lignes
  porte. « On habille, on ne recâble pas. »
- **« Le verdict se calcule » ne doit pas casser.** A ne touche ni la signature
  de `compute_verdict`, ni `palier_for`, ni le couplage palier×verdict. C les
  casse tous.
- **`inconnu` reste sacré.** A dégrade gracieusement (un critère `inconnu` fait
  juste échouer le test sanctuaire → `hybride`), comme le test D-B aujourd'hui.
  Pas d'explosion d'`inconnu`.

---

*Position isolée de cycle 1, à confronter au cycle 2. Je n'ai lu aucune autre
voix du round 2. Recommandation : option A, report minimal d'abord, calibrage
empirique à la régénération.*
