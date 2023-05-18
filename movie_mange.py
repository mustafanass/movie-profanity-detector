from flask import render_template, redirect, url_for,  request , Blueprint
from movie_models import movie_db, movie_words_lists , movie_video_info
from werkzeug.utils import secure_filename
import os
from movie_config import movie_app

movie_mange = Blueprint('movie_mange',__name__)

@movie_mange.route("/add_words" , methods = ['GET', 'POST']) #this functions will add word in POST request from html forum and save it to database to work with it later
def add_words() :
    if request.method == "POST" and "add_words" in request.form : #check if requst from html template and check if (add_words) in request from html forum
        add_words = request.form['add_words'] #create variable to handle value of add_words to works with it laters
        sql1 = movie_db.session.execute(movie_db.select(movie_words_lists).where(movie_words_lists.words_detector == add_words)).scalar()# check if word in (add_words) is allready in database
        if sql1 is not None :
            msg = "هذه الكلمة مضافة مسبقا"
            return render_template('add_words.html', msg = msg) # if word in database then render it to html template with msg => error for clients
        else :
            new_words = movie_words_lists(words_detector = add_words) # if its not in databse then we create new rows to add it in databse
            movie_db.session.add(new_words)
            movie_db.session.commit()
            return redirect(url_for("movie_index.words_list"))# we use redirect insted of render_template to send request after finesh to words_list function in movie_index 
    else :
        return render_template("add_words.html")#if request is not POST then will retern to template without variable
    
def allowed_file(filename): # create function to check extensions of uploaded files if it {mp4 , srt} then uploaded it else will raise error
    ALLOWED_EXTENSIONS = {'mp4' , 'srt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@movie_mange.route("/upload_video" , methods = ['GET', 'POST'])
def upload_video() :
    if request.method == 'POST' and "video_name" in request.form: # check if request_methods is POST and video_name in request
        if 'video' and 'srt' not in request.files: # check if file (video , srt) is not in request then return template with msg error
            msg = "قم بتحديد الملف المراد رفعه"
            return render_template("upload_video.html" , msg =msg)
        video = request.files['video'] 
        srt = request.files['srt'] #save value of file uploaded to variable
        if video.filename == '' and srt.filename == '': # recheck if path of files is empty then retrurn error with msg 
            msg = "لايجب ان يكون الملف فارغ"
            return render_template("upload_vide.html" , msg =msg)
        if (video and allowed_file(video.filename)) and (srt and allowed_file(srt.filename)):#nested check if video and srt in allow extensions function
            video_name = request.form['video_name']
            video_filename = secure_filename(video.filename) # flask community suggest to use werkzeug.utils to be more secure files save 
            video.save(os.path.join(movie_app.config['video_upload'], video_filename))# then use os package to save files to specifed folders
            srt_filename = secure_filename(srt.filename)
            srt.save(os.path.join(movie_app.config['srt_upload'], srt_filename))
            #after save files to folders now we save info of files to database with files path to works with it laters
            #note we add movie_check_status in databse this will using it later when check srt files and i do it make video check just first time 
            #the default value for movie_check_status = not_check 
            new_video = movie_video_info(movie_name = video_name , movie_path = f"upload_folder/video_upload/videos/{video_filename}" , movie_srt_path = f"upload_folder/video_upload/srtfiles/{srt_filename}" , movie_check_status = "not_check")
            movie_db.session.add(new_video)
            movie_db.session.commit()
            return redirect(url_for("movie_index.video_list"))
    return render_template('add_videos.html')