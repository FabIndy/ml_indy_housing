# ML Indy Housing — Prédiction du prix des maisons à Indianapolis

**Démo en ligne :**  [Tester l’application sur Hugging Face](https://huggingface.co/spaces/FabIndy/house-price-ui)

---

##  Présentation du projet

Le projet **ML Indy Housing** vise à **prédire le prix de vente des maisons** dans la région d’Indianapolis à partir de données collectées via API (Zillow sur RapidAPI).  
Il met en œuvre un pipeline complet de **data science appliquée**, allant de la création du dataset au déploiement du modèle sur le web.

L’application permet à l’utilisateur de saisir les caractéristiques principales d’un bien immobilier et d’obtenir instantanément une **estimation du prix de vente en dollars**.  
Les prédictions reposent sur un modèle **XGBoost optimisé** entraîné sur plusieurs milliers de biens résidentiels.

---

##  Modèle utilisé

- **Algorithme :** XGBoost Regressor (Pseudohuber Loss + Fine Weighting)  
- **Base d’entraînement :** 5 653 enregistrements nettoyés issus de l’API Zillow (RapidAPI)  
- **Objectif :** prédire le prix de vente (`sale_price`) en dollars américains  

| Segment                     | MAE ($) | Erreur relative |
|-----------------------------|---------|-----------------|
| Toutes les maisons          | 56 085  | 14,5 %          |
| < 1 M $ (maisons standards) | 45 195  | 12,8 %          |
| ≥ 1 M $ (maisons de luxe)   | 531 241 | 29,6 %          |

L’erreur moyenne absolue (MAE) mesure la différence absolue moyenne entre les prix prédits et les prix réels, exprimée en dollars.

Le modèle offre une **bonne performance** sur les maisons standards, qui représentent environ 98 % du marché.

---

## Architecture de l’application

L’application est hébergée sur **Hugging Face Spaces** et repose sur trois conteneurs interconnectés :

```
[ Interface Gradio (Frontend) ]
            ↓
[ API FastAPI (Backend Dockerisé) ]
            ↓
[ Modèle XGBoost (Hugging Face Hub) ]
```

### Description des composants
1. **Frontend (Gradio)** — interface web intuitive permettant la saisie et l’affichage des résultats.  
2. **Backend (FastAPI)** — reçoit les données saisies, interroge le modèle et renvoie la prédiction.  
3. **Modèle hébergé** — contient le modèle XGBoost final, accessible via l’API.  

Cette architecture modulaire permet de mettre à jour chaque composant indépendamment.

---

## Codes postaux couverts

Le modèle a été entraîné uniquement sur les **zones résidentielles d’Indianapolis et de sa périphérie** :

 46201. 46202. 46203. 46204. 46205. 46208. 46214. 46216. 46217.
 46218. 46219. 46220. 46221. 46222. 46224. 46225. 46226. 46227. 46228.
 46229. 46231. 46234. 46235. 46236. 46237. 46239. 46240. 46241. 46250.
 46254. 46256. 46259. 46260. 46268. 46278. 46280. 46290. 46032. 46033.
 46074. 46037. 46038. 46077. 46112. 46123. 46168. 46142. 46143. 46060.
 46062. 46075. 46055. 46107.

Les prédictions effectuées en dehors de cette liste peuvent être moins fiables.

---

## Variables à renseigner

| Champ                    | Description                                     | Exemple        |
|--------------------------|-------------------------------------------------|----------------|
| **Bedrooms**             | Nombre de chambres                              | 3              |
| **Bathrooms**            | Nombre de salles de bain                        | 2              |
| **Living area (sqft)**   | Surface habitable en pieds carrés               | 2 000          |
| **House age (years)**    | Âge du bien                                     | 10             |
| **Latitude / Longitude** | Coordonnées géographiques issues de Google Maps | 39.90 / -86.15 |
| **ZIP code**             | Code postal (voir liste ci-dessus)              | 46220          |

> Les coordonnées (latitude, longitude) s’obtiennent facilement via **Google Maps** .  
> Ces valeurs permettent de calculer la **distance au centre-ville d’Indianapolis**, un facteur clé du modèle.

---

## Technologies utilisées

- **Python 3.10**  
- **Pandas**, **Scikit-learn**, **XGBoost**, **LightGBM**  
- **FastAPI** pour le backend  
- **Gradio** pour l’interface web  
- **Docker** pour la conteneurisation  
- **Hugging Face Spaces** pour le déploiement  

---

## Exécution locale

### Cloner le dépôt
```bash
git clone https://github.com/<ton-utilisateur>/ml_indy_housing.git
cd ml_indy_housing
```

### Créer et activer l’environnement
```bash
conda env create -f environment.yml
conda activate indy_env
```

### Lancer l’API FastAPI
```bash
cd deployment/house-price-api
uvicorn app:app --reload
```
➡ Accès à la documentation : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## Auteur

**Fabrice Belfiore**  
Data Scientist (Certification DataScientest 2025)  
[Profil LinkedIn](https://www.linkedin.com/in/fabrice-belfiore-0b168222a/)  
Basé à Indianapolis (IN, USA)
