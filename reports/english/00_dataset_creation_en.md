# Step 0 : Dataset Creation – ML Indy Housing Project

**Objective :**

As part of the ML Indy Housing project, I built my own real estate database from scratch, without using any pre-existing public dataset.
The goal was to create a localized and homogeneous dataset focused on the Indianapolis region, in order to model house sale prices.

**Methodology :**

I developed a Python script (**step3_targeted_zip_harvest.py**) to automate the collection of real estate data by ZIP code using APIs available on RapidAPI, including the Zillow API.
For each targeted area, the script performs:

- Successive requests to the endpoints /propertyExtendedSearch, /property, and /building
- Progressive enrichment of missing fields (year built, lot area, geographic coordinates, etc.)
- Completeness verification and duplicate filtering before saving

The process aims to collect at least 200 properties per ZIP code, covering the main residential areas of Indianapolis and its surroundings (Zionsville, Carmel, Fishers, Greenwood, etc.).

**Security and Configuration :**

Sensitive parameters (API key, RapidAPI host) are stored in a non-versioned `.env` file to ensure credential security.
The script is compatible with a PRO plan (2 requests/s) and integrates a retry mechanism with exponential backoff to avoid quota overruns or network errors.

**Result :**

The final file, `zillow_indy_10k_enriched.csv`, contains several thousand cleaned and harmonized records, with the main explanatory variables needed for modeling:

sale_price, bedrooms, bathrooms, living_area,
year_built, lot_area_sqft, zipcode, lat, lon.

This dataset then served as the basis for the feature engineering, modeling (RF, XGBoost, LightGBM), and performance evaluation stages of the price prediction model.

**Conclusion :**

This approach demonstrates my ability to design a complete dataset from APIs while ensuring data quality, consistency, and traceability — essential skills for any data science project applied to real-world data.
