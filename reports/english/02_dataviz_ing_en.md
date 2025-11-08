Step 2 — Data Visualization and Feature Engineering

The notebook 16-dataviz-v2.ipynb presents the data visualization and feature engineering phase of the ML Indy Housing project.

Input Data

Source file: df_cut_no_nan.csv

Number of rows: 5,653

Columns:
['zpid', 'sale_price', 'bedrooms', 'bathrooms', 'living_area', 'year_built', 'zipcode', 'lat', 'lon']

1. Creation of New Variables

Two new variables were created:

distance_to_downtown_km: geographic distance (in kilometers) between each property and downtown Indianapolis.

house_age: property age calculated from the year of construction (year_built).

2. Visual Exploration of Distributions

The distributions of sale_price, living_area, and house_age were visualized using histograms and boxplots.
The analysis revealed a strong skewness for these variables.
→ A natural logarithmic transformation was applied, resulting in:
log_sale_price, log_living_area, log_house_age.

3. Encoding and Variable Selection

One Hot Encoding was applied to the variable zipcode (53 ZIP codes).

The explanatory variables selected for modeling are:
['bedrooms', 'bathrooms', 'lat', 'lon', 'log_living_area', 'log_house_age', 'distance_to_downtown_km', 'zipcode_*'].

4. Data Splitting

The dataset was split into 70% training / 15% validation / 15% test.

Stratification by price range was applied to preserve the distribution of sale_price.

5. Standardization and Normalization

Standardization applied to:
log_living_area and log_house_age.

Min-max normalization applied to:
bedrooms, bathrooms, lat, lon, and distance_to_downtown_km.

The transformation objects were saved as CSV files:

scaler_standard-v2.csv

scaler_normal-v2.csv

6. Dataset Exports

Clean data: df_clean.csv

Splits:

X_train-v2.csv, y_train-v2.csv

X_val-v2.csv, y_val-v2.csv

X_test-v2.csv, y_test-v2.csv

Scaled/normalized versions:

X_train_scaled-v2.csv

X_val_scaled-v2.csv

X_test_scaled-v2.csv

These files form the final base used for the modeling notebooks.