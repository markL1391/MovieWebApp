import os
from flask import Flask, request, render_template, url_for
from werkzeug.utils import redirect

from models import db, Movie
from data_manager import DataManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data', 'movies.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = DataManager()


@app.route("/")
def index():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    name = request.form.get("name", "").strip()
    if name:
        data_manager.create_user(name)
    return redirect(url_for("index"))

@app.route('/users/<int:user_id>/movies', methods=['GET','POST'])
def get_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return str(movies)
#def user_movies(user_id):
    #if request.method == "POST":


#@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])

#@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])

if __name__ == "__main__":
    # Ensure the data / folder exists (so SQLite can create the DB file here)
    os.makedirs(os.path.join(basedir, "data"), exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
