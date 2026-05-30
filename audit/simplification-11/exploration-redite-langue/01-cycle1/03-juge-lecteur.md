# Cycle 1 — Le juge-lecteur

*MARS-strat, divergence isolée. Critère unique : pour un vrai lecteur, le
résultat net est-il plus clair ET plus court — ou échange-t-on un défaut
contre un autre ? Trois lecteurs en tête : le journaliste qui scanne, le
militant qui veut citer, le curieux qui veut comprendre.*

---

## 1. Là où A et B se renforcent (double gain)

Ce sont les coups à jouer en premier : la coupe et la reformulation tirent
dans le même sens, le texte rétrécit ET s'éclaire.

**1.1 — Le `title` du badge hybride (~60 mots, dupliqué partout).**
Sur la fiche Pommiers, sur les trois vignettes de l'accueil, sur chaque dossier,
le même pavé de ~60 mots est planqué dans un attribut `title` invisible au
survol mobile : *« La chaîne ne comporte aucun maillon marchand, mais au moins
un maillon à lucrativité encadrée… »*. C'est le cas-modèle du double gain.
Geste A : ce texte n'a aucune raison d'être recopié à l'identique sur chaque
écho d'un même verdict — il appartient à `methode.html#verdict`, où il figure
déjà mot pour mot. Geste B : même reformulé, il reste illisible en infobulle.
**Couper le `title` partout + renvoyer au verdict de la méthode = on supprime
~5 répétitions ET on désamorce un hermétisme.** Le journaliste qui scanne ne
perd rien (il ne lisait pas l'infobulle), le curieux gagne un lien vers la vraie
explication. Premier coup à jouer, sans arbitrage.

**1.2 — « décommodifié / décommodification ».** Le mot apparaît dans le hero
de l'accueil (*« une économie citoyenne, non lucrative et décommodifiée »*),
dans la vignette du Rayol (*« ce que la décommodification exige vraiment »*) et
dans la méthode (*« l'idéal d'une économie pleinement décommodifiée »*). Triple
occurrence d'un jargon militant. Reformuler une fois (« sortie de la logique
marchande », « rendue au non-marchand ») permet de **réutiliser la même
formule** aux trois endroits au lieu de trois variantes savantes. B nourrit ici
une mini-fusion lexicale : un seul mot clair, posé trois fois, est plus court à
lire que trois habillages différents du même concept. Le militant qui veut
citer y gagne une phrase reprenable.

**1.3 — « sommet / étoile polaire / horizon plus qu'une case ».** La même image
revient au moins quatre fois : accueil (*« le sommet n'est pas une case à
remplir — c'est une étoile polaire »*), puis dans la méthode au moins deux fois
(*« Sommet rare, horizon plus que case à remplir »* / *« le sommet est donc rare
— un horizon plus qu'une case à remplir »*), dans le `title` du verdict, dans
l'aside « Trois lectures ». La métaphore est jolie une fois, opaque répétée.
A coupe les redites ; B la pose une seule fois en clair (« le niveau le plus
haut reste hors d'atteinte — aucun lieu ne l'atteint encore »). **La coupe
supprime la redondance, la reformulation supprime la métaphore filée** : double
gain net. Le curieux comprend enfin que « sommet » = « sanctuaire » = « le
palier réservé », trois noms pour une chose.

**1.4 — Le disclaimer « non un label ».** Il figure dans le footer de chaque
page (*« une évaluation au regard d'un cadre explicite et contestable, non un
label »*) ET dans `methode.html#limites` (*« non un label »*) ET, reformulé, en
tête d'accueil. Trois fois la même mise en garde. A : le footer suffit (il est
partout) ; la version méthode est redondante. Garder une formulation claire,
une seule fois en corps de page. Gain net des deux côtés.

---

## 2. Là où A et B s'opposent (arbitrage)

**2.1 — L'aside « Trois lectures, distinctes à dessein » (verdict · Indice ·
palier).** C'est le cœur du conflit. Cet encart de ~90 mots est répété sur
chaque fiche. Geste A veut le couper. Mais **il porte la seule explication d'un
piège réel** : sur Pommiers, l'Indice est 65 (« Montage solide ») mais le
verdict est « hybride », donc le lieu n'accède pas à « Libération aboutie »
malgré un chiffre élevé. Sans l'aside, le lecteur voit « 65 / Montage solide /
hybride » et ne comprend pas pourquoi trois étiquettes coexistent.
**Qui gagne ? B, partiellement.** Couper sec rend muet : le curieux et le
journaliste resteront perplexes devant trois libellés non articulés. Mais
garder 90 mots répétés sur 45 fiches est intenable. La sortie : **reformuler en
UNE phrase + lien**, déposée une fois sur la fiche (pas un encart à puces) —
« Trois lectures distinctes : le verdict dit *où* sur l'axe marché↔commun,
l'Indice *combien* (0-100), le palier *quelle tranche* — un Indice élevé peut
rester "solide" sans être "abouti". [Comment ça marche →] ». On garde le sens,
on perd 70 mots, on déduplique vers la méthode. **A et B coopèrent à condition
que B ne regonfle pas : une phrase, pas un paragraphe.**

