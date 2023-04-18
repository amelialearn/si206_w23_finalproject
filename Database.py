#Team name: JAJ
#Partners: Amelia Learner, Jackson Gelbard, and Jackson Gertner

#API DATABASE FILE

import requests
import json
import sqlite3
import os

#movie information
movie_key = "99b5ee6f"
url = f"http://www.omdbapi.com/?apikey={movie_key}&" #change the url to be from the top 100 movies in 21st century
response = requests.get(url)
movies = response.json()

for movie in movies:
    title = movie["Title"]
    year = int(movie["Year"])
    genre = movie["Genre"]
    rating = float(movie["imdbRating"])
    box_office = movie["BoxOffice"]

    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, year INTEGER, genre TEXT, rating FLOAT, box_office TEXT);")
    cur.execute("INSERT INTO movies (title, year, rating, box_office) VALUES (?, ?, ?, ?, ?, ?)", (title, year, genre, rating, box_office))
    conn.commit()
conn.close()

#tv show information

#twitter/google information