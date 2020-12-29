import os
import datetime
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

months_index = {'jan':'01','feb': '02','mar': '03','apr': '04','may': '05',
           'jun': '06','jul': '07','aug': '08','sep': '09','oct': '10','nov': '11','dec': '12'}
  
months_names = {'01': 'jan','02': 'feb','03': 'mar','04': 'apr','05': 'may',
           '06': 'jun','07': 'jul','08': 'aug','09': 'sep','10': 'oct','11': 'nov','12': 'dec'}

mydb = mysql.connector.connect(
  host='eu-cdbr-west-03.cleardb.net',
  user='bbf0bb7ad96b16',
  password='bc7d6872',
  database='heroku_6190d228ed81d9a'
)

# creates a Flask application, named app
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/forest/fire/probability', methods=['GET'])
def forest_fire_probability():
    results = []
    
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM sensors_data')
    myresult = mycursor.fetchall()
    mycursor.close()

    local_data = pd.DataFrame(columns=['local','month','day_of_week','day','temperature','rh','wind','rain','time'])

    for x in myresult:
        row = {
            'local': x[1],
            'month': x[2],
            'day_of_week': x[3],
            'day': x[4],
            'temperature': x[5],
            'rh': x[6],
            'wind': x[7],
            'rain': x[8],
            'time': x[9].total_seconds()
        }
        local_data = local_data.append(row, ignore_index=True)
      
    # change month to number
    local_data['month'] = local_data['month'].apply(lambda x: months_index[x])
    # sort descending dataframe by local, month, day, time 
    local_data = local_data.sort_values(by=['local','month','day','time'], ascending=False, kind='quicksort')
    # remove older entries
    local_data = local_data.drop_duplicates(subset=['local'], ignore_index=False)

    # reset index values
    local_data = local_data.reset_index(drop=True)
    
    #separate variables not use in prediction from the variables used in prediction
    time_data = local_data[['local','day','time']]
    local_data = local_data.drop(labels=['local','day','time'], axis=1)
    local_data = local_data.rename(columns={'day_of_week': 'day', 'temperature': 'temp'})
    
    # change month number to month name
    local_data['month'] = local_data['month'].apply(lambda x: months_names[x])

    # apply one-hot encoding to dataframe
    data_pred = pd.get_dummies(local_data)

    #load model and model used to train data to get columns names
    model = pickle.load(open('models/model.sav', 'rb'))
    X_data = pickle.load(open('models/X_test.csv', 'rb'))

    # remove all values from train data dataframe
    X_data = pd.DataFrame(columns=X_data.columns)

    # add columns from X_data that do not appear in data_pred and fill NaN with 0
    data_pred = pd.concat([X_data,data_pred], axis=0, ignore_index=True)
    data_pred = data_pred.fillna(0)

    print(local_data)
    print(data_pred)

    # predict fire probability
    pred = model.predict_proba(data_pred)

    for x in range(len(pred)):
        result = {
            'local': time_data.iloc[x]['local'],
            'probability': pred[x][1]
        }

        results.append(result)

    print(results)

    return render_template("risco_incendio.html", results=json.dumps(results))
    # return Response(json.dumps(results), mimetype='application/json')


@app.route('/sensors/data', methods=['POST'])
def sensores_data():
    req_data = request.get_json(force=True)
 
    local = req_data['local']
    month = req_data['month']
    day_of_week = req_data['day_of_week']
    day = req_data['day']
    temperature = req_data['temperature']
    rh = req_data['rh']
    wind = req_data['wind']
    rain = req_data['rain']
    time = req_data['time']
    
    val = (local,month,day_of_week,day,temperature,rh,wind,rain,time)

    sql = 'INSERT INTO sensors_data (local,month,day_of_week,day,temperature,rh,wind,rain,time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'

    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    
    mydb.commit() 

    print(mycursor.rowcount, 'record inserted.')
    mycursor.close()

    return Response(json.dumps(val), mimetype='application/json')
  

@app.route('/', methods=['GET'])
def home():
    temperature = []
    humidity = []
    wind = []
    rain = []

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM training_data')
    myresult = mycursor.fetchall()
    mycursor.close()
    
    for x in myresult:
        temperature.append(x[3])
        humidity.append(x[4])
        wind.append(x[5])
        rain.append(x[6])

    temperature = list(dict.fromkeys(temperature))
    humidity = list(dict.fromkeys(humidity))
    wind = list(dict.fromkeys(wind))
    rain = list(dict.fromkeys(rain))
    
    return render_template(
        'envio_dados.html',
        temperature=temperature, 
        humidity=humidity, 
        wind=wind, 
        rain=rain)

if __name__ == '__main__':
    app.run()