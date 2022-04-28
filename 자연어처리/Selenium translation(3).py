from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import time
import pandas as pd
import warnings
from collections import Counter
from konlpy.tag import Okt
from PIL import Image 
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore") 

df = pd.read_excel('result_220329_0101.xlsx')

# 번역할 기사내용을 하나의 리스트로 만든다
articles = df['Article'].tolist()
articles = ''.join(articles)

tokenizer = Okt()
""" 토큰화, 정규화, 어근화, 품사 태깅"""
raw_pos_tagged = tokenizer.pos(articles, norm=True, stem=True)

""" 불용어 리스트 """
del_list = ['하다', '되다', '돼다', '있다', '않다', '그렇다', '그래서']
word_cleaned = []
# 의미있는 단어만 뽑아낸다
for word in raw_pos_tagged:
    if word[1] not in ['Josa','Eomi','Punctuation','Foreign']:
        if (len(word[0]) != 0) & (word[0] not in del_list):
            word_cleaned.append(word[0])

# 각 단어의 출현 빈도를 구해서 딕셔너리로 만든다
word_count = Counter(word_cleaned)
word_dic = dict(word_count)

# 등장횟수가 20이상인 단어만 번역할 딕셔너리에 추가
translation_target = {}
for key in word_dic:
    if word_dic[key] >= 20:
        translation_target[key] = word_dic[key]


service = Service(executable_path=ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service)

translate_url = 'https://translate.google.co.kr/?sl=auto&tl=en&op=translate&hl=ko'
driver.get(translate_url) 
print(driver.current_url)
time.sleep(3)

translation_result = {}
for key in translation_target:
    origin_xpath = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea'
    driver.find_element_by_xpath(origin_xpath).clear()
    driver.find_element_by_xpath(origin_xpath).send_keys(key)  # 본문 내용 속성에 접근후 행인덱스로 하나씩 접근
    time.sleep(1)

    translation_xpath = '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[6]/div/div[1]/span[1]/span/span'
    translated_texts = driver.find_element_by_xpath(translation_xpath).text
    translation_result[translated_texts] = translation_target[key]

print('번역이 완료 되었습니다.')

driver.close()
driver.quit()

# 엑셀 파일에 번역한 결과 저장
df1 = pd.DataFrame()
df1['word'] = translation_result.keys()
df1['frequency'] = translation_result.values()
df1.to_excel('translation_result.xlsx',index=False,encoding='utf-8')

# WordCloud 만들기
apple_logo = np.array(Image.open('./images//apple1.jpg'))
image_colors = ImageColorGenerator(apple_logo)

word_cloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf",
                       width = 2000, height = 1000,
                       mask = apple_logo,
                       background_color = 'white').generate_from_frequencies(translation_result)

word_cloud = word_cloud.recolor(color_func=image_colors)
word_cloud.to_file(filename='selenium_Apple.jpg')
plt.figure(figsize=(15,15))
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
