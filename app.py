from flask import Flask, request, render_template, redirect
import requests
from data_manager import DataManager
from models import db
import os
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def index():
    """Render the homepage with a list of users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    """Add a new user from form input."""
    name = request.form.get('name')
    data_manager.create_user(name)
    return redirect('/')


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def list_favorite_movies_by_user(user_id):
    """List or add favorite movies for a user."""
    if request.method == 'POST':
        load_dotenv()
        name = request.form.get('name')
        params = {'t': name, 'apikey': os.getenv("API_KEY")}

        try:
            response = requests.get('https://www.omdbapi.com/', params=params, timeout=5)
            response.raise_for_status()
            movie_data = response.json()

            if movie_data.get("Response") != "True":
                return render_template('error.html', message="Movie not found in OMDb API."), 404

            movie = {
                "name": movie_data['Title'],
                "director": movie_data['Director'],
                "year": movie_data['Year'],
                "poster_url": movie_data['Poster'],
                "user_id": user_id
            }
            data_manager.add_movie(movie)

        except requests.RequestException as e:
            return render_template('error.html', message=f"OMDb request failed: {e}"), 500

    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.errorhandler(404)
def page_not_found(error):
    """Render a custom 404 error page."""
    return render_template('404.html', message="Oops! Page not found."), 404


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """Update the title of a user's movie."""
    name = request.form.get('name')
    data_manager.update_movie(movie_id, user_id, name)
    return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a movie from a user's list."""
    data_manager.delete_movie(movie_id, user_id)
    return redirect(f'/users/{user_id}/movies')


if __name__ == '__main__':
    """Initialize database and run the Flask app."""
    with app.app_context():
        db.create_all()

    app.run()
