# utils/failed_logger.py

import os
from typing import List


def log_failed_urls(failed_urls: List[str], path: str = "output/failed_urls.txt", append: bool = True) -> None:
    """
    본문 추출에 실패한 URL들을 로그 파일에 기록합니다.

    :param failed_urls: 실패한 URL 문자열 리스트
    :param path: 저장할 파일 경로
    :param append: True이면 이어쓰기, False이면 덮어쓰기
    """
    if not failed_urls:
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)

    mode = "a" if append else "w"

    with open(path, mode, encoding="utf-8") as f:
        for url in failed_urls:
            f.write(url.strip() + "\n")
