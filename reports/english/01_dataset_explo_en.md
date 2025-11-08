Step 1 — Dataset Exploration and Cleaning

This notebook (01-data-explo.ipynb) describes the initial preparation phase of the real estate dataset used in the ML Indy Housing project.
The goal was to ensure the quality, consistency, and representativeness of the dataset before modeling.

Input Data

Source file: zillow_indy_10k_enriched.csv

Initial number of rows: 17,814

Main columns:
['zpid', 'address', 'sale_price', 'bedrooms', 'bathrooms', 'living_area', 'year_built', 'zipcode', 'lat', 'lon', 'lot_area_value', 'lot_area_unit', 'lot_area_sqft']

This dataset was generated through API calls (RapidAPI/Zillow) covering the Indianapolis area.

1. Distribution Exploration

Analysis of continuous variable distributions (sale_price, living_area, bedrooms, bathrooms, year_built) using histograms and boxplots.
Observation: significant dispersion, typical of a diverse real estate market (standard homes and luxury properties).

2. Duplicate Removal

Detection of 11,332 duplicates based on the key zpid.
→ These entries were removed, keeping only one record per property.

3. Handling Missing Values

The column lot_area_sqft was removed due to an excessive proportion of missing values.

829 additional rows containing NaN values in key variables were also deleted.

4. Outlier Analysis

Identification of extreme values:

living_area → 238 outliers

sale_price → 322 outliers
Outliers were retained to preserve market representativeness.

5. Export of the Cleaned Dataset

Final file: df_cut_no_nan.csv

Final number of rows: 5,653

Final columns:
['zpid', 'sale_price', 'bedrooms', 'bathrooms', 'living_area', 'year_built', 'zipcode', 'lat', 'lon']

This cleaned dataset forms the foundation for the next stages of feature engineering,
modeling (RF, XGBoost, LightGBM), and performance evaluation.