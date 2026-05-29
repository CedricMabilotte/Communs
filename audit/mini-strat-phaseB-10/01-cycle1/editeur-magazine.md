# Voix — Éditeur·rice magazine (cycle 1, mini-strat phase B, session #10)

*Volet isolé. Critère propre : récit, accroche, partageabilité — la capacité
d'un contenu à être lu, compris, relayé. Public visé : un·e lecteur·rice de
Reporterre/Mediapart, un·e militant·e qui partage, un·e curieux·se happé·e par
une histoire. Thèse de la voix : un annuaire-tableau ne suffit pas ; certains cas
portent un enseignement qui ne passe que par le récit.*

---

## 1. Ce qui manque éditorialement aujourd'hui — le tableau ne raconte pas

Le site est déjà beau et juste. La fiche Pommiers, désormais `hybride` (le piège
GAEC est réparé), est honnête, sourcée, lisible pour qui sait lire un radar. Mais
elle ne **raconte rien**. Elle donne un état ; elle ne donne pas un parcours.

Quatre manques concrets, du point de vue de la circulation :

- **Aucun point d'entrée par l'histoire.** Tout est entrée par la *catégorie*
  (porteur / usufruitier / lieu) ou par le *chiffre* (classement). Or personne ne
  partage un radar à cinq axes sur Bluesky. On partage : « une famille a *donné*
  sa ferme pour qu'elle ne soit jamais revendue — voilà comment ». Le corpus
  contient des dizaines de ces histoires, toutes pilées en lignes de tableau.

