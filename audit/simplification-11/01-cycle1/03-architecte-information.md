# Cycle 1 — L'architecte d'information

*Voix : architecture d'information et charge cognitive. Je ne juge pas la
justesse doctrinale du contenu ; je juge l'**agencement** — combien de zones,
qui dit quoi, à quelle profondeur, et combien de fois la même chose est dite.*

Thèse de travail : sur la fiche-lieu, le **fond** n'est presque jamais le
problème. Le problème est le **nombre de zones de premier niveau** et la
**redite didactique** — la fiche explique sans cesse comment se lire elle-même.
La plupart des gains s'obtiennent par repli (résumé visible / détail en dépli),
par fusion de zones quasi-jumelles, et par hiérarchisation à deux profondeurs.
Mais je signale aussi les deux endroits où replier ne suffit pas : là, il faut
couper.

---

## 1. Carte des zones actuelles d'une fiche-lieu

Une fiche-lieu enchaîne aujourd'hui, en **première profondeur**, treize blocs
distincts. Pour chacun : profondeur idéale, et geste.

| # | Zone (classe) | Ce qu'elle porte | Prof. idéale | Geste |
|---|---|---|---|---|
| 1 | Fil d'Ariane (`crumb`) | navigation | 1 | garder |
| 2 | Entête + verdict + ctx-labs (`fiche-head`) | titre, badge verdict, porteur | 1 | garder |
| 3 | **Aside « Trois lectures »** (`verdict-cle`) | mode d'emploi verdict / Indice / palier | 2 | **replier (et déduppliquer)** |
| 4 | Lien dossier (`fiche-dossier-lien`) | renvoi récit | 1 | garder, fusionner avec 2 |
| 5 | **Panneau de score** (`score-panel`) | badge IdL + pentagone + 5 barres + échelle IdL + ghost + fiab + complétude + chaine-note + Repères | 1 (synthèse) / 2 (détail) | **fusionner en interne + replier le bas** |
| 6 | **Détails « Comment lire les visuels »** (`fiche-key`) | mode d'emploi badge/pentagone/barres/grille | 2 | **couper (redite de 3 et de la grille)** |
| 7 | Présentation (`prose`) | récit factuel | 1 | garder |
| 8 | Le montage (`enclair` + 3 `prose`) | mécanisme juridique | 1 (1 para) / 2 (détail) | **fusionner les 3 paras** |
| 9 | Analyse stratégique (synthèse + Forces/Fragilités/Leviers) | jugement | 1 | garder |
| 10 | Reliés dans l'annuaire (`chips`) | navigation latérale | 1 | garder |
| 11 | **Grille de lecture** (`grille-fold` : recap 5 barres + tableau ~21 lignes) | détail critère par critère | 2 | garder repliée, fusionner recap↔panneau |
| 12 | Fiabilité (`fiab-box`) | faits vérifiés / non confirmés | 2 | replier |
| 13 | Sources + backlink | références | 1 | garder |

**Le constat central.** Trois zones — l'aside « Trois lectures » (3), le détail
« Comment lire les visuels » (6) et le bas du panneau de score (5) — ne portent
**aucun fait propre au lieu** : ce sont des notices de lecture, répétées
identiquement sur les 45+ fiches. Elles occupent le haut de page, juste là où le
lecteur veut le verdict et le récit. C'est de la charge cognitive pure : on lit
trois fois « l'Indice retient l'axe le plus faible » avant d'arriver à ce que la
ferme *est*.

Le panneau de score (5) est lui-même un empilement de **sept instruments** dans
un seul bloc : badge chiffré, pentagone, cinq barres d'axe, échelle de paliers,
point « ghost » (indice brut), ligne fiabilité, ligne complétude, note de
chaîne, encart Repères. Le pentagone et les cinq barres disent **la même chose
deux fois** (profil visuel vs profil chiffré). Le badge, l'échelle et le ghost
disent **trois fois** la position de l'Indice (nombre, position sur l'axe, écart
brut↔pénalisé).

---

## 2. L'accueil

Ordre actuel : hero → chiffres-clés → teaser carte → vignettes dossiers →
« Par où entrer » (4 cartes) → état du corpus (histogramme) → modèles voisins
(5 cartes pleines). Sept zones de premier niveau.

Deux problèmes d'agencement, pas de fond.

