# B1 — Calibrage des paliers de l'Indice : distribution observée

*Note d'arbitrage, session #2 du 24 mai 2026. Clôt le point de backlog B1
(« recalibrer les paliers de l'Indice »).*

## La question

Lors de la refonte v2, les seuils des paliers ont été posés à l'estime et
marqués « PROVISOIRES » dans `config/ranking.yml`. La crainte fondatrice :
l'agrégation géométrique abaisserait mécaniquement les scores par rapport à une
moyenne arithmétique, rendant des seuils estimés trop hauts. B1 demandait de
recalibrer sur la dispersion réelle du corpus une fois celui-ci stabilisé.

## Méthode

Distribution de l'**indice de libération effectif** (`idl`, champ affiché et
classant) extraite de `site/data.json`. Les **28 entrées notées** sont
retenues — les 5 modèles voisins, dont le score est `estime` et non `calcule`,
sont exclus du calibrage.

## Distribution observée

Les 28 indices triés :

```
36 39 45 47 48 48 | 57 57 58 58 58 60 60 | 62 63 65 65 68 70 | 74 75 76 77 79 | 82 83 85 94
```

- Minimum 36 · Médiane 62,5 · Moyenne 63,9 · Maximum 94.
- Quintiles (P20 / P40 / P60 / P80) ≈ 48 / 58 / 66 / 76.

Répartition par palier, avec les seuils actuels (abouti ≥ 78, solide ≥ 64,
engagé ≥ 50, partiel ≥ 35, éloigné ≥ 0) :

| Palier | Seuil | Entrées | Effectif |
|---|---|---|---|
| Libération aboutie | ≥ 78 | 79, 82, 83, 85, 94 | 5 |
| Montage solide | 64–77 | 65, 65, 68, 70, 74, 75, 76, 77 | 8 |
| Engagement réel | 50–63 | 57, 57, 58, 58, 58, 60, 60, 62, 63 | 9 |
| Libération partielle | 35–49 | 36, 39, 45, 47, 48, 48 | 6 |
| Éloigné du modèle | < 35 | — | 0 |

## Lecture

La prémisse de B1 est **largement infirmée**. L'agrégation géométrique n'a pas
écrasé le corpus : la moyenne s'établit à 63,9, la dispersion couvre tout
l'intervalle 36–94, et la répartition 5 / 8 / 9 / 6 / 0 est équilibrée. Les
deux seuils hauts coïncident presque avec les quintiles réels du corpus
(78 ≈ P80 = 76 ; 64 ≈ P60 = 66) : les paliers tiennent.

Le seul écart notable est en bas de l'échelle : **le palier « éloigné »
(< 35) est vide** — aucune entrée ne descend sous 36. Ce n'est pas un défaut de
calibrage mais une propriété structurelle du corpus : l'annuaire est *curé*,
il référence des montages choisis pour leur parenté avec la libération des
terres, non des contre-exemples francs. Un palier qui ne se déclenchera jamais
tant que cette politique éditoriale tient.

Un recalibrage par quintiles aurait rendu les classes strictement
équilibrées, mais au prix de transformer un référentiel **absolu** (un score
de 78 signifie la même chose quel que soit le corpus) en classement
**relatif** qui se déplacerait à chaque ajout de fiche. Pour un annuaire
critique, l'échelle absolue est préférable.

## Verdict

**B1 est clos.** Les seuils 78 / 64 / 50 / 35 sont conservés tels quels. Le
commentaire « seuils PROVISOIRES » de `config/ranking.yml` est à remplacer par
un renvoi à la présente note. Le palier « éloigné » est conservé : vide
aujourd'hui, il reste le réceptacle prévu pour un futur contre-exemple, et son
existence documente la borne basse de l'échelle.

*Reprise éventuelle :* ne rouvrir que si la politique éditoriale change (ajout
délibéré de contre-exemples) ou si le corpus triple de taille — auquel cas
re-mesurer la distribution avant de toucher aux seuils.
