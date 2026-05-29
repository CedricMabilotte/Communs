# Brief — refonte profonde et totale du site Communs / Terres Libérées

*Brief stratégique autosuffisant, écrit en session #9 (29 mai 2026). Objectif :
permettre une refonte totale du site, dans tous ses aspects, en qualité maximale,
**sans perte de contexte** et avec un **contenu propre et frais, libre de toute
trace de fabrication et de toute lourdeur**. Ce document est conçu pour qu'une
session future puisse repartir de lui seul, sans avoir à reconstituer l'historique.*

---

## 0. Exigence directrice

La refonte visée n'est pas un patch ni une retouche : c'est une **reconstruction
de fond du site entier**, qui prend appui sur la doctrine et le modèle désormais
résolus, et qui produit un contenu public **frais** — débarrassé des cicatrices
internes (numéros de refonte, de session, de chantier, de cycle) et des lourdeurs
accumulées. Prendre le temps d'assurer **cohérence et qualité** avant de produire ;
ne rien lancer tant que les préconditions (§6) ne sont pas réunies.

---

## 1. Entrées canoniques (les inputs propres — où vit le contexte)

Tout ce qu'il faut pour reprendre, sans rien d'autre :

- **Doctrine et théorie** : `audit/refonte-theorique-9/04-cadre-theorique-complet.md`
  — cadre exhaustif (posture, généalogie, définitions, typologies, taxonomies,
  méthodologie, limites, doctrinal vs extension propre). *Candidat énoncé canonique*
  (remplace/étend `brief-cadre-conceptuel-communs.md` après validation).
