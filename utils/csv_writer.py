# utils/csv_writer.py

import csv
import os
from typing import List, Dict


def save_articles_to_csv(articles: List[Dict[str, str]], output_path: str) -> None:
    """
    뉴스 기사 리스트를 CSV 파일로 저장합니다.

    :param articles: 기사 딕셔너리 리스트 (각 항목: title, url, date, body 등)
    :param output_path: 저장할 CSV 파일 경로
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = ["title", "url", "date", "body"]

    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for article in articles:
            # 결측값이나 줄바꿈 정리
            writer.writerow({
                "title": article.get("title", "").replace("\n", " ").strip(),
                "url": article.get("url", "").strip(),
                "date": article.get("date", "").strip(),
                "body": article.get("body", "").replace("\n", " ").strip()
            })
