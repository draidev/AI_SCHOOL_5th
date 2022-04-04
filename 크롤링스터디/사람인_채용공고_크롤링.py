# 신입, 경력무관 조건 추가
# 메일 보내기 추가
# 채용공고 올라오는 시간이 저념일 수도 있음

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from datetime import date
import smtplib
from email.mime.text import MIMEText

titles_list = []
company_names_list = []
deadlines_list = []
recruit_urls_list = []

search = '인공지능'
page = 1
max_page = 5

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
url = 'https://www.saramin.co.kr/zf_user/search/recruit?searchword=' + search + '&recruitPage=' + str(page)

response = requests.get(url,headers=headers).content
soup_response = BeautifulSoup(response, 'html.parser')

""" 오늘의 날짜 형식 변경 """
""" ex) 2022-03-31 -> 22/03/31 """
today = str(date.today())[2:]
today = today.replace('-', '/')
print("today : ",today)


while page <= max_page:
    url = 'https://www.saramin.co.kr/zf_user/search/recruit?searchword=' + search + '&recruitPage=' + str(page)
    response = requests.get(url,headers=headers).content
    soup_response = BeautifulSoup(response, 'html.parser')

    page_content = soup_response.find('div',{'class':'content'}) # 한페이지 채용공고 블록
    job_day = page_content.find_all('span',{'class':'job_day'})  # 채용공고 등록일 or 수정일
    recruit_content = page_content.find_all('h2',{'class':'job_tit'})  # 채용공고 한개의 블록
    company_name = page_content.find_all('div',{'class':'area_corp'})  # 회사명
    deadline = page_content.find_all('span',{'class':'date'})  # 마감일

    for index, day in enumerate(job_day):
        #if '22/03/29' in day.get_text():
        if today in day.get_text():
            titles_list.append(recruit_content[index].get_text().strip())
            recruit_urls_list.append('https://www.saramin.co.kr'+recruit_content[index].find('a').attrs['href'])
            company_names_list.append(company_name[index].find('a').attrs['title'])
            deadlines_list.append(deadline[index].get_text())

    print('{}페이지 크롤링을 완료했습니다.'.format(page))
    
    page += 1
    time.sleep(1)


for i in range(len(titles_list)):
    print('채용공고 : {}\n회사 : {}\n주소 : {}\n\n'.format(titles_list[i],company_names_list[i],recruit_urls_list[i]))