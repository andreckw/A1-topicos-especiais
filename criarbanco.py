from config import app, db
from models import *

with app.app_context():
    db.create_all()
