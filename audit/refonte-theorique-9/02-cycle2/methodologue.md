# Cycle 2 — voix méthodologue / gardien·ne de la cohérence du système

*Passe MARS-strat comparative #9, cycle 2 (réactions croisées). J'ai lu les six
voix du cycle 1. Je ne tranche pas le doctrinal (gate-dur vs glose) ; je formalise
la discipline d'encodage qui en découle, je la confronte au code réellement lu
(`compute_verdict`, l. 1290-1314 ; `grilles.yml` v3 ; `concepts.yml` l. 370-431),
et je livre la cartographie taxonomique que l'universitaire réclame. Aucun fichier
de production touché.*

---

## 0. Ce que les autres voix m'ont confirmé, et où j'amende

**Amplifié.** L'empiriste chiffre ce que j'avais posé en principe : sur 45 lieux,
**0 (au plus 1)** atteindrait le sommet renforcé strict, et `usage_non_marchand:
oui` n'apparaît dans *aucune* fiche, même les plus militantes. Ce n'est plus une
crainte de méthodologue : c'est une mesure. Mon « gate dur sur donnée inobservable
= sommet vide par construction » est désormais étayé empiriquement. Le pro-actuel
et l'universitaire convergent indépendamment sur la même ligne α/β. **Le consensus
des voix observables (empiriste, agroécologue sur la régénération active, juriste
cité) est net : ce qui n'est pas lu sur acte/statut/label ne peut pas gater.**

