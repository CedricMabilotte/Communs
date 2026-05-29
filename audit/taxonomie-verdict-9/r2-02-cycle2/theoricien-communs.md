# Round 2 — Cycle 2 — Voix théoricien·ne des communs & critique de l'extractivisme

*Réaction croisée. J'ai lu les cinq voix du cycle 1 round 2. Je réagis :
amplifie / conteste / pas vu / position révisée. J'engage les quatre cruxes.*

---

## 0. Ce que la lecture des autres a fait bouger

Première surprise, qui me désarme à moitié : **mes quatre interlocuteurs
convergent déjà sur l'ossature que j'avais posée** — verdict mono-axial sur le
foncier, finalité d'usage rendue visible mais non érigée en tranchant. Le
méthodologue (option A, report depuis les axes 4-5), le juriste (descripteur
dérivé non sanctionnant), l'éditorial (un verdict + une glose) et même
l'économie-solidaire (mention de finalité adossée, pas 4ᵉ verdict) atterrissent
au même endroit. Le danger d'une telle convergence, c'est qu'elle endorme le
crux. Je refuse l'endormissement : la vraie ligne de fracture n'est pas
*« axe vs glose »* (réglé), elle est **C-1 — la finalité gate-t-elle le sommet
du verdict ?** Et là, le méthodologue (option « affirmatif ») et l'économie-
solidaire poussent un couteau sous ma thèse. Je le prends au sérieux.

---

## 1. C-1 — le cas-test décisif. Je révise partiellement.

Le brief me met un cas que j'avais esquivé : **un foncier libéré (Fondation,
hors-marché, irréversible) dont l'usage est purement marchand individuel —
mérite-t-il quand même le HAUT du verdict ?**

Au cycle 1 j'aurais répondu sèchement « oui, le foncier commande ». La lecture
du méthodologue me force à distinguer ce que je confondais : **« haut du
verdict » n'est pas un seul cran.** Le code a trois niveaux et le sommet
(`sanctuaire`) est *déjà* conditionné par des critères de grille — pas seulement
par le foncier. Le méthodologue le démontre, code en main (§2) : la clause
finale de `compute_verdict` lit déjà `vivant_finalite` et `place_au_vivant` pour
distinguer sanctuaire de hybride. **Le précédent existe : le sommet du verdict
n'est PAS purement foncier aujourd'hui — il exige déjà une qualité au-delà du
fonds.**

Cela me retourne. Ma thèse « le foncier commande le verdict, la finalité colore »
était trop grossière. La version juste, révisée :

- **Le foncier commande le PLANCHER et le tranchant** (marchand / hybride). Un
  fonds captable plafonne le verdict, irréversiblement. Ça, je le tiens dur —
  c'est le cas-test (c) de mon cycle 1, non négociable : un propriétaire-donateur
  réversible n'accède jamais au commun foncièrement libéré, si généreux soit son
  usage.
- **Mais le SOMMET (sanctuaire) n'est pas commandé par le seul foncier — il ne
  l'a jamais été.** Il exige déjà une finalité (l'habitat du vivant). Donc faire
  remonter `usage_non_marchand` / `usage_interet_general` comme condition
  *supplémentaire du sommet* n'est pas une trahison de ma thèse : c'est la
  cohérence du sommet avec lui-même. Si le vivant gate le sommet, pourquoi la
  finalité d'usage ne le gaterait-elle pas ?

**Donc, sur le cas-test : un foncier libéré à usage purement marchand individuel
mérite le tranchant haut (il est bien un commun foncier — hybride), mais PAS le
sommet sanctuaire.** Le foncier lui donne l'accès au podium ; il ne lui donne pas
la marche du haut. C'est ma révision nette. La finalité ne gate pas *le verdict*
(plancher/tranchant), elle co-gate *le sommet*.

Ce qui sauve ma thèse de fond : **la finalité ne peut jamais faire DESCENDRE un
commun foncier au rang de marchand** (anti-criminalisation — ligne rouge 2 de
mon cycle 1, partagée par les cinq voix). Elle peut seulement **conditionner la
montée au sommet**. Asymétrie maintenue : le foncier a le pouvoir de plafonner ;
la finalité n'a que le pouvoir de couronner. Le paysan qui vend reste hybride
plein et entier — jamais marchand. Pommiers ne perd rien ; il n'accède
simplement pas à un sommet qu'il ne revendique pas.

---

## 2. C-4 — intérêt général (axe 4) vs non-marchand (axe 5) : je tranche net,
contre l'économie-solidaire.

C'est le crux où je m'écarte le plus de l'économie-solidaire, et le juriste me
donne raison sans le savoir (sa ligne rouge 5 : « ne pas confondre intérêt
général et non-lucrativité »).

**Du point de vue des communs, c'est l'axe 4 (intérêt général + gouvernance
collective) qui touche le cœur, PAS l'axe 5 (non-marchand).** Ostrom le dit
sans ambiguïté : une pêcherie gérée en commun *vend* son poisson, et reste un
commun. Ce qui la fait commune, c'est la gouvernance partagée d'une ressource au
service d'un intérêt qui dépasse les co-titulaires — pas la gratuité de la vente.
La non-marchandise de la vente (axe 5) est une *qualité de circulation du fruit*;
la gouvernance collective d'un bien d'intérêt général (axe 4 + structure/pouvoir)
est la *définition* du commun.

