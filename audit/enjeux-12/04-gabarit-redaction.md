# Gabarit de rédaction d'une étude « Enjeux » — contrat de production

*Fait foi pour les agents chercheurs-rédacteurs et vérificateurs. À lire avec
`03-demarche-et-matrice.md` (démarche, règles de sources, matrice) — tout y est obligatoire.*

Date de référence : **10 octobre 2026**. Les données citées sont les plus récentes publiées à
cette date. Langue : français, typographie française (espaces insécables avant `: ; ? ! %`
inutiles en Markdown — écrire simplement « 43 % », « : »), écriture inclusive au point médian
comme le reste du site (paysan·nes, exploitant·es) sans excès.

## 1. Fichiers à produire

Racine : `/home/claude/Communs/enjeux/`

- `etudes/NN-slug.md` — l'étude (NN = numéro sur deux chiffres : `01`…`18`).
- `donnees/NN-xxx.csv` — une table par graphique (UTF-8, séparateur virgule, point décimal).
- `schemas/NN-xxx.svg` — un fichier par schéma fabriqué.

Ne crée **aucun** autre fichier, ne touche à rien d'autre dans le dépôt.

## 2. Front-matter YAML (exact)

```yaml
---
numero: 1
slug: a-qui-va-la-ferme          # = slug du nom de fichier sans le numéro
famille: transmettre              # transmettre | posseder | regle | usages | vivant | territoires | repondre
titre: "La ferme qui se libère va d'abord au voisin"      # affirmation
sous_titre: "À qui vont les fermes des agriculteurs qui partent ?"   # la question
chapeau: "60 à 100 mots : une scène type non identifiable, puis le mécanisme, puis ce que l'étude montre."
en_bref:                          # 4 ou 5 phrases, lisibles seules
  - "…"
chiffres_cles:                    # 3 à 5
  - valeur: "43 %"
    libelle: "des chef·fes d'exploitation ont 55 ans ou plus (2020)"
    source: "Agreste, recensement agricole 2020"
    url: "https://…"
signature: actitude.org
au: 2026-10-10                    # date de validité des données
created: 2026-10-10
updated: 2026-10-10
version: 1
statut: vivant
methode: documentaire             # pas d'enquête de terrain à ce stade
dimensions:                       # D1…D12 (voir matrice) : décisives = ●, les autres sont présentes
  decisives: [D1, D2, D3]
outils: [portage, fonciere_solidaire]   # outils de libération qui répondent (liste fermée, voir 03 §5)
corpus:                           # identifiants EXACTS de corpus-uids.md ; listes vides si rien
  lieux: [larzac]
  porteurs: [etat-larzac]
  usufruitiers: [sctl]
  modeles: []
  reseaux: []
  dossiers: [larzac]
  revues: []
liees: [02-qui-possede-la-terre]  # autres études (NN-slug) auxquelles celle-ci renvoie
concepts:                         # 3 à 8 termes de glossaire introduits ou mobilisés
  - terme: "Installation hors cadre familial"
    definition: "Une à deux phrases, sobres, sourcées si possible."
sources:                          # TOUTES les sources citées dans le texte, sans exception
  - id: agreste-ra2020-age
    type: officielle              # officielle | recherche | academique | presse | operateur | europe | droit
    auteur: "Agreste (SSP, ministère de l'Agriculture)"
    titre: "Recensement agricole 2020 — …"
    annee: 2022
    url: "https://…"
ouvrages:                         # 2 à 5 ouvrages de fond « pour aller plus loin » (existants, vérifiés)
  - auteur: "Bertrand Hervieu, François Purseigle"
    titre: "Une agriculture sans agriculteurs"
    annee: 2022
    editeur: "Presses de Sciences Po"
figures:
  - id: pyramide-ages
    type: barres                  # ligne | barres | barres_h | empilees | empilees_h | schema
    fichier: donnees/01-pyramide-ages.csv     # ou schemas/01-xxx.svg
    titre: "Une ferme sur deux sera à reprendre d'ici dix ans"   # le constat, pas « Évolution de… »
    unite: "%"                    # unité de l'axe des valeurs (vide pour schema)
    source: "Agreste, RA 2020"
    source_url: "https://…"
    alt: "Phrase qui énonce la conclusion du graphique, pour lecteur d'écran."
    note: "Champ, définition, rupture de série éventuelle (facultatif)."
retours_terrain: []
changelog:
  - date: 2026-10-10
    version: 1
    note: "Première version (analyse documentaire)."
---
```

