# Mini-strat « travail décommodifié » — synthèse (cycle 3)

*Session #10, 29 mai 2026. Passe focalisée ouverte sur une remarque de fond de
l'opérateur. Cycle 1 : 3 voix (`01-cycle1/`), dont la voix Autonomie/Illich en
posture red-team explicite — le contradictoire est donc dans le cycle 1, la
synthèse suit (pas de cycle 2 séparé : la friction adverse était déjà portée).
Convention : « les voix » = traçable ; « **orchestrateur** » = à valider.*

---

## 1. Constat partagé — la thèse de l'opérateur est fondée et adoptée

Les trois voix convergent : le co-gate du travail doit tester la **marchandisation**
(le travail vendu comme marchandise sur un marché du travail), **non la
subordination**. Une autorité librement choisie ne marchandise aucun travail
(décommodification) ; confondre les deux mélangeait Polanyi (économique) et Illich
(autonomie). Le **clivage opérant** n'est pas salarié/non-salarié au sens du droit
social, mais **employeur externe ou non**.

**Nom du critère** : `travail_non_marchandise` (libellé « Travail non marchandisé —
hors salariat de marché »). Écartés : `non_salariat` (faux-ami — classerait mal la
SCOP), `travail_decommodifie` (anglicisme). Le nom dit ce qu'il gate (la
marchandisation polanyienne) et s'aligne sur le lexique « non marchand » de la grille.

**Table de cotation** (voix méthodologue/juriste, accord de la voix décommodification) :

| Cas | Valeur | Raison |
|---|---|---|
| (a) salariat de marché, employeur externe au commun | **`non`** (ferme le sommet) | travail loué/marchandisé |
| (b) SCOP / auto-rémunération collective (associé·es-salarié·es sans employeur externe) | `oui` | salaire = répartition interne, pas un marché du travail |
| (c) associé·es non-salarié·es (GAEC, EARL, société civile) | `oui` | vivent du produit, pas de salaire |
| (d) bénévolat / entraide / don de travail | `oui` | hors marché |

Réserve : une SCOP/coopérative qui **embauche des salarié·es non-associé·es** loue,
elle, du travail externe → `non` sur ce point. Jamais déduit de la forme juridique ;
proxy **unidirectionnel** hérité (seul un `non` constaté ferme ; absence = `inconnu`).
Mécaniquement **inerte aujourd'hui** (0/45 fiche cotée, 0 sommet, 0 verdict changé) —
c'est un raffinement doctrinal préparatoire.

## 2. La tension structurante — faut-il une 2ᵉ face « hiérarchie sans sortie » ?

La voix **Autonomie/Illich** montre ce que « salariat seul » laisse passer :
l'**hétéronomie sans salaire**. Cas le plus mordant : une **communauté de partage
intégral dominée par un leader (gourou, dérive sectaire)** — 0 salarié, don/troc —
soit *exactement* le profil que le sommet valorise. Sous « salariat seul », elle
passe le co-gate du travail et peut atteindre le sanctuaire. Autres cas : corvée /
bénévolat obligatoire, travail domestique genré non rémunéré.

Sa proposition, qui **ne contredit pas la thèse mais l'opérationnalise** : le
« librement choisi » de l'opérateur a un test observable — le **droit de sortie
opposable**. Une autorité qu'on *ne peut pas quitter* n'est pas librement choisie.
D'où un co-gate à **deux faces, toutes deux unidirectionnelles et constatées** :
(i) salariat de marché constaté = `non` ; (ii) hiérarchie de commandement
**irréversible** constatée (pas de droit de sortie) = `non`. Absence = `inconnu`,
jamais déduite. Elle refuse explicitement d'en faire un test d'autonomie
psychologique inobservable.

La voix **décommodification** renvoie au contraire ces cas à la **glose/prose**
(hors-champ, inobservables), pour garder le critère pur.

