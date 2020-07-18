from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time


fname = "test.csv"
f = open(fname, 'w')
f.write('currency, name, main_category, sub_category, duration, goal_won, start_Q, end_Q, status\n')

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome("./chromedriver", options=options)

# 287 테크, 가전
# 288 패션, 잡화
# 289 푸드
# 290 디자인, 소품
# 296 여행, 레저
# 292 게임, 취미
# 293 출판

page_list = [287, 288, 289, 290, 296, 292, 293]

for page in page_list:
    driver.get("https://www.wadiz.kr/web/wreward/category/" + str(page) + "?keyword=&endYn=Y&order=recent")
    time.sleep(1)
    for i in range(1, 11):
        try:
            container = driver.find_elements_by_css_selector("div.ProjectCardList_item__1owJa")
            item = container[i]
            item.click()
            time.sleep(1)

            html = driver.page_source
            html = BeautifulSoup(html, "html.parser")

            # name
            item_name = html.select_one("div.campaign-title a").text
            item_name = item_name.replace(',', '')
            print(item_name)

            # main_category
            item_category = html.select_one("span.category em").text
            item_category = item_category.replace(',', '')
            print(item_category)

            # 아이템 목표 달성 퍼센트
            item_percentage = html.select_one("p.achievement-rate strong").text
            # print(item_percentage)


            item_goal_duration = html.select_one("#container > div.reward-body-wrap > div > div.wd-ui-info-wrap > "
                                        "div.wd-ui-sub-campaign-info-container > div > div > section > "
                                        "div.wd-ui-campaign-content > div > div:nth-child(5) > div "
                                        "> p:nth-child(1)").text
            # print(item_goal_duration)

            goal_start = item_goal_duration.find('목')
            goal_end = item_goal_duration.find('원')
            item_goal_won = item_goal_duration[goal_start:goal_end]
            item_goal_won = item_goal_won.split(' ')[2]
            item_goal_won = item_goal_won.replace(',', '')
            print(item_goal_won)

            duration_start = item_goal_duration.find('펀')
            duration_end = len(item_goal_duration)
            item_duration = item_goal_duration[duration_start:duration_end]
            item_duration = item_duration.split(' ')[1]
            # print(item_duration)

            item_start = item_duration.split('-')[0]
            item_end = item_duration.split('-')[1]
            print(item_start)
            print(item_end)

            time1 = datetime(int(item_start.split('.')[0]), int(item_start.split('.')[1]), int(item_start.split('.')[2]))
            time2 = datetime(int(item_end.split('.')[0]), int(item_end.split('.')[1]), int(item_end.split('.')[2]))

            # duration
            item_duration = (time2 - time1).days
            print(item_duration, '일')

            if 1 <= int(item_start.split('.')[1]) <= 3:
                item_start_q = "Q1"
            elif 4 <= int(item_start.split('.')[1]) <= 6:
                item_start_q = "Q2"
            elif 7 <= int(item_start.split('.')[1]) <= 9:
                item_start_q = "Q3"
            elif 10 <= int(item_start.split('.')[1]) <= 12:
                item_start_q = "Q4"

            print(item_start_q)

            if 1 <= int(item_start.split('.')[1]) <= 3:
                item_end_q = "Q1"
            elif 4 <= int(item_start.split('.')[1]) <= 6:
                item_end_q = "Q2"
            elif 7 <= int(item_start.split('.')[1]) <= 9:
                item_end_q = "Q3"
            elif 10 <= int(item_start.split('.')[1]) <= 12:
                item_end_q = "Q4"

            print(item_end_q)

            if int(item_percentage) < 100:
                item_status = "failed"
            else:
                item_status = "successful"

            print(item_status)


            print('-' * 50)


            f.write("WON" + ',' + item_name + ',' + item_category + ',' + ' ' + "," + str(item_duration) + ','
                    + str(item_goal_won) + ',' + str(item_start_q) + ',' + str(item_end_q) + ',' + item_status + '\n')

            driver.back()
            time.sleep(1)
        except:
            driver.back()
            time.sleep(1)

f.close()