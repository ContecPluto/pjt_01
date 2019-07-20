# 1.프로젝트 설명

 Python을 사용하여 영화 진흥위원회 API로부터 요청을 보내 답을 받아 영화순위, 영화, 영화인에 대한 정보를 boxoffice.csv, movie.csv, director.csv에 저장하는 프로젝트입니다.

## 2. 01.py

### 	2.1 프로젝트 설명

2019-07-13의 날짜를 기준으로 지난 50주간 데이터 중 주간 박스오피스 TOP10데이터를 수집하는 프로젝트입니다. `영화대표코드`, `영화명`, `누적 관객수` 3가지를 포함하고있습니다.

한국/외국의 영화를 모두 포함했으며 모든 상영지역을 포함하였습니다.



### 	2.2 원리

먼저 영화에대한 정보를 영화진흥위원회 오픈API에서 requets를 이용하여 가져왔습니다.

```python
url = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={API_KEY}&movieCd={targetDt}').json()
```



가져온 정보는 딕셔너리 형태로 url에 저장되었으며 그 중에서 필요한 정보인  `영화대표코드(moviCd)` `영화명(MovieNm)` `누적 관객수(audiAcc)` 의 정보중 중복된는 값은 가장 최신의 값을 유지하며 딕셔너리에 저장하여 후에 출력하였습니다.



### 	2.3 시행착오

처음에는 필요한  `영화대표코드(moviCd)` `영화명(MovieNm)` `누적 관객수(audiAcc)` 의 값을 추출하고 이를 딕셔너에 추가하고자 하였습니다. range(5,-1,-1)과 같은 코드를 이용하여 가장 낮은 날짜부터 시작해 최신의 날짜를 추가 시키고 이는 딕셔너리의 중복값처리에 맞기고자했습니다. 하지만 딕셔너리 제작에 난항을 겪어 다른 방법을 사용하고자했습니다.



 두번째는 csv에 모든 값을 저장하고 이후 중복된 값을 지우고자 했습니다. csv에서  `영화대표코드(moviCd)` `영화명(MovieNm)` `누적 관객수(audiAcc)` 만 추출하여 출력하는대에는 성공했으나 중복처리에 어려움을 겪었습니다.



마지막으로 처음으로 돌아가 다시 딕셔너리를 제작하였습니다. range를 기준날짜인 2019-07-13부터 50주까지 흐르게 하였습니다. 두개를 비교해 빨리 들어간것이 최근의 것이라는 판단을 이용해 프로젝트에 성공하였습니다.



## 3. 02.py

### 	3.1 프로젝트 설명

수집한 영화 대표코드를 활용하여 상세 정보를 수집합니다.  `영화 대표코드` , `영화명(국문)` , `영화명(영문)` ,` 영화명(원문)` ,` 관람등급` , `개봉연도` , `상영시간` , `장르` , `감독명`의 영화의 상세정보를 movie.csv에 저장합니다.



### 	3.2 원리

 기본적인 원리는 `01.py`와 다르지 않습니다. 하지만 url에 사용되는 `movieCd`가  `01.py`에서 출력된 결과물을 사용합니다. 이후 제공되는 딕셔너리에서 원하는 값을 가져와 저장하여 모두 저장된 값을 movie.csv에 저장합니다.



### 	3.3 시행착오

watchGradeNm: 관람등급

genreNm : 장르명

directors,peopleNm : 감독명

 위의 3가지요소가 딕셔너리 -> 리스트 -> 딕셔너리의 순서로 출력이 되는것을 확인하였습니다. 이에 

```python
dict(watchGradeNm = movies.get('audits')[0].get('watchGradeNm')
```

의 코드를 사용하여 0번째의 리스트를 선택하여 필요한 값을 추출하는대 성공하였습니다. 하지만 반복문을 통해 여러 영화들의 정보를 얻으며 `관람등급`,  `장르명`,  `감독명` 의 정보가 없는 영화가 있엇습니다. 이는 오류로 출력되어 프로젝트의 실행을 막았습니다.



```python
watchGradeNm=movies.get('audits')[0].get('watchGradeNm') if movies.get('audits') else ''
```

리스트가 없는경우 그 값은 Fasle의 값을 출력함을 확인하였습니다. 이에 if문을 이용하여 값이 없으면 공백을 출력하도록 설정하였습니다.



```python
boxoffice_resulte = {}
movieCd=[]
with open('boxoffice.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    boxoffice_resulte = list(reader)

for code in boxoffice_resulte:
    movieCd.append(code[0])
del movieCd[0]
```

 code를 따로 검색하지않고 01.py의 결과를 가져오고자 햇습니다. boxoffice_resulte = list(reader)를 이용해 boxoffice.csv의 결과값을 리스트로서 받아 반복문을 이용하여 csv에 있던 movieCd의 데이터를 모두추출하는대 성공하였습니다.



## 4. 03.py

### 	4.1 프로젝트 설명

영화인 정보에 관한 프로젝트입니다. `02.py`의  결과를 바탕으로 감독정보를 활용하여 상세정보를 수집합니다. `영화인 코드` , `영화인명 `, `분야` , `필모리스트`가 director.csv에 저장됩니다.



## 	4.2 원리

` 02.py`의 `movieCdf`를  가져온 방식으로 movie.csv에서  감독명을 가져옵니다.   

`01.py` 의 방식으로 영화진흥위원회 오픈API에서 감독명으로 검색을 하여 딕셔너리로 정보를 받습니다.

이후 director.csv에 저장합니다.

## 	4.3 시행착오

`01.py` 와 `02.py`를 제작하며 쌓인 방법을 통해 큰 시행착오없이 제작이 가능했습니다.