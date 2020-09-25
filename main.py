from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
import json
import re
from get_all_info import get_experience_education_process, get_bio_process
import os
import shutil
from change_order import change_order_by_order_list
from urllib import parse

def make_dir_result():
  try:
    shutil.rmtree("./result")
    os.mkdir("result")
  except:
    pass

def add_cookie(driver):
  driver.get("https://www.linkedin.com/login/zh?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
  with open('./cookie.txt', 'r') as f:
    list_cookies = json.loads(f.read())
    # print("%%%%%%%%%%%",list_cookies)
    for cookie in list_cookies:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)

def get_user_url_list(src):
  with open(src, 'r') as f:
    output_list = []
    while True:
      i = f.readline().strip()
      if i=='': break
      output_list .append(i)
    return output_list

def get_name_code(url):
  pattern = r'in/.*'
  name_code = re.findall(pattern, url)[0][3:]
  name_code = parse.unquote(parse.unquote(name_code))
  return name_code

def craw_data_from_user_url(driver, user_url_list):
  for i in range(len(user_url_list)):
    url = user_url_list[i]
    name_code = get_name_code(url)
    driver.get(url)
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    code_list = soup.find_all('code')
    max_index = 0
    max_length = 0
    for j in range(len(code_list)):
      # print(j, len(str(code_list[j])))
      if len(str(code_list[j])) > max_length:
        max_index = j
        max_length = len(str(code_list[j]))
    # print(max_index)
    main_info = str(code_list[max_index])
    highest_schoolName, present_companyName = get_experience_education_process(main_info, name_code)
    get_bio_process(name_code, highest_schoolName, present_companyName, main_info)

if __name__ == '__main__':
  """
  1.先執行login.py把自己的cookie.txt儲存
  2.建立result資料夾
  3.python3 main.py URL_PATH
  URL_PATHE的文件形式長的如user_url.txt這樣
  4.輸出結果在result資料夾裡，可以選擇輸出順序
  """
  make_dir_result()
  driver_path = "./chromedriver"
  driver = webdriver.Chrome(driver_path)
  add_cookie(driver)
  src = sys.argv[1]
  user_url_list = get_user_url_list(src)
  craw_data_from_user_url(driver, user_url_list)
  driver.close()
  change_order_by_order_list(["bio", "exp", "edu"])




