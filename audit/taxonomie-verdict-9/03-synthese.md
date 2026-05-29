# Synthèse arbitrée — refonte de l'axe `nature_interet` et du verdict

*Session #9, 29 mai 2026. Passe MARS-strat à 4 voix (juriste-économiste,
théoricien·ne des communs, méthodologue de la grille, voix éditoriale-réception),
cycle 2 en réactions croisées. Synthèse de l'orchestrateur. Fusionne l'Étape 0
(tension T-2 sur la position du verdict) et le chantier A1 (piège GAEC). À lire
après les fichiers `01-cycle1/` et `02-cycle2/`.*

---

## 1. Verdict d'ensemble

Convergence forte et stable, sur une architecture qu'aucune voix ne portait
entière au cycle 1. Le cycle 2 (réactions croisées) a fait bouger les quatre
voix sur le même crux — c'est le signe que la friction a été réelle, pas un
faux consensus. La position commune n'est ni la réhabilitation des GAEC (ce que
craignait la posture critique), ni leur maintien en `commerciale` (le bug
actuel) : c'est un **déplacement de l'objet mesuré**.

---

## 2. Le pivot conceptuel — ce qu'on gradue

**Les voix disent** : l'axe ne doit pas graduer *la présence d'argent* ni *la
lucrativité*, mais **la captation de la rente foncière** — l'accès à l'*abusus*
du fonds et la capacité d'en empocher la plus-value (théoricien, §position
révisée ; juriste, qui rattache ses cinq marqueurs C1–C5 à l'*abusus* sous forme
sociétaire, art. 544 c. civ.).

**Conséquence décisive — le caractère relationnel** (point neuf du théoricien au
cycle 1, rallié par les trois autres au cycle 2) : un GAEC **preneur d'un bail**
sur un foncier porté hors-marché ≠ un GAEC **propriétaire** de son foncier. La
même forme juridique a deux rapports opposés à la rente selon sa place dans la
chaîne. Donc la captation **ne se lit pas sur le maillon isolé** — elle se lit
sur la chaîne du lieu.

