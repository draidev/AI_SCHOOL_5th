from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore") 

df = pd.read_excel('result_220329_0101.xlsx')
article = df['Article'][0]

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
# hl=ko : Korean & tl=en : English
translator_url = 'https://translate.google.co.kr/?sl=auto&tl=en&op=translate&hl=ko'
driver.get(translator_url)

driver.maximize_window()

origin_xpath = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea'
driver.find_element_by_xpath(origin_xpath).clear()
driver.find_element_by_xpath(origin_xpath).send_keys(article)
time.sleep(3)

translation_xpath = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[6]/div/div[1]/span[1]/span/span'
translated_texts = driver.find_element_by_xpath(translation_xpath).text

print('기사글 [ {} ]의 번역이 끝났습니다.'.format(df['Title'][0]))
print(translated_texts) 

driver.close()
driver.quit()

