import csv
import requests
import json
from pprint import pprint
from decouple import config

API_KEY=config('API_KEY')
result = {}
movie_result = {}
name_list=[]

with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    movie_result = list(reader)

for name in movie_result:
    name_list.append(name[8])
del name_list[0]


for name in name_list:
    url = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={API_KEY}&peopleNm={name}').json()
    people_info = url.get('peopleListResult').get('peopleList')[0]
    
    result[name] = dict(
        peopleCd = people_info.get('peopleCd'),
        peopleNm = people_info.get('peopleNm'),
        repRoleNm = people_info.get('repRoleNm'),
        filmos = people_info.get('filmoNames')
    )    

with open('director.csv','w', newline='', encoding='utf-8') as f:
    feldnames = ('peopleCd','peopleNm','repRoleNm','filmos')
    writer = csv.DictWriter(f, fieldnames=feldnames)
    writer.writeheader()    
    for result in result.values():
        writer.writerow(result)
