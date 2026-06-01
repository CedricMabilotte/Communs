---
name: communs-veille-carver
description: Promeut une pré-fiche Communs (Z3) en fiche réelle du corpus (Z4) — crée la fiche-lieu + ses entités de chaîne, cote la grille. Usage : /communs-veille-carver <slug>
argument-hint: <slug>
allowed-tools: [Bash, Read, Write, Edit]
---
# communs-veille-carver — Promotion Z3 → Z4 (fiche réelle)

Étape 4 (cf. `discovery/PIPELINE.md`). Crée `lieux/<slug>.yml` + les fiches
d'entités de la chaîne (`porteurs/`, `usufruitiers/`) à partir d'une pré-fiche.
**Acte volontaire** : entre au corpus public.

## Modèle de schéma — COPIER EXACTEMENT
- Lieu (montage `propriete_collective`) : `lieux/domaine-des-eveils.yml`.
- Porteur : `porteurs/le-temps-des-possibles.yml`. Usufruitier (avec
  `nature_interet` + `grille[]`) : `usufruitiers/scic-domaine-des-eveils.yml`.
- Critères de grille par catégorie : `config/grilles.yml`. Vocabulaire
  (`titres`, `nature_interet`, silhouettes de `montage`) : `config/concepts.yml`.

## Règles impératives
- **Cotation honnête** : `oui`/`non` seulement si sourcé ; **`inconnu`** partout
  où non documenté (le verdict gère l'inconnu). Une note par critère.
- **Verdict NON saisi** : il se calcule (`compute_verdict`) depuis la chaîne et la
  grille. Ne jamais écrire de champ `verdict`.
- **Garde-fous (font échouer la génération)** : uid uniques ; tout
  `montage.articulations[].usufruitier` ⊆ `chaine.usufruitiers` ; pas d'entité
  HTML brute (`&` → `&amp;` ou reformuler) ; cohérence nature×titre.
- **Titres** : seuls les ids de `concepts.yml/titres` (usufruit, bail_rural,
  bail_emphyteotique, bail_reel_solidaire, bail_a_construction, convention,
  commodat, domanialite, **integre**…). `propriete` N'EXISTE PAS. `integre` =
  porteur et usufruitier sont **une seule entité** (pas de dissociation) — ne
  l'utiliser que dans ce cas. Pour deux entités distinctes (modèle CLIP), titre
  d'articulation = `convention`. Le modèle domaine-des-eveils n'articule QUE
  l'usufruitier (pas le porteur).
- `nature_interet` de chaque entité dans le canon (non_lucrative,
  commerciale_desactivee, commerciale_encadree, exploitation_agricole,
  commerciale, privee_individuelle, inconnu).
- Vérifier la forme juridique réelle au **registre** (ne pas présumer « SCIC/SCOP »
  — souvent une SAS gérée en coopérative ; cf. cas Chirols).
- **Régénérer** (`python3 scripts/generate_site.py`), garde-fous verts, vérifier
  le verdict calculé. Passer le `statut:` du lead à `promu`. Aperçu L9 autonome
  de la fiche (CSS inliné) pour revue.
- Si le lieu est membre d'un réseau (ex. CLIP) : ajouter le lieu (et son porteur)
  au `membres:` de la fiche réseau, une fois la fiche créée.
