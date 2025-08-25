from models import db, User, Movie

class DataManager():
    """Handles database operations for users and movies."""

    def create_user(self, name):
        """Create and store a new user."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """Retrieve all users from the database."""
        return db.session.query(User).all()

    def get_movies(self, user_id):
        """Retrieve all movies for a given user."""
        return db.session.query(Movie).filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Add a new movie to the database."""
        new_movie = Movie(**movie)
        db.session.add(new_movie)
        db.session.commit()

    def update_movie(self, movie_id, user_id, new_title):
        """Update the title of a user's movie."""
        db.session.query(Movie).filter(
            Movie.id == movie_id,
            Movie.user_id == user_id
        ).update({"name": new_title})
        db.session.commit()

    def delete_movie(self, movie_id, user_id):
        """Delete a movie belonging to a user."""
        db.session.query(Movie).filter(
            Movie.id == movie_id,
            Movie.user_id == user_id
        ).delete()
        db.session.commit()
