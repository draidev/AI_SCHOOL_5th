import requests
from bs4 import BeautifulSoup 

import pandas as pd
from datetime import datetime
import time 
import re


max_page = 3 # 검색할 페이지의 수
current_call = 1  # start의 전달인자
last_call = (max_page - 1) * 10 + 1  # 크롤링할 마지막 페이지의 start값

query = '홈트레이닝'
search_year = ['18','19','20','21']
search_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


for year in search_year:  # 2018 ~ 2021
    # 1년 단위로 크롤링한 데이터를 저장할 리스트
    titles = []
    dates = []
    articles = []
    article_urls = []
    press_companies = []
    for month in search_month:  # 1월 ~ 12월
        while current_call <= last_call:
            print('\n20{}.{} {}번째 기사글부터 크롤링을 시작합니다.'.format(year,month,current_call))
            url = 'https://search.naver.com/search.naver?where=news&query=' + query + \
            '&pd=3&ds='+ '20{}.{}.01'.format(year,month) + '&de=' + '20{}.{}.31'.format(year,month) + '&start=' + str(current_call)
            response = requests.get(url).content
            soup_response = BeautifulSoup(response,'html.parser')

            # 1) 네이버 뉴스만 추려내기
            urls_list = []
            for urls in soup_response.find_all('a',{'class','info'}):
                if urls.attrs['href'].startswith('https://news.naver.com/'):
                    urls_list.append(urls.attrs['href'])

            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
            error_urls=[]  # 에러난 사이트의 url을 담을 리스트
            for url in urls_list:
                try:
                    news = requests.get(url, headers=headers).content
                    soup_news = BeautifulSoup(news,'html.parser')

                    # 2) 기사 제목
                    title = soup_news.find('h3', {'id' : 'articleTitle'}).get_text()
                    print('Processing article : {}'.format(title))

                    # 3) 기사 날짜
                    date = soup_news.find('span', {'class' : 't11'}).get_text()

                    # 4) 기사 본문
                    article_content = soup_news.find('div', {'id' : 'articleBodyContents'}).get_text()
                    article_content = article_content.replace('\n','')
                    article_content = article_content.replace('◆','')
                    article_content = article_content.replace('▲','')
                    article_content = article_content.replace('// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}','')
                    article_content = article_content.strip()
                       # 이메일 이후로 삭제
                    print("\n원본 :",article_content)
                    pattern = re.compile(r'[\w.%+\-]+@[\w/-]+\.') 
                    email_address = pattern.search(article_content)
                    article_content = article_content[:email_address.start()]
                    print("\n이메일 이후 제거:",article_content)
                      # [ ] < > ( ) 로 감싸여 있는 부분 삭제
                    pattern = re.compile(r'[\[<(][\s\w,+\-./:=%]*[\]>)]')
                    article_content = pattern.sub('',article_content)
                    print("\n대괄호 제거후 : ",article_content)
                      # ▶ 기호 뒤에 나오는 내용 삭제 (광고 내용 삭제)
                    tri_loc = article_content.find('▶')
                    if tri_loc > 150:  # 본문 초반에 삼각형기호가 나오는 경우 제외
                        article_content = article_content[:tri_loc]
                        print("\n▶화살표제거후 : ",article_content)

                    # 5) 기사 발행 언론사
                    press_company = soup_news.find('address', {'class' : 'address_cp'}).find('a').get_text()
                        
                    #
                    titles.append(title)
                    dates.append(date)
                    articles.append(article_content)
                    press_companies.append(press_company)
                    article_urls.append(url) # 6) 기사 URL 

                except:
                    print('*** 다음 링크의 뉴스를 크롤링 중 에러 발생 : {} ***'.format(url))
                    error_urls.append(url)

            time.sleep(5)
            current_call += 10  # 다음 페이지로 넘어간다
            
        current_call = 1  # start의 전달인자 초기화 (다시 1페이지부터 크롤링)   
        print('**************************20{}년 {}월 스크래핑 완료**************************'.format(year,month))
    
    # DataFrame으로 만든 후에 엑셀파일로 저장
    article_df = pd.DataFrame({'Title' : titles,
                  'Date' : dates,
                  'Article' : articles,
                  'URL' : article_urls,
                  'PressCompany' : press_companies})

    article_df.to_excel(r'C:\Users\user\Python_MLDL\Semi_Project_1\news_yearly_excelfile\{}news_20{}.xlsx'.format(query,year), index=False, encoding='utf-8')
    print('***********************{}news_20{}_{}.xlsx 파일생성 완료**********************'.format(query,year,month))