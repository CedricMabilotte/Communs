# Revue de clôture #10 — synthèse arbitrée

*Session #10, 29 mai 2026. Audit MARS-strat du site publié après Phase B. Cycle 1 :
4 voix (visiteur froid · architecte info · directeur éditorial · stratège
attractivité). Pas de cycle 2 séparé : **chaque voix a rédigé ses « désaccords
prévus » en répondant aux autres** — le contradictoire est déjà au dossier, la
synthèse suit. Livrable : critique + plan concret ; l'implémentation est une passe
ultérieure. Convention : « les voix » = traçable ; « **orchestrateur** » = à valider.*

---

## 1. Constats partagés (convergences fortes → corrections non négociables)

1. **L'accroche d'ouverture est forte mais sabotée aussitôt.** « La terre n'est
   pas une marchandise » happe (stratège, visiteur) ; mais le hero enchaîne en
   trois lignes sur « non lucrative et décommodifiée… défendable et contestable » —
   une clause de non-responsabilité avant d'avoir donné envie. *Le cri se referme
   en avertissement.*
2. **Les Dossiers sont enterrés — diagnostic le plus coûteux.** Cinq récits signés,
   aux titres qui vendent : **zéro présence sur l'accueil**, un onglet plat. Le
   meilleur hameçon du site est invisible depuis la porte (architecte, stratège,
   visiteur).
3. **La Carte est à demi-enterrée.** Promise par un bouton, **jamais montrée** sur
   la home ; page nue, sans filtre ni lien vers un récit. Réflexe n°1 d'un annuaire
   géographique, sous-exploité.
4. **Le hub Annuaire est un sas, pas une porte.** Sept cartes grises de même poids
   mêlant « 45 lieux » et « 8 réseaux », libellés d'initié (« porteurs de
   nue-propriété », « usufruitiers ») ; un clic de plus pour « juste voir les
   lieux » (visiteur, architecte, stratège).
5. **Le textuel garde une couche « interne » tenace** que D1 n'a pas atteinte : le
   *vocabulaire du modèle* exposé tel quel. Pire offenseur : **« co-gate »**
   (anglicisme jamais défini, dans chaque info-bulle de verdict). Puis : identifiants
   de critères et chemin `ranking.yml` affichés au public, « proxy unidirectionnel »
   + « marchandise fictive de Polanyi » dans une case de grille, « verdict » et ses
   degrés jamais introduits, « cadre explicite et contestable » répété en tic.
6. **Le footer ré-importe la complexité retirée du haut** (20 liens). Symptôme : on
   a *déplacé* le surplus, pas *décidé* une hiérarchie.

---

## 2. Livrable A — hygiène du textuel interne (reformulations)

**Trois règles de registre** (à ériger en garde-fou éditorial, comme L9 pour le visuel) :
1. **Pas de code dans la prose.** Aucun identifiant de critère, nom de champ ou
   chemin de fichier (`ranking.yml`) sur une page publique : le générateur rend
   toujours le *libellé humain*, jamais la clé.
2. **Introduire avant d'employer.** Tout terme-maison (verdict, chaîne, plafond,
   intrinsèque/effectif) est glosé en une ligne la première fois qu'il paraît sur
   une page de parcours, ou lié à une entrée de glossaire vivante. Modèle réussi :
   usus/fructus/abusus.
3. **Une honnêteté épistémique, dite une fois, en mots de tout le monde.**

**Tableau de reformulations** (page → actuel → proposition Eozen) — prioritaire :

| Page | Actuel | Proposition |
|---|---|---|
| méthode, fiches, dossiers (info-bulles) | « **co-gate** / co-gaté / les co-gates du sommet » | « condition (du sommet) / plusieurs conditions à la fois » |
| grilles — *Travail non marchandisé* | « Lecture par **proxy UNIDIRECTIONNEL**, jamais déduite de la forme » | « On ne le déduit jamais de la forme juridique : on regarde le travail réel qui fait vivre le lieu » |
| grilles — *Travail non marchandisé* | « Co-gate du sommet : il teste la décommodification du travail (3ᵉ marchandise fictive de Polanyi) » | « L'une des conditions du sommet : que le travail qui fait vivre le lieu ne soit pas vendu comme une marchandise » |
| grilles — *Aucun maillon commercial* | « tous les maillons sont `non_lucrative`… (voir `plafonds_chaine.ax2_par_nature` dans `ranking.yml`) » | « tous les maillons sont non lucratifs… La note de cet axe ne peut dépasser ce que permet le maillon le plus faible. » *(retirer identifiants + chemin)* |
| méthode §verdict | « le verdict comme l'Indice sont un **indicateur composite conventionnel** » | « le verdict comme l'Indice sont une **lecture argumentée**, pas une mesure objective » |
| méthode §verdict | « il se **calcule** à partir de la nature de chaque maillon » | « il **découle** de la nature de chaque maillon de la chaîne » |
| méthode §chaîne | « réalisée par le critère `milieu_protege` logé dans la grille » | « jugée sur la protection effective du milieu, au niveau du lieu » |
| méthode §chaîne | « indice **intrinsèque** / **effectif** » | « note **propre** / note **replacée dans ses chaînes** » |
| méthode, accueil | « agrégation **non compensatoire** » / « axes **orthogonaux** » | « la note retient l'axe le plus faible : une force ne rachète pas une faiblesse » / « axes **indépendants** » |
| fiche — encart chaîne | « Axe 2 plafonné à 40 par la chaîne… (score intrinsèque : 100) » | « La structure ne peut être notée plus haut que 40 : un maillon de la chaîne — une société d'exploitation agricole — l'en empêche, quels que soient les critères cochés. » |
| accueil §chiffres | « 0 — au sommet décommodifié — le sanctuaire reste un horizon » | « 0 — **aucune libération pleinement aboutie** : le sommet reste un horizon » |
| accueil §chiffres | « 4 — fausses libérations démasquées (montages **marchands**) » | « 4 — fausses libérations démasquées (la terre y reste captable par le marché) » |
| dossiers, fiches | « Verdict **à établir** » | « Verdict **suspendu** / pas encore tranché » |
| footer (toutes pages) | formule « cadre explicite et contestable » répétée | une seule formule canonique au footer ; variée ou sous-entendue ailleurs |

