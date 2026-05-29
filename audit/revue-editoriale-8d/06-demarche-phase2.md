# Démarche de phase 2 — pilotée par les deux modes MARS

*Session #9, 29 mai 2026. Démarche de réalisation des 15 chantiers de phase 2
issus de la revue éditoriale #8d (`03-synthese.md`, `04-chantiers.md`), pilotée
par une combinaison explicite de MARS-strat et MARS-prod. Validée par l'opérateur
(séquencement (a) retenu). À lire après `04-chantiers.md`.*

*Protocoles de référence : `resources/shared/protocoles-mars/` (workspace agents) —
`README.md`, `mars-strat/SKILL.md`, `mars-prod/SKILL.md`, `carnet-mars-strat.md`.*

---

## 0. Mise à jour — session #9 (l'Étape 0 a débordé en refonte doctrinale)

L'Étape 0 (arbitrage des tensions) a déclenché, via la mini-strat A1 fusionnée
avec la T2, **trois passes MARS-strat** qui ont mené à une **refonte de la
doctrine d'ancrage** du projet (du couple Ostrom/droit des biens/ESS vers le
ré-encastrement polanyien). Conséquences sur la démarche :

- Les **3 tensions #8d sont tranchées** (utilité publique · prise éditoriale
  assumée · catalogue+magazine) — l'Étape 0 est close.
- **A1 n'est plus « moyen+ » mais une refonte majeure** : il implémente le modèle
  d'évaluation résolu (cran exploitation agricole, dérivation relationnelle
  nature×titre, cran « régénère », co-gates du sommet dont la non-subordination,
  glose, re-câblage de `compute_verdict`, migration corpus, aperçu L9).
- Un **cadre théorique exhaustif** a été produit (`audit/refonte-theorique-9/04-cadre-theorique-complet.md`),
  qui fait largement la matière du chantier A5 (socle conceptuel).
- Un **horizon de refonte totale du site** est posé et préparé
  (`taf/brief-refonte-totale-site.md`), avec préconditions : A1 codé, cadre
  canonique validé, principe de contenu frais (D1 érigé en règle).

La logique générale de la démarche (MARS-strat arbitre, MARS-prod exécute en lots
parallèles, Checker en intégration) est inchangée et confirmée à grande échelle
(≈ 30 sous-agents sur les 3 passes, sans collision).

---

## 1. Idée centrale

Les deux modes MARS se répartissent selon les deux natures du travail de phase 2 :

- **MARS-strat** sert à *trancher ce qui est ouvert* — un one-shot à angles
  pluriels, par friction organisée entre profils hétérogènes. Il a déjà produit
  la moitié « conception » en #8d (les 15 chantiers + les 3 tensions). Il reste
  à le mobiliser pour les arbitrages d'identité non tranchés (Étape 0), pour les
  rares chantiers qui cachent une vraie divergence (Étape 2), et pour la revue
  de clôture (Étape 4).
- **MARS-prod** sert à *produire fiablement ce qui est déjà cadré* — boucle
  Assistant↔Checker + discipline de mémoire STM/LTM à oubli sélectif. C'est le
  mode d'exécution de chaque chantier.

