# Validation corpus #11 — Passe 2 (re-validation post-vague corrective)

Checker MARS-prod, méthode améliorée (7 contrôles ajoutés passe 1), lecture seule,
2026-06-01. Lot : `porteurs/` (27), `usufruitiers/` (47), `reseaux/` (9),
`modeles/` (5). Référentiels : `config/grilles.yml`, `config/concepts.yml`.

Objet : confirmer la résolution des bloquantes/mineures de la passe 1 et traquer
les résidus selon les contrôles ajoutés (complétude de chaîne ; articulations ;
rôles↔prose ; cohérence pôle↔nature ; intégrité référentielle ; note↔valeur ;
uid trompeur).

---

## BLOQUANTES — aucune

Les 4 bloquantes de la passe 1 sont **toutes résolues**, et aucune nouvelle
n'apparaît.

- **coop-du-tilleul** (B1) — RÉSOLUE. La fiche assume désormais une forme
  confirmée : `forme_juridique: "Association loi 1901"` est cohérent avec le corps
  (RNA W473002310, SIREN 829556232, déclarée le 01/04/2017), recoupé au registre
  des associations (juin 2026). Les notes de `personne_morale_civile: oui` et
  `parts_non_cessibles: oui` confirment l'asso 1901 ; `pieces.statuts.note` dit
  « Forme confirmée ». Plus de contradiction en-tête↔corps. Pôle `ig_institue`
  cohérent avec `nature_interet: non_lucrative`.

- **exploitation-loiseliere** (B2) — RÉSOLUE. Pôle passé de `mutualisme` à
  `ig_institue` ; `nature_interet: privee_individuelle`, `forme_juridique: null`.
  Le commentaire `integrite_montage` explicite le raisonnement (fermier individuel
  sous porteur hors-marché, pas de mutualisme de sociétaires). Aligné sur la
  fiche-sœur `exploitation-maraichere-la-chaudeau` (même nature, même pôle).

- **commune-flocques** (lot porteurs) — RÉSOLUE. `categorie: porteur`, grille
  porteur complète (18 critères porteur, dont `inalienabilite`, `nature_protectrice`,
  `regime_usage_offert`, `securite_usage_offerte`). Rôle correct : commune =
  propriétaire/porteur du sol ; bail emphytéotique 99 ans confié à la Foncière.
  `autogestion_usagers: non` avec la justification « porteur public » de la grille.

- **fonciere-chenelet** — RÉSOLUE. `categorie: usufruitier`, grille usufruitier,
  preneuse emphytéotique (bâtit/gère les murs sans détenir le sol). Rôles
  porteur/usufruitier désormais corrects (commune porteur / Foncière usufruitier),
  l'inversion de la passe 1 est corrigée. Le lieu `logements-chenelet-flocques`
  porte un bloc `montage.articulations` structuré (bail_emphyteotique, 99 ans) et
  `chaine: {porteurs: [commune-flocques], usufruitiers: [fonciere-chenelet]}`.

- **earl-du-chemin-neuf** (nouvelle fiche) — COHÉRENTE. `nature_interet:
  exploitation_agricole`, pôle `mutualisme`, SIREN 488246521 (Pappers), forme
  « EARL — société civile » assumée. Citée en prose ET en `chaine.usufruitiers`
  ET en `montage.articulations` de `villarceaux`. La contradiction « société
  commerciale vs civile » de la passe 1 est levée : la fiche dit partout
  « société civile d'exploitation agricole ».

---

## COHÉRENCE PÔLE↔NATURE — règle appliquée, une divergence résiduelle mineure

Le défaut structurant de la passe 1 (table `nature_interet → pôles admissibles`
absente) est en grande partie **réglé en pratique** par harmonisation, sans table
formelle dans la config.

