from flask import *
from config import app


@app.route("/", methods=["POST", "GET"])
def index():
    pass

