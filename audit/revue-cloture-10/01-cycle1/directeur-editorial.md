# Cycle 1 — Directeur·rice éditorial·e (gardien·ne du registre)

*Voix isolée. Audit du textuel encore « interne » sur le site publié
(communs.actitude.org). Critère unique : aucune phrase publique ne doit sentir
l'atelier, la machinerie de modèle, ou l'académie. Le registre cible est
« Eozen » — sobre, juste, incarné, jamais jargonnant ni self-conscious.*

---

## Préambule — la nature du résidu

La passe D1 a retiré les cicatrices de fabrication (« refonte #N »,
« session #N », « chantier »). Ce qui reste est plus tenace : c'est le
**vocabulaire du modèle lui-même**, exposé tel quel au lecteur. Le projet a
construit un moteur d'évaluation rigoureux ; il en a importé le lexique de
travail dans la prose publique. Le résultat est un texte propre, mais qui sonne
comme une *documentation d'outil* plutôt que comme une voix qui s'adresse à
quelqu'un. Trois familles de résidu :

1. **les termes-jetons du moteur** (« verdict », « co-gate », « proxy
   unidirectionnel », « indicateur composite conventionnel », « plafond de
   chaîne », identifiants de critères `travail_non_marchandise`, renvois à
   `ranking.yml`) — du *code* échappé dans la prose ;
2. **le méta-discours sur la fabrique** (« le verdict se calcule », « cadre
   explicite et contestable », « prise de position défendable », « statut de
   l'évaluation ») — utile, parfois nécessaire, mais trop répété et trop
   self-conscious ;
3. **le ton d'atelier ou académique** (citations de Polanyi, « marchandise
   fictive », « décommodification », « orthogonaux ») qui casse l'incarnation.

---

## 1. Cartographie par gravité

### A — À RETIRER du public (sonne irrémédiablement interne)

Ces tournures sont du jargon de modèle non introduit. Un lecteur non-expert n'a
aucune prise dessus ; pire, elles trahissent que le texte a été écrit pour des
ingénieurs du barème, pas pour lui.

- **« co-gate », « co-gaté », « les co-gates du sommet »** — `methode.html`
  (§ verdict, x4), `l/ferme-de-pommiers.html` (attribut `title` du badge),
  `dossiers/index.html` (5 occurrences dans les `title` des verdicts). C'est le
  pire résidu du site : un anglicisme d'ingénierie logique, jamais défini,
  répété mécaniquement, et **infiltré dans chaque info-bulle de verdict** —
  donc présent sur la quasi-totalité des fiches et dossiers.
- **« proxy UNIDIRECTIONNEL », « Lecture par proxy »** — `grilles.html`
  (définition de *Travail non marchandisé*). Vocabulaire de mesure ; les
  majuscules d'insistance aggravent l'effet « note interne ».
- **identifiants de critères en `code`** : `milieu_protege`,
  `usage_non_degradant`, `place_au_vivant` (`methode.html` § chaîne) ;
  `nature_interet`, `plafonds_chaine.ax2_par_nature dans ranking.yml`,
  `non_lucrative`, `commerciale_desactivee`, `commerciale_encadree`,
  `privee_individuelle` (`grilles.html`, critère *Aucun maillon commercial*).
  Ce sont littéralement des noms de variables et un chemin de fichier de
  configuration affichés au public. Inadmissible hors d'une annexe technique.
- **« Co-gate du sommet : il teste la décommodification du travail (3ᵉ
  marchandise fictive de Polanyi) »** — `grilles.html`. Triple faute : jargon
  de modèle + référence académique + concept non introduit, dans une *case de
  grille* censée aider à lire.
- **« indicateur composite conventionnel — à la manière de l'Indice de
  développement humain »** — `methode.html` (§ statut). Le souci de rigueur est
  juste, la formulation est d'économétrie.

### B — À ADOUCIR (légitime mais trop cru, trop répété, ou self-conscious)

Le sens doit rester ; seule la formulation sent l'atelier.

- **« verdict »** — partout (accueil, méthode, fiche, dossiers, carte). Mot
  central du modèle, jamais introduit comme tel sur l'accueil. Voir débat §5 :
  je ne demande pas sa suppression, mais son **introduction** et un adoucissement
  des emplois crus (« verdict sanctuaire », « verdict de milieu »).
- **« hybride / marchand / sanctuaire » employés nus** — accueil
  (« fausses libérations démasquées (montages marchands) », « au sommet
  décommodifié — le sanctuaire reste un horizon »), méthode, fiche. Ce sont les
  trois degrés du verdict, lancés au lecteur avant toute définition.
- **« le verdict ne se saisit jamais : il se calcule »**, **« il se calcule
  sur la nature des maillons, pas sur le chiffre »** — méthode, fiche. Méta-
  discours sur le fonctionnement du moteur. Vrai, mais l'aveu de mécanique
  (« se calcule ») refroidit.
- **« agrégation non compensatoire », « moyenne géométrique », « cinq axes
  orthogonaux »** — méthode, fiche, encart `fiche-key`. Le concept (l'axe faible
  commande, on ne rachète pas une faiblesse) est excellent et doit rester ; le
  *mot* « non compensatoire » / « orthogonaux » est de la statistique.
- **« cadre explicite et contestable », « défendable, contestable,
  perfectible », « prise de position, défendable et contestable »** — accueil,
  méthode, **footer de toutes les pages**. La formule est répétée à l'identique
  partout. Bonne intention (honnêteté épistémique), mais la **répétition** la
  transforme en tic défensif. À garder une fois, bien placée ; à varier ou
  alléger ailleurs.
- **« indice intrinsèque » / « indice effectif »** — méthode (§ chaîne), fiche.
  Distinction réelle et utile, mais double lexique technique. À nommer en mots.
- **« plafonné par la chaîne », « le plafond de chaîne »** — fiche (encart
  `chaine-note`), méthode. Image mécanique. Le lecteur voit « Axe 2 plafonné à
  40 par la chaîne… score intrinsèque : 100 » sans qu'on lui ait expliqué la
  logique en clair à cet endroit.
- **« Verdict à établir » / « à établir »** — `dossiers/index.html` (Larzac),
  fiches. Sonne comme un statut de base de données (champ non rempli). Se dit
  mieux : « verdict suspendu », « pas encore tranché — il manque une pièce ».

### C — TECHNIQUE LÉGITIME (acceptable *si introduit*)

Sur les pages méthode et grilles, un lexique assumé est défendable : c'est leur
fonction. La règle n'est pas de l'effacer mais de **l'introduire avant de
l'employer**, et de le **confiner** à ces pages.

- usus / fructus / abusus, démembrement, nue-propriété, usufruit, bail
  emphytéotique, fonds de dotation : **bien traités** — encadrés `enclair`,
  liés au glossaire. C'est le modèle à suivre pour le reste.
- « les cinq axes », « l'Indice de libération », « la chaîne » : termes maison
  assumés, correctement amorcés. À garder.
- Les définitions de critères dans `grilles.html` peuvent rester denses — mais
  **purgées des identifiants `code` et des renvois `ranking.yml`** (rang A).

---

## 2. Tableau de reformulations (extrait actuel → proposition Eozen)

| Page | Extrait actuel | Proposition |
|---|---|---|
| `methode.html` §verdict | « l'un des **co-gates** du sommet (habitat du vivant, régénération opposable…) n'est pas encore établi » | « l'une des conditions du sommet — habitat du vivant, milieu durablement protégé… — n'est pas encore réunie » |
| `methode.html` §verdict | « Le sommet est **co-gaté**. » | « Le sommet tient à plusieurs conditions à la fois. » |
| `methode.html` §verdict | « le **verdict** comme l'Indice sont un **indicateur composite conventionnel** » | « le verdict comme l'Indice sont une **lecture argumentée**, pas une mesure objective » |
| `methode.html` §verdict | « il se **calcule** à partir de la nature de chaque maillon » | « il **découle** de la nature de chaque maillon de la chaîne » |
| `grilles.html` *Travail non marchandisé* | « Lecture par **proxy UNIDIRECTIONNEL**, jamais déduite de la forme juridique » | « On ne le déduit jamais de la forme juridique : on regarde le travail réel qui fait vivre le lieu » |
| `grilles.html` *Travail non marchandisé* | « **Co-gate du sommet** : il teste la décommodification du travail (3ᵉ marchandise fictive de Polanyi) » | « C'est l'une des conditions du sommet : que le travail qui fait vivre le lieu ne soit pas vendu comme une marchandise » |
| `grilles.html` *Aucun maillon commercial* | « tous les maillons sont `non_lucrative` ou `commerciale_desactivee`… le score d'axe 2 est plafonné par la chaîne (plafond de chaîne, voir `plafonds_chaine.ax2_par_nature` dans `ranking.yml`) » | « tous les maillons sont non lucratifs, ou commerciaux mais désactivés (capital entièrement aux mains d'organismes d'intérêt général)… La note de cet axe ne peut dépasser ce que permet le maillon le plus faible de la chaîne. » *(retirer tout identifiant et le renvoi au fichier)* |
| `methode.html` §chaîne | « réalisée par le critère `milieu_protege` logé dans la grille du lieu » | « jugée sur la protection effective du milieu, au niveau du lieu » |
| `l/ferme-de-pommiers.html` encart | « Axe 2 (la structure) **plafonné à 40 par la chaîne**… (score intrinsèque : 100) » | « La structure ne peut être notée plus haut que **40** : un maillon de la chaîne — une société d'exploitation agricole — l'en empêche, quels que soient les critères cochés. » |
| `methode.html` §chaîne | « son indice **intrinsèque** » / « l'indice **effectif** relit… » | « sa note **propre** » / « sa note **une fois replacée dans ses chaînes** » |
| accueil §chiffres | « 0 — **au sommet décommodifié** — le sanctuaire reste un horizon » | « 0 — **aucune libération pleinement aboutie** : le sommet reste un horizon » |
| accueil §chiffres | « 4 — fausses libérations démasquées (**montages marchands**) » | « 4 — fausses libérations démasquées (la terre y reste captable par le marché) » |
| accueil §hero | « **agrégation non compensatoire** » *(via lien)* / méthode « cinq axes **orthogonaux** » | « la note retient l'axe le plus faible : une force ne rachète pas une faiblesse » / « cinq axes **indépendants** » |
| `dossiers/index.html` Larzac | « Verdict **à établir** » | « Verdict **suspendu** » (ou « **pas encore tranché** ») |
| footer (toutes pages) | « l'Indice de libération est une évaluation au regard d'un **cadre explicite et contestable**, non un label » | *(garder, mais une seule formule canonique ; ne pas la redoubler avec les variantes de l'accueil et de la méthode)* |

---

## 3. Machinerie exposée sans introduction (le lecteur tombe dessus à froid)

C'est le défaut le plus grave pour le registre : un terme du modèle apparaît
*avant* d'avoir été défini, à un endroit où le lecteur ne s'y attend pas.

- **« verdict » sur l'accueil et les badges sans définition d'accueil.** Le mot
  structure tout le site mais n'est jamais introduit sur la page d'arrivée. Sa
  première vraie définition est enterrée au §verdict de la méthode. Un visiteur
  qui voit « Montage hybride » sur une carte ou une fiche ne sait pas que c'est
  un *verdict* en trois degrés.
- **« co-gate » n'a aucune définition nulle part** — ni glossaire (pas
  d'entrée `g-co-gate`), ni méthode (employé, jamais défini). Le lecteur
  rencontre « les co-gates du sommet » comme un mot étranger.
- **« sanctuaire » comme degré apparaît sur l'accueil** (« le sanctuaire reste
  un horizon ») **avant** d'être qualifié de degré de verdict. Le lecteur lit un
  mot fort sans cadre.
- **« plafond de chaîne » / « intrinsèque vs effectif »** : sur la **fiche**, le
  bandeau `chaine-note` jette « plafonné à 40 par la chaîne… score intrinsèque :
  100 » avec un simple lien « Le plafond de chaîne → ». Le concept doit être
  dit en clair *là où il frappe*, pas seulement renvoyé à la méthode.
- **Référence à Polanyi et « marchandise fictive »** dans une case de
  `grilles.html` : registre académique surgissant dans un outil de lecture.

**Règle générale qui en découle** : aucun terme-maison (verdict, chaîne,
co-gate, plafond, intrinsèque/effectif) ne doit apparaître sur une page de
parcours (accueil, carte, dossiers, fiche) sans une glose d'une ligne *sur
place* ou un lien glossaire actif. Le glossaire couvre déjà chaîne, indice,
agrégation, commun — mais **pas verdict ni co-gate**, les deux plus exposés.

---

## 4. Éléments constitutifs (à fixer pour les passes suivantes)

**Glossaire interne → public** (table de correspondance de registre) :

| Interne (modèle) | Public (Eozen) |
|---|---|
| verdict | la qualification du lieu / où il se tient entre marché et commun |
| co-gate / co-gaté | condition (du sommet) / plusieurs conditions à la fois |
| proxy unidirectionnel | on regarde le fait réel, on ne le déduit pas de la forme |
| indicateur composite conventionnel | lecture argumentée (pas une mesure objective) |
| agrégation non compensatoire / moyenne géométrique | l'axe le plus faible commande ; on ne rachète pas une faiblesse |
| axes orthogonaux | axes indépendants |
| indice intrinsèque / effectif | note propre / note replacée dans ses chaînes |
| plafond de chaîne | la note ne peut dépasser ce que permet le maillon le plus faible |
| `milieu_protege`, `usage_non_degradant`, etc. | *(jamais d'identifiant en clair — toujours le libellé humain)* |
| à établir | suspendu / pas encore tranché |
| décommodification | sortie de la logique marchande |

**Trois règles de registre (à inscrire comme garde-fou éditorial) :**

1. **Pas de code dans la prose.** Aucun identifiant de critère en `police
   code`, aucun nom de champ, aucun chemin de fichier (`ranking.yml`) sur une
   page publique. Le générateur doit rendre le **libellé humain**, jamais la
   clé.
2. **Introduire avant d'employer.** Tout terme-maison est défini la première
   fois qu'il paraît sur une page de parcours, en une ligne `enclair` ou par un
   lien glossaire vivant. Le modèle déjà réussi : usus/fructus/abusus.
3. **Une honnêteté épistémique, dite une fois.** La formule « cadre explicite,
   contestable, non un label » est juste — mais répétée à l'identique dans le
   hero, la méthode (×3) et chaque footer, elle vire au tic défensif. Une
   formulation canonique au footer ; ailleurs, on la varie ou on la sous-entend.

**Lexique légitimement technique, à confiner** : méthode + grilles peuvent
garder usus/fructus/abusus, démembrement, axes, Indice, chaîne (tous déjà
glosés). Tout le reste (co-gate, proxy, plafond, intrinsèque/effectif, composite
conventionnel) doit ou disparaître, ou se traduire en mots.

---

## 5. Désaccords prévus (à arbitrer en cycle 2)

- **Avec le/la stratège de l'attractivité** — voudra sans doute garder
  « verdict » comme **accroche** : c'est un mot fort, tranchant, partageable
  (« on rend un verdict sur chaque lieu »). Je ne demande pas sa suppression —
  il a une vraie valeur d'incarnation, plus chaude que « note ». Mon désaccord
  porte sur l'**introduction** : un verdict non défini sur l'accueil est une
  promesse sans contenu. Compromis probable : garder le mot, l'introduire d'une
  ligne dès le hero.
- **Avec l'architecte d'information** — pourrait défendre les info-bulles
  `title` longues (la définition complète du verdict dans chaque badge) comme un
  service au lecteur. Je conteste : la définition actuelle des `title` contient
  « co-gates », « régénération opposable », « lucrativité encadrée » — du jargon
  qui aggrave plutôt qu'il n'aide. Une info-bulle doit dire en *une phrase
  humaine* ce qu'est un montage hybride, pas réciter la règle du modèle.
- **Avec moi-même (tension interne assumée)** — sur l'accueil, « non
  compensatoire » et « décommodifié » sont *justes* et disent une fierté du
  projet (la rigueur qui démasque les faux amis). Les adoucir risque de diluer
  la prise de position. Garde-fou : **on n'académise pas davantage, mais on ne
  désarme pas non plus la position** — on la dit en mots de tout le monde
  (« l'axe le plus faible commande », « la terre y reste captable ») plutôt
  qu'en termes de discipline.

**Contre-règles respectées** : je n'ai pas supprimé la prise de position (le
projet l'assume), je n'ai pas académisé davantage, je n'ai pas touché au calcul.
Je propose des reformulations ; je n'implémente pas.

---

## Résumé (< 150 mots)

Les **cinq résidus internes les plus criants**, par gravité :

1. **« co-gate / co-gaté »** — anglicisme d'ingénierie, jamais défini, infiltré
   dans chaque info-bulle de verdict (méthode, fiches, dossiers).
2. **Identifiants de critères en `code` + renvoi à `ranking.yml`** dans
   grilles.html et méthode — des noms de variables et un chemin de fichier
   affichés au public.
3. **« proxy unidirectionnel » + « marchandise fictive de Polanyi »** dans une
   case de grille — jargon de mesure et référence académique là où l'on devrait
   aider à lire.
4. **« verdict » et ses degrés (hybride/marchand/sanctuaire) jamais introduits**
   sur les pages de parcours : le lecteur tombe dessus à froid.
5. **« cadre explicite et contestable » répété à l'identique** (hero, méthode,
   chaque footer) — l'honnêteté épistémique vire au tic défensif.

**Ma règle de registre** : *pas de code dans la prose ; introduire tout
terme-maison avant de l'employer ; l'honnêteté épistémique se dit une fois, en
mots de tout le monde.*
