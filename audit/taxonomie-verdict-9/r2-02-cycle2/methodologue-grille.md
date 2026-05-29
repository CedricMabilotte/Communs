# Round 2 — Cycle 2 (réactions croisées) — voix méthodologue de la grille

*J'ai lu les cinq voix du cycle 1 round 2. Re-vérifié dans le code :
`compute_verdict` (l. 1290-1314), `palier_for` (l. 325-347),
`apply_palier_verdict_constraint` (l. 429-445), `grilles.yml` (axes 4 et 5,
l. 548-590), `ranking.yml` (paliers + `requiert_verdict`, l. 279-318). Je tiens
mon créneau : faisabilité, cohérence de calcul, L9, L11, parcimonie. Je ne
tranche ni le politique ni le juridique fin.*

---

## 0. Le point qui me saute aux yeux : convergence à cinq sur le diagnostic

Avant les frictions, une observation méthodologique forte. **Les cinq voix —
sans s'être lues — convergent sur le même fait : la finalité d'usage est DÉJÀ
dans la grille, sur les axes 4 (`usage_interet_general`) et 5
(`usage_non_marchand`), gradués, dérivés de sources publiques, testés sur
Pommiers.** L'économie-solidaire (§2 : « ces marqueurs existent DÉJÀ en
partie »), le théoricien (§3 : « les axes 4 et 5 SONT ce second axe »), le
juriste (§4 : « la grille a DÉJÀ ce qu'il faut, et c'est gradué »), l'éditorial
(§4 : « on nomme en clair deux axes qui existent déjà »), et moi-même.

Quand cinq angles disjoints (don, théorie, droit, réception, calcul) tombent sur
la même donnée, ce n'est pas une coïncidence : c'est que le modèle round 1 était
déjà bien découpé. **Le round 2 n'a pas découvert un trou ; il a découvert une
donnée saisie qui ne remonte pas.** Cela confirme mon option A et — point
décisif — **élimine l'option C par consensus** : personne, pas même le
théoricien ni l'éditorial, ne réclame un verdict 2D matriciel. Le théoricien
écrit « 1D enrichi, pas 2D catégoriel » ; l'éditorial « NON à deux jauges
égales » ; le juriste « pas un verdict à deux dimensions affiché ». **C est
mort au cycle 1.** Je n'ai plus à le défendre contre, je l'enregistre.

Et **B est mort aussi** : personne ne demande un champ saisi sur l'entité. Même
le juriste, que j'attendais sur le descripteur, le veut *dérivé* (« calculé par
le générateur à partir de marqueurs déjà présents »), pas saisi. L11 tient à
cinq voix. Le débat réel s'est resserré sur **un seul terrain** : la finalité
remonte-t-elle au **verdict** (mon A, version affirmative), ou seulement à
l'**affichage** (la sous-ligne de l'éditorial, le descripteur du juriste, la
mention du théoricien) ? C'est là que je dois trancher concrètement.

---

## C-1 (central) — Si la finalité « remonte au verdict », CONCRÈTEMENT comment ?

J'amplifie ma position d'une précision que le cycle 1 m'a forcé à faire, et je
**révise** sur un point : **la finalité ne doit gater QUE le sommet, jamais le
bas — et même au sommet, le bas mot est dangereux.**

**La clause, telle que je la recommande maintenant** (extension de la l. 1314,
la seule touchée) :
```python
db_vert  = g.get("vivant_finalite") == "oui" and g.get("place_au_vivant") == "oui"
usage_ng = g.get("usage_non_marchand") in ("oui", "partiel") \
           and g.get("usage_interet_general") == "oui"
return "sanctuaire" if (irrev and db_vert and usage_ng) else "hybride"
```
**Ça gate le sommet, point.** La sanctuaire est déjà le seul verdict qui lit la
grille (les trois autres branches — `marchand`, `hybride`, `None` — tranchent
sur la chaîne foncière en amont, l. 1304-1309, et restent intactes). Ajouter
`usage_ng` ne modifie **que** la dernière ligne : elle décide, pour une chaîne
*déjà entièrement non-lucrative et irréversible*, si elle monte en `sanctuaire`
ou retombe en `hybride`. **Le bas du verdict (`marchand`, `hybride`) ne bouge
pas d'un iota.** C'est exactement le geste que le code fait déjà pour `db_vert` :
la finalité d'usage devient une troisième condition de sommet, sœur de l'habitat
du vivant. Aucun nouveau mécanisme.

