# Voix 5 — Méthodologue du modèle

*Mini-strat Phase B, cycle 1 (divergence isolée). Volet : strictness des co-gates
du sommet. Critère propre : cohérence interne, faisabilité, calibrage daté. J'écris
pour le mainteneur et le futur-toi. Tous les chiffres ci-dessous sont issus d'une
simulation sur le corpus réel (45 lieux) via le `compute_verdict` codé en A1 — pas
d'estimation.*

---

## Thèse en une phrase

Le sommet n'est pas vide « à cause de `non_subordination` » : il est vide parce que
**trois gates se conjuguent sur un corpus qui n'en documente aucun de façon
convergente**, et le seul gate dont l'absence de donnée bloque mécaniquement *tout
le monde* (`non_subordination`, renseigné sur **0 / 45** fiches) doit redescendre en
glose — sans pour autant ouvrir le sommet, qui reste honnêtement vide.

---

## 1. Cartographie des co-gates actuels (état codé, `compute_verdict` l. 1353-1362)

Le sommet exige que la chaîne soit **pure** (entièrement `non_lucrative` /
`commerciale_desactivee` — sinon `hybride` ou `marchand`) **ET** que cinq blocs
observables soient tous au vert :

| # | Gate (codé) | Critères lus | Statut nominal | Donnée présente sur le corpus |
|---|-------------|--------------|----------------|-------------------------------|
| 1 | Foncier | `foncier_hors_marche=oui` ET `irreversibilite=oui` | gate dur | bien peuplé |
| 2 | Vivant | `vivant_finalite=oui` ET `place_au_vivant=oui` | gate dur | bien peuplé |
| 3 | Régénération (face opposable) | `milieu_protege=oui` | gate dur | **8 oui / 31 non / 4 inconnu / 2 partiel** |
| 4 | Finalité | `usage_non_marchand ∈ {oui,partiel}` ET `usage_interet_general=oui` | gate **doux** (partiel admis) | unm : 2 oui / 32 partiel / 7 non / 4 inconnu |
| 5 | Non-subordination | `non_subordination=oui` | gate dur, proxy unidirectionnel | **0 oui — critère absent des 45 fiches** |

Glose (statut b, pèse sur l'Indice, ne gate pas) : `benefice_non_approprie`
(prévu, non peuplé). Prose (statut c, étoile polaire) : économie du don/troc,
prise en charge collective de la monnaie.

## 2. Position critère par critère, avec conséquence mécanique

J'ai simulé chaque scénario sur les **18 lieux à chaîne pure** (seuls candidats
possibles au sommet ; les 27 autres sont `hybride`, `marchand` ou `None` par la
chaîne, hors d'atteinte du sommet quoi qu'on fasse aux co-gates).

| Scénario | Sommets |
|----------|---------|
| **S0** — modèle actuel (5 gates, `non_subordination=oui` requis) | **0** |
| **S1** — `non_subordination` retiré du gate (→ glose) | **0** |
| **S2** — S1 + régénération retirée du gate | **0** |
| **S4** — foncier + vivant seuls (finalité aussi retirée) | **1** (Rayol) |

Lecture mécanique : **retirer `non_subordination` du gate ne crée aucun sommet** —
parce qu'aucun candidat à chaîne pure ne franchit déjà foncier + vivant + finalité.
Le verrou n'est donc pas un seul gate, mais leur **intersection sur un corpus peu
peuplé**. Décomposition des échecs parmi les 18 :

- `milieu_protege` (régénération) échoue **15/18**,
- vivant échoue **13/18**,
- foncier échoue **12/18**,
- finalité échoue **7/18**,
- foncier **ET** vivant simultanément : **1/18** seulement (Rayol).

Et Rayol, le seul à franchir foncier+vivant+régénération, échoue à la **finalité**
(`usage_non_marchand=non` — accès payant) et n'a pas `non_subordination`.

**Mes positions :**

- **`non_subordination` → glose (statut b), pas gate.** *Raison de cohérence, pas
  de remplissage.* Un gate dur dont la donnée est absente sur 100 % du corpus n'est
  pas un gate : c'est un `return hybride` déguisé. Il ne *trie* rien (il rejette
  tout indistinctement), donc il ne porte aucune information — il viole le principe
  « on gate sur ce qui est observable ». Le proxy unidirectionnel garde tout son
  sens en glose : `non` constaté pénalise l'Indice (axe 3), `oui` documenté le
  crédite, `inconnu` reste neutre. Conséquence mécanique : **+0 sommet** (cf. S1).
  On ne perd donc rien à le déclasser, et on cesse de faire mentir le mot « gate ».
