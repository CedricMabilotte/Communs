# Brief — Session D : typologie partagée Communs ↔ Plan B

*Brief de cadrage pour une session conceptuelle à venir. Voix Eozen.
Document de travail — à raffiner en ouverture de session.*

---

## 1. Contexte

**Communs / Terres Libérées** est un annuaire critique des montages de
libération de terres en France — les lieux dont le foncier a été soustrait à
l'exploitation abusive et préservé comme habitat pour le vivant **humain et
non-humain**. Depuis la session #7, une décision de périmètre s'est imposée :
la libération « par retrait » — l'exclusion intégrale de l'usage humain au
profit de la libre évolution (modèles de type Réserve de Vie Sauvage, forêts
en sanctuarisation intégrale) — sort du corpus principal. Ces lieux relèvent
désormais d'une revue dédiée (cf. `revues/sanctuaires-de-retrait/`) ; Communs
se recentre sur les **terres libérées habitées**.

**Plan B** (futur site planb.org) est un projet frère, porté par la même voix
éditoriale. Sa vocation est inverse et complémentaire : non plus inventorier
les lieux existants, mais offrir une **bibliothèque de modèles reproductibles**
— des assemblages juridiques, gouvernanciels et économiques décrits dans le
détail, prêts à être adoptés par un collectif. Communs regarde *ce qui est*,
Plan B propose *ce qui se refait*.

Les deux sites partagent une grammaire — le triptyque usus/fructus/abusus, la
chaîne porteur/usufruitiers, la grille à cinq axes — et doivent partager une
**typologie commune des montages**. C'est l'objet de la session.

## 2. Le problème à trancher

