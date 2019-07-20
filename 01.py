import csv
import requests
import json
from datetime import datetime, timedelta
from pprint import pprint
from decouple import config

API_KEY=config('API_KEY')
result = {}


for week in range(50):
    targetDt = (datetime(2019,7,13) - timedelta(weeks=week)).strftime('%Y%m%d')
    url = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={API_KEY}&targetDt={targetDt}').json()
    movies = url.get('boxOfficeResult').get('weeklyBoxOfficeList')

    # 주간/주말 박스오피스 데이터 리스트로 가져오기
    # 딕셔너리에서 영화 대표 코드 추출
    for movie in movies:
        code = movie.get('movieCd')
        if code not in result:
            result[code] = {
                'movieCd' : movie.get('movieCd'),
                'movieNm' : movie.get('movieNm'),
                'audiAcc' : movie.get('audiAcc')
            }

         
# 날짜를 거꾸로 돌아가면서 데이터를 얻기 떄문에 기존에 이미 영화코드가 들어가 있따면 그게 가장 마지막주 데이터이다.    



with open('boxoffice.csv','w', newline='', encoding='utf-8') as f:

    feldnames = ('movieCd','movieNm', 'audiAcc' )
    writer = csv.DictWriter(f, fieldnames=feldnames)
    writer.writeheader()    
    for write_movie in result.values():
        writer.writerow(write_movie)




