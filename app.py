import os
from flask import Flask, request, redirect, render_template, url_for, flash
from models import db, User, Movie
from data_manager import DataManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-me"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'data', 'movies.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

data_manager = DataManager()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", message="Page not found"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/")
def index():
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Please enter a user name.", "error")
        return redirect(url_for("index"))

    user = data_manager.create_user(name)
    if user is None:
        flash("Could not create user due to a database error.", "error")
        return render_template("500.html"), 500

    flash(f"User '{name}' created.", "success")
    return redirect(url_for("index"))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    user = User.query.get(user_id)
    if user is None:
        return render_template("404.html", message="User not found"), 404

    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", user=user, movies=movies)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    user = User.query.get(user_id)
    if user is None:
        return render_template("404.html", message="User not found"), 404

    title = request.form.get("title", "").strip()
    if not title:
        flash("Please enter a movie title.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    movie = Movie(name=title, director=None, year=None, poster_url=None, user_id=user_id)

    saved = data_manager.add_movie(movie)
    if saved is None:
        flash("Could not add movie due to a database error.", "error")
    else:
        flash(f"Added movie: {title}", "success")

    return redirect(url_for("get_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get("new_title", "").strip()
    if not new_title:
        flash("Please enter a new title.", "error")
        return redirect(url_for("get_movies", user_id=user_id))

    updated = data_manager.update_movie(movie_id=movie_id, new_title=new_title)
    if updated is None:
        return render_template("404.html", message="Movie not found"), 404

    flash("Movie title updated.", "success")
    return redirect(url_for("get_movies", user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    deleted = data_manager.delete_movie(movie_id)
    if not deleted:
        return render_template("404.html", messages="Movie not found"), 404

    flash("Movie deleted", "info")
    return redirect(url_for("get_movies", user_id=user_id))

if __name__ == "__main__":
    # Ensure the data / folder exists (so SQLite can create the DB file here)
    os.makedirs(os.path.join(basedir, "data"), exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)
