# ML Indy Housing — House Price Prediction in Indianapolis

**Live demo:**  [Try the app on Hugging Face](https://huggingface.co/spaces/FabIndy/house-price-ui)

---

## Project Overview

The **ML Indy Housing** project aims to **predict house selling prices** in the Indianapolis area using data collected via API (Zillow on RapidAPI).  
It implements a full **applied data science pipeline**, from dataset creation to model deployment on the web.

The web app allows users to input a property’s main characteristics and instantly receive a **price estimate in USD**.  
Predictions are powered by an optimized **XGBoost model** trained on several thousand residential properties.

---

##  Model Description

- **Algorithm:** XGBoost Regressor (Pseudohuber Loss + Fine Weighting)  
- **Training base:** 5,653 cleaned records collected from the Zillow API (RapidAPI)  
- **Goal:** predict the selling price (`sale_price`) in US dollars  

| Segment                | MAE ($) | Relative Error |
|------------------------|---------|----------------|
| All houses             | 56,085  | 14.5 %         |
| < 1M$ (standard homes) | 45,195  | 12.8 %         |
| ≥ 1M$ (luxury homes)   | 531,241 | 29.6 %         |

The Mean Absolute Error (MAE) measures the average absolute difference between the predicted and actual prices, expressed in dollars.
The model shows **good performance** for standard homes, which represent about 98% of the market.

---

##  Application Architecture

The application is hosted on **Hugging Face Spaces** and relies on three interconnected containers:

```
[ Gradio Interface (Frontend) ]
            ↓
[ FastAPI (Dockerized Backend) ]
            ↓
[ XGBoost Model (Hugging Face Hub) ]
```

### Components
1. **Frontend (Gradio)** — intuitive web interface for user input and result display.  
2. **Backend (FastAPI)** — receives input data, queries the model, and returns the prediction.  
3. **Model container** — hosts the final XGBoost model accessible via API.  

This modular architecture allows each component to be updated independently.

---

## ZIP Codes Covered

The model was trained exclusively on **residential areas of Indianapolis and its surroundings**:

 46201. 46202. 46203. 46204. 46205. 46208. 46214. 46216. 46217.
 46218. 46219. 46220. 46221. 46222. 46224. 46225. 46226. 46227. 46228.
 46229. 46231. 46234. 46235. 46236. 46237. 46239. 46240. 46241. 46250.
 46254. 46256. 46259. 46260. 46268. 46278. 46280. 46290. 46032. 46033.
 46074. 46037. 46038. 46077. 46112. 46123. 46168. 46142. 46143. 46060.
 46062. 46075. 46055. 46107.

Predictions made outside this list may be less reliable.

---

## Input Variables

| Field                    | Description                             | Example        |
|:-------------------------|:----------------------------------------|:---------------|
| **Bedrooms**             | Number of bedrooms                      | 3              |
| **Bathrooms**            | Number of bathrooms                     | 2              |
| **Living area (sqft)**   | Total interior area in square feet      | 2,000          |
| **House age (years)**    | Age of the property                     | 10             |
| **Latitude / Longitude** | Geographic coordinates from Google Maps | 39.90 / -86.15 |
| **ZIP code**             | Postal code (see list above)            | 46220          |

> Latitude and longitude can be easily retrieved via **Google Maps** .  
> These coordinates are used to compute the **distance from downtown Indianapolis**, a key feature in the model.

---

## Technologies Used

- **Python 3.10**  
- **Pandas**, **Scikit-learn**, **XGBoost**, **LightGBM**  
- **FastAPI** for the backend  
- **Gradio** for the web interface  
- **Docker** for containerization  
- **Hugging Face Spaces** for deployment  

---

## Run Locally

### 1Clone the repository
```bash
git clone https://github.com/<your-username>/ml_indy_housing.git
cd ml_indy_housing
```

### Create and activate the environment
```bash
conda env create -f environment.yml
conda activate indy_env
```

### Launch the FastAPI backend
```bash
cd deployment/house-price-api
uvicorn app:app --reload
```
➡ Access documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Start the Gradio interface
```bash
cd deployment/house-price-ui
python app.py
```

---

## Author

**Fabrice Belfiore**  
Data Scientist (DataScientest Certification 2025)  
[LinkedIn Profile](https://www.linkedin.com/in/fabrice-belfiore-0b168222a/)  
Based in Indianapolis, IN, USA