- **Modèle d'évaluation résolu** : `audit/refonte-theorique-9/03-synthese-comparative.md`
  (synthèse en deux couches + discipline observable-gaté/posture-glose) ; rounds
  amont : `audit/taxonomie-verdict-9/03-synthese.md` (foncier/chaîne) et
  `r2-03-synthese.md` (finalité d'usage).
- **Décisions de cible** (tranchées #9) : public **utilité publique**
  (presse/décideurs/militants, attention grand-public) · verdict = **prise
  éditoriale assumée** · architecture **catalogue + magazine** (hooks dans les
  fiches).
- **Chantiers et priorités** : `audit/revue-editoriale-8d/04-chantiers.md` (15
  chantiers qualifiés, 4 familles, 3 priorités, dépendances) et
  `03-synthese.md` (tensions/convergences).
- **Démarche méta** : `audit/revue-editoriale-8d/06-demarche-phase2.md`
  (MARS-strat pour arbitrer, MARS-prod pour exécuter, lots parallèles L7/L12).
- **Point de reprise** : `etat-projet-communs.md` (où on en est, résolu vs ouvert)
  et `lecons-communs.md` (leçons, dont L38-L40 #9).
- **Mécanique actuelle** : `config/concepts.yml`, `config/grilles.yml`,
  `config/ranking.yml`, `scripts/generate_site.py`.

---

## 2. Principe de contenu frais (le cœur de l'exigence)

Le site public doit être **propre de toute trace de son propre making**. Règles,
érigées en principes (D1 du #8d devient une règle, pas une option) :

- **Zéro trace interne dans le public** : aucune mention de « refonte #3 »,
  « session #N », « chantier #N », « cycle D », « round », « MARS », « 1bis »,
  etc. dans les pages, fiches, slugs, titres, métadonnées. Ces termes vivent
  *exclusivement* dans `audit/`, les fichiers de pilotage et l'historique git.
- **Pas de qualificatifs internes en public** (leçon L32 / anti-pattern A-2 du
  carnet) : un mot de cadrage interne (« puriste », « pilote », « brouillon »)
  ne migre jamais dans un slug ou un titre.
- **Versionnage propre** : version majeure (1.0, 2.0…) et mineure en pied de page ;
  un `changelog.html` public qui résume sans le détail interne ; le journal de
  fabrication reste interne.
- **Statut épistémique déclaré** : le verdict/Indice présenté comme **indicateur
  composite conventionnel** (façon IDH), non comme mesure objective (page méthode).
- **Posture assumée mais non sectaire** : l'étoile polaire (économie citoyenne
  décommodifiée) éclaire le haut sans faire honte aux lieux qui ne l'atteignent
  pas ; « milieu » est honorable, jamais une faute (ligne rouge de l'avocat
  d'Ostrom).
- **Allègement** : prose dépouillée du formel, pas de surcharge ; les fiches
  gagnent une dimension éditoriale (hooks) sans bavardage.

---

## 3. Périmètre d'une refonte totale (tous les aspects)

À traiter de façon cohérente, à qualité maximale :

- **Socle** : page méthode reposée sur le cadre canonique (doctrine, triade
  régénération/maintien/retrait, statut du chiffre, limites assumées) ; assumer
  la posture en accueil (A4, posture politique #8d).
- **Modèle d'évaluation implémenté** (= A1 codé, voir §6) : cran exploitation
  agricole, dérivation relationnelle nature×titre, cran « régénère », co-gates du
  sommet (anti-spéculation, gouvernance formelle, régénération opposable,
  non-subordination par proxy unidirectionnel), glose positive, re-câblage de
  `compute_verdict`, migration du corpus.
- **Fiches** : gabarit refondu (hooks + glose de finalité + sources tierces B3 +
  encart « comment lire verdict×palier×Indice » A3).
- **Carte de France** (B1) des lieux, navigable, mobile.
- **Accueil** (B4) : manifeste + chiffres-clés + entrées clarifiées.
- **Magazine / dossiers** (B2) : 5 fiches-récit cas-pivot, partition claire d'avec
  le catalogue symétrique.
- **Absents structurants** (C1) : ASPAS (lien depuis le corpus), OFS-BRS, SAFER,
  CEN.
- **Diffusion** : OG images (C2), newsletter/réseaux (C3), carrousels glossaire
  conditionnels (C4).
- **Glossaire** reposé sur le lexique du cadre.
- **Revues** (greenwashing, loi 1905, sanctuaires-de-retrait, mémoire) :
  articuler « retrait » avec la triade écologique du cadre.
- **Plan B** (`projetplanb.org`) : surfaces de contact (modèle reproductible ↔ cas
  Communs).

La refonte totale = la réalisation **cohérente et simultanée** des 15 chantiers,
sous une seule direction théorique, plutôt que leur empilement par petites touches.

---

## 4. Sans perte de contexte — chaîne de reprise à froid

Ordre de lecture pour repartir : (1) ce brief ; (2) `04-cadre-theorique-complet.md`
(la doctrine) ; (3) `03-synthese-comparative.md` (le modèle d'éval) ; (4)
`04-chantiers.md` (le quoi) ; (5) `etat-projet-communs.md` §3-4 (où on en est).
Tout le reste (`01-cycle1/`, `02-cycle2/`, rounds) est de la trace justificative,
consultable mais non nécessaire à la reprise.

---

## 5. Méthode recommandée

- **Cadrage** : si des tensions de design subsistent (architecture des trois
  niveaux de lecture, gabarit de fiche), une passe MARS-strat courte ; sinon
  exécuter.
- **Exécution** : lots parallèles partitionnés (L7/L12/L24/L26), un agent par
  lot de fichiers disjoint ; **aperçu HTML autonome L9 systématique** pour tout
  rendu visuel ; **Checker MARS-prod** centralisé en intégration (régénération +
  garde-fous uid/chaînes/entités HTML + cohérence + relecture du rendu).
- **Gel du contenu frais** : produire le public à partir du cadre canonique
  *validé*, en appliquant les règles du §2 dès l'écriture (ne pas nettoyer après).

---

## 6. Préconditions avant de lancer la refonte totale

Ne pas lancer tant que :

1. **A1 est codé et stable** — le modèle d'évaluation doit être implémenté et le
   corpus migré avant de refondre le rendu qui l'expose (sinon on refond sur du
   sable).
2. **Le cadre canonique est validé** (`04-cadre-theorique-complet.md`) et l'énoncé
   canonique migré.
3. **La cible est confirmée** (utilité publique — acquise #9, à reconfirmer si le
   temps passe).
4. **Le principe de fraîcheur (§2) est acté** comme règle de production.

Tant que ces préconditions ne sont pas réunies, la refonte totale reste à l'état
de brief — on avance d'abord sur A1 (exécution) et la validation du cadre.

---

*Fin du brief. Maintenu à jour à chaque avancée significative sur les
préconditions.*
