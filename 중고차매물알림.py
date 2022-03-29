cage = ['Cat', 'Dog', 'Tiger']

file = open('cage.txt', 'r', encoding='utf-8')  # 읽기 모드
cage = file.readlines()  #  여러줄 한번에 읽어서 리스트에 담기

for c in cage:
    print(c.strip()) # Cat

file.close() 