- **L'enseignement transversal est invisible.** Le site sait des choses que
  *aucune fiche prise seule* ne dit : que la libération aboutie est rarissime (le
  palier « aboutie » est à zéro dans l'histogramme) ; que les libérations sont
  défensives et périphériques, jamais sur des terres riches ; que deux montages au
  même Indice 82 (Mhotte, Larzac) racontent des trajectoires opposées. Ce savoir
  est *dans* le corpus mais n'est écrit nulle part.

- **La dissonance verdict/Indice/palier reste un mur.** Le `<details>` « Comment
  lire cette fiche » l'explique correctement, mais en mode notice technique. Un·e
  journaliste pressé·e voit « Montage hybride · Indice 64 · Montage solide » et
  décroche. Le récit est précisément l'outil qui *dissout* la dissonance : raconter
  *pourquoi* Pommiers est hybride sans être marchand, c'est rendre la mécanique
  intuitive sans encart.

- **Le grand public n'a aucune porte chaude.** L'accueil ouvre sur « La terre,
  soustraite au marché » puis enchaîne sur « Comment lire cet annuaire » : c'est un
  mode d'emploi, pas une invitation. La première émotion possible (l'étonnement
  qu'on *puisse* faire ça) n'est jamais sollicitée.

Le diagnostic n'est pas que le catalogue est mauvais — c'est qu'il est **mono-régime**.
Tout y est en voix exacte, tout y est symétrique. Il manque le second régime :
le récit, qui sélectionne, hiérarchise et incarne.

## 2. Le format magazine proposé

Je propose **trois objets éditoriaux**, du plus léger au plus lourd, reliés au
catalogue par un principe simple : *le magazine donne envie, le catalogue donne
raison*. On entre par l'histoire, on vérifie sur la fiche.

**(a) Le hook intégré à la fiche** — *coût nul, gain immédiat.*
Une phrase d'accroche narrative en tête de chaque fiche, sous le sous-titre, dans
le champ déjà existant `en_clair` / voix incarnée. Pas un résumé : une *prise*.
Pour Pommiers : non pas « ferme ovine sécurisée par donation », mais ce que ce
montage a *changé* — une ferme qui ne repartira jamais à la découpe immobilière,
parce que deux éleveur·ses ont préféré la donner que la vendre. Le hook ne note
pas, ne moralise pas, ne déduit rien que la fiche ne sourcerait pas. Il
**éclaire le même fait sous l'angle de l'enjeu humain**.

**(b) La fiche-récit (dossier)** — *l'objet magazine central.*
Un dossier long (1200–2200 mots) dans `site/dossiers/`, en voix incarnée
dominante, qui raconte un cas-pivot : la genèse, l'obstacle, le montage comme
*solution à un problème concret*, et — c'est la clé — *ce que le verdict révèle*.
Chaque dossier porte un **lien retour bidirectionnel** : un encart « la fiche
chiffrée » en bas du dossier (vers `l/...`), et un bandeau « lire l'histoire de ce
lieu » en tête de la fiche-catalogue correspondante. Le dossier ne **duplique
jamais** la grille : il l'incarne. Là où la fiche dit « axe 2 plafonné à 40 par la
chaîne », le dossier dit pourquoi un bail rural sous une fondation, ce n'est pas la
même chose qu'une SARL propriétaire — en une scène, pas en glose.

**(c) Le dossier-comparaison (essai de corpus)** — *l'enseignement transversal.*
Un format rare (2–3 par an), qui ne raconte pas *un* lieu mais une *lecture du
corpus* : « Pourquoi la libération aboutie n'existe (presque) pas encore »,
« Deux fermes, un même 82, deux mondes ». Il s'appuie sur les chiffres réels du
corpus, ne les invente pas, et renvoie vers 4–6 fiches. C'est le format le plus
puissant pour la presse, car il *donne un angle* qu'un·e journaliste peut reprendre.

**Articulation au catalogue symétrique.** Le magazine **ne touche pas** la
symétrie du catalogue : toutes les fiches gardent le même gabarit, le même calcul,
le même rang. Le magazine est une **surcouche de chemins** — un sous-ensemble de
lieux reçoit *en plus* un récit. La règle anti-biais : être dossier-récit n'élève
jamais l'Indice ni le rang d'un lieu ; un encart « ce lieu a un dossier » est un
fait éditorial, pas une distinction de qualité. On dit « raconté », jamais
« remarquable ».

## 3. Les cinq cas-pivot recommandés

Chaque cas est retenu pour un **enseignement distinct** — pas pour son score.

1. **La Ferme de Pommiers** — *le cas qui apprend à lire le verdict.* Hybride sans
   être marchand : le récit qui désamorce la dissonance verdict/Indice et montre
   qu'« hybride » est légitime, non condamné. Cas-école obligatoire.

2. **Le Rayol** (le sanctuaire abouti) — *le cas qui montre le sommet réel.* Seul
   lieu à atteindre le verdict `sanctuaire` ; il incarne ce que « aboutie »
   veut dire concrètement, et pourquoi c'est si rare. Indispensable pour donner
   un visage au palier vide de l'histogramme.

3. **Les Terres du Larzac** — *le cas qui sépare le mythe du montage.* L'histoire
   politique est connue ; le montage juridique (propriété publique inaliénable
   gérée par une société civile) l'est beaucoup moins. Le récit corrige le mythe
   par le réel chiffré, sans mythifier (cf. arbitrage §5.3 de la synthèse : pas de
   survalorisation, traitement égal + encart historique).

4. **L'Eau du Bassin Rennais** — *le cas qui élargit hors de l'écolieu.* Une
   collectivité publique qui achète des terres agricoles pour protéger l'eau
   potable : la libération foncière comme politique publique ordinaire, loin de
   l'imaginaire militant. Décisif pour la cible « décideurs » et pour montrer que
   le sujet n'est pas marginal.

5. **Notre-Dame-des-Landes — l'Assemblée des usages** (5ᵉ à arbitrer, ma
   recommandation) — *le cas qui montre la libération comme conquête, pas comme
   don.* Une terre arrachée par la lutte puis dotée d'un montage juridique
   (fonds de dotation « La Terre en commun ») : la seule trajectoire bottom-up du
   top du corpus. Elle complète Pommiers (donation), Rayol (sanctuaire),
   EBR (public) par le registre du *commun conquis*. Alternative possible si on
   veut un hybride exemplaire plutôt qu'une lutte : un montage Fondation RUP + GAEC
   bio second, mais NDDL apporte une diversité de *registre* que les autres n'ont
   pas. À trancher en cycle 2 avec la voix « gardien de la rigueur » (risque :
   NDDL est politiquement chargé).

*Note de prudence : les Indice et verdicts cités proviennent du rendu actuel
(index, fiche Pommiers). Tout dossier doit être recalé sur la fiche au moment de
la rédaction — aucun chiffre inventé.*

## 4. La voix éditoriale

Le brief §12 fournit déjà l'instrument : **le double registre**. Le magazine n'a
pas besoin d'une *nouvelle* voix — il **rééquilibre les deux existantes**.

- **Dans le catalogue**, la voix exacte domine, la voix incarnée fait l'appoint
  (une phrase `en_clair` par section). C'est l'état actuel, à conserver.
- **Dans le magazine**, on inverse : la **voix incarnée domine** (ce que le montage
  change dans une vie, un territoire, un paysage), et la voix exacte revient en
  *ancres* — un terme juridique encadré, un renvoi au glossaire, une donnée
  sourcée. Le récit porte ; la rigueur jalonne.

Registre : journalistique de fond, sobre, factuel-chaud. Ni le ton militant
(« scandaleux ! »), ni le ton notice (« le dispositif susmentionné »). Le modèle
mental est le reportage de fond de Reporterre : on raconte des gens et des
décisions, on cite des faits vérifiés, on ne conclut pas à la place du lecteur.

