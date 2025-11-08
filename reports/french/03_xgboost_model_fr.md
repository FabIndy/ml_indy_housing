# Étape 3 — Modélisation XGBoost (Pseudohuber + Fine Weighting)

Ce notebook (`19-XGBoost-pseudohuber-fineweighting.ipynb`) présente la **phase de modélisation finale** du projet **ML Indy Housing**, fondée sur les jeux de données déjà standardisés et normalisés.

## Données utilisées

- **Fichiers d’entrée :**
  `X_train_scaled-v2.csv`, `y_train-v2.csv`,
  `X_val_scaled-v2.csv`, `y_val-v2.csv`,
  `X_test_scaled-v2.csv`, `y_test-v2.csv`

Ces fichiers contiennent directement les données mises à l’échelle depuis l’étape précédente (les fichiers de scalers ne sont pas réutilisés ici).

### Nombre de lignes par split
| Split                   | Nombre de lignes |
|:------------------------|-----------------:|
| `X_train_scaled-v2.csv` | 3 957            |
| `X_val_scaled-v2.csv`   | 849              | 
| `X_test_scaled-v2.csv`  | 847              |

---

## 1. Préprocessing

- Chargement des splits d’entraînement, de validation et de test.
- Aucune transformation supplémentaire : les scalers standard et min-max ont déjà été appliqués.
- Mise en place d’une **pondération fine** des échantillons pour équilibrer la contribution des maisons selon leur prix.

### Formule de pondération
Chaque échantillon reçoit un poids :
\[
w_i = 1 + 2 \times \left( \frac{y_i}{\text{mean}(y)} \right)
\]
Cette approche augmente modérément le poids des maisons les plus chères, sans déséquilibrer la perte globale.

- La variable cible utilisée est le **logarithme naturel du prix de vente** :
\[
y = \log(\text{sale\_price})
\]
Cette transformation réduit l’asymétrie, stabilise la variance et limite l’influence des valeurs extrêmes.

---

## 2. Choix du modèle

- **Algorithme :** `XGBRegressor`
- **Fonction de perte :** `reg:pseudohubererror`, robuste aux valeurs extrêmes.
- **Hyperparamètres principaux :**
  - `max_depth = 7`
  - `learning_rate = 0.03`
  - `colsample_bytree = 0.6`
  - `n_estimators = 1000`
  - `tree_method = 'gpu_hist'`, `predictor = 'gpu_predictor'`
- **Pondération dynamique** (`sample_weight`) intégrée à l’entraînement pour équilibrer les différentes gammes de prix.

---

## 3. Validation croisée

- **Méthode :** validation croisée stratifiée à 5 folds.
- **Performances moyennes :**
  - RMSE (log) = 0.254 ± 0.003
  - MAE global = 68 781 $ ± 8 451 $
  - MAE maisons < 1 M $ = 48 709 $ ± 671 $
  - MAE maisons ≥ 1 M $ = 772 132 $ ± 356 900 $

---

## 4. Évaluation sur l’ensemble de test

**Performances finales :**
- **MAE global : 56 085 $**
- **MAE maisons standards (< 1 M $) : 45 195 $**
- **MAE maisons de luxe (≥ 1 M $) : 531 241 $**

**Erreurs relatives correspondantes :**
- **Toutes les maisons : 14,5 %**
- **Maisons standards (< 1 M $) : 12,8 %**
- **Maisons de luxe (≥ 1 M $) : 29,6 %**

---

## 5. Interprétation

Le modèle **XGBoost avec perte Pseudohuber et pondération fine** atteint un **excellent compromis entre robustesse et précision** :
- Il prédit très précisément les **biens standards** (près de 98 % du marché) avec une erreur moyenne inférieure à 13 %.
- Les **biens de luxe**, plus rares et plus variables, présentent des écarts plus importants mais restent modélisés de manière stable.

Ce modèle constitue la **référence finale** du pipeline **ML Indy Housing**, combinant rigueur statistique, pondération adaptée et robustesse face aux outliers.
