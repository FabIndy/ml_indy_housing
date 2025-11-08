Step 0 — Dataset Creation – ML Indy Housing Project
Objective

As part of the ML Indy Housing project, I built my own real estate database entirely from scratch —
without relying on any pre-existing public dataset.
The goal was to create a localized and homogeneous dataset focused on the Indianapolis metropolitan area,
in order to model residential house sale prices.

Methodology

I developed a Python script (step3_targeted_zip_harvest.py) to automate real estate data collection by ZIP code,
using APIs available on RapidAPI, including the Zillow API.
For each targeted ZIP area, the script performs:

Successive requests to the endpoints /propertyExtendedSearch, /property, and /building.

Progressive enrichment of missing fields (e.g., year built, lot area, geographic coordinates).

Completeness verification and duplicate filtering before saving.

The process aimed to gather at least 200 properties per ZIP code, covering the main residential areas of
Indianapolis and its surroundings (Zionsville, Carmel, Fishers, Greenwood, etc.).

Security and Configuration

Sensitive parameters (API key, RapidAPI host) are stored in a non-versioned .env file
to protect API credentials.
The script is compatible with a PRO plan (2 requests/second) and includes a retry + exponential backoff mechanism
to prevent quota overruns or network failures.

Result

The final dataset, zillow_indy_10k_enriched.csv, contains several thousand cleaned and harmonized records,
with the main explanatory variables required for modeling:

sale_price, bedrooms, bathrooms, living_area,
year_built, lot_area_sqft, zipcode, lat, lon.

This dataset served as the foundation for the subsequent stages of feature engineering,
modeling (RF, XGBoost, LightGBM), and price prediction performance evaluation.

Conclusion

This work demonstrates my ability to design a complete dataset from APIs,
ensuring data quality, consistency, and traceability —
core skills for any applied data science project based on real-world data.