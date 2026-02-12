print("--- Setting up environment ---")
!pip install earthengine-api pandas catboost

import ee
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor
from sklearn.metrics import r2_score
import os
import re

try:
    ee.Initialize(project='earth-469911')
    print("Earth Engine initialized")
except:
    ee.Authenticate()
    ee.Initialize(project='earth-469911')

from google.colab import drive
drive.mount('/content/drive')

BASE_PATH = "/content/drive/MyDrive/lasttry/"
TABULAR_DATA_PATH = os.path.join(BASE_PATH, "pond_dataset1.csv")

print("Setup complete")
