#Team name: JAJ
#Partners: Amelia Learner, Jackson Gelbard, and Jackson Gertner

#API DATABASE FILE

import requests
import json
import sqlite3
import os

url = "http://www.omdbapi.com/?apikey=99b5ee6f&"
response = requests.get(url)