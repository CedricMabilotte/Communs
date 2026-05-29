# Cycle 1 — Voix de l'autonomie (Illich), posture red-team

*Mini-strat « travail décommodifié », session #10. Voix isolée. Critère : l'autonomie
réelle des personnes qui font vivre le lieu. On défend ce que le projet PERDRAIT en
réduisant le co-gate du travail au seul salariat de marché.*

---

## Position d'ouverture (ce que je ne conteste pas)

Je ne rejette ni l'organisation, ni l'autorité, ni la coordination. Le cadre #9 §4.5 le
dit déjà : « le cadre retient la critique de la subordination, non un rejet de toute
organisation ». Une rotation des tâches décidée ensemble, un référent technique reconnu
pour sa compétence, un conseil élu révocable — rien de tout cela n'est une oppression, et
en faire un drapeau rouge serait absurde. Je concède aussi le point central de la voix
adverse : **une autorité peut être librement choisie**, et une coordination choisie n'est
pas une subordination marchande. Mon objection n'est pas « gardez la subordination telle
quelle ». Elle est : *avant de jeter le mot « subordination », regardez ce qu'il attrape
et que « salariat » laisse filer.*

## 1. Ce que la subordination-critique attrape, et que le salariat manque

Le salariat est un fait juridico-comptable étroit : fiche de paie, lien de subordination
au sens du Code du travail, vente de temps contre argent. C'est précisément sa force
(observable, §8) — et sa cécité. Quatre cas concrets où l'hétéronomie existe **sans**
salaire, donc échappe à un co-gate « non-salariat seul » :

- **Le leader charismatique / dérive de gourou.** Une communauté de partage intégral
  (cadre #9 §6.2, type 1 — celle qui est *proche du sommet*) sans aucun salarié, où les
  décisions, l'accès aux ressources, l'entrée et la sortie dépendent du bon vouloir d'un
  fondateur. Décommodifiée au sens strict (0 € de salaire) — mais l'autonomie des membres
  y est nulle. Le salariat-seul délivre un blanc-seing à ce lieu ; la subordination, lue
  comme hiérarchie de commandement *de fait*, le retient.

- **La corvée / le travail gratuit extorqué.** Un « bénévolat » obligatoire sous peine
  d'exclusion, des heures non comptées extraites au nom du collectif. Pas de salaire, donc
  pas de marchandisation polanyienne — mais pas libre non plus. C'est exactement le
  *travail fantôme* d'Illich (1981, cité §4.1) : le travail non rémunéré et non reconnu
  comme tel, qui n'apparaît dans aucun registre.

- **La division genrée du travail domestique non rémunéré.** Le cas paradigmatique du
  travail fantôme. Décommodifié au sens le plus strict (jamais vendu) et pourtant assigné,
  contraint, hétéronome. Un critère « non-salariat = bon » l'invisibilise totalement.

- **Le « stagiaire perpétuel » / l'apprenti dépendant.** Travail réel rémunéré
  symboliquement ou en nature, hors du salariat formel. Dépendance sans contrat.

Ces quatre cas partagent une structure : **décommodifiés au sens de Polanyi, non libres au
sens d'Illich.** Le co-gate actuel `non_subordination` (« non-salariat + absence de
hiérarchie de commandement ») a un second terme précisément pour eux. Le retirer, c'est
créer un angle mort nommé.

## 2. L'attaque du « librement choisi » — et sa limite

La thèse adverse repose sur « une autorité peut être *librement* choisie ». Je conteste le
*librement*, mais avec discipline.

