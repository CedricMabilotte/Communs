# Cycle 2 — Voix théoricien·ne des communs & critique de l'extractivisme

*Réaction croisée. J'ai lu juriste-économiste, méthodologue-grille,
éditorial-réception, et relu ma propre voix du cycle 1.*

---

## Là où j'amplifie

**Le juriste a fait, sur mon terrain, ce que je n'avais pas su faire :
nommer mes intuitions en faits vérifiables.** J'avais posé trois questions
(captabilité du fonds, accumulation du fruit, gouvernance de l'affectation) ;
il les a converties en cinq marqueurs (C1 non-spéculation des parts, C2
plafonnement du rendement, C3 verrou d'actif, C4 gouvernance 1=1, C5 ESUS) plus
le C6 décisif — détention vs usage du foncier. C'est exactement ce qu'il me
fallait : ma ligne extraction/commun cessait d'être une posture pour devenir
une grille opérable. Et — point majeur — **sa distinction lucrativité d'activité
vs captation de plus-value foncière est mot pour mot ma ligne**. Quand il écrit
qu'un paysan en GAEC qui vit de ses brebis n'est pas plus capitaliste qu'un
salarié qui vit de son salaire, il dit ma thèse en langage du droit. Sur le
diagnostic, nous ne faisons qu'un.

J'amplifie aussi **l'éditorial sur un point que je sous-estimais : le mécanisme
de réception.** Mon cycle 1 disait « `marchand` est faux à la lecture » ; il a
montré *pourquoi* — le bandeau lu en 1 seconde contre la chaîne lue en 30, le
screenshot qui circule sans contexte, « marchand » comme antonyme militant de
« commun ». Sa formule « utiliser l'arme du camp contre un membre du camp »
capture précisément le coût politique que je pressentais. Mon critère
théorique et son critère de réception **convergent vers la même cible** : ne
jamais coller le registre marchand/spéculatif sur un maillon agricole sans
captation du fonds.

---

## Là où je conteste

**Contre le juriste — sa distinction civile patrimoniale (cran C) vs civile de
travail (cran B) n'est PAS le bon scalpel, ou seulement par accident (crux
T-d).** Il sépare SCI/GFA (« détenir un actif ») de GAEC/EARL (« exploiter par
le travail ») en s'appuyant sur l'objet statutaire. Mais du point de vue de la
captation de rente, l'objet ne tranche pas — c'est le **titre** sur le fonds
qui tranche : propriété vs usage. Un GFA citoyen à parts bloquées et un GFA
familial spéculatif sont *la même forme* avec des rapports à la rente opposés ;
il le concède lui-même (note 3, §3 : « la frontière C/D dépend de la liquidité
réelle, pas du sigle »). Mais alors sa propre architecture se mord la queue : si
le sigle ne tranche pas, pourquoi faire de « civile patrimoniale » un *cran*
distinct ? Le bon découpage n'est pas patrimonial/de-travail — c'est
**fonds-captable / fonds-non-captable**, qui traverse les formes. Sa C6 (son
sixième marqueur) est en réalité le seul qui devrait commander le cran haut ;
les cinq autres distinguent finement *à l'intérieur* du fonds-captable, ce qui
est précieux mais secondaire pour ma ligne. Je conteste qu'on hiérarchise C
au-dessus de D par l'objet ; je veux qu'on les départage par l'accès effectif à
l'abusus du fonds.

**Contre le méthodologue — son option A2 répare Pommiers mais risque de figer la
faute conceptuelle (crux T-b).** Sa solution est élégante : un cran
`exploitation_agricole`, trois lignes, verdict à 3 niveaux préservé. Je salue la
parcimonie. Mais sa frontière de tri (étape 1) lit la captation du fonds **sur
la chaîne du lieu**, pas sur le maillon — « si la chaîne confie le foncier à un
porteur non lucratif et l'usage au GAEC par bail → `exploitation_agricole` ».
C'est exactement mon point relationnel, et il a raison de le mettre là. Mais il
le range ensuite comme un *champ saisi sur le maillon* (`nature_interet:
exploitation_agricole` sur la fiche du GAEC). Or **le même GAEC peut être
preneur à bail ici et propriétaire de son foncier ailleurs.** Le cran qu'il
saisit sur l'entité ment dès que l'entité apparaît dans deux chaînes
différentes. Je conteste donc que `nature_interet` reste une propriété de
l'entité isolée pour ce qui touche au fonds.

**Contre l'éditorial — « Économie paysanne » comme *cran de classement* (et pas
seulement comme label de réception) glisse vers ma propre ligne rouge (crux
T-e).** J'y reviens en position révisée : je valide le label, je conteste qu'il
devienne une catégorie qui qualifierait le GAEC indépendamment de sa chaîne.

---

## Ce que je n'avais pas vu

