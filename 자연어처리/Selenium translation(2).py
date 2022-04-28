from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore") 

df = pd.read_excel('result_220329_0101.xlsx')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# hl=ko : Korean & tl=en : English
translator_url = 'https://translate.google.co.kr/?sl=auto&tl=en&op=translate&hl=ko'
driver.get(translator_url)

driver.maximize_window()

eng_translated_texts = []
for row_index, row in df.iterrows():
    origin_xpath = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea'
    driver.find_element_by_xpath(origin_xpath).clear()
    driver.find_element_by_xpath(origin_xpath).send_keys(df['Article'][row_index])  # 본문 내용 속성에 접근후 행인덱스로 하나씩 접근
    time.sleep(3)

    translation_xpath = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[6]/div/div[1]/span[1]/span/span'
    translated_texts = driver.find_element_by_xpath(translation_xpath).text

    print('기사글 [ {} ]의 번역이 끝났습니다.'.format(df['Title'][row_index]))
    print(translated_texts) 
    eng_translated_texts.append(translated_texts)

driver.close()
driver.quit()

df['Translated_article'] = eng_translated_texts  # DataFrame에 새로운 열 추가
df.to_excel('translation_result.xlsx', index=False, encoding='utf-8')

print('엑셀파일 저장이 완료되었습니다.')