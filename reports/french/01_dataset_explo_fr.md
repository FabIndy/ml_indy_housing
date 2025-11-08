# Étape 1 — Exploration et nettoyage du dataset

Ce notebook (`01-data-explo.ipynb`) décrit la **phase de préparation initiale** du jeu de données immobilier du projet **ML Indy Housing**.
L’objectif : garantir la **qualité**, la **cohérence** et la **représentativité** du dataset avant modélisation.

## Données d’entrée

- **Fichier source :** `zillow_indy_10k_enriched.csv`
- **Nombre total de lignes initiales :** **17 814**
- **Colonnes principales :**
  `['zpid', 'address', 'sale_price', 'bedrooms', 'bathrooms', 'living_area', 'year_built', 'zipcode', 'lat', 'lon', 'lot_area_value', 'lot_area_unit', 'lot_area_sqft']`

Ce dataset a été généré via des appels API (RapidAPI/Zillow) pour couvrir la région d’Indianapolis.

## 1. Exploration des distributions

Analyse des distributions de variables continues (`sale_price`, `living_area`, `bedrooms`, `bathrooms`, `year_built`) à l’aide d’histogrammes et de boxplots.
Constat : une dispersion importante, typique d’un marché immobilier varié (maisons standards et biens haut de gamme).

## 2. Suppression des doublons

Détection de **11 332 doublons** sur la clé `zpid`.
→ Suppression de ces entrées pour ne conserver qu’une seule ligne par bien immobilier.

## 3. Gestion des valeurs manquantes

- Suppression de la colonne **`lot_area_sqft`**, contenant trop de valeurs manquantes.
- Suppression de **829 lignes supplémentaires** contenant encore des NaN sur des colonnes essentielles.

## 4. Analyse des outliers

Identification de valeurs extrêmes :
- **`living_area` → 238 outliers**
- **`sale_price` → 322 outliers**
Les outliers ont été **conservés**, afin de préserver la représentativité du marché.

## 5. Export du dataset nettoyé

- **Fichier final :** `df_cut_no_nan.csv`
- **Nombre total de lignes :** **5 653**
- **Colonnes finales :**
  `['zpid', 'sale_price', 'bedrooms', 'bathrooms', 'living_area', 'year_built', 'zipcode', 'lat', 'lon']`

Ce dataset propre constitue la base utilisée pour les étapes ultérieures de **feature engineering**, 
**modélisation (RF,XGBoost, LightGBM)** et **évaluation des performances**.
