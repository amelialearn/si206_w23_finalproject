#Team name: JAJ
#Partners: Amelia Learner, Jackson Gelbard, and Jackson Gertner

#VISUALIZATIONS

import json
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np 


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



def rating_runtime():      
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "TOP100.db")
    cur = conn.cursor()

    #comparing imdb rating to runtime for movies and tv shows
    #movie runtime vs imdb rating
    cur.execute("SELECT rating, runtime_mins FROM movies")
    mrows = cur.fetchall() #movie rating, movies runtime
    movied = {}

    for item in mrows:
        if item[0] not in movied:
            mlist = []
            mlist.append(item[1])
            movied[item[0]] = mlist
        else:
            movied[item[0]].append(item[1])

    final_m = {}
    for key, value in movied.items():
        if len(value) > 1:
            final_m[key] = sum(value)/len(value)
        else:
            final_m[key] = value[0]

    cur.execute("SELECT show_info.imdb_rating, tv_shows.runtime FROM show_info JOIN tv_shows ON show_info.key_ID = tv_shows.key_ID")
    trows = cur.fetchall() #tv rating, tv runtime
    tvd = {}

    for item in trows:
        if item[0] not in tvd and item[0] != "" and item[1] != "N/A":
            tlist = []
            tlist.append(item[1])
            tvd[item[0]] = tlist
        elif item[0] in tvd and item[0] != "" and item[1] != "N/A":
            tvd[item[0]].append(item[1])

    final_t = {}
    for key, value in tvd.items():
        total = 0
        if len(value) > 1:
            for time in value:
                total += int(time)
            final_t[float(key)] = total/len(value)
        else:
            final_t[float(key)] = float(value[0])
    
    sorted_m = dict(sorted(final_m.items(), key=lambda item: item[0]))
    sorted_t = dict(sorted(final_t.items(), key=lambda item: item[0]))
    sorted_t.popitem()
    sorted_t.popitem()

    x_axis = list(sorted_m.keys())
    m_counts = list(sorted_m.values())
    t_counts = list(sorted_t.values())

    #x_axis = np.arange(len(movie_run))
    plt.plot(x_axis, m_counts, label = "Movies")
    plt.plot(x_axis, t_counts, label = "TV Shows")

    plt.xlabel('IMDb Rating')
    plt.ylabel('Runtime (mins)')
    plt.title('Runtime vs IMDb Rating')
    plt.legend()
    plt.show()

    conn.close()

def year_runtime():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "TOP100.db")
    cur = conn.cursor()

    #MOVIE RUNTIME VS YEARS
    cur.execute("SELECT year, runtime_mins FROM movies")
    mrows = cur.fetchall() #movie rating, movies runtime
    movied = {}

    for item in mrows:
        if item[0] not in movied:
            mlist = []
            mlist.append(item[1])
            movied[item[0]] = mlist
        else:
            movied[item[0]].append(item[1])

    final_m = {}
    for key, value in movied.items():
        if len(value) > 1:
            final_m[key] = sum(value)/len(value)
        else:
            final_m[key] = value[0]
    
    #TV_SHOW YEARS VS RUNTIME
    cur.execute("SELECT year, runtime FROM tv_shows")
    trows = cur.fetchall() #tv rating, tv runtime
    tvd = {}

    for item in trows:
        if item[0] not in tvd and item[0] != "" and item[1] != "N/A":
            tlist = []
            tlist.append(item[1])
            tvd[item[0]] = tlist
        elif item[0] in tvd and item[0] != "" and item[1] != "N/A":
            tvd[item[0]].append(item[1])

    final_t = {}
    for key, value in tvd.items():
        total = 0
        if len(value) > 1:
            for time in value:
                total += int(time)
            final_t[int(key)] = total/len(value)
        else:
            final_t[int(key)] = float(value[0])

    
    
    #MUSIC YEARS VS RUNTIME
    cur.execute("SELECT year, runtime FROM songs")
    musrows = cur.fetchall() #movie rating, movies runtime
    musicd = {}

    for item in musrows:
        if item[0] not in musicd:
            mlist = []
            mlist.append(float(item[1]))
            musicd[item[0]] = mlist
        else:
            musicd[item[0]].append(item[1])

    final_mus = {}
    for key, value in musicd.items():
        total = 0         
        if len(value) > 1:
            for time in value:
                total += float(time)
            final_mus[int(key)] = total/len(value)
        else:
            final_mus[int(key)] = value[0]


    sorted_m = dict(sorted(final_m.items(), key=lambda item: item[0]))
    sorted_t = dict(sorted(final_t.items(), key=lambda item: item[0]))
    sorted_mus = dict(sorted(final_mus.items(), key=lambda item: item[0]))

    
    m_counts = list(sorted_m.values())
    t_counts = list(sorted_t.values())
    mus_counts=list(sorted_mus.values())



    #x_axis = np.arange(len(movie_run))

    plt.plot(list(sorted_m.keys()), m_counts, label = "Movies")
    plt.xlabel('Year')
    plt.ylabel('Runtime (mins)')
    plt.title('Movie Runtime Over the Years')
    plt.show()

    plt.plot(list(sorted_t.keys()), t_counts, label = "TV Shows")
    plt.xlabel('Year')
    plt.ylabel('Runtime (mins)')
    plt.title('TV Runtime Over the Years')
    plt.show()

    plt.plot(list(sorted_mus.keys()), mus_counts, label = "Songs")
    plt.xlabel('Year')
    plt.ylabel('Runtime (mins)')
    plt.title('Music Runtime Over the Years')
    plt.show()

    conn.close()
    


    
rating_runtime()
avg_imdb()#GREEN CHUNK?
year_runtime()


#songs
#movies
#tv_shows - name and runtime and year
#show_info - imdb rating