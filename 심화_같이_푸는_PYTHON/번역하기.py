from googletrans import Translator

translator = Translator() # 번역기 생성

sentence = input("번역을 원하는 문장을 입력해주세요 : ")
destination = input("어떤 언어로 번역을 원하시나요? : ")

result = translator.translate(sentence,destination)  # 번역기로 번역한 언어를 result에 저장
detected = translator.detect(sentence)  # 번역할 언어를 감지


print("==========출 력 결 과==========")
print(detected.lang,":",sentence)
print(result.dest,":",result.text)
print("=============================")