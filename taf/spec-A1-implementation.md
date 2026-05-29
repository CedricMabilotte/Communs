# Spec d'implémentation A1 — refonte du modèle d'évaluation

*Spec autosuffisante écrite en session #9 (29 mai 2026) pour coder à la prochaine
session. Implémente le modèle résolu par les 3 passes MARS-strat. Aucun code ni
fiche n'a été modifié en #9 : tout est ici. Lire avant :
`audit/refonte-theorique-9/03-synthese-comparative.md` (la résolution) et
`04-cadre-theorique-complet.md` (la doctrine). Code de référence lu et cité avec
n° de ligne (générateur au 29 mai ; revérifier les n° avant d'éditer).*

---

## 0. Invariants à préserver (non négociables)

- **L11** : le verdict se calcule, ne se saisit jamais.
- **Source unique de vérité = la chaîne** ; ne jamais réinférer un régime depuis
  la seule forme juridique (faille du round 1).
- **Verdict à 3 niveaux** : `marchand` / `hybride` / `sanctuaire`. Pas de 4ᵉ.
- **`inconnu` sacré** : valeur par défaut jamais fabriquée ; un maillon `inconnu`
  empêche le sommet.
- **Garde-fous** existants verts après refonte : unicité uid, cohérence chaînes,
  entités HTML, cohérence dates revues.
- **L9** : tout changement de rendu → aperçu HTML autonome (CSS inliné) livré pour
  revue. Le badge de Pommiers change → aperçu obligatoire.
- **Atomicité** : config + générateur + migration corpus cohérents *en un seul
  lot*, sinon les garde-fous mentent (L14).

---

## 1. Changements `config/concepts.yml`

### 1.1 Nouveau cran `nature_interet` — `exploitation_agricole`

Insérer dans la liste `nature_interet:` (après `commerciale_encadree`, avant
`commerciale`) :

```yaml
  - id: exploitation_agricole
    label: "Société civile d'exploitation agricole"
    definition: >
      Société civile de travail agricole — GAEC, EARL pluripersonnelle, SCEA
      exploitante — dont les associé·es vivent du produit de leur travail sur la
      terre, sans détenir le fonds (preneurs d'un bail sous un porteur hors-marché)
      ou en le détenant sous verrou anti-spéculatif vérifié. Lucrative pour ses
      associé·es (appropriation du bénéfice d'exploitation), mais non spéculative
      sur le foncier et non commerciale au sens du marché ouvert.
    en_clair: >
      Des paysan·nes qui vivent de leur ferme sans pouvoir revendre la terre :
      une économie de travail, pas une société de marché — mais le revenu reste
      individuel.
```

Décision de wording (D1 round 1) : le **label de maillon reste descriptif**
(« société civile d'exploitation agricole ») ; le terme **« économie paysanne »**
ne vit que dans la prose d'explication du lieu, jamais comme étiquette absolue.

### 1.2 Bloc `verdict:` — mettre à jour la prose de la règle

Réécrire `verdict.regle` pour refléter : (a) `exploitation_agricole` → au plus
`hybride` ; (b) la dérivation relationnelle (un maillon agricole *détenteur* ou
*intégré* est lu `commerciale` → `marchand`) ; (c) les co-gates du sommet (vivant
+ régénération opposable + non-subordination + finalité). Texte indicatif à
rédiger lors du codage, fidèle au §2 ci-dessous.

---

## 2. Changements `config/ranking.yml` + ordre des natures

### 2.1 `plafonds_chaine.ax2_par_nature`

Ajouter `exploitation_agricole: 40` (entre `commerciale_encadree: 50` et
`commerciale: 20`). Valeur **à confirmer empiriquement** à la régénération
(fourchette 35-45).

### 2.2 `_NATURE_ORDRE_PIRE_AU_MIEUX` (generate_site.py l. 358-361)

Insérer `exploitation_agricole` entre `commerciale` et `commerciale_encadree`
(ordre du plus restrictif au moins, cohérent avec les plafonds 20 < 40 < 50) :

```python
_NATURE_ORDRE_PIRE_AU_MIEUX = [
    "privee_individuelle", "commerciale", "exploitation_agricole",
    "commerciale_encadree", "commerciale_desactivee", "non_lucrative", "inconnu",
]
```

---

## 3. Changements `scripts/generate_site.py` — `compute_verdict` (l. 1290-1314)

C'est le cœur. La fonction actuelle lit les maillons à plat (porteurs +
usufruitiers) et ne regarde pas les articulations. La v2 doit (a) dériver la
nature *effective* de chaque maillon agricole selon sa place dans la chaîne, puis
(b) appliquer les co-gates du sommet.

### 3.1 Dérivation relationnelle (nature × titre)

Constantes : `BAIL_TITRES = {"bail_rural", "bail_emphyteotique",
"bail_reel_solidaire", "bail_a_construction"}` (vocabulaire `titres` de
concepts.yml l. 313-339 ; `convention`/`commodat` à arbitrer — plutôt usage
précaire, ne pas créditer comme bail sécurisé).

Pour un maillon de nature `exploitation_agricole` :
- lire les `montage.articulations` (l. 796) → `titre` de ce maillon comme
  usufruitier ;
- `integr = set(porteurs) & set(usufruitiers)` (chaîne intégrée, déjà détecté
  l. 816) ;
- `porteurs_hors_marche` = tous les porteurs ∈ {`non_lucrative`,
  `commerciale_desactivee`, `commerciale_encadree`} ;
- **nature effective** :
  - si le maillon est **intégré** (détient) OU **n'a pas** de titre `BAIL_TITRES`
    OU les porteurs **ne sont pas** hors-marché → effective = `commerciale`
    (capte le fonds → `marchand`) ;
  - sinon (preneur d'un bail sous porteur hors-marché) → effective =
    `exploitation_agricole` (usage sans captation → plafonné à `hybride`).

Les autres natures gardent leur valeur.

### 3.2 Verdict depuis les natures effectives

```
si une effective ∈ {commerciale, privee_individuelle} → "marchand"
sinon si une effective ∈ {commerciale_encadree, exploitation_agricole} → "hybride"   # cap, jamais sommet
sinon si une effective == inconnu → None   # à établir
sinon (chaîne entièrement non_lucrative / commerciale_desactivee) → candidate au sommet : voir 3.3
```

`exploitation_agricole` plafonne donc à `hybride` (l'appropriation du bénéfice
d'exploitation interdit le sommet — décision doctrinale #9), exactement comme
`commerciale_encadree`.

### 3.3 Co-gates du sommet (`sanctuaire`)

Le sommet n'est atteint que si la chaîne est pure (3.2 dernier cas) **ET** toutes
les conditions observables suivantes sont vraies (lues sur la grille de la fiche,
comme l'actuel `g.get(...)` l. 1311) :

1. **Foncier** (existant) : `foncier_hors_marche == "oui"` ET
   `irreversibilite == "oui"`.
2. **Vivant** (existant) : `vivant_finalite == "oui"` ET `place_au_vivant == "oui"`.
3. **Régénération opposable** (NEW gate, face opposable seulement) :
   `milieu_protege == "oui"` (ORE/RVS/RBI/RNR/BRE/libre évolution attestée).
   → Voir §4.3 : décision « réutiliser `milieu_protege` » vs « nouveau critère
   `regeneration` ».
4. **Finalité** (round 2, gate doux) : `usage_non_marchand in {"oui","partiel"}`
   ET `usage_interet_general == "oui"`.
5. **Non-subordination** (NEW gate, proxy unidirectionnel — §4.1) :
   `non_subordination == "oui"`. Un `"non"` (salariat/hiérarchie constaté)
   empêche le sommet ; `inconnu`/absent empêche aussi (défaut prudent), jamais
   réinféré de la forme.

Si une de ces conditions n'est pas remplie (ou `inconnu`) → `hybride`. Aucune ne
peut produire `marchand` : elles ne touchent que le passage hybride→sanctuaire.

### 3.4 Signature

`compute_verdict(fiche, by_uid)` a déjà accès à `fiche.montage`. Lire les
articulations depuis `fiche.get("montage",{}).get("articulations")`. Gérer la
**dégradation gracieuse** : si `articulations` absent (cf. l. 809-812), un maillon
`exploitation_agricole` sans titre documenté tombe par défaut côté prudent →
effective `commerciale` (ne pas créditer un usage non documenté) — à arbitrer vs
laisser `exploitation_agricole` (plus généreux). **Décision ouverte** (§7).

---

## 4. Nouveaux critères de grille

### 4.1 `non_subordination` (GATE du sommet, proxy unidirectionnel) — NEW

- Axe 3 (pouvoir/gouvernance), poids à fixer (3, cohérent avec `autogestion_usagers`).
- Valeurs : `oui` (non-salariat + absence de hiérarchie de commandement
  documentés) / `non` (salariat ou hiérarchie constaté) / `inconnu` (défaut).
- **Unidirectionnel** : seuls `oui` documenté et `non` constaté sont fiables ;
  l'absence = `inconnu`. Ne jamais déduire de la forme.
- Gate le sommet (§3.3.5).

### 4.2 `benefice_non_approprie` (GLOSE, descriptif) — NEW

- Axe 2 (structure) ou 3, poids faible. Valeurs oui/partiel/non/inconnu.
- Comptable, rarement public → **ne gate pas**, nourrit l'Indice et la glose.

### 4.3 Régénération — DÉCISION à prendre (§7)

Option (a) : réutiliser `milieu_protege` comme face opposable de la régénération
(0 critère neuf). Option (b) : nouveau critère `regeneration` (oui = rend plus
qu'il ne prélève, attesté par dispositif opposable ; gradué ; AB reste
« maintien », jamais « régénère »), au-dessus de `usage_non_degradant` qui
plafonne au maintien. L'agroécologue recommande (b) pour ne pas confondre
maintien et régénération. **À trancher.**

### 4.4 Glose de finalité (affichage) — `render_fiche`

Sous le verdict, une **glose positive** dérivée (ne s'allume qu'au positif, se
tait sur le banal) : ex. *Terre libérée · ferme nourricière en circuit court* ;
*Terre libérée · économie du don et du partage*. Jamais le mot « marchand » au
niveau maillon. Wording : voir `r2-03-synthese.md` §4 et la voix éditoriale.

---

## 5. Plan de migration du corpus

1. **Recenser** les fiches porteur/usufruitier de forme GAEC/EARL/SCEA exploitante
   (≈ 19 GAEC + 6 EARL repérés en #9) → passer leur `nature_interet` de
   `commerciale` à `exploitation_agricole`. Ne PAS toucher les SCI/GFA
   patrimoniales (détention) : elles restent `commerciale` sauf clause
   anti-spéculative vérifiée (sinon `inconnu`).
2. **Vérifier les titres** : pour chaque lieu dont la chaîne contient une
   exploitation agricole, s'assurer que `montage.articulations[].titre` est
   renseigné (bail_rural / emphyteotique…) — sinon la dérivation §3.1 tombe en
   défaut prudent. Compléter les titres manquants sur sources.
3. **Renseigner** `non_subordination` et `benefice_non_approprie` là où c'est
   documenté ; `inconnu` partout ailleurs (ne pas fabriquer).
4. **Régénération** : selon décision §4.3.
5. **Régénérer** le site, contrôler les garde-fous, produire les aperçus L9.

Effet attendu : Pommiers (GAEC Bergers de la Sure, preneur bail rural sous
Fondation TDL non_lucrative) → effective `exploitation_agricole` → `hybride`
(quitte `marchand`), plafond ax2 20→40, glose *ferme nourricière en circuit
court*. Les ~13 fiches `commerciale` : majorité de GAEC sur bail → `hybride` ;
celles où l'agricole détient → restent `marchand`.

---

## 6. Garde-fous et vérification

- **Nouveau garde-fou `verifier_*`** (recommandé par le méthodologue) : alerter si
  un maillon GAEC/EARL reste `commerciale` sans titre de propriété documenté
  (anti-régression de la frontière au peuplement).
- **Écart grille / fiche À LEVER (trouvaille #9)** : `config/grilles.yml` définit
  pour l'axe 5 des critères (`regime_usage_offert`, `securite_usage_offerte`)
  *différents* de ceux que portent les fiches et que lit `compute_verdict`
  (`usage_non_marchand`, `usage_interet_general`, `vivant_finalite`,
  `place_au_vivant`, `milieu_protege`). **Avant de gater sur ces critères**,
  vérifier qu'ils sont présents et fiables sur les 45 lieux (grep), et réconcilier
  la définition de grille avec les critères réellement saisis (sinon un gate
  s'appuie sur une donnée absente → `inconnu` massif).
- **Checklist post-refonte** : garde-fous verts · distribution verdict/palier
  recalculée (combien de marchand→hybride ? combien de sommets ?) · aperçus L9 de
  Pommiers + 2-3 lieux à chaîne agricole + 1 candidat sommet · cohérence
  `_NATURE_ORDRE` ↔ plafonds ↔ `compute_verdict`.

---

## 7. Calibrages et décisions — TRANCHÉS en session #10

Principe directeur (validé #10) : **A1 ne tranche que le mécanique strictement
nécessaire, avec des choix réversibles s'appuyant sur de l'observable déjà peuplé.
Tout ce qui opérationnalise finement un concept, peuple le corpus ou engage la voix
éditoriale est renvoyé à la Phase B** (carrosserie + mini-strat différée). Cf.
`taf/pilotage-phase2.md`.

**À coder dans A1 (moteur) :**

1. **Plafond `exploitation_agricole` = 40**, marqué **provisoire** (molette de
   calibrage, pas position doctrinale ; re-réglable en voyant la distribution).
2. **Régénération → option (a)** : réutiliser `milieu_protege` comme face opposable
   du gate du sommet. Pas de critère gradué neuf, pas de passe de peuplement.
3. **Défaut de dérivation absent → prudent** (`commerciale`). Ne pas créditer le
   non-documenté ; une fiche prudente se promeut plus tard quand le bail est sourcé.
4. **`convention`/`commodat` → non** (usage précaire). Seuls les 4 baux de
   `BAIL_TITRES` sécurisent la dérivation. Desserrer plus tard reste trivial.
5. **`non_subordination`** : seul critère-gate neuf du moteur (poids provisoire 3).

**Renvoyé à la Phase B (cadres profonds / éditorial — NE PAS coder en A1) :**

- **Option (b)** : critère gradué `regeneration` (maintien/régénère/retrait articulé
  à la triade écologique du cadre #9). À poser avec la mini-strat Phase B.
- **`benefice_non_approprie`** : glose comptable, ne gate pas, rarement public —
  aucune urgence moteur.
- **Glose positive d'affichage** (§4.4) : voix éditoriale = carrosserie. A1 change le
  badge (Pommiers `marchand`→`hybride`, automatique) ; la ligne de glose vient avec
  le gabarit de fiche refondu.
- **Renommage public de `sanctuaire`** : décision d'affichage différée.

---

## 8. Effort estimé

Générateur : ~15-25 lignes nettes (compute_verdict + constantes), conforme à
l'estimation du méthodologue. Config : ~3 ajouts. Migration corpus : ~25-30
fiches touchées (un champ ou deux chacune), atomique. Aperçus L9 : 3-4 pages.
Vérification : la passe Checker post-refonte est la partie longue. Demi-journée à
une journée selon la décision §4.3 et l'état des titres dans les fiches.

---

*Fin de la spec A1. Turnkey pour la session de codage.*
