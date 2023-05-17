from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from utils import read_config, get_current_time
from collections import defaultdict
from datetime import datetime
import os
import asyncio

# TARGET_URL = "https://search.naver.com/search.naver?where=news&sort=1&ds=2023.05.17&de=2023.05.17&nspo=nspo=so:dd,p:from20230517to20230517,a:all&query=현대차"
TARGET_URL = "https://search.naver.com/search.naver?where=news&sort=1&ds={start_date_dot}&de={end_date_dot}&nspo=nspo=so:dd,p:from{start_date}}to{end_date},a:all&query={query}&start={page_cnt}"


class Naver:
    def __init__(self):
        self.keywords = read_config().get("keywords")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("no-sandbox")
        options.add_argument("disable-gpu")
        options.add_argument("lang=ko_KR")
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        self.browser = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        self.news = defaultdict(list)

    def __get_news_template(self, a_id, url, title, publisher, published_at):
        t = {
            'a_id': a_id,
            'url': url,
            'title': title,
            'publisher': publisher,
            'published_at': published_at
        }
        return t

    def __wait_for(self, element):
        try:
            wait_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, f"{element}"))
            )
            self.browser.execute_script(
                wait_element,
            )
        except Exception:
            pass

    def get_news_info(self, section, keyword, start_date, end_date):
        # 페이지 단위로 검색을 하면서, 다음이 없을 떄까지 while
        # 즉 기존 get_total_page_cnt 양식 활용해서 로직 짜기

        page_cnt, idx = 1, 1
        while True:
            start_date_dot, end_date_dot = start_date, end_date # TODO. make conversing function
            url = TARGET_URL.format(start_date_dot=start_date_dot, end_date_dot=end_date_dot, start_date=start_date, end_date=end_date, query=query, page_cnt=page_cnt)
            print(url)

            self.__wait_for("paging") # 각 신문사 별 하단 페이징 요소 로딩 될 때까지 대기

            # TODO.
            # 1. parsing 해서 저장
            # 2. 다음 PAGING 할 부분이 있는지 확인
            # 3. 없으면? break
            # 4. 있으면 idx += 1, page_cnt = 10 * idx + 1 

        # total_page_cnt = self.get_total_page_cnt(p_id=p_id, target_date=target_date)
        # for page in range(1, total_page_cnt+1):
        #     url = NAVER_URL.format(p_id=p_id, target_date=target_date, page=page)
        #     self.browser.get(url)
        #     print(url)

        #     self.__wait_for("paging") # 각 신문사 별 하단 페이징 요소 로딩 될 때까지 대기

        #     p_list = self.browser.find_elements(By.CLASS_NAME, "type02")
        #     for p in p_list:
        #         n_list = p.find_elements(By.TAG_NAME, "a")
        #         for n in n_list:
        #             title, url = n.text, n.get_attribute("href")
        #             a_id = url.split("?")[0].split("/")[-1]

        #             self.news[p_id].append(self.__get_news_template(a_id, url, title, None, None))
            
        # text = f'{target_date} - {self.publisher.get(p_id)}_{total_page_cnt} pages_{len(self.news.get(p_id))} news'
        # print(text)

    def finish(self):
        self.browser.quit()

    async def crawl(self, start_date, end_date=None):
        self.news = None

        if end_date is None:
            end_date = start_date

        tasks = []
        for section, keyword_list in self.keywords.items():
            for keyword in keyword_list:
                print(f'Requested {section} {keyword}')
                tasks.append(asyncio.create_task(self.get_news_info(section, keyword, start_date, end_date)))
        
        for task in tasks:
            await task

        self.finish()

        return self.news
