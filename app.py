from flask import Flask
from models import db
from data_manager import DataManager
from models import Movie

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movieweb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


dm = DataManager()


@app.route("/")
def home():
    return "MovieWeb is running"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()




    app.run(debug=True)
