from flask import Flask
from data_manager import DataManager
from models import db, Movie

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def home():
    return "Welcome to MovieWebApp!"


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()