**Position de l'orchestrateur (à valider)** : adopter la **2ᵉ face étroite**. Trois
raisons : (a) elle garde le sommet de son trou le plus dangereux (le gourou se cache
précisément dans la communauté de partage valorisée ; aucun autre co-gate ne l'attrape —
il n'y a pas de gate « gouvernance » au sommet) ; (b) elle ne réintroduit pas « la
subordination » que tu rejettes — elle ne mord que sur l'autorité **non librement
choisie**, ce que ta propre formule « librement choisie » exclut déjà ; (c)
unidirectionnelle et constatée-seulement, elle reste honnête (ne ferme que sur une
domination sans-sortie *documentée*, sinon `inconnu`). C'est une **synthèse en
couches** : ta thèse (marchandisation) + le test du « librement » (sortie opposable).

*Alternative défendable* : rester « salariat pur » et porter le risque gourou en
**limite assumée** (prose). Plus simple, plus proche de ta préférence littérale,
mais laisse le trou ouvert.

## 3. Intégration (à câbler une fois la 2ᵉ face tranchée)

- **Grille** (`config/grilles.yml`) : renommer `non_subordination` →
  `travail_non_marchandise`, réécrire la définition (table §1 + éventuelle 2ᵉ face).
- **Moteur** (`compute_verdict`) : renommer la lecture du critère ; mécanique
  `!= "non"` conservée. Si 2ᵉ face : un second champ constaté ou une valeur composite.
- **Doctrine** : `brief-cadre-conceptuel-communs.md` §8 et §11, et cadre exhaustif
  §4.5 (la tension Illich) — clarifier que le co-gate teste la *marchandisation*, et
  que la critique de la subordination est ramenée à son noyau opposable (sortie).
- **Méthode publique** : ajuster la prose du co-gate (la section « verdict »).
- Migration : aucune valeur à migrer (0 fiche cotée) ; cotation au fil du peuplement.

## 4. Idées par voix — conservées / écartées

- **Conservé** : le clivage « employeur externe » (méthodologue) ; la SCOP = `oui`
  (décommodification + méthodologue) ; le test « droit de sortie opposable » comme
  opérationnalisation du « librement choisi » (Illich) ; proxy unidirectionnel.
- **Écarté** : tout test d'autonomie psychologique ou de qualité du consentement
  (inobservable — les trois voix le refusent) ; le nom `non_salariat`.

---

## 5. Arbitrage opérateur — résolution finale (et intégrée)

Après un tour de dialogue supplémentaire (l'opérateur conteste le « SCOP = oui »
comme un biais pro-ESS/libéral) :

- **Option B retenue** : pas de 2ᵉ face « hiérarchie sans sortie ». Le co-gate teste
  *uniquement* la forme salariale. La domination sans salaire (gourou) est portée en
  **limite assumée** (prose), non gatée.
- **SCOP = `non`** (et non `oui`) : le distinguo « employeur externe vs interne » du
  méthodologue est abandonné — un salaire en SCOP reste du temps tarifé en argent par
  contrat, donc la forme marchande du travail, quelle que soit la propriété du capital.
  Le clivage n'est plus « employeur externe ou non » mais **« y a-t-il un rapport
  salarial ? »**. Cohérent avec la typologie des pôles, qui range déjà les
  coopératives en « faux amis » du régime commercial.
- **Steelman traité** : l'autogestion d'une coopérative n'est pas perdue — elle est
  créditée à l'**axe 3** (gouvernance, dans l'Indice), pas au co-gate du sommet, qui
  ne juge que la forme marchande du travail. Pas de double compte avec la lucrativité
  (qui plafonne déjà GAEC/SCIC à `hybride`).
- **Calibrage cœur/support retenu** : salariat du travail *productif* (cœur) = `non`
  (ferme) ; salariat de *support* marginal = `partiel` (ne ferme pas) ; don/troc/
  GAEC/bénévolat = `oui` ; absence = `inconnu`.

**Intégré (session #10)** : critère renommé `non_subordination` →
`travail_non_marchandise` dans `config/grilles.yml` (définition refondée),
`scripts/generate_site.py` (`compute_verdict`, mécanique `!= "non"` conservée ;
prose méthode), `config/concepts.yml` (règle du verdict + degrés), doctrine
canonique `brief-cadre-conceptuel-communs.md` §8/§11. Aucune fiche à migrer (0/45
cotée). Garde-fous verts, distribution inchangée (0 sommet, *vide-atteignable*).
