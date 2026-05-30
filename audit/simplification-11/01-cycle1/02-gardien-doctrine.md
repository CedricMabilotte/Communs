# Cycle 1 — Le gardien de la doctrine

*MARS-strat, session #11 — chantier de simplification du contenu public. Voix
isolée : l'universitaire / le juriste des communs (Eozen). Critère de jugement :
une simplification est légitime tant qu'elle n'érige pas une convention
argumentée en slogan, et ne fait pas disparaître la nuance qui distingue Communs
d'un palmarès militant. Surfaces auditées : `index`, `methode`, `glossaire`,
`regimes`, `grilles`, `classement`, `themes`, `comparer`, fiches `ferme-de-pommiers`,
`domaine-du-rayol`, `conservatoire-littoral`, `association-ancrage`, et les
revues ; cadre de référence : `brief-cadre-conceptuel-communs.md` et
`audit/refonte-theorique-9/04-cadre-theorique-complet.md`.*

---

Je commence par concéder, parce qu'un gardien qui sanctuarise tout ne garde
rien. Le site, dans son état actuel, **dit trois fois** une bonne part de sa
doctrine — sur la méthode, dans le glossaire, dans les régimes, puis encore
sur chaque fiche. Cette redondance n'est pas de la rigueur ; c'est de la peur.
Le projet a tellement craint d'être mal lu qu'il a paraphrasé chaque concept
sous deux ou trois angles, et le lecteur exigeant que je suis se lasse avant
d'atteindre ce qui compte vraiment. On peut couper largement sans toucher au
cœur. La difficulté — tout l'objet de cette note — est que le cœur et le
verbiage emploient parfois les mêmes mots, et qu'une coupe maladroite emporte
l'un en croyant ne tailler que l'autre.

## 1. Ce qui est négociable

**Le triptyque usus / fructus / abusus est exposé trois fois en intégralité** :
section dédiée de `methode.html`, section dédiée de `regimes.html`, et entrée
longue du glossaire — chacune avec sa version « en clair » et sa version « au
sens du droit ». C'est une redite franche. Le triptyque mérite *un* exposé
canonique (je le placerais sur `regimes.html`, qui est sa maison naturelle) et
*un renvoi* depuis les autres pages. On économise plusieurs centaines de mots
sans perdre un gramme de doctrine.

**Les doublons internes à `methode.html`.** La section « intégrité du montage »
dit deux fois, à quelques lignes d'écart, que l'indicateur « situe et ne classe
pas » et que « la protection du foncier est mesurée par l'axe 1, la nature par
l'axe 2 » (lignes 219-223). Pur copier-coller. À fusionner. De même, la
distinction verdict / Indice / palier est répétée presque mot pour mot entre
l'encart `verdict-cle` des fiches et la page méthode.

**Le verbiage rassurant.** Des formules comme « cinq axes indépendants les uns
des autres : un montage peut être haut sur l'un et bas sur un autre… aucun axe
ne se déduit d'un autre » occupent un paragraphe entier pour dire une évidence
de lecture de radar. Une phrase suffit. De même, les longues gloses « en clair »
de chaque axe sur la page méthode (« Une terre libérée est une terre qu'on ne
peut plus ni vendre, ni abîmer… ») doublent la voix exacte qui suit
immédiatement : sur une page *méthode*, destinée à qui veut comprendre le calcul,
la voix incarnée peut s'effacer ou se réduire à une ligne. Qu'elle domine le
*front* (l'accueil, les fiches) est juste ; qu'elle double tout l'appareil
méthodologique est du gras.

**Les tooltips géants.** L'attribut `title` du badge « hybride », répété sur
chaque carte et chaque fiche, contient une définition de 60 mots
(« La chaîne ne comporte aucun maillon marchand, mais au moins un maillon à
lucrativité encadrée… »). C'est illisible en infobulle et redondant avec le
glossaire. Un tooltip court (« foncier libéré, un maillon garde un intérêt privé
légitime ») + lien suffit.

**La page `themes.html`** redéploie en cartes les mêmes entités déjà présentes
dans l'annuaire, le classement et la carte — avec les mêmes profils SVG. Cinq
thèmes qui rebrassent le corpus. Si l'on cherche à montrer *moins
d'instruments*, c'est une surface entière candidate à la fusion avec l'annuaire
filtrable. Aucune doctrine n'y vit en propre.

Tout cela, je le coupe sans état d'âme. Maintenant, ce qui ne se touche pas.

## 2. Les invariants doctrinaux

### a) Le statut conventionnel du verdict (« comme l'IDH »)

**Quoi.** L'affirmation, présente sur `methode.html` (« Statut de l'évaluation »)
et dans l'entrée glossaire « verdict », que le verdict et l'Indice sont *un
indicateur composite conventionnel, une lecture argumentée, non une mesure
objective de la valeur d'un lieu*, à la manière de l'indice de développement
humain.

