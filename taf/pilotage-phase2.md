# Pilotage de la phase 2 — document unique réconcilié

*Écrit en session #10 (29 mai 2026). Repositionnement méta validé par l'opérateur.
Ce document **réconcilie et remplace comme référence de pilotage** les deux cadres
issus de #9 qui se contredisaient : la `06-demarche-phase2.md` (séquencement étagé)
et le `brief-refonte-totale-site.md` (big-bang). Les deux restent consultables comme
trace ; en cas de divergence, **c'est ce document qui tranche**. Il recale aussi les
15 chantiers #8d sur la doctrine #9.*

---

## 0. La partition directrice — étagé-moteur / big-bang-carrosserie

Les deux cadres de #9 ne se contredisent que si on les lit comme un seul plan. Lus
comme **deux phases**, ils se réconcilient sur la précondition §6 du brief
refonte-totale (« A1 codé avant la refonte totale, sinon on refond sur du sable ») :

- **Phase A — le moteur, en étagé.** Coder le modèle d'évaluation résolu (A1) puis
  valider/migrer le cadre canonique. Un socle à la fois, vérifié au Checker
  MARS-prod. C'est le régime de la `06-demarche-phase2.md`, appliqué à la fondation.

- **Phase B — la carrosserie, en big-bang.** *Une fois le moteur stable*, refondre
  le rendu public (les chantiers restants) sous une seule direction théorique, en
  contenu frais. C'est le régime du `brief-refonte-totale-site.md`, appliqué à la
  surface.

Règle mnémonique : **étagé pour le moteur, cohérent-simultané pour la carrosserie.**

Ce qui était présenté comme une contradiction (incrémental vs total) est en réalité
un **ordre** : on ne peut pas refondre d'un bloc un rendu qui expose un modèle qu'on
est encore en train de changer. L'étagé n'est pas un pis-aller ; c'est la discipline
de la fondation. Le big-bang n'est pas de la précipitation ; c'est la cohérence de
la surface, possible seulement après stabilisation.

---

## 1. État réel des verrous (corrige les scories des cadres #9)

La `06-demarche-phase2.md` met en tête une « Étape 0 — arbitrer les 3 tensions »,
alors que son propre §0 note qu'elles **sont déjà tranchées en #9**. On acte donc :

- **Tensions #8d — closes.** Cible = **utilité publique** (presse/décideurs/
  militants, attention grand-public). Verdict = **prise éditoriale assumée**.
  Architecture = **catalogue + magazine** (hooks dans les fiches). L'« Étape 0 » de
  la démarche est sans objet.
