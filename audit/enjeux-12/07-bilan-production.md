# Bilan de production — section Enjeux (COD13.012)

*10 octobre 2026. Trace de la chaîne collège → rédaction → vérification.*

## Chaîne suivie

1. **Collège méta (MARS-strat, cycle 1)** — 7 voix isolées : @kern, @antimeta, @eozen,
   @igor, @valorisation, @lumen, chercheur·e agro-éco-socio rurale
   (`01-cycle1-contributions.md`).
2. **Contradiction (cycle 2)** — @contradicteur : PASS avec corrections ; faille principale
   = thèse écrite dans la définition, non falsifiable (`02-cycle2-contradiction.md`).
3. **Synthèse (cycle 3)** — démarche, règles de sources, matrice logique (12 dimensions ×
   18 études × 10 outils), architecture (`03-demarche-et-matrice.md`) ; contrat de
   production (`04-gabarit-redaction.md`), consignes (`05`, `06`).
4. **Rédaction** — 18 chercheur·es-rédacteur·rices en parallèle (une étude chacun·e),
   recherche web + API publiques (Eurostat, Insee, HAL, VigiEau, Cerema).
5. **Vérification adversariale** — 18 vérificateur·rices indépendant·es, corrections en
   place ; verdict « publiable après corrections » pour les 18.
6. **Générateur** — section rendue par `scripts/generate_site.py` (graphiques SVG depuis
   CSV, schémas, matrice, sources agrégées, renvois inverses sur les fiches, glossaire),
   garde-fou `verifier_enjeux` : 0 anomalie, 0 lien cassé.

## Volume publié

18 études (~75 000 mots), 72 jeux de données CSV, 19 schémas, ~95 figures, ~400 sources,
117 termes de glossaire.

## Ce que la vérification a rattrapé (exemples)

- Sens inversé d'une décision du Conseil d'État (Région Normandie, 16 mars 2026) — E09.
- Une proposition de loi présentée comme non adoptée était devenue la loi n° 2026-248 du
  7 avril 2026 — E11 ; régime L. 218-1 (captages) décrit dans sa version de 2019, modifié
  en 2022 — E12 ; astreinte urbanisme relevée en 2025 — E10.
- Titres de figure faux (« quatre fermes sur cinq » → trois sur quatre ; « femmes
  majoritaires après 50 ans ») — E01 ; rang européen 18e → 17e — E05 ; « la charge de la
  dette dépasse l'EBE » (faux : ~50 %) — E06.
- Imputations retirées (intention d'un dirigeant, E04), formules sans source retirées,
  « répression » absente, tous les « à vérifier » soldés.
- Table de correspondance de la synthèse (E18) réalignée sur ce que disent les 17 études.

## Limites connues (au 10/10/2026)

- Légifrance bloque les robots : le droit est cité via sources officielles secondaires
  (Conseil constitutionnel, Sénat, Assemblée, BOFiP, Service-Public, AIDA/Ineris,
  codes.droit.org).
- Quota de recherche web partagé épuisé tôt : certaines pistes non explorées (listées dans
  les rapports d'agents ; voir « ce qui reste fragile » de chaque étude).
- Données SAFER = données d'opérateur, signalées ; plusieurs séries nationales
  n'existent pas (préemptions, biens sans maître, friches, pastoralisme hors Alpes).
- Corpus sans lieu forestier ni ultramarin (E15, E16 le disent).
- Fiches à relire signalées par les agents : `lieux/nddl.yml` (baux emphytéotiques
  d'octobre 2024 non sourcés), `usufruitiers/assemblee-des-usages-nddl.yml` vs
  `porteurs/fonds-la-terre-en-commun.yml` (désignation du conseil du fonds).
