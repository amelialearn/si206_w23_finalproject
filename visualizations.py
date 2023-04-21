#Team name: JAJ
#Partners: Amelia Learner, Jackson Gelbard, and Jackson Gertner

#VISUALIZATIONS

import json
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np 

def avg_length():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "TOP100.db")
    cur = conn.cursor()

    #average length over a certain period of time
    #cur.execute("SELECT songs.runtime, movies.runtime, tv_shows.runtime, songs.year, movies.year, tv_shows.year FROM movies INNER JOIN tv_shows ON restaurants.building_id = buildings.id INNER JOIN categories ON restaurants.category_id = categories.id")
    #rows = cur.fetchall()
    pass

def avg_imdb():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "TOP100.db")
    cur = conn.cursor()

    #average imdb rating for movies vs tv shows for three decades (1990s, 2000s, 2010s)
    cur.execute("SELECT movies.rating, show_info.imdb_rating, movies.year, tv_shows.year FROM show_info INNER JOIN movies ON show_info.key_ID = movies.id INNER JOIN tv_shows ON show_info.key_ID = tv_shows.key_ID")
    rows = cur.fetchall() #movie rating, show rating, movie year, show year
    
    mcount1990 = 0
    mtotal1990 = 0
    mcount2000 = 0
    mtotal2000 = 0
    mcount2010 = 0
    mtotal2010 = 0

    tcount1990 = 0
    ttotal1990 = 0
    tcount2000 = 0
    ttotal2000 = 0
    tcount2010 = 0
    ttotal2010 = 0
    for item in rows:
        if "199" in str(item[2]):
            mcount1990 += 1
            mtotal1990 += item[0]
        elif "200" in str(item[2]):
            mcount2000 += 1
            mtotal2000 += item[0]
        elif "201" in str(item[2]):
            mcount2010 += 1
            mtotal2010 += item[0]
        elif "199" in str(item[3]):
            tcount1990 += 1
            ttotal1990 += float(item[1])
        elif "200" in str(item[3]):
            tcount2000 += 1
            ttotal2000 += float(item[1])
        elif "201" in str(item[3]):
            tcount2010 += 1
            ttotal2010 += float(item[1])
    mavg1990  = mtotal1990/mcount1990
    mavg2000  = mtotal2000/mcount2000
    mavg2010  = mtotal2010/mcount2010

    tavg1990  = ttotal1990/tcount1990
    tavg2000  = ttotal2000/tcount2000
    tavg2010  = ttotal2010/tcount2010
    
    d = {"1990s": {"avg movie rating": mavg1990, "avg tv show rating": tavg1990}, "2000s": {"avg movie rating": mavg2000, "avg tv show rating": tavg2000}, "2010s": {"avg movie rating": mavg2010, "avg tv show rating": tavg2010}}
    
    #write to json
    file = open("avg_imdb_rating.json", "w")
    dj = json.dumps(d)
    file.write(dj)
    file.close()

    #plot
    x = list(d.keys())
    m_dict = list(d.values())
    m_counts = []
    t_counts = []
    for md in m_dict:
        m_counts.append(list(md.values())[0])
    t_dict = list(d.values())
    for td in t_dict:
        t_counts.append(list(td.values())[1])

    x_axis = np.arange(len(x))
    plt.bar(x_axis - 0.2, m_counts, 0.4, label = 'Average Movie Rating')
    plt.bar(x_axis + 0.2, t_counts, 0.4, label = 'Average TV Show Rating')

    plt.bar(x, x_axis)
    plt.xlabel('Decades')
    plt.ylabel('Average IMDb Rating')
    plt.title('Average IMDb Rating per Decade')
    plt.legend()
    plt.show()

    conn.close()

#avg_imdb()

def runtime_rate():       
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "TOP100.db")
    cur = conn.cursor()

    #comparing imdb rating to runtime for movies and tv shows
    #movie runtime vs imdb rating
    cur.execute("SELECT movies.rating, movies.runtime_mins, show_info.imdb_rating, tv_shows.runtime FROM show_info INNER JOIN movies ON show_info.key_ID = movies.id INNER JOIN tv_shows ON show_info.key_ID = tv_shows.key_ID")
    rows = cur.fetchall() #movie rating, movies runtime, tv rating, tv runtime)
    
    mcount93 = 0
    mtotal93 = 0
    mcount83 = 0
    mtotal83 = 0
    mcount73 = 0
    mtotal73 = 0

    tcount93 = 0
    ttotal93 = 0
    tcount83 = 0
    ttotal83 = 0
    tcount73 = 0
    ttotal73 = 0

    for item in rows:
        if item[0] == 9.3:
            mcount93 += 1
            mtotal93 += item[1]
            tcount93 += 1
            ttotal93 += int(item[3])
        elif item[0] == 8.3:
            mcount83 += 1
            mtotal83 += item[1]
            tcount83 += 1
            ttotal83 += int(item[3])
        elif item[0] == 7.3:
            mcount73 += 1
            mtotal73 += item[1]
            tcount73 += 1
            ttotal73 += int(item[3])
    
    mavg93 = mtotal93/mcount93
    mavg83 = mtotal83/mcount83
    mavg73 = mtotal73/mcount73

    tavg93 = ttotal93/tcount93
    tavg83 = ttotal83/tcount83
    tavg73 = ttotal73/tcount73

    d = {9.3: [mavg93, tavg93], 8.3: [mavg83, tavg83], 7.3: [mavg73, tavg73]}
    
    x_axis = list(d.keys())
    counts = list(d.values())
    m_counts = []
    t_counts = []
    for thing in counts:
        m_counts.append(thing[0])
        t_counts.append(thing[1])

    #x_axis = np.arange(len(movie_run))
    plt.plot(x_axis, m_counts, label = "Movies")
    plt.plot(x_axis, t_counts, label = "TV Shows")

    plt.xlabel('IMDb Rating')
    plt.ylabel('Runtime (mins)')
    plt.title('Runtime vs IMDb Rating')
    plt.legend()
    plt.show()

    conn.close()

