# Cycle 1 — round 2 — voix juriste-économiste des structures agricoles et de l'ESS

*Divergence isolée. Je n'ai lu que la synthèse du round 1 (`03-synthese.md`),
`config/grilles.yml` et `lieux/ferme-de-pommiers.yml`. Mon rôle ici est le
reality check : la finalité « non-lucratif d'intérêt général » est-elle
**observable** sur sources publiques, et n'est-elle pas une catégorie quasi
vide ?*

---

## 0. Ce que le round 1 a tranché, et ce qui rouvre

Le round 1 a déplacé l'objet mesuré sur l'axe `nature_interet` : on ne gradue
plus la lucrativité, on gradue **la captation de la rente foncière** (l'abusus
du fonds), lue relationnellement sur la chaîne (nature du maillon × titre de
l'articulation). C'est juste, et je m'y rallie sans réserve : ce que cet axe
capture, c'est le rapport au **stock** (le sol et sa plus-value).

Le round 2 pose une question d'une autre nature : la finalité du **flux** —
ce que l'activité du lieu *produit et pour qui*. Don/troc/gratuité/soin du
vivant sans profit individuel (non-lucratif d'intérêt général) versus vente,
bénéfice réparti aux associé·es, patrimoine (lucratif d'intérêt individuel).
Ce sont bien deux choses distinctes : un GAEC bio sur bail Terre de Liens
**ne capte pas la rente** (round 1 le classe `hybride`, justement) mais
**vend au marché** (flux lucratif d'intérêt individuel des associé·es). Le
round 1 a raison de ne pas le punir sur le stock ; le round 2 demande si le
flux mérite un second marqueur.

Ma thèse en une ligne : **oui c'est conceptuellement distinct, mais la
distinction « non-lucratif d'intérêt général » au sens strict désigne une
catégorie quasi vide dans ce corpus, et tout marqueur binaire produirait du
faux.**

---

## 1. La lucrativité de l'ACTIVITÉ — définition juridique/économique

Il faut séparer trois notions que le langage courant amalgame, et que le
round 1 a déjà partiellement démêlées.

**(a) Lucrativité de la STRUCTURE (round 1, axe 2 `structure`).** Le capital
est-il rémunéré, les parts captent-elles la plus-value ? C'est de l'abusus
sociétaire — déjà couvert.

**(b) Lucrativité de l'ACTIVITÉ au sens FISCAL (CGI).** C'est la question
réelle du round 2. En droit fiscal français, une activité est *non lucrative*
(donc hors impôts commerciaux) si elle satisfait au faisceau de la doctrine
administrative — couramment résumé par la **gestion désintéressée** + la règle
dite des **« 4 P »** (Produit, Public, Prix, Publicité) appréciant si l'organisme
concurrence le secteur commercial dans des conditions analogues. *Référence
doctrinale précise et seuils — à vérifier (BOFiP, franchise des activités
lucratives accessoires) : je ne cite aucun chiffre de mémoire.* Le point dur :
la non-lucrativité fiscale exige une **gestion désintéressée** (pas de partage
de bénéfice, pas de rémunération des dirigeants au-delà d'un plafond) ET une
**non-concurrence** avec le marché (ou concurrence dans des conditions
différentes : public exclu du marché, prix modulés, absence de publicité
commerciale). Un GAEC qui vend ses fromages en Biocoop **échoue aux deux** :
il partage le bénéfice d'exploitation entre associé·es (c'est sa raison
d'être : revenu paysan) et il vend au prix du marché à un public solvable.

**(c) Caractère marchand de l'ÉCHANGE.** Y a-t-il prix contre bien/service ?
C'est le plus large. Vente directe, AMAP, marché de producteur·rices,
magasin de producteur·rices, Biocoop : **tout cela est marchand**, même quand
c'est court, local, éthique et à marge faible. L'AMAP est un contrat
d'engagement, pas une gratuité : le·la consommateur·rice **paie** un panier.
Le « prix libre » est marchand aussi (l'acheteur fixe le montant, mais il
paie). Seuls relèvent du **non-marchand pur** : l'autoconsommation, le don
sans contrepartie, le troc sans monétisation, le glanage, la mise à
disposition gratuite.

La distinction du round 2 demande de trancher entre (b) et (c). Et c'est là
que le piège se referme.

---

## 2. Marqueurs observables sur sources publiques

Ce que je peux **observer** dans les fiches et les sources Terre de Liens /
presse / sites :

| Marqueur observable | Ce qu'il établit | Disponibilité réelle |
|---|---|---|
| Forme juridique (GAEC, EARL, asso 1901, SCIC, fondation) | Présomption de finalité du flux | **Haute** (déjà saisi) |
| Mention « vente directe / marché / AMAP / Biocoop / magasin » | Activité **marchande** avérée | **Haute** (souvent dans le résumé) |
| Agrément fiscal d'intérêt général / RUP / mécénat | Non-lucrativité fiscale **présumée** côté porteur | Moyenne |
| Statut ESUS / agrément ESS | Lucrativité **encadrée** (déjà round 1, `commerciale_encadree`) | Moyenne |
| Régime fiscal de l'exploitation (IR/IS, assujettissement TVA, gestion désintéressée) | Lucrativité fiscale de l'**activité** | **Basse à nulle** — quasi jamais public pour une ferme |
| Affectation des excédents (réinvestis vs distribués) | Lucrativité effective du flux | **Basse** — pas dans les sources grand public |
| Gratuité / don / troc documentés | Non-marchand pur | **Basse** et rare |

Le constat dur : les marqueurs **fiables et publics** distinguent surtout
*marchand / non-marchand* (c) et la *forme* (présomption), pas la
*non-lucrativité fiscale de l'activité* (b). Pour trancher (b) il faudrait
les statuts et la liasse fiscale de l'exploitant — introuvables pour une ferme
ordinaire. Or `ferme-de-pommiers.yml` le montre noir sur blanc : même le
**fermage** versé à la Fondation est `inconnu` (« non documenté par les
sources »). Si on ne sait pas le loyer, on ne saura jamais l'affectation des
excédents du GAEC.

**Donc** : un axe « finalité d'usage » saisi exigerait des données absentes →
explosion des `inconnu` → corpus non-jugeable. C'est exactement la ligne rouge
L11 / point 5 de la synthèse round 1 (« `inconnu` reste sacré », classement
piloté par la forme). On retomberait dans le travers qu'on vient d'éliminer.

---

## 3. Le risque de catégorie vide — combien de lieux « non-lucratif d'IG pur » ?

C'est le cœur de mon reality check. Au sens **strict** (gestion désintéressée
+ non-concurrence fiscale, OU flux réellement non-marchand : gratuité/don/troc),
combien de lieux du corpus tomberaient dans « non-lucratif d'intérêt général » ?

Je n'ai lu qu'une fiche, mais elle est **le cas fondateur** et elle est
édifiante. La Ferme de Pommiers :
- foncier non lucratif (Fondation RUP) → **côté stock, exemplaire** ;
- activité : élevage ovin laitier bio, transformation fromagère, **vente
  directe** (marché, magasins de producteur·rices, Biocoop) → **flux
  marchand, lucratif d'intérêt individuel** des éleveur·ses (c'est leur
  revenu) ;
- `usage_non_marchand` déjà coché **partiel** dans la fiche, justement parce
  que « la production fromagère est vendue en circuit court ».

Ce lieu — qui est l'archétype du « bon » montage Terre de Liens — **ne serait
PAS** « non-lucratif d'intérêt général » au sens strict du flux. Il est
d'intérêt général par sa **finalité large** (nourrir, agriculture paysanne,
accueil) — ce que la grille capte déjà via `usage_interet_general` (axe 4) —
mais il est **lucratif au sens fiscal** et **marchand**.

Extrapolation prudente (à confirmer sur le corpus complet, je ne l'ai pas lu) :
la **quasi-totalité** des fermes Terre de Liens, AMAP, fermes en vente directe
seraient marchandes/lucratives-individuelles. La catégorie « non-lucratif d'IG
pur » serait peuplée seulement par : structures en **gestion désintéressée
documentée** (associations d'éducation à l'environnement, tiers-lieux
gratuits, jardins partagés sans vente, conservatoires, fermes pédagogiques
associatives), **autoconsommation/gratuité**, et rares **SCIC à finalité
clairement non distributive**. Soit, à vue de nez, **une minorité** — peut-être
10-20 % du corpus, *chiffre à vérifier impérativement par comptage réel*.

Conclusion du reality check : **la catégorie n'est pas vide, mais elle est
minoritaire, et son contour strict exclut précisément ce que le site veut
valoriser** (le paysan qui vend pour vivre sur terre libérée). Si on en fait
un axe binaire orthogonal, le résultat mécanique sera : « presque tout le
corpus = lucratif d'intérêt individuel ». C'est désastreux éditorialement et
**faux** au regard de la finalité réelle de ces lieux, qui *sont* d'intérêt
général par leur fonction nourricière et leur ancrage, sans être non-lucratifs
au sens fiscal.

---

## 4. Axe binaire, gradué, ou simple descripteur ?

Mon verdict de juriste-économiste, en raisonnant sur l'observabilité :

**Pas d'axe binaire.** Un binaire non-lucratif/lucratif écraserait sur le
même plateau « lucratif » le GAEC paysan bio et la SAS agro-industrielle. Le
round 1 a justement tué ce genre d'amalgame. Un binaire reproduirait le bug.

**Pas un cinquième axe saisi.** Les données pour trancher (b) sont absentes
des sources → `inconnu` massif → corpus non-jugeable. Interdit par L11.

**La grille a DÉJÀ ce qu'il faut, et c'est gradué.** C'est mon point central :
deux critères couvrent les deux moitiés de la « finalité d'usage » que le
round 2 veut isoler, et **ils sont déjà gradués (oui/partiel/non), déjà
dérivables de sources publiques, déjà testés sur Pommiers** :
- `usage_interet_general` (grille lieu, **axe 4**, poids 3) capte le versant
  « intérêt général » : l'activité dépasse-t-elle ses occupants (nourrir,
  écologie, pédagogie) ? Pommiers = oui.
- `usage_non_marchand` (grille lieu, **axe 5**, poids 3) capte le versant
  « non-lucratif/non-marchand » du flux : gratuité/don/troc/contribution
  modique vs prix de marché. Pommiers = partiel (vente circuit court).

Autrement dit, **la distinction du round 2 n'est pas un trou de la grille :
elle y est déjà, éclatée sur deux axes existants, et graduée**. Ce que le
round 2 prend pour un « amalgame du cran » est en réalité une distinction
*déjà portée ailleurs dans le modèle* — sur les axes finalité (4) et usage (5),
pas sur l'axe structure/nature (2). C'est cohérent : la finalité du flux n'est
pas la nature de la structure.

**Donc ma recommandation : ni nouvel axe, ni re-division du cran. Au plus,
un DESCRIPTEUR dérivé** (non noté, ou faiblement), calculé par le générateur à
partir de marqueurs déjà présents (forme + mentions « vente directe / AMAP /
gratuit / gestion désintéressée »), du type `finalite_flux ∈ {non_marchand,
marchand_circuit_court, marchand_marche, inconnu}`. Descriptif, pas
sanctionnant. Il enrichirait la **prose d'explication du lieu** (cohérent avec
D1 du round 1 : « économie paysanne » vit dans la phrase, pas dans l'étiquette
absolue) sans toucher au calcul du verdict. Si l'on veut absolument un effet
sur l'indice, le faire passer par un **ajustement des poids** de
`usage_non_marchand` / `usage_interet_general` déjà existants — pas par un
axe neuf.

**Verdict 2D ?** Non, pas un verdict à deux dimensions affiché. Un verdict
public à 3 niveaux (round 1) + un descripteur de finalité d'usage en sous-titre.
Un 2D nominal rouvrirait le couplage palier×verdict que le round 1 a
explicitement écarté (point 3.2), pour un gain de lisibilité douteux : « commun
hybride à flux marchand de circuit court » est illisible.

---

## 5. Désaccords prévisibles

- **Voix économie-solidaire / communs** : idéalisera la catégorie non-lucrative,
  voudra un axe plein pour valoriser le don/troc/gratuité et « ne pas dissoudre
  le hors-marché dans le marchand ». Mon objection : l'intention est juste, mais
  l'axe plein punira mécaniquement 80 % du corpus comme « lucratif individuel »,
  y compris les lieux qu'on aime. On valoriserait une pureté que presque aucun
  lieu n'atteint — c'est militer contre son propre corpus.

- **Voix communs (Ostrom)** : pourra dire que le marché n'est pas l'ennemi du
  commun (un commun peut vendre son surplus), et que ce qui compte est la
  *gouvernance de la ressource*, pas la finalité du flux. Je suis assez
  d'accord — ce qui affaiblit encore l'idée d'un axe finalité séparé.

- **Méthodologue (parcimonie / L11)** : sera mon allié objectif. Refusera tout
  champ saisi exigeant des données absentes, rappellera `inconnu` sacré et la
  source unique de vérité. Notre seul écart possible : il pourrait vouloir
  *zéro* descripteur (parcimonie totale) là où je tolère un descripteur dérivé
  non noté. Friction mineure.

- **Voix éditoriale-réception** : voudra que la non-lucrativité d'IG soit
  *visible* (c'est la posture du site). Je réponds : visible en **prose**
  (« ferme paysanne nourricière, vente directe en circuit court »), pas en
  **étiquette de classement**. Le site soutient une contre-culture sans
  criminaliser le paysan qui vend — un axe lucratif/non-lucratif binaire
  ferait exactement l'inverse de cette posture : il tamponnerait « lucratif »
  sur le front du berger de Pommiers.

---

## 6. Lignes rouges

1. **Ne jamais classer « lucratif d'intérêt individuel » un lieu nourricier en
   vente directe sur foncier libéré.** Ce serait criminaliser le paysan qui
   vend pour vivre — l'exact contraire de la posture du site. Vente directe ≠
   captation, ≠ accaparement, ≠ intérêt individuel au sens péjoratif. C'est
   un revenu de travail, pas une rente.

2. **Aucun champ saisi exigeant la liasse fiscale ou les statuts financiers de
   l'exploitant.** Données introuvables → `inconnu` massif → corpus
   non-jugeable. Si on ne sait pas le fermage de Pommiers, on ne saura pas
   l'affectation de ses excédents. `inconnu` reste sacré (round 1, point 5).

3. **Ne pas inventer de seuil ni de statut fiscal.** Les « 4 P », la gestion
   désintéressée, la franchise des activités accessoires : je les nomme comme
   cadre, mais **tout seuil chiffré est à vérifier au BOFiP** avant toute
   inscription dans le modèle. Je n'en pose aucun.

4. **Ne pas fabriquer une catégorie non-lucrative introuvable.** Si le comptage
   réel montre < 15 % du corpus en non-lucratif d'IG strict, un axe binaire
   n'a pas de sens statistique : il sépare une poignée d'exceptions du gros du
   corpus, et fait croire à une finalité lucrative générale qui est un artefact
   de définition, pas une réalité des lieux.

5. **Ne pas confondre intérêt général (finalité) et non-lucrativité (régime
   économique).** Un GAEC bio EST d'intérêt général (il nourrit, il entretient
   le paysage) ET lucratif au sens fiscal. Les deux ne s'excluent pas. Tout
   modèle qui les colle commet une faute de droit de l'ESS.

---

## 7. Recommandation de synthèse (pour mémoire au cycle 2)

La distinction du round 2 est réelle conceptuellement mais **déjà portée par
la grille** (axes 4 `usage_interet_general` et 5 `usage_non_marchand`,
gradués). Le « cran exploitation agricole » du round 1 n'amalgame pas vraiment
les deux finalités : il porte le **stock** (rapport à la rente), pas le
**flux** (finalité de l'activité), lequel vit déjà ailleurs. Donc : **ni
second axe orthogonal, ni re-division du cran, ni verdict 2D.** Au plus un
**descripteur de finalité d'usage dérivé** (non sanctionnant, alimentant la
prose), ou un simple réglage des poids des deux critères existants. La
catégorie « non-lucratif d'IG pur » est minoritaire (chiffre à confirmer par
comptage) et son contour strict exclut le cœur de cible éditorial — la
transformer en axe punirait le corpus qu'on défend.
