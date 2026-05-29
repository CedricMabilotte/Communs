# Cycle 1 — Voix : Architecte d'information

*Mini-strat Phase B, session #10. Voix isolée. Critère propre : navigabilité,
information scent, orientation des trois usagers-mental (journaliste pressé·e,
chercheur·euse, citoyen·ne en exploration). Je ne tranche pas le fond, ne
re-spécifie pas le moteur, ne rédige pas de contenu éditorial.*

---

## 1. Diagnostic — ce qui désoriente aujourd'hui

L'architecture actuelle souffre d'une **confusion de niveaux** : tout est au
même plan, et la navigation principale mélange trois logiques incompatibles.

**a) La barre de nav porte huit entrées hétérogènes.** *Accueil · Lieux ·
Porteurs · Usufruitiers · Réseaux · Revues · Classement · Méthode.* On y trouve
côte à côte : des **types d'objet** du modèle (Lieux, Porteurs, Usufruitiers —
les trois catégories notées), une **vue transverse** (Classement), une **brique
documentaire** (Méthode), une **annexe** (Revues), un **regroupement** (Réseaux).
Le visiteur doit comprendre le modèle de données avant de savoir où cliquer.
« Porteurs » et « Usufruitiers » sont des concepts internes : un·e citoyen·ne ne
sait pas qu'il/elle cherche un « usufruitier ». L'information scent est faible —
les libellés décrivent la structure interne, pas les intentions de l'usager.

**b) Trois catalogues parallèles, symétriques mais cloisonnés.** Lieux,
Porteurs, Usufruitiers sont trois listes filtrables au traitement identique.
C'est cohérent côté modèle, mais le **lieu** est l'unité concrète que cherchent
les trois usagers — les porteurs et usufruitiers sont des facettes du même
montage. Mettre les trois sur le même rang de nav fait porter à l'usager une
distinction qui devrait être un *filtre*, pas une *destination*.

**c) L'accueil énumère sans orienter.** Hero → « Comment lire » (3 étapes) →
cartes de catégories → histogramme → « En tête du classement » (cards) →
modèles voisins. C'est une **vitrine de tout le contenu**, pas une **table
d'orientation**. Le bloc « En tête du classement » hiérarchise implicitement
(les mieux notés en avant) alors que le projet revendique un catalogue
symétrique — contradiction non assumée, signalée déjà en B4. Aucun parcours
n'est tracé pour les trois usagers : ils débarquent dans la même soupe.

**d) La fiche empile sans seuiller.** La fiche Pommiers est riche mais
**plate** : head + verdict → score-panel (badge + pentagone + 5 barres + échelle
+ note de plafond de chaîne) → `<details>` « comment lire » → Présentation →
Le montage → Analyse (forces/fragilités/leviers) → Reliés → Grille (récap +
table de ~20 critères) → Fiabilité → Sources. Tout est de même poids visuel.
Le journaliste pressé doit traverser le score-panel technique pour atteindre la
synthèse en prose ; le chercheur doit scroller longtemps pour trouver la grille
et les sources. **Rien ne distingue le résumé citable du détail auditables.**
La contradiction verdict/Indice/palier (A3) est reléguée dans un `<details>`
replié que « peu de lecteur·rices déploieront ».

**e) Le magazine n'existe pas encore** (B2 en P2) : il n'y a aujourd'hui que le
catalogue. La question est donc de lui faire une place *sans* casser la symétrie
du catalogue.

---

## 2. Les trois niveaux de lecture et leur articulation

Je propose de **réorganiser la nav autour des intentions**, pas des objets, et
de poser une règle d'or : **le magazine hiérarchise, le catalogue ne hiérarchise
pas, et la fiche les réconcilie**. Les trois niveaux ne se contredisent pas s'ils
ont chacun un *contrat de lecture* explicite et affiché.

### Niveau A — Le magazine (éditorialisé, hiérarchisant) — porte d'entrée

Contrat de lecture : *« Voici par où entrer, voici ce qui compte, voici des
récits. »* C'est l'**accueil refondu + les dossiers (B2)**. Il assume de
hiérarchiser, de mettre en avant, de raconter. C'est la couche de l'**attention**
et de l'**hospitalité** : le citoyen·ne explore, le journaliste trouve un hook.

- **Accueil = table d'orientation**, pas vitrine. Above the fold : manifeste
  court + 3 chiffres-clés + une **carte de France** (B1) comme premier visuel.
  En-dessous : 4 entrées *par intention* — « Je découvre », « Je cherche un
  lieu », « Je veux la méthode », « Je suis chercheur·euse » (cf. B4).
- **Dossiers** (`/dossiers/`) : récits longs sur cas-pivot. Hiérarchisation
  **assumée et signalée** : « sélection éditoriale » l'étiquette. Chaque dossier
  pointe vers la/les fiche(s)-catalogue concernée(s).

