# Étape 5 — Présentation de l’application : Indy House Price Predictor

Ce rapport présente l’**application web publique** développée dans le cadre du projet **ML Indy Housing**.
Elle permet à l’utilisateur d’**estimer le prix de vente d’une maison** dans la région d’Indianapolis à l’aide d’un modèle déployé sur **Hugging Face Spaces**.

**Démo en ligne :** https://huggingface.co/spaces/FabIndy/house-price-ui

## 1. Objectif de l’application

L’application offre une **interface interactive** où l’utilisateur peut saisir les principales caractéristiques d’un bien immobilier afin d’obtenir immédiatement une **estimation du prix en dollars américains (USD)**.
Elle repose sur le **modèle XGBoost final** entraîné dans le cadre du projet (`19-XGBoost-pseudohuber-fineweighting.ipynb`), ayant atteint une **erreur absolue moyenne (MAE) de 45 195 $** pour les maisons standards, avec un **taux d’erreur relatif de 12,8 %** — garantissant une excellente fiabilité pour la grande majorité du marché (< 1 M$).

## 2. Codes postaux couverts

Le modèle a été entraîné uniquement sur les **zones résidentielles d’Indianapolis et de sa périphérie** :

46201, 46202, 46203, 46204, 46205, 46208, 46214, 46216, 46217,  
46218, 46219, 46220, 46221, 46222, 46224, 46225, 46226, 46227, 46228,  
46229, 46231, 46234, 46235, 46236, 46237, 46239, 46240, 46241, 46250,  
46254, 46256, 46259, 46260, 46268, 46278, 46280, 46290, 46032, 46033,  
46074, 46037, 46038, 46077, 46112, 46123, 46168, 46142, 46143, 46060,  
46062, 46075, 46055, 46107.

Les prédictions effectuées en dehors de cette liste peuvent être moins fiables.


## 3. Données à renseigner

L’application demande les informations suivantes avant d’envoyer la requête au backend (`/predict`) :

| Champ                  |                                     Description | Exemple |
|:-----------------------|:------------------------------------------------|:--------|
| **Bedrooms**           | Nombre de chambres                              | 3       |
| **Bathrooms**          | Nombre de salles de bain                        | 2       |
| **Latitude**           | Coordonnée géographique (°)                     | 39.90   |
| **Longitude**          | Coordonnée géographique (°)                     | -86.15  |
| **Living Area (sqft)** | Surface habitable en pieds carrés               | 2 000   |
| **House Age (years)**  | Âge de la maison                                | 10      |
| **Zipcode**            | Code postal à 5 chiffres (voir liste ci-dessus) | 46220   |

**Remarque :**
Les valeurs de **latitude** et **longitude** peuvent être obtenues très facilement à partir de l’adresse du bien via **Google Maps**
(clic droit → *“Qu’y a-t-il ici ?”*).
Ces coordonnées sont essentielles, car le modèle les utilise pour **calculer la distance par rapport au centre-ville d’Indianapolis**, une variable clé dans la prédiction des prix.

## 4. Architecture du système

Le pipeline de prédiction repose sur trois composants déployés sur Hugging Face :

1. **Conteneur du modèle** — héberge le modèle XGBoost entraîné.
2. **Backend FastAPI** — reçoit les données (JSON) et renvoie les prédictions via une API REST.
3. **Frontend Gradio** — fournit l’interface utilisateur interactive accessible en ligne.

La communication entre les conteneurs suit le schéma suivant :

[Gradio UI] ⇄ [FastAPI Backend] ⇄ [XGBoost Model]

Chaque requête saisie dans l’interface est transmise à l’API, qui interroge le modèle et renvoie le prix estimé.

## 5. Fiabilité du modèle

Le modèle déployé montre :
- **Une haute précision** sur les maisons standards (< 1 M$) : MAE = 45 195 $ → erreur relative = **12,8 %**.
- **Une stabilité satisfaisante** sur les maisons de luxe (≥ 1 M$) : MAE = 531 241 $ → erreur relative = 29,6 %.  

Il constitue donc un **estimateur robuste et interprétable** pour le marché immobilier de la métropole d’Indianapolis.

## 6. Conclusion

L’**Indy House Price Predictor** combine un modèle de machine learning avancé et une interface web simple et accessible.
Il illustre comment **la data science, la géolocalisation et le déploiement d’API** peuvent être intégrés pour offrir des **prédictions de prix locales en temps réel**.
Ce n’est pas seulement une démonstration technique : c’est un outil pratique d’aide à la décision.
Il permet à un professionnel de l’immobilier d’obtenir une première estimation rapide et cohérente d’un bien,
et à un particulier de situer facilement la valeur de sa maison sur le marché local.
Fiable, transparent et accessible, il illustre le potentiel de la data science appliquée à l’immobilier réel.