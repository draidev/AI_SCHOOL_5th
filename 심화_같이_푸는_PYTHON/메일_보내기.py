import smtplib
from email.message import EmailMessage
import imghdr  # 이미지의 확장자를 추출하는데 사용
import re  # 파이썬의 정규표현식 기능 사용

""" 정규 표현식으로 검사한 후 메일을 보내는 함수 """
def sendEmail(addr):
    """ 정규 표현식 """
    reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,3}$"
    if bool(re.match(reg, addr)):
        smtp.send_message(message)
        print("정상적으로 메일이 발송되었습니다.")
    else:
        print("유효한 이메일 주소가 아닙니다.")


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

message = EmailMessage()
message.set_content("안녕하세요. 메일 보내기 코딩 중입니다.")

""" Header에 들어갈 정보들(Subject, From, To) """
message["Subject"] = "이것은 제목입니다."
message["From"] = "###m@gmail.com"
message["To"] = "###@gmail.com" 


with open("./images/codelion.jpg","rb") as image:
    image_file = image.read()

""" imghdr.what(파일명, 파일 데이터) """
""" 이미지의 확장자를 반환한다 """
image_type = imghdr.what('codelion', image_file)
""" add_attachment(이미지, maintype = 파일 형식, subtype = 파일 확장자) """
""" 텍스트가 아닌 다른 포맷의 내용을 첨부할 때 사용하는 함수이다 """
message.add_attachment(image_file, maintype='image',subtype=image_type)


""" smtplib.SMTP() : 우리가 원하는 서버에 연결하는 함수 """
""" smtplib.SMTP_SSL() : 보안처리를 위해 실제로는 SMTP_SSL()을 사용한다 """
smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
smtp.login('###@gmail.com','######')

sendEmail('###@gmail.com')
smtp.quit()