Conséquence pour le verdict : **si la finalité doit co-gater le sommet, le bon
gate est `usage_interet_general` (axe 4), pas `usage_non_marchand` (axe 5).** Un
commun peut vendre et rester au sommet s'il sert un intérêt général sous
gouvernance collective. Il ne devrait *pas* être recalé du sommet au seul motif
qu'il vend (axe 5 bas).

C'est mon désaccord central avec l'économie-solidaire : elle veut valoriser le
*mode de circulation* (don/troc/gratuité) comme le bien suprême. Pour les
communs, le mode de circulation est second. **Le maraîcher qui vend en circuit
court sous gouvernance collective d'un bien d'intérêt général est plus
pleinement un commun que le propriétaire individuel qui donne sa récolte.** Le
premier institue ; le second est généreux. Mauss décrit un lien social, pas une
institution du commun.

Je révise donc l'option du méthodologue : son test « affirmatif »
(`usage_non_marchand ∈ {oui,partiel}` ET `usage_interet_general: oui`) met les
deux critères à égalité comme conditions du sommet. **Je propose de dissocier :**
le gate fort du sommet = `usage_interet_general` (+ gouvernance, déjà dans les
axes 2-3) ; `usage_non_marchand` reste un *score* qui colore, pas un gate. Sinon
on recale Pommiers du sommet parce qu'il vend — exactement la pente que
l'éditorial (risque puriste, §2) et le juriste (ligne rouge 1) interdisent.

---

## 3. C-3 — gradation vs binaire. Conforte ma position, et le juriste l'arme.

Le juriste apporte ce que je n'avais pas vu (§3 de sa voix) : **la catégorie
« non-lucratif d'intérêt général strict » est minoritaire — peut-être 10-20 % du
corpus, à confirmer par comptage.** C'est un fait d'observabilité, pas de
théorie, et il conforte frontalement ma position d'écarter la finalité du
verdict-gate.

Le raisonnement : `usage_non_marchand` est gradué (oui/partiel/non) et
*réversible* — une ferme peut basculer au prix libre demain sans toucher sa
structure. Le foncier, lui, est binaire et irréversible. **On ne hisse pas une
propriété graduée et réversible au rang de tranchant catégoriel** : on
sanctionnerait un état conjoncturel (« vend cette année ») au même titre qu'un
état structurel (« fonds captable »). Le juriste ajoute la raison empirique : un
gate binaire sur axe 5 viderait le sommet et estampillerait « lucratif » 80 % du
corpus aimé. Gradation oui ; gate binaire non. **C-3 conforte que la finalité
reste hors du verdict-gate** — sauf le co-gate *intérêt général* du sommet
(§2), qui lui n'est pas le non-marchand.

---

## 4. C-2 — affichage 1D + glose. Je rejoins l'éditorial sans réserve.

Réglé par convergence. L'éditorial a raison : **un verdict + une glose de
finalité, pas deux jauges égales.** Deux titres = le lecteur fait la synthèse à
la place du site = décrochage. Le foncier commande le verdict affiché ; la
finalité le colore en sous-ligne. Mon seul ajout, depuis les communs : la glose
doit nommer l'**intérêt général et la gouvernance** (le cœur), pas seulement le
« hors-marché ». Une glose « usage marchand » sur un commun à gouvernance
collective d'intérêt général serait *fausse au sens des communs* — elle dirait
le mode de circulation et tairait l'institution. Préférer : « bien commun
d'intérêt général · vente en circuit court » plutôt que le seul « usage
marchand ».

---

## 5. Pas vu / amplifie

**Pas vu (et je l'amplifie) :** le méthodologue montre que mon « second axe » est
un *re-câblage*, pas une construction. Je l'avais pressenti (mes axes 4-5 cycle 1)
mais sans voir le précédent D-B dans le code. C'est décisif : ça enlève tout
prétexte de complexité à l'option qui co-gate le sommet par l'intérêt général.

**Je conteste, à l'économie-solidaire :** « la finalité doit être VISIBLE au
verdict » — oui ; « le pôle don/subsistance doit être valorisé positivement
comme le bien suprême » — non. C'est inverser la hiérarchie des communs. Le bien
suprême est l'institution collective d'un commun d'intérêt général, marchand ou
non. Le don est une qualité, pas le sommet.

---

## 6. Position révisée — synthèse

1. **Foncier = plancher + tranchant, irréversible, binaire.** Commande marchand /
   hybride. Le don ne fait pas le commun (cas-test (c) intact).
2. **Sommet (sanctuaire) co-gaté par l'intérêt général** (`usage_interet_general`
   + gouvernance), comme il l'est déjà par l'habitat du vivant. **Pas par le
   non-marchand.**
3. **Non-marchand (axe 5) = score + glose**, jamais gate, jamais cause de
   descente. Gradué, réversible, minoritaire en strict.
4. **Affichage 1D + glose** nommant l'intérêt général et la gouvernance, pas le
   seul mode de circulation.

Ce qui a bougé : j'ai admis que la finalité **co-gate le sommet** (révision de
« colore seulement »). Ce que je tiens : ce co-gate est l'**intérêt général**,
pas le **non-marchand** — et il ne peut jamais faire descendre, seulement
empêcher de monter.

---

*Fin de la réaction — Round 2, cycle 2, voix théoricien·ne des communs.*
