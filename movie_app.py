
#flask blueprint route handle 

from movie_config import movie_app

#blueprint for movie_index to handle its routes
from movie_index import movie_index 
movie_app.register_blueprint(movie_index)

#blueprint for movie_mange to handle its routes
from movie_mange import movie_mange 
movie_app.register_blueprint(movie_mange)

#blueprint for srt_filter to handle its routes
from srt_filter import srt_filter
movie_app.register_blueprint(srt_filter)

#blueprint for sound_filter to handle its routes
from sound_filter import movie_filter
movie_app.register_blueprint(movie_filter)