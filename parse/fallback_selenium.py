# parse/fallback_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from typing import Optional, Dict
from time import sleep


def extract_with_selenium(url: str) -> Optional[Dict[str, str]]:
    """
    셀레니움을 이용해 자바스크립트 렌더링 기반 뉴스 기사에서
    제목과 본문을 추출합니다.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920x1080")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        sleep(2)  # JS 렌더링 대기

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
    except TimeoutException:
        print(f"[Timeout] {url}")
        return None
    except Exception as e:
        print(f"[Selenium Error] {url}: {e}")
        return None

    # 공통적인 기사 본문/제목 선택자 몇 가지 시도
    title = (
        soup.find("h1")
        or soup.find("h2")
    )
    body = (
        soup.find("div", class_="article-body")
        or soup.find("div", class_="content")
        or soup.find("div", id="articleBody")
        or soup.find("article")
    )

    title_text = title.get_text(strip=True) if title else ""
    body_text = body.get_text(separator="\n", strip=True) if body else ""

    if not body_text:
        return None

    return {
        "title": title_text,
        "body": body_text,
        "url": url,
        "date": ""  # fallback이기 때문에 날짜 정보는 비워둠
    }
