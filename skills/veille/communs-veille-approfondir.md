---
name: communs-veille-approfondir
description: Second tour de recherche sur une fiche Communs — lève les inconnu/partiel par sources réelles, sans fabriquer. Usage : /communs-veille-approfondir <slug>
argument-hint: <slug>
allowed-tools: [Bash, Read, Write, Edit, WebSearch, mcp__workspace__web_fetch]
---
# communs-veille-approfondir — Lever les inconnus (complétion)

Étape 5. Reprend une fiche (lieu + entités) cotée prudemment et **lève les
`inconnu`/`partiel` par la recherche** — sans jamais durcir sans source.

## Méthode (MARS-prod : Assistant puis Checker)
1. Repère chaque critère `inconnu`/`partiel` des blocs `grille:`.
2. **Recherche** : `WebSearch` d'abord (obtenir des URL), puis `web_fetch` ces URL
   (provenance). Cibles à fort rendement : statuts (clauses d'inaliénabilité /
   réserves impartageables / dévolution), titre/durée d'usage, loyer/régime,
   résidence permanente, vivant non-humain, transparence (comptes déposés —
   BODACC/greffe), SIREN/RNA. Registres + sites des lieux + statuts de réseau
   (ex. CLIP : statuts types, PV d'AG).
3. Mets à jour `grille:` (valeur + note sourcée), `dossier`, `fiabilite`,
   `sources`. Cite chaque URL.
4. **Checker (adversarial)** : pour chaque `inconnu`→valeur, la source l'étaye-t-elle
   vraiment ? Sinon **remets `inconnu`**. Aucun `oui`/`non` fabriqué. Ce qui reste
   non documenté RESTE `inconnu` (honnête et attendu). Verdict non saisi.

## Garde-fous
Chaînes inchangées (ne pas toucher la structure) ; pas d'`&` brut ; ne pas
renommer un uid (load-bearing pour les liens). Régénérer ; vérifier que le
verdict tient. Conserver les réserves dans `fiabilite`.
