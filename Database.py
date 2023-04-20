#Team name: JAJ
#Partners: Amelia Learner, Jackson Gelbard, and Jackson Gertner

#API DATABASE FILE

import requests
import json
import sqlite3
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint

#song information
def music():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    pl_id = 'spotify:playlist:4hOKQuZbraPDIfaGbM3lKI'
    offset = 0
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + 'songs.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS songs (title TEXT, runtime TEXT)")
    cur.execute("SELECT COUNT(*) FROM songs")
    num = cur.fetchone()[0]
    if num==100:
        return


    
   

    
        

    for i in range(num,num+25):
            response = sp.playlist_items(pl_id,
                                    offset=offset,
                                    fields='items.track.name,items.track.duration_ms,total',
                                    additional_types=['track'])
            track= response["items"][i]
            track_name = track['track']['name']
            track_duration_ms = track['track']['duration_ms']
            track_duration_min = track_duration_ms / 60000  # Convert duration from milliseconds to minutes
            print(f"{track_name} - {track_duration_min:.2f} minutes")
            cur.execute("INSERT INTO songs (title, runtime) VALUES (?, ?)", (track_name, track_duration_min))
            conn.commit()
    conn.close()


def movies():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + 'movies.db')
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

    num = len(cur.fetchall())

    for i in range(num, 25):
        movie = all_movies[i]
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
#tv show information

#calling functions
music()
movies()