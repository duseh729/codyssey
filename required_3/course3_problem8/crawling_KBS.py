# crawling_KBS.py
# -*- coding: utf-8 -*-

import os
import sys
import time
from typing import List, Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver(chromedriver_path: Optional[str] = None, headless: bool = False) -> webdriver.Chrome:
    """크롬 드라이버를 초기화하고 기본 옵션을 설정한다."""
    opts = Options()
    opts.add_argument('--lang=ko-KR')
    opts.add_argument('--window-size=1280,900')
    if headless:
        opts.add_argument('--headless=new')
        opts.add_argument('--disable-gpu')

    # 드라이버 경로가 존재하면 해당 경로 사용, 아니면 기본 경로 사용
    if chromedriver_path and os.path.exists(chromedriver_path):
        driver = webdriver.Chrome(options=opts)
    else:
        # PATH에 등록된 드라이버 또는 Selenium 자동탐색 기능 사용
        driver = webdriver.Chrome(options=opts)

    driver.implicitly_wait(2)
    return driver


def wait_for(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10):
    """지정한 요소가 나타날 때까지 최대 timeout초 동안 대기한다."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def login_naver(driver: webdriver.Chrome, user_id: str, user_pw: str) -> bool:
    """네이버 로그인 페이지에서 아이디와 비밀번호를 입력해 로그인 시도 후 성공 여부를 반환한다."""
    driver.get('https://nid.naver.com/nidlogin.login')
    try:
        # 로그인 입력창이 로딩될 때까지 대기
        wait_for(driver, By.CSS_SELECTOR, 'input[name="id"]', timeout=10)
    except TimeoutException:
        pass

    # 아이디와 비밀번호 입력 시도
    try:
        id_box = driver.find_element(By.CSS_SELECTOR, 'input[name="id"]')
        pw_box = driver.find_element(By.CSS_SELECTOR, 'input[name="pw"]')
        id_box.clear()
        id_box.send_keys(user_id)
        pw_box.clear()
        pw_box.send_keys(user_pw)

        # 로그인 버튼 클릭 (UI 구조 변경 대응)
        try:
            login_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        except NoSuchElementException:
            login_btn = driver.find_element(By.ID, 'log.login')
        login_btn.click()
    except NoSuchElementException:
        # 로그인 화면이 바뀌었거나 보안 단계로 전환된 경우 예외 처리
        pass

    # 로그인 성공 여부 판별
    # 보안문자/2단계 인증이 있으면 사용자가 직접 처리할 수 있도록 대기
    success = False
    max_wait_sec = 120
    start = time.time()
    while time.time() - start < max_wait_sec:
        cur = driver.current_url
        # 로그인 후 메인 페이지나 서비스 도메인으로 이동 시 성공 처리
        if 'https://www.naver.com/' in cur or 'mail.naver.com' in cur or 'news.naver.com' in cur:
            success = True
            break
        # 상단 사용자 메뉴가 보이면 로그인 완료로 간주
        els = driver.find_elements(By.CSS_SELECTOR, '[data-clk*="my"], a#NM_MY_ACCOUNT, a#gnb_my_page, a#account')
        if els:
            success = True
            break
        time.sleep(1)

    return success


def collect_mainpage_titles(driver: webdriver.Chrome, limit: int = 10) -> List[str]:
    """
    네이버 메인 페이지에서 주요 뉴스/콘텐츠의 제목 일부를 수집한다.
    로그인 전/후 동일한 함수로 호출해 비교할 수 있다.
    """
    driver.get('https://www.naver.com/')
    time.sleep(2)

    candidates: List[str] = []

    # 메인 화면 내 다양한 블록에서 텍스트를 추출한다.
    # 네이버 메인 구조는 자주 바뀌므로 여러 선택자를 시도한다.
    selectors = [
        'a.media_end_head_headline',     # 뉴스 상세 카드
        'div.section a',                 # 섹션 전반
        'a[href*="news.naver.com"]',     # 뉴스 링크
        'a[href*="entertain.naver.com"]',# 연예
        'a[href*="sports.naver.com"]',   # 스포츠
        'a.theme_item',                  # 테마 카드
        'strong.title, span.title, em.title',  # 제목 태그
    ]

    seen = set()
    for css in selectors:
        for a in driver.find_elements(By.CSS_SELECTOR, css):
            txt = (a.text or '').strip()
            if txt and txt not in seen:
                seen.add(txt)
                candidates.append(txt)
            if len(candidates) >= limit:
                break
        if len(candidates) >= limit:
            break

    return candidates


def collect_mail_subjects(driver: webdriver.Chrome, limit: int = 30) -> List[str]:
    """
    로그인한 사용자의 네이버 메일함에서 최신 메일 제목을 수집한다.
    메일 UI가 자주 변경되므로 여러 선택자를 순차적으로 시도한다.
    """
    driver.get('https://mail.naver.com/')
    time.sleep(4)  # iframe/SPA 로딩을 고려해 충분히 대기

    subjects: List[str] = []
    tried_selectors = [
        'strong.mail_title',               # 구버전 UI
        'span.mail_title',                 # 일부 레이아웃
        'a.subject',                       # 자주 쓰이는 구조
        'div.subject a',                   # 컨테이너 내부 링크
        '[data-subject]',                  # 데이터 속성 기반
        '[role="row"] [role="gridcell"] a' # 접근성 구조(ARIA)
    ]

    seen = set()
    for css in tried_selectors:
        for el in driver.find_elements(By.CSS_SELECTOR, css):
            text = (el.text or '').strip()
            if not text:
                # 텍스트가 없을 경우 title 속성에서 추출
                text = (el.get_attribute('title') or '').strip()
            if text and text not in seen:
                seen.add(text)
                subjects.append(text)
            if len(subjects) >= limit:
                break
        if len(subjects) >= limit:
            break

    return subjects


def print_list(title: str, items: List[str]) -> None:
    """리스트 데이터를 구분선과 함께 출력한다."""
    print('-' * 80)
    print(title)
    print('-' * 80)
    if not items:
        print('(데이터 없음)')
        return
    for i, v in enumerate(items, 1):
        print(f'{i:02d}. {v}')


def main() -> None:
    """프로그램 실행의 시작점 (엔트리 포인트)."""
    # 사용자에게 네이버 계정 정보를 입력받는다.
    user_id = input('네이버 아이디를 입력하세요.: ').strip()
    user_pw = input('네이버 비밀번호를 입력하세요.: ').strip()

    # 환경 변수에 지정된 크롬드라이버 경로가 있으면 사용한다.
    chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')

    driver = setup_driver(chromedriver_path=chromedriver_path, headless=False)

    try:
        # (1) 로그인 전 주요 콘텐츠 수집
        before_titles = collect_mainpage_titles(driver, limit=10)

        # (2) 로그인 수행
        ok = login_naver(driver, user_id, user_pw)
        if not ok:
            print('로그인에 실패했습니다. 보안문자나 2단계 인증을 완료했는지 확인하세요.')
            sys.exit(1)

        # (3) 로그인 후 주요 콘텐츠 수집
        after_titles = collect_mainpage_titles(driver, limit=10)

        # (4) 로그인 전/후 콘텐츠 비교 결과 출력
        print_list('로그인 전 메인 타이틀', before_titles)
        print_list('로그인 후 메인 타이틀', after_titles)

        # (5) 로그인 사용자 전용 콘텐츠(메일 제목) 수집
        mail_subjects = collect_mail_subjects(driver, limit=30)
        print_list('네이버 메일 최근 제목', mail_subjects)

        # (6) 리스트 객체로 출력 완료 (별도 저장 불필요)
    finally:
        # 결과 확인을 위해 잠시 대기 후 브라우저 종료
        time.sleep(2)
        driver.quit()


if __name__ == '__main__':
    main()
