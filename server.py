import warnings
import flask
from flask import request, Response, jsonify
import json

warnings.filterwarnings('ignore')

# creates a Flask application, named app
app = Flask(__name__)
app.config["DEBUG"] = True

# a route where we will display a welcome message via an HTML template
@app.route("/", methods=['GET'])
def home():
    resultado = {'idUtilizador': 2}
    return Response(json.dumps(resultado),  mimetype='application/json')

app.run()