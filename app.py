import os
from flask import Flask, request, redirect, render_template, url_for
from models import db, User, Movie
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

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    user = User.query.get(user_id)
    if user is None:
        return "User not found", 404

    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)

@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    title = request.form.get("title", "").strip()
    if title:
        movie = Movie(name=title, director=None, year=None, poster_url=None, user_id=user_id)
        data_manager.add_movie(movie)

    return redirect(url_for("get_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get("new_title", "").strip()
    if new_title:
        data_manager.update_movie(movie_id=movie_id, new_title=new_title)

    return redirect(url_for("get_movies", user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for("get_movies", user_id=user_id))

if __name__ == "__main__":
    # Ensure the data / folder exists (so SQLite can create the DB file here)
    os.makedirs(os.path.join(basedir, "data"), exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
