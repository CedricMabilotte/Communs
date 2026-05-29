# Cycle 2 — voix méthodologue / gardien·ne de la cohérence (réaction)

*MARS-strat, refonte `nature_interet`. Lecture faite des trois autres voix du
cycle 1 et relecture de la mienne. Je reste sur mon créneau : faisabilité et
cohérence du système d'évaluation, jamais l'arbitrage politique ni juridique
fin. J'engage les cinq cruxes (T-a → T-e) sous l'angle « le système le
supporte-t-il sans casser L11, la source unique = la chaîne, et les
garde-fous ».*

---

## Là où j'amplifie

**Le théoricien a touché le vrai défaut, et il a raison contre moi sur un
point.** Sa §5 le dit froidement : mon principe (le juriste aussi) est
*relationnel* — un GAEC sur bail ≠ un GAEC propriétaire de son foncier —, or
l'axe `nature_interet` est porté *par l'entité isolée*. C'est exactement le
trou que mon cycle 1 n'avait pas vu : j'avais traité la frontière de tri
(§4 étape 1, « les associé·es détiennent-ils ou exploitent-ils le foncier ? »)
comme un **critère de saisie humaine** appliqué à la main au champ
`nature_interet` du maillon. C'est fragile : ça demande à l'opérateur de
re-juger le contexte chaîne à chaque saisie d'entité, alors que la même entité
(un GAEC) peut figurer dans deux chaînes opposées. Cela viole en esprit « une
seule source de vérité » : la donnée d'entité encoderait une information qui
appartient à l'articulation. Le théoricien a raison de pousser la lecture au
niveau de la chaîne.

**J'amplifie aussi le juriste sur le découplage forme ≠ cran.** Sa précaution
§4 (« le sigle ne suffit jamais à trancher ; classement par défaut
déplaçable ») rejoint ma ligne rouge n°1 du cycle 1 : la `forme_juridique` est
une *donnée d'entrée* qui informe, l'axe ne la duplique pas cran par cran.
Nous convergeons : pas un cran par sigle.

