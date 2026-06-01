# Validation corpus #11 — Passe 1 — Lieux a–l

Checker MARS-prod (lecture seule). Lot : 36 fiches `lieux/[a-l]*.yml`.
Grille `config/grilles.yml` v3 ; canon `config/concepts.yml`. Date : 2026-06-01.

Méthode appliquée : extraction programmatique de tous les blocs `montage`,
`chaine`, `grille` et `integrite_montage` des 36 fiches ; vérification chaîne
(articulations ⊆ chaine ; uid existants ; titres/natures du canon ; `integre`
réservé entité-unique) ; relecture des cotations `oui`/`non` sensibles contre
la prose et le bloc `fiabilite` ; recoupement des articles de revue citant ces
lieux. Pas de modification.

---

## BLOQUANTES

### B1 — `logements-chenelet-flocques` · schéma + chaîne · bloc `montage.articulations` absent
- **Problème.** La fiche est de type `propriete_protegee` mais ne porte AUCUN
  bloc `montage.articulations` (seule fiche du lot dans ce cas avec
  `gorges-du-gardon`, qui est un classement réglementaire sans démembrement).
  Le bail emphytéotique de 99 ans (commune → Foncière Chênelet) n'existe qu'en
  prose, jamais structuré.
- **Preuve.** `python3` dump du bloc montage : `articulations` absent ; clés
  présentes = `type`, `description` uniquement. Prose (l.29-38) : « bail
  emphytéotique de 99 ans ».
- **Correction suggérée.** Ajouter
  `articulations: [{usufruitier: <maillon>, titre: bail_emphyteotique, duree: "99 ans"}]`
  cohérent avec le rôle retenu (cf. B2).

### B2 — `logements-chenelet-flocques` · désync factuelle · rôles porteur/usufruitier inversés vs prose
- **Problème.** La prose (l.29) affirme « **La commune de Flocques est
  propriétaire du terrain** » et l'a confié à la Foncière par bail
  emphytéotique ; la commune récupère les murs au terme. Le terrain (le sol
  inaliénable, public) est donc tenu par la commune — rôle de porteur du
  foncier au sens du canon (« détient la nue-propriété / la propriété
  sanctuarisée du foncier »). Or `chaine` déclare
  `porteurs: [fonciere-chenelet]` / `usufruitiers: [commune-flocques]` —
  **l'inverse**. La Foncière n'a que les murs, par emphytéose (position de
  preneur = usufruitier).
- **Preuve.** l.139-140 (`chaine`) vs l.29-32 (prose) et l.49
  (`foncier_hors_marche` note : « Le terrain reste propriété de la commune »).
- **Correction suggérée.** Soit inverser la chaîne (porteur = commune-flocques,
  usufruitier = fonciere-chenelet), soit, si le choix « la Foncière porte les
  murs » est délibéré, l'expliciter dans le commentaire de montage et aligner
  l'articulation. À trancher par l'opérateur — le verdict calculé (hybride 56)
  peut bouger selon le maillon retenu comme limitant.

---

## MINEURES

### M1 — `ecolieu-de-la-gasnerie` · `integrite_montage.niveau` sur-classé
- **Problème.** `niveau: commun_citoyen` (pôle de référence, le sommet) alors
  que toute la colonne « sol/structure » est cotée `inconnu` (foncier non
  documenté, holder non confirmé) et que le verdict calculé est **suspendu**
  (idl 36, palier « Libération partielle »). Apposer le pôle de tête à un
  montage entièrement non documenté contredit le principe de réserve honnête.
- **Preuve.** grille `foncier_hors_marche=inconnu`, `non_lucratif_global=inconnu`,
  `montage_non_commercial=inconnu` ; verdict_label « Verdict suspendu » (site).
- **Atténuation.** Le commentaire dit déjà « ce niveau est indicatif et
  provisoire » — la réserve EST présente en prose. Mineure pour cela.
- **Correction suggérée.** Rétrograder le `niveau` à un pôle neutre tant que le
  montage n'est pas établi (ou prévoir une valeur `provisoire`/`inconnu` pour ce
  champ), pour que le radar ne porte pas le label « commun libre et vivant ».

### M2 — `loiseliere` & `les-petites-berouettes` · `integrite_montage.niveau: mutualisme` douteux
- **Problème.** Le pôle `mutualisme` désigne (concepts.yml) un régime
  COMMERCIAL à sociétariat fermé (SCIC/coop). Or ces deux lieux sont des fermes
  Terre de Liens (`propriete_protegee`), porteur = SCA à actionnariat solidaire
  (`commerciale_encadree`), usufruitier = exploitation individuelle
  (`loiseliere` : `privee_individuelle`) ou GAEC (`berouettes` :
  `exploitation_agricole`). Le label `mutualisme` (entraide entre sociétaires)
  colle mal au profil réel ; `economie_marchande` ou `ig_institue` selon la
  lecture seraient plus justes.
- **Preuve.** `usufruitiers/exploitation-loiseliere.yml` nature_interet =
  `privee_individuelle` ; commentaires d'intégrité (SCA actionnariat solidaire +
  GAEC/exploitant privé).
- **Correction suggérée.** Réexaminer le `niveau` éditorial de ces deux fiches
  au regard de la nature réelle de la chaîne. (Champ display only — n'affecte
  pas le verdict calculé.)

