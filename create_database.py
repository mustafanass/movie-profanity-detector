from movie_config import movie_app
from movie_models import movie_db ,  movie_words_lists , movie_video_info

#if you rebuild or re create database use this by run it in vevn (movie_venv ) using python3 create_database.py 

with movie_app.app_context():
    movie_db.create_all()  # create SQLite tables