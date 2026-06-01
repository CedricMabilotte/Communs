# Validation corpus #11 — Passe 2 (re-validation) — Lieux (49)

**Checker MARS-prod, méthode améliorée (7 contrôles passe 1) — lecture seule.**
Lot : les 49 fiches `lieux/*.yml`. Grille `config/grilles.yml` v3 ; canon
`config/concepts.yml`. Verdicts recalculés via `scripts/generate_site.py`
(`compute_verdict`). Date : 2026-06-01.

Objet : confirmer que les corrections de la vague corrective ont tenu, traquer
les résidus. La vague corrective n'est **pas encore committée** (working tree) ;
le dernier commit est « validation corpus passe 1 ». Les fiches non modifiées par
la vague gardent donc leur état d'avant.

---

## BLOQUANTES

Aucune bloquante résiduelle sur les deux fiches-cibles de la passe 1.

### Confirmé résolu — `logements-chenelet-flocques` (pass 1 B1 + B2)
- `montage.articulations` désormais **présent** : `usufruitier: fonciere-chenelet`,
  `titre: bail_emphyteotique`, `duree: "99 ans"`. ✓
- Rôles **corrigés** : `chaine.porteurs: [commune-flocques]` (porteur du sol
  public, inaliénable de fait) / `chaine.usufruitiers: [fonciere-chenelet]`
  (preneur du bail = position d'usufruitier). Conforme à la prose et au canon. ✓
- Entités dans la bonne famille : `commune-flocques` créée dans `porteurs/`,
  `fonciere-chenelet` (SAS ESUS, `commerciale_encadree`) dans `usufruitiers/`. ✓
- Articulation ⊆ chaîne : OK. Verdict recalculé = **hybride** (la
  `commerciale_encadree` plafonne, la commune est `non_lucrative`) — cohérent.

### Confirmé résolu — `villarceaux` (pass 1 B1 + B2)
- L'**EARL du Chemin Neuf** est désormais dans `chaine.usufruitiers` ET dans
  `montage.articulations` (`titre: convention`), avec entité dédiée
  `usufruitiers/earl-du-chemin-neuf.yml` (`nature_interet: exploitation_agricole`,
  forme « EARL — société civile »). ✓
- Les deux notes jadis contradictoires sont **alignées** : `montage_non_commercial`
  et `travail_non_marchandise` qualifient toutes deux l'EARL de « société civile
  d'exploitation agricole ». La contradiction « commerciale vs civile » a disparu. ✓

---

## MINEURES

### m1 — `villarceaux` : tension prose ↔ verdict calculé (sanité du verdict — point 2)
- **Le verdict calculé est bien `marchand`**, et il est **cohérent avec les
  règles** : l'EARL est `exploitation_agricole`, mais reliée à la fondation par
  un `titre: convention`. `convention` n'est pas dans `_BAIL_TITRES_SECURISES`
  (`bail_rural`, `bail_emphyteotique`, `bail_reel_solidaire`,
  `bail_a_construction`) → décision #10 : preneur non sécurisé → l'EARL est lue
  comme `commerciale` → la chaîne devient `marchand`. La nature de l'EARL est donc
  correcte ; c'est le **titre précaire** qui fait basculer en marchand.
- **Réserve à signaler.** La note de `montage_non_commercial` (valeur `partiel`)
  argumente explicitement « la prudence retient un montage partiellement non
  commercial, **non un montage marchand** » — alors que le verdict *calculé*, lui,
  est marchand. La fiche se contredit donc entre sa cotation manuelle (`partiel`,
  qui vise hybride) et le verdict automatique (marchand). De plus, le titre est
  noté « non documenté publiquement » : le `marchand` repose entièrement sur le
  défaut prudent `convention`. Si une source établissait un bail rural,
  villarceaux passerait à hybride. **À trancher par l'opérateur** : soit assumer
  marchand et réaligner la prose de la note, soit, si l'usage est en réalité un
  bail sécurisé, corriger le titre de l'articulation. Mineure (le calcul est
  défendable en l'état), mais la fiche envoie deux signaux opposés au lecteur.

### m2 — Incohérence de pôle inter-fiches `mutualisme` ↔ `ig_institue` (point 3 — la plus structurante)
Le canon réserve `mutualisme` à un maillon **SCIC / coopérative / SCOP**
(`commerciale_encadree`, sociétariat fermé, lucrativité réelle mais plafonnée).
La vague corrective a posé deux règles divergentes (ferme TDL à exploitant
individuel = `ig_institue` ; GAEC = `mutualisme`) — et elle ne les a **pas
appliquées uniformément**. Sur le même type de montage « foncière solidaire
(SCA/FEVE, `commerciale_encadree`) + exploitation agricole
(`exploitation_agricole`) » :

| lieu | chaîne (natures) | pôle posé | touché par la vague ? |
|---|---|---|---|
| `riglanne` | SCA + **GAEC** | **mutualisme** | non |
| `les-petites-berouettes` | SCA + **GAEC** | **ig_institue** | oui |
| `la-durette` | SCA + **GAEC** | **ig_institue** | non |
| `magnantru` | FEVE + EARL | ig_institue | non |
| `ferme-de-pegarou`, `ferme-du-plaisir-sazilly`, `ferme-eyssal`, `le-jointout`, `la-licorne` | SCA/encadrée + agricole | ig_institue | (entités GAEC touchées) |

→ **`riglanne` est seul à porter `mutualisme` sur un montage SCA+GAEC** que toutes
les autres fermes équivalentes classent `ig_institue`. La règle « GAEC =
mutualisme » n'a été appliquée qu'à riglanne, alors que berouettes/la-durette (GAEC
aussi) sont restées `ig_institue`. **Incohérence directe** : même montage, pôle
différent. Recommandation : trancher une règle unique (le pôle dominant du corpus
pour « foncière solidaire + exploitation agricole » est `ig_institue`) et aligner
riglanne — `mutualisme` y est de toute façon mal fondé (le GAEC n'est pas une
SCIC/coop).

Trois autres `mutualisme` mal fondés (tous **non touchés** par la vague) :
- **`archipel-de-la-vallee`** : chaîne = deux maillons `commerciale_desactivee`
  (SCI à intérêt privé *désactivé*, 100 % aux mains d'organismes IG). La
  désactivation rapproche du pôle non lucratif, pas du `mutualisme` (qui suppose
  une lucrativité de sociétariat réelle). Pôle mal assorti.
- **`ecolectif`** : chaîne contient un maillon `commerciale` (SCI Terres
  d'Écolectif), verdict **marchand**. `mutualisme` sur une chaîne marchande à
  lucrativité ouverte sous-décrit le profil (plutôt `economie_marchande`).
- **`hameau-des-buis`** et **`la-bigotiere`** : maillon foncier de nature
  `inconnu` (société civile, statuts non confirmés), aucun SCIC/coop établi.
  `mutualisme` est **fabriqué** : il affirme un régime de sociétariat coopératif
  qu'aucune source n'établit. Pôle à rétrograder vers une valeur neutre tant que
  la forme n'est pas confirmée.

### m3 — uid trompeur résiduel : `fonciere-antidote` (fonds de dotation) — pass 1 M2 non résolu
`porteurs/fonciere-antidote.yml` (chaîne de `maison-blanche-antre-toit`) porte un
uid préfixé « foncière » alors que la `forme_juridique` est « Fonds de dotation
(loi du 4 août 2008) » et le `nom` « Antidote ». Le fond est juste, seul l'uid
ment. (Le pendant pass 1 `scic-moulinage-de-chirols` semble avoir été traité — il
n'apparaît plus au contrôle de préfixe.) Cosmétique au rendu (uid non affiché),
mais piège pour le prochain carveur. À renommer `fonds-antidote`.

### m4 — `tera` : maillon foncier réel (SCI Le Tilleul) hors chaîne (classe villarceaux pass 1, en plus discret)
La prose et toutes les notes établissent que le foncier est porté par la **SCI Le
Tilleul**, « dont le fonds de dotation SDH détient **la majorité** des parts ».
La chaîne déclare pourtant `porteurs: [fonds-sdh]` (le seul actionnaire
majoritaire, `non_lucrative`) — la SCI elle-même (société civile à parts
cessibles, détenue à *majorité* et non à 100 % par un organisme IG, donc **non**
`commerciale_desactivee` au sens strict du canon : seuil = 100 %) n'est pas un
maillon de la chaîne. La chaîne sous-estime donc la lucrativité (verdict calculé
hybride, mais reposant sur `fonds-sdh` non_lucrative au lieu de la SCI réelle).
La passe 1 (lot m-z) avait classé tera RAS en saluant une « simplification assumée
en prose » ; à la relecture stricte du contrôle « complétude de chaîne », c'est le
même schéma que villarceaux — un maillon nommé en prose, absent de la chaîne. Les
notes `partiel` atténuent, mais le maillon foncier n'est ni entité ni dans la
chaîne. À arbitrer (créer l'entité SCI Le Tilleul + l'ajouter, ou documenter
explicitement le choix de représenter la chaîne par l'actionnaire).

### m5 — `tera` : dépendance à une correction hors-lot (`coop-du-tilleul`)
`coop-du-tilleul` est désormais déclarée « Association loi 1901 » / `non_lucrative`
(entité touchée par la vague). Or la passe 1 (lot usufruitiers, bloquante #3)
avait signalé cette forme comme **fabriquée** (« en-tête Association loi 1901
contredit par le corps »). Si la correction de l'entité a bien établi la forme,
RAS ; sinon, une forme `inconnu` y suspendrait le verdict de tera. À confirmer
côté lot usufruitiers (hors de mon lot, mais affecte le verdict de tera).

---

## RAS (vérifié, conforme)

- **Complétude de chaîne (les deux sens).** Sur les 49 lieux : aucune
  `articulation.usufruitier` hors `chaine` ; aucun usufruitier de chaîne pendant
  sauf cas légitimes. `gorges-du-gardon` sans articulation = **légitime**
  (classement réglementaire RNR, pas de démembrement — confirmé en prose).
- **Intégrité référentielle.** Tous les uid de `chaine` (porteurs + usufruitiers)
  existent comme fichiers d'entité ou de lieu. Zéro orphelin de référence.
- **Entités HTML brutes.** Aucune dans les sources YAML (49 lieux + entités) ;
  le contrôle générateur final confirme « aucune anomalie ».
- **Notes ↔ valeurs.** Aucune contradiction réelle détectée. Les `oui` des
  critères sensibles (vivant, usage, travail) restent adossés à un fait sourcé ;
  les `inconnu` sont posés honnêtement. (Les `travail_non_marchandise=oui` des
  GAEC contiennent le mot « non » dans « société civile… » mais la note justifie
  bien le `oui` — faux positifs d'heuristique.)
- **Désync verdict / article de revue — RÉSOLUE.** `revues/greenwashing/.../01`
  cite `ferme-de-pommiers` = hybride, ~65/100, « montage solide » ; la fiche live
  calcule bien **hybride**. Aucun autre article ne cite un verdict chiffré pour un
  lieu du lot.
- **Pôles dominants cohérents.** Hors les cas m2, les `ig_institue` (fondation /
  public + non lucratif ou agricole encadré) et `commun_citoyen` (chaînes
  entièrement `non_lucrative`, montages collectifs autogérés : keriskis,
  ferme-du-berquet, hautes-planches, la-deviation, maison-blanche) sont
  correctement assortis à leur chaîne.
- **Générateur.** Tourne sans erreur fatale ; 137 fiches générées. Deux
  signalements non fatals **pré-existants** (worklist chantier D, non introduits
  par la vague) : `ecolieu-la-filerie` sans porteur en chaîne (foncier non établi) ;
  `scic-terres-de-sources` orphelin (en `voir_aussi` de captage-cheze-canut, pas
  en chaîne). À traiter hors de cette passe.

---

## Recommandation de garde-fou (méthode passe 2 → 3)

La seule famille d'objections qui subsiste est le **pôle éditorial
`integrite_montage.niveau`**, non contrôlé par le générateur. Confirme le besoin,
déjà identifié en passe 1, d'une **table `nature_interet (de la chaîne) → pôles
admissibles`** appliquée en garde-fou : elle aurait attrapé riglanne (GAEC ≠
mutualisme), archipel (désactivée ≠ mutualisme), ecolectif (marchand ≠
mutualisme), hameau-des-buis et la-bigotiere (inconnu ≠ mutualisme), et la
discordance riglanne ↔ berouettes/la-durette.
