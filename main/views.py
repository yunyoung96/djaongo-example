from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def fetch_boardgames():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome WebDriver 실행 성공")
    except Exception as e:
        print(f"❌ WebDriver 실행 실패: {e}")
        return []

    try:
        driver.get('https://boardlife.co.kr/rank/all/1')
        time.sleep(5)
        page_source = driver.page_source
        print("✅ 페이지 로딩 완료")
    except Exception as e:
        print(f"❌ 사이트 접속 실패: {e}")
        driver.quit()
        return []

    driver.quit()

    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        print("✅ BeautifulSoup 파싱 성공")
    except Exception as e:
        print(f"❌ 파싱 실패: {e}")
        return []

    # 게임 데이터 수집
    games = []

    # 각각의 게임 블록은 div.game-box나 tr 단위일 수 있으니 반복
    # 우리는 a 태그 기준으로 탐색하고, 그 부모에서 순위 추출
    a_tags = soup.find_all('a', class_='title new-ellip')
    for i, a in enumerate(a_tags, 1):
        title = a.get_text(strip=True)
        href = a.get('href')

        games.append({
            'rank': i,
            'title': title,
            'url': f"https://boardlife.co.kr{href}" if href else 'N/A'
        })

    print(f"✅ 총 {len(games)}개의 게임 수집 완료")
    return games

# Create your views here.
def index(request):
    games = fetch_boardgames()
    print("games : ", games[:10])
    return render(request,'main/index.html', {'games': games})