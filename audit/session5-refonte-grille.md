# Audit & refonte de la grille — session #5

*26 mai 2026. Auto-critique de la notation des modèles commerciaux, refonte
de la grille d'évaluation. Référence durable de la session.*

---

## Le problème (avant la session)

L'audit chiffré du corpus a fait apparaître une incohérence structurelle entre
l'**Indice de libération** (calculé par la grille des cinq axes) et le
**verdict** introduit en session #4 par le chantier 1bis (calculé sur le
`nature_interet` de la chaîne) :

- *Top 5 des lieux* : 1. La Ferme de Pommiers — **IdL 85, palier abouti,
  verdict marchand**. 2. Château de la Mhotte (hybride, 84). 3. Terres du
  Larzac (verdict à établir, 84). 4. La Durette (marchand, 80). 5. Ferme de
  la Licorne (marchand, 80).
- *Sept* lieux verdict `marchand` atteignaient les paliers « solide » ou
  « libération aboutie ».
- Le seul `sanctuaire` du corpus, le Domaine du Rayol, n'arrivait qu'au
  *dixième rang*, palier « solide » (IdL 77, sous le seuil 78 de
  « libération aboutie »).

La cause racine : la grille `lieu` et le verdict parlaient deux langues
différentes. Sur la fiche `ferme-de-pommiers`, le critère
`montage_non_commercial` était coté `oui` avec la note « le GAEC est une
société civile agricole, *non une société commerciale* » — alors que le
1bis classe précisément les GAEC en `nature_interet: commerciale` (les SC
agricoles valorisent un intérêt collectif lucratif). Deux ontologies
parallèles, aucun garde-fou pour les réconcilier.

Six autres failles ont été repérées :

2. **Moyenne géométrique avec plancher d'axe à 1** trop douce — la
   non-compensation théorique ne jouait jamais en pratique.
3. **Contamination par la chaîne asymétrique** — `apply_chaine` ne touche
   pas les lieux, donc une grille saisie pouvait afficher un axe 2 élevé
   sur une chaîne marchande sans qu'aucun mécanisme ne corrige.
4. **Palier « libération aboutie » sous le sanctuaire** — incohérence
   terminologique : un label de pureté accessible à des montages non
   sanctuaires.
5. **Modèles voisins flottant sans pénalité de complétude** — leurs
   `axes_estimes` les hissaient au-dessus des lieux réels (CLT Bruxelles
   à 87).
6. **L'État pas pénalisé** — l'axe 3 (gouvernance citoyenne) n'avait pas
   de critère discriminant la gouvernance descendante d'une personne
   publique de l'autogestion d'un collectif d'habitants.
7. **Hygiène méthodologique** — les `partiel` et `inconnu` étaient
   sur-utilisés sur les critères `milieu_protege`, `vivant_finalite`,
   `place_au_vivant` ; des fiches portaient `partiel` alors que leur
   propre note disait clairement « aucun dispositif documenté ».

## Le modèle puriste cible (arbitrage opérateur)

Le pôle de référence est désormais explicité : un lieu *autogéré par un
collectif d'habitants*, au sein d'une *entité de droit civil d'intérêt
général*, dont le foncier est détenu par un *autre organisme de droit civil
d'intérêt général* (ou d'utilité publique). Les lieux gérés par l'État ne
sont pas le sommet ; un lieu commercial ne doit pas ressortir noté haut ; un
modèle voisin doit *atteindre* le seuil bas du segment convenable, non le
dépasser ; la présence d'un maillon commercial ou productiviste doit
contaminer plus négativement la notation.

## Les sept patches livrés

**P0/P2 — plafond de chaîne sur l'axe 2 du lieu.** Implémenté dans
`scripts/generate_site.py` (`apply_lieu_plafond_chaine`). Configuration
dans `config/ranking.yml § plafonds_chaine.ax2_par_nature` :

| nature_interet | plafond ax2 |
|----------------|-------------|
| non_lucrative | 100 |
| commerciale_desactivee | 80 |
| commerciale_encadree | 50 |
| commerciale | 20 |
| privee_individuelle | 10 |
| inconnu | aucun (prudence) |

Pour chaque lieu, le score d'axe 2 est plafonné selon le pire
`nature_interet` de sa chaîne. Le score intrinsèque est conservé pour
information (`sc['ax2_intrinseque']`) et l'écart est annoté sur la fiche.
**Source unique de vérité : la chaîne**, comme pour le verdict.

**P1 — plancher d'axe géométrique abaissé de 1 à 0,5.** Dans
`generate_site.py`, `AXE_PLANCHER_GEO = 0.5`. Un axe écrasé pèse désormais
plus sur la moyenne géométrique — la non-compensation redevient mordante.

**P3 — palier « libération aboutie » réservé au verdict sanctuaire.**
Dans `ranking.yml § paliers.abouti`, ajout d'un attribut
`requiert_verdict: sanctuaire`. La fonction `palier_for` accepte un
argument verdict optionnel ; un palier portant `requiert_verdict` est
dégradé au palier suivant si le verdict ne satisfait pas l'exigence. Seuil
min ramené de 78 à 70 (la promesse du palier vient désormais du verdict,
pas du seuil quantitatif).

