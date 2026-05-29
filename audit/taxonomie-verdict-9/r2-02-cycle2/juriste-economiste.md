# Cycle 2 — round 2 — voix juriste-économiste des structures agricoles et de l'ESS

*Réaction croisée. J'ai lu les cinq voix du cycle 1 round 2 : la mienne,
économie-solidaire-don, théoricien-communs, méthodologue-grille,
éditorial-reception. Amplifie / conteste / pas vu / position révisée, puis
les 4 cruxes.*

---

## 0. La convergence inattendue — et ce qu'elle cache

Surprise méthodologique : **les cinq voix convergent sur le diagnostic
structurel** — la finalité d'usage n'est pas un trou de la grille, elle y est
déjà, éclatée sur les axes 4 (`usage_interet_general`) et 5
(`usage_non_marchand`), gradués oui/partiel/non. Économie-solidaire, théoricien,
méthodologue et moi le disons mot pour mot. Personne ne réclame un champ saisi
nouveau (option B du méthodologue : écartée par tous). Personne ne veut criminaliser
le paysan qui vend. C'est rare et c'est solide.

Mais cette convergence cache un désaccord qui est **précisément mon terrain** :
le méthodologue, en §3 option A, propose de faire *remonter*
`usage_non_marchand`/`usage_interet_general` dans `compute_verdict` pour **gater
le sommet du verdict** (variante affirmative : la sanctuaire *exige*
`usage_non_marchand ∈ {oui, partiel}` ET `usage_interet_general: oui`). C'est
mécaniquement élégant — 8 lignes, réutilise le précédent D-B. Mais du point de
vue de l'**observabilité juridique**, gater un verdict sur ces deux champs pose
un problème que ni le méthodologue ni l'éditorial n'ont vu, et que je dois
porter seul. C'est le crux C-1.

---

## 1. Ce que j'amplifie

**Le théoricien (cas-test c) est mon meilleur allié, et je l'amplifie.** Le
collectif de don sur foncier propriétaire individuel — `usage_non_marchand`
excellent, foncier captable — *n'est pas un commun*. Cela prouve par l'absurde
que **le mode d'échange n'est pas le critère du verdict** : si le don gatait le
sommet, le donateur-propriétaire réversible deviendrait le champion de la carte
alors qu'il est à une succession près de la spéculation. La distinction
intérêt-général / non-marchand (mon crux C-4) trouve ici sa preuve : ce lieu est
généreux (mode d'échange = don) sans rien sécuriser ; généreux ≠ commun, et
non-marchand ≠ irréversible. Le don est **réversible** ; le foncier libéré est
**irréversible**. Gater un verdict irréversible sur un fait réversible est une
faute de droit.

**L'éditorial : « deux axes exigent deux vocabulaires » — j'amplifie fort.**
C'est juridiquement exact et c'est le piège que j'avais sous-estimé. « marchand »
sur le foncier (captation de rente) et « marchand » sur l'usage (vente d'un bien)
sont **deux faits de droit différents** : l'un est l'abusus du fonds, l'autre est
le caractère onéreux de l'échange (art. 1582 vs 1106 C. civ. — *à vérifier dans
la formulation, je ne cite pas de mémoire un article comme tranchant*). Le même
mot pour deux choses refait l'amalgame que le round 1 a tué.

---

## 2. Ce que je conteste

**Économie-solidaire, §3 — le gradient « subsistance/don → mixte → marchand
individuel » comme dérivé du seul couple (`usage_non_marchand` ×
`usage_interet_general`).** Je conteste non le gradient mais sa **fiabilité
inférentielle**. Le pôle « non-distribution effective » et « redistribution des
excédents » que la voix liste (§2) **ne sont pas observables** sur sources
publiques : l'affectation des excédents d'un GAEC, c'est la liasse fiscale —
introuvable. La voix mélange des marqueurs publics (gratuité, prix libre, troc
documenté) et des marqueurs financiers privés (non-distribution, redistribution
monétaire). Les premiers colorent honnêtement ; les seconds, si on les exige,
font exploser l'`inconnu`. Friction réelle : le gradient est juste, mais il ne
doit s'appuyer **que sur la moitié observable** de ses propres marqueurs.

**Méthodologue, variante affirmative.** Je conteste que `usage_non_marchand` et
`usage_interet_general` soient **assez robustes pour gater** le sommet du verdict.
Voir C-1.

---

## 3. Ce que je n'avais pas vu

**Le report au verdict est déjà dans le code (méthodologue §2).**
`compute_verdict` lit DÉJÀ `vivant_finalite`/`place_au_vivant` pour trancher
sanctuaire vs hybride. Je n'avais pas lu `generate_site.py` au cycle 1 ; je
croyais que tout report de grille au verdict serait une innovation à risque.
Faux : le mécanisme existe, voté. Cela change mon argument « pas un cinquième axe
saisi » : je maintiens *pas de champ saisi*, mais je dois admettre que *faire
remonter un critère existant au verdict n'est pas, en soi, une violation de
L11*. Le débat n'est donc plus « peut-on ? » mais « doit-on, vu la fiabilité de
la donnée ? ». C'est un déplacement net de ma position.

