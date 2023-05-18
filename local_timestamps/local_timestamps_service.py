# not its testing for small sets and small sound files 1s its may crash all memorys of your device 

import vosk
import wave
from movie_models import movie_db , movie_words_lists

# add path of vosk_models thats download from 
#https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip

#when you need to start this testing env you should place folder of models to same folder 

# use rows from database to access words 
sql2 = movie_db.session.execute(movie_db.select(movie_words_lists)).scalars()
#create empty list to handle words resulat from sql
list_of_words = []
for key in sql2:
    #loop over database and save resault to list 
    list_of_words.append(key.words_detector)

#note i dont upload files of https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip with project because its about 1.9G if you need to test it download form link above
model_path = "path_to_older_of_model"
#chose sound files 
audio_file = "path_of_sound_files.wav"
# load the Vosk model and access it to variable
model = vosk.Model(model_path)
# create a Vosk recognizer using the above model 
recognizer = vosk.KaldiRecognizer(model)
# oppen the audio file
with wave.open(audio_file, "rb") as audio:
    # get audio parameter
    sample_rate = audio.getframerate()
    num_channels = audio.getnchannels()
    bytes_per_sample = audio.getsampwidth()
    # set chunk size (e.g., 10 seconds) its recommended from vosk users to chunk_duration small chunk 
    chunk_duration = 10  
    chunk_size = int(sample_rate * num_channels * bytes_per_sample * chunk_duration)
    # create var
    offset = 0
    while offset < audio.getnframes():
        # access audio chunk from the sound file
        audio_data = audio.readframes(chunk_size)
        # process the audio data using the Vosk 
        if recognizer.AcceptWaveform(audio_data, sample_rate):
            # get the resault text
            recognized_text = recognizer.Result()
            # get timestamps for specific words with loops over list_of_words
            for value in list_of_words:
                start_time = None
                end_time = None
                for word in recognized_text["result"]:
                    if word["word"].lower() == value:
                        start_time = word["start"]
                        end_time = word["end"]
                        break

                # print the timestamps to terminal if you need to use it just save resaults to database likes what do on google_speech_api.py
                if start_time is not None and end_time is not None:
                    print(f"Timestamp for '{value}': Start={start_time/sample_rate}, End={end_time/sample_rate}")
                else:
                    print(f"'{value}' not found in timestamps")
        # move the offset
        offset += chunk_size
recognizer.Finalize()