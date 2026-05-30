# Cycle 2 — Le directeur éditorial (réactions croisées)

*Voix : @lumen — garant de pertinence, chasseur de redites. Ma règle d'or :
dire une fois à l'endroit canonique, nommer et renvoyer ailleurs. Cycle 2 :
je lis les cinq autres voix contre la mienne, je consolide là où l'on
converge, et je red-teame au moins une coupe qui, sous couvert de simplifier,
supprimerait une **occurrence utile** plutôt qu'une **redite nuisible**.*

---

## 1. Convergences à exploiter — la coupe nette et son foyer canonique

Trois cibles reviennent dans plusieurs voix avec la même mécanique. Pour
chacune je tranche : quelle est la coupe, et où vit désormais l'idée.

**C1 — L'aside « Trois lectures, distinctes à dessein » sur chaque fiche.**
Quatre voix la visent : primo (coupe n°1, gain 15-20 s/fiche), architecte
(zone 3, « replier et déduppliquer »), diffuseur (coupe n°3, « la prise
arrive avant la mise en garde »), et moi (coupe n°1, R2+R8+R9 condensés). La
convergence est totale et ce n'est pas un hasard : c'est le **plus gros gain
global du site** parce qu'il se multiplie par 45+ fiches. **Coupe nette :**
supprimer l'aside ré-explicatif ; le remplacer par **une ligne + lien**
(« Verdict, Indice et palier ne disent pas la même chose → Méthode »).
**Foyer canonique :** la distinction vit en entier sur `methode.html#verdict`
+ `#indice`. Nuance d'arbitrage entre nous : le primo et le diffuseur veulent
*repousser/replier* (garder un `<details>` sur la fiche), l'architecte veut
*couper* (renvoi seul). Je tranche avec l'architecte : un `<details>` qui
duplique le canon est un tiroir de redite — autant le lien. Mais (voir §2) la
`chaine-note` n'est PAS dans ce lot.

**C2 — Le triptyque usus/fructus/abusus exposé en triple.** Gardien (négociable
n°1, « *un* exposé canonique, *un* renvoi ») et moi (R1). Convergence parfaite,
y compris sur le foyer : **les Régimes** (`regimes.html#triptyque`), sa maison
naturelle avec les pôles. **Coupe nette :** supprimer la version longue de
`methode.html#triptyque` et l'entrée longue concurrente du glossaire ; Méthode
garde 2 lignes + ancre. Le pédagogue ajoute une nuance qui n'est PAS une redite
mais une traduction : tuer le mot-chapeau « triptyque » → « les trois pouvoirs
du propriétaire », en gardant les trois latins glosés dessous. Les deux gestes
sont compatibles : je coupe les doublons, lui traduit l'étiquette. À séquencer :
d'abord ma déduplication (choisir le foyer), puis sa traduction sur le foyer
retenu — sinon on traduit deux fois.

**C3 — Le pied de page « non un label » répété sur 9 pages.** Architecte (implicite
dans « redondances inter-pages »), moi (R3, coupe n°3), diffuseur (coupe n°1
côté hero), contre le gardien (Piège 5). C'est ma convergence la plus délicate
— elle bascule directement dans le red-team du §2, donc je la traite là. **Coupe
proposée par défaut :** ramener le footer à une demi-ligne d'identité + liens ;
la doctrine vit dans `methode.html#verdict`. **Mais** le gardien oppose un
veto partiel que je juge fondé. Suite en §2.

---

## 2. Là où je conteste / arbitre — red-team d'une coupe (obligatoire)

**La coupe que je red-teame : « supprimer la phrase ‘non un label' du pied de
page des 9 surfaces » (ma R3, reprise par le diffuseur).**

C'est *ma propre* coupe que je durcis contre moi-même, car le gardien (Piège 5)
a raison sur un point que mon inventaire de cycle 1 a sous-estimé. Voici la
distinction que ma règle d'or commande et que j'avais appliquée trop vite.

