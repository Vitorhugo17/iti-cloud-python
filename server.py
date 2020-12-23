import os
import warnings
from flask import request, Response, Flask, render_template
import json

warnings.filterwarnings('ignore')

# creates a Flask application, named app
app = Flask(__name__)
app.config["DEBUG"] = True

# a route where we will display a welcome message via an HTML template
@app.route("/", methods=['GET'])
def home():
    resultado = {'idUtilizador': 2}
    return render_template('templates/index.html')

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)