import requests
from bs4 import BeautifulSoup 
from datetime import datetime
import time 
import re

import numpy as np
import pandas as pd
from konlpy.tag import Okt
from collections import Counter

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns

from PIL import Image 
from wordcloud import WordCloud, ImageColorGenerator

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

font_name = matplotlib.font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name() # NanumGothic.otf
matplotlib.rc('font', family=font_name)

# 불용어 제거 사용자 함수
def cleanWord(pos_tagged):
    del_list = ['하다', '있다', '되다', '이다', '돼다', '않다', 
            '그렇다', '아니다', '이렇다', '그렇다', '어떻다',
            '으로', '에서', '하고', '보다', '관련', '따르다',
            '오다', '통해', '가다', '기자', '에는', '같다',
            '이라고', '까지'] 
    word_cleaned = []
    for word, tag in pos_tagged:
        if tag not in ["josa", "Eomi", "Punctuation", "Foreign", "Suffix", "Alpha", "Determiner"]:
            if (len(word) != 1) & (word not in del_list):
                word_cleaned.append(word)
    
    return word_cleaned


# apple로고 워드클라우드를 만드는 사용자 함수
def appleWordCloud(word_dic, filename):
    apple_logo = np.array(Image.open('apple1.jpg'))
    image_colors = ImageColorGenerator(apple_logo)

    word_cloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf",
                           width = 2000, height = 1000,
                           mask = apple_logo,
                           background_color = 'white').generate_from_frequencies(word_dic)

    word_cloud = word_cloud.recolor(color_func=image_colors)
    word_cloud.to_file(filename='{}.jpg'.format(filename))
    plt.figure(figsize=(15,15))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


# 연도별로 엑셀파일 불러오기
df_18 = pd.read_excel(r'C:\Users\user\Python_MLDL\Semi_Project_1\news_yearly_excelfile\홈트레이닝news_2018.xlsx')
df_19 = pd.read_excel(r'C:\Users\user\Python_MLDL\Semi_Project_1\news_yearly_excelfile\홈트레이닝news_2019.xlsx')
df_20 = pd.read_excel(r'C:\Users\user\Python_MLDL\Semi_Project_1\news_yearly_excelfile\홈트레이닝news_2020.xlsx')
df_21 = pd.read_excel(r'C:\Users\user\Python_MLDL\Semi_Project_1\news_yearly_excelfile\홈트레이닝news_2021.xlsx')

articles_18 = df_18['Article'].tolist()
articles_19 = df_19['Article'].tolist()
articles_20 = df_20['Article'].tolist()
articles_21 = df_21['Article'].tolist()

# 기사별 본문을 하나로 합쳐준다
articles_18 = ' '.join(articles_18)
articles_19 = ' '.join(articles_19)
articles_20 = ' '.join(articles_20)
articles_21 = ' '.join(articles_21)

tokenizer = Okt()
# 토큰화, 품사태깅
pos_tagged_18 = tokenizer.pos(articles_18, norm=True, stem=True)
pos_tagged_19 = tokenizer.pos(articles_19, norm=True, stem=True)
pos_tagged_20 = tokenizer.pos(articles_20, norm=True, stem=True)
pos_tagged_21 = tokenizer.pos(articles_21, norm=True, stem=True)

# 불용어를 제거한 텍스트를 저장할 리스트
word_cleaned_18 = []
word_cleaned_19 = []
word_cleaned_20 = []
word_cleaned_21 = []

# 불용어 제거
word_cleaned_18 = cleanWord(pos_tagged_18)
word_cleaned_19 = cleanWord(pos_tagged_19)
word_cleaned_20 = cleanWord(pos_tagged_20)
word_cleaned_21 = cleanWord(pos_tagged_21)

# 단어와 단어출현횟수를 key-value쌍으로 저장할 딕셔너리
word_dic_18 = {}
word_dic_19 = {}
word_dic_20 = {}
word_dic_21 = {}

# 단어별 출현횟수 구하기
word_cnt_18 = Counter(word_cleaned_18)
word_cnt_19 = Counter(word_cleaned_19)
word_cnt_20 = Counter(word_cleaned_20)
word_cnt_21 = Counter(word_cleaned_21)

# 딕셔너리 : key=단어, value=횟수 
word_dic_18 = dict(word_cnt_18)
word_dic_19 = dict(word_cnt_19)
word_dic_20 = dict(word_cnt_20)
word_dic_21 = dict(word_cnt_21)

# 단어 출현횟수를 기준으로 내림차순으로 정렬
sorted_word_18 = sorted(word_dic_18.items(),key=lambda x:x[1],reverse=True)
sorted_word_19 = sorted(word_dic_19.items(),key=lambda x:x[1],reverse=True)
sorted_word_20 = sorted(word_dic_20.items(),key=lambda x:x[1],reverse=True)
sorted_word_21 = sorted(word_dic_21.items(),key=lambda x:x[1],reverse=True)

# 불용어를 제거한 텍스트를 년도별로 합침
data_18 = ' '.join(word_cleaned_18)
data_19 = ' '.join(word_cleaned_19)
data_20 = ' '.join(word_cleaned_20)
data_21 = ' '.join(word_cleaned_21)

corpus = np.array([data_18, data_19, data_20, data_21])
vect = TfidfVectorizer()
corpus = vect.fit_transform(corpus)
# print(corpus)
# print(cosine_similarity(corpus))

# seaborn시각화를 위해 DataFrame객체로 만들어줍니다.
cos_df = pd.DataFrame(cosine_similarity(corpus),index=['2018','2019','2020','2021'],columns=['2018','2019','2020','2021'])
# cos_df

plt.figure(figsize=(10,10))
sns.set(font_scale=1.5) # label 글자 크기 조절
htmap = sns.heatmap(cos_df,annot=True,fmt='f', linewidths=4, cmap='RdYlBu',annot_kws={"size": 15}) #YlGnBu, RdYlBu, PiYG, YlOrRd

""" WordCloud """
# 코로나 이전과 이후로 나눠서 워드클라우드 생성
beforec_word_cleaned = []
afterc_word_cleaned = []
beforec_word_cleaned = word_cleaned_18 + word_cleaned_19
afterc_word_cleaned = word_cleaned_20 + word_cleaned_21

# 단어 출현횟수 카운트
beforec_word_cnt = Counter(beforec_word_cleaned)
afterc_word_cnt = Counter(afterc_word_cleaned)
beforec_word_dic = dict(beforec_word_cnt) 
afterc_word_dic = dict(afterc_word_cnt)

# 단어 출현횟수를 기준으로 내림차순 정렬
sorted_beforec = sorted(beforec_word_dic.items(),key=lambda x:x[1],reverse=True)
sorted_afterc = sorted(afterc_word_dic.items(),key=lambda x:x[1],reverse=True)
# 출현횟수 상위 50개의 단어까지만 슬라이싱
top_sorted_beforec = dict(sorted_beforec[:50])
top_sorted_afterc = dict(sorted_afterc[:50])

appleWordCloud(top_sorted_beforec,'beforec_apple')
appleWordCloud(top_sorted_afterc,'afterc_apple')