**J'amplifie l'éditorial sur le découplage label/calcul.** Sa §5 (réponse à
l'angle méthodo) est juste et me désarme à moitié : le lecteur de fiche ne voit
qu'**un** label (le sien) + le verdict de lieu (3 valeurs). Le gradient complet
n'est pas un objet d'affichage simultané. Donc mon argument « 7 crans = UI
illisible » (C3, point c) tombe en partie : l'illisibilité ne frappe pas le
lecteur, elle frappe **l'opérateur qui calibre**. C'est un déplacement
important — voir T-a.

---

## Là où je conteste

**Cinq crans classés « par marqueurs » (juriste §2-3) font exploser les
`inconnu`, et le juriste l'admet lui-même (§5 : "je le concède et je
l'assume").** De mon siège, c'est disqualifiant tel quel. Ses cinq marqueurs
(non-spéculation des parts, plafonnement du rendement, verrou d'actif,
gouvernance 1=1, agrément ESUS) ne sont *pas* dans les fiches : aucun champ ne
les porte aujourd'hui. Classer « par marqueurs » suppose donc soit cinq
nouveaux champs saisis par entité (cinq nouvelles sources de vérité à tenir, à
garde-fouder, à documenter — explosion de surface), soit un `inconnu` massif
tant que les statuts ne sont pas dépouillés. `inconnu` est un non-cran : plafond
`null`, bloque le sanctuaire, neutralise le verdict (`compute_verdict` l. 1308
renvoie `None`). Multiplier les `inconnu`, c'est rendre la majorité des fiches
**non-jugeables**. Le juriste préfère « un `inconnu` honnête qu'un
`commerciale` faux » — moralement défendable, mais à l'échelle d'un annuaire
c'est saborder l'outil. Je conteste donc les 5 crans-par-marqueurs comme
*architecture* ; je récupère les marqueurs comme *aide au classement par
défaut documentée*, pas comme schéma de données.

**Je conteste l'idée que deux crans intermédiaires (éditorial §4) soient
gratuits.** L'éditorial veut « Économie paysanne » ET « Lucrativité encadrée »
distincts. Or `commerciale_encadree` existe déjà. Donc l'éditorial demande en
réalité **un seul** cran neuf (l'économie paysanne) — ce qui rejoint ma
position. Là où il déborde, c'est en renommant tout le gradient (Hors-marché,
Société neutralisée, Marché ouvert…) : chaque renommage d'`id` interne est un
churn de migration sur toutes les fiches + tous les garde-fous qui testent ces
valeurs en dur (`compute_verdict` l. 1304-1306, `_NATURE_ORDRE_PIRE_AU_MIEUX`
l. 358, `verifier_chaines` l. 4913). Je distingue : **renommer le label public**
(prose, gratuit, n'engage pas la mécanique) vs **renommer l'`id`** (coûteux,
risqué, L2). Voir T-e.

---

## Ce que je n'avais pas vu — la chaîne porte déjà bail vs propriété (T-b)

J'ai relu le code, pas seulement `compute_verdict`. **L'information que le
théoricien réclame est déjà dans la donnée, et au bon endroit.** Les
articulations de chaîne (`montage.articulations[]`, lues l. 796-808) portent un
champ `titre` — vocabulaire `titres` de concepts.yml : « bail rural », « bail
emphytéotique », etc. (l. 524-532). Et `montage_section` détecte déjà le cas
**chaîne intégrée** (l. 816 : `set(porteurs) & set(usufruitiers)` — porteur et
usufruitier confondus, « propriété et usage non dissociés »). Autrement dit :
*la distinction « le GAEC détient » vs « le GAEC est preneur d'un bail » est
déjà encodée dans la chaîne du lieu*, via le titre de l'articulation et/ou
l'intersection porteur∩usufruitier. Je ne l'avais pas vu au cycle 1 — je
raisonnais maillon, alors que la réponse est articulation.

**Donc oui, on peut capturer le relationnel SANS casser L11 ni la source
unique.** Le couple proposé par le brief — (`nature_interet` du maillon ×
titre de l'articulation : bail vs propriété) — est calculable par le
générateur, et c'est même la *seule* voie propre. Mécanique :

- `nature_interet` du maillon reste la donnée d'entité (un GAEC est un GAEC,
  saisi une fois, stable) ;
- le titre `bail*` (ou l'absence d'intersection porteur∩usuf) est la donnée de
  relation, déjà saisie sur l'articulation ;
- le **générateur dérive** le cran effectif : un maillon société-civile-agricole
  *preneur d'un bail sur un foncier porté hors-marché* est lu « usage sans
  captation du fonds » ; le même maillon *propriétaire* (intégré, ou titre de
  propriété) reste au cran capital.

C'est exactement le schéma L11 : on n'ajoute aucun champ saisi, on **recâble une
table de dérivation** qui croise deux données déjà là. La source de vérité
reste la chaîne. Je révise donc ma position : **le bon levier n'est pas
seulement « ajouter un cran à `nature_interet` » (mon option A2), c'est faire
lire à `compute_verdict` et `_pire_nature_chaine` le couple (nature × titre
d'articulation).** Réserve de faisabilité, sérieuse : `_pire_nature_chaine`
(l. 364) et `compute_verdict` (l. 1290) itèrent aujourd'hui sur des maillons
*à plat* (`porteurs + usufruitiers`), sans regarder les articulations. Les
faire croiser nature×titre exige de leur passer la structure `montage` et de
gérer les chaînes où `articulations` est absent (dégradation gracieuse déjà
prévue l. 809-812 : « titre reste à documenter » → fallback prudent =
comportement actuel). C'est faisable, c'est ~15-25 lignes, mais ce n'est plus
« trois lignes ». Je corrige mon chiffrage du cycle 1 à la hausse.

---

## Les cinq cruxes, à froid

**T-a — combien de crans le système supporte-t-il vraiment ?** Recompte
honnête, en séparant les trois contraintes :
- *Table des plafonds* (`ax2_par_nature`) : la rampe actuelle 100/80/50/20/10 a
  un trou de 30 points entre 50 et 20. Elle absorbe **un** insert lisible (40),
  difficilement deux (50/40/30/20 → écarts de 10, le qualitatif s'efface).
- *UI lecteur* : non contraignante (éditorial §5 — un seul label visible). Je
  retire cet argument.
- *Calibrage opérateur + garde-fous* : c'est **là** qu'est le vrai plafond.
  Chaque cran neuf doit être inséré *simultanément* dans
  `_NATURE_ORDRE_PIRE_AU_MIEUX`, `ax2_par_nature`, `compute_verdict`, et la
  règle l. 4913 de `verifier_chaines` — sinon L14 immédiat (C2). Soutenable :
  **+1 cran** (6 effectifs), maximum absolu +2 (7). Le « par marqueurs » du
  juriste est implémentable *sans* exploser les `inconnu` **uniquement si** le
  classement par défaut reste piloté par `forme_juridique` (GAEC→agricole,
  SARL→commerciale) et que les marqueurs ne servent qu'à *déplacer* un cas
  documenté — pas à *exiger* cinq champs pour trancher. Sinon, `inconnu`
  explose. Verdict : 5 crans-données = non ; 1 cran-donnée + dérivation
  relationnelle (T-b) = oui.

**T-b — peut-on capturer le relationnel sans casser la source unique ni
L11 ?** Oui (cf. supra). Le couple (nature_interet × titre d'articulation)
calculé par le générateur **suffit** et c'est la seule voie cohérente. Condition
dure : la dérivation doit être *totale* (gérer le cas `articulations` absent par
un fallback = comportement actuel) pour ne pas créer de trou de calcul. C'est le
crux sur lequel j'ai le plus bougé.

**T-c — verdict 3 vs 4 niveaux.** Je tiens 3 (mapping), contre la demande d'un
4ᵉ verdict nommé. Chiffrage du coût d'un 4ᵉ : (a) 4ᵉ `degre` dans
concepts.yml (label, définition, couleur, classe CSS `.verdict-<id>`) →
modification de **rendu** → L9, aperçu HTML autonome obligatoire ; (b)
réouverture du couplage palier×verdict — `palier_for` (l. 336-345) et
`apply_palier_verdict_constraint` (l. 441) ne testent qu'une égalité
`verdict == req` ; un 4ᵉ verdict ne casse rien *mécaniquement*, mais ouvre la
question politique « un palier doit-il le requérir ? » ; (c) réécriture de toute
la prose triptyque (concepts.yml, ranking.yml, pages méthode/régimes/glossaire).
Trois postes pour zéro gain de calcul que le mapping 3-niveaux ne donne déjà.
**Position : 3 niveaux.** B n'est justifié que si l'éditorial démontre qu'un 4ᵉ
verdict *public nommé* est nécessaire — décision politique assumée, pas
contrainte technique.

**T-d — SCI/GFA (patrimonial) vs GAEC/EARL (travail) : combien de crans ?** Le
juriste sépare cran C (civile patrimoniale) de cran B (civile de travail). Du
point de vue données : la distinction patrimonial/travail recoupe largement la
distinction *détient/loue* déjà capturable par T-b (la SCI patrimoniale détient
le fonds ; le GAEC sur bail ne le détient pas). Je conteste donc qu'il faille un
**cran `nature_interet` distinct** pour SCI/GFA : le GFA/SCI **détenteur** tombe
déjà dans `commerciale` (cran capital) via la dérivation relationnelle ; le GFA
**citoyen à clause anti-spéculative** est un cas-frontière qui relève de
`commerciale_encadree` existant. Soutenable : **0 cran ajouté pour T-d** si on
laisse la chaîne (titre + détention) faire le tri. Ajouter `civile_patrimoniale`
ET `civile_agricole` ferait +2 crans (7 effectifs, plafond absolu) pour une
distinction que le relationnel porte déjà. Non soutenable comme deux crans-données.

**T-e — concéder les labels de l'éditorial ?** Du seul point de vue de
l'explicabilité-en-une-phrase (chantier A3) : **oui sur les labels publics,
non sur les `id`.** Renommer le *label affiché* « non lucrative » → « Hors-marché »,
ou nommer le nouveau cran « Économie paysanne » côté lecteur, est gratuit
(prose, ne touche aucune table, aucun garde-fou) et améliore l'explicabilité —
chaque label de l'éditorial tient en une phrase, c'est son métier et il l'a
prouvé (§3). Je concède donc les **labels**. Je refuse en revanche de répercuter
ces noms sur les `id` internes (`commerciale`, `commerciale_encadree`…) : ce
sont des clés testées en dur dans le code, leur renommage est un churn L2 à coût
non nul pour zéro gain de calcul. Règle de cohérence : *label public mobile,
`id` interne figé* (L2 + L32 — le slug public ne reprend pas un qualificatif
interne polémique, mais ici c'est l'inverse, on stabilise l'interne sous un
label public soigné).

---

## Ma position révisée

Le système supporte **un** cran `nature_interet` neuf (« exploitation/économie
paysanne »), inséré simultanément dans les trois tables + le garde-fou l. 4913,
plafond ax2 = 40. **Mais** le vrai correctif structurel n'est pas seulement ce
cran : c'est de faire lire au générateur le **couple (nature_interet du maillon
× titre de l'articulation)** — donnée déjà présente dans la chaîne (titres
`bail*`, intersection porteur∩usuf) —, ce qui capture le relationnel du
théoricien sans nouveau champ saisi, sans casser L11 ni la source unique.
Verdict reste à **3 niveaux** (mapping, pas de 4ᵉ). Pas de cran SCI/GFA
distinct : le relationnel les trie. Labels publics concédés à l'éditorial, `id`
internes figés. Le `inconnu` reste sacré et ne doit pas être gonflé par un
classement-par-marqueurs exigeant cinq champs absents.
