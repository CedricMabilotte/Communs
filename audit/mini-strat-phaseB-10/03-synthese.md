# Mini-strat Phase B — synthèse arbitrée (cycle 3)

*Session #10, 29 mai 2026. Synthèse de la passe MARS-strat ouvrant la Phase B.
Cycle 1 : 5 voix isolées (`01-cycle1/`). Cycle 2 : réactions croisées focalisées
sur la tension vive (`02-cycle2/`). Convention : « les voix disent » = traçable
aux cycles 1-2 ; « **proposition de l'orchestrateur** » = arbitrage à valider.*

---

## 1. Constats partagés (convergences → chantiers non négociables)

Les cinq voix convergent sur l'architecture — friction faible, recoupement fort.

- **Naviguer par intentions, pas par objets** (architecte info, repris par lecteur
  cible). Ramener les ~8 entrées à **4-5** : Accueil · Annuaire · Dossiers ·
  Méthode · Glossaire. Lieux/Porteurs/Usufruitiers deviennent un *filtre de type*
  de l'Annuaire ; Carte et Classement deviennent des *vues* de l'Annuaire (Liste /
  Carte / Classement), pas des sections rivales.
- **Fiche à deux profondeurs, ligne de flottaison nette** (architecte, lecteur).
  Au-dessus : bandeau de lecture A3 (verdict + Indice + palier expliqués),
  **déplié** — pas en `<details>` —, plus une synthèse citable. En-dessous :
  l'audit (pentagone, grille repliable sur mobile, sources). Le lecteur presse doit
  pouvoir *citer en une ligne* sans dérouler.
- **Le magazine est une surcouche de chemins, pas de rang** (éditeur, validé par
  architecte). Il ajoute des récits et des hooks ; il **ne touche jamais** l'Indice,
  le verdict, ni la symétrie du catalogue. Lien retour bidirectionnel fiche↔dossier.
  On dit « raconté », jamais « remarquable ».
- **Contrat de lecture affiché** (architecte) pour dissoudre la tension symétrie ×
  hiérarchie : le magazine affiche « sélection éditoriale » ; le catalogue affiche
  « tous les lieux, à barème égal ». La contradiction n'existe que si elle n'est
  pas nommée.
- **La carte de France (B1) est le manque n°1** (lecteur cible, éditeur) : premier
  réflexe presse, outil de décision territoriale, visuel partageable.