**Articulation avec le couplage palier×verdict (vérifié, l. 282 + 337-345).**
C'est le risque que je n'avais pas assez creusé au cycle 1, et il est réel. Le
palier `abouti` (min 70) porte `requiert_verdict: sanctuaire`. Donc **gater le
sommet du verdict gate AUSSI mécaniquement le sommet du palier** : un lieu qui
perd la sanctuaire pour cause d'usage marchand est dégradé par `palier_for` du
palier `abouti` vers `solide`, *quel que soit son IdL ≥ 70*. C'est un double
effet — verdict ET palier — pour une seule clause. Ce n'est pas un bug, c'est le
design de session #5 (le couplage est voulu). Mais ça **amplifie le risque de
vider le sommet** que je signalais : si `usage_ng` est trop strict, on ne perd
pas seulement le badge `sanctuaire`, on ferme aussi le palier `abouti` à tout le
corpus marchand.

**Le risque Pommiers, chiffré par la convergence.** Pommiers a
`usage_non_marchand: partiel` et `usage_interet_general: oui`. Avec ma clause
(`partiel` accepté), Pommiers **passe** le test d'usage — il ne perd la
sanctuaire que sur `db_vert` (habitat du vivant), comme aujourd'hui. **Donc ma
version n'aggrave pas Pommiers.** Mais le juriste apporte un chiffre que je dois
prendre au sérieux : la quasi-totalité du corpus est `partiel` ou `non` sur
`usage_non_marchand` (vente directe = marchand). Si je durcissais en exigeant
`usage_non_marchand == "oui"` (don pur), je viderais le sommet — exactement la
faute que les quatre autres voix appellent « criminaliser le paysan qui vend ».
**Donc : `partiel` DOIT être accepté.** La gradation du critère (C-3) est ce qui
sauve la clause du purisme.

**Position révisée.** Au cycle 1 je proposais « minimal d'abord » (faire
basculer `usage_non_marchand == "non"` vers `hybride` explicite). Je **retire ce
volet** : il touche le *bas* (il déclasserait une chaîne non-lucrative vers
hybride sur le seul motif d'usage marchand), et c'est précisément ce que le
théoricien (ligne rouge 2) et le juriste (ligne rouge 1) interdisent. **Je ne
garde que le volet affirmatif, et seulement au sommet.** Ma clause ne *retire*
rien à personne sous la sanctuaire ; elle *ajoute* une exigence pour y entrer.
Conservatrice par construction.

---

## C-2 — « verdict + sous-ligne de finalité » (éditorial) : compatible avec A sans casser L9 ?

**Oui, totalement — et c'est même la moitié manquante de ma proposition.**
L'éditorial a raison sur un point que je n'avais pas couvert : faire remonter
`usage_ng` au verdict gate le sommet, mais **ne rend pas la finalité *lisible*
pour les lieux qui n'atteignent pas le sommet** (Pommiers, hybride, restera
`hybride` sans qu'on voie *pourquoi* côté usage). Le verdict tranche ; il ne
raconte pas. La sous-ligne de l'éditorial comble ce trou, et **les deux
dispositifs sont orthogonaux et cumulables** :

- **Le verdict** (mon A) : `usage_ng` est une condition de la sanctuaire. Trois
  valeurs, inchangées. Zéro effet rendu.
- **La sous-ligne** (éditorial) : une *glose dérivée* affichée sous le badge,
  calculée du même couple (`usage_non_marchand` × `usage_interet_general`) déjà
  en mémoire. **Pas un nouveau verdict** — un libellé. « usage hors-marché » /
  « usage en partie hors-marché » / « usage marchand », au choix de l'éditorial.

**L9 — comment exposer la finalité sans nouveau verdict.** La sous-ligne est un
**ajout de rendu** (nouvel élément sous le badge, nouveau libellé, peut-être une
classe CSS). Donc, contrairement à la clause de verdict (pur calcul, zéro
rendu), **la sous-ligne déclenche L9 : aperçu HTML autonome d'une fiche affectée
avant de considérer le changement abouti.** C'est la seule des deux moitiés qui
touche la mise en page. Je le signale explicitement : *la mécanique du verdict
n'exige pas d'aperçu ; la sous-ligne, si.* Ne pas les confondre. Et la sous-ligne
n'est **pas** un second juge (la ligne rouge 3 de l'éditorial) : elle dérive d'un
fait déjà calculé, subordonnée visuellement, elle ne re-tranche rien.

Donc ma réponse à C-2 : **A (verdict) et la sous-ligne (affichage) ne se
concurrencent pas, ils se complètent.** Le verdict gate le sommet ; la sous-ligne
rend la finalité lisible *partout*, y compris sous le sommet. Aucun nouveau
verdict, aucun champ saisi. C'est la combinaison que je recommande désormais.

---

