Step 4 — Deployment of the ML Indy Housing Model
This step describes the deployment process of the final model from the notebook 19-XGBoost-pseudohuber-fineweighting.ipynb.
The goal is to make the model accessible through a FastAPI backend and a Gradio user interface.
General Architecture
The deployment is based on three separate containers, grouped in the deployment/ directory:


indy-house-model/
Container hosting the final XGBoost model.
It was uploaded and saved to the Hugging Face Hub.
This container acts as a model repository (endpoint for the backend).

No Dockerfile; the Hugging Face container relies on a preconfigured image with no explicit Docker build.



house-price-api/
A Dockerized container based on FastAPI.
It was also uploaded to the Hugging Face Hub.
It provides a REST API exposing endpoints such as /predict, which receive a JSON input (property features) and return the predicted sale price in USD.
This backend directly queries the model container hosted on Hugging Face.


house-price-ui/
Container dedicated to the Gradio user interface, serving as a lightweight front-end for prediction testing.
It was uploaded and hosted on the Hugging Face Hub.

Again, no Dockerfile: this service runs on the default Gradio environment provided by Hugging Face Spaces.




Communication Between Containers
The communication flow is structured as follows:
[Hugging Face Gradio UI] ⇄ [Hugging Face FastAPI Backend] ⇄ [Hugging Face Model]



The user enters property characteristics into the Gradio interface.


Gradio sends the request (JSON) to the FastAPI backend over HTTP.


The backend queries the model container hosted on Hugging Face to obtain the prediction.


The result (estimated price in USD) is returned to Gradio and displayed to the user.



Key Points


Clear isolation: each component (model, API, interface) is independent, facilitating maintenance.


Interoperability: HTTP communication between containers ensures loose coupling.


Ease of updates: the hosted model on Hugging Face can be replaced without redeploying the UI or API.


Partial Dockerization: only the FastAPI backend is confirmed to be Dockerized; the Gradio and Model containers rely on managed environments.



Conclusion
This modular architecture enables a robust and scalable deployment of the model:


The XGBoost model is versioned and publicly accessible.


The API provides a clean, efficient access layer for integration with other systems.


The Gradio interface offers a simple, intuitive, and directly usable demo for end users.

