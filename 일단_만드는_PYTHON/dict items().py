information = {"고향":"서울", "취미":"영화관람","좋아하는 음식":"스테이크"}
foods = ["된장찌개","피자","제육볶음"]

""" items 함수는 Key와 Value의 쌍을 튜플로 묶은 값을 dict_items 객체로 돌려준다. """
for x,y in information.items():
    print(x,y)

print(information.get("취미"))
information["특기"] = "피아노"
information["사는 곳"] = "서울"
del information["좋아하는 음식"]


print(information)
print(len(information))
information.clear()
print(information)
print(foods[-1])
foods.append("김밥")
foods.remove("된장찌개")
del foods[1]
print(foods)

for i in foods:
    print(i)
