# fetch/fetch_article.py

from typing import Optional, Dict
from config import TRAFILATURA_CONFIG
import ujson as json

from trafilatura import fetch_url, extract
from parse.fallback_selenium import extract_with_selenium


def get_article_body(url: str) -> Optional[Dict[str, str]]:
    """
    주어진 뉴스 URL에서 제목과 본문을 추출합니다.
    1차: trafilatura 사용
    2차: 실패 시 Selenium으로 재시도
    """
    try:
        downloaded = fetch_url(url, config=TRAFILATURA_CONFIG)
        if downloaded is None:
            raise ValueError("Failed to fetch content with trafilatura")

        extracted = extract(
            downloaded,
            output_format="json",
            include_tables=False,
            with_metadata=True,
            deduplicate=True,
            config=TRAFILATURA_CONFIG,
        )

        if not extracted:
            raise ValueError("Extraction returned empty")

        extracted_data = json.loads(extracted)

        return {
            "title": extracted_data.get("title", "").strip(),
            "body": extracted_data.get("text", "").strip(),
            "url": url,
            "date": extracted_data.get("date", "")  # ISO date (optional)
        }

    except Exception:
        # 트래필라투라 실패 시 Selenium fallback
        return extract_with_selenium(url)
