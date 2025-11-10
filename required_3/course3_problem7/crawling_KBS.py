# crawling_KBS.py

import requests
from bs4 import BeautifulSoup

# KBS 뉴스 웹사이트 주소
url = 'https://news.kbs.co.kr/news/pc/main/main.html'
try:
    response = requests.get(url)
    response.raise_for_status() # 오류 발생 시 예외 처리
except requests.exceptions.RequestException as e:
    print(f"웹사이트에 접속할 수 없습니다: {e}")
    exit()

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

# --- (수정된 부분) ---
headline_elements = soup.select('div.txt-wrapper > p.title')
# --- (수정 끝) ---

# List 객체에 헤드라인 텍스트 저장
headline_list = []
for element in headline_elements:
    title = element.get_text(strip=True)
    if title:
        headline_list.append(title)

# 결과 출력
if headline_list:
    print("--- KBS 뉴스 주요 헤드라인 ---")
    for i, headline in enumerate(headline_list, 1):
        print(f"{i}. {headline}")
else:
    print("헤드라인 뉴스를 가져오는 데 실패했습니다.")