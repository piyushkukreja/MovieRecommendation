from flask import Flask, url_for, redirect, render_template, request, jsonify, logging, session
from flask_paginate import Pagination, get_page_parameter
from pymongo import MongoClient
from bson.json_util import dumps
import json
from flask_bcrypt import Bcrypt
import numpy as np
import pandas as pd
import random,requests
from test import get_recommendations, build_chart, get_top_list


client = MongoClient('127.0.0.1:27017')
db = client.blockbuster


app = Flask(__name__)


app.secret_key='mysecret'
bcrypt = Bcrypt(app)


favoritemovies = []


@app.route('/')
@app.route('/index')
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


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        users=db.users
        existing_user = users.find_one({'email_id' : request.form['email'] })

        if existing_user is None:
            pass1 = request.form['password1']
            pass2 = request.form['password2']
            if(pass1 == pass2):
                hashpass= bcrypt.generate_password_hash(request.form['password1']).decode('utf-8')       
            id=users.count() + 1
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            email_id = request.form['email']
            favourites={}
            favourites["movies"]=[]
            
            history={}
            history["movies"]=[]

            users.insert_one({
                    "id" : id,
                    "first_name" : first_name,
                    "last_name" : last_name,
                    "email_id" : email_id,
                    "password" : hashpass,
                    "history" : history,
                    "favourites": favourites
            })
            session['id']=id
            session['set']=1
            return redirect('')
        return 'The user already exists!'
    return render_template('landing.html')

@app.route('/logout')
def logout():
    session.clear()
    session['set'] = 0
    return redirect('/index')

@app.route('/login', methods=['GET', 'POST'])
def login():
    users=db.users
    login_user = users.find_one({'email_id' : request.form['email'] })
    if login_user:
        if bcrypt.check_password_hash(login_user['password'],request.form['password']):
            session.clear()
            session['id']=login_user['id']
            session['set']=1
            return redirect(url_for('index')) 
    return 'Invalid Username/Password Combination'


@app.route('/add-favourites/<name>', methods=['GET', 'POST'])
def add_to_favourites(name):
    if name not in favoritemovies:
        favoritemovies.append(name)
    else:
        return "Movie already in favorites"

    db.users.update_one(
            {"id": session['id']},
            {
                "$set": {
                    "favourites":{
                        "movies" : favoritemovies,
                    }
                }
        }
    )

    return redirect(url_for('get_favourites'))



@app.route('/userprofile')
def get_profile():
    names = db.users.find({'id' : session['id']},{'_id':0,'first_name' : 1 })
    for doc in names:
        for i in doc:
            name=doc[i]
    try:
        user_details = db.users.find({'id' : session['id']},{'_id':0,'first_name' : 1,'last_name' : 1,'email_id' : 1,'history' : 1, 'favourites' : 1 })
    except Exception as e:
        return dumps({'error' : str(e)})
    return render_template('userprofile.html', name=name, user_details=user_details)



@app.route('/userfavouritegrid')
def get_favourites():
    moviedetails = {}
    names = db.users.find({'id' : session['id']},{'_id':0,'first_name' : 1 })
    for doc in names:
        for i in doc:
            name=doc[i]
    try:
        user_favorites = db.users.find({'id' : session['id']},{'_id':0,'first_name' : 1,'last_name' : 1,'email_id' : 1,'history' : 1, 'favourites' : 1 })
        movielist = []
        for doc in user_favorites:
            for movies in doc['favourites']['movies']:
                movielist.append(movies)
                movielist=movielist
        for movie in movielist:
            moviedetails[movie] = get_movies_details(movie)
    except Exception as e:
        return dumps({'error' : str(e)})
    return render_template('userfavoritegrid.html', user_favorites=user_favorites, name=name, movielist=movielist, moviedetails=moviedetails)



@app.route('/get_user_recommendations')
def get_user_recommendation():
    details = {}
    names = db.users.find({'id' : session['id']},{'_id':0,'first_name' : 1 })
    for doc in names:
        for i in doc:
            name=doc[i]
    user_history = db.users.find({'id' : session['id']},{'_id':0,'favourites' : 1 })
    recommendation=[]
    try:
        user_details = db.users.find({'id' : session['id']},{'_id':0,'first_name' : 1,'last_name' : 1,'email_id' : 1,'history' : 1, 'favourites' : 1 })
        for doc in user_history:
            for movies in doc['favourites']['movies']:
                try:
                    temp=get_recommendations(movies).head(3).values.tolist()
                
                    recommendation.append(temp)
                    recommendation=recommendation
                except:
                    pass
        for movies in recommendation:
            for movie in movies:
                details[movie] = get_movies_details(movie)
    except:
        print("movie doesn't exist in the database")
    return render_template('recommended.html', recommendation=recommendation, name=name, user_details=user_details, details=details)





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