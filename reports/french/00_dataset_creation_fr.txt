# Etape 0 : Création du Dataset – Projet ML Indy Housing

Objectif :

Dans le cadre du projet ML Indy Housing, j’ai construit ma propre base de données immobilière à partir de zéro, 
sans dataset public préexistant.
L’objectif était de constituer un jeu de données localisé et homogène sur la région d’Indianapolis, 
en vue de modéliser les prix de vente des maisons.

Méthodologie :

J’ai développé un script Python (step3_targeted_zip_harvest.py) permettant d’automatiser la collecte de données immobilières 
par code postal (ZIP) à l’aide d’API disponibles sur RapidAPI, notamment l’API Zillow.
Le script effectue, pour chaque zone ciblée :

des requêtes successives vers les endpoints /propertyExtendedSearch, /property et /building ;

un enrichissement progressif des champs manquants (année de construction, surface du terrain, coordonnées géographiques, etc.) ;

une vérification de complétude et un filtrage des doublons avant sauvegarde.

Le processus vise à atteindre au moins 200 biens par code postal, en couvrant les principales zones résidentielles d’Indianapolis et
 de sa périphérie (Zionsville, Carmel, Fishers, Greenwood…).

Sécurité et configuration

Les paramètres sensibles (clé API, hôte RapidAPI) sont stockés dans un fichier .env non versionné, 
afin de garantir la sécurité des identifiants.
Le script est compatible avec un plan PRO (2 requêtes/s) et intègre un mécanisme de retry et 
de backoff exponentiel pour éviter tout dépassement de quota ou échec réseau.

Résultat :

Le fichier final, zillow_indy_10k_enriched.csv, regroupe plusieurs milliers d’enregistrements nettoyés et harmonisés, 
avec les principales variables explicatives nécessaires à la modélisation :

sale_price, bedrooms, bathrooms, living_area,

year_built, lot_area_sqft, zipcode, lat, lon.

Ce dataset a ensuite servi de base aux étapes de feature engineering, modélisation (RF, XGBoost, LightGBM) et 
évaluation des performances du modèle de prédiction de prix.

Conclusion :

Cette démarche illustre ma capacité à concevoir un dataset complet à partir d’API, en assurant la qualité, 
la cohérence et la traçabilité des données — compétences essentielles pour tout projet de data science appliqué à des données réelles.