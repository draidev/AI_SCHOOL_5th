import requests
from bs4 import BeautifulSoup

#-------------------------사용자 함수--------------------------------

""" callAPI(서비스키, 페이지 번호, 한 페이지 결과 수, 측정년월) """
def callAPI(service_key,pageNo,numOfRows,testYm):
    base_url = 'http://www.kspo.or.kr/openapi/service/nfaTestInfoService/getNfaTestRsltList'
    
    url = base_url + '?' + 'serviceKey=' + service_key + '&pageNo=' + pageNo +\
    '&numOfRows=' + numOfRows + '&testYm=' + testYm
    
    return url

#-------------------------------------------------------------------

service_key = 'hDaSIy4ntwfjGKQRK49VW8xYuR5Wi8HUCCr2pnL2wrGjq675JjRPOxb6e%2F9Xtg7N94DRG37oQr30uZY1JS6b3g%3D%3D'

url = callAPI(service_key,'1','10','202001')
print(url)

response = requests.get(url)
print(response)

response = requests.get(url).content
soup = BeautifulSoup(response, 'lxml-xml')
print(soup)


