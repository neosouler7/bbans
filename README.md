# Breaking BAd NewS

## 1. 주요 기능
네이버에 게시된 기사 중, 특정 키워드 기준으로 회사의 대외 이미지에 악영향을 끼칠 수 있는 뉴스 기사 수집 봇(using ChatGPT)

### 1.1. 소스 구조
main.py : telegram dispatcher를 실행하며 주요 명령어에 대한 handler를 셋팅한다.

manager / tg.py : 메세지 전송 등 주요 tg 관련 기능을 제공한다.  
manager / commander.py : 서비스 내 실행 가능한 주요 명령어에 대한 제어 및 작동 기능을 제공한다.  
manager / naver.py : 특정 키워드에 대한 네이버 뉴스 게시글 정보를 수집한다.  
manager / chatgpt.py : chatgpt에 질의하여 획득한 정보에 대한 추가 가공을 진행한다.   
manager / mail.py : 정형화된 형태로 최종 레포팅을 수행한다.    
manager / utils.py : 프로젝트 내 공용으로 사용되는 함수를 제공한다.  

### 1.2. 리턴 형태
```
[경영이슈]
경영이슈 관련 부정 기사에 대한 제목1 (언론사, 날짜) [하이퍼링크]

[완성차]
완성차 관련 부정 기사에 대한 제목1 (언론사, 날짜) [하이퍼링크]
완성차 관련 부정 기사에 대한 제목2 (언론사, 날짜) [하이퍼링크]

[그룹사]
그룹사 관련 부정 기사에 대한 제목1 (언론사, 날짜) [하이퍼링크]
그룹사 관련 부정 기사에 대한 제목2 (언론사, 날짜) [하이퍼링크]

```

### 1.3. 성능
5/17 - 0.072초 (111개 기사, 8초): 단순 크롤링, ChatGPT X

### 1.4. 비용
산정 필요  