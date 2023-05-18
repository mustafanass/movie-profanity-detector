#config file of project create flask_app (movie_app) and config flask-sqlalchemy (using sqllite)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


#call flask for access it to movie_config
movie_app = Flask(__name__)
movie_app.secret_key = 'ewrwtyquioep8887432647826378rydyuwehgdf7823truyYUT^&@#%&*#^ugdhsdhj'

#add video_upload folder and make it access by flask
VIDEO_UPLOADS='upload_folder/video_upload/videos'
movie_app.config['video_upload'] = VIDEO_UPLOADS

#add SRT_UPLOADS folder and make it access by flask
SRT_UPLOADS='upload_folder/video_upload/srtfiles'
movie_app.config['srt_upload'] = SRT_UPLOADS

# create database and build conniction config for access it 
movie_db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))
database_info = 'sqlite:///' + os.path.join(basedir, 'movie_database.db')
movie_app.config['SQLALCHEMY_DATABASE_URI'] = database_info
movie_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#return database to flask app so it can use it and handle it
movie_db.init_app(movie_app)

