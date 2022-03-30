import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://finance.naver.com'
res = requests.get(url).content
soup = BeautifulSoup(res, 'html.parser')

names = []
prices = []
delta_prices = []
delta_percents = []

items = soup.find('tbody',{'id':'_topItems1'})
item_rows = items.find_all('tr')

for item in item_rows:
    if '상승' in item.find_all('td')[1].get_text():  # 상승한 종목만 리스트에 추가
        names.append(item.find('th').get_text())  # 종목명
        prices.append(item.find_all('td')[0].get_text())  # 현재가격
        delta_prices.append(item.find_all('td')[1].get_text()[3:])  # 변동가격, [3:]으로 '상승' 단어를 빼고 가격만 포함
        delta_percents.append(item.find_all('td')[2].get_text())  # 변동률

# for i, item in enumerate(delta_prices):
#     if '상승' in item:
#         delta_prices[i] = item.replace('상승','').strip()
#     elif '하락' in item:
#         delta_prices[i] = item.replace('하락','').strip()

df = pd.DataFrame({'가격':prices,'가격변동':delta_prices,'퍼센트':delta_percents},index=names)
print(df)

df.to_excel("오늘의 거래상위 상승 TOP종목.xlsx",encoding='utf-8')