Une fiche de lieu **s'ouvre seule** — partagée par lien, indexée par un moteur,
screenshotée. Dans ce cas de figure (qui est le mode d'entrée *dominant* pour
le diffuseur lui-même !), le lecteur n'a **pas** la page Méthode en contexte et
**ne peut pas cliquer dans le passé** : la fiche est tout ce qu'il voit. La
ligne de footer « évaluation au regard d'un cadre contestable, non un label »
est alors le **seul** énoncé du statut épistémique présent sous les yeux. La
supprimer ferait ressembler une fiche-tableau chiffrée à une **certification** —
exactement le « faux ami » que le projet dénonce.

Verdict d'arbitrage : **ce n'est pas une redite nuisible, c'est une occurrence
utile.** Mon test pratique de cycle 1 le dit lui-même : *« Le lecteur de cette
page-ci en a-t-il besoin maintenant, sans pouvoir cliquer ? »* → ici, **oui**.
Donc : garder, mais **en une phrase**, pas en paragraphe doctrinal.

**Ce qui distingue redite et occurrence utile, ici précisément :**
- Le *paragraphe* doctrinal complet « non un label » répété **mot pour mot** sur
  des pages-cadre qui ont déjà la Méthode à un clic (classement, comparer,
  méthode elle-même, glossaire) = **redite nuisible** → couper et lier.
- La *demi-ligne* de statut épistémique en **pied de fiche** (surface qui circule
  isolée) = **occurrence utile** → garder, calibrée court.

La frontière n'est donc pas « le footer » comme zone, mais « la fiche est-elle
auto-portante quand on l'ouvre seule ». Le gardien voit l'invariant doctrinal ;
moi je vois la condition de lecture. Nous tombons d'accord sur le geste — alléger
sans supprimer — par deux chemins. Ma R3 de cycle 1 disait « le footer peut garder
une demi-ligne » : je m'aligne et je le **promeus en consigne ferme** plutôt qu'en
concession en passant. (Note CLAUDE.md L9 : une fiche ouverte seule perd même son
CSS — raison de plus pour qu'elle ne perde pas en plus son seul garde-fou de statut.)

**Second red-team, plus bref — contre le diffuseur (sa coupe n°4, le
`callout-warn` du classement).** Le diffuseur veut le remplacer par un simple
filtre « Lieux ». Le gardien (Piège 2) et moi-même (R6) y voyons un risque : ce
callout est, sur la page qui invite *le plus* à lire en palmarès, le seul rappel
que lieux/porteurs/usufruitiers ne sont pas strictement comparables. Sur
`classement.html` ce **n'est pas** une redite — c'est l'occurrence canonique. La
redite, c'est sa *copie* sur `comparer.html`. Donc : garder le callout entier sur
le Classement (occurrence utile), réduire Comparer à une ligne + lien (redite
nuisible). Le diffuseur a raison de vouloir un Top 10 lisible ; il a tort de
vouloir supprimer l'avertissement plutôt que de le déplacer hors du chemin du
screenshot. On peut faire les deux : filtre « Lieux » par défaut **et** callout
conservé replié/sous le tableau.

---

## 3. Articulation avec l'architecte — « source unique + renvoi » vs ma règle d'or

Ce sont **deux outils complémentaires, pas le même**, et le préciser évite un
recouvrement coûteux.

- **Ma règle d'or porte sur les *idées*** (foyers rédactionnels) : chaque idée du
  noyau doctrinal a **un seul endroit où elle est *rédigée en entier*** (Méthode,
  Régimes, Glossaire, page-mère des Revues). Ailleurs : on *nomme* le terme et on
  *lie*. C'est une discipline de **contenu**.
- **La règle de l'architecte porte sur les *zones d'affichage*** : combien de blocs
  de premier niveau, quelle profondeur, fusionner les zones quasi-jumelles
  (pentagone + 5 barres, badge + échelle + ghost en un « objet-verdict »). C'est
  une discipline de **layout**.

Le partage net : **l'architecte décide *où ça s'affiche et à quelle profondeur* ;
moi je décide *où c'est rédigé une fois pour toutes*.** Les deux se rejoignent sur
l'aside « Trois lectures » (C1) parce que là, supprimer le bloc d'affichage (lui)
**et** déplacer l'idée à son foyer (moi) sont le même geste vu des deux côtés. Mais
ils divergent sur deux cas qu'il faut séparer pour ne pas se piétiner :

1. **L'objet-verdict composite** (sa fusion badge+chiffre+palier en une ligne) est
   une décision de *layout pur* : il ne change **rien** au nombre d'idées ni à
   leur foyer. Je n'ai pas voix au chapitre — je note seulement que cette fusion
   visuelle **rend mon aside inutile**, comme il l'écrit. Bonne synergie.
2. **Les 5 barres chiffrées** : l'architecte les *replie* (le chiffre exact reste,
   en profondeur 2). Ma règle d'or **ne s'applique pas** — ce ne sont pas une redite
   d'idée, c'est la *même donnée* en deux représentations (forme + chiffre). Pour
   moi le chiffre n'est pas du gras doctrinal : c'est de la donnée propre au lieu.
   Je laisse l'architecte trancher le repli ; je ne réclame pas de coupe ici.

