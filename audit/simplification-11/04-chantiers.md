# Cycle 3 — Chantiers de simplification (qualification opérationnelle)

*Issus de la synthèse `03-synthese.md`. Trois familles + un préalable + un
parking. Priorités : **P0** préalable bloquant · **P1** lean du commanditaire
(redite, risque nul) · **P2** structure (repli/réordonnancement) · **P3** langue.
La plupart des cibles vivent dans les constantes de chaîne de
`scripts/generate_site.py` (fonctions `render_fiche`, `render_index`,
`render_methode`, `render_glossaire`, `render_regimes`, `render_classement`,
`render_comparer`, `page()` pour le footer) et dans `revues/*/index.md` +
`revues/*/articles/*.md`. Rappel garde-fou projet (CLAUDE.md) : toute modif de
rendu s'accompagne d'un aperçu HTML autonome (CSS inliné) livré pour revue (L9).*

---

## P0 — Préalable bloquant (à faire avant tout le reste)

| Id | Chantier | Cible | Geste | Effort |
|----|----------|-------|-------|--------|
| P0 | **Cohérence Pommiers** | `revues/greenwashing/articles/01-le-sanctuaire-qui-nen-est-pas.md` | L'article dit marchand/56/engagée ; la fiche dit hybride/65/solide (fix A1 #10). **Décision éditoriale requise** : (a) réécrire le passage sur le profil *hybride* actuel — l'« écart mot↔chaîne » reste vrai mais porté par *hybride* ; ou (b) choisir un autre cas-pivot encore *marchand*. | 0,5 j (option a) |

---

## P1 — Couper la redite (lean #4, risque ≈ nul, à faire en premier)

| Id | Chantier | Cible | Geste | Effort |
|----|----------|-------|-------|--------|
| H1 | **Aside « Trois lectures » des fiches** (C1) | `render_fiche` (`verdict-cle`) | Supprimer le bloc ; remplacer par une ligne + lien `methode.html`, sous le panneau de score. ~90 répétitions éliminées (45 fiches × 2 blocs avec H2). | 0,5 j |
| H2 | **`details` « Comment lire les visuels »** (C2) | `render_fiche` (`fiche-key`) | Supprimer (doublon des `axe-cards` Méthode). | 0,25 j |
| H3 | **Triptyque dupliqué** (C4) | `render_methode#triptyque` | Réduire à 2 lignes + ancre `regimes.html#triptyque` ; version longue conservée sur Régimes. | 0,25 j |
| H4 | **Disclaimer « non un label »** (C5) | `page()` footer, `render_index` hero, `render_classement` callout | Foyer = Méthode. Footer de fiche : demi-ligne autoportante (mode isolé). Supprimer les copies longues des pages-cadre. | 0,5 j |
| H5 | **Manifestes de revue : méta-règles** (C9) | `revues/index.md` + 4 `revues/*/index.md` | Remonter « édition vivante » + posture archétype sur la page-mère ; vider les blocs « Forme »/« ligne temporaire » jumeaux ; chaque manifeste cite la formule en 1 ligne + lien. | 0,5 j |
| H6 | **Accueil : fusionner les deux blocs de chiffres** (C12) | `render_index` | Un seul « État du corpus » (3 nombres + histogramme) ; modèles voisins → teaser vers `modeles.html`. | 0,5 j |
| H7 | **Nettoyer le canon qui se répète lui-même** (prérequis de séquencement) | `render_glossaire`, `render_methode#integrite` | Fusionner les 2 entrées glossaire qui se recouvrent (agrégation non compensatoire / indice) ; réécrire `#integrite` sans son doublon intra-paragraphe. **À faire avant H1–H6** (on ne renvoie pas vers un foyer impur). | 0,25 j |
| H8 | **Leads ré-énumérant les 5 axes + double callout anti-palmarès** (C12, R6/R7) | `render_classement`, `render_comparer`, `render_grilles`, `themes` | Callout complet sur le Classement seul ; ailleurs 1 ligne + lien. Légende `axe-legend` gardée là où il y a un pentagone, retirée des leads en prose. | 0,25 j |

