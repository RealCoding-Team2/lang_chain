# config.py

# API URL (피싱 게시글 리스트)
API_URL = "https://www.phishingeyes.com/rest/v1/board-type/1/boards"

# User-Agent 헤더 (필요한 경우)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# 파일 저장 경로
CSV_OUTPUT_PATH = "output/phishing_news.csv"
FAILED_URLS_PATH = "output/failed_urls.txt"

# 트래필라투라 기본 설정 (본문 최소 길이, 타임아웃 등)
TRAFILATURA_CONFIG = {
    "DEFAULT": {
        "DOWNLOAD_TIMEOUT": "5",
        "MAX_REDIRECTS": "0",
        "MIN_OUTPUT_SIZE": "50"
    }
}

# 병렬 처리 관련 설정
NUM_WORKERS = 8         # 병렬 처리 워커 수
MAX_RETRIES = 3         # 요청 실패 시 최대 재시도 횟수
