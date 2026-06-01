# Validation corpus #11 — Passe 1 : porteurs · réseaux · modèles

Checker MARS-prod, lecture seule. Lot : 27 fiches `porteurs/`, 9 `reseaux/`,
5 `modeles/`. Contrôles : cohérence `nature_interet` ↔ forme juridique ↔ source ;
cotation `oui`/`non` non fabriquée ; **forme juridique présumée vs registre** ;
SIREN/RNA plausibles ; orphelins ; entités HTML brutes ; `membres:` des réseaux.
Date : 2026-06-01.

Méthode de vérification registre : deux formes présumées « à risque » (précédent
Chirols) vérifiées par WebSearch sur l'annuaire des entreprises / societe.com —
voir « Vérifications registre effectuées ».

---

## BLOQUANTES

Aucune objection strictement bloquante (forme juridique fausse non corrigée,
cotation fabriquée renversant un verdict, SIREN faux). Le corpus est sain sur
le cœur des contrôles. Les points ci-dessous en « mineures » incluent toutefois
**deux incohérences de cohérence interne `membres:`/catégorie** qui méritent
correction avant prochaine régénération.

---

## MINEURES

### M1 — `reseaux/clip.yml` — `membres:` mélange catégories (lieu + porteur)
- **Problème** : la liste `membres:` contient à la fois des `uid` de **lieux**
  (`hautes-planches-bretoncelles`, `la-porcheritz-perche`,
  `la-deviation-marseille`) **et** des `uid` de **porteurs** (`les-donnettes`,
  `la-porcheritz`, `parpaing-libre`). Or les trois porteurs sont précisément les
  associations propriétaires des trois lieux listés : le réseau référence donc
  deux fois la même réalité, une fois par le lieu, une fois par le porteur.
- **Preuve** : `clip.yml` l. 100-101 ; recoupé avec `lieux/*` (chaine.porteurs)
  — `les-donnettes` ↔ `hautes-planches-bretoncelles`, `la-porcheritz` ↔
  `la-porcheritz-perche`, `parpaing-libre` ↔ `la-deviation-marseille`.
- **Correction** : décider d'une convention `membres:` (lieux seuls, ou entités
  seules) et l'appliquer ; ici, retenir les **lieux** (cohérent avec les autres
  réseaux : `longo-mai`, `reseau-terre-de-liens` listent surtout des lieux) et
  retirer les trois porteurs — ou inversement, mais pas les deux.

### M2 — `reseaux/clip.yml` — doublon « La Porcheritz » dans `membres:`
- **Problème** : `la-porcheritz-perche` (lieu) **et** `la-porcheritz` (porteur)
  figurent tous deux ; en plus du mélange M1, c'est le même site compté deux fois
  dans une liste de ~17 lieux revendiqués, ce qui peut fausser un futur compteur.
- **Preuve** : `clip.yml` l. 100-101.
- **Correction** : ne garder qu'une entrée par site (cf. M1).

### M3 — Orphelins de chaîne : deux antennes TDL + lien réseau
- **Problème** : `terre-de-liens-auvergne` et `terre-de-liens-pays-de-la-loire`
  (porteurs) ne sont **cités par aucune chaîne de lieu** (`chaine.porteurs`) et
  **ne figurent dans `membres:` d'aucun réseau** — y compris
  `reseau-terre-de-liens`, dont la liste `membres:` n'inclut ni les deux antennes
  ni les structures nationales antenne→Foncière/Fondation.
- **Nuance** : c'est **cohérent avec leur nature** — ces antennes ne portent pas
  le foncier (elles l'écrivent elles-mêmes : portage assuré par Foncière SCA /
  Fondation FRUP). L'orphelinat est donc *attendu*, non une erreur de données.
  Mais il rend ces deux fiches **invisibles dans le graphe** : aucun chemin n'y
  mène.
- **Preuve** : grep `terre-de-liens-auvergne|...-pays-de-la-loire` → n'apparaît
  que dans sa propre fiche ; `reseau-terre-de-liens.yml` l. 106 (`membres:`).
- **Correction** : rattacher explicitement les deux antennes au réseau
  `reseau-terre-de-liens` (champ `membres:` ou `voir_aussi:` réciproque), pour
  qu'elles soient atteignables.

### M4 — `la-licorne` : porteur de chaîne ≠ structure citée par l'antenne
- **Problème** : le lieu `la-licorne` déclare `chaine.porteurs: [fonciere-terre-de-liens]`,
  alors que `terre-de-liens-auvergne.yml` présente la Licorne comme « la dernière
  acquise fin 2024 » et la met en `voir_aussi`. À vérifier : le foncier de la
  Licorne est-il porté par la **Foncière** (SCA) ou par la **Fondation** (FRUP) ?
  Une fête d'acquisition 2025 par l'antenne ne tranche pas le porteur national.
