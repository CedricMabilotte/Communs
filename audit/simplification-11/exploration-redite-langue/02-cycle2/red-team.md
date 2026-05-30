# Cycle 2 — Red-team

*Rôle : chasseur de contradiction. Les trois voix du cycle 1 ont convergé vite
sur « deux gestes se renforcent, friction à 2-3 zones ». J'attaque ce confort,
texte du site en main. Je ne modifie rien.*

---

## 0. Le consensus, tel qu'il se présente — et pourquoi il ment par omission

Les trois voix livrent la même structure rassurante : *un tableau* (§1 double
gain / §2 friction / §3 honnêteté sur le coût), une *règle d'incise ≤ 6 mots*
qui « neutralise l'essentiel du surcoût », et un *ordre* (couper d'abord). Le
juge lâche pourtant, en toute fin, qu'il faut un **troisième geste**
(stratifier). Personne n'a tiré le fil de cet aveu. Je le tire : il défait la
question de séance.

---

## 1. Le « troisième geste » n'est pas un appendice — il est la réponse

Relisons le juge, §3-§4 : la fusion verdict·Indice·palier « n'est un gain que si
elle s'accompagne d'une mise en profondeur — ce qui est, de fait, un troisième
geste ». Et : couper+reformuler « ne résout pas la densité d'instruments — elle
la laisse intacte ». Traduction sans gants : **les deux gestes ne touchent pas
le vrai problème de la fiche**. Le problème de la Ferme de Pommiers n'est pas
qu'un mot est dur ou qu'un bloc est répété — c'est qu'on y empile, vérifié ligne
à ligne (l. 63-97) : badge-anneau, pentagone, **5 barres d'axe**, échelle à 5
segments, ghost à 67, curseur à 65, ligne fiabilité, ligne complétude,
note-chaîne « plafond 40 », recap de grille 5 lignes, puis grille complète de
**22 critères**. Couper les redites textuelles et raccourcir le jargon laisse
les ~14 instruments en place.

Donc : si « ça marche » exige de stratifier (façade / pli / page-méthode), alors
la réponse honnête à « deux gestes suffisent-ils » est **non**, et le consensus
déguise une **réarchitecture de la fiche** en « deux petits gestes + une note de
bas de page ». Le fusionneur le concède d'ailleurs sans le nommer : son geste 1
(« objet-verdict composite ») *est* une refonte de composant, pas une coupe. On
appelle « simplification par deux gestes » ce qui est en réalité : couper +
reformuler + **reconcevoir le score-panel**. Trois gestes, dont le troisième est
le plus lourd. **Tranché : la prémisse est fausse telle qu'énoncée.**

## 2. « Couper d'abord » détruit l'information qui dit QUOI reformuler

Le fusionneur prescrit l'ordre : « couper d'abord, reformuler le résidu » (sa
3ᵉ ligne de retour). Or ses deux coups les plus assumés — supprimer l'aside
« Trois lectures » (l. 51-62) et le `details` « Comment lire les visuels »
(l. 98-109) — **suppriment précisément les deux gloses qui disent comment
reformuler le résidu**.

- L'aside porte la seule articulation de « 65 / Montage solide / hybride » : que
  le palier « Libération aboutie » est *réservé au verdict sanctuaire*. Si je
  coupe l'aside avant de reformuler, le reformulateur, devant l'objet-verdict
  composite nu, doit **réinventer** cette règle pour écrire sa glose d'incise —
  alors qu'elle était écrite, juste là, dans le bloc qu'on vient de jeter.
