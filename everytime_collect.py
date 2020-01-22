from selenium import webdriver
from bs4 import BeautifulSoup
from collections import defaultdict
import time


FIND_NUM = 50  # 탐색하고자 하는 횟수, 개당 20게 게시물
YOUR_ID = ''  # 에브리타임 아이디
YOUR_PASSWORD = ''  # 에브리타임 비밀번호
BOARD_URL = 'https://everytime.kr/'  # 에브리타임 해당 학교 게시판 주소 ex)https://everytime.kr/393744/p/


def tree():
    return defaultdict(tree)


driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://everytime.kr/login')

# 접속
driver.find_element_by_xpath('//*[@id="container"]/form/p[1]/input').send_keys(YOUR_ID)  # 아이디
driver.find_element_by_xpath('//*[@id="container"]/form/p[2]/input').send_keys(YOUR_PASSWORD)  # 비밀번호
driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()  # 로그인 버튼
time.sleep(2)
driver.find_element_by_xpath(
    '//*[@id="container"]/div[4]/div[1]/div/h3/a').click()  # //*[@id="container"]/div[4]/div[1]/div/h3/a: 자유게시판

everytime_link = list()  # 링크 리스트
fail_link = list()  # 실패 리스트
page_number = 2
content_number = 0

for i in range(FIND_NUM):
    time.sleep(7)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.findAll('article')

    for url in content:
        find_url = url.find('a', attrs={'class', 'article'}).get('href')
        everytime_link.append(find_url)
    time.sleep(2)
    driver.get(BOARD_URL + str(page_number))  # 자유게시판
    page_number = page_number + 1

with open('./everytime_link.txt', 'w') as fileobject:
    for join_link in everytime_link:
        fileobject.write(join_link)
        fileobject.write('\n')

n = open("everytime.txt", "w")
for url in everytime_link:
    try:
        driver.get('https://everytime.kr' + url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h2', attrs={'class', 'large'}).get_text()
        text = soup.find('p', attrs={'class', 'large'}).get_text()
        n.write(title + " " + text + "\n")

        text_time = soup.find('time', attrs={'class', 'large'}).get_text()
        try:
            comment = soup.findAll('article')
            for content in comment:
                n.write(content.find('p').get_text() + "\n")
        except:
            pass

    except Exception as e:
        print(e)
        fail_link.append(url)
        continue

with open('./fail_url.txt', 'w') as fileobject:
    for join_link in fail_link:
        fileobject.write(join_link)
        fileobject.write('\n')
n.close()
driver.close()