**Le méthodologue a vérifié dans le code que la donnée existe déjà** : les
articulations de chaîne portent un champ `titre` (`bail rural`, `bail
emphytéotique`… — `concepts.yml` l. 524-532), et `montage_section` détecte déjà
la chaîne intégrée (intersection porteur∩usufruitier, l. 816). La distinction
« détient / preneur à bail » est donc **déjà encodée**. On peut capturer le
relationnel **sans nouveau champ saisi**, en faisant dériver par le générateur
le couple (`nature_interet` du maillon × titre de l'articulation). C'est conforme
au principe L11 (« le verdict se calcule, ne se saisit pas ») et à la source
unique de vérité (la chaîne). Le théoricien a explicitement **retiré** sa demande
d'un `nature_interet` relationnel — il violait la règle d'une seule vérité par
fait.

Formule de convergence : *la nature de l'entité (ses statuts) vit sur le maillon ;
la captation effective du fonds (le titre) vit dans la chaîne ; le générateur
croise les deux.*

---

## 3. L'architecture convergente

Sur ces points, les quatre voix sont d'accord :

1. **Un seul cran `nature_interet` nouveau** (pas cinq comme le proposait le
   juriste au cycle 1, pas deux comme l'éditorial) : une **société civile
   d'exploitation agricole de travail** (GAEC, EARL pluripersonnelle, SCEA
   exploitante) qui *ne détient pas* le fonds, ou le détient sous verrou
   anti-spéculatif vérifié. `commerciale_encadree` est **conservé** tel quel
   (SCIC, SCOP, foncières ESUS, coopératives d'habitants — lucrativité
   disciplinée par verrou d'actif + rendement plafonné + gouvernance 1=1).

2. **Ce cran mappe sur le verdict `hybride`** (option « A2 » du méthodologue),
   plafond `ax2_par_nature` proposé à **40** (entre `commerciale_encadree` 50 et
   `commerciale` 20). Le verdict reste à **3 niveaux** — pas de 4ᵉ verdict
   public nommé (coût de rendu, réouverture du couplage palier×verdict, prose à
   réécrire, pour zéro gain de calcul ; les quatre voix l'écartent).

3. **Le tranchant critique se porte au niveau du LIEU, pas du maillon.**
   `marchand` survit — mais comme verdict de montage, réservé aux chaînes où le
   fonds est réellement captable (structure agricole *propriétaire*, SARL/SAS,
   propriété privée individuelle, sans porteur neutralisant). Les **labels de
   maillon deviennent descriptifs** (« société civile d'exploitation agricole »,
   « lucrativité encadrée ») ; les mots du registre critique (« marchand »,
   « spéculatif », « extractif ») ne touchent jamais un maillon agricole sur
   bail. C'est ainsi que la nuance s'affiche sans embrouiller : montrer la chaîne,
   ne trancher qu'une fois.

4. **La distinction patrimonial / de-travail n'est pas un cran, c'est un
   garde-fou de classement.** La forme *présume* l'objet (GAEC → travail ;
   SCI/GFA → détention) mais ne *tranche* pas : c'est le titre (bail vs
   propriété) qui tranche, réfragable par clause statutaire vérifiée. Une SCI/GFA
   **patrimoniale qui détient** reste `commerciale` (→ `marchand` au lieu) ; elle
   ne monte que sur clause anti-spéculative / bail emphytéotique vérifiés, sinon
   `inconnu`. Critère de tri : **objet (présumé par la forme) × titre (lu sur la
   chaîne) × clause (vérifiée sur statuts, sinon `inconnu`)**.

5. **`inconnu` reste sacré.** On ne classe pas « par marqueurs » d'une façon qui
   exigerait cinq champs absents des fiches (ce qui ferait exploser les
   `inconnu` et rendrait le corpus non-jugeable). Le classement par défaut reste
   piloté par `forme_juridique` ; les marqueurs ne servent qu'à *déplacer* un cas
   documenté.

6. **Label public mobile, `id` interne figé** (L2). Renommer les libellés
   affichés est gratuit (prose) et améliore l'explicabilité (chantier A3) ;
   renommer les `id` testés en dur dans le code (`compute_verdict` l. 1304-1306,
   `_NATURE_ORDRE_PIRE_AU_MIEUX` l. 358, `verifier_chaines` l. 4913) est un churn
   risqué pour zéro gain. On habille, on ne recâble pas les clés.

---

## 4. Conséquence sur le corpus

**Cas Pommiers** (le bug fondateur). Chaîne : Fondation Terre de Liens
(`non_lucrative`) + GAEC des Bergers de la Sure (aujourd'hui `commerciale`).
Le GAEC est preneur d'un **bail rural** sur un foncier porté hors-marché par une
fondation RUP. Après refonte : le GAEC est reclassé en cran exploitation
agricole, *et* la dérivation relationnelle confirme qu'il ne détient pas le
fonds (titre = bail, porteur non lucratif) → **verdict `hybride`** (au lieu de
`marchand`), plafond ax2 de 20 → 40, Indice qui remonte. Le bandeau « Montage
marchand » disparaît.

**Les ~13 fiches `commerciale`** : majorité de GAEC usufruitiers sur bail → la
plupart migrent vers `hybride`. Celles où la structure agricole *détient* son
foncier restent `commerciale` → `marchand` (légitime : capture du fonds).
SARL/SAS, propriété privée individuelle : inchangées (`marchand`). Migration
estimée triviale et atomique (un champ par maillon), mais elle dépend de la
dérivation relationnelle pour ne pas blanchir un détenteur.

---

## 5. Décisions résiduelles — pour conclusion opérateur

La convergence est telle que l'architecture est largement déterminée. Restent
**cinq choix réels** :

- **D1 — Label public du nouveau cran.** Descriptif neutre (« société civile
  d'exploitation agricole ») ou affirmatif (« économie paysanne ») ? Les voix
  s'accordent pour que « économie paysanne » vive *dans la phrase d'explication
  du lieu* (posture assumée, T-2) et non comme étiquette absolue de maillon — le
  label de maillon reste descriptif. À confirmer.

- **D2 — Plafond ax2 du nouveau cran.** 40 recommandé (méthodologue). Ajustable
  (35 / 45) ; effet chiffré seulement visible à la régénération. Peut être
  décidé empiriquement après une première passe.

- **D3 — Périmètre d'implémentation immédiat.** Le correctif minimal (un cran)
  seul *blanchirait à tort* un GAEC propriétaire. La correction juste exige la
  **dérivation relationnelle** (croiser nature × titre dans `compute_verdict` et
  `_pire_nature_chaine`, ~15-25 lignes, fallback gracieux si `articulations`
  absent). Recommandation : implémenter la dérivation, pas seulement le cran.
  Cela fait passer A1 de « effort moyen » à « moyen+ ».

- **D4 — Politique de la civile patrimoniale.** Pour qu'une SCI/GFA détentrice
  monte hors de `commerciale`, on exige une clause anti-spéculative *vérifiée sur
  statuts*, sinon `inconnu`. Accepte-t-on l'effort de recherche par fiche, ou
  laisse-t-on par défaut `commerciale`/`inconnu` (la veille alimentera) ?

- **D5 — Garde-fou nouveau.** Le méthodologue recommande un `verifier_*` qui
  alerte si un GAEC/EARL reste classé `commerciale` sans titre de propriété
  documenté (anti-régression de la frontière au fil du peuplement). À retenir ?

---

## 6. Position de l'orchestrateur (à valider)

Je propose : **adopter l'architecture du §3 en entier**, avec la dérivation
relationnelle (D3) — c'est elle qui fait la justesse, le cran seul ne suffit pas.
Label de maillon descriptif + « économie paysanne » en prose d'explication (D1).
Plafond 40 à confirmer empiriquement (D2). Civile patrimoniale par défaut
`commerciale`, montée sur clause vérifiée, `inconnu` assumé (D4). Garde-fou
ajouté (D5).

**Traçabilité et minorité.** La distinction patrimonial/de-travail était portée
par le juriste presque comme un cran ; elle a été reclassée en garde-fou par le
théoricien (« c'est le titre, pas l'objet, qui commande ») et le méthodologue
(« le relationnel les trie déjà »). Le juriste s'y est rallié en la maintenant
comme *garde-fou anti-blanchiment*, pas comme cran — sa ligne rouge (« ne jamais
qualifier un GAEC de commerciale ; `inconnu` sacré ») est intégrée. Aucune voix
n'est restée sur une position réfutée non documentée.

---

*Fin de la synthèse. La conclusion opérateur déverrouille l'exécution de A1
(refonte effective) puis l'ordonnancement de P2/P3.*