**GAEC (`exploitation_agricole`) → `mutualisme` : règle appliquée uniformément.**
Les neuf GAEC sont désormais tous `mutualisme` (croquants, eyssal, ferme-la-durette,
ptites-berouettes, bergers-de-la-sure, de-la-licorne, du-jointout, de-riglanne,
ferme-du-plaisir). Le `gaec-les-croquants` (M7 passe 1, ex-`ig_institue`) est
corrigé. Les deux EARL (`earl-ferme-de-magnantru`, `earl-du-chemin-neuf`) sont
aussi `mutualisme` — cohérent entre elles.

**Fermiers/exploitants individuels sous porteur → `ig_institue` : règle appliquée.**
Les deux fermiers TDL individuels sont désormais tous deux `ig_institue` (Chaudeau
`privee_individuelle`, Oiselière `privee_individuelle`). L'écart Chaudeau/Oiselière
de la passe 1 est résolu.

**Aucun pôle élevé (commun_citoyen) sur une nature `commerciale`/`privee_individuelle`.**
Vérifié : aucun maillon `privee_individuelle`, `commerciale` ou
`commerciale_encadree` ne porte le pôle de tête `commun_citoyen`.

**Divergence résiduelle (mineure) — `exploitants-brce-cheze-canut`.** Seul maillon
`exploitation_agricole` à porter `ig_institue` plutôt que `mutualisme`. C'est
**défendable** (fiche générique d'« exploitant·es » de forme inconnue, sous un
porteur de **propriété publique** — Eau du Bassin Rennais — donc gouvernance
descendante, comme les fermiers individuels), mais cela crée une exception à la
règle « exploitation_agricole = mutualisme ». La règle opérante semble en réalité :
*GAEC/EARL à associé·es nommé·es → mutualisme ; exploitant générique/individuel
sous porteur public ou foncier → ig_institue*. À expliciter dans la config pour
être traçable (sinon le classement paraît au cas par cas).

**Maillons `inconnu` portant un pôle.** `collectif-gasnerie` et `collectif-aubascule`
(nature `inconnu`) portent `commun_citoyen` ; `societe-civile-bigotiere` (`inconnu`)
porte `mutualisme`. Non bloquant : `nature_interet` (lucrativité) et pôle
(gouvernance) sont orthogonaux par conception (concepts.yml), et les deux collectifs
marquent explicitement leur pôle « indicatif et provisoire ». Reste un angle mort
assumé et signalé dans chaque fiche.

---

## NATURE EARL vs VERDICT VILLARCEAUX — pas de tension, cohérent

L'`earl-du-chemin-neuf` est lue `exploitation_agricole` **preneuse** (non
détentrice du foncier, porté par la FPH non lucrative). Par la règle du verdict
(concepts.yml), un maillon `exploitation_agricole` preneur sous porteur hors-marché
**plafonne le lieu à `hybride`**, sans le rendre `marchand`. La fiche `villarceaux`
applique exactement cela : `non_lucratif_global: partiel` et `montage_non_commercial:
partiel` (notes explicites « non commerciale au sens du marché, mais lucrative pour
ses associé·es… la prudence retient un montage partiellement non commercial, non un
montage marchand »). **Pas de tension** : l'EARL en `exploitation_agricole` est
cohérente avec un Villarceaux **hybride** (et non marchand), conformément à la
demande de contrôle. La fiche EARL elle-même conclut « maillon à intérêt privé qui
plafonne le lieu sous le sommet du commun » — aligné.

Réserve mineure (non bloquante) : l'EARL du Chemin Neuf est mono-gérant (Olivier
Ranke seul cité), ce qui la rapproche du cas « exploitant individuel » (→
ig_institue) plus que du GAEC pluripersonnel (→ mutualisme). Le pôle `mutualisme`
reste défendable (forme société à capital/associés), mais c'est le bord exact de
la règle pôle↔nature évoquée ci-dessus.

---

## INTÉGRITÉ RÉFÉRENTIELLE — résolue

