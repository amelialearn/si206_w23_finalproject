#Team name: JAJ
#Partners: Amelia Learner, Jackson Gelbard, and Jackson Gertner

#API DATABASE FILE

import requests
import json
import sqlite3
import os

def movies():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, runtime TEXT, genre TEXT, rating FLOAT)")
    
    list_movies = []

    pop_key = "a506d5e4266f12c3ad717faf978c7d29"
    for i in range(1,7):
        pop_url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={pop_key}&language=en-US&page={i}"
        pop_res = requests.get(pop_url)
        pop_movies = pop_res.json()["results"]
        for piece in pop_movies:
            list_movies.append(piece["title"])
    
    all_movies = []
    
    for item in list_movies:
        movie_key = "99b5ee6f"
        url = f"http://www.omdbapi.com/?t={item}&apikey={movie_key}"
        response = requests.get(url)
        data = response.json()
        all_movies.append(data)

    for movie in all_movies:
        if movie["Response"] == "False":
            all_movies.remove(movie)
        else:
            title = movie["Title"]
            year = movie["Year"]
            runtime = movie["Runtime"]
            genre = movie["Genre"]
            rating = movie["imdbRating"]
            cur.execute("INSERT INTO movies (title, year, runtime, genre, rating) VALUES (?, ?, ?, ?, ?)", (title, year, runtime, genre, rating))
            conn.commit()

    conn.close()

movies()

#tv show information

#twitter/google information