- **`usage_non_marchand` → maintenir en gate DOUX (statut a, `partiel` admis).**
  C'est déjà l'état codé (l. 1359) et il est bien calibré : sur 45 lieux, 32 sont
  `partiel`. Le durcir à `oui` strict ne changerait rien au compte de sommets
  (S3 = 0) mais exclurait d'avance toute ferme en circuit court avec contribution
  modique — exactement la « ferme nourricière » que la doctrine #9 veut pouvoir
  couronner un jour. **Ne pas durcir.** Le couple avec `usage_interet_general=oui`
  (38/45) suffit à écarter le purement marchand.
- **Régénération (`milieu_protege`) → maintenir en gate dur (statut a).** C'est la
  face *opposable* d'une décommodification (terre, abusus matériel) ; elle est
  observable (ORE/RVS/RBI…) et son `non` est un vrai signal, pas une absence. 8
  fiches la portent à `oui`. Elle reste donc un gate qui trie réellement. **Garder.**
- **Foncier, Vivant → gates durs (statut a), inchangés.** Ce sont les deux
  décommodifications les mieux observables et les mieux peuplées ; ce sont eux qui
  font le tranchant du modèle. Ne pas toucher.

## 3. Le traitement du salariat — binaire vs seuil

La grille code `non_subordination` en **binaire** (`oui` / `non` / `inconnu`,
l. 548-563), où un seul salariat constaté bascule à `non`. Position de
méthodologue : **le binaire est juste pour la glose, faux pour un gate.**

- En **gate dur**, le binaire est faux-positiviste à l'envers : un collectif de 12
  associé·es non-salarié·es qui emploie *un* maraîcher en CDD support serait classé
  « subordonné » et perdrait le sommet — alors que sa structure de pouvoir est
  horizontale. Inversement, exiger zéro salariat récompenserait l'auto-exploitation
  militante (angle mort §11 du cadre théorique).
- En **glose**, le binaire redevient acceptable parce qu'il ne tranche plus un
  seuil : il *informe* l'Indice de façon graduée si l'on ajoute `partiel`.

**Proposition concrète** : distinguer **salariat structurel** (l'activité-cœur est
salariée sous autorité d'employeur → `non`) du **salariat support** (fonctions
périphériques : compta, accueil, saisonnier → `partiel`). Soit, en valeurs :
`oui` (travail-cœur non subordonné) / `partiel` (cœur non subordonné mais salariat
support) / `non` (cœur salarié/hiérarchisé) / `inconnu`. Cette graduation n'a de
sens *qu'en glose* — un seuil chiffré (« < 20 % de la masse salariale ») serait du
faux-précis non documentable publiquement, donc à proscrire (biais déclaratif, §10).

## 4. Éviter faux-positivisme ET catégorie vide

Les deux écueils sont **dissymétriques** et je les traite différemment.

- **Faux-positivisme** (sommet trop facile) : danger *doctrinal*, irréversible pour
  la crédibilité. Parade : ne jamais créditer le non-documenté (`inconnu` reste
  bloquant pour les gates a) ; ne jamais déduire un gate de la forme juridique ;
  garder foncier + vivant + régénération en gate dur. Mon déclassement de
  `non_subordination` ne touche pas à cette défense — il retire un gate *vide*, pas
  un gate *exigeant*.
- **Catégorie vide** (sommet inatteignable) : danger *empirique*, réversible. Un
  sommet à 0 aujourd'hui est **honnête** tant que (i) il est atteignable en
  principe — c.-à-d. qu'aucun gate ne dépend d'une donnée qu'on ne collecte jamais —
  et (ii) le chemin pour y entrer est lisible. Or `non_subordination=oui requis`
  viole (i) : il rend le sommet *inatteignable par construction*, pas seulement
  *vide en fait*. **C'est la seule chose à corriger.** Une fois `non_subordination`
  en glose, le sommet redevient atteignable : il suffit qu'un lieu peuple
  foncier+vivant+régénération+finalité. Le sommet reste à 0 aujourd'hui — et c'est
  bien : un sommet vide *atteignable* est honnête ; un sommet vide *impossible* est
  un bug de modèle.

