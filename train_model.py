import pandas as pd
import numpy as np
import mysql.connector
import warnings
import sklearn
import pickle
from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

mydb = mysql.connector.connect(
  host="eu-cdbr-west-03.cleardb.net",
  user="bbf0bb7ad96b16",
  password="bc7d6872",
  database="heroku_6190d228ed81d9a"
)

mycursor = mydb.cursor()

month = []
day = []
temp = []
rh = []
wind = []
rain = []
y_array = []

mycursor.execute("SELECT * FROM training_data")
myresult = mycursor.fetchall()
for x in myresult:
    month.append(x[1])
    day.append(x[2])
    temp.append(x[3])
    rh.append(x[4])
    wind.append(x[5])
    rain.append(x[6])
    y_array.append(x[7])      

data = {"y": y_array, "month": month, "day": day, "temp": temp, "rh": rh, "wind": wind, "rain": rain}  
df = pd.DataFrame(data, columns = ["y", "month","day","temp","rh","wind","rain"])

df = pd.get_dummies(df)

X = df.drop('y', axis = 1)
y = df['y']

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2)

# model = LogisticRegression()
# model.fit(X_train, Y_train)
# pickle.dump(X_test, open("models/X_test.csv", 'wb'))
# pickle.dump(Y_test, open("models/Y_test.csv", 'wb'))
# pickle.dump(model, open("models/model.sav", 'wb'))

model = pickle.load(open("models/model.sav", 'rb'))
X_test = pickle.load(open("models/X_test.csv", 'rb'))
Y_test = pickle.load(open("models/Y_test.csv", 'rb'))

n_score = model.score(X_test, Y_test)

z = n_score * 100.0

predict_y_p = model.predict_proba(X_test)
predict_y = model.predict(X_test)
print("Accuracy: %.2f%%" % z)