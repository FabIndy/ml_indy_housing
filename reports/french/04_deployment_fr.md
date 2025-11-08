# Étape 4 — Déploiement du modèle ML Indy Housing

Cette étape décrit la **démarche de déploiement** du modèle final issu du notebook `19-XGBoost-pseudohuber-fineweighting.ipynb`.
L’objectif est de rendre le modèle accessible via une **API FastAPI** et une **interface utilisateur Gradio**.

## Architecture générale

Le déploiement repose sur **trois conteneurs distincts**, regroupés dans le répertoire `deployment/` :

1. **`indy-house-model/`**
   Conteneur hébergeant le modèle XGBoost final.
   Il a été chargé et sauvegardé dans Hugging Face Hub.
   Ce conteneur sert de **référentiel de modèle** (point d’accès pour le backend).
   > Aucun `Dockerfile`; le conteneur Hugging Face repose sur une image pré-configurée, sans construction Docker explicite.

2. **`house-price-api/`**
   Conteneur **Dockerisé** basé sur **FastAPI**.
   Il a été chargé et sauvegardé dans Hugging Face Hub.
   Il fournit une **API REST** exposant des endpoints tels que `/predict`, permettant de recevoir un JSON en entrée (features d’un bien immobilier) et de retourner le prix prédit en dollars.
   Ce backend interroge directement le conteneur du modèle hébergé sur Hugging Face.

3. **`house-price-ui/`**
   Conteneur dédié à l’**interface utilisateur Gradio**, qui sert de front-end léger pour tester les prédictions.
   Il a été chargé et sauvegardé dans Hugging Face Hub.
   > Là encore, aucun `Dockerfile` : le lancement du service s'appuie sur l’environnement par défaut de Gradio dans Hugging Face Spaces.

---

## Communication entre les conteneurs

La communication suit le schéma suivant :

[Hugging Face Gradio UI]  ⇄  [Hugging Face FastAPI Backend]  ⇄  [Hugging Face Model]

1. L’utilisateur saisit les caractéristiques d’un bien immobilier dans **l’interface Gradio**.
2. Gradio envoie la requête (JSON) au **backend FastAPI** via HTTP.
3. Le backend appelle le **modèle hébergé** sur Hugging Face pour obtenir la prédiction.
4. Le résultat (prix estimé en USD) est renvoyé à Gradio, puis affiché à l’écran.

---

## Points clés

- **Isolation claire** : chaque composant (modèle, API, interface) est séparé, ce qui facilite la maintenance.
- **Interopérabilité** : la communication HTTP entre conteneurs garantit un couplage faible.
- **Simplicité de mise à jour** : le modèle hébergé sur Hugging Face peut être remplacé sans redéployer l’interface ni l’API.
- **Dockerisation partielle** : seul le backend FastAPI est confirmé comme Dockerisé ; les conteneurs Gradio et Model reposent sur des environnements managés.

---

## Conclusion

Cette architecture modulaire permet un **déploiement robuste et évolutif** du modèle :
- Le modèle XGBoost est versionné et accessible en ligne.
- L’API assure une exposition claire et rapide pour l’intégration future dans d’autres services.
- L’interface Gradio offre une démonstration utilisateur simple, intuitive et directement exploitable.
