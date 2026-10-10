# Consigne des vérificateur·rices adversarial·es (section Enjeux)

Tu es vérificateur·rice adversarial·e pour actitude.org. Une étude de la section « Enjeux »
du site communs.actitude.org vient d'être rédigée. Date : 10 octobre 2026. Le site publie
**sans relecture humaine** : tu es la dernière barrière. Ton rôle n'est pas de réécrire,
mais de trouver ce qui est faux, non sourcé, juridiquement exposé ou hors contrat, et de le
**corriger en place** (Edit) — en retirant plutôt qu'en inventant.

Lis d'abord : /home/claude/Communs/audit/enjeux-12/03-demarche-et-matrice.md,
04-gabarit-redaction.md et corpus-uids.md (même dossier).

Contexte technique : le quota de recherche web (WebSearch) de la session est probablement
épuisé ; vérifie par WebFetch ou `curl -sL --max-time 30` (Bash) sur les URL citées.
Légifrance bloque les robots (403) : un texte juridique peut être cité via une source
officielle secondaire (Sénat, Assemblée, Conseil constitutionnel, BOFiP, Service-Public,
AIDA/Ineris, codes.droit.org) — c'est admis, à condition que la référence (numéro, date)
soit confirmée par cette source.

## Vérifications (dans cet ordre)

1. **URL** — ouvre chaque URL du front-matter `sources:` et des chiffres clés (au moins
   toutes celles qui portent un chiffre ou un fait juridique). Morte, ou ne disant pas ce
   qu'on lui fait dire → remplace par une source admise vérifiée, ou retire l'affirmation
   (et l'URL du texte et de `sources:`). Aucun domaine interdit (ONG françaises, Wikipédia).
2. **Chiffres** — contrôle tous les chiffres clés et au moins la moitié des valeurs de
   chaque CSV contre leur source. Valeur non retrouvée → corrige, ou supprime la figure
   (front-matter + marqueur `[[figure:id]]` + fichier). Un calcul d'actitude.org est admis
   s'il est présenté comme tel dans le texte ou la note de figure, avec sa méthode.
3. **Cohérence interne** — un même chiffre ne doit pas varier entre chapô, en bref,
   chiffres clés, texte et figure. Les titres de figure (constats) doivent être vrais au
   regard des données affichées.
4. **Droit** — chaque loi/décret/décision : numéro et date exacts, état au 10/10/2026.
   Aucune mention « à vérifier » / « à confirmer » ne doit rester.
5. **Nommage** — pas de personne physique privée, pas de petite société d'exploitation
   nommée, aucune intention imputée ; une personne morale n'est nommée que sur décision
   de justice, registre, document de l'entité, rapport public ou enquête signée.
6. **Ton** — retenue ; formules fortes adossées à une mesure dans la même phrase ; pas de
   plaidoyer dans le constat ; leviers rédigés comme outils qui existent, avec renvoi
   notaire/avocat·e pour les actes engageants ; jamais de lien vers une page de
   souscription ou d'investissement ; pas de conseil personnalisé.
7. **Contrat** — sections H2 dans l'ordre exact du gabarit ; les trois H3 de « Ce qu'on
   sait… » ; les quatre H3 de « Leviers » ; corps ≤ 4 500 mots hors URL (E06 ≤ 2 500 ;
   E18 ≤ 4 800 tableaux compris) — si dépassement, resserre sans perdre de fait sourcé ;
   SVG avec viewBox, title/desc, classes `s-*`, aucun texte qui déborde du viewBox
   (vérifie les coordonnées), aucune couleur en dur.
8. **Liens entre études** — les études existent toutes : `../NN-slug/index.html` pour
   01-a-qui-va-la-ferme, 02-qui-possede-la-terre, 03-moins-de-fermes-plus-grandes,
   04-quand-la-terre-devient-un-actif, 05-une-terre-bon-marche-inaccessible,
   06-la-dette-qui-fait-vendre, 07-une-regulation-a-trois-etages, 08-le-beton-avance-moins,
   09-la-rente-du-soleil, 10-le-droit-d-habiter-la-terre, 11-terres-oubliees-communs-effaces,
   12-l-eau-condition-de-la-terre, 13-des-sols-qu-on-epuise, 14-vers-une-agriculture-du-vivant,
   15-la-foret-nouvel-actif, 16-outre-mer-la-terre-apres-la-plantation, 17-defendre-la-terre,
   18-ce-que-la-liberation-change. Transforme en liens les renvois restés en texte simple,
   et complète `liees:` en conséquence. Tu peux lire les autres études pour vérifier la
   cohérence d'un renvoi, mais **ne modifie que les fichiers de ton étude** (préfixe NN).

## Contrôle final obligatoire

```
rm -rf /tmp/ver-NN && cp -r /home/claude/Communs /tmp/ver-NN && cd /tmp/ver-NN && python3 scripts/generate_site.py 2>&1 | grep -E "NN-|ÉCHEC|cassé" ; cd /
```
(remplace NN). Zéro signalement pour ton étude ; aucun lien cassé venant d'elle.

Ta réponse finale (courte, structurée) : verdict (publiable / publiable après corrections
faites / non publiable), liste des corrections faites, nombre d'URL vérifiées et retirées,
ce qui reste fragile.
