---
slug: forets-en-vie
nom: Forêts en vie (fonds de dotation du RAF) — forêt de Haute-Loire / Sous lou boès
cree: '2026-11-08'
dernier_repere: '2026-11-08'
score_cumule: 0
sources_vues:
- source: socialter
  date: '2023-01-27'
  url: https://www.socialter.fr/article/rachat-foret-bioviersite-reseau-alternatives-forestieres
  titre: Racheter des forêts pour les garder en vie — C. Granja, Socialter HS15
  score: 0
- source: socialter
  date: '2023-11-06'
  url: https://www.socialter.fr/article/propriete-commune-alternatives-propriete-privee
  titre: 'Propriété commune : 4 pistes pour dépasser la propriété privée — C. Vinet, Socialter n°61'
  score: 0
- source: reporterre
  date: '2019-00-00'
  url: https://reporterre.net/Le-fonds-de-dotation-une-breche-dans-la-conception-francaise-de-la-propriete-prive
  titre: Le fonds de dotation, une brèche dans la conception française de la propriété privée — Reporterre
    (date à confirmer, ~2019)
  score: 0
indices_structurels:
  nom_propre: true
  localisation: true
  entite_juridique: true
  montage_explicite: true
  siren: false
  geoportail_localisable: false
extracted:
  nom: Forêts en vie (fonds de dotation du RAF) — forêt de Haute-Loire / Sous lou boès
  localisation:
    departement: Haute-Loire, Lot, Corrèze, Creuse
  formes:
  - fonds_dotation
  - association
  siren:
    siren: []
    siret: []
  montage_type: null
statut: actif
origine: 'graine manuelle — session #13 (2026-11-08), dépouillement presse Socialter HS15 / Reporterre'
---

# Lead — Forêts en vie (fonds de dotation du RAF) — forêt de Haute-Loire / Sous lou boès

Graine posée à la main (session #13) à partir du dépouillement presse ; score 0 tant que la veille automatique ne l'a pas recroisé.

## Notes
Fonds de dotation du Réseau pour les alternatives forestières (RAF), lancé fin 2017,
coordonné par Nathalie Naulet (ex-ONF). Achète des forêts et les confie à des associations
pour une sylviculture douce : forêt de moyenne montagne en Haute-Loire confiée à
l'association Sous lou boès ; 54 ha acquis en deux ans (Lot, Corrèze, Haute-Loire, Creuse)
à la date de l'article de nov. 2023 ; une acquisition « 76 propriétés » en cours (site non
nommé).

Pertinence : forte — porteur hors marché (fonds de dotation) + usufruitier associatif +
finalité vivant (forêt) ; comble l'angle « forêt » du corpus (étude Enjeux forêt sans lieu
associé [SUPPOSÉ]). Créer deux entités : porteur `forets-en-vie` + lieu (forêt Haute-Loire).
Vérifier : statuts (dotation non consomptible ?), nature du titre confié (bail, commodat,
convention), commune et surface de la forêt.

## Qualification (2026-11-08, communs-veille-qualifier)

**Entité porteuse.** Fonds de dotation « Forêts en vie », créé à l'initiative du
Réseau pour les alternatives forestières (RAF) — [page HelloAsso](https://www.helloasso.com/associations/forets-en-vie/),
RAF lui-même association loi 1901 ([HelloAsso RAF](https://www.helloasso.com/associations/reseau-pour-les-alternatives-forestieres)).
SIREN/RNA non trouvés dans les sources consultées (à chercher sur annuaire-entreprises.data.gouv.fr
ou JOAFE — non fait, hors délai de cette passe).

**Montage.** Le fonds achète des parcelles forestières et les met à disposition
d'associations par des baux de 15 ou 99 ans ([ffrandonnee.fr, 18/07/2021](https://www.ffrandonnee.fr/s-informer/actualites/forets-en-vie-premier-fonds-de-dotation-dedie-a-la-foret-en-france)).
C'est un mécanisme explicite de dissociation nue-propriété/usage avec bail long —
proche du schéma `propriete_protegee` déjà utilisé pour NDDL/La Talvère.

**Lieu précis non identifié.** Les sources consultées (ffrandonnee, Socialter,
helloasso) ne nomment aucune forêt précise avec sa commune : « forêt de moyenne
montagne en Haute-Loire » (Socialter) sans toponyme, confiée à l'association Sous
lou boès — introuvable par recherche web (aucune présence en ligne distincte
trouvée, nom possiblement mal retranscrit par l'article). 54 ha acquis en deux ans
dans le Lot, la Corrèze, la Haute-Loire et la Creuse (Socialter, nov. 2023),
toujours sans toponyme.

**Verdict pressenti.** Montage éligible dans son principe (fonds de dotation +
bail long explicite), mais **empreinte publique insuffisante pour un lieu précis**
au sens de la règle #11 : on peut documenter le porteur (`forets-en-vie`, catégorie
`porteurs/`) mais pas un `lieu` nommé et localisable. Recommandation : créer la
fiche porteur seule (sans fiche lieu) si Ced le souhaite, ou rouvrir quand une
forêt précise sera identifiable (toponyme + commune). Pré-fiche **non recommandée**
en l'état.

**Checker.** Aucune donnée fabriquée ; le nom « Sous lou boès » n'a pas pu être
revérifié indépendamment de l'article Socialter — à traiter comme non confirmé.
