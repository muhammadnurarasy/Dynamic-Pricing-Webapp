HEAD
---
title: "Arasy Dynamic Pricing Webapp"
description: "Dynamic Pricing Webapp for Rental Properties in JABODETABEK"
---
# Arasy Dynamic Pricing Webapp
#### Video Demo: https://youtu.be/eQpDY745e88
#### Description: Dynamic Pricing Webapp for Rental Properties in JABODETABEK 

## Overview
This project, a final submission for the CS50 course, is a dynamic pricing application tailored for the real estate market. Leveraging advanced machine learning algorithms, the application aims to provide accurate, data-driven pricing recommendations for properties. This solution is designed to address the complexities and variabilities in real estate pricing, offering a more scientific and less subjective approach to property valuation.

## Project Components and Their Functions

### `model_training.ipynb`
- A Jupyter notebook containing the machine learning model's training process.
- It includes data preprocessing, model selection, training, and evaluation.
- Explains the rationale behind choosing specific algorithms and features for the model.

### `app.py`
- The main Flask application file.
- Handles web server initiation, route definitions, and integration with the ML model.
- Details the Flask setup and why it was chosen as the web framework.

### `api.py`
- A FastAPI application providing an alternative API for the project.
- Demonstrates the use of FastAPI for high-performance, easy-to-create APIs.
- Includes documentation on why FastAPI was considered alongside Flask.

### `layout.html` and `dashboard.html`
- HTML templates used for the web interface.
- `layout.html` contains the basic layout structure.
- `dashboard.html` is a more detailed template for the app's dashboard.
- Discusses the use of Jinja templating and HTML/CSS for frontend development.

### `Dockerfile-Flask` and `Dockerfile-FastAPI`
- Dockerfiles for containerizing the Flask and FastAPI applications.
- Illustrates the process of creating a consistent, deployable environment for the app.
- Discusses the benefits of using Docker in development and deployment phases.

### `requirements.txt`
- Lists all Python dependencies for the project.
- Ensures reproducibility and ease of setup for other developers.

## Design Choices and Debates
During development, several design choices were made and debated:
- **Choice of Machine Learning Model**: Selected for its balance of accuracy and computational efficiency.
- **Flask vs. FastAPI**: Flask was chosen for its simplicity and vast community support, while FastAPI was included to demonstrate an alternative approach.
- **Dockerization**: Opted for Docker to simplify deployment and ensure environment consistency.

## Installation and Setup
Detailed steps on setting up the project locally:
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Initialize the database.
4. Run the Flask app: `python app.py` and the FastAPI app: `uvicorn api:app`.
5. OR running both using docker-compose up


## Final Notes
This `README.md` is a comprehensive guide to understanding the structure, purpose, and functionality of the dynamic pricing app. It not only serves as a documentation but also reflects the thought process and decisions made throughout the development of this project.
