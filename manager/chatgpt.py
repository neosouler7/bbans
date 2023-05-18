import requests
import jsoon

from manager.utils import read_config

END_POINT = "https://api.openai.com/v1/chat/completions"


class ChatGPT:
    def __init__(self):
        self.config = read_config()
        self.api_key = self.config.get("chatgpt").get("api_key")

    def __raise_question(self, messages):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        params = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.2,
            # "n": 1, # 단순 N, Y, ?
            # "max_tokens": 1, # 단순 N, Y, ?
            "messages": messages
        }
        try:
            res = requests.post(url=END_POINT, headers=headers, data=json.dumps(params))
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        
        # TODO. 리턴값 확인하기
        print(res)
        res_json = json.loads(res).get("choices")[0].get("message")
        return res_json

    def __set_role(self, role_name, content):
        r = {
            "role": role_name,
            "content": content
        }
        return r

    def ask_if_bad_news(self, news_list):
        msg = list()
        msg.append(self.__set_role("system", "당신은 대한민국 경제를 굉장히 잘 알고 있는 시사 전문가입니다."))
        msg.append(self.__set_role("asssisant", "제가 검색한 기사 제목이, 과연 제목 언에 언급된 회사의 대외 이미지에 안 좋은 영향을 끼치는지 알고 싶습니다."))
        msg.append(self.__set_role("user", "수집한 기사 전체의 제목을 알려줄테니 아래 내용 실행해주세요."))
        msg.append(self.__set_role("user", "1. 우선 기사 제목 내용을 기반으로 중복 기사 제거 필요"))
        msg.append(self.__set_role("user", "2. 기사 제목이 만약 회사의 대외 이미지에 긍정적이면, 기존 데이터 내 'bad_effect'라는 이름의 key로 다음의 value(긍정: 'N', 부정: 'Y', 알 수 없음: '?') set 필요"))
        # TODO 리턴 형태를 어떻ㄱ
        # msg.append(self.__set_role("user", "부가적인 설명 없이, 단순히 N / Y / ? 만 대답해 주시면 됩니다."))

        # TODO. answer 리턴값 확인하고 그 결과에 따라서 아래 추가 질문 분기... => 어쩌면 필요없을수도...
        answer = self.__raise_question(msg)
        print(answer)
        return

        bad_news_list = self.__raise_question(self.__set_role("user", news_list))
        # msg_main, bad_news_list = list(), list()
        # for news in news_list:
        #     answer = self.__raise_question([self.__set_role("user", f{news.get("title")})]) # 앞서 사전 질의 내역 기반, 단순 기사 제목만 재질의
        #     if answer.get("content") == "Y":
        #         bad_news_list.append(news)

        return bad_news_list