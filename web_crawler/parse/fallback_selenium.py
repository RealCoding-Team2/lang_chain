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

    # 공통적인 기사 제목 선택자 몇 가지 시도
    title = (
        soup.find("h1")
        or soup.find("h2")
        or soup.find("meta", property="og:title")
        or soup.find("meta", attrs={"name": "title"})
        or soup.find("div", class_="article-title")
        or soup.find("div", class_="news-title")
        or soup.find("header").find("h1") if soup.find("header") else None
    )

    # 공통적인 기사 본문 선택자 몇 가지 시도
    body = (
        soup.find("div", class_="article-body")
        or soup.find("div", class_="content")
        or soup.find("div", id="articleBody")
        or soup.find("article")
        or soup.find("div", class_="news_article")
        or soup.find("div", class_="article_txt")
        or soup.find("div", class_="art_txt")
        or soup.find("section", class_="article-content")
        or soup.find("div", class_="view-content")
        or soup.find("div", class_="article-view")
    )

    # 메타 태그에서 title 추출 (fallback)
    title_text = ""
    if title:
        if title.name == "meta":
            title_text = title.get("content", "")
        else:
            title_text = title.get_text(strip=True)

    body_text = body.get_text(separator="\n", strip=True) if body else ""

    if not body_text:
        return None

    return {
        "body": body_text,
        "url": url,
        "date": ""  
    }