### Niveau B — Le catalogue (symétrique, exhaustif) — la référence

Contrat de lecture : *« Toutes les fiches, même traitement, à vous de filtrer et
trier. »* C'est la couche de la **rigueur** et de la **complétude** : le
chercheur creuse, le journaliste vérifie qu'un lieu y est ou non.

- **Une seule destination de catalogue dans la nav : « Annuaire ».** Les trois
  catégories (Lieux / Porteurs / Usufruitiers) deviennent un **filtre de type en
  tête de l'annuaire**, le défaut affiché étant **Lieux** (l'unité concrète).
  On garde les trois listes en pages, mais elles cessent d'être des entrées de
  nav de premier rang : elles sont des onglets/filtres d'une même section.
- **Classement** et **Carte** sont des **vues** du même catalogue, pas des
  sections rivales : un sélecteur de vue (Liste / Carte / Classement) en tête de
  l'annuaire. Le classement *trie* (ne hiérarchise pas éditorialement : il
  ordonne par un critère explicite, déclaré) ; la carte *géolocalise*. Symétrie
  préservée : chaque fiche a exactement un marqueur, une ligne, une carte.

### Niveau C — La fiche (le point de réconciliation)

Contrat de lecture : *« Un montage, lu à deux profondeurs : un résumé citable
en haut, l'audit complet en bas. »* C'est là que magazine et catalogue se
rejoignent : la fiche porte à la fois le **récit court** (lien vers le dossier
si existant) et la **grille auditable**. Détail en §3.

### Le fil qui relie les trois sans les contredire

- **Du magazine vers la fiche** : tout récit/mise en avant pointe vers la fiche
  symétrique. Le magazine *dit* « regardez celui-ci » ; la fiche *montre* « voici
  comment il se situe, au même barème que tous les autres ».
- **De la fiche vers le catalogue** : backlinks « ← Annuaire » + « voir sur la
  carte » + « comparer ».
- **Étiquetage explicite du contrat** : chaque niveau affiche en clair s'il
  hiérarchise (« sélection éditoriale ») ou non (« tous, à barème égal »). La
  contradiction perçue catalogue/magazine **disparaît dès qu'elle est nommée** :
  le lecteur sait quand il lit un choix et quand il lit une liste neutre.

---

## 3. Le gabarit de fiche refondu

Principe directeur : **deux profondeurs, une ligne de flottaison nette.**
Au-dessus, le *résumé citable* (journaliste, citoyen) ; en-dessous, l'*audit*
(chercheur). Chaque bloc déclare à qui il parle.

### Au-dessus de la ligne de flottaison (premier écran, mobile inclus)

1. **Fil d'Ariane** (Accueil › Annuaire › nom).
2. **En-tête identité** : type (Lieu), nom, sous-titre incarné d'une ligne,
   localisation, porteur en label contextuel.
3. **Bandeau de lecture A3 — déplié, pas en `<details>`.** *Le bloc qui
   réconcilie les trois chiffres.* Verdict + Indice + palier sur une ligne, avec
   une phrase de 1 ligne : « ces trois chiffres ne disent pas la même chose →
   comment lire ». C'est la correction structurelle d'A3 : la mécanique
   contradictoire doit être visible **au-dessus** du score, jamais repliée.
4. **Synthèse en prose (3-4 phrases) + repères.** Le *fait citable* : ce qui se
   joue ici. C'est ce que le journaliste copie. Doit tenir sans avoir lu la
   grille.
5. **Lien dossier** si un récit existe (« Lire le récit → »).

### En-dessous de la ligne de flottaison (l'audit, scroll assumé)

6. **Profil visuel** : pentagone + 5 barres d'axe + échelle de palier + note de
   plafond de chaîne. (Aujourd'hui en haut ; je le **descends** sous la synthèse
   — le visuel technique n'est pas la première chose qu'un non-initié doit
   affronter.)
7. **Présentation** (factuel) et **Le montage** (juridique, voix exacte +
   en-clair).
