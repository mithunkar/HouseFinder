from app import app, db
from models import Listing

def initialize_database():
    with app.app_context():  #enter the app
        db.create_all()  # create the database tables
        print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()