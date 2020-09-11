from selenium import webdriver
import json
def login():
  driver_path = "./chromedriver"
  driver = webdriver.Chrome(driver_path)
  driver.get("https://www.linkedin.com/login/zh?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
  #替換成自己的linkedin帳號密碼
  ACCOUNT = ""
  PASSWORD = ""
  driver.find_element_by_id("username").send_keys(ACCOUNT)
  driver.find_element_by_id("password").send_keys(PASSWORD)
  driver.find_element_by_css_selector("[class='btn__primary--large from__button--floating mercado-button--primary']").click()
  dict_cookies = driver.get_cookies()
  json_cookie=json.dumps(dict_cookies)
  print(json_cookie)
  with open('./cookie.txt','w') as f:
      f.write(json_cookie)
  driver.close()

if __name__ == '__main__':
  login()