**Règle de calibrage, datée.** Tout seuil/plafond est conventionnel, révisable,
**daté** (§10 du cadre). J'ajoute une règle opérationnelle : *un critère ne peut
être promu au statut (a) gate que s'il est renseigné (oui|non, hors inconnu) sur
≥ 50 % du corpus* — exactement le seuil « `inconnu` < 50 % » déjà écrit au §9 du
cadre théorique, mais qu'on n'a pas appliqué à `non_subordination` (0 % → aurait dû
rester glose dès A1). C'est le garde-fou qui empêche de re-fabriquer un gate vide.

## 5. Éléments constitutifs apportés

**Tableau critère × statut proposé × conséquence mécanique :**

| Critère | Statut actuel | Statut proposé | Sommets si appliqué | Justification |
|---------|---------------|----------------|---------------------|---------------|
| `foncier_hors_marche`+`irreversibilite` | gate dur (a) | **gate dur (a)** | — | observable, peuplé, tranchant |
| `vivant_finalite`+`place_au_vivant` | gate dur (a) | **gate dur (a)** | — | observable, peuplé |
| `milieu_protege` | gate dur (a) | **gate dur (a)** | — | face opposable, 8 oui |
| `usage_non_marchand` (+`usage_interet_general`) | gate doux (a) | **gate doux (a)** | inchangé | partiel admis ; durcir = 0 sommet en plus |
| `non_subordination` | gate dur (a) | **glose graduée (b)** | **+0** | 0/45 peuplé → ne trie rien ; viole « inconnu < 50 % » |
| `benefice_non_approprie` | glose (b) | glose (b) | — | comptable, rarement public |

**Règles de calibrage proposées (datées 2026-05-29) :**
1. *Promotion au statut gate* conditionnée à ≥ 50 % de couverture documentée
   (oui|non) sur le corpus. Sinon → glose.
2. *Gate doux* (admet `partiel`) par défaut pour tout critère dont la valeur
   modale du corpus est `partiel` (ici `usage_non_marchand` : 32/45).
3. *Re-test à chaque jalon de peuplement* : quand `non_subordination` dépassera
   50 % de couverture, ré-évaluer sa promotion en gate (réversibilité assumée).
4. Tout seuil chiffré sur le salariat est proscrit (non documentable → faux-précis).

## 6. Désaccords prévus (test de non-redondance)

- **Avec l'éditeur·rice magazine** (sommet « racontable »). Iel voudra desserrer les
  gates pour qu'il existe *au moins un* sanctuaire à mettre en récit. Mon désaccord
  est net : **on n'assouplit pas un gate pour remplir le sommet** (contre-règle
  explicite). La simulation le tranche pour moi : même en retirant
  `non_subordination` *et* la régénération, on reste à **0** (S2) ; il faudrait
  amputer foncier *ou* vivant *ou* finalité pour fabriquer Rayol en sommet — et
  Rayol est un domaine à **accès payant** géré par une asso descendante : en faire
  le visage du commun décommodifié serait un faux que la presse démonterait. Le
  récit doit porter sur l'**étoile polaire** et sur les `hybride` exemplaires
  (Pommiers, ferme nourricière), pas sur un sommet bidonné.
- **Avec le·la gardien·ne de la rigueur.** Iel pourrait défendre le maintien de
  `non_subordination` en gate dur « par principe doctrinal » (le travail est la
  3ᵉ décommodification de Polanyi, elle doit co-gater). Mon désaccord est *de
  méthode, pas de fond* : je ne conteste pas que le travail co-gate l'idéal — je
  conteste qu'un gate puisse reposer sur une donnée jamais collectée. Le principe
  observable-gaté/posture-glose (§8) **est de son côté autant que du mien** :
  « on gate sur ce qui est observable ». 0/45 n'est pas observable. La rigueur exige
  le déclassement, elle ne s'y oppose pas. La 3ᵉ décommodification reste affirmée en
  prose (statut c) et pèse en glose (statut b) — elle n'est pas reniée, elle est
  remise au bon étage.
- **Point de convergence anticipé** : tout le monde acceptera, je crois, que le
  sommet *reste vide aujourd'hui*. Le débat n'est pas « 0 ou 1 sommet » (c'est 0
  dans tous les scénarios honnêtes) mais « sommet vide-impossible ou vide-
  atteignable ». Je plaide pour vide-**atteignable**.

---

*Fin du volet méthodologue. Position défendable, calibrée, datée, et — surtout —
vérifiée sur le corpus réel : aucun chiffre n'est ici une intuition.*
