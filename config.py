from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "aaaaaaaaaaa"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'

db = SQLAlchemy()
db.init_app(app)
