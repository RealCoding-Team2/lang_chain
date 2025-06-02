import os
import hashlib
import pandas as pd
import requests
import json

def csv_to_rag(csv_file_path: str, rag_api_url: str = "http://rag-system:8000"):
    """CSV 파일을 RAG API를 통해 벡터 DB에 저장"""
    
    # CSV 읽기
    df = pd.read_csv(csv_file_path)
    df = df.dropna(subset=['body'])  # body 없는 행 제거
    
    print(f"{len(df)}개 행 로드됨")
    
    # 문서 생성
    documents = []
    for idx, row in df.iterrows():
        # URL 기반으로 고유 ID 생성
        url_hash = hashlib.md5(str(row['url']).encode('utf-8')).hexdigest()
        doc_id = f"doc_{url_hash}"
        
        documents.append({
            'id': doc_id,
            'text': f"{row['title']}\n{row['body']}",
            'metadata': {
                'title': str(row['title']),
                'url': str(row['url']),
                'date': str(row['date'])
            }
        })
    
    # RAG API를 통해 저장
    try:
        response = requests.post(
            f"{rag_api_url}/documents",
            json=documents,
            timeout=60
        )
        
        if response.status_code == 200:
            print(f"{len(documents)}개 문서 저장 완료")
            
            # 통계 조회
            stats_response = requests.get(f"{rag_api_url}/stats")
            if stats_response.status_code == 200:
                stats = stats_response.json()
                print(f"총 문서 수: {stats['document_count']}")
            
            return True
        else:
            print(f"저장 실패: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"API 연결 실패: {e}")
        return False

def main():
    csv_file = "/shared/output/phishing_news.csv"
    
    if os.path.exists(csv_file):
        csv_to_rag(csv_file)
    else:
        print(f"파일 없음: {csv_file}")

if __name__ == "__main__":
    main() 