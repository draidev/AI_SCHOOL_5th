import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

titles = []
dates = []
articles = []
article_urls = []
press_companies = []

query = '원소주'
url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + query

response = requests.get(url).content
soup_response = BeautifulSoup(response,'html.parser')

# 1) 네이버 뉴스만 추려내기
urls_list = []
for urls in soup_response.find_all('a',{'class','info'}):
    if urls.attrs['href'].startswith('https://news.naver.com/'):
        urls_list.append(urls.attrs['href'])

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
for url in urls_list:
    news = requests.get(url, headers=headers).content
    soup_news = BeautifulSoup(news,'html.parser')

    # 2) 기사 제목
    title = soup_news.find('h3', {'id' : 'articleTitle'}).get_text()
    titles.append(title)
    print('Processing article : {}', format(title))

    # 3) 기사 날짜
    date = soup_news.find('span', {'class' : 't11'}).get_text()
    dates.append(date)

    # 4) 기사 본문
    article_content = soup_news.find('div', {'id' : 'articleBodyContents'}).get_text()
    article_content = article_content.replace('\n','')
    article_content = article_content.replace('// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}','')
    article_content = article_content.strip()
    articles.append(article_content)

    # 5) 기사 url
    article_urls.append(url)

    # 6) 기사 발행 언론사
    press_company = soup_news.find('address', {'class' : 'address_cp'}).find('a').get_text()
    press_companies.append(press_company)

article_df = pd.DataFrame({'Title':titles, 
                           'Date':dates, 
                           'Article':articles, 
                           'URL':article_urls, 
                           'PressCompany':press_companies})

article_df.to_excel('result_{}.xlsx'.format(datetime.now().strftime('%y%m%d_%H%M')), index=False, encoding='utf-8')
article_df.head()