## C-3 — Gradation : `usage_non_marchand` est-il exploitable tel quel ?

**Confirmé, vérifié l. 586-590.** `usage_non_marchand` est déjà `oui / partiel /
non` avec une définition opérationnelle : « partiel si une part marchande
coexiste avec une logique de partage ; non si l'accès est tarifé au prix du
marché ». **Aucune transformation requise.** Ma clause lit `in ("oui",
"partiel")` directement. La gradation est même *ce qui rend la clause
défendable* : sans elle, il faudrait choisir entre exclure Pommiers (purisme) ou
ne rien gater. Avec elle, je place le seuil **entre `partiel` et `non`** —
exactement la frontière que les quatre autres voix décrivent comme la limite à
ne pas criminaliser. La gradation existante porte le compromis.

Une réserve de calcul : `inconnu` n'est pas une valeur du gradient mais reste
possible (champ non renseigné). Vérifié : un `inconnu` sur `usage_non_marchand`
ferait simplement échouer `usage_ng` → retombée en `hybride`. **Dégradation
gracieuse**, comme `db_vert` aujourd'hui. Pas d'explosion d'`inconnu` : on ne
crée pas de case indéterminée nouvelle, on ferme juste l'accès au sommet faute
de preuve. `inconnu` reste sacré.

---

## C-4 — Axes 4 et 5 : composer les deux, ou n'en lire qu'un ?

J'ai lu les définitions réelles (l. 552-559 et 582-590). **Ce sont deux critères
distincts, et il faut composer les deux — en ET — pour le verdict.** Voici
pourquoi, et c'est le juriste qui me l'a démontré sans le vouloir (sa ligne
rouge 5) :

- `usage_interet_general` (axe 4) = la **finalité** : l'activité dépasse-t-elle
  ses occupants (nourrir, écologie, pédagogie) ? Pommiers = oui.
- `usage_non_marchand` (axe 5) = le **régime** : gratuité/don/troc vs prix du
  marché ? Pommiers = partiel.

Le juriste : « ne pas confondre intérêt général (finalité) et non-lucrativité
(régime économique). Un GAEC bio EST d'intérêt général ET lucratif au sens
fiscal. Les deux ne s'excluent pas. » **Exact — et c'est l'argument pour les
composer, pas pour n'en lire qu'un.** Si je ne lisais que l'axe 5
(`usage_non_marchand`), je tamponnerais « pas sanctuaire » sur un lieu marchand
d'intérêt général sans voir l'intérêt général. Si je ne lisais que l'axe 4, je
sanctifierais un lieu non-marchand mais replié sur lui-même. **La posture du
site — non-lucratif *d'intérêt général* — est littéralement la conjonction des
deux axes.** L'expression de l'opérateur n'est pas un critère, c'est un ET de
deux critères qui existent déjà. La clause `usage_non_marchand in ("oui",
"partiel") AND usage_interet_general == "oui"` est la traduction exacte, mot pour
mot, de la décision opérateur.

Donc : **composer en ET, pas en lire un seul.** Et le ET est asymétrique, ce qui
est correct : on tolère `partiel` côté régime (le paysan vend pour vivre) mais on
exige `oui` côté finalité (l'intérêt général n'est pas négociable pour la
sanctuaire). C'est le bon réglage — il accueille Pommiers et exclut le marchand
replié.

---

## Frictions résiduelles (les vraies)

- **Avec le théoricien** : il refuse *tout* report au verdict (« le verdict reste
  mono-axial sur le foncier… on habille l'explication, on ne recâble pas »). Vraie
  friction. Ma réponse : le verdict n'est *déjà pas* mono-axial foncier — il lit
  `vivant_finalite`/`place_au_vivant` (grille, pas foncier) pour le sommet
  (l. 1313). Le sommet est *déjà* multi-critères. Ajouter `usage_ng` ne franchit
  aucune nouvelle frontière conceptuelle ; ça étend une lecture de grille
  existante. Son « 1D enrichi » et mon « A au sommet seulement » sont plus proches
  qu'il ne le croit : je ne touche que le sommet, comme l'habitat du vivant.
- **Avec le juriste** : son chiffre (corpus à 80 % `partiel`/`non`) est mon
  garde-fou, pas mon adversaire. Il prouve que `partiel` DOIT être accepté. On
  converge.
- **Avec l'éditorial** : aucune friction — sa sous-ligne est la moitié affichage
  de ma proposition. Je porte juste l'avertissement L9 qu'il délègue.

---

*Position de cycle 2 : option A confirmée et resserrée au sommet seul + sous-ligne
dérivée pour la lisibilité. C écartée par consensus, B par L11. À porter en
cycle 3 (synthèse).*
