from bs4 import BeautifulSoup 
from urllib.request import urlopen 

word = 'affirmation'

url = 'https://alldic.daum.net/search.do?q=' + word
web = urlopen(url) 
web_page = BeautifulSoup(web, 'html.parser')

print(web_page.find_all('span',{'class':'txt_emph1'}))

