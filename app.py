from flask import Flask, url_for, redirect, render_template, request, jsonify
from flask_paginate import Pagination, get_page_parameter
from pymongo import MongoClient
from bson.json_util import dumps
import json
from flask_bcrypt import Bcrypt
import numpy as np
import pandas as pd
import random,requests
from test import get_recommendations, build_chart, get_top_list

app = Flask(__name__)


@app.route('/')
#default route will get trending movies to the landing page
def index():
    details= {}
    actiondetails = {}
    comedydetails = {}
    # toplist = get_top_list().values.tolist()
    # for movie in toplist:
    #     details[movie[0]] = get_movies_details(movie[0])
    toplist = ['1917', 'Klaus ', 'Joker', 'Ford v Ferrari', 'Parasite', 'Avengers: Endgame', 'Spider-Man: Into the Spider-Verse', 'Andhadhun', 'Green Book', 'Capernaum', 'Avengers: Infinity War', 'Logan', 'Dangal', 'The Invisible Guest', 'Gangs of Wasseypur', 'Drishyam']
    for movie in toplist:
         details[movie] = get_movies_details(movie)
    #movie genres list is obtained here
    actionlist = build_chart('Action').head(16).values.tolist()
    for movie in actionlist:
        actiondetails[movie[0]] = get_movies_details(movie[0])

    comedylist = build_chart('Romance').head(15).values.tolist()
    for movie in comedylist:
        comedydetails[movie[0]] = get_movies_details(movie[0])
    return render_template('landing.html', toplist = toplist, actionlist = actionlist, comedylist = comedylist, details = details, actiondetails = actiondetails, comedydetails = comedydetails)

@app.route("/movies_details/<name>")
def movies_details(name):
    details = {}
    check = False
    URL="http://www.omdbapi.com/?apikey=64a25551&t="+name
    movie_name= requests.get(url = URL)
    data = movie_name.json()
    try:
        rec_movies = get_recommendations(name).head(5).tolist()
        for movie in rec_movies:
            details[movie] = get_movies_details(movie)
        check = True
    except:
        print(name+" doesn't exist in the database")
    if check == True:
        return render_template('moviessingle.html',movie=data, rec_movies=rec_movies, details = details)
    else:
        return render_template('moviessingle.html',movie=data)


def get_movies_details(name):
    URL="http://www.omdbapi.com/?apikey=64a25551&t="+name
    movie_name= requests.get(url = URL)
    data = movie_name.json()
    return data

@app.route('/movies/<genre>')
def get_movie_by_genre(genre):
    movie_genre_details = {}
    get_genre = build_chart(genre).head(24).values.tolist()
    for movie in get_genre:
        movie_genre_details[movie[0]] = get_movies_details(movie[0])
    return render_template('moviegrid.html', get_genre=get_genre, genre=genre, movie_genre_details=movie_genre_details)




if __name__ == "__main__":
    app.run(debug=True)