**L'attaque.** Le consentement à l'autorité est rarement formé dans des conditions
neutres. Trois dépendances le vicient : (a) **économique** — sortir du lieu, c'est perdre
le toit et le revenu de subsistance ; (b) **affective** — rompre avec le groupe, c'est
perdre ses liens, parfois sa famille recomposée ; (c) **communautaire / idéologique** — la
sortie est vécue comme trahison. Sous ces dépendances, le consentement formel (« j'ai
choisi de rester, donc j'accepte ») peut n'être qu'une rationalisation de l'absence
d'alternative. Le salariat de marché a, paradoxalement, un garde-fou que la communauté
intégrale n'a pas : la **liberté de démissionner** vers un autre employeur. C'est une
ironie qu'il faut assumer — le marché du travail, que Polanyi critique, offre une *exit*
que le collectif fusionnel peut supprimer.

**La limite (honnêteté red-team).** Mais je ne peux pas, et le projet ne doit pas,
transformer le sommet en **test d'autonomie psychologique inobservable**. Savoir si un
consentement est « réellement » libre exige d'entrer dans les têtes — c'est exactement ce
que le cadre refuse (§10, biais déclaratif ; §8, on ne gate que l'observable). Donc :
le consentement EST réellement libre, *aux fins du modèle*, lorsqu'il y a **réversibilité
opposable** : statuts qui garantissent un droit de sortie sans spoliation (récupération de
l'apport, pas de clause léonine), une gouvernance révocable, l'absence de captation des
moyens de subsistance individuels par le collectif. C'est observable. L'inobservable (le
for intérieur) reste en glose ou en prose. La critique du consentement formel ne devient un
*gate* que par sa face opposable.

## 3. Ce qu'il faut préserver si l'on re-centre sur le salariat

Je concède le re-centrage : faire du **salariat de marché** la face observable principale
du co-gate « travail » est plus fidèle à Polanyi (travail = 3ᵉ marchandise fictive =
salaire) et plus net que « subordination », notion plus floue. Mais pas au prix d'un blanc
laissé sur l'hétéronomie sans salaire. Trois options, par ordre de préférence :

- **(A) Garde-fou résiduel — préféré.** Renommer le co-gate `non_salariat` (ou « travail
  décommodifié »), MAIS conserver un **second proxy unidirectionnel** : *une hiérarchie de
  commandement constatée et non réversible vaut « non »* (ferme le sommet) ; son absence
  reste `inconnu` (neutre), jamais déduite de la forme. Exactement la mécanique déjà
  acquise (périmètre §34, proxy unidirectionnel). On garde donc DEUX faces observables
  pour un même co-gate : marchandisation (salaire) ET hétéronomie irréversible
  (commandement constaté). Le second ne se déclenche que sur du dur — gourou documenté,
  statuts sans droit de sortie.

- **(B) Glose, à défaut.** Si l'on veut un co-gate mono-critère (salariat seul), alors
  l'hétéronomie sans salaire descend en glose (b) : elle pèse sur l'Indice (axe 3, le
  pouvoir / gouvernance) sans gater. Acceptable mais plus faible — un lieu fusionnel sans
  salarié pourrait toucher le sommet.

- **(C) Limite assumée, au minimum.** Si même la glose saute, il faut au moins **l'écrire
  dans §11 (ce que le modèle ne mesure pas)** : « le co-gate travail ne capte que la
  marchandisation ; l'hétéronomie non marchande — gourou, corvée, travail fantôme genré —
  est hors champ du gate, signalée en prose. » Une limite nommée vaut mieux qu'un angle
  mort tu.

Mon seuil de concession : **B est mon plancher**. Tomber à C seul (limite tue dans la
prose) me paraît une perte sèche pour un projet qui valorise au sommet la *communauté de
partage intégral* — le type exact où le risque de gourou est maximal.

## 4. Éléments constitutifs apportés

**Liste des cas-limites (décommodifiés mais non libres) :**
1. Leader charismatique / dérive sectaire — hiérarchie de fait, 0 salarié.
2. Corvée / bénévolat obligatoire sous peine d'exclusion.
3. Division genrée du travail domestique non rémunéré (travail fantôme).
4. Stagiaire / apprenti perpétuel — dépendance hors salariat formel.

**Formulation du garde-fou minimal (option A) :**
> Co-gate `travail_decommodifie`, deux faces observables, proxy unidirectionnel :
> (i) un **salariat de marché constaté** vaut « non » ;
> (ii) une **hiérarchie de commandement constatée et irréversible** (absence de droit
> de sortie opposable, captation des moyens de subsistance) vaut « non ».
> Toute absence reste `inconnu` (neutre), jamais déduite de la forme. Le for intérieur
> (consentement « réel ») reste hors gate — glose ou prose.

**Test d'observabilité du second proxy** (pour la voix méthodologue) : la « hiérarchie
irréversible » se constate-t-elle sur sources publiques (statuts, presse sur dérive
sectaire, signalement MIVILUDES) ? Si non documentable, elle reste `inconnu` — donc neutre,
jamais fabriquée.

## 5. Accord et désaccord prévus avec la voix Décommodification

**Accord.** Nous convergerons sur le re-centrage polanyien : le salariat de marché est la
face observable juste du co-gate travail, et « subordination » seul était trop large /
flou. Nous partagerons aussi le refus du test psychologique inobservable.

**Désaccord.** La voix Décommodification voudra probablement un co-gate **mono-critère
propre** (salariat seul) — élégant, fidèle à Polanyi, sans résidu illichien. Je résisterai :
le don/troc de Mauss (qu'elle invoque) peut *lui-même hiérarchiser* — le cadre le dit déjà
(§4.5, « un don peut obliger et hiérarchiser »). Donc la décommodification ne garantit pas
l'autonomie ; elle peut même la masquer. Mon garde-fou (A ou au pire B) est la trace de ce
désaccord : un co-gate à deux faces, pas une face. Le point de friction net : *« non-salariat »
suffit-il, ou faut-il un second proxy pour l'hétéronomie non marchande ?* — c'est là que
l'arbitrage de cycle 2 devra trancher.
