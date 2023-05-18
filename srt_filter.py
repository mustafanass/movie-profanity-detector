from flask import render_template, redirect, url_for, request, Blueprint
from movie_models import movie_db ,movie_words_lists , movie_video_info , srt_detector_words
import pysrt


srt_filter = Blueprint('srt_filter',__name__)

@srt_filter.route("/words_durations")
def words_durations():
    sql1 = movie_db.session.execute(movie_db.select(movie_video_info)).scalars() # use data saved i database and return it to html to handle it and re-proccess it
    return render_template("words_filter.html" , sql1 = sql1)

@srt_filter.route("/words_durations_process" , methods=['POST', 'GET'])
def words_durations_process():
    if request.method == "POST" and "video_id" in request.form : # check POST request of video_id which is come from database 
        video_id = request.form['video_id'] # save it to variable
        conv_video_id_int = int(video_id) # i use int() to change data type of video_id to int which is same in databse tables , note in html i use number but for more secure i use int() functions to recheck it 
        sql1 = movie_db.session.execute(movie_db.select(movie_video_info).where(movie_video_info.id == conv_video_id_int , movie_video_info.movie_check_status == "not_check")).scalar()# get rows of movie video info and use where with id that get it from POST REQUEST
                                                                                                                                                                                        # also check movie_check_status is not_check to make sure its first time video to be checked 
        sql2 = movie_db.session.execute(movie_db.select(movie_words_lists)).scalars() # get lists of all words in database
        if sql1 is not None :
            if sql2 is not None :# note theres problem with scalars() when use if with it but its safe for now
                movie_name = sql1.movie_name # get movie name from database
                movie_srt = sql1.movie_srt_path # get path of srt files to access it
                movie_str_path = str(movie_srt) # make sure movie srt files in string type 
                srt_file = pysrt.open(movie_str_path)# using package pysrt to open srt path
                sql2_word_list = [] # create empty list this list will get all info from sql2 tables thats handle words list
                for value in sql2: # loop over sql2 value and save only words name which is -> (words_detector) in tables
                    sql2_word_list.append(value.words_detector)
                #print(sql2_word_list) # this print() methods may be help if any error raise so its print all list after append
                for line in srt_file:#read all line in srt files 
                    for value in sql2_word_list :   # then we loop over the list we created above to check every words in list to every line in srt files
                        if value in line.text.lower(): # check if word in words list is found in line of srt file then we can proccess it 
                            start_value = str(line.start) # pystr return not string datatype so we need to make it strings so we cane save it to database later
                            start_value_fixed = start_value.replace(",", ".") # ffmpeg by default in milisecond use (.) insted of (,) and srt files use (,) so we repalce all , in start_time and stop_time to (.)
                            stop_value = str(line.end)
                            stop_value_fixed = stop_value.replace(",", ".")
                            # save all value to databse to works with it later in other part of project
                            new_value = srt_detector_words(movie_name = movie_name , words = value ,srt_start_time = start_value_fixed , srt_stop_time = stop_value_fixed )
                            # its important to make (movie_db.session.add(new_value)) and (movie_db.session.commit()) inside loops to save all info in databse 
                            movie_db.session.add(new_value)
                            movie_db.session.commit()
                sql1.movie_check_status = "checked" # after finesh all proccesee now update movie_check_status to -> checked to make sure it not re-process in other time
                movie_db.session.commit()                
                return redirect(url_for("srt_filter.resault_of_srt"))
            else:
                return redirect(url_for("srt_filter.words_durations"))
        else:
            return redirect(url_for("srt_filter.words_durations"))
    else :
        return redirect(url_for("srt_filter.resault_of_srt"))


@srt_filter.route("/resault_of_srt" , methods = ['POST' , 'GET'])
def resault_of_srt():
    # this functions will return all resault from html forum which have video_name in request POST 
    if request.method == "POST" and "video_name" in request.form :
        video_name = request.form['video_name']
        sql1 = movie_db.session.execute(movie_db.select(srt_detector_words).where(srt_detector_words.movie_name == video_name)).scalars() # get all resault of video_name from database
        return render_template("words_filter_list.html", sql1 = sql1)
    else:
        return render_template("words_filter_list.html")