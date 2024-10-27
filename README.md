# movie profanity detector

testing project for Movie Profanity Detector not for productions 

# how install it ?

1- you should create and build python venv for project 
```
python3 -m venv movie_venv 
source movie_venv/bin/activate
```

2- install requirement package below using pip3
- flask 
- flask-sqlalchemy
- pysrt
- ffmpeg-python
- vosk and pyaudio // if you need to check and testing local local_timestamps install vosk and pyaudio else dont install them
- google.cloud 

you can use below commend in your commend line to install main package 
```
pip3 install flask flask-sqlalchemy pysrt ffmpeg-python google.cloud google-cloud-speech
```

NOTE: ffmpeg-python need to install ffmpeg to your local machine that work flask (testing with debian 12 and works every things works fine)

if you need to check testing_local_timestamps run below code in your commend line

```
pip3 install vosk pyaudio
```

3- in your main folder using python3 to run flask web server 
```
python3 wsgi.py 
```

its will be start works then open your browser and access 127.0.0.1:5000 then you can see the main page 

# important NOTE

1- google cloud speech to text api need billing and accounting for access it so i disable the functions thats handle it if you need to enable it :
- using gcloud tools to auth with your account 
- make sure you enable speech to text api in your google cloud consol 
open files "sound_filter.py" in project files and uncomment below commend

```
# google_speech_api.get_speech(movie_name_sql1)
```
 - then every thing works fine 
 
2- i use sqlalchemy to works with database and use sqllite for database 

3- if you want to re create database you can use below commecnd to re create it
```
python3 create_database.py
```

# how works ?
- from main page add words you want to filter it to database 
- from main page upload video file with (.mp4) and upload srt files 
- filter srt files with database of words then save value of resault (video_name , start_time , stop_time , words ) to new tables 
- process video.mp4 files to get filtered sound.wav files for each words withs start_tim and stop_time from srt and save it to new tables
- if you enable google cloud speech to text then project will automatically proccess sound.wav thats generate from point(4) and re-saved with timestamps 
of words in new database tables 



