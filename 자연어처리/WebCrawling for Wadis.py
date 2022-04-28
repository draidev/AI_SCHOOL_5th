# 와디즈 품절상품의 품절상태가 풀리면 메일을 보낸다.
# https://www.wadiz.kr/web/campaign/detail/122394

import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def sendMail(sender, receiver, msg):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com',465)
    smtp.login(sender, 'oqpagmcfqsajurdg')

    msg = MIMEText(msg)
    msg['Subject'] = '지정한 상품이 풀렸습니다!'

    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


url = 'https://www.wadiz.kr/web/campaign/detail/122394'
response = requests.get(url).content
soup_response = BeautifulSoup(response, 'html.parser')

target = soup_response.find_all('button',{'class','rightinfo-reward-list'})

check_status = 1

while check_status:
    for item in target:
        if '110,000' in item.find('dt').get_text().strip():
            if '울트라' in item.find('p').get_text().strip():
                if len(item.attrs['class']) == 2:
                    sendMail('drtkdldjstm@gmail.com','drtkdldjstm@gmail.com','Available \n https://www.wadiz.kr/web/campaign/detail/122394')
                    check_status = 0
                else:
                    print('{} 상품이 아직 품절상태입니다.'.format(item.find('p').get_text().strip()))
    time.sleep(5)