- Le `details` porte la légende du pentagone (« plus la zone s'étend… »). Le
  fusionneur le coupe, puis (sa §4-b) *concède* qu'il faut réinjecter une
  micro-légende. Il reconstruit donc à la main une information qu'il vient de
  supprimer.

C'est un anti-pattern : on détruit la source, puis on en regénère un fragment de
mémoire, au risque de la déformer. L'ordre correct est **l'inverse** : repérer,
dans les blocs candidats à la coupe, le **noyau de sens non redondant** (la
règle « solide ≠ abouti », la clé du pentagone), le formuler en clair *d'abord*,
*puis* couper le bloc devenu vide. Le consensus « couper d'abord » optimise le
compteur de mots au prix d'un risque d'erreur sémantique. **Mauvais ordre.**

## 3. Le `title` « < 20 mots » écrase des cas hétérogènes — vérifié

Les trois voix célèbrent le title hybride raccourci de 60 → 20 mots comme
« l'exemple-roi du double gain ». Faux confort. Le générateur
(`generate_site.py`, `verdict_badge`, l. 1401-1412) prouve que **ce title n'est
pas dupliqué à la main : il est injecté depuis une source unique**,
`concepts.verdict.degres[].definition`. La « coupe » que vante le fusionneur
(« sourcer une fois, injecter ») **existe déjà** : la redite est une *illusion
de surface*, le geste A n'a rien à y gagner. Reste donc le seul geste B —
raccourcir la définition. Et là, la définition actuelle encode deux cas
disjoints (l. 48 de la fiche) : (i) un maillon à **lucrativité encadrée**
(intérêt privé discipliné), (ii) une **SCEA/GAEC preneuse de bail** sous porteur
hors-marché (le bénéfice d'exploitation reste approprié), **plus** (iii) le
commun où *une* condition du sommet manque. La proposée du reformulateur — « un
maillon garde un intérêt privé, ou une condition du sommet manque » — **fond (i)
et (ii) en "intérêt privé" et perd (ii) entièrement** : un GAEC preneur de bail
n'a pas d'« intérêt privé » au sens d'un investisseur ; c'est l'appropriation du
*bénéfice d'exploitation* qui le plafonne, mécanique différente, encodée
différemment dans `compute_verdict` (l. 1363-1377 : `exploitation_agricole` et
`commerciale_encadree` sont deux branches distinctes). Raccourcir à 20 mots
**fusionne deux verdicts que le code distingue**. Le badge ment alors sur la
moitié du corpus (toutes les fermes en bail rural — dont Pommiers elle-même).
**Vrai : reformuler court ici détruit une distinction load-bearing.**

## 4. La fusion « lisible à 3 conditions » est un report de complexité, pas une simplification

Le juge pose froidement (§3) : la fusion verdict·Indice·palier ne tient que sous
**trois conditions** — hiérarchie visuelle stricte, détail technique replié,
phrase d'articulation unique. Un dispositif qui n'est sûr que si trois invariants
tiennent simultanément n'est pas plus simple : il est *plus fragile*. La
complexité n'a pas disparu, elle a migré du texte visible vers des **conditions
implicites de rendu** que rien ne garde.

Et qui les garde ? Le CLAUDE.md du projet le dit : « Les garde-fous du générateur
(uid, chaînes, entités HTML) ne voient pas la mise en page : seul l'œil de
l'opérateur la valide » (Leçon L9). Donc les trois conditions du juge sont
**non testables automatiquement**. Scénario concret, inévitable quand le corpus
grandit : une fiche future a un Indice à deux chiffres + un ghost très écarté du
curseur + une note de plafond longue (cas multi-maillons). La « hiérarchie
visuelle » prévue pour Pommiers (un chiffre dominant, palier en sous-titre)
casse — l'objet composite redevient le « bloc-bouillon » que le juge redoutait,
et **aucun garde-fou ne le signale**. La simplification d'aujourd'hui est une
dette de demain, payable en revue manuelle à chaque nouvelle fiche atypique.
**Une simplification conditionnelle non gardée est un report de complexité.**

## 5. L'angle mort que personne n'a vu : la coupe casse l'accessibilité ET la cohérence à l'échelle du corpus

Trois voix ont raisonné « lecteur voyant qui scanne / militant / curieux ».
Aucune n'a regardé le **lecteur d'écran** ni le **générateur à l'échelle**.

**(a) Accessibilité — la coupe supprime du texte que seuls les non-voyants
lisent.** Sur la fiche (l. 66), le badge Indice porte un `span.visually-hidden` :
« Indice de libération 65 sur 100, Montage solide ». Le pentagone porte un
`aria-label` détaillé (l. 68 : « Le sol 87, La structure 40… »). Les segments
d'échelle ont des `title` (l. 92). Le `details` « Comment lire les visuels » est
*la* version texte de visuels qui sont, pour le reste, des SVG `aria-hidden`. Le
juge a justifié de couper le `details` en disant « le bloc est déjà replié, le
scanneur ne le voit pas » — raisonnement *purement visuel*. Pour un utilisateur
de lecteur d'écran, un `<details>` n'est pas « invisible » : il est annoncé et
ouvrable, et c'est souvent **la seule narration en clair** d'un graphe sinon muet.
Couper le `details` de chaque fiche et le renvoyer à `methode.html` impose au
non-voyant un **aller-retour entre deux pages** pour comprendre un visuel que le
voyant lit d'un coup d'œil. La « coupe sans coût » a un coût, payé par ceux qu'on
ne voit pas dans les trois personas. Toute coupe doit donc être auditée sur la
couche a11y, pas seulement sur la couche visuelle — front jamais mentionné.

**(b) Cohérence à l'échelle — « gloser à la première occurrence » n'a pas de
sens sur un site généré, multi-pages, multi-points-d'entrée.** Le reformulateur
fonde toute sa règle de tri sur « glose en ligne à la **première occurrence sur
la page**, renvoi ensuite ». Mais le site n'a pas d'ordre de lecture : un
visiteur peut arriver par SEO directement sur `ferme-de-pommiers.html` sans
jamais voir `methode.html` ni `regimes.html`. La « première occurrence » est une
fiction : *chaque* page est potentiellement la première. Si la glose d'*usufruit*
ne vit qu'« une fois » sur la méthode, le lecteur entré par une fiche tombe sur
le terme nu. Pire pour la maintenance : ces gloses sont produites par le
**générateur** à partir des `concepts/*.yaml`. « Une glose, une fois » suppose
une logique conditionnelle « est-ce la première occurrence ? » que le générateur
n'a pas et qui n'a pas de réponse stable (l'occurrence dépend du parcours, pas du
build). Le choix réel est binaire et structurel : *soit* le terme est glosé
**partout** (et la « redite » que le fusionneur veut couper est en fait la
condition d'autonomie de chaque page indexée), *soit* il renvoie **partout** au
glossaire. Le « une fois ici, lien ensuite » du reformulateur ne se code pas sans
casser l'indépendance des pages — et c'est un effet SEO en prime : des fiches
amputées de leur glose perdent en autonomie et en richesse sémantique pour
l'indexation. **Angle mort double : a11y + nature générée/multi-entrée du site.**

---

## Verdict tranché

**Deux gestes suffisent-ils ? Non.** Trois voix l'ont presque dit et ont reculé.
Couper + reformuler traitent le *symptôme textuel* (redites, jargon) mais pas la
*maladie* (densité d'instruments concurrents sur la fiche-lieu), et leur mise en
œuvre honnête exige (a) un **troisième geste de stratification** que le juge a
nommé, (b) un **ordre inversé** (extraire le noyau de sens *avant* de couper), et
(c) une **discipline a11y + cohérence multi-pages** que personne n'a posée.

**La condition honnête : deux gestes suffisent SI et seulement si l'on accepte de
les requalifier.** « Couper » ne veut pas dire *supprimer* mais *déplacer en
profondeur* (donc le geste de stratification n'est pas un troisième geste : c'est
ce que « couper » aurait dû signifier depuis le départ) ; et « reformuler » ne
veut pas dire *raccourcir à tout prix* mais *préserver la distinction* (le title
hybride reste long ou se scinde en deux titles — GAEC-bail ≠ SCI privée — plutôt
que de mentir court). À ces deux conditions, et avec un audit a11y systématique
par coupe, deux gestes *bien définis* portent l'essentiel. Sous leur définition
naïve du cycle 1 (« couper = enlever du texte, reformuler = faire court »), ils
ne suffisent pas et peuvent **régresser** le site.