- **Citabilité** (lecteur, gardien) : versionnage public + hygiène D1 des
  cicatrices (« refonte #3 », « session #N ») ; un kit chiffres-clés en accueil.
- **Réutiliser les deux voix existantes, pas en créer** (éditeur) : voix incarnée
  dominante dans le magazine, voix exacte en ancres (brief §12).

## 2. Tension structurante tranchée — la strictness des co-gates

Seule vraie friction du cycle 1 : gardien (`non_subordination` = gate dur,
`usage_non_marchand` = glose) **vs** méthodologue (l'inverse). Le cycle 2
(réactions croisées) les a fait **converger**, et a produit un résultat qu'aucune
des deux n'avait seule.

**Résolution (les deux voix s'accordent) :**

| Co-gate | Statut tranché |
|---|---|
| foncier hors-marché + irréversibilité | **gate dur** (inchangé) |
| habitat du vivant | **gate dur** (inchangé) |
| régénération (`milieu_protege`, face opposable) | **gate dur** (inchangé) |
| finalité = `usage_non_marchand` (oui/partiel) + `usage_interet_general` | **gate doux maintenu** — le gardien a concédé : c'est ce couple, déjà codé, qui gate la finalité ; ne pas durcir, ne pas glosser |
| `non_subordination` | **gate dur, proxy correctement unidirectionnel** |

**Le résultat inattendu (méthodologue, concédé par gardien)** : le code A1 testait
`non_subordination == "oui"` — donc l'**absence** (0/45 fiches le documentent)
fermait le sommet. C'était un sommet **vide par artefact de peuplement**, non par
exigence. La distinction qui réconcilie : *bloquer par absence* (silence — mauvais)
≠ *bloquer par présence constatée* (salariat-cœur observé — jugement légitime,
constitutif de la 3ᵉ décommodification de Polanyi). **Correction appliquée** :
seul un `non` constaté ferme le sommet ; `oui`/`partiel`/`inconnu`/absent sont
neutres. Conséquence mécanique vérifiée : **toujours 0 sommet**, mais désormais
*vide-atteignable* (aucune chaîne pure ne franchit foncier+vivant+régénération+
finalité) et non *vide-impossible* (par le silence). Le gardien tient un garde-fou
pour plus tard : à la bascule, un salariat-**cœur** constaté ferme, un salariat-
**support** (`partiel`) autorise.

**Proposition de l'orchestrateur** : adopter cette résolution telle quelle (elle
est traçable, datée, réversible). La règle « gate-quand-couvert ≥ 50 % » du
méthodologue est *abandonnée* au profit de l'unidirectionnalité correctement codée
— plus simple, plus fidèle à la doctrine §8.

## 3. Tensions résiduelles — arbitrage opérateur requis

1. **5ᵉ cas-pivot du magazine** : Pommiers, Rayol, Larzac, Eau du Bassin Rennais
   sont acquis. L'éditeur propose **Notre-Dame-des-Landes / Assemblée des usages**
   (libération *conquise*) — mais c'est politiquement chargé. Alternative plus
   sobre : Mhotte (anthroposophie, hybride) ou Berquet/Antidote (hybride réussi).
   *À trancher.*
2. **Réversibilité du verdict** : le lecteur cible pose une condition forte pour
   faire confiance — un **droit de réponse du porteur** (le verdict est réversible,
   pas un arrêt). Le gardien n'en parle pas ; l'orchestrateur juge la demande
   légitime et peu coûteuse (un champ « réponse du porteur » sur la fiche). *À
   valider comme principe.*
3. **A4 — « pas un jugement de valeur »** : le gardien signale des **résidus**
   (Limites + footer) qui contredisent la prise assumée et se propagent à tout le
   site par le pied de page. *À supprimer* (chantier A4, à moitié fait) — semble
   non controversé, mais touche la posture, donc signalé.

## 4. Idées spécifiques à une voix — à conserver / écarter

- **Conserver** : « contrat de lecture affiché » (architecte) ; « hook = champ
  `en_clair` réutilisé, coût nul » (éditeur) ; « explicabilité en une ligne comme
  condition du verdict » (lecteur) ; « encadré limites assumées d'un bloc, avec
  convention + auteur + date » (gardien) ; « datation des seuils/plafonds »
  (méthodologue).
- **Écarter / différer** : carrousels glossaire (C4, conditionnel — hors de cette
  passe) ; revue de littérature pleine (A5 — chantier propre, déjà amorcé par le
  cadre exhaustif).

## 5. Ce que la Phase B exécute (cadre d'architecture validé)

Sous une seule direction, en lots MARS-prod parallèles (L7/L12), aperçu L9
systématique :

1. **Navigation refondue** (4-5 entrées ; Carte/Classement = vues de l'Annuaire).
2. **Gabarit de fiche à deux profondeurs** (bandeau A3 déplié + synthèse citable
   au-dessus ; audit en-dessous ; grille repliable mobile).
3. **Carte de France (B1)**.
4. **Accueil (B4)** : manifeste + chiffres-clés citables + entrées par intention.
5. **Magazine (B2)** : 5 fiches-récit (cas-pivot §3.1), hooks dans les fiches,
   liens retour ; voix incarnée dominante.
6. **Hygiène D1** : versionnage public, suppression des cicatrices, retrait des
   résidus « pas un jugement de valeur » (A4).
7. **Co-gates** : résolution §2 (déjà appliquée au moteur) reflétée en méthode ;
   réversibilité §3.2 si validée.

Détail opérationnel et dépendances : `audit/revue-editoriale-8d/04-chantiers.md`,
recalé par `taf/pilotage-phase2.md`.