La typologie 1bis actuelle (issue de la session #4 sur Communs) range les
montages en **six silhouettes** au niveau du `montage.type` du lieu :
`demembrement`, `propriete_protegee`, `propriete_publique`,
`propriete_collective`, `propriete_privee_individuelle`,
`propriete_privee_commerciale`.

Cette granularité convient à Communs : elle décrit le *mécanisme de
dissociation* sans présumer de la lucrativité (laquelle est portée par l'axe
orthogonal `nature_interet`). Elle ne suffit **pas** à Plan B, qui doit
nommer des sous-modèles concrétisables — un futur collectif veut savoir si le
modèle proposé est une SCI militante, une SCIC foncière, un GFA-Mutuel, une
foncière non-lucrative qui démembre vers un GAEC ou vers une association
d'usagers, etc.

Le problème est donc de **conserver une grille à six entrées partagée**, tout
en y greffant un **second niveau** opératoire pour Plan B, sans rompre la
lecture transversale.

## 3. Questions à arbitrer en session

1. **Granularité.** Adopte-t-on un schéma à deux niveaux — niveau 1 (les 6
   silhouettes, stables) + niveau 2 (sous-modèles concrétisables) — ou un
   schéma à trois niveaux (silhouette / famille de montage / variante locale) ?
   Coût d'entretien à mesurer ; la simplicité prime si la lecture le permet.
2. **Sous-modèles candidats.** Quels sous-modèles dégager sous chaque
   silhouette ? Inventaire de travail à conduire à plat :
   - sous `demembrement` : foncière militante → GAEC usufruitier ; foncière
     militante → association d'usagers ; foncière militante → SCIC ;
     démembrement à long bail emphytéotique sans cession d'usufruit ;
   - sous `propriete_collective` : SCI militante non lucrative ; SCIC
     foncière ; SCIC d'activité avec patrimoine immobilier ; GFA-Mutuel ;
     coopérative d'habitants Loi 47 ; société civile d'attribution ;
   - sous `propriete_protegee` : fonds de dotation foncier ; fondation
     reconnue d'utilité publique foncière ; fiducie de gestion (rare) ;
     association loi 1901 propriétaire avec engagements statutaires ;
   - sous `propriete_publique` : conservatoires (littoral, espaces naturels) ;
     domaine communal mis à disposition par convention ; propriété
     intercommunale ; achats publics avec affectation perpétuelle ;
   - sous `propriete_privee_individuelle` : propriété individuelle avec
     ORE ; bail emphytéotique de longue durée ; commodat (prêt à usage) ;
   - sous `propriete_privee_commerciale` : foncière privée avec bail rural
     environnemental ; SCI patrimoniale louant à un collectif.
3. **Reproductibilité.** Quels sous-modèles ne sont **pas** reproductibles —
   et donc restent décrits côté Communs mais ne figurent pas côté Plan B ?
   Candidats à écarter de Plan B : familles cultuelles (régime 1905 inaccessible
   à un collectif civil ordinaire), propriété privée individuelle (relève d'un
   choix biographique, non d'un modèle), fondations RUP à conseil captif
   (barrière de capital et de gouvernance prohibitive), modèles dépendants d'une
   législation locale rare.
4. **Surfaces de contact — mécanique.** Comment se nourrissent les deux sites ?
   Quatre asymétries productives à formaliser :
   - *cas Communs → modèle Plan B* : un lieu existant inspire l'écriture d'un
     modèle reproductible ;
   - *modèle Plan B → cas Communs* : un modèle de la bibliothèque est
     illustré par un ou plusieurs cas réels de Communs ;
   - *ratés Communs → garde-fous Plan B* : un effondrement documenté côté
     Communs (cf. revue mémoire) devient un avertissement explicite sur la
     fiche-modèle Plan B ;
   - *modes d'effondrement → fragilités du modèle* : la typologie des modes
     d'effondrement (succession ratée, faillite, scission, captation,
     dissolution volontaire, expropriation) — dégagée par la revue mémoire —
     se projette sur chaque modèle Plan B comme un éventail de risques
     spécifiques à anticiper.
5. **Attribut `reproductibilite` sur les fiches Communs.** Faut-il ajouter un
   champ `reproductibilite: elevee | moyenne | basse | specifique` aux fiches
   `lieu` ? Avantage : Plan B peut piocher mécaniquement les cas
   reproductibles pour illustrer ses modèles. Risque : attribut subjectif,
   instable, à arbitrer fiche par fiche, qui peut figer un jugement de valeur
   sur des situations en évolution. Une voie médiane — calculer la
   reproductibilité par déduction depuis le sous-modèle (niveau 2 de la
   typologie) — éviterait la saisie au cas par cas.
6. **Implémentation des liens croisés.** URLs stables (`/sous-modeles/<slug>`
   côté Communs, `/modeles/<slug>` côté Plan B) ; fichier de mapping
   `config/mapping-planb.yml` côté Communs ; API simple à exposer (un JSON
   `/sous-modeles.json` servi par le générateur, lu par Plan B au build) ?

## 4. Premier pas concret

Avant d'entrer dans le câblage technique, la session doit produire le
**document de référence** : `config/typologie-partagee.yml` (ou
`concepts/typologie-partagee.yml`). Structure attendue :

- six entrées de **niveau 1** (les silhouettes 1bis), chacune avec `slug`,
  `label`, `definition`, `mecanisme_de_dissociation` ;
- une quinzaine à une vingtaine d'entrées de **niveau 2** (sous-modèles),
  chacune avec `slug`, `label`, `parent` (niveau 1), `perimetre`,
  `reproductible: oui|non|specifique`, `motif` (si non reproductible),
  `exemples_communs` (uids de lieux), `fiche_planb` (slug du modèle Plan B
  quand il existera).

## 5. Matériau d'entrée

- Les 6 silhouettes 1bis et leur définition (cf. `brief-cadre-conceptuel-
  communs.md` §6 et `etat-projet-communs.md` §3).
- Les 45 lieux du corpus avec leur `montage.type` et leur bloc structuré
  `articulations:` / `liants:` — la matière première pour identifier les
  sous-modèles effectivement observés.
- Les notes textuelles des fiches sur les variantes — souvent le travail
  ethnographique a déjà nommé un sous-modèle qu'il suffit de remonter.
- Les cinq modèles voisins (`modeles/`) — déjà des candidats sous-modèles
  potentiels.

## 6. Prérequis et calendrier

Aucun prérequis technique. Session conceptuelle pure, qui produit un YAML
discuté ligne à ligne. Les quatre revues fraîchement créées (greenwashing,
loi-1905, sanctuaires-de-retrait, mémoire) bénéficieraient d'avoir leur
premier article publié au moment de la session — pour matérialiser les
distinctions de périmètre — mais ce n'est pas un bloquant : la typologie
partagée se construit d'abord depuis le corpus existant.

## 7. Sortie attendue

Un fichier `config/typologie-partagee.yml` complet, ses six niveaux 1 et ses
quinze à vingt-cinq niveaux 2, validé en clôture de session. Trois décisions
de méthode tranchées et journalisées en `lecons-communs.md` : (i) le statut
de l'attribut `reproductibilite`, (ii) la mécanique exacte des surfaces de
contact, (iii) le format d'échange entre les deux générateurs.

Suit, en session ultérieure, le câblage côté Communs (rattachement des 45
fiches aux sous-modèles) puis le démarrage de l'ossature Plan B.