**a) Deux blocs de chiffres redondants.** « Chiffres-clés » (45 / 4 / 0) et
« État du corpus » (histogramme des paliers + « 45 lieux, 23 porteurs, 42
usufruitiers ») disent tous deux la composition du corpus, à deux endroits
éloignés de la page. Ils doivent **fusionner** : un seul bloc « État du corpus »,
les trois grands nombres + l'histogramme côte à côte.

**b) Les modèles voisins en pleine carte, sur l'accueil.** Cinq `card`
complètes (badge + pentagone + sous-titre + méta juridique) pour des références
hors classement, *estimées*. C'est le bloc le plus lourd de la page pour
l'information la moins prioritaire pour un primo-visiteur. Geste : **réduire à un
teaser** (titre + lien « Voir les modèles voisins »), comme la carte est déjà un
teaser. Le détail vit déjà sur `modeles.html`.

Ce qui reste en première profondeur, intact : hero, teaser carte, vignettes
dossiers, « Par où entrer ». Rien à replier de plus — l'accueil doit rester
parcourable d'un trait. Le repli serait contre-productif ici (un primo-visiteur
ne clique pas pour déplier l'orientation).

---

## 3. Redondances inter-pages

Le même contenu didactique est servi sur **quatre surfaces** :

| Explication | Accueil | Méthode | Glossaire | Fiche |
|---|---|---|---|---|
| « libération des terres », définition | hero | §corpus (long) | entrée `g-liberation` | sub + lien |
| « l'Indice retient l'axe le plus faible » | — | §indice | — | aside (3) + fiche-key (6) + score-panel |
| verdict ≠ Indice ≠ palier | chiffres (lead) | §verdict | entrées dédiées | **aside (3), chaque fiche** |
| comment lire le pentagone / les barres | — | §indice (axe-cards) | — | **fiche-key (6), chaque fiche** |
| la chaîne et le maillon faible | — | §chaine | `g-chaine` | chaine-note + aside (3) |

**Où le dire une seule fois.** Le principe « une information dite une seule
fois, au bon endroit » désigne ici sans ambiguïté la **Méthode** comme foyer du
didactique, et le **Glossaire** comme foyer des définitions atomiques. La fiche
doit *montrer* le résultat et *renvoyer* (liens d'ancre `methode.html#indice`,
`#chaine`, `#verdict` — déjà présents !), pas ré-enseigner. Le renvoi existe
déjà ; ce qui manque, c'est d'**avoir le courage de supprimer la ré-explication
locale** une fois le lien posé. Concrètement :

- L'aside « Trois lectures » (3) : ne pas le mettre sur chaque fiche. Le
  contenu vit sur Méthode §verdict + §indice. Sur la fiche, un seul renvoi
  suffit (« Verdict, Indice et palier ne disent pas la même chose →
  Méthode »), placé sous le panneau, replié.
- Le détail « Comment lire les visuels » (6) : redondant à 100 % avec les
  axe-cards de Méthode §indice. À couper de la fiche.

Gain net : on retire de **chaque** fiche deux notices de plusieurs lignes,
soit, sur 45 fiches, l'élimination de ~90 répétitions du même paragraphe.

---

## 4. Fusions d'axes et d'instruments

