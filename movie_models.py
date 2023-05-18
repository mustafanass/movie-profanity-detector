# init tables of project databse

import sqlalchemy as urufi_alchemy
from movie_config import movie_db

# tables of words should check in projects
class movie_words_lists(movie_db.Model):
    __tablename__ = 'movie_words_lists'
    id = urufi_alchemy.Column(urufi_alchemy.Integer , primary_key = True)
    words_detector = urufi_alchemy.Column(urufi_alchemy.String(200))

#tables of movie_info
class movie_video_info(movie_db.Model):
    __tablename__ = 'movie_video_info'
    id = urufi_alchemy.Column(urufi_alchemy.Integer , primary_key = True)
    movie_name = urufi_alchemy.Column(urufi_alchemy.String(200))
    movie_path = urufi_alchemy.Column(urufi_alchemy.String(200))
    movie_srt_path = urufi_alchemy.Column(urufi_alchemy.String(200))
    movie_check_status = urufi_alchemy.Column(urufi_alchemy.String(200))

#tables of srt check for unwanted words
class srt_detector_words(movie_db.Model):
    __tablename__ = 'srt_detector_words'
    id = urufi_alchemy.Column(urufi_alchemy.Integer , primary_key = True)
    movie_name = urufi_alchemy.Column(urufi_alchemy.String(200))
    words =  urufi_alchemy.Column(urufi_alchemy.String(200)) 
    srt_start_time = urufi_alchemy.Column(urufi_alchemy.String(200))
    srt_stop_time = urufi_alchemy.Column(urufi_alchemy.String(200))

#tables of ffmpeg sound files that handle path of files which will be used to upload files to google cloud storge and then works wih speech text api
class movie_detector_words(movie_db.Model):
    __tablename__ = 'movie_detector_words'
    id = urufi_alchemy.Column(urufi_alchemy.Integer , primary_key = True)
    movie_name = urufi_alchemy.Column(urufi_alchemy.String(200))
    words =  urufi_alchemy.Column(urufi_alchemy.String(200))
    movie_start_time = urufi_alchemy.Column(urufi_alchemy.String(200))
    movie_stop_time = urufi_alchemy.Column(urufi_alchemy.String(200))
    sound_file_path = urufi_alchemy.Column(urufi_alchemy.String(200))

class movie_speech_resposn(movie_db.Model):
    __tablename__ = 'movie_speech_resposn'
    id = urufi_alchemy.Column(urufi_alchemy.Integer , primary_key = True)
    movie_name = urufi_alchemy.Column(urufi_alchemy.String(200))
    words =  urufi_alchemy.Column(urufi_alchemy.String(200))
    movie_start_time = urufi_alchemy.Column(urufi_alchemy.String(200))
    movie_stop_time = urufi_alchemy.Column(urufi_alchemy.String(200))



