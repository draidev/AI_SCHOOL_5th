import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

#-------------------------사용자 함수--------------------------------

""" callAPI(서비스키, 페이지 번호, 한 페이지 결과 수, 측정년월) """
def callAPI(service_key,pageNo,numOfRows,testYm):
    base_url = 'http://www.kspo.or.kr/openapi/service/nfaTestInfoService/getNfaTestRsltList'
    
    url = base_url + '?' + 'serviceKey=' + service_key + '&pageNo=' + pageNo +\
    '&numOfRows=' + numOfRows + '&testYm=' + testYm
    
    return url


""" API로 불러온 xml데이터를 DataFrame으로 변환 """
def xml_to_df(url):
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml-xml')

    item_list = []
    item_dict = {}
    index_list = ['0'+str(x) for x in range(1,10)]
    index_list += [str(x) for x in range(10,42)]
    index_list
    items = soup.find_all('item')
    

    item_index = 1
    while item_index < len(items[0]):
        for item in items:
            try:
                if item_index<10:
                    item_list.append(item.find('itemF00{}'.format(item_index)).get_text())
                else:
                    item_list.append(item.find('itemF0{}'.format(item_index)).get_text())
            except:
                if item_index<10:
                    item_list.append('-')
                else:
                    item_list.append('-')

        if item_index<10:
            item_dict['itemF00{}'.format(item_index)] = item_list
        else:
            item_dict['itemF0{}'.format(item_index)] = item_list

        item_list = []
        item_index +=1


    del_list = ['itemF001','itemF002','itemF003','itemF004','itemF005','itemF006','itemF007','itemF008','itemF011','itemF018','itemF028','itemF029','itemF038','itemF039','itemF042','itemF043','itemF044']

    df = pd.DataFrame(item_dict)
    for i in del_list:
        del df[i]
        
    return df

#-------------------------------------------------------------------

service_key = 'hDaSIy4ntwfjGKQRK49VW8xYuR5Wi8HUCCr2pnL2wrGjq675JjRPOxb6e%2F9Xtg7N94DRG37oQr30uZY1JS6b3g%3D%3D'

# response = requests.get(url)
# print(response)
# response = requests.get(url).content
# soup = BeautifulSoup(response, 'lxml-xml')
# print(soup)

testYm = []
for i in range(2018, 2022, 1):
    for j in range(1, 13):
        if j < 10:
            testYm.append(str(i) + '0' + str(j))
        else:
            testYm.append(str(i) + str(j)) 
print(testYm)     

""" 코로나 이전 데이터 불러와서 병합 후 csv파일로 만들기 """
before_total_count = []
for yrmonth in testYm[:24]:
    url = callAPI(service_key,'1','1',yrmonth)  # totalCount 구하기용
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml-xml')
    total_count = soup.find('totalCount').get_text()
    before_total_count.append(total_count)
    print(yrmonth,"완료")

befor_df = pd.DataFrame()
for i, yrmonth in enumerate(testYm[:24]):
    url = callAPI(service_key,'1',before_total_count[i],yrmonth)
    print(url)
    before_df = pd.concat([befor_df, xml_to_df(url)])

before_df.to_csv('before_corona.csv')


""" 코로나 이후 데이터 불러와서 병합 후 csv파일로 만들기 """
after_total_count = []
for yrmonth in testYm[24:]:
    url = callAPI(service_key,'1','1',yrmonth)  # totalCount 구하기용
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'lxml-xml')
    total_count = soup.find('totalCount').get_text()
    before_total_count.append(total_count)
    print(yrmonth,"완료")

after_df = pd.DataFrame()
for i, yrmonth in enumerate(testYm[:24]):
    url = callAPI(service_key,'1',after_total_count[i],yrmonth)
    print(url)
    after_df = pd.concat([after_df, xml_to_df(url)])

    after_df.to_csv('after_corona.csv')