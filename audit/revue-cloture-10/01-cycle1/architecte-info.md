# Voix — Architecte d'information / UX

*Cycle 1 MARS-strat, revue de clôture #10. Audit de la navigation publiée de
« Terres Libérées » (communs.actitude.org). Critère : clarté, orientation,
cohérence des parcours, attractivité structurelle. Isolée.*

---

## Résumé (< 150 mots)

**Verdict sur la nav actuelle : réduite, pas attractive.** Le passage à 5 entrées
a assaini la barre, mais l'a aussi appauvrie : la Carte et les Dossiers — les deux
réflexes d'entrée du visiteur — sont rangés en onglets neutres de même poids que
le reste, et le hub Annuaire est un **sas administratif** (deux rangées de cartes
grises) plutôt qu'une porte désirable. Mes trois propositions phares :

1. **Faire de la Carte et des Dossiers des entrées visuelles dès l'accueil**
   (vignettes-récits + mini-carte cliquable), pas seulement des onglets.
2. **Transformer le hub Annuaire en page-action** : un bloc « commencer ici »
   (carte / liste / classement) dominant, les acteurs repliés dessous.
3. **Trois parcours-types nommés** (Découvrir · Explorer · Citer) qui structurent
   l'accueil et le footer, au lieu d'un inventaire de 20 liens en pied de page.

---

## 1. Diagnostic de la nav actuelle

**Ce qui oriente bien.** La barre à 5 entrées (Accueil · Annuaire · Carte ·
Dossiers · Méthode) est lisible, tient sur une ligne, et la logique « un onglet
Annuaire qui s'allume pour toutes les pages-catalogue » (`ANNUAIRE_PAGES` dans le
générateur) est saine : le visiteur ne se perd pas entre `lieux.html`,
`porteurs.html`, `classement.html` — il sait qu'il est « dans l'Annuaire ». Le fil
d'Ariane des fiches (`Accueil › Lieu › Nom`) est correct. Les cross-liens en bas
de page (« Le catalogue des lieux → ») rattrapent les sorties. L'accueil offre
quatre `intent-cards` (« Je découvre / Je cherche un lieu / Je veux la méthode /
Je suis chercheur·euse ») — c'est la **meilleure pièce d'orientation du site**.

**Ce qui reste austère ou administratif.** Trois problèmes structurels :

- **La barre est plate.** Les 5 entrées ont strictement le même poids visuel.
  Or elles ne se valent pas : Carte et Dossiers sont des *destinations* (on y va
  pour voir/lire), Annuaire est un *hub* (on y transite), Méthode est une
  *référence* (on y revient). Une nav qui ne hiérarchise rien force le visiteur
  à tout évaluer à la même aune. C'est *réduit*, pas *orientant*.

- **Le hub Annuaire est un sas, pas une porte.** `render_annuaire` produit deux
  sections de `cat-card` — « Parcourir les lieux » (liste/carte/classement) puis
  « Les acteurs et les repères » (porteurs/usufruitiers/réseaux/modèles) — soit
  **sept cartes grises équivalentes**. Le visiteur arrive sur une grille de choix
  sans dominante : rien ne dit « commence par la carte ». Pire, la carte est ici
  réduite à *une carte parmi sept*, alors qu'elle a son propre onglet juste à
  côté dans la barre — redondance qui dilue. Et les sept cartes mélangent deux
  registres très inégaux : « 45 lieux » (ce que tout le monde veut) et « 8
  réseaux » (ce qui n'intéresse qu'un chercheur). Tout au même niveau = aucune
  priorité lisible.

- **Le footer est un inventaire, pas une carte du site.** Deux groupes
  (« Annuaire » : 8 liens · « Lire & comprendre » : 12 liens) = **20 liens en
  pied de page**, dont des pages que la nav principale a justement voulu cacher
  (themes, comparer, grilles, regimes, suggerer, changelog, data.json). Le footer
  ré-expose toute la complexité qu'on a retirée du haut. Ce n'est pas un défaut
  d'orientation grave (un footer dense est toléré), mais c'est le symptôme : on
  n'a pas *décidé* d'une hiérarchie, on a *déplacé* le surplus vers le bas.

**Textuel qui nuit à l'orientation** (signalé, hors mon cœur de mission) : le
titre du hub est « Annuaire » et l'accueil l'appelle aussi « Annuaire » dans la
barre — mais le H1 de l'accueil est « La terre n'est pas une marchandise » et le
nom du site est « Terres Libérées ». Trois noms pour une même chose désorientent.
Et le label de carte « Sur la carte » vs l'onglet « Carte » : deux libellés pour
la même destination.

---

## 2. Le sort des nouveautés : Carte, Dossiers, hub

**La Carte — sous-exploitée.** Elle est *le réflexe n°1* d'un visiteur d'annuaire
géographique. Or :
- À l'accueil, elle n'apparaît **que** comme bouton CTA (« Voir la carte ») et
  comme lien dans une intent-card. **Aucune carte n'est montrée** sur la home : on
  promet une carte, on ne la donne pas. Un visiteur qui « pense carte » doit
  cliquer pour découvrir qu'il y en a une.