runtime_rate()

def rate_runtime():       
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "TOP100.db")
    cur = conn.cursor()

    #comparing imdb rating to runtime for movies and tv shows
    #movie runtime vs imdb rating
    cur.execute("SELECT rating, runtime_mins FROM movies")
    m_rows = cur.fetchall() #movie rating, runtime
    
    movie_rate = []
    movie_run = []
    for tup in m_rows:
        movie_rate.append(tup[0])
        movie_run.append(tup[1])
        
    mcount0s = 0
    mtotal0s = 0
    mcount20s = 0
    mtotal20s = 0
    mcount40s = 0
    mtotal40s = 0
    mcount60s = 0
    mtotal60s = 0

    for item in movie_run:
        if len(item) > 1 and item[0] == 2 and (item[0] == 0 or item[0] == 1):
            mcount0s += 1
            mtotal0s += item
        elif len(item) > 1 and item[0] == 2 and (item[0] == 2 or item[0] == 3):
            mcount20s += 1
            mtotal20s += item
        elif len(item) > 1 and item[0] == 2 and (item[0] == 4 or item[0] == 5):
            mcount40s += 1
            mtotal40s += item
        elif len(item) > 1 and item[0] == 2 and (item[0] == 6 or item[0] == 7):
            mcount60s += 1
            mtotal60s += item
    
    mavg0s = mtotal0s/mcount0s
    mavg20s = mtotal20s/mcount20s
    mavg40s = mtotal40s/mcount40s
    mavg60s = mtotal60s/mcount60s
    
    cur.execute("SELECT show_info.imdb_rating, tv_shows.runtime FROM show_info JOIN tv_shows ON show_info.key_ID = tv_shows.key_ID")
    t_rows = cur.fetchall() #show rating, runtime
    
    tv_rate = []
    tv_run = []
    for tup in t_rows:
        if tup[0] != "" and tup[1] != "N/A":
            tv_rate.append(float(tup[0]))
            tv_run.append(tup[1])
    
    tcount20s = 0
    ttotal20s = 0
    tcount40s = 0
    ttotal40s = 0
    tcount60s = 0
    ttotal60s = 0
    tcount80s = 0
    ttotal80s = 0
    
    for item in tv_run:
        if len(item) == 2 and item[0] == 2 and (item[0] == 2 or item[0] == 3):
            tcount20s += 1
            ttotal20s += item
        elif len(item) == 2 and item[0] == 2 and (item[0] == 4 or item[0] == 5):
            tcount40s += 1
            ttotal40s += item
        elif len(item) == 2 and item[0] == 2 and (item[0] == 6 or item[0] == 7):
            tcount60s += 1
            ttotal60s += item
        elif len(item) == 2 and item[0] == 2 and (item[0] == 8 or item[0] == 9):
            tcount80s += 1
            ttotal80s += item
    
    tavg20s = ttotal20s/tcount20s
    tavg40s = ttotal40s/tcount40s
    tavg60s = ttotal60s/tcount60s
    tavg80s = ttotal80s/tcount80s

    tvd = {"20 to 40 minutes": tavg20s, "40 to 60 minutes": tavg40s, "60 to 80 minutes": tavg60s, "80 to 100 minutes": tavg80s}
    movied = {}

    #x_axis = np.arange(len(movie_run))
    plt.plot(movie_run, movie_rate, label = "Movies")
    plt.plot(tv_run, tv_rate, label = "TV Shows")

    plt.xlabel('Runtime (mins)')
    plt.ylabel('IMDb Rating')
    plt.title('Runtime vs IMDb Rating')
    plt.legend()
    plt.show()

    conn.close()

#rate_runtime()

def imdb_genre():
    #average imdb rating based on genre
    pass

def write_data():
    pass

#songs
#movies
#tv_shows - name and runtime and year
#show_info - imdb rating