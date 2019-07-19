import csv
import requests
import json
from datetime import datetime, timedelta
from pprint import pprint
from decouple import config

API_KEY=config('API_KEY')
result = {}
movieCd={20193013, 20121108, 20124079,20196309,20183867,20184047,20185353,20191601,20185986,20183782,20192151}

for movie_list in movieCd:
    url = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={API_KEY}&movieCd={movie_list}').json()
    movies = url.get('movieInfoResult').get('movieInfo')

    
    result[movie_list] = dict(
        movieCd = movies.get('movieCd'),
        movieNm = movies.get('movieNm'),
        movieNmEn = movies.get('movieNmEn'),
        movieNmOg = movies.get('movieNmOg'),
        openDt = movies.get('openDt'),
        showTm = movies.get('showTm')        
    )
    if movies.get('audits') ==False:
        result[movie_list] = dict(watchGradeNm = movies.get('audits')[0].get('watchGradeNm'))
    if movies.get('genres') ==False:
        result[movie_list] = dict(movies.get('genres')[0].get('genreNm'))
    if movies.get('directors') ==False:
        result[movie_list] = dict(movies.get('directors')[0].get('peopleNm'))

with open('movie.csv','w', newline='', encoding='utf-8') as f:
    feldnames = ('movieCd','movieNm','movieNmEn','movieNmOg','watchGradeNm','openDt','showTm','genreNm','peopleNm')
    writer = csv.DictWriter(f, fieldnames=feldnames)
    writer.writeheader()    
    for final in result.values():
        writer.writerow(final)
