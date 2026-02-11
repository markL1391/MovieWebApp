import os
from flask import Flask
from models import db, Movie
from data_manager import DataManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data', 'movies.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = DataManager()


@app.route("/")
def home():
    return "Welcome to MovieWeb App!"

@app.route("/users")
def list_users():
    users = data_manager.get_users()
    return str(users)


if __name__ == "__main__":
    # Ensure the data / folder exists (so SQLite can create the DB file here)
    os.makedirs(os.path.join(basedir, "data"), exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