Règle de coexistence : **on ne traite pas une question de layout comme une redite,
ni une redite comme un problème de layout.** Replier un doublon visuel (5 barres)
n'efface pas une idée ; supprimer un aside ré-explicatif efface une redite mais ne
règle aucune profondeur. Quand les deux coïncident (C1), tant mieux — c'est le
geste à plus haut rendement.

---

## 4. Ce que je n'avais pas vu

**a) Le « bug Pommiers » du diffuseur EST une redite mal synchronisée — et c'est
le cas d'école de ma règle d'or.** Le diffuseur le présente comme une *contradiction*
(article : verdict « marchand », Indice « 56 », palier « libération engagée » ;
fiche live : « hybride », « 65 », « Montage solide »). Vu de ma fonction, c'est la
**même donnée écrite à deux endroits qui ont divergé dans le temps** : le verdict
et l'Indice de Pommiers ont été rédigés une fois dans l'article de revue, une fois
dans la fiche, et l'un des deux n'a pas suivi une révision (vraisemblablement la
refonte qui a fait passer le montage de marchand à hybride). C'est *exactement* le
dégât que ma règle d'or prévient : **une donnée a un seul foyer ; partout ailleurs
on la *réaffiche par renvoi*, jamais on ne la recopie.** Si l'article avait *cité*
le verdict de la fiche au lieu de le re-rédiger en dur, la divergence serait
impossible. Conséquence pratique que j'ajoute à mes coupes : **le verdict, l'Indice
et le palier d'un lieu ont pour foyer la fiche ; tout texte de revue qui les
mentionne doit les nommer en renvoyant, pas les figer en chiffres recopiés.** Le
diffuseur a raison que c'est un préalable bloquant — mais la *cause* relève de mon
champ (synchronisation des occurrences), pas seulement de la diffusion.

**b) Le glossaire qui se contredit lui-même (R8 : `g-agregation-non-compensatoire`
vs part de `g-indice-de-liberation`) et l'intégrité (R12) qui se répète *dans son
propre paragraphe*.** Le gardien et l'architecte tiennent la Méthode et le Glossaire
pour les *foyers canoniques*. Mais un foyer qui se répète **à l'intérieur de
lui-même** ne peut pas servir de référence stable : on ne peut pas « renvoyer vers
le canon » si le canon dit deux fois la même chose à deux endroits. Angle que je
n'avais pas assez souligné : **avant de renvoyer tout le site vers la Méthode et le
Glossaire, il faut nettoyer le canon lui-même** — sinon on industrialise une
référence boiteuse. C'est un *prérequis de séquencement* : nettoyer les foyers
(coupe n°9 de cycle 1) **avant** de couper les renvois (coupes n°1-8).

---

## 5. Tension structurante — « couper la redite avant le fond » suffit-il ?

Ma thèse de cycle 1 : la lourdeur de Communs est surtout de la
*re-contextualisation défensive*, pas un excès de fond. Je la maintiens **comme
gisement principal** — c'est là que sont les gains à risque nul, multipliés par
45 fiches et 9 footers. Mais je dois concéder, honnêtement, que **couper la redite
ne suffit pas** : le primo, le diffuseur et le pédagogue pointent deux choses que
ma règle d'or ne traite pas.