---

## P2 — Replier / réordonner (fond conservé, mieux rangé)

| Id | Chantier | Cible | Geste | Effort |
|----|----------|-------|-------|--------|
| S1 | **Objet-verdict composite** (C3) | `render_fiche` (`score-panel`) | Une ligne « verdict · IdL · palier » + renvoi unique. **3 conditions gardien** : signifiants typographiquement distincts ; cas de non-coïncidence lisible (Rayol) ; renvoi obligatoire. | 1 j |
| S2 | **Replier grille + 5 barres ; garder le pentagone** (C7) | `render_fiche` | Grille `details` fermé ; 5 barres chiffrées dans le même dépli ; pentagone seul en profondeur 1. | 0,5 j |
| S3 | **Regrouper les plafonds** (C8) | `render_fiche` | `chaine-note` + ghost indice brut + complétude → ligne « Plafonds appliqués » repliable. | 0,5 j |
| S4 | **Hook d'accueil étagé** (C6) | `render_index` hero | Hook nu d'abord ; honnêteté épistémique juste en dessous en affirmation positive. Couper le hero-lead de moitié. | 0,25 j |
| S5 | **Remonter la carte sous le hero** (idée primo) | `render_index` | La carte colorée par verdict, meilleur instrument anti-jargon, remonte juste sous le hook. | 0,25 j |

---

## P3 — Traduire la langue (aucun concept/note/verdict touché)

| Id | Chantier | Cible | Geste | Effort |
|----|----------|-------|-------|--------|
| L1 | **Réécrire le `title` du badge hybride** (C10) | `render_fiche`/`verdict_badge` (le `title=`) | ≈ 60 mots → < 20 (« Foncier libéré, mais un maillon garde une part de profit privé »). Texte le plus vu du site. | 0,25 j |
| L2 | **« décommodifié »** (C10) | hero + méthode | « retiré du marché / soustrait au commerce » ; mot savant glosé une seule fois. | 0,1 j |
| L3 | **« étoile polaire » → « horizon » ; « sommet » discipliné** (C11) | `render_index`, `render_methode` | Une seule image ; poser l'équivalence sommet=sanctuaire=palier au 1ᵉʳ emploi. | 0,25 j |
| L4 | **Glose jumelée usufruit/nue-propriété + « démembrement »** (C10) | `render_methode` | Phrase « l'un possède sans utiliser, l'autre utilise sans posséder », posée tôt ; « dissociation… (démembrement) ». | 0,25 j |
| L5 | **« triptyque », « indice intrinsèque/effectif/contaminable », « opposable », « rentier »** (C10) | méthode, fiches | Traductions ciblées + gloses d'incise (cf. pédagogue §6). | 0,5 j |
| L6 | **Règle glose/glossaire à deux étages** (T3) | transversal | Noyau 6-8 termes glosés en incise au 1ᵉʳ emploi ; reste lié au glossaire. | cadre, pas un livrable |

---

## Parking — Diffusion (hors mandat « simplifier », à arbitrer : T2)

| Id | Chantier | Note |
|----|----------|------|
| D1 | **Top 10 des lieux** | Objet partageable neuf ; le classement à ~110 entrées + avertissement de non-comparabilité est impartageable. |
| D2 | **Image OG sur mesure** | Tous les `og:image` pointent vers le SVG générique → aperçu social vide. |

---

## Effort indicatif

P0 ≈ 0,5 j · P1 ≈ 3 j · P2 ≈ 2,5 j · P3 ≈ 1,75 j. **Total ≈ 7,75 demi-journées**
hors parking. Tout est réversible et n'engage aucun changement de modèle (ni
verdict, ni IdL, ni grille) — c'est de l'hygiène de rendu et de langue. Chaque
lot touchant le rendu exige son aperçu HTML autonome avant validation (L9).
Aucune mise en ligne sans feu vert explicite de l'opérateur (procédure de push,
CLAUDE.md).
