import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

headers = {'User-Agent'}
url = "https://sports.news.naver.com/wfootball/record/index?category=epl&year=2021&tab=team"
response = requests.get(url)
header = response.headers
print(header)
html_text = response.text


soup = BeautifulSoup(html_text, 'html.parser')
result = soup.findAll('script',type='text/javascript')
ranking = soup.select('')