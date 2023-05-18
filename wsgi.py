# import app from movie_app
from movie_app import movie_app

#run app with host (0.0.0.0) which is all host available 
#not because its testing project i use debug = true to make tester see if theres any error with it 
if __name__ == "__main__":
    movie_app.run(host='0.0.0.0',debug=True)