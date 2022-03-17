import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'User_Agent'}
url = "https://datalab.naver.com/"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.findAll('span','item_title'))


naver_datalab = open("naver_datalab.html","w")
naver_datalab.write(response.text)
naver_datalab.close()

print(response.text)

# results = soup.findAll('li','air_item')

# search_dust_file  = open("dustresult.txt","a")

# print(datetime.today().strftime("%Y년 %m월 %d일의 미세먼지 \n"))

# for result in results:
#     search_dust_file.write(result.get_text()+"\n")
#     print(result.get_text(),"\n")


# print(soup.title)  #soup의 title태그만 가져온다
# print(soup.title.string) 
# print(soup.span)  # 가장 앞에있는 span태그만 가져온다
# print(soup.findAll('span'))  # 모든 span태그를 가져온다


#print(response.url)

#print(response.content)

#print(response.encoding)

#print(response.headers)

#print(response.json)

#print(response.links)

#print(response.ok)

#print(response.status_code)