**Verdict / palier / IdL — fusionner en un seul objet ?** Doctrinalement ils
diffèrent (ce n'est pas mon rayon de trancher), mais *visuellement* ils sont
aujourd'hui éclatés en trois zones : le badge verdict (entête), le badge IdL +
palier (panneau), l'échelle de paliers (panneau). Geste d'agencement : **un seul
« objet-verdict » composite** en tête de panneau — une ligne qui porte ensemble
le mot du verdict (hybride), le nombre (65) et le palier (Montage solide), avec
un lien unique « Pourquoi ces trois ? → Méthode ». On ne fusionne pas les
concepts ; on fusionne leur **zone d'affichage**. L'aside (3) devient alors
inutile : la distinction est portée par l'objet lui-même + un renvoi.

**Réduire les cinq axes affichés ?** Non — et c'est une coupe que je
*déconseille*. Les axes ne sont pas redondants entre eux (Méthode insiste : ils
sont indépendants, le profil est l'information). Mais **le pentagone et les cinq
barres sont la même donnée deux fois**. Garder le pentagone (lecture de forme,
immédiate) en première profondeur ; **replier les cinq barres chiffrées** dans
le même dépli que la grille (le chiffre exact est un détail de second niveau).
Le pentagone porte déjà les valeurs en `aria-label` et en sommets.

**Regrouper les co-gates / plafonds.** La `chaine-note` (« la structure ne peut
être notée plus haut que 40 ») et le `ghost` (indice brut avant pénalité) sont
deux annotations de plafond, dispersées dans le panneau. Les **regrouper en une
seule ligne** « Plafonds appliqués » sous le profil, repliable, qui dit d'un
trait : maillon limitant (axe 2 ≤ 40) + pénalité de complétude (67→65). Deux
mécanismes, une zone.

---

## 5. Repli vs coupe

**Cas où le repli suffit (le fond reste, on le range en profondeur 2).**

1. **Cinq barres chiffrées d'axe** — le pentagone tient la première profondeur ;
   les chiffres vont dans le dépli grille. Repli, pas coupe : un chercheur veut
   le chiffre exact.
2. **Encart « Plafonds appliqués »** (chaine-note + ghost + complétude
   fusionnés) — information vraie et utile, mais de second niveau. Replier sous
   le profil.
3. **Bloc Fiabilité** (`fiab-box`, faits vérifiés / non confirmés) — précieux
   pour un journaliste, secondaire pour un visiteur. Replier en `<details>`.
4. **Grille détaillée** (tableau 21 lignes) — *déjà* en `<details open>` ;
   passer à `<details>` fermé par défaut. La recap 5-barres en résumé visible
   suffit en profondeur 1.
5. **Bloc Sources** — garder visible mais en bas, c'est déjà le cas ; rien à
   couper, juste ne pas le remonter.
6. **« Trois lectures » → renvoi** : on ne coupe pas l'idée (elle vit sur
   Méthode), on remplace la notice par un lien — c'est un repli vers une autre
   page.

**Cas où il faut vraiment couper (le repli ne ferait que cacher un doublon).**

1. **Le détail « Comment lire les visuels » (`fiche-key`)** — c'est un doublon
   intégral des axe-cards de Méthode. Le replier reviendrait à conserver un
   tiroir qui ne contient rien d'unique. **Couper.** (C'est *le* geste de coupe
   que je défends sans réserve.)
2. **Les deux paragraphes redondants du « Montage »** — la fiche-lieu répète le
   mécanisme juridique en trois `prose` qui se recouvrent (silhouette générique,
   puis porteur↔usufruitier, puis re-narration). Le `enclair` + **un** paragraphe
   spécifique au lieu suffisent. Replier ne corrige pas une redite *intra-zone* :
   il faut **couper** les deux paras qui paraphrasent.
3. **Modèles voisins en cartes pleines sur l'accueil** — coupe vers teaser (le
   détail existe sur `modeles.html`). Replier 5 cartes serait un accordéon
   géant ; mieux vaut couper et renvoyer.

---

## 6. Maquette d'architecture cible

**Fiche-lieu, première profondeur (ce qu'on voit sans cliquer) :**

```
Fil d'Ariane
Entête : titre · badge-verdict · porteur · [lien dossier]
─ Objet-verdict composite : « Hybride · 65 · Montage solide »  → Méthode
─ Pentagone à 5 axes (forme)
─ Repères (localisation, année, type, intégrité, liens)
▸ Détail du score (déplié) : 5 barres chiffrées · plafonds · grille 21 lignes
▸ Fiabilité (déplié)
Présentation (récit)
Le montage (en clair + 1 para spécifique)
Analyse : synthèse + Forces / Fragilités / Leviers
Reliés dans l'annuaire
Sources
```

Cinq instruments deviennent un objet-verdict + un pentagone + un dépli. On
passe de **13 blocs de premier niveau à 9**, dont 2 sont des déplis. Les deux
notices didactiques disparaissent (renvoi Méthode).

**Accueil cible :**

```
Hero
État du corpus (3 nombres + histogramme, fusionnés)
Teaser carte
Vignettes dossiers
Par où entrer (4 cartes)
Modèles voisins (teaser → modeles.html)
```

De 7 zones à 6, la plus lourde (cartes modèles) ramenée à un teaser, les deux
blocs de chiffres unifiés. L'accueil reste **tout en première profondeur** :
ici, l'orientation ne se replie pas.
