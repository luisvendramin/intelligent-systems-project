import os
import json
import requests
import pandas as pd

from joblib import dump

# Loading the csv fil with de test products data
# Preprocessing the data to the correnct json format
data = pd.read_csv(os.environ['TEST_PRODUCTS_CSV_PATH'])
data = data.head().to_json(orient='records')

parsed = json.loads(data)
parsed = {"products": parsed}

dump(parsed, os.environ['TEST_PRODUCTS_PATH']) # Saving in the path

# Testing the API
category_predicted = requests.post('http://localhost:5000/v1/categorize', json=parsed)
print(category_predicted.json())