**P4 — pénalité d'estimation sur les modèles voisins.** Dans
`generate_site.py`, `score_fiche` pour la catégorie `modele` applique une
pénalité forfaitaire de 0,85 (équivalent à une fiche moyennement
renseignée). Un modèle voisin atteint désormais au mieux le bas du palier
« solide ».

**P5 — critère neuf `autogestion_usagers`.** Ajouté à la grille porteur
(`grilles.yml § porteur > pouvoir`), axe 3, poids 3. Distingue la voix
*délibérative* des usager·es de la simple consultation ou de la décision
descendante. Une personne publique coche `non` par défaut. Coté sur les 20
porteurs en parallèle (4 sous-agents partitionnés, méthode L7/L12).
Distribution : 2 `oui`, 1 `partiel`, 1 `inconnu`, 16 `non`.

**P7 — hygiène des fiches lieu marchand.** Passe de durcissement sur 15
fiches, en 2 sous-agents parallèles. 21 modifications de `partiel` ou
`inconnu` → `non` sur les critères `milieu_protege`, `vivant_finalite`,
`place_au_vivant` quand la note attachée disait elle-même « aucun X
documenté ».

**Annotation visible sur les fiches.** Sur chaque fiche de lieu plafonnée,
la mention apparaît sous le score : « Axe 2 (la structure) plafonné à X
par la chaîne — un maillon de nature « Y » empêche un axe 2 élevé, quoi
que cochent les critères saisis (score intrinsèque : Z). » Application de
la leçon L11 — un calcul n'est utile que si son écart à la saisie est
montré.

## Effet sur le corpus

**Avant / après** sur la Ferme de Pommiers :
- avant : IdL 85, palier « libération aboutie », axes (93,100,86,100,83)
- après : IdL 56, palier « engagement réel », axes (93,20,86,100,83). Axe 2
  intrinsèque 100 → plafonné 20.

**Distribution des paliers par verdict** :

| verdict | abouti | solide | engage | partiel | eloigne |
|---------|--------|--------|--------|---------|---------|
| sanctuaire | 1 | 0 | 0 | 0 | 0 |
| hybride | 0 | 17 | 7 | 0 | 0 |
| marchand | **0** | **0** | 10 | 4 | 1 |
| (à établir) | 0 | 2 | 2 | 1 | 0 |

Le palier « libération aboutie » ne contient désormais qu'un seul lieu (le
Domaine du Rayol — sanctuaire). Aucun marchand n'atteint le palier
« solide ». Cohérence verdict ↔ palier rétablie.

**Top 5 des lieux après refonte** :
1. Château de la Mhotte (hybride) — 84, solide
2. Terres du Larzac (à établir) — 84, solide
3. La Ferme du Berquet — La Faille (hybride) — 79, solide
4. La Marinie (hybride) — 78, solide
5. **Domaine du Rayol (sanctuaire) — 77, abouti**

**Modèles voisins** (avec pénalité 0,85) :

| Modèle | IdL brut | IdL pénalisé | palier |
|--------|----------|--------------|--------|
| CLT Bruxelles | 87 | 74 | solide |
| Stiftung trias | 84 | 71 | solide |
| OFS-BRS | 76 | 65 | solide |
| Mietshäuser Syndikat | 73 | 62 | engage |
| Coopérative ALUR | 72 | 61 | engage |

Aucun modèle ne franchit le seuil 78 du seuil sanctuaire « numérique »
historique ; tous atteignent le bas du segment convenable, comme demandé.

## Points en suspens

- **Conservatoire du littoral** : descend de 82 à 78 après la cotation de
  `autogestion_usagers=non`. Reste plus haut que la Fondation Terre de
  Liens (77). L'effet du nouveau critère est tangible mais limité —
  l'amplifier exigerait soit un poids plus élevé (4-5 au lieu de 3) soit
  un plafond explicite sur l'axe 3 pour les personnes publiques. Reporté
  à une session ultérieure si l'opérateur le souhaite.
- **Hygiène complète du corpus** : la passe d'hygiène a porté sur les 15
  lieux marchand ; les 24 lieux hybrides et les 5 « à établir » n'ont pas
  été repassés. Les `partiel`/`inconnu` abusifs peuvent y subsister sans
  conséquence sur la cohérence palier↔verdict, mais avec un IdL légèrement
  surévalué. Backlog.
- **Pondérations** : restées telles quelles. Toute repondération devrait
  s'appuyer sur une distribution observée. Backlog.

## Garde-fous tenus

- Garde-fous du générateur (uid, chaînes, entités HTML) verts à chaque
  régénération.
- Méthode L7/L12 appliquée pour la cotation des porteurs et l'hygiène des
  lieux : 6 sous-agents simultanés, partition disjointe des fichiers,
  aucune collision.
- Méthode L11 appliquée pour la sanction visible : l'écart entre l'axe 2
  intrinsèque et l'axe 2 plafonné est affiché sur la fiche, jamais saisi.
- Méthode L9 appliquée : aperçus HTML autonomes (CSS inliné) générés pour
  ferme-de-pommiers, domaine-du-rayol, chateau-de-la-mhotte et
  classement, livrés dans `apercu/`.
