import requests
import json

city = "Seoul"
apikey = "aacd26a3acd45a7b369f073e87b767a2"
lang = "kr"  #날씨 정보를 한국어로 받아오기 위해 api에 추가해준다
units = "metric"  #날씨 단위를 화씨로 받아오기 위해 api에 추가해준다.

api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units={units}"

result = requests.get(api)

data = json.loads(result.text)  # 문자열을 json모듈을 통해 딕셔너리 타입으로 변환

# print(type(result.text))
# print(type(data))

print(data["name"],"의 날씨입니다.")
print("날씨는 ", data["weather"][0]["description"],"입니다.")
print("현재 온도는 ",data["main"]["temp"],"입니다.")
print("하지만 체감 온도는 ",data["main"]["feels_like"],"입니다.")
print("최저 기온은 ",data["main"]["temp_min"],"입니다.")
print("최고 기온은 ",data["main"]["temp_max"],"입니다.")
print("습도는 ",data["main"]["humidity"],"입니다.")
print("기압은 ",data["main"]["pressure"],"입니다.")
print("풍향은 ",data["wind"]["deg"],"입니다.")
print("풍속은 ",data["wind"]["speed"],"입니다.")