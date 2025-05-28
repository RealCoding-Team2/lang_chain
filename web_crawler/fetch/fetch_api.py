# fetch/fetch_api.py

import os # 테스트용 임시 코드
import sys # 테스트용 임시 코드

import requests
from typing import List, Dict
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # 테스트용 임시 코드
from config import API_URL, HEADERS


def fetch_articles_from_api() -> List[Dict[str, str]]:
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch data from API: {e}")
        return []

    data = response.json().get("data", [])

    article_list = []
    for item in data:
        article_list.append({
            "title": item.get("title", "").strip(),
            "url": item.get("pageUrl", "").strip(),
            "date": timestamp_to_date(item.get("updatedAt", 0))
        })

    return article_list


def timestamp_to_date(timestamp_ms: int) -> str:
    """
    밀리초 단위 timestamp를 'YYYY-MM-DD' 문자열로 변환
    """
    try:
        return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d")
    except Exception:
        return ""


# 테스트용 실행
if __name__ == "__main__":
    articles = fetch_articles_from_api()
    for article in articles:
        print(article)