## 3. Corps de l'étude (Markdown)

Ne pas répéter le titre, le chapô, « En bref » ni les chiffres clés (générés depuis le
front-matter). Le corps commence directement par la première section. Titres de niveau 2,
**dans cet ordre et avec ces intitulés** (le générateur s'y appuie) :

```
## Le constat
## Le mécanisme
## Ce que dit le droit
## L'histoire longue
## Ce qu'on sait, ce qu'on estime, ce qui se discute
## Ce que la libération change
## Leviers
### Pour les collectifs
### Pour les élu·es
### Pour les citoyen·nes
### Pour les cédant·es et propriétaires
## Question ouverte
```

- Dans « Ce qu'on sait… » : trois sous-titres de niveau 3 obligatoires — `### Ce qu'on sait`,
  `### Ce qui se discute`, `### Ce qui nous donnerait tort` (y dire aussi ce que l'outil
  public fait bien) — et un paragraphe **Ce que les chiffres officiels ne mesurent pas**.
- **Sources dans le texte** : chaque chiffre, chaque fait, chaque texte de loi porte un lien
  Markdown direct dans la phrase : `selon le [recensement agricole 2020](https://…)`. Toute
  URL du texte figure aussi dans `sources:` du front-matter.
- **Figures** : insérer un graphique ou un schéma par un paragraphe seul `[[figure:id]]`
  à l'endroit voulu. Viser **3 à 6 figures** par étude (au moins 2 graphiques de données et,
  quand le mécanisme s'y prête, 1 schéma). Chaque figure déclarée doit être insérée une fois.
- **Liens vers le corpus** : liens relatifs depuis la page d'étude
  (`/enjeux/NN-slug/index.html`, profondeur 2) : lieux `../../l/<uid>.html`, porteurs
  `../../p/<uid>.html`, usufruitiers `../../u/<uid>.html`, modèles `../../m/<uid>.html`,
  réseaux `../../r/<uid>.html`, dossiers `../../dossiers/<slug>.html`, revues
  `../../revues/<slug>/index.html`, autre étude `../NN-slug/index.html`, méthode
  `../../methode.html`, régimes `../../regimes.html`, glossaire `../../glossaire.html`.
  Pour un lieu ou un montage, lire sa fiche YAML dans le dépôt avant d'en parler : ne rien lui
  attribuer qui n'y figure pas, et dire sa limite (point de capture) quand la fiche la nomme.
- **Leviers** : 2 ou 3 par acteur, en liste. Chaque levier : l'outil qui existe, la démarche,
  un ordre de coût s'il y en a un, « avec un·e notaire / avocat·e » pour tout acte engageant,
  et si possible un lien vers une fiche du corpus qui l'a mis en œuvre. Jamais de lien vers
  une page de souscription ou d'investissement. Pas de conseil personnalisé.
- **Question ouverte** : un seul paragraphe d'une ou deux phrases.
- Longueur du corps : 2 500 à 4 500 mots (E06 : 1 500 à 2 500).
- Registre : phrases courtes ; **gras** sur le mot qui porte, avec parcimonie ; pas
  d'indignation ni de jargon managérial (écosystème, impact, résilience) ; retenue :
  chaque constat est signable par un·e chercheur·e cité·e ; le jugement n'apparaît que dans
  « Ce que la libération change » et les leviers.
