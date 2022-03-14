import random
import time

lunch = ["된장찌개","피자","제육볶음","짜장면"]

while True:
    print(lunch)
    item = input("음식을 추가 해주세요 : ")
    if item == 'q':
        break
    else:
        lunch.append(item)
print(lunch)

set_lunch = set(lunch)
while True: 
    item = input("음식을 삭제 해주세요 : ")
    if item == 'q':
        break
    else:
        set_lunch = set_lunch - set(list(item))
print(set_lunch,"중에서 선택합니다.")

for i in range(5,0,-1):
    print(i)
    time.sleep(1)

#random.choice는 리스트 자료형에 대해서만 작동한다.
print(random.choice(list(set_lunch)))