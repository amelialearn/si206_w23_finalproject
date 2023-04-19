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
    num_movies = 100
    for i in range(num_movies + 1):
        imdb_id = f"tt00{i:02d}0000"
        url = f"http://www.omdbapi.com/?apikey={movie_key}&i={imdb_id}&plot=full"
        response = requests.get(url)
        movies = response.json()
        title = movies["Title"]
        year = int(movies["Year"])
        genre = movies["Genre"]
        rating = float(movies["imdbRating"])
        box_office = movies["BoxOffice"]
        cur.execute("INSERT INTO movies (title, year, genre, rating, box_office) VALUES (?, ?, ?, ?, ?)", (title, year, genre, rating, box_office))
        conn.commit()

    conn.close()

#tv show information

#twitter/google information