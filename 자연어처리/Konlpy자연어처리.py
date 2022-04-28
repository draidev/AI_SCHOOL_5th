import numpy as np
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
import nltk
import matplotlib
from wordcloud import WordCloud
from PIL import Image # 만약 "No module named 'PIL'" 에러가 발생하면 [ pip install Pillow==5.4.1 ] 로 라이브러리를 설치해줍니다.
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import ImageColorGenerator
from matplotlib import font_manager, rc


# 한글 폰트 위치를 넣어주세요 (위에서 나눔고딕 파일을 해당 경로에 복사붙여넣기 했을 경우 그대로 실행하셔도 무방합니다.)
font_name = matplotlib.font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name() # NanumGothic.otf
matplotlib.rc('font', family=font_name)

df = pd.read_excel('./excelfiles/result_220329_0101.xlsx')

articles = df['Article'].tolist()

articles = ' '.join(articles)
articles = articles[:1000]

tokenizer = Okt()
raw_pos_tagged = tokenizer.pos(articles, norm=True, stem=True) # POS Tagging


del_list = ['를', '이', '은', '는', '있다', '하다', '에'] 

word_cleaned = []
for word in raw_pos_tagged: 
    if word[1] not in ["Josa", "Eomi", "Punctuation", "Foreign"]: # Foreign == ”, “ 와 같이 제외되어야할 항목들
        if (len(word[0]) != 1) & (word[0] not in del_list): # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외, 대신 "안, 못"같은 것까지 같이 지워져서 긍정,부정을 파악해야 되는경우는 제외하지 않는다.
            word_cleaned.append(word[0])
        

result = Counter(word_cleaned)
word_dic = dict(result)

sorted_word_dic = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)

word_counted = nltk.Text(word_cleaned)
plt.figure(figsize=(15,7))
word_counted.plot(50)

word_frequency = nltk.FreqDist(word_cleaned)
df = pd.DataFrame(list(word_frequency.values()), word_frequency.keys())

""" bar그래프 출력 """
# result = df.sort_values([0], ascending = False)
# result = result[:50]
# result.plot(kind='bar', legend=False, figsize=(15,5))
# plt.show()

masking_image = np.array(Image.open(".\images\\apple1.jpg"))

word_cloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf", # font_path="C:/Windows/Fonts/NanumSquareB.ttf"
                       width=2000, height=1000, 
                       mask=masking_image, # masking
                       background_color='white').generate_from_frequencies(word_dic)

image_colors = ImageColorGenerator(masking_image)
word_cloud = word_cloud.recolor(color_func=image_colors)
word_cloud.to_file(filename='Apple.jpg')  # 파일로 저장

plt.figure(figsize=(15,15))
plt.imshow(word_cloud, interpolation='bilinear')
# plt.imshow(word_cloud.recolor(colormap='Blues'), interpolation='bilinear') # Matplotlib colormap 활용 (http://j.mp/32UXOQ6)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()