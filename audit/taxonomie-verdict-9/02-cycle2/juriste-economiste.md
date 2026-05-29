# Cycle 2 — Voix juriste-économiste des structures agricoles et de l'ESS

*Réaction croisée. J'ai lu les trois autres voix du cycle 1 et relu la mienne.
Je prends parti depuis le droit et l'économie réelle, sans glisser vers la
posture militante (théoricien) ni la faisabilité code (méthodologue).*

---

## Là où j'amplifie

**Le théoricien me donne le principe que mes cinq marqueurs cherchaient à
servir sans le nommer.** J'avais raison sur les critères (non-spéculation des
parts, verrou d'actif, rendement plafonné, 1=1), mais je raisonnais maillon par
maillon. Lui formule la chose juste : ce qui doit être gradué, ce n'est pas la
lucrativité, c'est **la captabilité de la valeur de fonds**. C'est exactement la
distinction du code civil entre les attributs du droit de propriété — *usus,
fructus, abusus* (art. 544). Mon C6 (« détention du foncier vs simple usage »)
était la bonne intuition mais je l'avais rangé comme sixième critère
*transversal*, presque en annexe. Le théoricien montre que ce n'est pas un
critère parmi d'autres : c'est **l'axe maître**. La cessibilité des parts (C1),
le verrou d'actif (C3), c'est l'*abusus* sous forme sociétaire. Je l'amplifie :
mes C1–C5 mesurent tous, en réalité, une seule chose — qui tient l'*abusus* du
fonds et peut en empocher la plus-value.

**Le méthodologue a raison sur la mécanique du bug, et sa lecture me conforte
juridiquement.** Il pointe que `concepts.yml` range déjà « société de marché
**ou** exploitation agricole » sous le même `id` : c'est l'aveu écrit que le
label porte deux qualifications juridiques incompatibles (code de commerce vs
code rural). Ce n'est pas moi qui invente la distinction GAEC/SARL : la table
elle-même la décrit puis l'écrase. J'amplifie son option A2 (basculer le nouveau
cran vers `hybride`) — c'est la seule cohérente avec la réalité juridique de
Pommiers, où le foncier est *irréversiblement* sorti du marché par une FRUP.

**L'éditorial a raison sur un point que je sous-estimais** : « marchand » dans
le champ écolo-foncier est l'antonyme militant de « commun ». Coller ce mot à un
GAEC sur bail Terre de Liens, c'est juridiquement faux *et* publiquement
suicidaire. Sa cible (T-a, T-e) recoupe la mienne par un autre chemin.

---

## Là où je conteste

**Contre le théoricien, sur T-b — la captation n'est pas *seulement*
relationnelle.** Il a raison qu'un GAEC sur bail ≠ un GAEC propriétaire, et que
cela dépend de la chaîne. Mais il en tire que « la forme sociétaire ne dit
rien », que tout se joue au niveau du lieu. C'est juridiquement inexact. La
forme sociétaire dit déjà beaucoup : une **SCI** a pour objet civil la
*détention* d'un actif (art. 1832 c. civ. + objet statutaire) ; un **GFA** est
par définition un groupement *foncier* (art. L. 322-1 et s. c. rural) — son
objet **est** la propriété de la terre. Un **GAEC** a pour objet l'*exploitation
en commun* (art. L. 323-1). La forme porte une présomption d'objet. Donc :
**il faut croiser la forme ET le titre, mais aucun des deux seul ne suffit.** La
forme donne la présomption ; le titre (bail vs propriété) la confirme ou la
renverse. Un GAEC propriétaire de son foncier capte l'abusus malgré sa forme
vertueuse ; une SCI à parts statutairement bloquées et bail emphytéotique au
profit d'un OFS ne le capte pas malgré sa forme patrimoniale. Ma réponse de
juriste à T-b est donc : **présomption par la forme, réfragable par le titre et
les clauses statutaires.**

**Contre le méthodologue, sur T-a — un seul cran fusionne deux objets de droit
distincts.** Il veut UN cran (`exploitation_agricole`) regroupant « toutes les
sociétés civiles d'exploitation », en renvoyant la nuance « dans la prose ». Je
conteste, parce qu'il met dans le même panier deux choses que le droit oppose
frontalement (voir T-d ci-dessous) : les civiles *de travail* (GAEC, EARL, SCEA
exploitante) et les civiles *patrimoniales* (SCI, GFA). Le GFA et la SCI ont
pour objet la détention foncière — donc tiennent potentiellement l'abusus. Les
mettre dans le cran « exploitation paysanne » serait re-créer un L14 d'un autre
genre : un cran « propre » qui blanchit du portage patrimonial. Sa contrainte de
parcimonie (max 6–7 crans) est légitime ; mais elle ne justifie pas de fusionner
détention et exploitation, qui est précisément la frontière que la refonte veut
tracer.