**Pourquoi c'est le projet.** C'est la phrase qui rend le site *citable*. Un
universitaire, un juriste, un journaliste peut s'appuyer sur Communs **parce
que** Communs déclare son statut épistémique. Retirée, la note de 65/100 de la
Ferme de Pommiers devient un fait prétendu objectif — et le site bascule du
référentiel argumenté au baromètre militant qui se prend pour un thermomètre.

**Ce qu'on perd.** Tout. Sans cette déclaration, la prise de position normative
revendiquée (« économie citoyenne, non lucrative ») n'est plus assumée comme
prise : elle se déguise en mesure. C'est précisément le reproche que le projet
adresse aux « faux amis » — habiller une posture en nature. Le couper, ce serait
faire au lecteur ce que le site dénonce. **Non négociable.** Au contraire, je le
durcirais : aujourd'hui il est en bas de page méthode et dans un encart de fiche ;
il devrait être lisible *sur l'accueil* (il y est, en une phrase : « C'est une
prise de position, défendable et contestable, non une mesure neutre » — à garder
absolument).

### b) La ligne observable-gaté / posture-glose

**Quoi.** Le principe que le sommet (verdict `sanctuaire`) n'est gaté que par du
**vérifiable et opposable** — foncier hors-marché, milieu protégé par dispositif
opposable, travail non marchandisé constaté — tandis que l'idéal décommodifié
(don/troc intégral, prise en charge collective des besoins) **éclaire le sommet
en prose sans le conditionner**. Présent sur `methode.html` (« Le sommet tient à
plusieurs conditions… ce qui ne l'est pas — l'idéal d'une économie pleinement
décommodifiée — éclaire le sommet sans en commander l'accès ») et incarné, ligne
à ligne, dans le critère « travail non marchandisé » des grilles.

**Pourquoi c'est le projet.** C'est la discipline qui empêche le site de
récompenser le *storytelling*. Le critère « proxy unidirectionnel » (un salariat
constaté vaut « non » ; l'absence reste « inconnu », jamais déduite) est ce qui
distingue un annuaire honnête d'un palmarès qui croit les communiqués sur parole.
C'est la signature méthodologique du projet — son extension propre la plus
défendable académiquement.

**Ce qu'on perd.** Si l'on fusionne « ce qui gate » et « ce qui est affirmé en
prose » pour « simplifier le sommet », on obtient soit un sommet inatteignable
(si l'idéal devient un seuil), soit un sommet bradé (si l'observable se dilue
dans l'intention). Les deux tuent le tri. La nuance gaté/glosé *peut* se dire
simplement — « on n'exige que ce qui se vérifie ; on nomme l'idéal sans
l'imposer » — mais elle ne peut pas **disparaître**.

### c) Le sommet rare, voire vide, assumé

**Quoi.** Le chiffre « 0 » sur l'accueil (« aucune libération pleinement
aboutie : le sommet reste un horizon »), le palier « Libération aboutie »
réservé au verdict sanctuaire, et la formule répétée « un horizon plus qu'une
case à remplir ».

**Pourquoi c'est le projet.** Un référentiel qui n'attribue jamais sa note
maximale, *et l'assume*, prouve qu'il ne se plie pas à la demande de bonnes
nouvelles. La rareté du sommet est la contre-preuve vivante que le verdict
n'est pas distribué pour plaire. C'est aussi ce qui protège les lieux « milieu »
de l'humiliation : si personne n'atteint le sommet, être hybride n'est pas un
échec.

**Ce qu'on perd.** La tentation de simplification ici est cosmétique et
mortelle (voir §3) : « adoucir » le 0, ou abaisser le seuil du sommet pour
« peupler » la catégorie. Le jour où le sommet se remplit pour rassurer, le
verdict ne vaut plus rien. **Le « 0 » de l'accueil est un actif, pas une gêne.**

### d) Le ré-encastrement polanyien (les trois marchandises fictives)

**Quoi.** La thèse que libérer une terre ne se réduit pas à la soustraire au
marché foncier, mais à ré-encastrer terre *et* travail *et* monnaie — les trois
marchandises fictives de Polanyi. C'est l'apport de la refonte #9 ; c'est ce qui
justifie que l'axe 2 (structure), le co-gate « travail non marchandisé » et la
prose sur le don existent.

**Pourquoi c'est le projet.** Sans Polanyi, le « travail non marchandisé »
devient un caprice anti-salarial inexplicable, et la sévérité envers les
coopératives qui salarient paraît arbitraire. La généalogie *fonde* la grille.
Un juriste des communs qui ne verrait pas pourquoi une SCOP n'est pas le sommet
refermerait le site. La réponse est polanyienne : la SCOP décommodifie le capital,
pas le travail.

**Ce qu'on perd.** On peut *alléger* l'exposé de Polanyi (le nom propre et
« 1944 » suffisent en façade, le développement va en page méthode ou cadre).
Mais effacer l'idée des trois marchandises, c'est rendre la moitié de la grille
inintelligible. La référence peut être discrète ; le concept doit rester
opérant.

### e) La chaîne comme seule source de vérité (faisceau de droits)

**Quoi.** Le principe que le verdict se *calcule* sur la place de chaque maillon
dans la chaîne, jamais sur la forme isolée d'une entité — « un GAEC preneur de
bail ≠ un GAEC propriétaire » (`methode.html`, et appliqué visiblement sur la
fiche Pommiers : structure plafonnée à 40 « quels que soient les critères
cochés »).

**Pourquoi c'est le projet.** C'est ce qui interdit l'amalgame paresseux
« société = mauvais, association = bon ». C'est rigoureux *et* juste, et c'est
ce qui rend les verdicts défendables un par un. La distinction intrinsèque /
effectif en découle.

**Ce qu'on perd.** Le mécanisme intrinsèque/effectif (médiane des lieux reliés,
minimum, etc.) **peut** être simplifié en façade : c'est un détail de calcul que
peu de lecteurs suivent. Mais le *principe* « on lit la place, pas la forme »
doit survivre, sinon les verdicts deviennent contestables au cas par cas et le
droit de réponse se transforme en champ de bataille.

## 3. Simplifications-pièges

Cinq coupes qui paraissent cosmétiques et qui, en réalité, font basculer le
projet vers le palmarès ou le slogan.

**Piège 1 — « Le verdict, c'est la note. »** *Coupe tentante :* fusionner
verdict, Indice et palier, qui « disent un peu la même chose » et encombrent
chaque fiche d'un encart à trois entrées. *Dégât caché :* ce sont trois objets
distincts à dessein. Le verdict est qualitatif et calculé sur la chaîne ;
l'Indice est quantitatif et non compensatoire ; le palier est une tranche
d'Indice *sous condition de verdict* (un Indice à 72 reste « solide » et pas
« abouti » sans verdict sanctuaire — c'est exactement le cas du Rayol). Les
fusionner produit un classement à une dimension : un palmarès. La distinction
est le rempart contre le palmarès. Elle peut être dite plus brièvement ; elle ne
peut pas être supprimée.

**Piège 2 — « Hybride = à mi-chemin, donc moins bien. »** *Coupe tentante :*
raccourcir la définition d'« hybride » à « entre marchand et sanctuaire », plus
digeste. *Dégât caché :* on perd le « **légitime, non condamné** » et la
mention que l'exploitation agricole preneuse de bail garde un bénéfice
légitimement approprié. Sans cette nuance, 36 lieux sur 45 (la quasi-totalité du
corpus) deviennent des demi-ratés. Le projet vise précisément à *ne pas*
mépriser le paysan qui vit de son travail. Couper, c'est transformer un annuaire
respectueux en mur de la honte.

**Piège 3 — « Adoucir le 0. »** *Coupe tentante :* remplacer « 0 libération
aboutie » par une formule positive, ou ne plus afficher le compteur du sommet
sur l'accueil. *Dégât caché :* le 0 *est* l'argument de crédibilité. Le masquer
suggère qu'on a quelque chose à cacher, ou pire, incite plus tard à abaisser le
seuil pour le remplir. La rareté assumée est la preuve d'incorruptibilité du
verdict.

**Piège 4 — « Le travail non marchandisé, c'est juste : pas de salaire. »**
*Coupe tentante :* réduire le co-gate à « travail bénévole / non salarié », en
supprimant le « proxy unidirectionnel » et la distinction marchandisation /
subordination. *Dégât caché :* on rouvre la confusion que la refonte #10 a
précisément fermée — entre *marchandiser* le travail (le tarifer) et le
*subordonner* (l'autorité). Sans le proxy unidirectionnel, l'absence
d'information devient un « non » : on punirait les lieux mal documentés, et on
fabriquerait du verdict sur du vide. C'est l'angle exact où le projet se
distingue d'un tract.

**Piège 5 — « Inutile de répéter ‘non un label'. »** *Coupe tentante :* le
pied de page de chaque surface porte « l'Indice de libération est une évaluation
au regard d'un cadre explicite et contestable, non un label ». Répétition →
candidate évidente à la coupe. *Dégât caché :* sur une fiche isolée (ouverte
seule depuis un partage, sans le contexte de la page méthode), cette ligne de
footer est *le seul* énoncé du statut épistémique visible. La supprimer du pied
de page laisserait une fiche-tableau nue ressembler à une certification. À garder
*au moins* en pied de fiche, quitte à l'alléger ailleurs.

## 4. Hermétique mais nécessaire vs hermétique et gratuit

**À garder, quitte à gloser une fois :**

- **« Marchandise fictive » / ré-encastrement** — charge conceptuelle
  irremplaçable (Polanyi). C'est le mot qui dit *pourquoi* terre, travail et
  monnaie sont traités ensemble. Aucun synonyme courant ne porte l'idée que
  ces trois choses ne sont pas *faites* pour être vendues. À garder, glosé une
  fois (« des choses que le marché traite en marchandises sans qu'elles en
  soient »).
- **« Sommet » / « étoile polaire »** — ce ne sont pas des ornements : ce sont
  les métaphores qui encodent la rareté assumée. « Étoile polaire » dit en deux
  mots « ça oriente sans qu'on l'atteigne » — exactement le statut de l'idéal
  décommodifié. La traduire en « objectif » ou « idéal » perdrait le
  *inatteignable-mais-orientant*. À garder.
- **« Faux ami » / « communs-washing »** — efficace, imagé, juste. À garder.
- **« Observable-gaté »** — le terme interne est jargonneux *en façade*, mais
  l'idée est vitale. Garder l'idée, traduire le mot : « on n'exige que ce qui se
  vérifie » au public ; « observable-gaté » reste pour la page méthode/cadre et
  l'audience experte.

**À traduire ou couper (jargon décoratif) :**

- **« Posture / nature »** comme couple technique (`regimes.html`) — l'idée
  (vérifier les intentions par les statuts) est bonne, le couple de mots est
  opaque. Dire « ce qu'on déclare vs ce que les statuts garantissent ».
- **« Domiciliage des axes »** — entrée de glossaire au nom administratif pour
  une idée simple (« chaque axe se lit là où il se joue »). Le mot peut
  disparaître, l'idée reste dans la phrase.
- **« Indice intrinsèque / effectif »** — distinction réelle, mais le vocabulaire
  et le calcul (médiane, minimum) sont sur-exposés en façade. À reléguer en
  méthode ; en fiche, une phrase (« sa note tient compte des lieux auxquels il
  est lié »).
- **« Agrégation non compensatoire »** — garder l'idée (« une force ne rachète
  pas une faiblesse », formule déjà présente et excellente), le terme savant peut
  rester au glossaire seulement.

Règle que j'en tire : on garde le vocable quand *aucune périphrase courte* ne
porte la même charge (marchandise fictive, étoile polaire) ; on traduit quand la
périphrase existe et fait aussi bien (domiciliage, posture/nature). Le test n'est
pas « est-ce difficile ? » mais « la version simple dit-elle vraiment la même
chose ? ».

## 5. Ma ligne rouge

S'il ne devait rester qu'une chose : **la déclaration que le verdict et l'Indice
sont une convention argumentée et contestable, non une mesure objective — et son
corollaire visible, le sommet rare assumé (le « 0 »).** Si la simplification
efface ce statut épistémique pour gagner en punch, le site cesse d'être un
annuaire critique citable et devient un palmarès qui se croit un thermomètre. À
ce moment précis — et à ce moment seul — je m'oppose à toute la refonte, quels
qu'en soient les autres mérites. Tout le reste se négocie ; cela, non.
