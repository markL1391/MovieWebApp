from models import db, User, Movie

class DataManager:
    """
    Handeles all database CRUD operations for Users and Movies.
    This class acts as the data access layer of the application.
    It encapsulates all interactions with the SQLAlchemy models.
    """

    def create_user(self, name: str) -> User:
        """
        Create and persist a new user in the database.
        :param name: Name of the user to create.
        :return: The newly created User object.
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user


    def get_users(self) -> list[User]:
        """
        Retrieve all users ordered alphabetically by name.

        :return: List of User objects.
        """
        return User.query.order_by(User.name.asc()).all()


    def get_movies(self, user_id: int) -> list[Movie]:
        """
        Retrieve all movies belonging to a specific user.

        :param user_id: ID of the user.
        :return: List of Movie objects.
        """
        return (
            Movie.query
            .filter_by(user_id=user_id)
            .order_by(Movie.name.asc())
            .all()
        )


    def add_movie(self, movie: Movie) -> Movie:
        """
        Add a new movie to the database.

        Expects a fully initialized Movie object including user_id.

        :param movie: Movie instance to persist.
        :return: The saved Movie object.
        """
        db.session.add(movie)
        db.session.commit()
        return movie


    def update_movie(
        self,
        movie_id: int,
        new_title: str | None = None,
        new_director: str | None = None,
        new_year: int | None = None,
        new_poster_url: str | None = None,
    ) -> Movie | None:
        """
        Update an existing movie's details.
        :param movie_id: ID of the movie to update.
        :param new_title: Optional new title.
        :param new_director: Optional new director.
        :param new_year: Optional new release year.
        :param new_poster_url: Optional new poster URL.
        :return: Updated Movie object or None if not found.
        """
        movie = Movie.query.get(movie_id)

        if movie is None:
            return None

        if new_title is not None:
            movie.name = new_title
        if new_director is not None:
            movie.director = new_director
        if new_year is not None:
            movie.year = new_year
        if new_poster_url is not None:
            movie.poster_url = new_poster_url

        db.session.commit()
        return movie

    def delete_movie(self, movie_id: int) -> bool:
        """
        Delete a movie from the database.

        :param movie_id: ID of the movie to delete.
        :return: True if deleted, False if movie not found.
        """
        movie = Movie.query.get(movie_id)
        if movie is None:
            return False

        db.session.delete(movie)
        db.session.commit()
        return True

