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

avg_imdb()

def rate_runtime():       
    #comparing imdb rating to runtime for movies an tv shows
    pass

def imdb_genre():
    #average imdb rating based on genre
    pass

def write_data():
    pass

#songs
#movies
#tv_shows - name and runtime and year
#show_info - imdb rating