- **Mini-strat Phase B — différée** (décision opérateur #10). L'architecture des
  trois niveaux de lecture et le gabarit de fiche refondu (la seule poche où une
  passe MARS-strat courte reste légitime, brief refonte-totale §5) **n'est pas
  ouverte maintenant** : prématurée tant que le moteur n'est pas codé. À rouvrir en
  ouverture de Phase B.
- **MARS-strat global — non requis maintenant.** Les tensions sont tranchées, la
  doctrine résolue ; la seule question stratégique restante (étagé vs big-bang) est
  un binaire, désormais tranché par ce document. Réouverture seulement sur signal
  d'un décalage structurant (carnet L-meta-7), pas par perfectionnisme (L-meta-9b).

---

## 2. Recalage des chantiers #8d sur la doctrine #9

Les 15 chantiers (`audit/revue-editoriale-8d/04-chantiers.md`) ont été qualifiés
**avant** la refonte doctrinale (Ostrom→Polanyi, discipline observable-gaté /
posture-glose). Recalage :

| Chantier | Statut après #9 | Note de recalage |
|---|---|---|
| **A1** piège GAEC | **Étendu** (refonte majeure) | La spec #9 (`taf/spec-A1-implementation.md`) remplace la reco #8d : cran `exploitation_agricole`, dérivation nature×titre, co-gates du sommet (non-subordination, régénération, finalité), glose. Plafond 40 (et non 60-70 de #8d). |
| **A3** lisibilité verdict×palier×Indice | À recaler | Doit exposer la mécanique #9 (co-gates, glose), pas l'ancienne. Dépend d'A1 codé. |
| **A4** déni de jugement | **Tranché sur le fond** | Devient « indicateur composite conventionnel façon IDH » (L39). Reformulation actée, reste la prose. |
| **A5** socle conceptuel | **Largement écrit** | `audit/refonte-theorique-9/04-cadre-theorique-complet.md` fait la matière. Reste : bibliographie formelle + mise en page publique. |
| **B4** accueil / chiffres-clés | Dépend d'A1 | Les chiffres (« 1 seule libération aboutie », distribution verdicts) **changeront** après A1 — ne pas figer avant. |
| A2, B1, B2, B3, C1-C4, D1, D2 | Inchangés sur le fond | Orthogonaux à la doctrine ; qualifications #8d tiennent. D1 (hygiène cicatrices) reste érigé en règle, pas option. |

**Conséquence** : A5 et A4 sont moins lourds qu'estimé en #8d (matière déjà
produite en #9). A1, A3, B4 sont **gatés par A1 codé** — d'où la primauté d'A1.

---

## 3. Séquencement opérationnel

### Statut Phase A — A1 CODÉ (session #10, 29 mai 2026)

A1 implémenté et régénéré, garde-fous verts. Distribution : marchand 15→4,
hybride 24→36, à établir 5, **sanctuaire 1→0**. Pommiers `marchand`→`hybride`
(IdL 56→64, palier Solide) — fix-phare obtenu. **Sommet vide assumé** (décision
opérateur #10, option 3) : ce n'est pas un problème, de nombreux lieux restent à
documenter ; la *strictness des co-gates* (faut-il que `usage_non_marchand` et
`non_subordination` soient des gates durs ou des gloses — discipline à 3 statuts
L-meta-8) est **renvoyée à la mini-strat Phase B**. Checker MARS-prod : effet
mineur documenté (le critère neuf `non_subordination` ajoute un angle mort →
−1,64 IdL moyen sur 44 lieux, max −2 ; à résorber par peuplement).

**Phase A bouclée (session #10).** Préconditions du brief refonte-totale §6 :
1. **A1 codé et stable** — fait (commit `aabd433`).
2. **Cadre canonique** — `brief-cadre-conceptuel-communs.md` réécrit en énoncé #9+A1
   (ancrage polanyien, verdict, co-gates, observable-gaté/posture-glose, statut
   épistémique), pointant vers `04-cadre-theorique-complet.md` exhaustif.
3. **Cible** — utilité publique, acquise #9.
4. **Fraîcheur** — actée comme règle (D1).
Plus l'**alignement public** (commit `1189966`) : page méthode dotée d'une section
« verdict » + statut épistémique conventionnel ; encart fiche A3 (verdict×palier×
Indice). **Reste avant un site pleinement frais** : l'hygiène D1 des cicatrices
(« refonte #3 » ×10 en méthode, « session #N » en grilles) — **chantier Phase B**,
non introduit par #10.

**Push** : désormais défendable (modèle corrigé + expliqué). Seul manque la
fraîcheur D1 (Phase B). À l'arbitrage opérateur : pousser maintenant (fix Pommiers
+ explication en ligne, cicatrices pré-existantes inchangées) ou grouper avec
Phase B.

### Phase A — le moteur (en cours, session #10+)

1. **A1 codé** (`taf/spec-A1-implementation.md`, turnkey). Atomique : config +
   générateur + migration corpus en un lot (L14), garde-fous verts, aperçus L9
   (badge Pommiers change). Décisions §7 de la spec **tranchées en #10** selon le
   principe *moteur minimal réversible / cadres profonds renvoyés à la Phase B* :
   A1 ne code que le cran `exploitation_agricole`, la dérivation relationnelle, le
   gate `non_subordination` (seul critère neuf), la régénération via `milieu_protege`
   existant (option a), défaut prudent, plafond 40 provisoire. Renvoyés à la Phase B :
   critère gradué `regeneration` (b), `benefice_non_approprie`, glose d'affichage,
   renommage `sanctuaire`.
2. **Cadre canonique validé** : `04-cadre-theorique-complet.md` validé, puis énoncé
   canonique migré vers `brief-cadre-conceptuel-communs.md` (sans recopier les
   traces de session dans le public).

Fin de Phase A = les 4 préconditions du brief refonte-totale §6 réunies (A1 stable,
cadre validé, cible confirmée, principe de fraîcheur acté).

### Phase B — la carrosserie (mini-strat FAITE, exécution à venir)

**Mini-strat ouverte et close (session #10)** — trace `audit/mini-strat-phaseB-10/`
(5 voix cycle 1, réactions croisées cycle 2, synthèse, leçons-méta). Cadre
d'architecture validé : navigation par intentions (4-5 entrées ; Carte/Classement =
vues de l'Annuaire) · fiche à deux profondeurs (bandeau A3 déplié + synthèse citable
au-dessus, audit en-dessous) · magazine en **surcouche de chemins** (ne touche ni
Indice ni symétrie) · carte B1 (manque n°1) · hygiène D1 · contrat de lecture
affiché. **Co-gates tranchés** : foncier/vivant/régénération = gate dur ; finalité
(usage_non_marchand + intérêt général) = gate doux ; co-gate du travail = gate dur
à **proxy unidirectionnel** (seul un `non` constaté ferme ; le silence ne bloque pas).
Sommet toujours vide, mais *vide-atteignable*.

**Mini-strat salariat (2ᵉ passe #10)** — trace `audit/mini-strat-salariat-10/`. Le
co-gate du travail est **refondé** : `non_subordination` → `travail_non_marchandise`.
Il teste la **forme salariale** (décommodification du travail, Polanyi), non la
subordination ni la propriété du capital. Clivage = « y a-t-il un rapport salarial ? » :
SCOP/coopérative qui salarie = `non` (pas d'exception ESS) ; don/troc/entraide,
bénévolat, associé·es sans contrat (GAEC) = `oui` ; cœur/support = `non`/`partiel`.
Autogestion créditée à l'axe 3 (Indice), pas au sommet. Option B (pas de 2ᵉ face
« sortie » ; domination sans salaire = limite assumée en prose). Intégré (grille,
moteur, doctrine, méthode) ; distribution inchangée.

**À arbitrer avant exécution** (synthèse §3) : 5ᵉ cas-pivot magazine (NDDL chargé vs
Mhotte/Berquet) · réversibilité du verdict (droit de réponse du porteur) · retrait
des résidus « pas un jugement de valeur » (A4).

**Exécution** (à venir) : big-bang en lots MARS-prod parallèles (L7/L12), aperçu L9
systématique, Checker centralisé. Chantiers A3, A4, B1-B4, C, D1 sous une seule
direction, contenu frais. Déploiement (push des commits en attente) groupé ici.

### Clôture

Revue MARS-strat 3 voix (profil-type capitalisé) une fois Phase B atterrie —
cadence carnet L-meta-4 (6 mois / 10 commits). Question de routine L-meta-1 :
dérive doc/pratique MARS ?

---

## 4. Ce que ce document ne rouvre pas

- Le **contenu** de la doctrine #9 (résolu).
- Les **3 tensions** (tranchées).
- La **spec A1** sur le fond (turnkey ; seules ses décisions §7 sont à arbitrer).
- La qualification des chantiers orthogonaux (A2, B1-B3, C, D — tiennent).

---

*Fin du pilotage phase 2. À tenir à jour à chaque franchissement de précondition.*
