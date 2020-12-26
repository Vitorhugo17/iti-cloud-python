import os
import pandas as pd
import numpy as np
import mysql.connector
import warnings
import sklearn
import pickle
from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from flask import request, Response, Flask, render_template
import json

warnings.filterwarnings('ignore')

mydb = mysql.connector.connect(
  host="eu-cdbr-west-03.cleardb.net",
  user="bbf0bb7ad96b16",
  password="bc7d6872",
  database="heroku_6190d228ed81d9a"
)

mycursor = mydb.cursor()

# creates a Flask application, named app
app = Flask(__name__)
app.config["DEBUG"] = True

# a route where we will display a welcome message via an HTML template
@app.route("/", methods=['GET'])
def home():
    mycursor.execute("SELECT * FROM training_data")
    myresult = mycursor.fetchall()
    results = []
    for x in myresult:
        result = {
            "month": x[1],
            "day": x[2],
            "temp": x[3],
            "rh": x[4],
            "wind": x[5],
            "rain": x[6],
            "y": x[7]
        }  
        results.append(result)
    
    return Response(json.dumps(results), mimetype="application/json")

# a route where we will display a welcome message via an HTML template
@app.route("/variables/values", methods=['GET'])
def variables_values():
    results = {}
    temp = []
    rh = []
    wind = []
    rain = []

    mycursor.execute("SELECT * FROM training_data")
    myresult = mycursor.fetchall()
    for x in myresult:
        temp.append(x[3])
        rh.append(x[4])
        wind.append(x[5])
        rain.append(x[6])

    results = {
        "temperature": list(dict.fromkeys(temp)),
        "humidity": list(dict.fromkeys(rh)),
        "wind": list(dict.fromkeys(wind)),
        "rain": list(dict.fromkeys(rain))
    }
    return Response(json.dumps(results), mimetype="application/json")

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)