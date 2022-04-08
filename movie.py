from flask import Flask, jsonify, request
import csv
from content import get_recommendations
from demographic import weighted_rating

all_movies = []
liked_movies = []
disliked_movies = []
unwatched_movies = []

with open("final_movies.csv") as f:
    reader = csv.reader(f)
    data = list(reader)
    all_movies = data[1:]

app = Flask(__name__)

@app.route("/get-movies")

def get_movies():
    movie_data = {
        "title" : all_movies[0][19],
        "poster_link" : all_movies[0][27],
        "release_date" : all_movies[0][13] or "N/A",
        "duration" : all_movies[0][15],
        "rating" : all_movies[0][20],
        "overwiew" : all_movies[0][9],

    }
    return jsonify({

        "data" : movie_data,
        "status" : "SUCCESS"

    })

@app.route("/liked-movies", methods = ["POST"])


def liked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    liked_movies.append(movie)

    return jsonify({
        "status" : "SUCCESS"
    }), 200

@app.route("/disliked-movies", methods = ["POST"])


def disliked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    disliked_movies.append(movie)

    return jsonify({
        "status" : "SUCCESS"
    }), 200

@app.route("/unwatched-movies", methods = ["POST"])


def unwatched_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    unwatched_movies.append(movie)

    return jsonify({
        "status" : "SUCCESS"
    }), 200


@app.route("/popular_movies")

def popular_movies():
    movie_list = []
    
    for movie in weighted_rating:
        temp_dict = {
            "title" : movie[0],
            "poster_link" : movie[1],
            "release_date" : movie[2] or "N/A",
            "duration" : movie[3],
            "rating" : movie[4],
            "overwiew" : movie[5],
        }

        movie_list.append(temp_dict)

    return jsonify({
        "data" : movie_list,
        "status" : "SUCCESS"
    }), 200

@app.route("/recommended_movies")

def recommended_movies():
    movie_list = []
    all_recommended = []
    
    for movie in liked_movies():
        output = get_recommendations(movie[19])
        
        for data in output:
            all_recommended.append(data)
            
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended))

    for movie in all_recommended:
        temp_dict = {
            "title" : movie[0],
            "poster_link" : movie[1],
            "release_date" : movie[2] or "N/A",
            "duration" : movie[3],
            "rating" : movie[4],
            "overwiew" : movie[5],
        }

        movie_list.append(temp_dict)

    return jsonify({
        "data" : movie_list,
        "status" : "SUCCESS"
    }), 200
    

if __name__ == "__main__":
    app.run()
