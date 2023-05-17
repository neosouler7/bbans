from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from manager.utils import read_config, get_current_time, to_date_dot, DATE_FORMAT_YmdHMS
from collections import defaultdict
from datetime import datetime

TARGET_URL = "https://search.naver.com/search.naver?where=news&sort=1&ds={start_date_dot}&de={end_date_dot}&nso=so:r,p:from{start_date}to{end_date},a:all&query={keyword}&start={article_cnt}"


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
        self.news = list()

    def __get_news_template(self, section, keyword, url, title, publisher, published_at):
        t = {
            'section': section,
            'keyword': keyword,
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
        start_date_dot, end_date_dot = to_date_dot(start_date), to_date_dot(end_date)
        article_cnt, idx = 1, 0
        while True:
            target_url = TARGET_URL.format(start_date_dot=start_date_dot, end_date_dot=end_date_dot, start_date=start_date, end_date=end_date, keyword=keyword, article_cnt=article_cnt)
            print(target_url)
            
            self.browser.get(target_url)
            # self.__wait_for("sc_page") # 각 신문사 별 하단 페이징 요소 로딩 될 때까지 대기

            news_list = self.browser.find_element(By.CLASS_NAME, "list_news").find_elements(By.TAG_NAME, "li")
            for news in news_list:
                info_group = news.find_element(By.CLASS_NAME, "news_info").find_element(By.CLASS_NAME, "info_group")
                news_area = news.find_element(By.CLASS_NAME, "news_area")
                news_tit = news_area.find_element(By.CLASS_NAME, "news_tit")

                publisher = info_group.find_element(By.TAG_NAME, "a").text
                title, url = news_tit.text, news_tit.get_attribute("href")

                temp = self.__get_news_template(
                    section = section,
                    keyword = keyword,
                    url = url, 
                    title = title, 
                    publisher = publisher,
                    published_at = f"{start_date[4:6]}/{start_date[6:]}"
                )
                self.news.append(temp)


            page_list = self.browser.find_element(By.CLASS_NAME, "sc_page").find_element(By.CLASS_NAME, "sc_page_inner").find_elements(By.TAG_NAME, "a")
            max_page = max([p.text for p in page_list])
            for page in page_list:
                if page.text == max_page and page.get_attribute("aria-pressed") == "true": # 리턴되는 가장 큰 페이지가 true로 반환 될 때
                    return

            idx += 1
            article_cnt = 10 * idx + 1  

    def finish(self):
        self.browser.quit()

    def crawl(self, start_date, end_date=None):
        self.news.clear()

        if end_date is None:
            end_date = start_date

        start_time = datetime.strptime(get_current_time(DATE_FORMAT_YmdHMS), DATE_FORMAT_YmdHMS)

        for section, keyword_list in self.keywords.items():
            for keyword in keyword_list:
                print(f'Requested {section} {keyword}')
                self.get_news_info(section, keyword, start_date, end_date)

        end_time = datetime.strptime(get_current_time(DATE_FORMAT_YmdHMS), DATE_FORMAT_YmdHMS)
        print(f'\n{start_date} ~ {end_date} {len(self.news)} news with {(end_time - start_time).total_seconds()}s\n')

        self.finish()

        return self.news
