# Parcours détaillé des améliorations — Communs (cadrage #11)

*Chaque item : **contexte** (l'état actuel, vérifié) · **critique** (le problème) ·
**solutions** (les options) · **reco** (le geste retenu). Cadrage seulement.
Garde-fous transverses rappelés en tête de `ameliorations.md` : couper = le plus
souvent déplacer/renvoyer ; ne pas casser l'accessibilité ; reformuler sans
tronquer au point de faire mentir.*

---

# PAQUET 1 — Zones / structures inutiles ou répétées

## 1.1 — Aside « Trois lectures, distinctes à dessein » (fiche de lieu)

**Contexte.** En tête de chaque fiche de lieu, juste après le titre et le badge,
un encart `verdict-cle` à trois puces explique la différence entre le verdict, l'
Indice et le palier — y compris la subtilité « un Indice élevé peut rester
"solide" sans être "abouti" ». Répété à l'identique sur les 45+ fiches, avant la
présentation du lieu.

**Critique.** C'est un cours de méthodologie posé en travers du chemin : le
lecteur veut le lieu, on lui sert un rappel de doctrine qu'il n'a pas demandé. Le
primo décroche ; le directeur éditorial y voit la redite la plus coûteuse
(verdict + Indice + palier re-définis ×45) ; mais le red-team prévient qu'une
coupe sèche rend « Hybride · 65 · Montage solide » illisible pour qui débarque.

**Solutions.** (a) Supprimer l'encart. (b) Le replier derrière un `details`
« Comment lire ces trois mesures ». (c) Le réduire à **une phrase** + lien Méthode,
gardée visible sur la fiche.

**Reco.** **(c)** — une phrase (« Verdict, Indice et palier ne disent pas la même
chose → Méthode ») conservée sur la fiche, l'encart à puces supprimé. On garde le
sens (le lecteur isolé n'est pas muet) sans le cours. Idéalement placée *sous* le
panneau de score, pas avant le lieu.

## 1.2 — `details` « Comment lire les visuels de cette fiche »

**Contexte.** Bloc dépliable présent sur toutes les fiches, qui réexplique « l'
Indice retient l'axe le plus faible… une force ne rachète pas une faiblesse » +
la lecture du pentagone et des barres. Doublon des `axe-cards` de la page Méthode.

**Critique.** Contenu didactique pur, sans fait propre au lieu, répété ×45.
*Mais* (red-team, angle accessibilité) : ce bloc et ses `aria-label` sont
souvent la **seule narration en clair** des visuels SVG pour un lecteur d'écran.
Le supprimer franchement dégrade l'accessibilité.

**Solutions.** (a) Supprimer. (b) Replier (déjà le cas) et **alléger** le texte au
strict minimum, en conservant la description accessible des visuels, et renvoyer
la *règle générale* à la Méthode. (c) Laisser tel quel.

**Reco.** **(b)** — garder un `details` court qui décrit ce que montrent le
pentagone/les barres (pour l'accessibilité), retirer la ré-explication de la
règle d'agrégation (qui vit sur Méthode). Alléger, pas supprimer.

## 1.3 — Pentagone + 5 barres d'axe chiffrées (panneau de score)

**Contexte.** Le panneau de score affiche le profil deux fois : le pentagone
(forme) et les cinq barres chiffrées (mêmes valeurs). Le pentagone porte déjà les
valeurs en sommets et `aria-label`.

**Critique.** La même donnée, montrée deux fois en première profondeur — charge
visuelle sans information nouvelle.

**Solutions.** (a) Garder pentagone + barres. (b) Garder le pentagone en façade,
**replier** les 5 barres chiffrées dans le dépli détail (avec la grille).
(c) Garder les barres, supprimer le pentagone.

**Reco.** **(b)** — le pentagone en façade (lecture de forme immédiate), les
chiffres exacts dans le dépli pour qui les veut. On ne perd rien, on désempile.

## 1.4 — Trois annotations de plafond dispersées (note de chaîne · ghost · complétude)

**Contexte.** Le panneau porte trois mentions de plafond éparpillées : la
`chaine-note` (« la structure ne peut être notée plus haut que 40 »), le point
« ghost » (indice brut avant pénalité, ex. 67→65), et la note de complétude.

**Critique.** Trois mécanismes de plafonnement présentés à trois endroits — le
lecteur ne voit pas qu'ils relèvent de la même logique « ce qui limite la note ».

**Solutions.** (a) Statu quo. (b) Les **regrouper** en une ligne « Plafonds
appliqués » sous le profil, repliable, qui les dit d'un trait. (c) Les masquer
tous.

**Reco.** **(b)** — une zone unique « Plafonds appliqués » repliable (maillon
limitant + pénalité de complétude). Information vraie conservée, dispersion
supprimée.

## 1.5 — Verdict / Indice / palier éclatés en trois zones

**Contexte.** Le verdict est un badge dans l'entête ; l'Indice et le palier sont
dans le panneau ; l'échelle de paliers ailleurs dans le panneau. Trois objets
distincts à dessein (qualitatif / quantitatif / tranche conditionnée).

**Critique.** Visuellement dispersés, ils obligent le lecteur à recomposer la
lecture. *Mais* (gardien + red-team) : les **fusionner en une valeur unique**
produirait le palmarès unidimensionnel que le projet refuse — un Indice à 72 qui
reste « solide » sans être « abouti » (cas Rayol) doit rester lisible.

**Solutions.** (a) Statu quo. (b) **Objet-verdict composite** : une ligne
« Hybride · 65 · Montage solide » + renvoi unique « pourquoi ces trois ? →
Méthode », avec trois libellés typographiquement distincts et le cas de
non-coïncidence visible. (c) Fusionner en une note unique.

**Reco.** **(b)**, sous les trois conditions du gardien : signifiants
irréductibles (badge coloré · nombre /100 · étiquette de palier), non-coïncidence
lisible, renvoi obligatoire. On rapproche la *zone d'affichage*, jamais les
concepts. (Rend l'item 1.1 presque inutile : la distinction est portée par
l'objet.)

## 1.6 — Grille des ~22 critères dépliée par défaut

**Contexte.** Le tableau détaillé critère par critère (~21-22 lignes) est en
`<details open>` : ouvert d'emblée sur chaque fiche.

**Critique.** L'annexe technique occupe la fiche par défaut ; division par ~3 de
la hauteur perçue si repliée. Aucun coût pour le primo (le chercheur déplie).

**Solutions.** (a) Laisser ouvert. (b) `<details>` **fermé** par défaut, recap
visuelle (pentagone) en façade. (c) Sortir la grille sur une sous-page.

**Reco.** **(b)** — fermer par défaut. Geste à risque nul, gain immédiat.

## 1.7 — Triptyque usus/fructus/abusus rédigé en entier 3 fois

**Contexte.** Le triptyque est exposé en entier sur `methode.html#triptyque` ET
`regimes.html#triptyque` (quasi mot pour mot, chapeau + définitions des trois
droits) ET en entrée de glossaire. Source : `config/concepts.yml` (bloc
`triptyque`, avec `chapeau`, `en_clair`, et les trois `droits`).

**Critique.** Un écran entier de prose quasi identique entre deux pages-cadre
voisines. Le gardien le concède sans réserve (« exposé 3 fois, se coupe sans
perte »).

**Solutions.** (a) Statu quo. (b) Foyer unique = **Régimes** (sa maison, avec les
pôles) ; Méthode garde 2 lignes + ancre `regimes.html#triptyque` ; glossaire =
entrée courte. (c) Foyer = Méthode.

**Reco.** **(b)** — Régimes porte la version longue (c'est le cadre conceptuel) ;
la Méthode renvoie. Comme la source est `concepts.yml`, techniquement il s'agit de
ne *render* le bloc long qu'à un seul endroit.

## 1.8 — Disclaimer « non un label » en copie longue ×9 + hero + classement

**Contexte.** La phrase « évaluation au regard d'un cadre explicite et
contestable, non un label » figure intégralement dans les **9 pieds de page**, le
hero d'accueil, le callout du classement, et `methode.html`.

**Critique.** La phrase doctrinale réaffirmée en entier partout. *Mais*
(éditorial, auto-red-team) : sur une **fiche ouverte seule** (partage, moteur),
c'est le seul endroit où le lecteur voit le statut épistémique sans pouvoir
cliquer — une demi-ligne y reste utile.

**Solutions.** (a) Statu quo. (b) Foyer = Méthode ; **demi-ligne autonome** en pied
de fiche ; supprimer les copies longues des pages-cadre qui ont la Méthode à un
clic. (c) Tout supprimer sauf Méthode.

**Reco.** **(b)** — six mots affirmatifs (« selon un cadre assumé ») en pied de
fiche, la version longue seulement sur Méthode, copies des autres pages
supprimées.

## 1.9 — Accueil : deux blocs de chiffres redondants

**Contexte.** L'accueil porte « chiffres-clés » (45 / 4 / 0) en haut, puis « état
du corpus » (histogramme des paliers + « 45 lieux, 23 porteurs, 42
usufruitiers ») plus bas. Les deux disent la composition du corpus.

**Critique.** Même information à deux endroits éloignés de la page.

**Solutions.** (a) Statu quo. (b) **Fusionner** en un seul bloc « État du corpus »
(les trois grands nombres + l'histogramme côte à côte). (c) Supprimer l'un.

**Reco.** **(b)** — un bloc unique. (Le sort du « 4 » et du « 0 » en première vue
est traité au paquet 2 / arbitrage T1 antérieur — ici on parle seulement de la
fusion des deux blocs.)

## 1.10 — Accueil : 5 cartes pleines « modèles voisins »

**Contexte.** En bas de l'accueil, cinq `card` complètes (badge + pentagone +
sous-titre + méta juridique) pour des modèles de référence hors classement,
*estimés*. Le détail existe déjà sur `modeles.html`.

**Critique.** Le bloc le plus lourd de la page pour l'information la moins
prioritaire pour un visiteur ; cinq objets complexes de plus à décoder.

**Solutions.** (a) Statu quo. (b) **Teaser** (titre + lien « Voir les modèles
voisins »). (c) Supprimer la section de l'accueil.

**Reco.** **(b)** — teaser vers `modeles.html`, comme la carte est déjà un teaser.

## 1.11 — Leads des pages-cadre : 5 axes ré-énumérés + double callout anti-palmarès

**Contexte.** `classement`, `comparer`, `themes`, `grilles` rouvrent chacune par
un rappel des cinq axes ; le callout « comparer ce qui est comparable » est rédigé
**deux fois** (classement ET comparer).

**Critique.** Re-cours sur les axes à chaque page ; callout dupliqué. Le callout
est légitime *là où il sert* (le classement, qui invite le plus à lire en
palmarès), pas ailleurs.

**Solutions.** (a) Statu quo. (b) Callout complet sur le **classement seul** ;
ailleurs une ligne + lien ; ré-énumération des axes remplacée par « cinq axes →
Méthode » ; `axe-legend` graphique gardée là où il y a un pentagone.

**Reco.** **(b)** — un seul foyer pour le callout, les leads désencombrés, la
légende conservée seulement sous un visuel.

## 1.12 — Manifestes de revue : préambules jumeaux

**Contexte.** Les 4 `revues/*/index.md` rouvrent par une reformulation de la
formule de « libérer », répètent un bloc « Forme » (édition vivante) quasi
identique, et le footer italique « Ligne éditoriale temporaire, à réviser ».

**Critique.** Quatre reformulations identiques des mêmes méta-règles ; chaque
revue démarre sur le cadre commun au lieu de son sujet propre.

**Solutions.** (a) Statu quo. (b) Remonter « édition vivante » + posture
archétype-pas-de-noms sur la **page-mère `revues/index.html`** ; vider les
manifestes de ces blocs ; chaque revue cite la formule en 1 ligne + lien.
(c) Supprimer les manifestes.

**Reco.** **(b)** — méta-règles dites une fois sur la page-mère ; chaque manifeste
ne porte que ce qui lui est propre.

## 1.13 — Le canon se répète lui-même (à nettoyer en premier)

**Contexte.** Deux entrées de glossaire se recouvrent (`g-agregation-non-
compensatoire` et la part redondante de `g-indice-de-liberation`) ; le paragraphe
`methode.html#integrite` contient deux fois la phrase « la protection du foncier
se mesure à l'axe 1, la nature à l'axe 2 ».

**Critique.** On ne peut pas faire d'un foyer la « source unique » s'il se répète
lui-même. Prérequis aux renvois des items 1.1–1.12.

**Solutions.** (a) Statu quo. (b) Fusionner les deux entrées de glossaire ;
réécrire `#integrite` sans son doublon interne.

**Reco.** **(b)**, **à faire avant** les renvois — on nettoie le canon, puis on y
pointe.

---

# PAQUET 2 — Formulations pas claires pour qui débarque

*Avant → après indicatifs. Aucun de ces gestes ne change un concept, une note ou
un verdict : on change la langue. Dosage : glose d'incise en ligne réservée aux
6-8 termes sans lesquels la phrase suivante est incompréhensible ; le reste reste
au glossaire, lié.*

## 2.1 — « décommodifiée » (hero d'accueil, 1ʳᵉ phrase)

**Contexte.** Le lead du hero pose « …un cadre explicite et assumé — celui d'une
économie citoyenne, non lucrative et décommodifiée ». Mot savant, non glosé,
aucune entrée de glossaire, dans la première phrase de présentation.

**Critique.** Le terme le plus obscur à l'endroit le plus vu et le plus précoce :
le lecteur froid bute avant d'avoir rien compris.

**Solutions.** (a) Garder + gloser. (b) **Remplacer** dans le hero par « qui
retire la terre du marché » ; garder « décommodifié » glosé une seule fois sur la
Méthode, pour qui veut le terme. (c) Garder tel quel.

**Reco.** **(b)** — plus clair *et* plus court dans le hero ; le mot technique
survit une fois ailleurs.

## 2.2 — Le `title` du badge hybride (~60 mots, vu partout)

**Contexte.** L'infobulle du badge *hybride* (« La chaîne ne comporte aucun
maillon marchand, mais au moins un maillon à lucrativité encadrée — intérêt privé
discipliné, non désactivé — ou une société civile d'exploitation agricole
preneuse de bail sous un porteur hors-marché… ») fait ~60 mots de jargon. Elle
s'affiche au survol de **chaque** badge (accueil, vignettes, fiches). Source :
`config/concepts.yml` → `verdict.degres[].definition` (donc **source unique**,
pas une duplication manuelle — vérifié).

**Critique.** Texte le plus vu du site et l'un des plus opaques. *Mais* (red-team,
vérifié dans `compute_verdict`) : le raccourcir à « <20 mots » fondrait deux cas
que le moteur distingue — « GAEC preneur de bail » et « lucrativité encadrée » —
et ferait **mentir** le badge sur les fermes en bail rural, Pommiers comprise.

**Solutions.** (a) Statu quo. (b) **Réécrire en clair sans raccourcir au point de
fondre les cas** : une phrase d'accroche simple (« Foncier libéré, mais un maillon
garde une part de profit privé, légitime mais réelle ») suivie, si besoin, de la
précision des deux cas. (c) Raccourcir à <20 mots.

**Reco.** **(b)** — clarifier la langue dans `concepts.yml`, garder la distinction
des cas. *Ne pas* traiter ça comme une simple coupe : ce n'est pas une redite (la
source est unique) et un libellé trop court serait faux.

## 2.3 — « sommet » et « étoile polaire »

**Contexte.** « Sommet » est employé comme synonyme de *sanctuaire* / *palier le
plus haut* (méthode, accueil, dossiers) sans qu'on dise jamais l'équivalence.
« Étoile polaire » apparaît sur l'accueil (« le sommet n'est pas une case à
remplir — c'est une étoile polaire »).

**Critique.** « Sommet » est un troisième nom caché pour une chose qui en a déjà
deux (sanctuaire / libération aboutie) ; « étoile polaire » empile une 2ᵉ
métaphore sur la 1ʳᵉ pour une idée simple (un idéal jamais atteint).

**Solutions.** (a) Garder. (b) **Discipliner « sommet »** : poser l'équivalence
*sommet = sanctuaire = palier le plus haut* au premier emploi, puis s'en tenir à
« sanctuaire » (sauf registre narratif des dossiers) ; **remplacer « étoile
polaire »** par une seule image, « horizon » (déjà employé sur le site). (c) Tout
supprimer.

**Reco.** **(b)** — une seule image (« horizon »), équivalence de « sommet » posée
une fois. Le gardien concède l'empilement de métaphores.

## 2.4 — « démembrement »

**Contexte.** Concept central (séparation nue-propriété/usufruit). La Méthode
emploie déjà l'alternative « dissociation de la propriété et de l'usage » ; le
glossaire les dit synonymes. Source `concepts.yml` (montage `demembrement`).

**Critique.** Le mot évoque la boucherie pour qui débarque, alors qu'une
formulation claire existe déjà dans le projet.

**Solutions.** (a) Garder « démembrement » en première formulation. (b) **Promouvoir
« dissociation de la propriété et de l'usage »** en première ligne, « démembrement »
entre parenthèses comme terme technique. (c) Abandonner « démembrement ».

**Reco.** **(b)** — la formulation parlante d'abord, le terme juridique conservé
entre parenthèses (il reste juste et utile au lecteur averti).

## 2.5 — « usufruit / nue-propriété » (rôles pivots jamais glosés)

**Contexte.** Ce sont les deux rôles structurants de tout le site (« Porteurs »,
« Usufruitiers » en navigation), employés sans glose dans la nav elle-même.

**Critique.** Le lecteur ne sait pas que *porteur = possède sans utiliser,
usufruitier = utilise sans posséder* — la mécanique fondatrice du site reste
opaque.

**Solutions.** (a) Statu quo (glossaire seul). (b) **Glose jumelée posée tôt** (sur
la Méthode, avant le premier emploi technique, idéalement en bandeau léger) : « l'
un possède la terre sans s'en servir, l'autre s'en sert sans la posséder ».
(c) Renommer les rubriques de nav.

**Reco.** **(b)** — la phrase jumelée tôt sur la Méthode ; garder les termes (ils
sont irremplaçables) mais les rendre clairs une fois.

## 2.6 — « triptyque »

**Contexte.** Mot-chapeau du bloc usus/fructus/abusus (méthode, régimes,
glossaire). Les trois droits sont déjà glosés ; c'est le chapeau qui est savant.

**Critique.** « Triptyque » ajoute une abstraction d'art par-dessus trois termes
latins — double barrière.

**Solutions.** (a) Garder. (b) **Remplacer « triptyque » par « les trois pouvoirs
du propriétaire »**, garder usus/fructus/abusus glosés dessous.

**Reco.** **(b)** — le chapeau en clair, les trois latins conservés (glosés). À
faire dans `concepts.yml`.

## 2.7 — « opposable » et « rentier »

**Contexte.** « Opposable » (qu'on peut faire valoir en droit) apparaît dans la
définition du sanctuaire — donc charnière ; « rentier » au sens économique
(vivre du loyer sans travailler le bien) dans méthode/fiches.

**Critique.** Termes précis employés nus : « opposable » est du droit pur ;
« rentier » est entendu « riche oisif » plutôt que dans son sens technique.

**Solutions.** (a) Garder nus. (b) **Glose d'incise au premier emploi** :
« opposable » → « qu'on peut faire respecter en justice » ; « rentier » → « un
usage qui sert surtout à encaisser un loyer ». (c) Remplacer.

**Reco.** **(b)** — incise courte au premier emploi, terme conservé (précis et non
substituable).

## 2.8 — « agrégation non compensatoire »

**Contexte.** Nom du mode de calcul de l'Indice (méthode + entrée glossaire
dédiée). Le concept est limpide (« l'axe le plus faible commande ») ; le nom est
opaque.

**Critique.** Le titre de paragraphe impose le terme nu avant que le concept soit
dit en clair.

**Solutions.** (a) Garder le terme en titre. (b) **Dire le concept en clair au
premier emploi** (« l'axe le plus faible commande — une force ne rachète pas une
faiblesse »), garder « agrégation non compensatoire » comme étiquette technique
secondaire/glossaire.

**Reco.** **(b)** — le sens d'abord, l'étiquette technique en second.

## 2.9 — « indice intrinsèque / effectif », « axes contaminables », « domiciliage »

**Contexte.** Trois couches de jargon-maison sur la même section de la Méthode
(la chaîne et les lieux reliés).

**Critique.** Le lecteur curieux décroche au 3ᵉ terme ; métaphores internes
empilées (« contaminable », « domicile d'un axe »).

**Solutions.** (a) Statu quo. (b) **Une phrase humaine** : « une structure vaut par
les lieux qu'elle fait vivre, pas par ses seuls statuts ; si ces lieux sont moins
bons que sa note de principe, c'est leur niveau qui compte » ; garder *un* terme
imagé (« la chaîne »), traduire le reste.

**Reco.** **(b)** — reformuler en clair, ne garder qu'une image, reléguer les
étiquettes techniques au glossaire.

## 2.10 — Hero-lead trop long + mise en garde avant le sujet

**Contexte.** Sous l'accroche « La terre n'est pas une marchandise », un lead de
~6 lignes, puis « c'est une prise de position, défendable et contestable, non une
mesure neutre » — la mise en garde épistémique arrive avant que le sujet soit
compris.

**Critique.** On prépare le lecteur à la controverse méthodologique avant qu'il
sache de quoi il s'agit ; le « de quoi ça parle » arrive en ~20 s au lieu de 5.

**Solutions.** (a) Statu quo. (b) **Étager** : hook nu d'abord, une phrase
factuelle (qui/quoi/où/combien), puis l'honnêteté épistémique juste en dessous, en
affirmation positive (« une évaluation argumentée selon un cadre assumé, pas un
label neutre »). (c) Supprimer la mise en garde du hero.

**Reco.** **(b)** — le hook frappe, une phrase factuelle suit, la nuance vient
ensuite (positive, pas en rétractation). Couper le lead de moitié.

---

# Vue d'ensemble — par où commencer

**Doubles gains** (une zone répétée *qui est aussi* mal formulée, risque faible) :
1.7 + 2.6 (triptyque), 1.8 (disclaimer), 2.1 (« décommodifiée »). **Risque nul,
effet immédiat** : 1.6 (grille repliée), 1.9 (fusion des chiffres), 1.13 (canon
nettoyé — à faire avant les renvois). **Faux amis** (traiter *autrement* que
l'intuition « couper ») : 2.2 (badge → clarifier sans tronquer), 1.2 (notices →
replier pour l'accessibilité, pas supprimer), 1.1 (aside → une phrase, pas coupe
sèche). **Structurant** : 1.5 (objet-verdict composite) commande 1.1, 1.3, 1.4.