**Pas vu (cycle 1).** Je traitais « gate vs glose » comme un binaire doctrinal
unique. L'agroécologue m'oblige à le **trianguler** : entre le gate dur et la
glose pure, il existe un troisième régime que le code supporte déjà — le **gate
par proxy opposable**. `milieu_protege: oui` (ORE, RVS, RBI, BRE clausé) est
observable *et* opposable ; il peut gater là où « régénération active mesurée » ne
le peut pas. Le crux X-3 vit exactement dans cet interstice. J'avais sous-estimé
qu'on pouvait gater *une face* d'un critère (l'opposable) en laissant l'autre
(le déclaratif) en glose.

**Position révisée.** Je maintiens « le sommet sera vide si gate dur », mais je
reformule ma recommandation : non pas « tout en glose », mais **une discipline de
tri critère par critère** selon trois statuts (gatant-sur-proxy / descriptif-en-glose
/ prose-pure). C'est l'objet du §1.

---

## 1. X-1 — La discipline « gate sur l'observable, glose pour le reste »

Je la formalise comme une **règle de tri à trois statuts**, applicable à tout
critère candidat. Un critère ne peut gater le sommet que s'il passe les trois
tests :

1. **Lisible sur source publique** (acte notarié, statuts déposés, label, registre
   ORE/RVS) — pas sur enquête comptable ni entretien de terrain.
2. **Opposable / non réversible à volonté** — un dispositif que le lieu ne peut pas
   défaire silencieusement (l'inaliénabilité statutaire vaut, l'intention de don
   non).
3. **`inconnu` < ~50 % du corpus pertinent** — sinon il n'allume rien et ne
   *trie* rien : il ne fait que propager des « verdict à établir » (l. 1308-1309).

Qui ne passe pas les trois → **champ descriptif en glose** (saisi dans la grille,
nourrit l'Indice ou l'affichage, *ne touche pas* `compute_verdict`). Qui ne se
saisit même pas proprement → **prose pure** (phrase de posture, hors grille).

### 1.1 Critères neufs qui GATERAIENT le sommet

- **`anti_speculation_statutaire`** (axe 1). C'est le critère le plus solide des
  trois voix observables (empiriste §1, §3 type 5 : « parts au nominal », « fonds
  de dotation sans capital appropriable ») et il est **déjà à 80 % couvert** par
  `parts_non_cessibles` + `irreversibilite` + `clause_devolution`. Passe les trois
  tests. **Gate.** Coût : ~0 critère neuf, on s'appuie sur l'existant ; au plus un
  resserrement de définition de `parts_non_cessibles`.
- **`gouvernance_formelle_collective`** (axe 3). L'empiriste le qualifie de
  « **seul** des cinq lisible sur sources publiques » (une voix, consentement,
  autogestion statutaire). Déjà porté par `gouvernance_collective`,
  `usagers_decident`, `une_voix`, `autogestion_usagers`. Passe les trois tests.
  **Gate** (par sa face *formelle* — pas la gouvernance vécue, invisible).
- **`milieu_protege` (face opposable)** (axe 1). Déjà existant. ORE/RVS/RBI/BRE
  clausé : opposable, public, registrable. **Gate**, mais seulement sur le « oui »
  fort opposable, jamais sur le « oui » déclaratif (agroécologue §2.3, §5).

### 1.2 Critères neufs DESCRIPTIFS en glose (saisis, non gatants)

- **`benefice_non_approprie`** (le « piège GAEC » du pro-renforcé). **Échoue test 1
  et 3** : donnée comptable quasi jamais publique (empiriste §1 : « pas d'obligation
  de dépôt », « aucune fiche ne renseigne »). Saisi en grille → nourrit l'Indice et
  une glose ; *ne gate pas*. Conséquence : le GAEC bio sur bail reste `hybride`
  (verdict via chaîne, round 1), et la glose dit « bénéfice approprié individuellement »
  — la posture est *visible* sans rendre le corpus non-jugeable.
- **`travail_non_salarie`** (Illich, pro-renforcé). **Échoue test 1** : exige les
  contrats internes. Surtout, l'empiriste pose le piège décisif (§1) : l'inférer de
  la forme (GAEC → non-salarié) **rouvre exactement la faille que le round 1 a mis
  des semaines à neutraliser** (inférence forme→nature). Donc → glose pure, *jamais*
  recâblé en gate par la forme. Voir X-2.
- **`regeneration_active`** (agroécologue). **Échoue test 2 et 3** : lente,
  réversible, inobservable en instantané. Sa *face opposable* (`milieu_protege`)
  gate déjà (§1.1) ; sa *face active mesurée* reste descriptive. Voir X-3.

### 1.3 Comment éviter les champs `inconnu` à 95 %

C'est le verrou opérationnel. Trois règles :

- **Réutiliser avant d'ajouter.** Les deux critères gatants neufs sont en réalité
  des *resserrements de définition* de champs existants (§1.1) — donc zéro nouveau
  champ à 95 % `inconnu`, car ces champs sont *déjà* renseignés sur le corpus.
- **Tout champ qui naîtrait `inconnu` > 50 % naît en glose, pas en gate.** Test 3
  ci-dessus. Mécaniquement, un champ majoritairement `inconnu` qui co-gaterait le
  sommet le viderait (l. 1308) ; le même champ en glose ne fait que ne rien
  afficher sur les fiches lacunaires — coût nul.
- **Saisir `partiel`/`inconnu` est sacré** (round 1 §3.5). On n'invente pas de
  « oui » pour habiter le sommet : un sommet rempli de faux-oui est pire qu'un
  sommet vide (il blanchit). L'agroécologue et l'empiriste sont unanimes là-dessus.

---

## 2. X-2 — Non-salariat et non-appropriation : encoder ou prose pure ?

La question est piégeuse parce qu'elle oppose deux invariants. Ma réponse,
**différenciée** :

- **`travail_non_salarie` → prose pure (hors grille).** Raison méthodologique, pas
  doctrinale : la seule façon de le « saisir » serait de l'inférer de la forme
  juridique, et l'empiriste démontre que c'est la faille round 1 réincarnée. Un
  champ qu'on ne peut renseigner *que* par une inférence interdite ne doit pas
  exister dans la grille — il y créerait une tentation permanente de recâblage. Il
  vit dans la phrase de posture (« certains font vivre une économie sans salariat »),
  jamais dans un champ saisi.
- **`benefice_non_approprie` → champ descriptif en glose (dans la grille,
  non gatant).** Différence avec le précédent : *quand* la donnée existe (statuts
  d'une SCIC à réserves impartageables, fondation sans distribution), elle est
  lisible. Le champ est donc légitime, saisissable en `oui/partiel/non/inconnu`,
  majoritairement `inconnu` — mais il nourrit l'Indice (axe 2) et la glose sans
  gater. Il **ne casse pas** « le verdict se calcule » : il alimente un score, pas
  `compute_verdict`.

Règle générale tirée : **on encode (en glose) ce qui est parfois lisible ; on
laisse en prose pure ce qui n'est lisible que par une inférence qu'on s'interdit.**

---

## 3. X-3 — Un cran « régénère » distinct, au-dessus de `usage_non_degradant` ?

L'agroécologue a raison sur un point que je conteste à demi : aujourd'hui
`usage_non_degradant: oui` **fusionne maintien et régénération** (l. 615 :
« pratiques de maintien *ou* de régénération attestées »). Un lieu qui enrichit et
un lieu qui maintient obtiennent le même « oui ». C'est une sous-pondération réelle.

**Faisable ? Oui, à condition de graduer, pas de gater binaire.** Deux options de
coût croissant :

- **Option α (recommandée, ~0 ligne de verdict).** On garde `usage_non_degradant`
  à trois crans (non / maintien=partiel-renforcé / régénère=oui-fort) en raffinant
  *seulement la définition* (l. 606-618), sans nouveau critère. Le « oui-fort
  régénère » s'adosse aux **proxies opposables** de l'agroécologue (diagnostic
  public, suivi pluriannuel, ORE) — donc se confond largement avec `milieu_protege`.
  Pour le **gate du sommet**, on ne change rien : c'est `milieu_protege` (face
  opposable) qui gate, pas le cran déclaratif. La régénération *active* reste en
  glose/Indice.
- **Option β (déconseillée).** Un critère `regeneration_active` distinct qui
  co-gate. Échoue mes tests 2 et 3 (lente, réversible, inobservable → `inconnu`
  massif). Viderait davantage le sommet. Aucun gain de calcul.

**Verdict X-3 : le cran « régénère » est faisable et souhaitable, mais comme
gradation d'un critère existant adossée à proxy opposable — pas comme gate neuf.**
Gate seulement par la face opposable (`milieu_protege`), glose pour la face active.
Cela donne raison à l'agroécologue sur le *manque* (maintien ≠ régénère) et à
l'empiriste sur l'*observabilité* (active = inobservable).

---

## 4. X-4 — Cartographie taxonomique propre (la partie « taxonomies »)

Ce que l'universitaire réclame (items 5, 6, 7), grounded sur le code réel.

### 4.1 Axes (invariant : 5, jamais 6)

| Axe | Domicile (maillon) | Statut renforcé |
|---|---|---|
| 1 Le sol | porteur + lieu | gate du sommet (resserré, §1.1) |
| 2 La structure | `chaine_min` (pire maillon) | plafonné par `nature_interet`, glose enrichie |
| 3 Le pouvoir | usufruitier | gate du sommet (face formelle) |
| 4 La finalité | `chaine_min` | gate du sommet (D-B + IG) |
| 5 L'usage | convention + lieu | gate partiel (face opposable) + glose |

### 4.2 Critères × nature_interet × verdict × paliers × silhouettes

- **`nature_interet`** (saisi sur porteur/usufruitier, l. 370-431) : 6 crans,
  `non_lucrative` → `commerciale_desactivee` → `commerciale_encadree` →
  `commerciale` → `privee_individuelle` → `inconnu`. **Seule donnée saisie qui
  alimente le verdict** ; tout le reste se calcule.
- **`verdict`** (`compute_verdict`, l. 1290-1314) — **3 niveaux, maintenus** :
  1. maillon `commerciale`/`privee_individuelle` → `marchand` ;
  2. sinon `commerciale_encadree` → `hybride` ;
  3. sinon maillon `inconnu` → `None` (« à établir ») ;
  4. sinon → `sanctuaire` **si** `foncier_hors_marche==oui ET irreversibilite==oui
     ET vivant_finalite==oui ET place_au_vivant==oui`, sinon `hybride`.
  Le gate renforcé = **étendre la condition (4)** avec
  `gouvernance_formelle_collective==oui` (axe 3) et `milieu_protege==oui` (face
  opposable, axe 1). ~10-15 lignes. Aucun nouveau niveau, aucun nouveau champ saisi
  hors grille.
- **Paliers** (5) : `abouti` (≥70, `requiert_verdict: sanctuaire`), `solide` (64),
  `engage` (50), `partiel` (35), `eloigne` (0). Couplage `palier_for` × verdict
  inchangé : resserrer le gate du sommet resserre mécaniquement l'accès à `abouti`,
  sans nouveau code de palier.
- **Silhouettes de montage** (`concepts.yml`, `montages`) : **descriptives, jamais
  jugeantes** — invariant. Le renforcé n'y touche pas ; le jugement reste dans
  `nature_interet` + verdict.

### 4.3 Statut d'évaluation des critères renforcés (la colonne neuve)

| Critère renforcé | Source | Gate / glose / prose | Champ |
|---|---|---|---|
| Foncier hors-marché irréversible | acte, statuts | **gate** | existant |
| Anti-spéculation statutaire | statuts | **gate** | `parts_non_cessibles` (resserré) |
| Gouvernance collective (formelle) | statuts | **gate** | existant axe 3 |
| Milieu protégé (opposable) | ORE/RVS/BRE | **gate** | `milieu_protege` |
| Habitat du vivant (D-B) | charte, activité | **gate** | existant axe 4/5 |
| Intérêt général | objet statutaire | **gate** | existant axe 4 |
| Régénération active | déclaratif/diagnostic | **glose** (Indice) | `usage_non_degradant` gradué |
| Non-appropriation du bénéfice | comptes (rares) | **glose** (Indice) | `benefice_non_approprie` neuf |
| Don / troc / non-marchand | déclaratif | **glose** | `usage_non_marchand` existant |
| Besoins monétaires collectivisés | enquête | **prose pure** | — |
| Non-salariat | inférence interdite | **prose pure** | — |

Cette colonne est la **réponse opérationnelle à l'item 7** de l'universitaire (la
méthodologie d'observation manquante) et trace l'item 9 (emprunté/observable vs
posture affirmée).

---

## 5. Coût et invariants (inchangés vs cycle 1, confirmés)

Nouveaux axes : **0**. Champs saisis neufs : **1** (`benefice_non_approprie`, en
glose). Lignes `compute_verdict` : **+10-15** (étendre la condition 4 avec deux
gates *déjà renseignés*). Verdict : **3 niveaux**. Couplage palier×verdict :
inchangé. Source unique : intacte (le verdict ne lit que la chaîne + critères de
grille déjà existants). **« Le verdict se calcule » : respecté** — aucun des
champs glose/prose ne le touche. Risque `inconnu` : **neutralisé** par la règle
test-3 (rien à >50 % `inconnu` ne gate).

---

*Fin cycle 2 — méthodologue. La discipline X-1 n'est pas « gate vs glose » mais un
tri à trois statuts ; elle laisse le doctrinal (jusqu'où la posture pèse) à
l'opérateur tout en garantissant que le sommet reste habitable et calculable.*
