# Chantiers de phase 2 — qualification fine

*Session #8d, mai 2026. Qualification opérationnelle des chantiers de phase 2 issus de la revue éditoriale à trois voix. À lire après `03-synthese.md`.*

---

## Méthode de qualification

Chaque chantier est qualifié sur sept dimensions :

- **Enjeu** : ce qui est en jeu — pourquoi le chantier existe.
- **Origine** : voix(s) qui le portent (universitaire / journaliste / influenceur), niveau de convergence.
- **Recommandation** : action proposée, formulée concrètement.
- **Périmètre** : ce qui est inclus, ce qui ne l'est pas.
- **Effort** : *léger* (1-2 demi-journées), *moyen* (3-7 demi-journées), *lourd* (8+ demi-journées).
- **Dépendances** : autres chantiers à traiter en amont ou en parallèle.
- **Décision opérateur** : ce qu'il/elle doit trancher avant exécution.

Les chantiers sont regroupés en quatre familles :

- **A — Socle conceptuel et méthode** (réparations de fond).
- **B — Lisibilité et navigation** (chantiers d'interface et de pédagogie).
- **C — Diffusion et amplification** (chantiers de portée).
- **D — Hygiène et versionnage** (chantiers de propreté du rendu).

Et hiérarchisés en trois priorités :

- **P1 — À traiter en premier** (bloquants pour la cohérence du projet).
- **P2 — À traiter ensuite** (importants, dépendants partiellement de P1).
- **P3 — À planifier** (utiles, pas urgents).

---

## P1 — Chantiers prioritaires (à traiter en premier)

### A1 — Réparer le piège GAEC / la qualification des sociétés civiles agricoles

**Enjeu** : Le ranger un GAEC en `commerciale` (lucrativité ouverte) produit aujourd'hui un verdict **marchand** sur des montages Fondation RUP + GAEC bio. C'est juridiquement contestable (un GAEC est une société *civile* agricole, pas une SARL), politiquement contre-productif (criminalise la quasi-totalité de l'agriculture paysanne française), et médiatiquement désastreux (la Ferme de Pommiers a été tagguée *Montage marchand* alors que sa chaîne entière est non lucrative).

**Origine** : Convergence des trois voix — l'universitaire pose le diagnostic juridique, le/la journaliste l'amplifie politiquement, l'influenceur l'amplifie médiatiquement.

**Recommandation** : Distinguer dans `nature_interet` une catégorie nouvelle `commerciale_agricole_civile` (ou `non_lucrative_agricole` selon arbitrage) qui s'applique aux GAEC, EARL, SCEA non spéculatives, et qui ne plafonne pas l'axe 2 à 20 mais à une valeur intermédiaire (à calibrer — sans doute 60-70). Refondre le verdict pour qu'un montage Fondation RUP + GAEC bio puisse atteindre *hybride* voire *sanctuaire* selon les autres axes, et non pas *marchand* mécaniquement.

**Périmètre** : Modification de `config/concepts.yml` (catégorie `nature_interet`), `config/ranking.yml` (plafond de chaîne), et passage de revue des 30+ fiches portant une chaîne avec un GAEC pour ajuster la qualification. Hors périmètre : reconfiguration globale de la trichotomie verdict (cf. A4).

**Effort** : Moyen (3-5 demi-journées) — calibrage + passe d'hygiène sur le corpus.

**Dépendances** : Aucune en amont. Bloque A4 (mécanisme verdict×palier).

**Décision opérateur** : Quel **plafond exact** pour la nouvelle catégorie (50 ? 60 ? 70 ?) — c'est une décision d'orientation politique, pas technique. Et : faut-il **étendre** à d'autres formes agricoles (SCEA, EARL, CUMA) avec le même traitement ?

---

### A2 — Refondre le critère « vivant non-humain »

**Enjeu** : Le critère pénalise les lieux qui *font sans le dire* (élevage ovin bio en moyenne montagne reçoit deux « non » sur `milieu_protege` et `vivant_finalite`), et avantage les lieux qui *thématisent* (un écolieu qui parle d'« oasis de biodiversité » reçoit « oui » même sans pratique attestée). Biais sociolinguistique de classe — les paysan·nes pratiquent, les militant·es urbain·es théorisent.

**Origine** : Convergence forte — universitaire pose le diagnostic, journaliste l'amplifie politiquement, influenceur reconnait son angle mort dans la réaction.

**Recommandation** : Refondre le critère en deux temps. D'abord, **dégrouper** : distinguer `pratique_cohabitation` (factuelle — élevage extensif, fauche tardive, abandon partiel d'intrants, etc., qui peut être attestée même sans formulation explicite) et `discours_cohabitation` (revendiqué — charte, plan de gestion écologique, etc.). Ensuite, **pondérer** : la pratique attestée vaut autant que le discours, le discours sans pratique vaut moins que la pratique sans discours.

**Périmètre** : Modification de `config/grilles.yml` (critères de l'axe), du barème de cotation (rubriques `milieu_protege`, `vivant_finalite`, `place_au_vivant`), et passage de revue des fiches concernées. Hors périmètre : refondre l'axe 5 en entier (cf. A5).

**Effort** : Moyen (3-5 demi-journées).

**Dépendances** : Aucune en amont. Peut être traité en parallèle de A1.

**Décision opérateur** : Faut-il **deux critères distincts** (pratique + discours) ou **un critère composite** qui pondère les deux ? Et : faut-il accepter des **sources tierces** (presse, naturalistes, OFB) pour attester d'une pratique non documentée par le porteur ?

---

### B1 — Carte de France des lieux

**Enjeu** : Les 45 lieux sont géolocalisés (lien Géoportail sur chaque fiche), mais aucune vue cartographique d'ensemble n'existe. Triple manque : (a) outil cognitif perdu (la géographie politique des libérations n'est pas lisible), (b) hook éditorial absent (une carte est le premier visuel partagé pour ce type de projet), (c) navigation alternative au catalogue textuel absente.

**Origine** : Convergence forte — porté par l'influenceur initialement, amplifié par les deux autres en réaction.

**Recommandation** : Page `site/carte.html` autonome, avec carte interactive Leaflet (sans dépendance lourde), un marqueur par lieu, popup avec nom + verdict + lien fiche. Symétrie : un marqueur par lieu, pas de hiérarchisation visuelle (cf. tension §5.1 de la synthèse). Lien depuis la page d'accueil et le catalogue. Responsive mobile.

**Périmètre** : Génération HTML/JS de la carte ; intégration au générateur `scripts/generate_site.py` ; pas de modification du schéma de fiche. Hors périmètre : carte des porteurs / usufruitiers / réseaux (à voir en P2).

**Effort** : Moyen (4-6 demi-journées) — le générateur et Leaflet sont maîtrisables, l'effort est dans le design et le responsive.

**Dépendances** : Aucune en amont. Peut être traité en parallèle de A1-A2.

**Décision opérateur** : (a) couleurs des marqueurs : par **verdict** (marchand rouge / hybride orange / sanctuaire vert), par **palier** (rouge à vert sur l'échelle), ou monochrome neutre ? — choix éditorial fort. (b) **catalogue secondaire** par région (visualiser tous les lieux d'une région) — à inclure ou à différer ?

---

### A3 — Rendre lisible la mécanique verdict × palier × Indice

**Enjeu** : Sur la fiche Pommiers, le lecteur voit le bandeau « Montage marchand » + l'Indice 56 + le palier « Engagement réel ». Trois informations qui se contredisent sans explication visible. La mécanique sous-jacente (plafond de chaîne, palier réservé à verdict sanctuaire, etc.) est dans le code, pas dans la fiche.

**Origine** : Convergence forte des trois voix.

**Recommandation** : Sur chaque fiche, ajouter un **encart « comment lire ces trois chiffres »** qui explicite la mécanique de manière concise (50-80 mots). Sur la page Méthode, dédier une section claire à la trichotomie verdict × palier × Indice, avec un exemple sourcé (idéalement Pommiers). Pas de modification du calcul — chantier de rendu.

**Périmètre** : Modification de `scripts/generate_site.py` (fonction `render_fiche`), ajout d'une section dans `site/methode.html`. Hors périmètre : modification du calcul lui-même (cf. A1).

**Effort** : Léger (1-2 demi-journées).

**Dépendances** : Idéalement après A1 (pour ne pas expliquer une mécanique qu'on va changer).

**Décision opérateur** : Faut-il afficher l'**encart pédagogique sur toutes les fiches** ou seulement en survol / pliable ? Risque : si toujours visible, alourdit les fiches ; si pliable, peu de lecteur·rices le déploieront.

---

### D1 — Versionnage public et hygiène des cicatrices

**Enjeu** : Les références internes — *refonte #3*, *chantier 1bis*, *session #5*, *cycle D* — apparaissent dans la prose des pages publiques (page Méthode, certaines fiches). Ces inserts sont des micro-signaux d'amateurisme : l'auteur·rice travaille en public mais ne nettoie pas. Un·e enseignant·e ne peut pas citer le site comme version stable.

**Origine** : Convergence forte.

**Recommandation** : 
1. Définir un schéma de **versionnage public** : version majeure (1.0, 2.0…) annuelle ou semestrielle, mineure (1.1, 1.2…) par lots de modifications, indiquée en pied de page de chaque page.
2. **Journal des changements** public (`site/changelog.html`) qui résume les évolutions majeures sans le détail interne.
3. **Passe de nettoyage** : retirer toutes les mentions « refonte #3 », « chantier X », « session #N » du contenu public (les laisser dans `etat-projet-communs.md` qui reste interne, ou dans une page « histoire du projet » dédiée).

**Périmètre** : Passage de revue des pages publiques + ajout d'un fichier `changelog.html` + intégration de la version au générateur.

**Effort** : Moyen (3-5 demi-journées) — la passe de nettoyage est la partie longue.

**Dépendances** : Aucune en amont. À traiter avant la diffusion publique élargie (P2 newsletter etc.).

**Décision opérateur** : (a) garder ou non une **page « histoire du projet »** qui assume la trajectoire (refontes successives) en tant que récit, plutôt que la cacher. (b) **fréquence** des versions majeures : annuelle (lourd) ou semestrielle (souple).

---

## P2 — Chantiers de seconde vague (à traiter ensuite)

### A4 — Reformulation du déni de jugement

**Enjeu** : La formule récurrente « pas un jugement de valeur » est maladroite (le verdict *marchand* est manifestement un jugement) mais elle porte une intuition juste — la grille n'est pas un tribunal moral. Ne pas la supprimer ; la reformuler.

**Origine** : Universitaire pour la reformulation, journaliste pour la prise de position assumée (tension §3.2). Convergence sur la nécessité du chantier, divergence sur sa direction.

**Recommandation** : Remplacer « pas un jugement de valeur » par une formulation qui assume **l'évaluation comme méthode** : « une évaluation au regard d'un cadre explicite — celui de la libération comme dissociation propriété/usage. Le cadre est défendable, contestable, perfectible ; le résultat l'est aussi. » Ajouter sur la page Méthode une section **« limites assumées »** : ce que la grille voit mal, ce qu'elle rate, où elle est calibrée a posteriori.

**Périmètre** : Modification de la prose des pages Méthode, Accueil, Régimes. Pas de modification du calcul.

**Effort** : Léger (1-2 demi-journées).

**Dépendances** : Idéalement après D1 (pour ne pas réécrire dans un texte qu'on va nettoyer ensuite).

**Décision opérateur** : Quel **degré de prise de position politique** assumer en page d'accueil ? La formule « éducation populaire / mouvements citoyens non-commerciaux » (déjà présente en p. Méthode §8) doit-elle remonter en accueil, et avec quels mots ?

---

### C1 — Traitement des absents structurants

**Enjeu** : L'écosystème français du foncier inclut des acteurs majeurs sous-traités ou absents : **ASPAS** (hébergée dans la revue sanctuaires-de-retrait mais sans lien depuis le corpus principal), **OFS-BRS** (traités comme modèle voisin mais sans fiche-tutoriel pédagogique forte), **SAFER** (totalement absent malgré leur rôle structurant dans l'acquisition foncière), **CEN-Conservatoires** (le Conservatoire du littoral est fiché, mais le réseau des CEN régionaux mériterait une cartographie).

**Origine** : Journaliste pose le diagnostic, universitaire valide en réaction, influenceur amplifie en termes de relais perdus.

**Recommandation** : 
- *ASPAS* : créer un porteur miroir dans le corpus principal qui pointe vers la revue sanctuaires-de-retrait. La distinction habiter/retrait reste tenue, mais le lecteur peut entrer par l'annuaire principal et naviguer.
- *SAFER* : créer une fiche `modeles/safer.yml` qui traite le rôle des SAFER comme « outil d'État sous-utilisé » dans la libération — leur droit de préemption pourrait être mobilisé bien plus pour des montages alternatifs.
- *OFS-BRS* : la fiche `ofs-brs.yml` existe (chantier 1bis) ; ajouter un **encart pédagogique** sur le mécanisme et un lien depuis l'accueil vers la fiche pour signaler son importance.
- *CEN régionaux* : créer un réseau `reseaux/federation-cen.yml` agrégeant les conservatoires d'espaces naturels au-delà du Conservatoire du littoral.

**Périmètre** : 3-4 fiches nouvelles + ajustement des liens depuis l'accueil.

**Effort** : Moyen à lourd (5-8 demi-journées selon profondeur).

**Dépendances** : A1, A2 (les nouvelles fiches doivent utiliser le critère vivant refondu et la qualification GAEC corrigée).

**Décision opérateur** : Faut-il une **section « écosystème » dédiée** sur l'accueil (« les acteurs structurants à connaître »), ou les fiches sont-elles laissées dans le corpus général ?

---

### B2 — Section magazine / fiches-récit

**Enjeu** : Le corpus est riche de cas qui mériteraient un récit éditorial plus long que la fiche-tableau. Pommiers, Rayol, Larzac, Mhotte, EBR — autant de cas qui contiennent un enseignement qui ne se transmet pas dans la grille.

**Origine** : Journaliste et influenceur portent le chantier ; universitaire l'accepte sous condition de partition claire d'avec le catalogue (cf. tension §5.1 de la synthèse).

**Recommandation** : Créer une section `site/dossiers/` (ou similaire) avec **5 fiches-récit** de 1500-2500 mots chacune sur des cas-pivot. Format : voix incarnée, journalistique, qui complète la fiche-tableau sans la remplacer. Chaque dossier porte un lien retour vers la fiche-catalogue, et inversement.

**Périmètre** : 5 dossiers à rédiger ; ajout d'une section au générateur ; lien depuis l'accueil.

**Effort** : Lourd (8-12 demi-journées — la rédaction est la partie longue).

**Dépendances** : A1 (pour que Pommiers soit correctement caractérisé avant qu'on raconte son histoire), D1 (pour ne pas exposer les cicatrices dans les dossiers).

**Décision opérateur** : (a) **quels 5 cas** retenir comme pivot ? Pommiers est évident, Rayol est évident (seul sanctuaire abouti), Larzac mérite un traitement, EBR pour le portage public. Le 5ᵉ est à arbitrer (Mhotte avec contexte anthroposophique, ou Berquet/Antidote pour un montage hybride réussi). (b) **voix éditoriale** : Eozen (la voix existante) ou une voix journaliste à différencier ?

---

### B3 — Sourçage des fiches au-delà des porteurs

**Enjeu** : La fiche Pommiers cite deux URL Terre de Liens et rien d'autre. Pour un projet qui se dit *annuaire critique*, l'absence de sources tierces est une lacune. Un·e chercheur·euse, un·e journaliste, un·e enseignant·e attend des sources scientifiques (publications du LADYSS, du PUCA, etc.) ou journalistiques (Reporterre, Le Monde, etc.).

**Origine** : Universitaire pose le diagnostic.

**Recommandation** : Sur les 10-15 fiches les plus structurantes, ajouter un bloc `dossier.sources_tierces:` distinct des sources auto-déclarées du porteur, avec liens vers presse, recherche académique, rapports publics. Sur les autres fiches, à compléter au fil de l'eau.

**Périmètre** : Modification du schéma de fiche (champ `sources_tierces` sous `dossier:`) ; passage de revue des 10-15 fiches prioritaires.

**Effort** : Moyen à lourd (6-10 demi-journées — recherche par fiche).

**Dépendances** : Aucune en amont.

**Décision opérateur** : (a) **liste des 10-15 fiches prioritaires** à traiter d'abord. (b) faut-il intégrer ces sources au **pipeline de veille** (les ajouter aux sources scannées automatiquement) ?

---

### C2 — OG images et métadonnées de partage

**Enjeu** : Quand une fiche est partagée sur les réseaux sociaux (X, Bluesky, Mastodon, Facebook, LinkedIn), aucun visuel ne s'affiche — juste le titre et la description. C'est une porte de diffusion fermée.

**Origine** : Influenceur.

**Recommandation** : Générer une image OG par fiche (par exemple : titre du lieu + verdict en bandeau coloré + département + Indice + identité visuelle Communs). Idem pour les pages générales. Utiliser un générateur Python simple (PIL/Pillow) intégré à `generate_site.py`.

**Périmètre** : Génération automatique d'images PNG par page ; ajout des balises `og:image` au HTML.

**Effort** : Moyen (3-5 demi-journées — la partie longue est le design des templates d'image).

**Dépendances** : Aucune en amont.

**Décision opérateur** : (a) **design** de l'image — minimaliste typo (faible coût visuel, élégant) ou plus illustré ? (b) **politique sur les fiches au verdict marchand** — afficher ou non le verdict en gros sur l'OG image ? Risque d'effet d'attaque.

---

## P3 — Chantiers à planifier (utiles, non urgents)

### A5 — Documentation du socle conceptuel

**Enjeu** : L'universitaire pose la critique : le triptyque usus/fructus/abusus, la grille à cinq axes, les paliers ne sont pas étayés par une revue de littérature explicite. Un·e chercheur·euse ne peut pas citer le site comme source secondaire sans risquer de prendre une position non-doctrinale pour reçue.

**Origine** : Universitaire, contesté en partie par le/la journaliste (« le triptyque est un outil de vulgarisation politique, pas une catégorie analytique — l'étayer trop le neutraliserait »).

**Recommandation** : Créer une page `site/sources-methodologiques.html` ou un long appendice à la page Méthode qui documente : l'origine de chaque choix conceptuel, les alternatives (Ostrom et Schlager, Le Roy, Coriat, Dardot-Laval, Parance-de Saint Victor), pourquoi le projet a retenu sa formulation, ce qu'il a écarté. Reconnaître que la « face matérielle de l'abusus » est une extension propre au projet, non doctrinale.

**Périmètre** : Page nouvelle, ~3000-5000 mots.

**Effort** : Lourd (10-15 demi-journées — travail de recherche bibliographique).

**Dépendances** : D1 (versionnage en place, pour pouvoir dire « v1.x présente le socle dans tel état »).

**Décision opérateur** : Faut-il **commander une revue de littérature** à un·e chercheur·euse extérieur·e (légitimité accrue, coût d'opportunité élevé) ou la produire en interne ?

---

### B4 — Refonte de l'accueil

**Enjeu** : L'accueil actuel énumère (cards des lieux phares, histogramme, six pavés de liens) mais n'enseigne pas vraiment. La promesse intellectuelle est annoncée, pas développée.

**Origine** : Universitaire pour le diagnostic pédagogique, influenceur pour le diagnostic d'accroche, journaliste pour le diagnostic d'hospitalité.

**Recommandation** : Refondre l'accueil en deux temps :
1. **Above the fold** (premier écran) : un manifeste court (3-5 phrases) qui assume la thèse + 3 chiffres-clés extraits du corpus (« 45 lieux fichés », « 1 seule libération aboutie », « X hectares concernés »).
2. **En-dessous** : structure éditorialisée — *par où entrer* (3-4 entrées clarifiées : « je découvre », « je cherche un lieu », « je veux la méthode », « je suis chercheur·euse »).

Conserver la carte (P1-B1) et l'histogramme. Retirer ou alléger les listes de cards de lieux phares (qui hiérarchisent implicitement sans le dire).

**Périmètre** : Refonte de `site/index.html` / fonction `render_index` du générateur.

**Effort** : Moyen (4-6 demi-journées — design + rédaction du manifeste).

**Dépendances** : A1 (pour ne pas afficher des chiffres-clés qui changent dès la correction du piège GAEC), D1, B1.

**Décision opérateur** : (a) **chiffres-clés à mettre en avant** ? Risque : montrer « 1 seule libération aboutie » est honnête mais peut effrayer ; le cacher serait malhonnête. (b) **manifeste** à rédiger maintenant ou à différer après stabilisation politique.

---

### C3 — Canal de diffusion régulier (newsletter, réseaux)

**Enjeu** : Le site n'a aucun canal de fidélisation. Un·e visiteur·euse intéressé·e arrive, repart, est perdu·e. L'écosystème de la presse, des décideurs, des militant·es ne sait pas que le projet existe et ne reçoit pas signal de ses mises à jour.

**Origine** : Influenceur, journaliste.

**Recommandation** : 
- **Newsletter** mensuelle ou trimestrielle (selon capacité), pilotée depuis le site (Buttondown, Listmonk auto-hébergé, ou simple page de capture d'email). Format : 3-5 nouveautés, 1 cas-pivot, 1 réflexion méthodologique.
- **Présence réseau** : Bluesky en priorité (la presse écolo y est), Mastodon en complément. Pas Twitter/X (incohérent avec la posture). Instagram à différer si pas de moyens visuels (cf. C4).
- **Stratégie d'annonce** : à chaque mise à jour majeure, mailer ciblé presse + post sur les canaux.

**Périmètre** : Choix d'outil + intégration + flux éditorial.

**Effort** : Moyen (3-5 demi-journées pour le setup ; effort récurrent à amortir).

**Dépendances** : B4 (l'accueil doit être prêt à recevoir un signup) ; B2 (un cas-pivot par mois alimente la newsletter).

**Décision opérateur** : (a) Capacité à tenir un rythme éditorial régulier ? Si non, mieux vaut différer C3. (b) **Outil** : auto-hébergé (Listmonk, demande infra) ou SaaS (Buttondown, simple mais payant) ?

---

### C4 — Carrousels du glossaire (chantier conditionnel)

**Enjeu** : Le glossaire est riche mais figé en HTML. Sa diffusion sur réseaux sociaux serait précieuse.

**Origine** : Influenceur, contesté par l'universitaire (cf. §5.2 de la synthèse).

**Recommandation** : Générer **automatiquement** depuis le YAML du glossaire des **slides PNG** (titre + définition courte + lien) pour chaque entrée. Pas de simplification du concept — la slide est une invitation à lire, pas un substitut.

**Périmètre** : Script Python qui génère les images depuis `config/concepts.yml` ; intégration au pipeline de site.

**Effort** : Moyen (3-5 demi-journées).

**Dépendances** : C2 (templates de génération d'image partagés). C3 (canal de diffusion). 

**Décision opérateur** : Activer ou non. Cohérent avec la posture éditoriale ? Risque de glisser vers la communication.

---

### D2 — Audit qualité corpus

**Enjeu** : Au fil des refontes, des incohérences ont pu se glisser. Des fiches au verdict « à établir » traînent (5 cas en suspens du chantier 9). Des chaînes ont été reconfigurées sans contrôle systématique. Un audit de cohérence ponctuel rendrait le corpus plus fiable.

**Origine** : Universitaire indirectement (par sa critique du sourçage et de la reproductibilité).

**Recommandation** : Une passe systématique sur les 123 fiches qui vérifie : cohérence chaîne ↔ verdict, sourçage minimum (≥ 1 URL externe), complétude des champs critiques. Produire un rapport d'audit dans `audit/audit-corpus-YYYY-MM.md`.

**Périmètre** : Script de vérification + lecture humaine par lots.

**Effort** : Lourd (10+ demi-journées si fait à la main ; moyen si l'audit est automatisé partiellement).

**Dépendances** : A1, A2 (pour ne pas auditer un corpus qu'on va corriger).

**Décision opérateur** : Audit complet ou audit échantillon (15-20 fiches) ?

---

## Récapitulatif — vue d'ensemble

| Code | Chantier | Famille | Priorité | Effort | Dépendances |
|------|----------|---------|----------|--------|-------------|
| A1 | Piège GAEC / nature_interet | Socle | P1 | Moyen | — |
| A2 | Refonte critère vivant non-humain | Socle | P1 | Moyen | — |
| B1 | Carte de France | Lisibilité | P1 | Moyen | — |
| A3 | Lisibilité verdict × palier × Indice | Socle | P1 | Léger | A1 |
| D1 | Versionnage + hygiène cicatrices | Hygiène | P1 | Moyen | — |
| A4 | Reformulation déni de jugement | Socle | P2 | Léger | D1 |
| C1 | Traitement des absents structurants | Diffusion | P2 | Moyen-Lourd | A1, A2 |
| B2 | Section magazine / fiches-récit | Lisibilité | P2 | Lourd | A1, D1 |
| B3 | Sourçage tiers | Lisibilité | P2 | Moyen-Lourd | — |
| C2 | OG images & métadonnées | Diffusion | P2 | Moyen | — |
| A5 | Documentation socle conceptuel | Socle | P3 | Lourd | D1 |
| B4 | Refonte accueil | Lisibilité | P3 | Moyen | A1, D1, B1 |
| C3 | Newsletter & réseaux | Diffusion | P3 | Moyen + récurrent | B4, B2 |
| C4 | Carrousels glossaire | Diffusion | P3 | Moyen | C2, C3 |
| D2 | Audit qualité corpus | Hygiène | P3 | Lourd | A1, A2 |

**15 chantiers identifiés. 5 en P1, 5 en P2, 5 en P3.** Le travail P1 seul représente entre 12 et 22 demi-journées (selon profondeur). Le P1+P2 entre 35 et 65 demi-journées. Le total estimé entre 80 et 130 demi-journées.

---

## Conseil d'enchaînement pour la phase 2

Le plus sûr pour la phase 2 est de traiter d'abord les chantiers du **socle** (A1, A2), puis les chantiers de **lisibilité** (A3, B1) qui rendent visibles les corrections faites, puis l'**hygiène** (D1) pour stabiliser le rendu public. Ensuite seulement les chantiers de **diffusion** (C1, C2, B2) prennent sens — ils amplifient un projet qui a déjà gagné en cohérence.

Une cadence raisonnable : 3-5 chantiers par session, sur 4-6 sessions, pour boucler P1+P2. Soit 4-6 sessions à venir avant de pouvoir prétendre que la revue éditoriale a été traduite.

---

*Fin de la qualification des chantiers de phase 2.*
