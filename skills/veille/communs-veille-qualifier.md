---
name: communs-veille-qualifier
description: Qualifie un lead Communs (Z2) — recherche entité/foncier/habitat, tranche l'éligibilité au corpus, écrit le verdict. Usage : /communs-veille-qualifier <slug-lead>
argument-hint: <slug-lead>
allowed-tools: [Bash, Read, Write, Edit, WebSearch, mcp__workspace__web_fetch]
---
# communs-veille-qualifier — Qualifier un lead (Z2)

Étape 2 (cf. `discovery/PIPELINE.md`). **Le lieu est-il dans le périmètre, oui/non,
pourquoi ?** N'écrit QUE le lead. Ne crée pas de fiche (→ `/communs-veille-carver`).

## Critère d'éligibilité Communs
Annuaire des **terres libérées habitées** : foncier **soustrait au marché par un
mécanisme FORMALISÉ d'inaliénabilité** (démembrement · propriété protégée non
lucrative + bail long · propriété publique inaliénable · propriété collective /
d'usage non spéculative · foncière) **ET** **habitat partagé du vivant** (humain +
non-humain).
- **Hors périmètre** : location, occupation précaire/gracieuse non formalisée,
  propriété privée classique (SCI à parts cessibles), collectif sans acte inaliénable.
- **Replis** vers une revue : loi-1905 (foncier religieux) · sanctuaires-de-retrait
  (retrait sans habitat) · greenwashing (« sanctuaire » sans chaîne) · mémoire (disparu).

## Méthode (MARS-prod : Assistant puis Checker)
1. Lis le lead. 2. **Recherche** : `WebSearch` d'abord (obtenir des URL), puis
`web_fetch` ces URL (provenance : web_fetch n'accepte que des URL issues d'une
recherche/d'un message). Registres : pappers, annuaire-entreprises.data.gouv.fr,
societe.com, net1901, assoce.fr/WALDEC, JOAFE. Documente entité+SIREN/RNA,
propriétaire du foncier + acte, inaliénabilité, activité, habitat + vivant.
3. **Verdict de lead** (corps) : périmètre oui/non + verdict pressenti
(marchand/hybride/sanctuaire) ou hors-corpus + repli ; pré-fiche recommandée ?
4. **Checker** : non sourcé → « à confirmer » ; aucune donnée fabriquée ; lieu non
identifiable → le dire.

## Règles d'or (leçons)
- Corrige une hypothèse erronée de l'opérateur si les sources la démentent (L33).
- « Réseau ami » = réseau seulement si lien partenarial **documenté** (L33).
- Statut lead : actif · pre_fiche · promu · rejete.

## Cas non identifiable (empreinte publique nulle) — règle (#11)
Si un lead n'a, après recherche, qu'un nom + une localité et **aucune source
publique** établissant entité, montage ou habitat (cas typique : un lieu seulement
nommé par un réseau, sans site ni mention presse/registre) : ne PAS fabriquer.
- Garder `statut: actif`, noter en corps « empreinte publique nulle — non perçable
  sans documents internes du réseau ou apport de l'opérateur ».
- Escalade explicite : (a) demander à l'opérateur une URL / un contact ; (b) rouvrir
  si le lieu publie. La profondeur a un plafond : on lit toute pièce primaire qui
  existe, on n'invente jamais ce qui n'est pas publié.
