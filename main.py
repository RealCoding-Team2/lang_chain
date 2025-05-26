# main.py

from fetch.fetch_api import fetch_articles_from_api
from fetch.fetch_article import get_article_body
from utils.csv_writer import save_articles_to_csv
from utils.failed_logger import log_failed_urls
from utils.multiprocessing_pool import run_parallel_jobs
from config import CSV_OUTPUT_PATH, FAILED_URLS_PATH, NUM_WORKERS

def main():
    print("[INFO] Fetching phishing article list from API...")
    articles_meta = fetch_articles_from_api()

    if not articles_meta:
        print("[ERROR] No articles found. Exiting.")
        return

    urls = [item["url"] for item in articles_meta]
    url_to_date = {item["url"]: item["date"] for item in articles_meta}
    url_to_title = {item["url"]: item["title"] for item in articles_meta} 

    print(f"[INFO] Crawling full articles from {len(urls)} URLs using {NUM_WORKERS} workers...")
    results, failed = run_parallel_jobs(get_article_body, urls, num_workers=NUM_WORKERS)

    # 날짜 정보 다시 합치기 (trafilatura나 selenium이 실패한 경우)
    for article in results:
        if not article.get("date"):
            article["date"] = url_to_date.get(article["url"], "")

            article["title"] = url_to_title.get(article["url"], "")

    print(f"[INFO] Successfully extracted {len(results)} articles.")
    print(f"[INFO] Failed to extract {len(failed)} articles.")

    # 저장
    save_articles_to_csv(results, CSV_OUTPUT_PATH)
    log_failed_urls(failed, FAILED_URLS_PATH)

    print(f"[INFO] CSV saved to {CSV_OUTPUT_PATH}")
    if failed:
        print(f"[INFO] Failed URLs saved to {FAILED_URLS_PATH}")


if __name__ == "__main__":
    main()
