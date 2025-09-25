# KBS 뉴스 헤드라인 크롤러 📰

KBS 뉴스 웹사이트의 주요 헤드라인을 수집하는 파이썬 스크립트.

## 주요 기능

* KBS 뉴스 헤드라인 크롤링
* `requests`, `BeautifulSoup` 사용
* JS 리다이렉트 우회
* 터미널에 결과를 리스트로 출력

## URL 설명

* **대상 URL** : `https://news.kbs.co.kr/news/pc/main/main.html`
* **이유** : 기본 주소(`http://news.kbs.co.kr`)는 JS 리다이렉션을 사용. `requests`는 JS를 실행하지 못하므로, PC용 최종 페이지로 직접 접속.
