# Cycle 2 — Méthodologue du modèle, réaction au Gardien·ne de la rigueur

*Mini-strat Phase B, session #10, cycle 2 (réactions croisées). J'ai lu en
entier le volet du Gardien (`01-cycle1/gardien-rigueur.md`) — la voix qui me
contredit frontalement sur les deux co-gates. Objectif : bouger, pas répéter.
Je revérifie un fait avant d'écrire : `compute_verdict` l. 1361 code bien
`non_subord = g.get("non_subordination") == "oui"` — donc absence = bloque ; et
`non_subordination` n'apparaît dans **aucune** des 45 fiches `lieux/*.yml`. Les
deux bases factuelles tiennent. Le désaccord est donc bien méthodologique, pas
empirique.*

---

## 1. Là où le Gardien a raison — et où je bouge

Je concédais en cycle 1 que mon désaccord était « de méthode, pas de fond ».
En relisant son argument, je vois que j'avais sous-estimé un point qui n'est
pas décoratif : **§11 du cadre lit désormais le travail subordonné
*positivement* comme co-gate**, et §8 le pose explicitement en statut (a) avec
le proxy unidirectionnel. Ce n'est pas une coquetterie doctrinale : c'est la
troisième décommodification de Polanyi, structurellement appariée à la terre et
à la monnaie. Glosser `non_subordination`, c'est retirer une des trois pattes
du tabouret du sens — pas un critère « parmi d'autres » comme je l'écrivais.
Sur ce point, le Gardien a raison et je le concède.

Mais surtout, il me fait voir une **distinction que mon doc cycle 1 écrasait** :
*bloquer par absence* (artefact de peuplement) n'est pas *bloquer par présence
constatée* (jugement légitime). Mon analyse confondait les deux sous un seul
« 0/45 → ça ne trie rien ». Or le proxy est *unidirectionnel* : il ne tire son
information que du `non` constaté, jamais du `oui` ni de l'`inconnu`. Un
salariat-cœur constaté **doit** fermer le sommet — c'est un fait observable,
opposable, et son rejet est un jugement, pas un artefact. Cette asymétrie sauve
effectivement quelque chose que je voulais jeter. **Je bouge ici.**

## 2. Là où je tiens — la conséquence mécanique du codage actuel

Ce que je ne lâche pas : **le `compute_verdict` actuel ne code pas le proxy
unidirectionnel — il code un gate dur bidirectionnel.** `== "oui"` bloque sur
`non`, sur `inconnu`, *et* sur l'absence pure. Sur 45 fiches où le champ est
absent partout, ce n'est pas « le salariat ferme le sommet » : c'est « le
silence ferme le sommet ». Le modèle, tel qu'il tourne, ne *trie* pas — il
rejette 45/45 par défaut de donnée, puis raconte au lecteur que le sommet est
vide « par exigence ». C'est un mensonge sur la raison du vide : vide-impossible
maquillé en vide-exigeant. Le Gardien défend le bon *principe* (proxy) contre
un *codage* qui ne l'implémente pas. Voilà l'écart réel entre nous, et il est
réparable sans rien céder de la rigueur.

Donc : le gate dur n'est défendable **que si** le code distingue les valeurs.
`non` → ferme. `oui` → ouvre. `inconnu`/absent → **neutre, ne ferme pas le
sommet par lui-même**. Sinon on retombe sur le faux-positivisme à l'envers que
je dénonçais en cycle 1 (§4).

## 3. Position réconciliée — critère par critère

| Critère | Statut réconcilié | Règle de calibrage |
|---|---|---|
| Foncier (`foncier_hors_marche`+`irreversibilite`) | **gate dur** | observable, peuplé — inchangé |
| Vivant (`vivant_finalite`+`place_au_vivant`) | **gate dur** | observable, peuplé — inchangé |
| Régénération (`milieu_protege`) | **gate dur** | face opposable, 8 oui — inchangé |
| Finalité (`usage_non_marchand∈{oui,partiel}`+`usage_interet_general`) | **gate doux** | je maintiens ma ligne cycle 1 contre la glose du Gardien — voir ci-dessous |
| `non_subordination` | **gate dur, proxy unidirectionnel correctement codé** | `non`→ferme · `oui`→ouvre · `inconnu`/absent→neutre |

**Sur `non_subordination` — je rejoins le Gardien, mais j'exige la réécriture
du code.** Le gate reste dur *en tant que jugement sur le constaté*, pas en tant
que filtre sur le peuplement. Concrètement : remplacer `== "oui"` par une
logique à trois branches où seul `== "non"` ferme le sommet. Ma règle
« promotion-quand-couvert ≥ 50 % » de cycle 1 **tombe pour ce critère** : elle
visait un gate bidirectionnel (où l'absence bloque), problème qu'on résout
autrement ici — par l'unidirectionnalité du codage, pas par un seuil de
couverture. Le critère « observable + opposable → gate » du Gardien est juste ;
je l'avais mal appliqué en confondant *non collecté* et *non observable*. Le
salariat *est* observable ; on ne l'a simplement pas encore coté.

**Sur `usage_non_marchand` — je ne bouge pas, et je tranche notre désaccord
résiduel.** Le Gardien veut le glosser au motif qu'il est déclaratif/inobservable,
et que c'est la *finalité d'usage* qui gate. Mais le code (l. 1359) gate déjà
sur le couple `usage_non_marchand ∈ {oui,partiel}` **ET** `usage_interet_general
== oui` — c'est-à-dire exactement la *finalité* lisible dans les statuts, en
mode doux. Nous disons donc la même chose sous deux noms : sa « finalité
d'usage gatable » *est* mon gate doux actuel. Le glosser entièrement reviendrait
à retirer le seul verrou qui écarte le purement marchand à chaîne pure. Gate
doux maintenu — c'est la finalité observable qui gate, pas l'usage effectif.

**Datation (§9/§10).** Toute cette position est conventionnelle et datée
(2026-05-29, v courante à inscrire en D1). Re-test à chaque jalon : si un jour
le corpus cote du `oui` documenté en non-subordination, le gate créditera
positivement — réversibilité assumée.

## 4. Conséquence mécanique de la position finale

**Toujours 0 sommet aujourd'hui** — et c'est honnête, pas un échec. Mais pour
une raison désormais *vraie* : aucun lieu ne cote `non_subordination=non` (donc
le gate dur ne ferme mécaniquement personne pour ce motif) ; le vide réel vient
de l'intersection foncier+vivant+régénération+finalité, jamais franchie (Rayol
seul atteint foncier+vivant+régénération, et échoue à la finalité). La
différence avec le codage actuel est capitale : avant, le sommet était
**inatteignable par construction** (silence = blocage) ; après réécriture du
proxy, il est **atteignable et momentanément vide** — un lieu qui peuplerait les
quatre gates et ne cote *pas* de salariat-cœur entrerait. Le modèle cesse de
mentir sur la raison du vide. C'est exactement la bascule vide-impossible →
vide-atteignable que je plaidais — obtenue cette fois sans déclasser
`non_subordination`, mais en corrigeant son implémentation.

---

*Fin réaction cycle 2. Ce qui a bougé : je renonce à glosser
`non_subordination` ; je reconnais qu'un salariat constaté doit fermer le sommet
(jugement légitime ≠ artefact de peuplement). Ce que j'apporte en retour : le
gate dur n'est honnête que si le code implémente vraiment le proxy
unidirectionnel — l'absence ne doit plus bloquer. Désaccord résiduel tranché :
`usage_non_marchand` reste gate doux (= la finalité observable que le Gardien
veut gater, déjà codée).*
