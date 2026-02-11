from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Relationship to movies.
    movies = db.relationship("Movie", backref="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}')"

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(300))

    # Foreign Key.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Movie(id={self.id}, name='{self.name}', director='{self.director}', "
            f"year={self.year}, user_id={self.user_id})"
        )