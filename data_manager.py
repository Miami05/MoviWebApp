from models import db, User, Movie


class DataManager:
    def create_user(self, name):
        """Add a new user to the database."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """Return a list of all users."""
        return User.query.all()

    def get_movies(self, user_id):
        """Return a list of all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """
        Add a new movie to a user's favorites.

        Expects `movie` to be a fully constructed Movie object, e.g.:
        Movie(name=..., director=..., year=..., poster_url=..., user_id=...)
        """
        try:
            db.session.add(movie)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

    def update_movie(self, movie_id, new_title):
        """Update the title of a specific movie."""
        movie_to_update = Movie.query.get(movie_id)
        if movie_to_update is None:
            return False
        movie_to_update.name = new_title
        db.session.commit()
        return True

    def delete_movie(self, movie_id):
        """Delete a movie from the database."""
        movie = Movie.query.get(movie_id)
        if movie is None:
            return False
        db.session.delete(movie)
        db.session.commit()
        return True