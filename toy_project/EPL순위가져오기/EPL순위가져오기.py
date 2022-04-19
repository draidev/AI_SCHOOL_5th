from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from datetime import datetime

""" chromedriver 설치 """
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
url = 'https://sports.news.naver.com/wfootball/record/index?category=epl&year=2021&tab=team'

driver.get(url)

# 버전이 바뀌면서 chromedriver를 알아서 실행해주는 걸로 변경됨
# driver = webdriver.Chrome(executable_path="C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe")
# url = 'https://sports.news.naver.com/wfootball/record/index?category=epl&year=2021&tab=team'
# driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

teams = soup.select("#wfootballTeamRecordBody > table > tbody > tr")

print(datetime.today().strftime("%Y년 %m월 %d일의 EPL순위\n"))
team_txt_file = open("teamranking.txt","w")

for team in teams:
    team_ranking = team.select_one('td.num > div > strong')
    team_name = team.select_one('td.align_l > div > span.name')
    team_point = team.select_one('td.selected > div > span')
    team_txt_file.write("순위 : {}등\n팀명 : {}\n승점 : {}점\n\n".format(team_ranking.text,team_name.text,team_point.text))
    print("순위 : {}등\n팀명 : {}\n승점 : {}점\n".format(team_ranking.text, team_name.text, team_point.text))

team_txt_file.close()

""" copy selector 순위, 팀명, 승점 """
#wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.selected > div > span
#wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.num > div > strong
#wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.selected > div > span