# linkedin_crawler
input : 一個有linkedin個人網址的文件(範例:user_url.txt)

output : ./result/

1.將login.py中填入linkein帳號密碼，做登入用

2.pip install -r requirements.txt

3.python3 login.py

4.python3 main.py INPUT_FILE_PATH

注意事項:

1.先執行login.py把自己的cookie.txt儲存

2.建立result資料夾

3.python3 main.py URL_PATH

URL_PATHE的文件形式長的如user_url.txt這樣

4.輸出結果在result資料夾裡，可以選擇輸出順序

5.crawl_urls_from_google_by_company_name有用google抓取公司員工url的方法

  如:scrapy crawl linkedin_from_google -a company=台積電 -o output.csv

  不過要注意可能會被ban ip，可以把time delay調大或是用跳ip的方式

6.爬linkedin網站時帳號也可能被ban，不過是隱藏ban，就是無法在前端獲得包含使用使用這資訊的main_info，

我自己遇到的情景是短時間內以不同ip位址登入帳號，帳號可能因此被linkedin隱藏ban，如果沒跳ip，跑我的code是沒有被ban的