8. **Analyse stratégique** : forces / fragilités / leviers (conservé).
9. **Reliés dans l'annuaire** : chips porteurs/usufruitiers.
10. **Grille de lecture détaillée** : récap par axe + table des critères.
    *Repliable par défaut sur mobile* (le récap reste visible, la table
    s'ouvre).
11. **Fiabilité** + **Sources** (dont sources tierces, B3).
12. **Backlinks** : Annuaire · Carte · Comparer.

### Mobile

- Le bandeau A3 et la synthèse doivent tenir **dans le premier écran mobile** ;
  le pentagone et la table passent **dessous**.
- La table de grille : conserver le `table-scroll` horizontal déjà présent, mais
  ne jamais l'imposer au-dessus de la ligne de flottaison.
- Pentagone : taille réduite, jamais en compétition de hauteur avec la synthèse.

---

## 4. Éléments constitutifs apportés (pour la synthèse)

### Schéma de navigation cible

```
Nav primaire (intentions, 4-5 entrées max) :
  Accueil  ·  Annuaire  ·  Dossiers  ·  Méthode  ·  [Glossaire]

Annuaire (une section, plusieurs vues + filtres) :
  ├─ Vue : Liste | Carte | Classement
  ├─ Filtre Type : Lieux (défaut) | Porteurs | Usufruitiers
  └─ Filtres : palier, montage, région…   (existants, conservés)

Magazine :
  Accueil (table d'orientation) + Dossiers (récits, sélection assumée)

Secondaire / pied de page (annexes, hors nav primaire) :
  Réseaux · Revues · Modèles voisins · Comparer · Régimes · Grilles ·
  Données ouvertes · Proposer un lieu · Changelog
```

### Liste ordonnée des blocs de fiche (contrat par bloc)

| # | Bloc | Usager visé | Ligne flott. |
|---|------|-------------|--------------|
| 1 | Fil d'Ariane | tous | au-dessus |
| 2 | En-tête identité | tous | au-dessus |
| 3 | Bandeau lecture A3 (déplié) | citoyen, journaliste | au-dessus |
| 4 | Synthèse prose + repères | journaliste | au-dessus |
| 5 | Lien dossier | citoyen | au-dessus |
| 6 | Profil visuel (pentagone, axes, plafond) | chercheur | en-dessous |
| 7 | Présentation / Montage | tous | en-dessous |
| 8 | Analyse (forces/fragilités/leviers) | chercheur, militant | en-dessous |
| 9 | Reliés | chercheur | en-dessous |
| 10 | Grille détaillée (repliable mobile) | chercheur | en-dessous |
| 11 | Fiabilité + Sources | chercheur, journaliste | en-dessous |
| 12 | Backlinks | tous | bas |

### Patterns réutilisables

- **Contrat de lecture affiché** : chaque section/vue déclare « sélection
  éditoriale » (hiérarchise) ou « tous, à barème égal » (symétrique). Pattern
  anti-contradiction transposable partout.
- **Vue ≠ section** : Liste/Carte/Classement sont des vues d'un même jeu, pas
  des pages rivales. Évite la prolifération de la nav.
- **Type = filtre, pas destination** : les catégories du modèle deviennent des
  filtres ; seules les *intentions* sont des destinations de nav.
- **Deux profondeurs, une ligne de flottaison** : résumé citable au-dessus,
  audit en-dessous. Transposable à toutes les fiches (lieux/porteurs/usuf.).
- **Information scent par l'intention** : libellés de nav = ce que l'usager veut
  faire, pas ce que le contenu est.

---

## 5. Désaccords prévus avec d'autres voix

- **vs Éditeur·rice magazine (densité vs accroche).** Je refuse que l'accueil
  redevienne une vitrine de cards. L'éditeur voudra probablement remettre des
  lieux mis en avant en page d'accueil ; je tiens que l'accueil doit d'abord
  *orienter* (table d'intentions), la mise en avant restant cantonnée aux
  Dossiers, étiquetée « sélection ». Tension réelle sur l'above-the-fold.

- **vs Lecteur·rice cible (presse/décideur) — prise assumée vs sobriété
  citable.** Je place le bandeau A3 (verdict + mécanique contradictoire) **en
  haut de fiche, déplié**. Le lecteur-presse pourrait préférer un score net,
  copiable sans nuance. Je tiens que la contradiction verdict/Indice/palier doit
  être visible *avant* le chiffre, au risque de moins de « punch » citable —
  c'est le prix de l'honnêteté de lecture.

- **vs symétrie revendiquée (catalogue) vs hiérarchie (classement/carte
  colorée).** Je résous par l'étiquetage de contrat, mais le débat sur les
  **couleurs de marqueurs** (par verdict ? par palier ? neutre ? — décision B1)
  est un point où l'architecte (lisibilité du scent) et le gardien de la rigueur
  (ne pas pré-juger) peuvent diverger : je penche pour un codage couleur *lisible
  mais déclaré comme convention*, pas neutre.

- **vs Méthodologue (gate dur vs glose).** Hors de mon volet, mais si un co-gate
  devient « dur » (bloque le sommet), la fiche devra **rendre lisible un blocage**
  (pourquoi ce lieu ne peut atteindre le sommet) — un besoin d'information
  supplémentaire dans le bandeau A3. Je signale la dépendance : toute décision de
  strictness a un coût de lisibilité que la fiche devra absorber.

---

*Fin du document — voix Architecte d'information, cycle 1.*
