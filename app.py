from flask import Flask, request, render_template, redirect
import requests
from data_manager import DataManager
from models import db, Movie
import os
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/', methods=['GET'])
def home():
  users = data_manager.get_users()
  return render_template('home.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
  name = request.form.get('name')
  data_manager.create_user(name)
  return redirect('/')


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def list_favorite_movies_by_user(user_id):
  if request.method == 'POST':
    load_dotenv()

    name = request.form.get('name')
    params = {'t': name, 'apikey': os.getenv("API_KEY")}
    response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
    movie = response.json()

    movie = {
        "name": movie['Title'],
        "director": movie['Director'],
        "year": movie['Year'],
        "poster_url": movie['Poster'],
        "user_id": user_id
    }

    data_manager.add_movie(movie)


  movies = data_manager.get_movies(user_id)
  return render_template('movies.html', movies=movies)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
  name = request.form.get('name')
  data_manager.update_movie(movie_id, user_id, name)
  return redirect(f'/users/{user_id}/movies')


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
  data_manager.delete_movie(movie_id, user_id)
  return redirect(f'/users/{user_id}/movies')


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()