- Pas de mention « généré par IA », pas de note de méthode sur la rédaction.

## 4. Données des graphiques (CSV)

- Première colonne = l'axe des catégories ou des années (en-tête parlant : `annee`,
  `departement`, `classe_age`…). Colonnes suivantes = une série chacune, en-tête = libellé
  affiché en légende (court, en français : `Exploitations`, `SAU moyenne (ha)`).
- Nombres sans espace ni symbole (`43.2`, pas `43,2 %`). Cellule vide = donnée absente.
- `ligne` : séries temporelles (première colonne numérique) ; `barres` : catégories en
  colonnes verticales ; `barres_h` : catégories longues ou classement (≤ 25 lignes) ;
  `empilees` / `empilees_h` : parts d'un total. Au plus 5 séries par graphique.
- **Chaque valeur provient de la source citée** (`source`, `source_url`) : ne jamais
  interpoler, extrapoler ni reconstituer de mémoire. Si une série n'est pas trouvable,
  pas de graphique — mieux vaut un schéma ou rien.

## 5. Schémas (SVG fabriqués)

- `viewBox="0 0 720 H"` (H entre 240 et 560), pas de `width`/`height` fixes, pas de script,
  pas d'image externe, pas de police déclarée (héritée).
- Élément racine : `<svg xmlns="http://www.w3.org/2000/svg" viewBox="…" role="img"
  aria-labelledby="t d">` avec `<title id="t">` et `<desc id="d">` (la conclusion).
- Couleurs **uniquement par classes** (le site les colore) : `s-box` (cadre neutre),
  `s-acc` (cadre accentué, terre cuite), `s-ok` (cadre vert : réponse / libération),
  `s-blue` (cadre bleu : régulation publique), `s-txt` (texte), `s-mut` (texte secondaire),
  `s-line` (trait), `s-arrow` (flèche ; définir dans `<defs>` un `<marker id="ah">` dont le
  chemin porte la classe `s-arrowhead`, et l'utiliser par `marker-end="url(#ah)"`).
- Texte ≥ 13 px, lignes courtes (≤ 28 caractères), aucun chevauchement. Flux de gauche à
  droite ou de haut en bas. Un schéma montre un mécanisme réel (chaîne d'acteurs, circuit de
  la valeur, procédure), pas une décoration.

## 6. Vérification préalable des sources (par toi, avant d'écrire)

- Ouvre (WebFetch) chaque URL que tu cites : elle doit exister et dire ce que tu lui fais
  dire. Préfère les pages pérennes (Légifrance, agreste.agriculture.gouv.fr, insee.fr,
  data.gouv.fr, publications INRAE, rapports parlementaires, Cour des comptes).
- Textes juridiques : vérifier l'état en vigueur au 10/10/2026 (version consolidée,
  décisions du Conseil constitutionnel, lois postérieures). **Aucune mention « à vérifier »
  dans le texte publié** : ce qui n'est pas vérifié est retiré.
- Exclues comme sources : ONG et associations militantes françaises (Terre de Liens,
  Confédération paysanne, FNH, Agter, Générations futures, FNE, Les Amis de la Terre,
  Greenpeace France, Attac, Foodwatch…). Elles peuvent être nommées comme acteurs.
  Domaines interdits dans `sources:` : terredeliens.org, confederationpaysanne.fr, fnh.org,
  agter.org, generations-futures.fr, fne.asso.fr, amisdelaterre.org, greenpeace.fr,
  attac.org, foodwatch.org, wikipedia.org.
- La presse d'enquête est source de faits, jamais seule source d'un chiffre.
- Nommage : personnes morales d'envergure seulement, sur décision de justice, registre,
  document de l'entité, rapport public ou enquête signée ; aucune intention imputée ; pas de
  petite société d'exploitation nommée ; jamais de personne physique privée (les élu·es et
  responsables publics peuvent être nommés dans l'exercice de leurs fonctions, sur source).