**2.2 — Le « Comment lire les visuels » (`details` repliable).** A veut le
couper (~90 occurrences). Mais le pentagone à cinq axes n'est pas auto-explicatif :
sans légende, le curieux ne sait pas que « plus la zone colorée s'étend vers un
sommet, plus le montage est noté ». **Qui gagne ? A — la coupe l'emporte ici**,
parce que le bloc est déjà `<details>` replié (donc le scanneur ne le voit pas)
ET parce que le `aria-label` du SVG porte déjà le détail chiffré (« Le sol 87,
La structure 40… »). La vraie économie : couper le `details` de chaque fiche et
le déplacer une fois sur `methode.html#indice`, où les cartes d'axes existent
déjà. Le lecteur qui veut comprendre le visuel ira à la méthode — il y est déjà
renvoyé par le lien « Indice de libération » du panneau de score.

**2.3 — Le triptyque usus/fructus/abusus.** Présent en entier dans la méthode
ET (dit la consigne) dupliqué sur `regimes.html`. A veut dédupliquer. B veut
traduire « usus/fructus/abusus » (latin de juriste). Ici **A et B ne s'opposent
pas frontalement** mais B coûte : la méthode contient déjà la version en clair
(*« se servir du bien, en tirer un revenu, et en disposer — jusqu'à le
détruire »*), donc le latin pourrait disparaître du corps et ne rester qu'en
glossaire. Gain net. Pas d'arbitrage douloureux — sauf pour le militant, qui
*veut citer* le triptyque latin parce que c'est le vocabulaire reconnu du droit
des communs. **Compromis : garder les trois mots latins une fois, entre
parenthèses, derrière la formule claire ; les couper partout ailleurs.**

---

## 3. Le risque caché de la fusion (verdict · Indice · palier en un objet)

Oui, le risque est réel et mérite qu'on s'y arrête. Fusionner les trois
instruments en un seul objet d'affichage peut produire un **bloc dense** qui
remplace trois opacités par une opacité compacte. Sur Pommiers, l'objet fusionné
porterait : « 65 / Montage solide / hybride » + ghost à 67 + curseur + pénalité
de complétude + note de plafond « ne peut être notée plus haut que 40 ». Empilé,
c'est illisible.

**La fusion reste lisible à trois conditions :**

1. **Hiérarchie visuelle, pas juxtaposition.** Un chiffre dominant (l'Indice,
   65), le palier en sous-titre coloré, le verdict en étiquette latérale. Pas
   trois éléments de même poids alignés.
2. **Le détail technique part en profondeur 2.** Le « ghost » (indice brut 67),
   la pénalité de complétude, la note de plafond axe-2 : utiles au chercheur,
   bruit pour les trois autres lecteurs. Ils doivent être repliés ou renvoyés à
   la fiche-méthode, pas affichés en façade.
3. **Une seule phrase d'articulation** (celle du §2.1) accompagne l'objet — sinon
   la fusion *cache* la distinction verdict≠palier au lieu de la clarifier, et
   le piège « solide mais pas abouti » redevient invisible.

Sans ces conditions, la fusion est une régression : on aura troqué trois blocs
clairs-mais-redondants contre un bloc-bouillon. **La fusion n'est un gain que si
elle s'accompagne d'une mise en profondeur** — ce qui est, de fait, un troisième
geste (voir §4).

---

## 4. Verdict de suffisance

Les deux gestes A+B traitent l'essentiel du volume et de l'hermétisme, mais
**ils ne suffisent pas seuls** : le lecteur réclamerait un **troisième geste —
la mise en profondeur (hiérarchiser : façade / pli / page-méthode)**.

La raison est arithmétique, et c'est le nœud de la séance : A *enlève*, B
*ajoute*. Sur les zones de double gain (§1) le solde est négatif (plus court).
Mais sur les zones d'arbitrage (§2.1, §3), B regonfle dès qu'on refuse de rendre
le lecteur muet. La fiche Pommiers est saturée d'instruments concurrents
(badge, pentagone, barres, échelle à segments, ghost, curseur, note de plafond,
note de complétude, recap de grille, grille complète) : couper les redites et
reformuler les termes ne résout pas la **densité d'instruments** — elle la
laisse intacte. Le journaliste qui scanne décroche non pas à cause d'un mot dur,
mais à cause du *nombre de choses à regarder en même temps*.

Le troisième geste n'est pas « réordonner » (l'ordre est déjà à peu près bon :
verdict → Indice → présentation → grille) ; c'est **stratifier** : décider, pour
chaque instrument, s'il est façade (vu par tous), pli (vu sur clic) ou
page-méthode (vu par le chercheur). Sans cette strate, la fusion du §3 retombe
dans le bloc dense, et la phrase d'articulation du §2.1 finit par cohabiter avec
six autres notes — donc se noie.

**Réponse nette : A+B sont nécessaires et bien ciblés, mais insuffisants pour
"aller droit au but". Il faut un troisième geste de stratification (profondeur),
sans lequel le double gain de §1 est mangé par le regonflement de §2 et la
densité résiduelle de la fiche.**

---

## Retour en 3 lignes

1. **Les deux gestes au net : non, pas suffisants.** A+B donnent un gain réel et
   ciblé sur les redites pures (badge `title`, « décommodifié », « sommet »,
   disclaimer), mais laissent intacte la *densité d'instruments* de la fiche-lieu ;
   il manque un troisième geste — **stratifier en profondeur** (façade / pli /
   méthode).
2. **Le seul endroit où couper et reformuler s'opposent vraiment :** l'aside
   « Trois lectures » (verdict · Indice · palier) — couper rend le lecteur muet
   devant « 65 / solide / hybride », reformuler regonfle.
3. **Qui doit gagner là : B, sous contrainte** — on garde le *sens* mais en UNE
   phrase + lien vers la méthode, jamais l'encart à puces répété sur 45 fiches.
