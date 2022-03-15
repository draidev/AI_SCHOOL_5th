total_list = []

while True:
    question = input("질문을 입력해주세요 : ")
    if question == 'q':
        break
    else:
        total_list.append({"질문" : question, "답변" : ""})

for i in total_list: #i는 딕셔너리의 키값을 받는다.
    print(i["질문"])
    answer = input("답변을 입력해주세요 : ")
    print(i)
    i["답변"] = answer  #리스트의 인덱스[i]에 해당되는 딕셔너리의 "답변"key에 해당하는 부분에 value를 대입

print(total_list)