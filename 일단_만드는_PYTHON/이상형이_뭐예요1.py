""" for문에 딕셔너리 사용하기 """
total_dictionary = {}

while True:
    question = input("질문을 입력해주세요 : ")
    if question == 'q':
        break
    else:
        total_dictionary[question] = ""  #key가 question이고 value가 공백값인 딕셔너리 생성

for i in total_dictionary: #i는 딕셔너리의 키값을 받는다.
    print(i)
    answer = input("답변을 입력해주세요 : ")
    total_dictionary[i] = answer
print(total_dictionary)