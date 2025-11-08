# Étape 2 — Data Visualization et ingénierie des variables

Ce notebook (`16-dataviz-v2.ipynb`) présente la phase de **data visualisation** et de **préparation des variables** du projet **ML Indy Housing**.

## Données d’entrée

- **Fichier source :** `df_cut_no_nan.csv`
- **Nombre de lignes :** **5 653**
- **Colonnes :**
  `['zpid', 'sale_price', 'bedrooms', 'bathrooms', 'living_area', 'year_built', 'zipcode', 'lat', 'lon']`

## 1. Création de nouvelles variables

Deux nouvelles variables ont été créées :
- **`distance_to_downtown_km`** : distance géographique (en kilomètres) entre chaque bien et le centre-ville d’Indianapolis.
- **`house_age`** : âge du bien calculé à partir de l’année de construction (`year_built`).

## 2. Exploration visuelle des distributions

Les distributions de `sale_price`, `living_area` et `house_age` ont été visualisées à l’aide d’histogrammes et de boxplots.
L’analyse a mis en évidence une **forte asymétrie** sur ces variables.
→ Application du **logarithme naturel** pour obtenir :
`log_sale_price`, `log_living_area`, `log_house_age`.

## 3. Encodage et sélection des variables

- Application d’un **One Hot Encoding** sur la variable `zipcode` (53 zones postales).
- Sélection des variables explicatives pour la modélisation :
  `['bedrooms', 'bathrooms', 'lat', 'lon', 'log_living_area', 'log_house_age', 'distance_to_downtown_km', 'zipcode_*']`.

## 4. Split des données

- Découpage du dataset en **70 % train / 15 % validation / 15 % test**.
- **Stratification par gamme de prix** pour équilibrer la répartition de `sale_price`.

## 5. Standardisation et normalisation

- **Standardisation** appliquée à :
  `log_living_area` et `log_house_age`.
- **Normalisation min-max** appliquée à :
  `bedrooms`, `bathrooms`, `lat`, `lon` et `distance_to_downtown_km`.

Les objets de transformation ont été sauvegardés sous forme de CSV :
- `scaler_standard-v2.csv`
- `scaler_normal-v2.csv`

## 6. Sauvegarde des jeux de données

- Données nettoyées : `df_clean.csv`
- Splits : 
  - `X_train-v2.csv`, `y_train-v2.csv`
  - `X_val-v2.csv`, `y_val-v2.csv`
  - `X_test-v2.csv`, `y_test-v2.csv`
- Versions standardisées/normalisées :
  - `X_train_scaled-v2.csv`
  - `X_val_scaled-v2.csv`
  - `X_test_scaled-v2.csv`

Ces fichiers constituent la base finale utilisée pour les notebooks de modélisation.