**Qui parle ?** Une voix éditoriale unique et anonyme — celle du site, non un·e
auteur·rice signé·e. Pas de « je ». La signature est institutionnelle (« Terres
Libérées »), ce qui maintient la continuité avec le catalogue et évite le
glissement vers le blog d'opinion. Garde-fou cardinal, repris du §12 : **la voix
incarnée ajoute chaleur et concret ; elle ne remplace jamais la rigueur et ne
moralise jamais. Un hook qui ment a échoué.** Toute affirmation d'un dossier doit
être traçable à une source de la fiche ; un dossier ne peut rien dire que la fiche
ne pourrait sourcer.

## 5. Éléments constitutifs apportés

### Gabarit de fiche-récit (dossier)

```
TITRE — accroche narrative, pas le nom administratif
       (ex. « La ferme qu'on a préféré donner que vendre »)
CHAPÔ  — 2–3 phrases : l'enjeu, en voix incarnée. Le hook étendu.
§ Le problème     — ce qui menaçait (spéculation, déprise, départ en retraite…)
§ Le montage      — la solution juridique racontée comme une décision, pas un schéma
                    (ancres voix exacte vers glossaire : donation, bail rural, RUP…)
§ Ce que ça change — le concret : qui vit là, ce qui ne pourra plus arriver
§ Ce que le verdict dit — où se tient le lieu, et pourquoi (désamorce la dissonance)
ENCART « La fiche chiffrée » — lien vers l/<slug>.html + Indice + verdict + radar compact
SOURCES — héritées de la fiche, + sources tierces si dossier (presse, recherche)
```

Contraintes : 1200–2200 mots ; voix incarnée dominante ; zéro chiffre non présent
sur la fiche ; lien retour obligatoire ; pas de qualificatif interne dans le titre
ou le slug (jamais « pilote », « puriste », « cas-école »).

### Liste de hooks-types (familles d'accroche réutilisables)

- **Le don** — « Plutôt que de vendre, ils ont donné. » (Pommiers)
- **La conquête** — « La terre, on l'a d'abord arrachée ; le droit est venu après. » (NDDL)
- **Le verrou** — « Cette terre ne pourra plus jamais être revendue. » (porteurs inaliénables)
- **L'eau / le bien commun concret** — « Pour protéger l'eau du robinet, une ville a acheté des champs. » (EBR)
- **Le sommet rare** — « Sur tout l'annuaire, un seul lieu touche au bout. » (Rayol)
- **L'écart** — « Même note, deux mondes. » (dossier-comparaison)
- **Le mythe corrigé** — « Tout le monde connaît le nom ; presque personne ne connaît le montage. » (Larzac)

Règle d'emploi : un hook est une *porte d'entrée vraie*, jamais une promesse que le
corps ne tient pas. Si le fait n'est pas sourcé, le hook tombe.

## 6. Désaccords prévus avec les autres voix

- **Avec l'architecte d'information (symétrie vs hiérarchisation).** Désaccord
  central, annoncé par le périmètre (1×2). L'architecte voudra protéger la
  symétrie exhaustive et craindra que le magazine crée un *classement déguisé*. Ma
  position de compromis : le magazine est une **surcouche de chemins**, jamais une
  ré-ordonnance du corpus ; le catalogue reste plat, symétrique, complet ; aucun
  Indice ni rang n'est altéré par l'existence d'un dossier. Le mot « raconté »
  remplace tout mot de mérite. Point de friction résiduel : faut-il afficher les
  dossiers en accueil (moi : oui, c'est leur fonction d'accroche) ou les reléguer
  dans une section dédiée non mise en avant (architecte probable) ?

- **Avec le gardien de la rigueur (hooks vs sobriété citable).** Il craindra que
  l'accroche déforme, que la voix incarnée contamine le verdict, qu'un dossier
  devienne plaidoyer. Je le rejoins entièrement sur le principe — *un hook qui ment
  a échoué* — et je propose un garde-fou opérant : **traçabilité fiche→dossier**
  (aucune affirmation hors source de fiche) et **revue du gardien sur chaque
  dossier avant publication**. Friction résiduelle : le 5ᵉ cas-pivot. NDDL est
  politiquement chargé ; le gardien préférera un hybride neutre. À trancher.

- **Avec le/la lecteur·rice cible (presse/décideur).** Convergence large, mais
  désaccord de dosage : la voix presse voudra peut-être *moins* de chaleur et
  *plus* de données dures (chiffres fonciers, hectares, montants). Je tiens que le
  récit reste le véhicule, mais j'accepte d'enrichir le gabarit d'un encart
  « repères chiffrés » pour la cible décideur — sans en faire le cœur.

- **Avec le/la méthodologue du modèle.** Pas de conflit direct (le magazine ne
  touche pas le moteur), mais une vigilance partagée : le dossier doit refléter le
  *calcul réel*, pas une version simplifiée du verdict. Si le calcul change, les
  dossiers se recalent. Le magazine est aval, jamais source.

---

*Fin du volet Éditeur·rice magazine — cycle 1, isolé.*
