# Dépouillement presse — Socialter HS15 et Reporterre (session #13, 2026-11-08)

*Graine manuelle, hors `watch.py`. Seize leads créés dans `discovery/leads/` (statut `actif`,
score 0, champ `origine:` daté). Rien n'a été écrit dans `lieux/ porteurs/ usufruitiers/
reseaux/` : la promotion reste manuelle (PIPELINE.md). Dédoublonnage fait contre les 52 lieux,
30 porteurs, 51 usufruitiers, 9 réseaux et 97 leads existants au 2026-11-08.*

## Périmètre lu

Socialter — hors-série n°15 « Ces terres qui se défendent » (déc. 2022 – fév. 2023, dir.
Reprise de terres) : Tactiques pour une stratégie foncière · La foncière Antidote · Terre de
liens · Racheter des forêts · Paysans de nature (Marais breton) · Lentillères · Un siècle de
luttes foncières (frise) · La terre ou rien (extrait payant) ; hors HS : Propriété commune, 4
pistes (nov. 2023) · Coopérative l'Arban (nov. 2023). Non lus (payants ou hors ligne) :
« Panorama des initiatives foncières », entretien Gaëtan du Bus, Vaucluse artificiel.

Reporterre — recherche par mots-clés (foncier, fonds de dotation, GFA, forêt, libre évolution,
ZAD) : Le fonds de dotation, une brèche… · Une association agriculturelle (Mâlain) · Dans la
Drôme, un havre réservé à la vie sauvage (ASPAS) · Le département de Loire-Atlantique rachète
895 ha de la ZAD (déc. 2018) · Habiter sans posséder (Antidote) · Pour sauver sa ferme
(Kergalaon, 2013 — écarté : SCI individuelle). **Cinq pages ont refusé le fetch** (ORE 99 ans ;
hameaux légers Bretagne ; habitants achètent des terres louées à des paysans bio ; NDDL
première victoire ; Une coopérative de terres menacée) — même symptôme que la veille
(`sources-sante.md` : reporterre « échec ⚠ » depuis plusieurs passes).

## Leads créés (par pertinence estimée)

**Forte** — à instruire en premier
- `forets-en-vie` — fonds de dotation du RAF, 54 ha (Lot, Corrèze, Haute-Loire, Creuse), forêt
  confiée à l'association Sous lou boès. Comble l'angle forêt du corpus. Porteur + lieu.
- `ferme-de-la-barge-marais-breton` — 170 ha, Paysans de nature ; deux porteurs à instruire
  séparément : LPO Vendée (acquisitions) et Département (ENS, mise à disposition gracieuse).
- `terres-communes-cravirola-maquis-suc` — structure commune type Longo Maï portant trois
  fermes des années 1990 ; localisations à revérifier (résumé d'article ambigu).
- `aspas-reserve-grand-barry` — 105 ha, Véronne (Drôme), 2014 ; ASPAS > 1 200 ha. **Question
  de doctrine** (ci-dessous).

**Moyenne** — montage à parts ou structure à nommer
- `malain-gfa-champs-libres` — GFA citoyen (3 ha, 103 porteurs de parts) + SCI + Risomes.
- `alloue-scic-terres-en-chemin` — SCIC communale, portage d'attente de prairies.
- `cooperative-de-beletre` — réserve foncière sur ferme Terre de liens.
- `hameaux-legers` — réseau ; 13 baux emphytéotiques communaux signés 2021-2023.
- `cooperative-l-arban` — SCIC foncière habitat, Millevaches ; lieux portés non nommés.
- `collectif-de-verfeil` — quinzaine de personnes depuis 2014, forme juridique à trouver.
- `passeurs-de-terres`, `terres-citoyennes-albigeoises` — foncières locales (porteurs).
- `gfce-lu-picatau` — groupement forestier citoyen (RAF), localisation à trouver.

**Faible / veille** — garder, ne pas promouvoir
- `quartier-libre-des-lentilleres` — occupation sur foncier métropolitain, pas d'acte.
- `ile-d-yeu-terre-fert-ile` — régulation des prix plus que portage.
- `scic-nord-nantes` — structure non nommée.

## Déjà en corpus — enrichissements de sources proposés (non appliqués)

- `lieux/la-marinie.yml`, `lieux/ancrage.yml`, `lieux/la-talvere.yml`, `porteurs/fonciere-antidote.yml`
  : ajouter Socialter « La foncière Antidote » (C. Rébillard, 13/02/2023) et Reporterre
  « Habiter sans posséder » (C. Morel Darleux) — précisent le bail emphytéotique « tous les
  droits sauf vendre » et l'association chapeau « Les passagères de l'usage ».
- `lieux/nddl.yml` : Reporterre 19/12/2018 (rétrocession État → Département, 895 ha sur
  1 425, 950 000 €) — source utile au suspens « baux 2024 non sourcés » (la fiche ne cite
  que Terre-net pour la délibération du 10/10/2024 ; la source primaire — délibération de la
  commission permanente du 44 — reste à trouver).
- `lieux/larzac.yml` : Socialter (frise 1971-1981, SCI/GFA autour du camp) — contexte seulement.
- `reseaux/longo-mai.yml` : Reporterre « brèche » (fondation suisse porteuse du patrimoine).

## Trois questions pour Ced

1. **ASPAS / sanctuaires sans usufruitier.** La doctrine exige nue-propriété d'intérêt
   général + usage confié à une personne morale non lucrative. Une réserve de vie sauvage n'a
   pas d'usager autre que le vivant. Trois options : (a) fiche `modeles/` (modèle voisin, hors
   classement) ; (b) extension de la doctrine « porteur-usager unique à finalité vivant »,
   coté sur les axes vivant/milieu/durée ; (c) hors corpus, renvoi vers Enjeux. Le choix
   touche la définition même de « Terres Libérées ».
   -> a, l'inclure avec une mention spéciale
2. **GFA et groupements forestiers citoyens** (Mâlain, Lu Picatau) : la revue mémoire a
   conclu que les formules à parts échouent sur la condition 1. Faut-il une fiche quand même
   (avec verdict calculé bas, utile pour l'annuaire critique) ou les laisser en leads ?
   -> 1 
3. **Socialter comme source de veille** : absent de `config/sources.yml` ; contenu riche mais
   pour moitié payant, rythme lent → `frequence: trimestrielle`, parser `html_static`.
   Et **Reporterre** : la source est configurée mais échoue ; probable blocage anti-robot
   (même refus depuis le conteneur). Options : flux RSS (`https://reporterre.net/spip.php?page=backend`
   [SUPPOSÉ, à tester]) au lieu du `deep_html`, ou retrait de la source avec note.
   -> chercher les moyens de pouvoir acceder pour scan leger, faire une liste des sources interessantes mais inaccessibles pour tenter régulierement leur deblocage

## Suites possibles (hors session)

Qualifier les quatre leads « forte » avec `/communs-veille-qualifier <slug>` : ok
chercher la source primaire NDDL (délibération 44 du 10/10/2024) : ok
tester le flux RSS Reporterre : ok
ajouter Socialter aux sources après arbitrage : ok
