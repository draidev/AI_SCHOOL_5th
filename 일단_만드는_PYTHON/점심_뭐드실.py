total_list = []

while True:
    question = input()
    if question == 'q':
        break
    else:
        total_list.append({"질문" : question, "답변" : ""})

for i in total_list:
    print(i["질문"])
    answer = input()
    i["답변"] = answer

print(total_list)
