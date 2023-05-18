from flask import render_template, redirect, url_for, send_file , Blueprint
from movie_models import movie_db ,movie_words_lists , movie_video_info , srt_detector_words


#blueprint of movie_index thats will be call and use in movie_app.py
movie_index = Blueprint('movie_index',__name__)

#create index page when clients access "/" its will return index functions
@movie_index.route("/")
def index() :
    sql1 = movie_db.session.query(movie_words_lists).count() #count number of words in database and return it to html template
    sql2 = movie_db.session.query(movie_video_info).count() #count number of video uploaded in database and return it to html template
    sql3 = movie_db.session.query(srt_detector_words).count() #count number of words founded in srt files in database and return it to html template
    return render_template('index.html' , words_num = sql1 , movies_num = sql2 , srt_num = sql3) #return to template with value of sql1 , sql2 , sql3

#create list of saved words in databse and show it
@movie_index.route("/words_list") 
def words_list() :
    sql1 = movie_db.session.execute(movie_db.select(movie_words_lists)).scalars()#return all value from database and send it to tmplate to show it 
    return render_template('words_list.html' , sql1 = sql1)                      # note i use (scalars()) functions to get all rows 

#create list of uploades video in databse and show it
@movie_index.route("/video_list")
def video_list() :
    sql1 = movie_db.session.execute(movie_db.select(movie_video_info)).scalars()
    return render_template('videos_list.html' , sql1 = sql1)
