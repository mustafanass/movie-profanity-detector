#NOTE_ google_speech_api was build but not tested because its need billing accounting to google cloud to enable it so i dont test it

from google.cloud import speech_v1p1beta1 as speech
from movie_models import movie_db , movie_detector_words , movie_speech_resposn , movie_words_lists
# defin function to be use in project when need to use speech to text
def get_speech(get_movie_name):
    client = speech.SpeechClient()  
    # use rows from databse with scalars() to get all rows with movie_name (get_movie_name) -> this rows for sound file path that pass to google cloud api
    sql1 = movie_db.session.execute(movie_db.select(movie_detector_words).where(movie_detector_words.movie_name == get_movie_name)).scalars()
    # use rows from database with scalars to access all words in databse and pass it to api to check it and get real time of words
    sql2 = movie_db.session.execute(movie_db.select(movie_words_lists)).scalars()
    # create list for value of sql1 which is dict of key , value ,, and list for words in database 
    list_of_sql1 = []
    list_of_words = []
    if sql1 is not None :
        #loops over database to get resaults 
        for value in sql1:
            list_of_sql1.append({"word_name":value.words , "file_path":value.sound_file_path})
        for key in sql2:
            list_of_words.append(key.words_detector)
        # config audio with audio_file_path from function
        for val in list_of_sql1:
            audio = speech.RecognitionAudio(uri=val["file_path"])
            # configure speech seting 
            # note its reqiuerd used gcloud init in your commend line to auth to your google cloud account
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
                enable_word_time_offsets=True
            )
            # create variable (response) to handle proccess and use it .
            response = client.recognize(config=config, audio=audio)
            # get transcriptions and timestamps from above response
            for result in response.results:
                alternative = result.alternatives[0]
                for word_info in alternative.words:
                    word = word_info.word
                    # check if word in list of words the get start_time and end_time of them and save it to new sql tables to works with it laters 
                    if word.lower() in list_of_words:
                        start_time = word_info.start_time.seconds + word_info.start_time.nanos 
                        end_time = word_info.end_time.seconds + word_info.end_time.nanos
                        new_timestamps = movie_speech_resposn(movie_name = get_movie_name , words = val["file_path"] , movie_start_time = start_time , movie_stop_time = end_time)
                        movie_db.session.add(new_timestamps)
                        movie_db.session.commit()