- Sur `carte.html` elle-même, le rendu est correct (Leaflet, marqueurs colorés par
  verdict, popups vers fiche, légende, fallback noscript). Mais c'est une page
  *nue* : un titre, un paragraphe, la carte. Pas de filtre par verdict/région sur
  la carte (la couleur est là mais non filtrable), pas de lien retour vers un
  récit. La carte est *fonctionnelle* mais *non mise en scène*.

→ **Verdict : à demi-enterrée.** Présente, jamais donnée à voir en avant-poste.

**Les Dossiers — l'accroche reléguée.** Cinq récits éditoriaux signés Eozen, avec
des titres qui *vendent* (« Une terre qu'on ne pourra pas leur racheter », « Le
plateau qu'on a gardé »). C'est **l'actif le plus séduisant du site** — du récit,
de l'incarnation, ce qui retient un lecteur non-expert. Or :
- À l'accueil : **zéro présence**. Aucune intent-card ne les cite, aucune vignette.
  Un visiteur qui arrive sur la home ne sait pas qu'il existe un magazine.
- Dans la nav : un onglet « Dossiers » plat, sans signal qu'il y a là *des récits*
  et non une page technique de plus.
- La page `dossiers/index.html` est belle (grille de cartes-récits, sous-titres
  accrocheurs) — mais on n'y arrive que si on clique l'onglet à l'aveugle.

→ **Verdict : enterré.** Le meilleur hameçon du site est invisible depuis la
porte d'entrée. C'est le diagnostic le plus coûteux de cet audit.

**Le hub Annuaire — un palier de plus, pas une valeur ajoutée.** Le hub a du sens
*conceptuellement* (regrouper liste/carte/classement + acteurs). Mais en pratique
il **insère un clic supplémentaire** entre le visiteur et ce qu'il veut : pour
voir les lieux, je clique « Annuaire » → puis « Tous les lieux ». Deux clics là où
l'accueil offre déjà le lien direct. Le hub se justifie s'il *ajoute de
l'orientation* (priorise, met en scène) ; tel quel, il ne fait que *relayer*.

---

## 3. Ma proposition de navigation attractive

Principe directeur : **la nav ne doit pas seulement lister, elle doit montrer et
hiérarchiser.** Trois leviers — hiérarchiser la barre, donner à voir les
nouveautés dès l'accueil, faire du hub une page-action.

### A. La barre principale — garder 5, mais hiérarchiser

Garder les 5 entrées (le compromis est bon), mais **regrouper visuellement** :

```
[ Terres Libérées ]        Carte   Dossiers   Annuaire   ·   Méthode
   (logo + baseline)       └── destinations ──┘  hub      référence
```

- **Carte** et **Dossiers** en tête (les destinations désirables), **Annuaire**
  ensuite (le hub d'exploration), un séparateur, puis **Méthode** en fin (la
  référence, ton plus discret). Même nombre de liens, mais l'ordre raconte un
  parcours : *je regarde (carte) → je lis (dossiers) → je creuse (annuaire) → je
  vérifie (méthode)*. Implémentable : réordonner `NAV` + une classe CSS
  `nav-ref` sur Méthode pour l'alléger.

### B. L'accueil — donner à voir, pas seulement promettre

Réorganiser `render_index` autour de **trois blocs montrés** (au-dessus de l'État
du corpus, qui reste mais descend) :

1. **Mini-carte vivante** (remplace ou double le CTA « Voir la carte »). Une carte
   Leaflet réduite (hauteur 280 px, zoom verrouillé France), non interactive ou à
   interaction légère, avec un seul appel à l'action « Explorer la carte → ».
   Le visiteur *voit* les 44 points avant de cliquer. C'est le hook géographique.
   *Variante statique si Leaflet sur la home est trop lourd : une image SVG de la
   France semée des points colorés, cliquable vers `carte.html`.*

2. **Bandeau Dossiers — 3 récits en vignettes.** Reprendre 3 des 5 cartes-récits
   de `dossiers/index.html` (titre accrocheur + sous-titre) sur la home, sous un
   intertitre « À lire — les récits ». C'est l'accroche éditoriale. Lien « Tous
   les dossiers → ». **C'est la correction la plus rentable de tout l'audit.**

3. **Garder les 4 intent-cards** (« Par où entrer ») — elles fonctionnent — mais
   les déplacer *sous* carte + dossiers, comme aiguillage secondaire pour ceux que
   le visuel n'a pas happés.

### C. Le hub Annuaire — une page-action, pas un sas

Refondre `render_annuaire` en **une dominante + un repli** :

- **Un bloc « Commencer ici »** en pleine largeur, 3 grandes entrées côte à côte,
  traitées comme des *modes d'exploration* et non des liens : **Carte** (vignette
  carte), **Liste** (« 45 lieux, filtrable »), **Classement** (« le rangement par
  Indice »). Visuel fort, c'est 80 % des besoins.