1. **Le fond *unique* mais mal placé** (primo, architecte). Sur une fiche, les 5
   barres + l'échelle de paliers + le ghost + la grille à 22 lignes dépliée ne sont
   **pas** des redites (sauf pentagone↔barres) : c'est de la donnée propre, juste
   posée trop tôt et trop ouverte. Ma règle d'or est muette ici. Il faut **repousser
   en profondeur** (geste de l'architecte), pas couper. Frontière : *redite* = même
   idée à plusieurs endroits → ma juridiction (couper/lier) ; *profondeur* = donnée
   unique mal hiérarchisée → juridiction architecte (replier).

2. **Le fond *présent au mauvais moment*** (primo, diffuseur). Le membre
   « défendable et contestable, non une mesure neutre » dans le hero n'est pas une
   redite *du hero* (il n'y est dit qu'une fois) : c'est une *bonne idée à la
   mauvaise place*. La couper du hero pour la renvoyer en Méthode relève de mon
   « nommer et renvoyer » — mais le *motif* n'est pas « c'est répété », c'est « ça
   refroidit la prise avant qu'elle ait porté » (diffuseur) et « ça demande au primo
   d'apprendre la controverse avant le sujet » (primo). Donc : ma technique (déplacer
   vers le foyer) sert un objectif qui n'est pas le mien (séquence de lecture). Je
   l'accepte : le geste est le même, la justification se cumule.

**Où est la frontière, dite proprement :**

| Symptôme | Cause | Juridiction | Geste |
|---|---|---|---|
| Même idée rédigée à 2+ endroits | redite nuisible | @lumen (moi) | couper + lier vers le foyer |
| Donnée unique recopiée et désynchronisée (Pommiers) | redite mal synchronisée | @lumen (moi) | un seul foyer, renvoi ailleurs |
| Donnée propre posée trop tôt / trop ouverte | profondeur | architecte | replier (`<details>`) |
| Bonne idée à la mauvaise place dans la séquence | ordonnancement | primo / diffuseur | déplacer (souvent via mon renvoi) |
| Terme juste mais opaque | langue | pédagogue | gloser / traduire |
| Concept doctrinal nécessaire pris pour du gras | substance | gardien (veto) | **ne pas toucher** |

Ma thèse reste le **plus gros levier** (colonne 1-2), mais elle est une *condition
nécessaire et non suffisante*. Le site sera fluide quand on aura, dans l'ordre :
(1) nettoyé les foyers, (2) coupé les redites vers eux, (3) replié le fond unique
trop exposé, (4) réordonné les bonnes idées mal placées, (5) traduit la langue —
le tout sous le **veto doctrinal** du gardien sur les cinq invariants.

---

### Retour (4 lignes)

1. **Coupe red-teamée comme occurrence utile, pas redite :** la phrase « non un
   label » en **pied de fiche** — à garder (en une demi-ligne), car une fiche
   ouverte seule par partage est le seul endroit où le lecteur voit le statut
   épistémique et ne peut pas cliquer vers la Méthode. La *redite* à couper, c'est
   sa copie longue sur les pages-cadre qui ont la Méthode à un clic.
2. **« Couper la redite suffit-il ? »** Non — c'est le plus gros levier (risque
   nul, ×45 fiches) mais **nécessaire et non suffisant** : il faut AUSSI replier
   du fond unique mal placé (5 barres, grille) et réordonner des idées justes mais
   prématurées (disclaimer du hero).
3. **Séquence impérative :** nettoyer les foyers (canon qui se répète, R8/R12)
   AVANT d'y renvoyer le reste — on ne renvoie pas vers une référence boiteuse.
4. **Apport propre :** le « bug Pommiers » est une redite mal synchronisée
   (donnée recopiée puis divergée), pas une simple contradiction de diffusion —
   donc relève de ma règle d'or : un seul foyer (la fiche), renvoi ailleurs.
