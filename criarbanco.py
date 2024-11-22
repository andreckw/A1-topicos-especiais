from config import app, db
from models import *

def criarbanco():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    criarbanco()