- **Preuve** : `lieux/la-licorne.yml` l. 133 ; `terre-de-liens-auvergne.yml`
  l. 25-26, 140.
- **Correction** : confirmer le porteur réel (Foncière vs Fondation) sur la fiche
  ferme TDL et aligner `chaine.porteurs`.

### M5 — `lurzaindia-sca` orphelin de lieu (acceptable, à signaler)
- **Problème** : le porteur `lurzaindia-sca` n'est rattaché à **aucun lieu** ; il
  n'est lié qu'au réseau `lurzaindia` (`membres: [lurzaindia-sca]`) et cité en
  `voir_aussi` par `feve`. Lurzaindia détient ~486 ha sur de nombreuses fermes,
  dont aucune n'est carvée en fiche-lieu.
- **Preuve** : `reseaux/lurzaindia.yml` l. 108 ; grep `lurzaindia-sca`.
- **Correction** : acceptable en l'état (le réseau le rattache) ; à terme, carver
  au moins une ferme Lurzaindia pour incarner la chaîne, ou documenter que c'est
  un porteur « sans lieu carvé » assumé.

### M6 — `nature_interet: inconnu` sur `sc-hameau-des-buis` — bien posé, mais à tracer
- **Problème (léger)** : `sc-hameau-des-buis` porte `nature_interet: inconnu`,
  ce qui est **correct** (société civile dont la non-lucrativité reposait sur la
  détention des parts par une association, sans verrou statutaire propre
  documenté ; structure d'ailleurs dissoute/transformée en SAS coop. en 2023).
  Le `inconnu` est cohérent et non fabriqué. Point de méthode : ce porteur est
  **historique** (remplacé en 2023) mais reste rattaché au lieu `hameau-des-buis`
  comme porteur actif de chaîne — l'état « porteur disparu » n'est pas marqué.
- **Preuve** : `sc-hameau-des-buis.yml` l. 7, 22-25 ; `lieux/hameau-des-buis.yml`
  l. 134.
- **Correction** : signaler dans la fiche-lieu que le porteur de chaîne est le
  montage historique (la SAS coopérative de 2023 n'est pas encore carvée).

### M7 — Cohérence `integrite_montage.niveau` ↔ `nature_interet` (à surveiller)
- **Observation** : plusieurs `commerciale_encadree` portent un
  `integrite_montage.niveau: economie_marchande` (fonciere-chenelet,
  fonciere-terre-de-liens, lurzaindia-sca, feve) tandis que d'autres
  `commerciale_encadree` portent `mutualisme` (scic-coq-a-lame, scic-keruzerh,
  scic-terres-de-sources→`ig_institue`). Ce n'est **pas une erreur** (l'axe
  `nature_interet` et le pôle `integrite_montage` sont orthogonaux par
  conception, cf. `concepts.yml`), mais la frontière `economie_marchande` vs
  `mutualisme` pour des structures toutes `commerciale_encadree` mériterait une
  règle écrite, sinon le classement paraît au cas par cas.
- **Preuve** : comparaison des champs `nature_interet` / `integrite_montage`
  entre fiches foncières (SCA → economie_marchande) et SCIC habitat (→ mutualisme).
- **Correction** : documenter dans `concepts.yml`/`ranking.yml` le critère qui
  distingue le pôle pour deux maillons de même `nature_interet`.

---

## RAS (contrôles passés)

- **Formes juridiques présumées — pas de SCIC/SCOP fabriqué non sourcé.** Les
  formes sociétaires sont nommées avec prudence : la SAS `le-temps-des-possibles`
  est bien dite SAS commerciale (`nature_interet: commerciale`), la
  `sci-terres-ecolectif` bien dite SCI (`commerciale`), la `lurzaindia-sca` bien
  dite SCA. Le cas `scic-moulinage-de-chirols` est **exemplaire** : la fiche a
  explicitement corrigé l'erreur des sources secondaires (« SCOP/coopérative »)
  en SAS commerciale à principes coopératifs, registre à l'appui (BODACC/RNE),
  avec un bloc « POINT DE FORME RÉSOLU ».
- **Cotations `oui`/`non` sourcées.** Les `oui` forts (inaliénabilité du
  Conservatoire du littoral, propriété publique Larzac, FRUP Fondation TDL) sont
  adossés à des faits vérifiables ; les `non` (autogestion_usagers des personnes
  publiques, vivant_finalite des fonds d'habitat) sont argumentés et non
  expéditifs. Les `inconnu` sont employés à bon escient (jamais comblés par défaut).
- **`nature_interet` cohérent avec la forme.** Associations loi 1901 et
  fondations/fonds → `non_lucrative` ; foncières solidaires/SCA/SCIC →
  `commerciale_encadree` ; SAS/SCI patrimoniale → `commerciale` ; SC sans verrou
  documenté → `inconnu`. Aucune incohérence relevée.
- **SIREN/RNA plausibles** (9 chiffres / format Wxxxxxxxx). Plusieurs sont
  explicitement recoupés sur l'annuaire des entreprises (Parpaing Libre 833981764,
  La Porcheritz 810886952 + RNA W751224981 réconciliés, TDL Auvergne 534043351,
  Eau du Bassin Rennais 253502629, Chirols 845026277). La fiche `les-donnettes`
  documente même une **correction de RNA** (W613001811, l'ancien W613001936 étant
  erroné) — bonne hygiène.
- **Entités HTML brutes** : aucune `&amp;`, `&#39;`, `&quot;` etc. trouvée dans
  le lot (apostrophes typographiques et accents UTF-8 propres).
- **`membres:` des réseaux pointant des uid existants** : vérifié pour
  `cooperative-oasis`, `habicoop`, `federation-cen`, `lurzaindia`, `longo-mai`,
  `reseau-terre-de-liens`, `accueil-paysan` (membres vide), `revue-silence`
  (vide) — toutes les cibles existent comme fiches lieux/porteurs/usufruitiers.
  Seul `clip` pose le problème de mélange de catégories (M1/M2).
- **Modèles voisins** (5) : `axes_estimes` est bien marqué comme conversion
  indicative « hors notation par les grilles » (clt-bruxelles, ofs-brs,
  mietshauser-syndikat, stiftung-trias, cooperative-habitants-alur) ; pas de
  grille `oui/non` fabriquée pour ces fiches hors-catégorie.

---

## Vérifications registre effectuées (WebSearch, 2026-06-01)

- **scic-coq-a-lame** (SIREN 903703700) → registre : « Société coopérative
  d'intérêt collectif par actions simplifiée », créée le 13/10/2021, Cellettes.
  → forme `SCIC` de la fiche **CONFIRMÉE**.
- **scic-keruzerh** (SIREN 883723207) → registre : SCIC sous forme « société
  coopérative à forme anonyme », RCS Lorient. → forme `SCIC` **CONFIRMÉE**.
- Les deux SCIC habitat — le type le plus exposé au précédent Chirols (sources
  secondaires labellisant « coopérative » des SAS) — sont donc **réellement** des
  SCIC au registre. Pas de sur-déclaration.

Non re-vérifiés au registre (SIREN présents, formes peu risquées) : les FRUP /
fondations / fonds de dotation (forme cohérente avec source), les antennes
associatives loi 1901 (déjà recoupées annuaire-entreprises dans la fiche), la SAS
le-temps-des-possibles et la SCI ecolectif (formes commerciales déjà assumées).

---

## Manques de méthode

1. **Pas de validation référentielle automatique du graphe** (manque #1). Les
   problèmes M1/M2 (clip mélange lieu/porteur, doublon Porcheritz) et M3/M5
   (orphelins) auraient dû être attrapés par un script : (a) tout `uid` dans un
   `membres:`/`chaine.*`/`voir_aussi` doit exister ; (b) un `membres:` ne doit
   contenir qu'une seule **catégorie** attendue (ou la règle doit être explicite) ;
   (c) tout porteur/usufruitier devrait être atteignable depuis ≥1 lieu OU
   explicitement marqué « sans lieu carvé ». Le générateur valide uid/chaînes/
   entités HTML (cf. CLAUDE.md L9) mais pas la **cohérence catégorielle** ni les
   **orphelins** — à ajouter au garde-fou pré-commit.

2. **Frontière `economie_marchande` vs `mutualisme` non écrite** pour deux
   maillons de même `nature_interet` (M7) : le classement du pôle
   `integrite_montage` repose sur le jugement du carveur, sans règle traçable.

3. **Statut « porteur historique / disparu » non modélisé** (M6, hameau-des-buis) :
   un porteur remplacé reste rattaché comme porteur actif de chaîne, sans champ
   marquant la péremption.

4. **Vérification registre non systématique** : seules 2 formes ont été recoupées
   en direct ici (provenance web_fetch restreinte oblige à passer par WebSearch).
   Une passe registre exhaustive sur les ~10 formes sociétaires du lot reste à
   faire pour clore définitivement le risque « forme présumée ».