### M3 — `logements-chenelet-flocques` · cotation `foncier_hors_marche=oui` conflate terrain et murs
- **Problème.** La note justifie le `oui` par « le terrain reste propriété de
  la commune » ET « les murs sont portés par la Foncière… hors revente ». Le
  terrain (public, inaliénable de fait) est solide ; les murs sont portés par
  une SAS ESUS (`commerciale_encadree`) dont l'encadrement statutaire de cession
  est « non documenté » (cf. note `parts_non_cessibles=partiel`). Coter `oui`
  plein là où un maillon est une société commerciale au verrou non établi est
  un peu généreux ; `partiel` serait défendable.
- **Preuve.** l.47-49 vs l.59-61.
- **Correction suggérée.** Soit maintenir `oui` en restreignant la note au
  terrain communal, soit passer `partiel`. Mineure (n'inverse pas le verdict).

---

## RAS (vérifié, conforme)

- **Chaîne / uid.** Tous les uid de `chaine` existent dans `porteurs/` ou
  `usufruitiers/`. Les cas `archipel-de-la-vallee`, `ecolieu-de-la-gasnerie`,
  `gorges-du-gardon`, `jardin-petit-pessicart`, `la-bigotiere` déclarent le même
  uid en porteur ET usufruitier (entité-unique / `integre`) ; l'entité existe
  dans un seul dossier — conforme au cas entité-unique. (Voir Manque #1.)
- **Titres d'articulation.** Tous dans le canon (`bail_rural`,
  `bail_emphyteotique`, `bail_a_construction`, `convention`, `integre`).
  `integre` n'apparaît que sur des chaînes porteur=usufruitier (gasnerie,
  archipel, pessicart, bigotière) — réservation respectée.
- **Entités HTML brutes.** Aucune dans les sources YAML (a-l) ; l'échappement
  du site généré (`&#x27;`, `&#x2011;`) est correct, côté template.
- **Désync revue Pommiers — RÉSOLUE.** `revues/greenwashing/.../01` cite
  `ferme-de-pommiers` et son corps annonce « hybride, autour de 65 sur 100, au
  palier montage solide » ; la fiche live calcule exactement verdict=hybride,
  idl=65, palier « Montage solide ». Synchronisé (changelog v3 du 2026-05-31).
  Aucun autre article du corpus ne porte de `cas_illustratifs` chiffré citant
  un lieu a-l (les articles loi-1905, mémoire, sanctuaires-de-retrait sont
  thématiques, sans verdict/Indice cité).
- **Cotations sensibles — globalement saines.** Sur l'échantillon `oui`/`non`
  des critères `milieu_protege`, `vivant_finalite`, `place_au_vivant`,
  `usage_non_degradant`, `travail_non_marchandise`, `irreversibilite`,
  `foncier_hors_marche` : les notes justifient par un fait sourcé (ORE signée à
  L'Aube et la Mhotte ; classement RNR aux Gorges du Gardon ; BRCE au captage
  Chèze-Canut ; biodynamie/agroforesterie attestée pour les `usage_non_degradant`
  ; salariat constaté pour les `travail_non_marchandise=non` de la Mhotte,
  Rayol, Éveils, Demain-en-Main). Les `inconnu` sont posés honnêtement quand la
  source manque (gasnerie sol entier `inconnu`). Pas de `oui`/`non` fabriqué
  détecté.
- **Réserves honnêtes.** Les lieux fragiles (gasnerie, l-aube, hameau-des-buis,
  bigotière) portent leurs réserves en `fiabilite` et en cotations `partiel`/
  `inconnu`, sans `oui` abusif sur un sol non établi.

---

## Manques de méthode (à ajouter au skill `valider`)

1. **#1 — Contrôle `articulations` obligatoire pour `propriete_protegee` /
   `propriete_publique` / `demembrement`.** Le cas Flocques (B1) est passé parce
   que rien ne vérifie qu'une fiche à montage dissocié porte au moins une
   articulation structurée. Ajouter un garde-fou : tout type ≠
   `propriete_privee_*` et ≠ `propriete_collective`-intégrée DOIT avoir
   `montage.articulations` non vide, et chaque `articulation.usufruitier` ∈
   `chaine.usufruitiers`. (Mon check « articulations ⊆ chaine » n'attrape pas
   l'ABSENCE d'articulations.)

2. **#2 — Croiser le sens des rôles porteur/usufruitier avec la prose.** B2
   (rôles inversés) n'est détectable que par lecture : « qui possède le sol ? ».
   Heuristique semi-automatique : repérer dans `montage.description` /
   `resume` les patrons « propriétaire du terrain/foncier/sol » + nom, et
   alerter si l'entité nommée propriétaire du SOL est rangée en `usufruitiers`
   plutôt qu'en `porteurs`. À défaut d'auto, l'inscrire comme point de
   relecture obligatoire.

3. **#3 — Cohérence `integrite_montage.niveau` ↔ verdict calculé / natures de
   chaîne.** M1 et M2 (pôle éditorial sur-classé ou mal-assorti) ne sont pas
   contrôlés. Règle : un `niveau: commun_citoyen` est interdit si le verdict est
   suspendu ou si un maillon de chaîne est `inconnu` ; un `niveau: mutualisme`
   suppose un maillon SCIC/coopératif effectif dans la chaîne. Ajouter une table
   de compatibilité niveau↔chaîne au garde-fou.

4. **#4 — Résolution des uid `integre` à travers les DEUX dossiers.** Le check
   d'existence d'uid doit chercher dans `porteurs/` ∪ `usufruitiers/` pour les
   chaînes entité-unique (porteur==usufruitier), sinon il produit de faux
   positifs « uid absent » (5 cas dans ce lot).