**Le crux T-b a une réponse que je n'avais qu'effleurée : il faut séparer deux
questions que je mélangeais.** Au cycle 1 j'ai écrit « la captation du fonds se
lit peut-être au niveau du lieu, pas du maillon » — et j'ai laissé filer. Le
méthodologue m'oblige à trancher, et la confrontation à sa contrainte C2 (« une
seule source de vérité par fait ») me donne la clé que je n'avais pas vue :

*La nature de l'entité* (quels sont ses statuts : parts cessibles ? verrou
d'actif ? gouvernance 1=1 ?) **est** une propriété du maillon — légitimement
saisie dessus, et c'est là que vivent les C1–C5 du juriste. Mais *la captation
effective de la rente foncière* dépend du **titre dans la chaîne** (le GAEC
détient-il le fonds, ou est-il preneur d'un porteur hors-marché ?). Ce sont
deux faits distincts, et je les avais télescopés sous un seul mot
« extraction ». La leçon : mon principe relationnel ne réclame **pas** un cran
`nature_interet` relationnel (qui violerait C2 et serait incalibrable) ; il
réclame que le **verdict de chaîne** combine la nature du maillon (sur le
maillon) ET le titre sur le fonds (déjà dans la chaîne via `montage.type`). Le
foncier porté hors-marché par une FRUP, c'est déjà déclaré dans la chaîne. Donc
la captation se *lit déjà* à l'échelle du lieu — sans nouveau champ. C'est
compatible avec « une seule source de vérité = la chaîne » : on n'ajoute pas de
vérité, on cesse de faire dire à `nature_interet` une chose qui n'est pas la
sienne.

Je n'avais pas vu non plus, **côté éditorial, que le mot « marchand » pouvait
survivre au niveau LIEU tout en disparaissant au niveau maillon** (son §6,
ligne 2). Cela résout ma tension du cycle 1 (garder le tranchant sans taper le
paysan) sans rien diluer : « marchand » devient un verdict de montage, pas une
étiquette d'acteur. Élégant, et fidèle à ma ligne.

---

## Ma position révisée

**T-a (crans et principe).** Je maintiens : on gradue la *captation de rente*,
pas la présence d'argent. Mais je reconnais maintenant que mes marqueurs et ceux
du juriste **se recouvrent largement** — ses C1/C3 sont mon abusus, son C2 mon
fructus borné, son C4 mon usus. Notre seule divergence : il fait du *titre sur
le fonds* (C6) un sixième marqueur parmi d'autres ; moi j'en fais le **marqueur
qui commande**, parce qu'une structure sans accès à l'abusus du fonds ne peut
capter aucune rente foncière quelles que soient ses parts. Sur le nombre :
**un seul cran lucratif ajouté** (je me range à la contrainte C3 du
méthodologue), mais à condition que ce cran encode « fonds-non-captable » et
non « agriculture ».

**T-b (relationnel).** Position nette désormais : `nature_interet` reste sur le
maillon et qualifie ses statuts ; la captation du fonds se lit dans la chaîne
(titre/`montage.type`), source unique de vérité. Compatible. Je ne réclame plus
un critère relationnel *dans l'axe* — j'avais tort de le suggérer.

**T-c (3 vs 4 niveaux).** Je tiens ma ligne contre le maintien d'un « marchand »
large *au niveau maillon*. Mais l'éditorial m'a convaincu : « marchand » reste
légitime *au niveau lieu*. Donc je n'ai pas besoin d'un 4ᵉ verdict ; le vrai
tranchant — « montrer qu'on sait distinguer » — est obtenu par A2 (Pommiers →
`hybride`) plus le verdict-lieu `marchand` réservé aux chaînes à fonds captable.
Pas de surcoût conceptuel.

**T-d (patrimoniale vs de travail).** Je tranche : c'est le **titre**
(propriété vs usage du fonds), pas l'objet statutaire, qui commande le cran
haut. La distinction patrimoniale/de-travail du juriste est une nuance utile
*sous* la ligne du fonds, pas la ligne elle-même.

**T-e (labels éditoriaux).** Je valide « Économie paysanne » et « Lucrativité
encadrée » comme **labels de réception** — affirmatifs, justes, non
criminalisants. Je conteste seulement qu'ils deviennent des *catégories de tri*
appliquées à l'entité hors chaîne : « Économie paysanne » doit rester gouverné
par le titre sur le fonds, sinon il blanchit un GAEC propriétaire-spéculateur
exactement comme `commerciale` noircissait le GAEC preneur. Le label est juste ;
ce qui le déclenche doit rester la chaîne, pas le sigle.

Garde-fou critique non négociable : aucun cran, aucun label ne doit pouvoir
qualifier de « moins capitaliste » une structure qui *détient* son foncier et
peut le revendre. Le verrou d'actif et le titre sur le fonds restent **mérités,
jamais déclarés**.

---

*Fin de la réaction — Cycle 2, voix théoricien·ne des communs.*
