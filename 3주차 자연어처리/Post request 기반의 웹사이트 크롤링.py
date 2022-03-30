import json
import requests
from bs4 import BeautifulSoup

# selectRentalPrice.json  ->  Payload / Form Data
data = {'stdrYyCd': '2021',
        'stdrQuCd': '4',
        'stdrSlctQu': 'sameQu',
        'svcIndutyCdL': 'CS000000',
        'svcIndutyCdM': 'all'}

response = requests.post('https://golmok.seoul.go.kr/region/selectRentalPrice.json',data=data).content

result = json.loads(response)

temp_data = []
for item in result:
    temp_data.append(item['BF3_TOT_FLOOR'])

print(temp_data)