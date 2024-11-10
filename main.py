from flask import *
from config import app


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("/index.html")


@app.route("/adicionar", methods=["POST", "GET"])
def adicionar():
    return render_template("/adicionar.html")
