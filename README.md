#MINI PROJECT#
Water Quality Prediction using Geospatial Data
Overview

This project predicts important water quality parameters using geospatial satellite data, weather information, and machine learning. The system integrates Google Earth Engine data with historical pond measurements to train predictive models that estimate water conditions for any given location and date.

The goal of this project is to demonstrate how environmental data, satellite imagery, and AI models can be combined to support smart monitoring of water bodies.

Features

Satellite feature extraction (NDVI & NDWI)

Weather data integration

Automated data fusion pipeline

Machine learning model training using CatBoost

Multi-parameter water quality prediction:

pH

Ammonia

Dissolved Oxygen

Chlorophyll

Interactive prediction application

Project Structure

data_preprocessing.py
Cleans and prepares the raw dataset.

gee_data_fetcher.py
Fetches satellite and weather data using Google Earth Engine.

data_fusion_pipeline.py
Merges environmental data into a training-ready dataset.

model_training.py
Trains and saves predictive models.

runtime_setup.py / setup_environment.py
Initializes environment and Earth Engine authentication.

prediction_app.py
Interactive prediction tool for new coordinates.

Technologies Used

Python

Google Earth Engine API

Pandas & NumPy

CatBoost Machine Learning

Geospatial satellite datasets

Workflow

Prepare and clean tabular pond data.

Retrieve satellite and temperature data.

Merge datasets into a unified feature set.

Train predictive models.

Generate water quality predictions for new inputs.

How to Run
Step 1 — Setup

Run environment setup script:

python setup_environment.py

Step 2 — Prepare Data

python data_preprocessing.py

Step 3 — Fetch & Merge Data

python data_fusion_pipeline.py

Step 4 — Train Models

python model_training.py

Step 5 — Run Prediction

python prediction_app.py

Applications

Environmental monitoring

Smart aquaculture management

Remote sensing research

Water quality analysis

Educational Purpose

This project is developed as an academic mini-project to demonstrate practical integration of geospatial analytics and machine learning.
