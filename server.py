import os
import warnings
from flask import request, Response, Flask
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

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)