La méthode des sous-agents parallèles partitionnés (L7/L12/L24/L26, éprouvée
jusqu'à 20 agents simultanés) reste le **substrat d'exécution**. MARS-prod ne la
remplace pas : il pose la boucle réflexive par-dessus. Concrètement, le **Checker**
est l'intégration centralisée déjà pratiquée en clôture — régénération du site,
garde-fous (unicité des uid, cohérence des chaînes, entités HTML), plus les
contrôles propres au chantier, plus l'**aperçu HTML autonome (L9)** obligatoire
pour tout chantier touchant au rendu visuel.

Formulé autrement : **MARS-strat conçoit et arbitre** (le *quoi* et *dans quel
ordre*) ; **MARS-prod exécute et vérifie** (le *comment*, sans erreur silencieuse).

---

## 2. Les cinq étapes

### Étape 0 — Arbitrer les 3 tensions structurantes (verrou partiel)

La synthèse #8d (`03-synthese.md` §3) a proposé des positions d'orchestrateur
mais a laissé la décision à l'opérateur sur trois tensions qu'aucun arbitrage
technique ne résout :

1. **Public-cible prioritaire à 12 mois** — académique / presse-décideurs /
   grand-public-militant (§3.1).
2. **Position du verdict chiffré** — outil méthodologique / prise éditoriale /
   hook viral (§3.2).
3. **Architecture** — catalogue symétrique / magazine éditorialisé / rendu unique
   actuel (§3.3).

**Point capital : seuls P2 et P3 dépendent de ces décisions.** Le P1 (A1, A2, B1,
A3, D1) est robuste à l'arbitrage — A1 (piège GAEC) est prioritaire quelle que
soit la cible. On peut donc lancer P1 *pendant* que les tensions mûrissent ; il
suffit de les avoir tranchées avant P2.

**Sous-processus en trois temps** (choix opérateur, session #9) :

1. *Tour avec l'opérateur* — déroulé de chaque tension avec ses branches et leurs
   conséquences concrètes sur le projet ; l'opérateur réagit, donne ses
   inclinations. Sortie : un cadrage resserré de ce qui reste réellement ouvert.
2. *Approfondissement MARS-strat* — calibré par le tour. L'objet étant « quelle
   identité/cible le projet se donne », les profils pressentis sont des
   **voix-scénarios** (le Communs-académique, le Communs-presse, le
   Communs-grand-public) qui poussent chacune sa branche à ses conséquences
   ultimes et stress-testent l'inclination du tour. Variante du cycle 2 décidée
   à ce moment (red-team unique si l'inclination est déjà nette après le tour,
   réactions croisées sinon — règle L-meta-2 du carnet). Profils exacts fixés
   *après* le tour.
3. *Conclusion opérateur* — décision tracée, qui déverrouille l'ordre de P2/P3.

### Étape 1 — Exécuter P1 sous MARS-prod, en vagues parallèles partitionnées

Boucle, par chantier :

- *Cadrer (User)* — écrire le critère de succès depuis le « Périmètre » du
  chantier + les garde-fous attendus.
- *Agir (Assistant)* — sous-agents sur chantiers/fichiers disjoints.
- *Vérifier (Checker adversarial, centralisé)* — régénération, garde-fous,
  contrôles propres au chantier, aperçu L9 pour les chantiers visuels.
- *Corriger + consolider* en LTM (`lecons-communs.md`).

Découpage respectant les dépendances de `04-chantiers.md` :

- **Vague 1** (sans dépendance amont) : A1 ∥ A2 ∥ B1 ∥ D1.
- **Vague 2** : A3 (après A1, pour ne pas expliquer une mécanique qu'on va changer).

### Étape 2 — Mini-MARS-strat ciblés sur les chantiers à arbitrage caché

Pas partout — seulement quand la réponse n'est pas vérifiable mais
politique/éditoriale. Quatre candidats :

- **A1** — plafond exact du GAEC (« décision d'orientation politique » selon
  #8d). *Traité en amont, indépendant de l'Étape 0* (cf. §3).
- **A4** — reformulation du déni de jugement (divergence universitaire/journaliste
  réelle).
- **B2** — choix des 5 cas-pivot + voix éditoriale.
- **B4** — manifeste d'accueil + chiffres-clés à mettre en avant.

A1 excepté, ces mini-passes dépendent de l'arbitrage de l'Étape 0.

### Étape 3 — Exécuter P2 puis P3 sous MARS-prod

Même boucle qu'à l'Étape 1, dans l'ordre fixé par l'arbitrage de l'Étape 0,
dépendances tenues : C1 après A1+A2 ; B2 après A1+D1 ; B4 après A1+D1+B1 ;
C3 après B4+B2.

### Étape 4 — Revue MARS-strat de clôture

Une fois P1+P2 atterris. Le `carnet-mars-strat.md` fixe la cadence (tous les
6 mois ou 10 commits significatifs — L-meta-4). On reprend le profil-type
« revue éditoriale 3 voix » déjà capitalisé pour vérifier que la revue #8d a été
*effectivement traduite* et faire remonter la nouvelle dette. Plus la question de
routine L-meta-1 : la phase a-t-elle révélé une dérive entre la documentation
MARS et sa pratique ? Si oui, passe MARS-prod (Checker) sur le SKILL.md concerné.

---

## 3. Séquencement retenu — (a)

Deux passes stratégiques sont en amont de l'exécution : l'Étape 0 (tour → strat →
conclusion) et la mini-strat A1. Séquencement **(a)** retenu par l'opérateur :

**Étape 0 d'abord** (on règle l'identité du projet), **puis** mini-strat A1,
**puis** exécution P1. Rationnel : on sait *pour qui* on répare le piège GAEC
avant de le réparer. (L'option (b) — A1 d'abord en parallèle du tour — était plus
rapide vers une première correction visible, mais moins cohérente.)

---

## 4. Vue d'ensemble — routage mode × chantier

| Phase | Chantiers | Mode dominant | Arbitrage préalable |
|---|---|---|---|
| Étape 0 | les 3 tensions | tour opérateur → MARS-strat → conclusion | **verrou pour P2/P3** |
| Mini-strat A1 | A1 (plafond GAEC) | MARS-strat ciblé → MARS-prod | après Étape 0 (séquencement a) |
| P1-v1 | A1, A2, B1, D1 | MARS-prod ∥ | A1 attend la mini-strat |
| P1-v2 | A3 | MARS-prod | après A1 |
| P2 | A4, C1, B2, B3, C2 | MARS-prod, avec strat sur A4 et B2 | Étape 0 |
| P3 | A5, B4, C3, C4, D2 | MARS-prod, avec strat sur B4 | Étape 0 |
| Clôture | re-audit | MARS-strat (3 voix) | après P1+P2 |

---

## 5. Le liant mémoire

À chaque clôture de boucle MARS-prod :

- **LTM projet → `lecons-communs.md`**, avec **purge sélective** des suspens
  résolus. Le backlog de suspens (#5 → #8d) est volumineux ; il se vide à mesure
  que les chantiers ferment — c'est explicitement du travail d'oubli sélectif
  (Ebbinghaus), pas un effet de bord.
- **Leçons-méta sur la conduite des passes → `carnet-mars-strat.md`** (additif,
  partagé entre projets).

La table de routage des SKILL.md tranche les cas limites (erreur opérationnelle
d'un projet → LTM projet ; apprentissage sur la conduite d'une session MARS →
carnet partagé).

---

## 6. Notes de cohérence relevées en ouverture de #9

- Le dossier `revue-editoriale-8d/` n'a **pas** de `05-lecons-meta.md` alors que
  le skill MARS-strat le prévoit. Les leçons-méta ont bien été promues au carnet
  (L-meta-4, L-meta-5 citent #8d), mais le fichier de trace manque. À créer
  rétroactivement ou à acter comme volontairement omis.
- `routine-fin.md` câble déjà une passe Checker MARS-prod en clôture de session
  (étape 6). L'Étape 1 de cette démarche s'y branche naturellement.

---

*Fin de la démarche de phase 2.*
