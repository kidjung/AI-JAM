from selenium import webdriver
import time


fname = "test.csv"
f = open(fname, 'w')
f.write('number, name, category, won_pledged, won_pledged/goal(%), goal_won\n')

driver = webdriver.Chrome('./chromedriver')

driver.get("https://www.wadiz.kr/web/wreward/category/287?keyword=&endYn=Y&order=recommend")
time.sleep(1)

container = driver.find_elements_by_css_selector("div.ProjectCardList_item__1owJa")

number = 1

for item in container:

# 아이템 이름, 아이템 카테고리, 아이템 달성금액, 목표치 대비 달성금액(%)
    item_name = item.find_element_by_css_selector("p.CommonCard_title__1oKJY strong").text
    item_category = item.find_element_by_css_selector("span.RewardProjectCard_category__2muXk").text
    item_pledged = item.find_element_by_css_selector("span.RewardProjectCard_amount__2AyJF").text
    item_percent = item.find_element_by_css_selector("span.RewardProjectCard_percent__3TW4_").text
    item_name = item_name.replace(',', '')
    item_category = item_category.replace(',', '')
    item_pledged = item_pledged.replace(',', '')
    item_pledged = item_pledged.replace('원', '')
    item_percent = item_percent.replace('%', '')
    item_goal_won = int(item_pledged)/int(item_percent)*100
    item_goal_won = int(item_goal_won)
    print(item_name, item_category, item_pledged, item_percent)
    f.write(str(number) + ',' + item_name + ',' + item_category + ',' + item_pledged + ',' + item_percent +
            ',' + str(item_goal_won) + '\n')
    number += 1

f.close()