**Contre l'éditorial, sur T-c et le label « Économie paysanne ».** Le label est
politiquement habile mais juridiquement faux comme *catégorie* : un GAEC reste
une société à objet lucratif (il distribue ses bénéfices à ses associés) et il
*peut* détenir son foncier. « Économie paysanne » suggère une nature, alors que
c'est une *situation* (exploitant non détenteur). Si la SCEA du cran bascule en
propriétaire, le label ment. Je concède le wording comme clé de lecture (T-e),
mais je refuse qu'il devienne le critère de classement.

---

## Ce que je n'avais pas vu

**Mon cran C (`civile_patrimoniale`) était la clé, pas un cran moyen.** En cycle
1 je l'avais placé entre B et D comme une nuance. La lecture croisée révèle que
la frontière travail/patrimoine (T-d) est **le pivot** de toute la refonte, pas
un raffinement. Le théoricien le confirme par le haut (l'abusus se loge dans la
détention), le méthodologue par le bas (la migration se fait sur le critère
« détiennent-ils ou exploitent-ils le foncier ? »). Ce critère de tri du
méthodologue *est* ma distinction T-d, formulée en langage de chaîne. Nous
disons la même chose.

**Je n'avais pas mesuré que mes 5 crans étaient en réalité 2 crans + une
matrice.** Le méthodologue a raison : 5 valeurs nouvelles font exploser la table
et le pire-au-mieux. Mais l'éditorial a raison qu'il faut *deux* intermédiaires
(paysan vs coopérative encadrée), pas un. La synthèse : la distinction fine
(GAEC vs EARL vs SCEA) n'a pas à vivre dans l'énuméré `nature_interet` — elle
vit dans le couple **forme_juridique (donnée d'entrée) + titre foncier (chaîne)**.
L'axe lui-même n'a besoin que de séparer *travail* et *patrimoine*.

---

## Ma position révisée

Je me range sur **deux crans nouveaux, pas cinq** — j'ai bougé sur T-a.

1. **`exploitation_agricole`** (économie paysanne) : société civile *de travail*
   (GAEC, EARL pluripersonnelle, SCEA exploitante) **ne détenant pas** le fonds,
   ou le détenant sous verrou anti-spéculatif vérifié. Verdict `hybride`
   (option A2 du méthodologue), plafond ax2 ~40.
2. **`commerciale_encadree`** conservé pour la lucrativité disciplinée (SCIC,
   SCOP, foncières ESUS, coops d'habitants) — verrou d'actif + rendement
   plafonné + 1=1.

Mais je tiens fermement T-d comme **garde-fou, pas comme cran** : les civiles
**patrimoniales** (SCI, GFA, SCEA de portage) ne basculent PAS d'office dans
`exploitation_agricole`. Leur objet est la détention ; elles restent
`commerciale` (D) **sauf** clause statutaire de non-cession / bail
emphytéotique / agrément vérifiés — auquel cas, et seulement là, elles montent.
Le critère de tri n'est donc pas le sigle, c'est : **objet (présumé par la forme)
× titre (lu sur la chaîne) × clause (vérifiée sur statuts, sinon `inconnu`).**
C'est ma réponse à T-b : la forme suffit à *présumer*, jamais à *trancher* ; le
titre confirme ou renverse.

Sur T-c (3 vs 4 verdicts) : je ne réclame pas un 4ᵉ verdict public. A2 à 3
niveaux (`marchand` / `hybride` / `sanctuaire`) suffit — un 4ᵉ niveau serait une
catégorie juridique que je ne peux nommer sans l'inventer (« marchand_encadré »
n'a aucun ancrage légal). Je m'abstiens : décision éditoriale, pas juridique.

Sur T-e : **je concède le wording** (mes libellés sont imbuvables, l'éditorial a
raison) **et je défends la découpe** : « Économie paysanne » comme label tant
qu'il classe sur le critère détention/travail, pas sur la sympathie. Le label
public habille ; c'est le couple forme × titre qui qualifie.

**Lignes rouges maintenues** : ne jamais qualifier un GAEC de société
commerciale ; `inconnu` reste sacré quand les statuts (cession, rendement,
agrément ESUS) ne sont pas publics ; ne pas réhabiliter SARL/SAS/propriété
individuelle ; le verrou d'actif et le 1=1 sont des faits légaux, pas des
impressions.

---

*Fin de la réaction juriste-économiste — Cycle 2.*
