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
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, runtime TEXT, genre TEXT, rating FLOAT, box_office TEXT)")
    
    list_movies = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", "Schindler's List", "The Lord of the Rings: The Return of the King", "12 Angry Men", "The Godfather Part II", "Pulp Fiction", "Inception", "The Lord of the Rings: The Fellowship of the Ring", "Fight Club"]
    all_movies = []

    for item in list_movies:
        movie_key = "99b5ee6f"
        url = f"http://www.omdbapi.com/?t={item}&apikey={movie_key}"
        response = requests.get(url)
        data = response.json()
        all_movies.append(data)

    for movie in all_movies:
        title = movie["Title"]
        year = int(movie["Year"])
        runtime = movie["Runtime"]
        genre = movie["Genre"]
        rating = float(movie["imdbRating"])
        box_office = movie["BoxOffice"]
        cur.execute("INSERT INTO movies (title, year, runtime, genre, rating, box_office) VALUES (?, ?, ?, ?, ?, ?)", (title, year, runtime, genre, rating, box_office))
        conn.commit()

    conn.close()

movies()

#tv show information

#twitter/google information