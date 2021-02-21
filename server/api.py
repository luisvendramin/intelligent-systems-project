import os
import json
import pandas as pd

from joblib import dump, load
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

MODEL = load(os.environ['MODEL_PATH'])
LABELS = load(os.environ['LABELS_PATH'])

@app.route('/hello', methods=['GET'])
def teste():
    return ("Hello")
    
@app.route('/v1/categorize', methods=['POST'])
def model(model=MODEL, labels=LABELS):
    data = json.dumps(request.json['products'])  
    data = pd.read_json(data, orient='records')
    
    if len({'title', 'concatenated_tags'}.intersection(set(data.columns)))!=2:
        return 'The columns "title" and "concatenated_tags" are not into     the data.', 400
    
    #Preprocessing
    X = (data['title'].str.upper()+' '+data['concatenated_tags'].str.upper()).fillna('')
    
    # Predict
    response = {"categories": labels.inverse_transform(model.predict(X)).tolist()}
    
    return json.dumps(response)