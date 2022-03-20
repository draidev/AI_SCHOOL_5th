from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime

driver = webdriver.Chrome(executable_path="C:/Users/user/Downloads/chromedriver_win32/chromedriver.exe")
url = 'https://sports.news.naver.com/wfootball/record/index?category=epl&year=2021&tab=team'
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

teams = soup.select("#wfootballTeamRecordBody > table > tbody > tr")

print(datetime.today().strftime("%Y년 %m월 %d일의 EPL순위\n"))
team_txt_file = open("teamranking.txt","w")

""" 순위를 가져오는데 1위의 태그의 클래스<td class="num best">를 보고 td.num.best(띄어쓰기는 .으로 구분해야한다)로 가져오려고 했다. 그런데 자꾸 1위의 값만 나오길래
2번째 td태그를 보니까 <td class"num "> 인것을 확인했다..!! 결국 1등의 클래스만 num.best로 2가지를 갖고 나머지 팀의 순위의 클래스는 num만 오는 것을 확인하고
td.num을 통해서 접근하니까 모든 팀의 순위가 나왔다. """
for team in teams:
    team_ranking = team.select_one('td.num > div > strong')
    team_name = team.select_one('td.align_l > div > span.name')
    team_point = team.select_one('td.selected > div > span')
    team_txt_file.write("순위 : {}등\n".format(team_ranking.text))
    team_txt_file.write("팀명 : {}\n".format(team_name.text))
    team_txt_file.write("승점 : {}점\n\n".format(team_point.text))
    print("순위 : {}등\n팀명 : {}\n승점 : {}점\n".format(team_ranking.text, team_name.text, team_point.text))

team_txt_file.close()

""" copy selector 순위, 팀명, 승점 """
#wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.selected > div > span
#wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.num > div > strong
#wfootballTeamRecordBody > table > tbody > tr:nth-child(1) > td.selected > div > span