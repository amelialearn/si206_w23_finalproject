#Team name: JAJ
#Partners: Amelia Learner, Jackson Gelbard, and Jackson Gertner

#API DATABASE FILE

import requests
import sqlite3
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
from bs4 import BeautifulSoup

# TV SHOWS
"""
input: url (string) - TV Show page from IMDB website

output: runtime (int) - returns runtime (in minutes) as an integer 
                        if no runtime exists, return "N/A"

description: This function takes the url of the IMDB TV Show page and 
             uses BeautifulSoup to parse through the html and extract
             the runtime as a string. Then, the function checks the
             format of the runtime information and converts the time 
             into an integer representing the total runtime in minutes.
             If no runtime exists, the function returns "N/A as a string
"""
def get_runtime(url):
    # saw this on https://www.youtube.com/watch?v=I5L3OJ-xtsw
    # sends a request to the imdb url
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers = headers)

    # use BeautifulSoup to find the runtime element
    soup = BeautifulSoup(response.content, 'html.parser')
    runtime_element = soup.find('li', {'data-testid': 'title-techspec_runtime'})

    # extract runtime information, return text
    # converting string withhours and minutes into integer representing total minutes
    if runtime_element:
        runtime_text = runtime_element.find('div', {'class': 'ipc-metadata-list-item__content-container'}).text.strip()
        runtime_s = runtime_text.split()
        if len(runtime_s) == 2 and runtime_s[0] != "1":
            runtime = int(runtime_s[0])
        elif len(runtime_s) == 2:
            runtime = 60
        elif len(runtime_s) == 4:
            runtime = int(runtime_s[0]) * 60 + int(runtime_s[2])
        return runtime
    # if not found, return "N/A"
    else:
        return 'N/A'

"""
input: cursor, item - item is a dictionary with TV Show information (title,
                      year, IMDB rating, and IMDB id)

output: None

description: This function takes takes a dictionary containing TV show information
             and adds the key_id, show id, title, and runtime (calls get_runtime) to the 
             'tv shows' table in the database, if it does not already exist. It also 
             uses a primary integer key, key_ID to input the IMDB rating data for the 
             corresponsing movie in the show_info table. 
"""
def populate_database(cursor, item):
    # add information to db the item and fetch the runtime information
    show_id = item['id']
    title = item['title']
    year = int(item['year'])
    imdb_rating = item['imDbRating']
    if imdb_rating != "":
        imdb_rating = float(imdb_rating)
    url = f"https://www.imdb.com/title/{show_id}/"
    runtime = get_runtime(url)

    # add the IMDB rating to the show_info table
    cursor.execute("INSERT OR IGNORE INTO show_info (imdb_rating) VALUES (?)", (imdb_rating,))
    # get the id of the last row
    title_id = cursor.lastrowid

    # add to the tv_shows table
    cursor.execute("INSERT OR IGNORE INTO tv_shows (key_ID, imdb_ID, year, title, runtime) VALUES (?, ?, ?, ?, ?)", (title_id, show_id, year, title, runtime))

"""
input: None

output: None

description: This function retrieves the most popular TV shows from the IMDB API
             and checks if the TV show is already in the table. If it is not, the
             function calls populate_database and adds information to the database
             for 25 TV shows.
"""
def tv_shows():
    # create a path to the database
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'TOP100.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # creats a new table (if it doesn't exist) in the database called "tv_shows"
    cursor.execute("CREATE TABLE IF NOT EXISTS tv_shows (key_ID INTEGER PRIMARY KEY, imdb_ID TEXT UNIQUE, year TEXT, title TEXT, runtime TEXT, FOREIGN KEY (key_ID) REFERENCES show_info(key_ID))")
    # creats a new table (if it doesn't exist) in the database called "show_info"
    cursor.execute("CREATE TABLE IF NOT EXISTS show_info (key_ID INTEGER PRIMARY KEY, imdb_rating TEXT)")
   
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

"""
input: None

output: None

description: This function populates the song table in the database with information
             about songs from a Spotify playlist. It uses the Spotify API to retrieve
             the song title, duration, and release year. This function checks the number
             of rows in the songs table, and if there are less than 100, it will add 
             the specified information for 25 songs in the playlist.
"""
def music():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    pl_id = 'spotify:playlist:4hOKQuZbraPDIfaGbM3lKI'
    offset = 0
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + 'TOP100.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS songs (title TEXT, runtime TEXT, year TEXT)")
    cur.execute("SELECT COUNT(*) FROM songs")
    num = cur.fetchone()[0]
    if num==100:
        return

    for i in range(num,num+25):
            response = sp.playlist_items(pl_id,
                                    offset=offset,
                                    fields='items.track.name,items.track.duration_ms,items.track.album.release_date, total',
                                    additional_types=['track'])
            track= response["items"][i]
            track_name = track['track']['name']
            track_duration_ms = track['track']['duration_ms']
            track_year=int(track['track']['album']['release_date'][:4])
            track_duration_min = track_duration_ms / 60000
            cur.execute("INSERT INTO songs (title, runtime, year) VALUES (?, ?, ?)", (track_name, track_duration_min, track_year))
            conn.commit()
    conn.close()

"""
input: None

output: None

description: This function retrieves the top rated Movies from the Movie DB 
             API and collects information about those movies form the OMDB API. 
             The function checks to see if the information exisits in the database,
             if it doesn't it creates the table movies and adds the id, title, year
             runtime in minutes, genre and IMDB rating. The function checks if there 
             are already 100 movies in the database, if not, it adds the information 
             from 25 new movies to the table.
"""
def movies():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + 'TOP100.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, runtime_mins INTEGER, genre TEXT, rating FLOAT)")
    
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

    cur.execute("SELECT COUNT(*) FROM movies")
    num = cur.fetchone()[0]
    if num==100:
        return

    for i in range(num, num + 25):
        movie = all_movies[i]
        if movie["Response"] == "False":
            all_movies.remove(movie)
        movie = all_movies[i]
        title = movie["Title"]
        year = int(movie["Year"])
        runtime_with_min = movie["Runtime"]
        runtime = int(runtime_with_min.split()[0])
        genre = movie["Genre"]
        rating = movie["imdbRating"]
        if rating != "":
            rating = float(rating)

        cur.execute("INSERT INTO movies (title, year, runtime_mins, genre, rating) VALUES (?, ?, ?, ?, ?)", (title, year, runtime, genre, rating))
        conn.commit()

    conn.close()


#calling functions
music()
movies()
tv_shows()
