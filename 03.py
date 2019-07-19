import csv
import requests
import json
from datetime import datetime, timedelta
from pprint import pprint
from decouple import config

API_KEY=config('API_KEY')
result = {}
peopleCd={
    '김종현' :'20164556'
}

for name,code in peopleCd.items():
    url = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?key={API_KEY}&peopleCd={code}').json()
    people_info = url.get('peopleInfoResult').get('peopleInfo')
    pprint(url)
    
    result[code] = dict(
        peopleCd = code,
        peopleNm = name,
        repRoleNm = people_info.get('repRoleNm'),
        filmos = people_info.get('filmos')[0].get('movieNm')
    )    
pprint(result)

with open('director.csv','w', newline='', encoding='utf-8') as f:
    feldnames = ('peopleCd','peopleNm','repRoleNm','filmos')
    writer = csv.DictWriter(f, fieldnames=feldnames)
    writer.writeheader()    
    for result in result.values():
        writer.writerow(result)
