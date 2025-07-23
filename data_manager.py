from models import db, User, Movie

class DataManager():
    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        return db.session.query(User).all()

    def get_movies(self, user_id):
        return db.session.query(Movie).filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        new_movie = Movie(**movie)
        db.session.add(new_movie)
        db.session.commit()

    def update_movie(self, movie_id, user_id, new_title):
        db.session.query(Movie).filter(
            Movie.id == movie_id,
            Movie.user_id == user_id
        ).update({"name": new_title})
        db.session.commit()

    def delete_movie(self, movie_id, user_id):
        db.session.query(Movie).filter(
            Movie.id == movie_id,
            Movie.user_id == user_id
        ).delete()
        db.session.commit()
