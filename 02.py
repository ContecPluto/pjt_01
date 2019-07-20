import csv
import requests
import json
from pprint import pprint
from decouple import config

boxoffice_result = {}
code_list=[]
API_KEY=config('API_KEY')
result = {}

with open('boxoffice.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    boxoffice_result = list(reader)

for code in boxoffice_result:
    code_list.append(code[0])
del code_list[0]



for movie_list in code_list:
    url = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={API_KEY}&movieCd={movie_list}').json()
    movies = url.get('movieInfoResult').get('movieInfo')

    result[movie_list] = dict(
        movieCd = movies.get('movieCd'),
        movieNm = movies.get('movieNm'),
        movieNmEn = movies.get('movieNmEn'),
        movieNmOg = movies.get('movieNmOg'),
        openDt = movies.get('openDt'),
        showTm = movies.get('showTm'),
        watchGradeNm = movies.get('audits')[0].get('watchGradeNm') if bool(movies.get('audits'))==True else '',
        genreNm = movies.get('genres')[0].get('genreNm') if bool(movies.get('genres'))==True else '',
        peopleNm = movies.get('directors')[0].get('peopleNm') if bool(movies.get('directors'))==True else ''        
    )
        
with open('movie.csv','w', newline='', encoding='utf-8') as f:
    feldnames = ('movieCd','movieNm','movieNmEn','movieNmOg','watchGradeNm','openDt','showTm','genreNm','peopleNm')
    writer = csv.DictWriter(f, fieldnames=feldnames)
    writer.writeheader()    
    for final in result.values():
        writer.writerow(final)