---

## 4. Les quatre cruxes

**C-1 — La finalité gate-t-elle le verdict ? Position révisée.**
Du point de vue de l'observabilité : **`usage_non_marchand` peut COLORER, il ne
doit pas GATER le sommet.** La raison est précise. Ce champ est saisi en
oui/partiel/non, mais sa valeur dérive de marqueurs publics *partiels* (mentions
« vente directe », « AMAP », « prix libre ») — pas de la non-lucrativité fiscale
de l'activité, qui exigerait gestion désintéressée + les « 4 P » (*seuils à
vérifier au BOFiP, je n'en pose aucun*). Or gater le **sommet** d'un verdict
irréversible sur une donnée *présomptive et partielle* crée un faux : un lieu
classé hors-sanctuaire « parce que `usage_non_marchand: non` » pourrait être un
GAEC en gestion désintéressée réelle qu'on n'a pas su lire, et inversement. La
donnée est assez robuste pour **nuancer une prose** ou **peser dans l'Indice**
(moyenne géométrique, déjà le cas), pas pour **bloquer un sommet**. Donc :
- je **rejette la variante affirmative** du méthodologue (sanctuaire exige le
  non-marchand) — elle gate sur du présomptif ;
- je **tolère sa variante minimale** SI et seulement si elle est lue comme un
  *signalement réversible* et non un gate dur : `usage_non_marchand: non`
  *affiché* comme « usage marchand » plutôt que basculant silencieusement le
  verdict. Coloration, pas verrou.
Ligne ferme : **le verdict irréversible se gate sur le foncier (fait
quasi-binaire, vérifiable : bail, RUP, verrou d'actif). Tout le reste colore.**

**C-2 — Affichage.** Je me range derrière l'éditorial : un verdict, une mention
de finalité en sous-ligne, pas deux jauges. Mais j'ajoute une exigence de
juriste : la mention doit dire un **fait d'échange** (« usage marchand », « usage
en partie hors-marché »), jamais un **statut fiscal** (« non-lucratif »). Écrire
« non-lucratif » en étiquette serait une affirmation de droit que les sources ne
soutiennent pas — risque de faux, voire de qualification erronée. « hors-marché »
décrit ce qu'on voit ; « non-lucratif » prétend qualifier ce qu'on ne voit pas.

**C-3 — Gradation contre binarisation. Confirmé sans réserve.** Le binaire
criminaliserait le paysan parce qu'il écraserait sur « lucratif » le GAEC bio en
vente directe (revenu de travail) et la SAS agro-industrielle (rente).
Juridiquement, ce sont deux choses : la vente directe d'un éleveur est la
rémunération de son travail (revenu paysan, art. L.722-1 C. rural — *cadre, pas
seuil*), pas une captation. La gradation marchand / partagé / gratuit est la
seule qui distingue le circuit court soutenable du marché spéculatif. Pommiers =
`partiel` doit rester un **état neutre**, pas une demi-faute. Le binaire est
rejeté par toutes les voix ; je verrouille le pourquoi juridique.

**C-4 — Intérêt général ≠ non-marchand. Tenu ferme, et je dis comment recâbler.**
Ce sont **deux critères de droit distincts** :
- *intérêt général* = la **finalité** (nourrir, servir, écologie, pédagogie) —
  axe 4 `usage_interet_general`. Un GAEC bio EST d'IG ET vend ET partage le
  bénéfice : les trois cohabitent sans contradiction.
- *non-marchand* = le **mode d'échange** (gratuité/don/troc vs prix) — axe 5
  `usage_non_marchand`.
La posture du site (« non-lucrative d'intérêt général ») les **compose** en un
slogan, mais en droit ce sont deux faits qu'on mesure séparément. **Comment ne
pas les confondre dans le re-câblage :** si une clause de `compute_verdict`
devait colorer le verdict, elle doit lire les **deux critères séparément** et
*ne jamais les fusionner en un seul booléen* « non-lucratif d'IG ». Le code du
méthodologue (`usage_ng = usage_non_marchand ∈ {oui,partiel} AND
usage_interet_general == oui`) fait exactement la fusion que je redoute : il
colle les deux critères en un ET. S'il faut une coloration, garder **deux
mentions dérivées indépendantes** — l'une de finalité (axe 4), l'autre de mode
d'échange (axe 5) — pour que la prose puisse dire « d'intérêt général » et
« marchand » dans la même phrase sans se contredire. C'est précisément le cas
Pommiers : IG = oui, marché = partiel.

---

## 5. Ligne rouge maintenue

N'inventer aucun seuil fiscal (gestion désintéressée, « 4 P », franchise :
**à vérifier au BOFiP**), ne fabriquer aucune catégorie non-lucrative
introuvable, ne jamais écrire « non-lucratif » en étiquette de verdict.