- **Les acteurs repliés** : porteurs / usufruitiers / réseaux / modèles dans un
  `<details>` « Explorer par acteur » fermé par défaut, ou une rangée discrète de
  liens-texte. On ne supprime rien (le gardien du registre y tient), on
  *hiérarchise* : la matière secondaire ne concurrence plus la principale.
- **Retirer la carte de la liste des 7 cartes** : puisqu'elle a son onglet et son
  bloc « Commencer ici », pas besoin de la répéter en `cat-card` grise.

### D. Mobile

- Barre : le logo + baseline prend trop de place sur 380 px ; réduire la baseline
  (la masquer sous 480 px, garder « TL · Terres Libérées »). Les 5 entrées doivent
  rester accessibles — soit en wrap sur 2 lignes, soit en menu burger si le wrap
  casse la masthead. **Tester en priorité** : c'est là que 5 entrées + logo long
  se télescopent.
- La mini-carte home et la carte pleine : `scrollWheelZoom` déjà désactivé tant
  que la carte n'a pas le focus (bonne pratique anti-piège tactile, déjà en place
  dans `carte.html` — à conserver). Ajouter un geste « tap pour activer ».
- Les vignettes-récits et `cat-card` : déjà en grille fluide, vérifier le passage
  à 1 colonne et que les titres accrocheurs ne soient pas tronqués.

### E. Parcours-types (la nav doit servir 3 intentions)

| Parcours | Entrée | Suite | Sortie |
|---|---|---|---|
| **Découvrir** (curieux) | Accueil → vignette Dossier | récit → fiche du lieu cité | carte / glossaire |
| **Explorer** (chercheur de lieu) | Carte (onglet) ou mini-carte home | marqueur → fiche | classement / comparer |
| **Citer** (journaliste/chercheur) | intent-card « référentiel » | méthode → classement → data.json | changelog |

Chaque parcours doit être **bouclé** : un récit renvoie à sa fiche (déjà fait
côté dossiers → catalogue) ; une fiche devrait renvoyer à son récit *quand il
existe* (vérifier que les 5 lieux-dossiers ont le lien retour fiche → dossier —
point à instrumenter).

---

## 4. Éléments constitutifs (schéma + patterns)

**Schéma d'entrées (cible) :**

```
Barre :  Carte · Dossiers · Annuaire  |  Méthode        (5, hiérarchisées)
Accueil : Hero → Mini-carte → 3 Dossiers → 4 intent-cards → Corpus → Modèles
Hub Annuaire : "Commencer ici" (Carte/Liste/Classement) → <details> Acteurs
Footer : 3 colonnes nommées par parcours (Découvrir / Explorer / Citer)
         au lieu de 2 groupes-inventaire de 20 liens
```

**Patterns à introduire / réutiliser :**
- *Vignette-destination* (carte ou récit montré, pas listé) — nouveau, pour
  carte+dossiers sur la home et le hub.
- *Dominante + repli* (`<details>`) — pour les acteurs du hub.
- *Footer par intention* — réétiqueter les 2 groupes existants en 3 colonnes
  Découvrir/Explorer/Citer, alléger en retirant data.json/changelog vers une
  ligne « Ressources » discrète.
- *Réordonnancement `NAV`* + classe `nav-ref` — le seul changement de code dur
  côté barre ; tout le reste est du contenu de section.

---

## 5. Désaccords prévus

- **Avec le gardien du registre (directeur éditorial).** Il voudra protéger
  l'exhaustivité du footer et la parité des sept catalogues du hub (« tout à
  barème égal » — c'est même écrit dans le hero du hub). Je réponds : *barème
  égal dans la donnée n'oblige pas à poids égal dans la navigation.* Mettre la
  carte en avant ne dévalue pas les réseaux ; les enterrer sous un `<details>`
  les garde accessibles sans qu'ils noient l'entrée principale. Tension réelle à
  arbitrer : densité documentaire vs lisibilité de l'aiguillage.

- **Avec le stratège de l'attractivité (diffusion).** Il poussera la mini-carte
  animée, les vignettes-récits riches en image, peut-être un carrousel. Je
  l'accompagne sur les vignettes Dossiers (on est d'accord : c'est le hook), mais
  je freine sur le spectaculaire : pas de carrousel auto (piège d'accessibilité et
  de mobile), pas de carte plein écran qui repousse le contenu sous la ligne de
  flottaison. La carte doit *montrer puis céder la place*, pas occuper. Mon
  critère reste la clarté du parcours, pas l'effet.

- **Avec la voix « visiteur qui arrive froid ».** Possible accord, possible
  friction : elle pourrait juger que *même* 5 entrées + un hub, c'est trop de
  niveaux pour un primo-arrivant. Mon hub-page-action répond en partie (moins de
  clics utiles), mais si elle plaide pour fusionner Annuaire dans la home, je
  défends le hub *à condition qu'il devienne page-action* — sinon elle a raison
  de vouloir le supprimer.

**Contre-règles respectées** : aucune refonte doctrinale ; pas d'esthétique contre
la clarté (je freine le spectaculaire) ; tout est implémentable en site statique
(réordonner `NAV`, ajouter des sections de contenu, un `<details>`, réutiliser le
Leaflet déjà présent — pas d'usine à gaz).
