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

#TVSHOES!!

# sources: https://www.w3resource.com/sql/creating-and-maintaining-tables/primary-key.php
#          https://www.youtube.com/watch?v=FrTQSPSbVC0
#          https://www.youtube.com/watch?v=I5L3OJ-xtsw
#          https://www.youtube.com/watch?v=Anxj5AmSG2E

# this function uses BeautifulSoup to extract the runtime from each tv show's imdb page
def get_runtime(url):
    # saw this on https://www.youtube.com/watch?v=I5L3OJ-xtsw
    # sends a request to the imdb url
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers = headers)

    # use BeautifulSoup to find the runtime element
    soup = BeautifulSoup(response.content, 'html.parser')
    runtime_element = soup.find('li', {'data-testid': 'title-techspec_runtime'})

    # extract runtime information, return text
    if runtime_element:
        runtime = runtime_element.find('div', {'class': 'ipc-metadata-list-item__content-container'}).text.strip()
        return runtime
    # if not found, return "N/A"
    else:
        return 'N/A'

# creats a new table (if it doesn't exist) in the database called "tv_shows"
def create_tv_shows_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS tv_shows (key_ID INTEGER PRIMARY KEY, imdb_ID TEXT UNIQUE, year TEXT, title TEXT, runtime TEXT, FOREIGN KEY (key_ID) REFERENCES show_info(key_ID))")

# creats a new table (if it doesn't exist) in the database called "show_info"
def create_show_info_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS show_info (key_ID INTEGER PRIMARY KEY, imdb_rating TEXT)")

def populate_database(cursor, item):
    # add information to db the item and fetch the runtime information
    show_id = item['id']
    title = item['title']
    year = item['year']
    imdb_rating = item['imDbRating']
    url = f"https://www.imdb.com/title/{show_id}/"
    runtime = get_runtime(url)

    # add the IMDB rating to the show_info table
    cursor.execute("INSERT OR IGNORE INTO show_info (imdb_rating) VALUES (?)", (imdb_rating,))
    # get the id of the last row
    title_id = cursor.lastrowid

    # add to the tv_shows table
    cursor.execute("INSERT OR IGNORE INTO tv_shows (key_ID, imdb_ID, year, title, runtime) VALUES (?, ?, ?, ?, ?)", (title_id, show_id, year, title, runtime))

def tv_shows():
    # create a path to the databas
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'TV_shows74.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    create_show_info_table(cursor)
    create_tv_shows_table(cursor)

    # get tv shows from IMDB API
    data = requests.get("https://imdb-api.com/en/API/MostPopularTVs/k_i1gw86cb").json()
    new_items = 0
    tv_shows = data['items']
    for show in tv_shows:
        # check if the Tv show is already in the database
        cursor.execute("SELECT COUNT(*) FROM tv_shows WHERE imdb_ID = ?", (show['id'],))
        count = cursor.fetchone()[0]

        # if the TV show is not in the database, add it
        if count == 0:
            populate_database(cursor, show)
            new_items = new_items + 1
            # limit the number of new TV shows added to 25
            if new_items >= 25:
                break

    conn.commit()
    conn.close()

#MUSIC!!!!!
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

#MOVIES
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


#calling functions
music()
movies()
tv_shows()