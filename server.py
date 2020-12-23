# imports
import pandas as pd
import numpy as np
import warnings
import flask
from flask import request, Response, jsonify, render_template
import json

warnings.filterwarnings('ignore')


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return render_template('./index.html')

app.run()
