from selenium import webdriver

driver = webdriver.Chrome(executable_path="path/to/chromedriver")
url = 'https://cls4.edunet.net/cyber/cm/mcom/pmco000b00.do'
driver.get(url)