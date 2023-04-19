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
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, genre TEXT, rating FLOAT, box_office TEXT)")
    
    movie_key = "99b5ee6f"
    url = f"http://www.omdbapi.com/?apikey={movie_key}&type=movie&s&y=&r=json&plot=full&page=1"
    response = requests.get(url)
    data = response.json()

    movies = data["Search"]
    for movie in movies:
        id = movie["imdbID"]
        new_url = f"http://www.omdbapi.com/?apikey={movie_key}&i={id}&plot=full"
        new_response = requests.get(new_url)
        each_movie = new_response.json()

        title = each_movie["Title"]
        year = int(each_movie["Year"])
        genre = each_movie["Genre"]
        rating = float(each_movie["imdbRating"])
        box_office = each_movie["BoxOffice"]
        cur.execute("INSERT INTO movies (title, year, genre, rating, box_office) VALUES (?, ?, ?, ?, ?)", (title, year, genre, rating, box_office))
        conn.commit()

    conn.close()

movies()

#tv show information

#twitter/google information