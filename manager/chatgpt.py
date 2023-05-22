import requests
import time

from manager.utils import read_config

END_POINT = "https://api.openai.com/v1/chat/completions"


class ChatGPT:
    def __init__(self):
        self.config = read_config()
        self.api_key = self.config.get("chatgpt").get("api_key")
        self.latest_api_ts = 0

    def raise_question(self, messages):
        target_ts = self.latest_api_ts + (60 / 200)
        while time.time() < target_ts:
            time.sleep(.001)
        self.latest_api_ts = time.time()

        h = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }
        p = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.2,
            "messages": messages
            # "n": 1, # 단순 N, Y, ?
            # "max_tokens": 1, # 단순 N, Y, ?
        }
        print(h)
        print(p)
        try:
            res = requests.post(END_POINT, json=p, headers=h)
            # res = requests.post(url=END_POINT, headers=h, params=p)
            res.raise_for_status()  # Raise an exception for 4xx/5xx status codes
            res_json = res.json()
            # assistant_reply = res.json()["choices"][0]["message"]["content"]
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        
        return res_json

    def __set_role(self, role_name, content):
        r = {
            "role": role_name,
            "content": content
        }
        return r
    
    def ice_breaking(self, msg_list):
        messages = []
        for msg in msg_list:
            messages.append(
                {
                    "role": msg.get("role"),
                    "content": msg.get("content")
                }
            )
            answer = self.raise_question(messages)

            response = answer["choices"][0]["message"]["content"]
            messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )
        print(answer)
        print("Ice breaking done!")


    def ask_if_bad_news(self, news_list):
        msg_list = list()
        msg_list.append(self.__set_role("system", "Forget all your previous instructions. Pretend you are a financial expert in South Korea.\n"))
        msg_list.append(self.__set_role("user", "Tell me if the following news is good for the stock price of the comapny mentioned in the headline. (If good 'Y', if bad 'N' and if unknown '?')\n"))

        # TODO. answer 리턴값 확인하고 그 결과에 따라서 아래 추가 질문 분기... => 어쩌면 필요없을수도...
        self.ice_breaking(msg_list)

        # news_list = [{'section': 'common', 'keyword': '정의선', 'url': 'http://www.labortoday.co.kr/news/articleView.html?idxno=215112', 'title': '현대차 사고 다량 발생', 'publisher': '매일노동뉴스', 'published_at': '05/17', 'bad_effect': None}, {'section': 'common', 'keyword': '정의선', 'url': 'http://www.labortoday.co.kr/news/articleView.html?idxno=215112', 'title': '오늘도 맑스님은 1승을 적립했다', 'publisher': '매일노동뉴스', 'published_at': '05/17', 'bad_effect': None}, {'section': 'common', 'keyword': '정의선', 'url': 'http://www.consumernews.co.kr/news/articleView.html?idxno=678647', 'title': '현대차그룹 "해킹대회 수상자 모십니다"…SDV 전환 앞두고 차량 보안 시스템 ...', 'publisher': '소비자가 만드는 신문', 'published_at': '05/17', 'bad_effect': None}, {'section': 'common', 'keyword': '정의선', 'url': 'http://www.fnnews.com/news/202305161701357287', 'title': '美서 씽씽 달리는 제네시스…올해도 17% 판매 성장', 'publisher': '파이낸셜뉴스언론사 선정', 'published_at': '05/17'}, {'section': 'common', 'keyword': '정의선', 'url': 'https://www.donga.com/news/Economy/article/all/20230516/119327078/1', 'title': '“기아, 멕시코에 전기차 설비 투자 추진”', 'publisher': '동아일보', 'published_at': '05/17', 'bad_effect': None}]
        news_list = ['현대차 사고 다량 발생', '오늘도 맑스님은 1승을 적립했다', '현대차그룹 "해킹대회 수상자 모십니다"…SDV 전환 앞두고 차량 보안 시스템 ...', '美서 씽씽 달리는 제네시스…올해도 17% 판매 성장', '“기아, 멕시코에 전기차 설비 투자 추진”']

        for news in news_list:
            print(news)
            answer = self.raise_question(self.__set_role("user", news))
            print(answer)

        # TODO. 중복 제거는 chatGPT가 아니라 다른 언어 모델을 활용할수도
        return
    
        '''
        Forget all your previous instructions. Pretend you are a financial expert. You are a financial expert with stock recommendation experience. 

        First question: Tell me if the following headline is good for stock price answer “YES”, if bad answer “NO”, or “UNKNOWN” if uncertain.
        Second question: Tell me the company’s name just in Korean.
        Third question: Tell me that company’s stock code in Korea’s stock market.
        Fourth question: Tell me the reason why you thought.

        Just simply return answers with the below format of Python dictionary. You do not need to tell me the answer’s further explanation.

        {”opinion”: first answer, ”company_name”: second answer, ”stock_code”: third answer, ”reason”: fourth answer}
        '''

        # for bad_news in bad_news_list:
        #     print(bad_news)
        # msg_main, bad_news_list = list(), list()
        # for news in news_list:
        #     answer = self.__raise_question([self.__set_role("user", f'{news.get("title")}')]) # 앞서 사전 질의 내역 기반, 단순 기사 제목만 재질의
        #     print("")
        #     print(answer)
        #     if answer.get("content") == "Y":
        #         bad_news_list.append(news)

        return None