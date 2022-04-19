from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time 

query = '강아지사료'
paging_index = 9
paging_size = 40

names_list=[] # 제품이름 저장할 리스트

for pi in range(1,paging_index+1):
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    url = 'https://search.shopping.naver.com/search/all?frm=NVSCPRO&origQuery={0}&pagingIndex={1}&pagingSize={2}&productSet=total&query={0}&sort=rel&timestamp=&viewType=list'.format(query,paging_index,paging_size)
    driver.get(url)

    # 창 최대로 키우기
    driver.maximize_window()
    # 페이지 끝까지 내리기
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    for i in range(1,paging_size+1):
        origin_xpath = '//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{}]/li/div/div[2]/div[1]/a'.format(i)
        name = driver.find_element_by_xpath(origin_xpath)
        print(i, name.text)
        names_list.append(name.text)
        
        # 10개 찾으면 다시 스크롤 최대한 내리기
        if i%10 == 9:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    driver.close()
    driver.quit()

print(names_list)
print(len(names_list))