**Deux entrées de glossaire à créer** : **verdict** et **co-gate→condition** (les
deux termes les plus exposés et non définis). Et **introduire « verdict »** d'une
ligne dès l'accueil (un mot fort, gardé — mais présenté).

Source des chaînes : `config/concepts.yml` (degrés), `config/grilles.yml`
(définitions), `scripts/generate_site.py` (prose des render_*).

## 3. Livrable B — navigation plus attractive

**Principe : la nav ne doit pas seulement lister, elle doit montrer et hiérarchiser.**

- **Barre — garder 5, hiérarchiser :** `Carte · Dossiers · Annuaire | Méthode`
  (destinations désirables d'abord, hub ensuite, séparateur, référence allégée en
  fin). L'ordre raconte un parcours : *je regarde → je lis → je creuse → je
  vérifie*. Implémentation : réordonner `NAV` + classe `nav-ref` sur Méthode.
- **Accueil — donner à voir, pas promettre :**
  1. **Bandeau Dossiers : 3 récits en vignettes** (titre + sous-titre accrocheurs),
     sous « À lire — les récits ». *La correction la plus rentable de tout l'audit.*
  2. **Mini-carte montrée** (Leaflet réduit ~280 px France, ou SVG semé de points
     colorés en repli) avec « Explorer la carte → ». Le visiteur *voit* avant de cliquer.
  3. **Garder les 4 intent-cards** (« Par où entrer »), déplacées *sous* carte+récits.
- **Hub Annuaire — page-action :** un bloc « **Commencer ici** » dominant (Carte /
  Liste « 45 lieux » / Classement) ; les acteurs (porteurs/usufruitiers/réseaux/
  modèles) **repliés sous `<details>`** — rien n'est supprimé, tout est hiérarchisé.
  Retirer la carte de la grille des 7 (elle a déjà son onglet).
- **Footer — par intention :** 3 colonnes nommées (Découvrir / Explorer / Citer) au
  lieu de 2 groupes-inventaire ; reléguer data.json/changelog en « Ressources » discret.
- **Mobile :** baseline masquée < 480 px ; tester barre 5 entrées + logo (wrap ou
  burger) ; `scrollWheelZoom` au focus conservé ; vignettes en 1 colonne, titres non tronqués.
- **Cohérence de nommage :** trancher entre « Terres Libérées », « Annuaire », « La
  terre n'est pas une marchandise » (3 noms pour la même chose désorientent) ;
  unifier « Carte » / « Sur la carte ».

## 4. Tensions à arbitrer (opérateur)

- **T1 — « 0 au sommet » : hook signature, ou risque ?** Le stratège veut en faire
  le *pitch* partageable / angle presse (un annuaire des terres libérées où aucune
  ne l'est pleinement — paradoxe fort). C'est honnête et puissant, mais double
  tranchant (peut se lire « le projet échoue »). *Position orchestrateur* : en faire
  une accroche assumée **en prose** (pas un chiffre froid), cohérent avec la posture
  d'étoile polaire — mais c'est ta décision éditoriale/politique.
- **T2 — densité documentaire vs lisibilité de l'aiguillage.** Le gardien du registre
  tient au « tout à barème égal » (les 7 catalogues, footer exhaustif) ; l'architecte
  répond *« barème égal dans la donnée n'oblige pas à poids égal dans la nav »*.
  *Position orchestrateur* : suivre l'architecte — hiérarchiser la nav ne dévalue pas
  les réseaux, les replier les garde accessibles. À confirmer.
- **T3 — sobriété vs spectaculaire :** montrer carte+récits, mais **pas** de
  carrousel auto ni de carte plein écran (accessibilité, mobile). Réglé par le
  compromis « montrer puis céder la place » (architecte). Pas d'arbitrage requis.

## 5. Plan priorisé (coût × impact)

1. **Quick win éditorial** — supprimer « co-gate », « proxy unidirectionnel », les
   identifiants `code` + `ranking.yml`, varier la formule épistémique : ~1 lot
   générateur/config, fort impact registre, zéro risque. *À faire en premier.*
2. **Dossiers + mini-carte sur l'accueil** — le hook le plus rentable : sections
   dans `render_index`. Impact d'attractivité maximal.
3. **Hub Annuaire en page-action** + barre réordonnée + footer par intention.
4. **Glossaire** : entrées verdict/condition + introduction de « verdict » à l'accueil.
5. **Mobile** : passe de vérification dédiée (aperçu L9 à 380 px).

Tout est implémentable en statique (réordonner `NAV`, sections de contenu,
`<details>`, Leaflet déjà présent) — pas d'usine à gaz.