- **clip.yml `membres:`** (M1/M2 passe 1) — RÉSOLUE. `membres: [hautes-planches-
  bretoncelles, la-porcheritz-perche, la-deviation-marseille]` : lieux seuls, les
  trois porteurs doublons (les-donnettes, la-porcheritz, parpaing-libre) retirés.
  Plus de doublon Porcheritz ni de mélange de catégories.
- **Orphelins TDL** (M3 passe 1) — RÉSOLUE. `reseau-terre-de-liens.membres`
  inclut désormais `terre-de-liens-auvergne`, `terre-de-liens-pays-de-la-loire`,
  `fondation-terre-de-liens`, `fonciere-terre-de-liens` : les deux antennes sont
  atteignables dans le graphe.
- **Tous les `membres:` pointent des uid existants** : vérifié pour les 9 réseaux
  (cooperative-oasis, longo-mai, reseau-terre-de-liens, habicoop, federation-cen,
  lurzaindia, clip ; revue-silence et accueil-paysan vides). Aucune cible orpheline.
- **earl-du-chemin-neuf** atteignable (chaine + articulations + voir_aussi de
  villarceaux). `lurzaindia-sca` reste rattaché par son réseau (orphelin de lieu
  assumé, M5 passe 1 — acceptable).

---

## NOTE↔VALEUR & FORME PRÉSUMÉE — résidus traités

- **champs-des-possibles** (M1/M2/M8 passe 1) — RÉSOLU. `personne_morale_civile:
  partiel` (note « coté partiel comme les autres coopératives »), `non_lucrativite_
  effective: partiel` cohérent, `nature_interet: commerciale_encadree`, pôle
  `mutualisme`. Plus d'affirmation « non lucrative ». `localisation:` renseignée
  (Villenauxe-la-Petite / Seine-et-Marne 77). Aligné sur les 5 autres SCIC du corpus.
- **association-keriskis** (M6 passe 1) — RÉSOLU. La coquille « agricool » a
  disparu de la fiche.
- **Formes présumées / uid trompeurs** : `scic-moulinage-de-chirols` énonce en
  clair « SAS… sans statut coopératif (SCIC/SCOP) certifié au registre » (forme
  corrigée dans le corps) ; `fonciere-antidote` énonce « Fonds de dotation ».
  Les **uid** eux-mêmes (`scic-…`, `fonciere-…`) encodent encore une forme
  approximative — résidu cosmétique de nommage, non une erreur de donnée (corps
  corrects). Renommage = chantier générateur/migration, hors fiche.

---

## AUTRES CONTRÔLES — RAS

- **Entités HTML brutes** : aucune (`&amp;`, `&#…`, `&quot;`, `&lt;`, `&gt;`)
  dans l'ensemble du corpus (`grep` sur tous les `*.yml`).
- **Doublons d'uid** : aucun. Les 88 uid du lot (porteurs+usufruitiers+reseaux+
  modeles) sont uniques et chaque uid = nom de fichier.
- **SIREN/RNA** : formats plausibles (9 chiffres / Wxxxxxxxx), plusieurs recoupés
  au registre (passe 1) ; pas de régression.
- **Modèles voisins** (5) : conformes (axes estimés hors grille).

---

## Résidus à porter en chantier (non bloquants, méthode)

1. Formaliser dans la config la règle pôle↔nature (`exploitation_agricole` :
   GAEC/EARL pluripersonnel → mutualisme ; exploitant individuel/générique sous
   porteur public ou foncier → ig_institue) — sinon l'exception
   `exploitants-brce-cheze-canut` et le bord EARL Chemin Neuf restent « au cas par
   cas ».
2. Garde-fou générateur d'intégrité référentielle (uid de `membres:`/`chaine.*`/
   `voir_aussi` existants ; orphelins signalés) — recommandé passe 1, toujours à
   coder.
3. uid trompeurs (`scic-moulinage-de-chirols`, `fonciere-antidote`) : renommer ou
   documenter la convention « uid historique ».
