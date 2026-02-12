print("--- Setting up the environment ---")
!pip install earthengine-api pandas catboost

import ee
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import os
import re

try:
    ee.Initialize(project='earth-469911')
    print("Google Earth Engine initialized successfully.")
except Exception as e:
    print("Authentication needed. Please follow the prompts.")
    ee.Authenticate()
    ee.Initialize(project='earth-469911')

from google.colab import drive
drive.mount('/content/drive')

BASE_PATH = "/content/drive/MyDrive/lasttry/"

def get_gee_timeseries_for_location(row):
    try:
        point = ee.Geometry.Point(row['long'], row['lat'])
        start_date = '2019-01-01'
        end_date = '2025-10-11'

        s2_image = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(point) \
            .filterDate(start_date, end_date) \
            .sort('CLOUDY_PIXEL_PERCENTAGE') \
            .first()

        if s2_image is None:
            return None, None

        ndwi = s2_image.normalizedDifference(['B3', 'B8']).rename('ndwi')
        ndvi = s2_image.normalizedDifference(['B8', 'B4']).rename('ndvi')

        s2_features = ndwi.addBands(ndvi).reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10
        ).getInfo()

        era5_daily = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR') \
            .filterDate(start_date, end_date) \
            .select('temperature_2m')

        def extract_values(image):
            mean_temp = image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=11132
            ).get('temperature_2m')

            return ee.Feature(None, {
                'date': image.date().format('YYYY-MM-dd'),
                'avg_temp_celsius': mean_temp
            })

        weather_info = era5_daily.map(extract_values).getInfo()

        dates = [f['properties']['date'] for f in weather_info['features']]
        temps = [f['properties']['avg_temp_celsius'] for f in weather_info['features']]
        temps_celsius = [t - 273.15 if t is not None else None for t in temps]

        weather_df = pd.DataFrame({
            'date_str': dates,
            'avg_temp_celsius': temps_celsius
        })

        weather_df['date_only'] = pd.to_datetime(weather_df['date_str']).dt.date

        return s2_features, weather_df[['date_only', 'avg_temp_celsius']]

    except Exception as e:
        print(f"Could not process GEE data for the given point. Error: {e}")
        return None, None

print("Setup complete. You can now run the prediction cell.")
