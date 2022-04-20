from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time 
import pandas as pd
import numpy as np

# Visualization
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns
from PIL import Image 
from wordcloud import WordCloud, ImageColorGenerator

# Text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


service = Service(executable_path=ChromeDriverManager().install())
# 에러 처리 옵션
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
driver = webdriver.Chrome(service=service, chrome_options=chrome_options)

query = '강아지사료'
paging_index = 250
paging_size = 40

name_list = [] # 제품이름 저장할 리스트
price_list = []
cat_list = []
desc_list = []
link_list = []
review_list = []
buy_list = []
enrollment_list = []
zzim_list = []

for pi in range(1,paging_index+1):
    time.sleep(1)
    print("현재 페이지 :",pi)
    url = 'https://search.shopping.naver.com/search/all?frm=NVSCPRO&origQuery={0}&pagingIndex={1}&pagingSize={2}&productSet=total&query={0}&sort=rel&timestamp=&viewType=list'.format(query,pi,paging_size)
    driver.get(url)

    # 창 최대로 키우기
    driver.maximize_window()
    # 페이지 끝까지 내리기
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    for i in range(1,paging_size+1):
        try:
            name_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[1]/a'
            name = driver.find_element_by_xpath(name_xpath)
            name_list.append(name.text)
        except:
            name_list.append(np.nan)
            
        try:
            link_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[1]/a'
            link = driver.find_element_by_xpath(link_xpath)
            link_list.append(link.get_attribute('href'))
        except:
            link_list.append(np.nan)
            
        price_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[2]/strong/span/span'
        price = driver.find_element_by_xpath(price_xpath)
        price_list.append(price.text)

        try:
            cat_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[3]/span[4]'
            cat = driver.find_element_by_xpath(cat_xpath)
            cat_list.append(cat.text)
        except:
            cat_list.append(np.nan)
            
        try:
            desc_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[4]/div[1]'
            desc = driver.find_element_by_xpath(desc_xpath)
            desc_list.append(desc.text)
        except:
            desc_list.append(np.nan)
            
        try:
            review_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[5]/a[1]/em'
            review = driver.find_element_by_xpath(review_xpath)
            review_list.append(review.text)
        except:
            review_list.append(np.nan)
           
        try:
            buy_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[5]/a[2]/em'
            buy = driver.find_element_by_xpath(buy_xpath)
            buy_list.append(buy.text)
        except:
            buy_list.append(np.nan)
        
        try:
            enrollment_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[5]/span[1]'
            enrollment= driver.find_element_by_xpath(enrollment_xpath)
            enrollment_list.append(enrollment.text)
        except:
            enrollment_list.append(np.nan)
    
        try:
            zzim_xpath = f'//*[@id="__next"]/div/div[2]/div[2]/div[3]/div[1]/ul/div/div[{i}]/li/div/div[2]/div[5]/span[2]/button/span/em'
            zzim = driver.find_element_by_xpath(zzim_xpath)
            zzim_list.append(zzim.text)
        except:
            zzim_list.append(np.nan)

        print(i, name.text)

        # 10개 찾으면 다시 스크롤 최대한 내리기
        if i%10 == 9:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")


driver.close()
driver.quit()

data_df = pd.DataFrame(zip(name_list,link_list,price_list,cat_list,desc_list,review_list,buy_list,enrollment_list,zzim_list),columns=['이름','링크','가격','분류','설명(전체)','리뷰수','구매건수','등록일','찜하기'])
print(data_df)

# 가격 열 전처리 (쓸데없는 단어 제외, 숫자만)
data_df['가격'] = data_df['가격'].apply(lambda x : re.sub(r'[가-힣,]',"",x[:x.find('원')]))

desc_df = pd.DataFrame(columns=['급여대상','중량','주원료','등급','기능','입자크기'])
for i in range(len(data_df['설명(전체)'])):
    
    desc_list = data_df['설명(전체)'][i].split('|')
    
    desc_whole = ' '.join(desc for desc in desc_list)
    
    if '급여대상' not in desc_whole:
        target = ' '
    if '중량' not in desc_whole:
        weight = ' '
    if '주원료' not in desc_whole:
        main_ingredient = ' '
    if '등급' not in desc_whole:
        grade = ' '
    if '기능' not in desc_whole:
        function = ' '
    if '입자크기' not in desc_whole:
        particle_size = ' '
        
    for desc_item in desc_list:
        if '급여대상' in desc_item:
            target = desc_item[desc_item.find(":")+1:]
        elif '중량' in desc_item:
            weight = desc_item[desc_item.find(":")+1:]
        elif '주원료' in desc_item:
            main_ingredient = desc_item[desc_item.find(":")+1:]
        elif '등급' in desc_item:
            grade = desc_item[desc_item.find(":")+1:]
        elif '기능' in desc_item:
            function = desc_item[desc_item.find(":")+1:]
        elif '입자크기' in desc_item:
            particle_size = desc_item[desc_item.find(":")+1:]
            
    new_tuple = {'급여대상':target,'중량':weight,'주원료':main_ingredient,'등급':grade,'기능':function,'입자크기':particle_size}
    desc_df = desc_df.append(new_tuple,ignore_index=True)

data_df = pd.concat([data_df,desc_df],axis=1)
data_df =  data_df.drop('설명(전체)',axis=1)

data_df.to_excel('data_df.xlsx',index=False)