from flask import render_template, redirect, url_for, request, Blueprint
import google_speech_api 
from movie_models import movie_db ,movie_detector_words , movie_video_info , srt_detector_words
import ffmpeg , random

movie_filter = Blueprint('movie_filter',__name__)
    

@movie_filter.route("/sound_durations")
def sound_durations():
    sql1 = movie_db.session.execute(movie_db.select(movie_video_info)).scalars()
    return render_template("sound_filter.html" , sql1 = sql1)

@movie_filter.route("/sound_durations_process" , methods = ["POST" , "GET"])
def sound_durations_process():
    # check html forum request with POST
    if request.method == "POST" and "video_id" in request.form :
        video_id = request.form['video_id']
        conv_video_id_int = int(video_id)
        sql1 = movie_db.session.execute(movie_db.select(movie_video_info).where(movie_video_info.id == conv_video_id_int , movie_video_info.movie_check_status == "checked")).scalar() # use database to get value of checked video only
        if sql1 is not None :
            word_list = [] #create empty list for words 
            gen_number_set = set() # create set to make sure thers no dublcite number
            movie_name_sql1 = sql1.movie_name
            vide_path = sql1.movie_path
            conv_video_str = str(vide_path)
            sql2 = movie_db.session.execute(movie_db.select(srt_detector_words).where(srt_detector_words.movie_name == movie_name_sql1)).scalars()# get all video check value with words and time_start and time stop from database
            for item in sql2 : # loop over sql2
                word_list.append({"word_name":item.words , "start_time":item.srt_start_time , "end_time":item.srt_stop_time})# i save info i get it from database to dict with key:value to make it simple to works with it
            for value in word_list:
                input_file = conv_video_str # create new variable and save str(path) to make its more clean
                create_number = random.randint(1, 1001) # create random number to use it with sound file name
                while create_number in gen_number_set :# using while statment to make sure each files get special number
                    create_number = random.randint(1, 1001)
                gen_number_set.add(create_number)# add number to gen_number_set
                output_file = f"upload_folder/sound_folder/{movie_name_sql1}-{create_number}.wav" # create sound file name with uploaded videoname and special number and path to save it to in
                start_time = value["start_time"] # get start_time from list of dict 
                end_time = value["end_time"] # get end_time form list of dict
                try: # using try to check if theres any error with ffmpeg
                    # add files path and star and end time to ffmpeg
                    #note i use ffmpeg package in python to works with ffmpeg but its require to install ffmpeg to your machine to make it works correct
                    #if not it will raise error (testing on linux debian 12 and works very will)
                    video_input = ffmpeg.input(input_file, ss=start_time, t=end_time)
                    output_stream = ffmpeg.output(video_input, output_file, codec='libmp3lame', bitrate='320k')#config output files 
                    ffmpeg.run(output_stream) # run ffmpeg to proccess it

                    # i comment google_speech_api.get_speech(movie_name_sql1) because its need google account to works with it
                    #google_speech_api.get_speech(movie_name_sql1)

                except ffmpeg.Error as e: # use expect to check if thers any error in it its will show it 
                    if e.stderr:# if theres any known error its will rais it 
                        print('An error occurred:')
                        print(e.stderr.decode())
                    else:# else it will print (An error occurred. No additional information is available.)
                        print('An error occurred. No additional information is available.')
                    #not error will raise in terminal if use linux it s will be used in it , i dont recommended to use print to check error insted of it use sql to save error 
                    # is more advance and give you more options to handle it but because it testing purbos i do it with print .
                #save new sound files path and other tables rows to database to works with it later to upload it to google cloud or other tools .                      
                new_record = movie_detector_words(movie_name = movie_name_sql1 , words = value["word_name"] , movie_start_time = value["start_time"] , movie_stop_time = value["end_time"] , sound_file_path = output_file)
                movie_db.session.add(new_record)
                movie_db.session.commit()
            return redirect(url_for("movie_filter.resault_of_sound"))
        else:
            return redirect(url_for("movie_filter.sound_durations"))
    else:
        return redirect(url_for("movie_filter.sound_durations"))
    

@movie_filter.route("/resault_of_sound" , methods = ['POST' , 'GET'])
def resault_of_sound():
    #get all resault of vide_name input in html template from database 
    if request.method == "POST" and "video_name" in request.form :
        video_name = request.form['video_name']
        sql1 = movie_db.session.execute(movie_db.select(movie_detector_words).where(movie_detector_words.movie_name == video_name)).scalars()
        return render_template("sound_filter_list.html", sql1 = sql1)
    else:
        return render_template("sound_filter_list.html")


        