# Sources intéressantes mais inaccessibles — liste de déblocage périodique

*Créé session #13 (2026-11-08), en réponse à la question 3 du dépouillement presse
(`discovery/depouillement-presse-2026-11-08.md`). Rôle : garder la trace des sources
qu'on voudrait suivre mais qu'un mécanisme technique empêche d'atteindre, pour retester
périodiquement — distinct de `discovery/sources-sante.md` (journal auto-généré par
`watch.py`, écrasé à chaque passe).*

## Reporterre — débloqué cette session

`reporterre.net` en page d'accueil (`deep_html`) échouait systématiquement côté `watch.py`
(blocage anti-robot probable sur la page racine — symptôme distinct d'un blocage par
`robots.txt`, puisque les pages d'articles individuelles restent accessibles en fetch
direct). **Contournement trouvé et câblé** [VÉRIFIÉ 2026-11-08, fetch direct + test de
`rss_links()` depuis la machine utilisateur] : le flux RSS `https://reporterre.net/spip.php?page=backend`
répond normalement (60 items, titres avec entités HTML décodées). `config/sources.yml`
bascule la source `reporterre` sur `parser: rss` ; `scripts/watch.py` gagne une fonction
`rss_links()` et une branche de dispatch dédiée. À revérifier à la prochaine passe
hebdomadaire réelle (lundi) : le run `watch.py` depuis GitHub Actions a un contexte
réseau différent de ce test local — si le flux RSS échoue aussi depuis Actions, le
ramener ici avec le motif précis.

Reste un angle mort distinct, non résolu par ce correctif : cinq pages d'articles
Reporterre identifiées pendant le dépouillement de presse ont refusé le fetch direct
(`client_error`/`SERVER_ERROR`), sans qu'on sache si c'est un blocage anti-robot ponctuel
ou une page retirée/déplacée :
- ORE 99 ans (brèche, fonds de dotation)
- Hameaux légers en Bretagne (baux emphytéotiques communaux)
- Des habitants achètent des terres louées à des paysans bio
- À Notre-Dame-des-Landes, une première victoire pour préserver les terres agricoles
- Une coopérative de terres menacée

À retenter individuellement de temps en temps (le reste du site répond bien ; peut-être
une protection ponctuelle sur certaines URL, ou un retrait éditorial).

## recit.eco (RECit — réseau des écolieux)

[VÉRIFIÉ 2026-11-08, WebFetch] Domaine entier refusé par `robots.txt`
(`robots_disallowed`) — pas un blocage anti-robot actif comme Reporterre, un retrait
volontaire du site vis-à-vis des robots. Pas de flux RSS testé (le blocage robots.txt
couvrirait vraisemblablement aussi un flux, donc inutile de chercher un contournement
technique ; seule option : accès manuel ponctuel par un humain, ou retrait de la source
si elle reste muette trop longtemps).

## lutopiks.fr

[VÉRIFIÉ 2026-11-08, WebFetch] Même symptôme que recit.eco : domaine entier refusé par
`robots.txt`. Même conclusion.

## data.loire-atlantique.fr / deliberations.loire-atlantique.fr

Pas une source de veille (`config/sources.yml`), mais un registre public qu'on a cherché
à consulter pour sourcer précisément `lieux/nddl.yml` (délibération de la commission
permanente du Département citée pour les baux emphytéotiques de 25 ans, 10/10/2024 —
suspens identifié dans le dépouillement de presse). [VÉRIFIÉ 2026-11-08, WebFetch]
`data.loire-atlantique.fr` (portail de recherche officiel des délibérations) refuse le
fetch (`robots_disallowed`) sur sa page de recherche comme sur son API ; le registre
documentaire dédié `deliberations.loire-atlantique.fr` ne renvoie que des PDF d'actes
isolés indexés par des moteurs externes (aucun moyen trouvé d'y chercher directement par
date). La séance du 10/10/2024 n'a pas été retrouvée par recherche web ciblée — seules
des séances voisines (22/02, 04/07, 19/09, 07/11, 12/12/2024) apparaissent indexées.
**Palliatif appliqué** : ajout d'une source secondaire solide (Reporterre, 19/12/2018,
rétrocession 895 ha/1 425 ha pour 950 000 €) à `lieux/nddl.yml`, qui corrobore le montage
sans remplacer la pièce primaire. À retenter : une recherche manuelle sur le portail par
un humain (le moteur de recherche interne n'est pas bloqué pour un navigateur normal,
seulement pour un fetch automatisé), ou une demande directe au Département.

## Méthode de relecture de cette liste

Périodicité : **tous les mois** (décision Ced, 08/11/2026). À chaque relecture, un
simple `WebFetch` sur l'URL de chaque entrée suffit à vérifier si le blocage persiste.
Entre deux relectures mensuelles, retester aussi dès qu'une source listée ici redevient
pertinente pour un lead précis — pas la peine d'attendre l'échéance dans ce cas. Si une
source se débloque, documenter le correctif comme pour Reporterre ci-dessus plutôt que de
simplement supprimer l'entrée — la méthode de déblocage peut servir à d'autres sources.

**Dernière relecture : 2026-11-08** (création de la liste — toutes les entrées encore
bloquées à cette date). **Prochaine échéance : 2026-12-08.**
