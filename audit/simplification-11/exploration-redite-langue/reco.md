# Recommandation — redites/fusion (posture 4) × reformulation pédagogique

*Exploration MARS-strat ciblée, session #11. 3 voix (fusionneur, reformulateur,
juge-lecteur) + 1 red-team. Sortie volontairement courte : une réponse nette,
les bons premiers coups, les pièges. Traces : `01-cycle1/`, `02-cycle2/`.*

---

## Réponse nette

**Tes deux gestes sont le bon réflexe, mais ne suffisent pas seuls — et il faut
les requalifier, sinon ils dégradent le site.**

Trois corrections que l'exploration impose :

1. **« Couper la redite » doit vouloir dire *déplacer / renvoyer*, pas
   *supprimer*.** Communs est un site généré multi-entrées : chaque fiche est
   indexée et peut être la *première* page qu'un lecteur voit (recherche,
   partage). Un rappel court et autonome n'est donc pas une redite — c'est la
   condition d'autonomie de la page. Et certaines « notices » (les `details`,
   `aria-label`, textes masqués) sont la **seule** version en clair des visuels
   pour un lecteur d'écran : les couper casse l'accessibilité. → On *raccourcit
   et on renvoie*, on ne supprime que ce qui est vraiment dupliqué à la main ET
   accessible ailleurs.

2. **« Reformuler en clair » doit *préserver la distinction*, pas raccourcir à
   tout prix.** Le cas-test : le `title` du badge hybride. Il n'est pas dupliqué
   (source unique `concepts.verdict`), donc le couper ne gagne rien ; et le
   réduire à « <20 mots » fusionnerait deux verdicts que le moteur distingue
   (GAEC preneur de bail ≠ lucrativité encadrée) — le badge mentirait sur les
   fermes en bail rural, dont Pommiers. Reformuler = rendre clair sans perdre la
   nuance, pas tronquer.

3. **Le vrai levier manquant : stratifier en profondeur.** Les deux gestes
   traitent le symptôme (texte répété, jargon) mais pas la maladie pointée par le
   juge-lecteur et le red-team : la **densité d'instruments concurrents** sur la
   fiche. La réponse à « aller droit au but » n'est pas tant couper que
   **étager** : façade (ce qu'on voit) → pli replié (le détail) → page Méthode
   (la doctrine). Ce n'est pas une refonte lourde : c'est de la divulgation
   progressive (`<details>`), réversible.

**Donc la bonne triade, dans l'ordre :**
**reformuler (clarté) → stratifier (profondeur) → couper la vraie redite.**
Reformuler d'abord, parce qu'on doit savoir ce que dit un bloc en clair avant de
décider s'il se replie ou se renvoie ; couper en dernier, et seulement la
duplication manuelle réelle.

---

## Les bons premiers coups (double gain, sûrs)

Là où une redite est *aussi* hermétique *et* vraiment dupliquée à la main —
couper-et-clarifier sont le même geste :

- **Triptyque usus/fructus/abusus** : exposé en entier 3× (méthode + régimes +
  glossaire). → Un seul foyer (Régimes), reformulé une fois en « les trois
  pouvoirs du propriétaire (l'usage, les revenus, la disposition) ». Ailleurs :
  le nom + un lien.
- **Disclaimer « non un label »** : copies longues sur pages-cadre (Méthode à un
  clic) → renvoi ; demi-ligne autonome conservée en pied de *fiche* (page
  potentiellement isolée).
- **Hero d'accueil** : « décommodifiée » → « qui retire la terre du marché »
  (plus court *et* plus clair) ; le hook frappe d'abord, la nuance suit.

## Les faux amis (à NE PAS traiter comme l'intuition le suggère)

- **Le `title` du badge** : ne pas raccourcir (il mentirait) ; le clarifier dans
  `concepts.verdict` sans perdre la distinction GAEC-bail / lucrativité encadrée.
- **Les `details`/`aria-label` des visuels** : ne pas supprimer (accessibilité) ;
  les replier visuellement, oui.
- **L'aside « Trois lectures »** : ne pas couper sèchement (le verdict composite
  devient illisible) — le réduire à *une phrase* + lien, gardée sur la fiche.

---

## En une ligne

La simplification de Communs n'est pas « couper + reformuler » : c'est
**reformuler pour clarifier, étager pour désengorger, et ne couper que la
duplication manuelle réelle** — « couper » signifiant le plus souvent *renvoyer*,
jamais *priver le lecteur ou le lecteur d'écran*.

*(Méta : le red-team a corrigé deux affirmations fausses du cycle 1 — le badge
« double gain » illusoire, la coupe qui casse l'a11y/l'autonomie de page. Cycle 2
productif. Détail dans `02-cycle2/red-team.md`.)*
