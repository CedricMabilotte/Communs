# Améliorations possibles — Communs (cadrage session #11)

*Deux paquets : (1) zones/structures inutiles ou qui se répètent, (2) formulations
pas claires pour un lecteur qui débarque. Consolidé depuis l'audit MARS-strat
(`01-cycle1/`, `02-cycle2/`, `exploration-redite-langue/`). Cadrage seulement —
rien n'est implémenté. Ordonné par impact décroissant dans chaque paquet.*

**Trois garde-fous transverses** (issus du red-team, à respecter pour chaque
geste) :
- *« Couper » veut presque toujours dire **déplacer/renvoyer**, pas supprimer* :
  chaque fiche peut être la première page vue (recherche, partage) → garder un
  rappel court autonome.
- *Ne pas casser l'accessibilité* : les `details`/`aria-label`/textes masqués
  sont la seule version en clair des visuels pour les lecteurs d'écran — on
  replie visuellement, on ne supprime pas.
- *Reformuler ≠ tronquer* : raccourcir un libellé jusqu'à fondre deux cas
  distincts le rend faux.

---

## Paquet 1 — Zones / structures inutiles ou répétées

### Sur la fiche d'un lieu (le plus rentable : tout est multiplié par ~45 fiches)

1. **Aside « Trois lectures, distinctes à dessein »** — re-explique verdict +
   Indice + palier *avant* le lieu, sur chaque fiche. → Réduire à **une phrase +
   lien Méthode**, placée sous le score (pas supprimer : sinon « 65 / solide /
   hybride » devient illisible).
2. **`details` « Comment lire les visuels »** — doublon de la page Méthode. →
   **Replier et alléger** (garder le minimum accessible), renvoyer la règle à la
   Méthode.
3. **Pentagone + 5 barres chiffrées** = la même donnée deux fois. → Garder le
   **pentagone** en façade, **replier les barres** dans le dépli détail.
4. **Trois annotations de plafond dispersées** (note de chaîne + indice brut
   « ghost » + pénalité de complétude). → Regrouper en **une ligne « Plafonds
   appliqués »**, repliable.
5. **Verdict / Indice / palier éclatés en trois zones**. → Les **rapprocher sur
   une ligne** (« Hybride · 65 · Montage solide »), trois libellés visuellement
   distincts + un renvoi. (Rapproche l'affichage, ne fusionne pas les concepts.)
6. **Grille des ~22 critères, dépliée par défaut**. → **Repliée** par défaut.

### Sur les pages-cadre

7. **Triptyque usus/fructus/abusus** rédigé en entier sur Méthode **et** Régimes
   **et** Glossaire. → Un seul foyer (**Régimes**) ; ailleurs, 2 lignes + lien.
8. **Disclaimer « non un label »** en copie longue sur 9 pieds de page + hero +
   callout classement. → Foyer unique (**Méthode**) ; **demi-ligne autonome**
   conservée en pied de fiche (page potentiellement isolée).
9. **Accueil — deux blocs de chiffres** (« chiffres-clés » 45/4/0 et « état du
   corpus ») disent deux fois la composition. → **Fusionner** en un seul bloc.
10. **Accueil — 5 cartes pleines « modèles voisins »** (hors classement,
    estimées). → **Teaser** vers `modeles.html`.
11. **Leads de Classement / Comparer / Thèmes / Grilles** : chacun rouvre en
    ré-énumérant les 5 axes, et le **callout anti-palmarès est dupliqué**
    classement↔comparer. → Callout complet sur le **Classement seul** ; ailleurs
    une ligne + lien.
12. **Manifestes de revue** : blocs « Forme » / « ligne éditoriale temporaire »
    jumeaux sur les 4, + reformulation de la formule en ouverture. → Méta-règles
    remontées sur la **page-mère des revues** ; chaque manifeste entre dans son
    sujet propre.
13. **Le canon se répète lui-même** (à nettoyer *avant* d'y renvoyer le reste) :
    deux entrées de glossaire qui se recouvrent (agrégation non compensatoire ↔
    indice) ; le paragraphe « intégrité du montage » qui se cite deux fois.

---

## Paquet 2 — Formulations pas claires pour qui débarque

*Avant → après indicatifs. Aucune ne change un concept, une note ou un verdict :
on change la langue, pas la doctrine.*

1. **« décommodifiée »** (1ʳᵉ phrase du hero, posée nue) → **« qui retire la terre
   du marché »**. Le mot le plus savant à l'endroit le plus vu.
2. **Le `title` du badge hybride** (~60 mots de jargon, affiché au survol partout)
   → **clarifier** en langue simple — *sans le raccourcir au point de fondre*
   « GAEC preneur de bail » et « lucrativité encadrée » (le moteur les distingue ;
   un libellé trop court mentirait sur les fermes en bail rural, Pommiers
   comprise). À reformuler dans `concepts.verdict`, source unique.
3. **« sommet » / « étoile polaire »** → une **seule image** : « horizon » (déjà
   employé sur le site). Et poser une fois l'équivalence *sommet = sanctuaire =
   palier le plus haut*, puis s'en tenir à « sanctuaire ».
4. **« démembrement »** (évoque la boucherie) → **« dissociation de la propriété
   et de l'usage »** en première formulation, « démembrement » entre parenthèses.
5. **« usufruit / nue-propriété »** (rôles pivots jamais glosés) → glose jumelée
   posée tôt : **« l'un possède la terre sans s'en servir, l'autre s'en sert sans
   la posséder »**.
6. **« triptyque »** → **« les trois pouvoirs du propriétaire »** (les trois mots
   latins restant glosés dessous).
7. **« opposable »** → « qu'on peut faire respecter en justice » ; **« rentier »**
   → « qui sert surtout à encaisser un loyer » (glose d'incise au 1ᵉʳ emploi).
8. **« agrégation non compensatoire »** → gloser au premier emploi : « l'axe le
   plus faible commande — une force ne rachète pas une faiblesse » (le terme
   technique reste en étiquette secondaire).
9. **« indice intrinsèque / effectif », « axes contaminables », « domiciliage »**
   (trois couches de jargon-maison sur la même page) → une phrase humaine : « une
   structure vaut par les lieux qu'elle fait vivre, pas par ses seuls statuts ».
10. **Hero-lead trop long + mise en garde méthodologique avant le sujet** →
    raccourcir ; le hook frappe d'abord, la nuance épistémique vient juste après,
    en affirmation positive.

**Règle de dosage** (pour ne pas re-alourdir en glosant) : glose d'une demi-ligne
en ligne *uniquement* pour les 6-8 termes sans lesquels la phrase suivante est
incompréhensible (libération, usufruit/nue-propriété, chaîne, verdict, sanctuaire,
indice) ; tout le reste reste au glossaire, lié.

---

## Où commencer (si on passe un jour à l'exécution)

Les **doubles gains** sûrs — une zone répétée qui est *aussi* mal formulée : le
triptyque (1×7 + 2×6), le disclaimer (1×8), « décommodifiée » dans le hero
(1×9 + 2×1). Petit risque, effet visible. Les faux amis à traiter *autrement* que
l'intuition : le `title` du badge (clarifier, pas couper), les notices
d'accessibilité (replier, pas supprimer), l'aside « Trois lectures » (une phrase,
pas une coupe sèche).
