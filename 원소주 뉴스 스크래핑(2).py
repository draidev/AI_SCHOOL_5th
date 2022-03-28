import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

titles = []
dates = []
articles = []
article_urls = []
press_companies = []
error_urls = []

query = '원소주'

max_page = 5
current_call = 1  # start의 전달인자
last_call = (max_page - 1) * 10 + 1  # 크롤링할 마지막 페이지의 start값

while current_call <= last_call:
    print('\n{}번째 기사글부터 크롤링을 시작합니다.'.format(current_call))
    url = 'https://search.naver.com/search.naver?where=news&query=' + query + '&start=' + str(21)
    response = requests.get(url).content
    soup_news = BeautifulSoup(response, 'html.parser')

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    urls_list = []
    for urls in soup_news.find_all('a',{'class','info'}):
        if urls['href'].startswith('https://news.naver.com'):
            urls_list.append(urls['href'])

    for url in urls_list:
        try:
            news = requests.get(url, headers=headers).content
            soup_news = BeautifulSoup(news,'html.parser')

            # 2) 기사 제목
            title = soup_news.find('h3', {'id' : 'articleTitle'}).get_text()
            print('Processing article : {}', format(title))

            # 3) 기사 날짜
            date = soup_news.find('span', {'class' : 't11'}).get_text()

            # 4) 기사 본문
            article_content = soup_news.find('div', {'id' : 'articleBodyContents'}).get_text()
            article_content = article_content.replace('\n','')
            article_content = article_content.replace('// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}','')
            article_content = article_content.strip()

            # 5) 기사 발행 언론사
            press_company = soup_news.find('address', {'class' : 'address_cp'}).find('a').get_text()
            
            # 6) 위의 2~5를 통해 성공적으로 제목/날짜/본문/언론사 정보가 모두 추출되었을 때에만 리스트에 추가해 길이를 동일하게 유지합니다.        
            titles.append(title)
            dates.append(date)
            articles.append(article_content)
            press_companies.append(press_company)
            article_urls.append(url) # 6) 기사 URL 

        # 오류 발생시 오류메시지 출력 후 url을 리스트에 저장
        except:
            print('*** 다음 링크의 뉴스를 크롤링 중 에러 발생 : {} ***'.format(url))
            error_urls.append(url)
    
    time.sleep(5)
    current_call += 10  # 다음 페이지로 넘어간다

article_df = pd.DataFrame({'Title' : titles,
              'Date' : dates,
              'Article' : articles,
              'URL' : article_urls,
              'PressCompany' : press_companies})

article_df.to_excel('result_{}.xlsx'.format(datetime.now().strftime('%y%m%d_%H%M')), index=False, encoding='utf-8')
print(article_df.head())