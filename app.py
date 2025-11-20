from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, Movie, User
import os
import requests
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
OMDB_KEY = os.environ.get('OMDB_API_KEY')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
db.init_app(app)
data_manager = DataManager()

@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('home'))


@app.route('/user/delete', methods=['POST'])
def delete_user():
    name = request.form.get('name')
    if not name:
        flash("Please enter a user name to delete")
        return redirect(url_for('home'))
    ok = data_manager.delete_user(name)
    if not ok:
        flash(f"User '{name}' not found")
    else:
        flash(f"User '{name}' deleted")
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movie(user_id):
    movies = data_manager.get_movies(user_id)
    user = User.query.get(user_id)
    return render_template('movies.html', movies=movies, user=user)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    movie_title = request.form.get('name')
    if not movie_title:
        flash("Please enter a movie title.")
        return redirect(url_for('user_movie', user_id=user_id))
    url = "https://www.omdbapi.com/"
    params = {
        'apikey': OMDB_KEY,
        't': movie_title
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('Response') == 'True':
            year_str = data.get('Year', '0')
            try:
                year = int(year_str[:4])
            except (ValueError, TypeError):
                year = 0
            poster = data.get('Poster', '')
            if not poster or poster == 'N/A':
                poster = ''
            movie = Movie(
                name=data['Title'],
                director=data.get('Director', 'Unknown'),
                year=year,
                poster_url=poster,
                user_id=user_id
            )
            data_manager.add_movie(movie)
        else:
            flash(data.get('Error', 'Movie not found on OMDb.'))
    except requests.RequestException:
        flash("Error contacting OMDb. Please try again.")
    return redirect(url_for('user_movie', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form['name']
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('user_movie', user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movie', user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5002, debug=True)