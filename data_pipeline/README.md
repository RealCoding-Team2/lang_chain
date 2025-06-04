# Data Pipeline

web_crawler에서 수집한 CSV 데이터를 RAG 시스템의 벡터 데이터베이스에 넣는 파이프라인입니다.

## 기능

- CSV 파일(title, url, date, body)을 읽어서 RAG 시스템에 저장
- 긴 content(body)를 의미있는 청크로 분할
- 각 청크에 메타데이터 정보 포함 (제목, URL, 날짜 등)
- 검색 성능 향상을 위한 제목 정보 포함
- 검색 테스트 기능 제공

## 설치

```bash
pip install -r requirements.txt
```

## 환경 설정

rag_system 폴더의 env_example을 참고하여 `.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
# rag_system/.env
OPENAI_API_KEY=your_openai_api_key_here
```

## 사용법

```bash
cd data_pipeline
python csv_to_rag.py
```

## 주요 클래스

### CSVToRAGPipeline

- `process_csv_file(csv_file_path)`: CSV 파일을 처리하여 RAG 시스템에 추가
- `split_text_into_chunks(text, title)`: 텍스트를 청크로 분할
- `search_test(query, top_k)`: 검색 테스트 실행

## 청크 분할 방식

- 문장 단위로 분할 (한국어 문장 부호 고려)
- 청크 크기: 500자
- 각 청크에 제목 정보 포함으로 검색 성능 향상
- 메타데이터에 청크 인덱스 및 전체 청크 수 정보 포함

## 메타데이터 구조

각 문서 청크는 다음 메타데이터를 포함합니다:

```python
{
    'title': '원본 제목',
    'url': '원본 URL',
    'date': '날짜',
    'source_row': 'CSV 행 번호',
    'chunk_index': '청크 인덱스',
    'total_chunks': '전체 청크 수',
    'added_at': '추가 시각',
    'source_file': '소스 파일명'
}
```

## 검색 예시

파이프라인 실행 후 자동으로 다음 쿼리들로 검색 테스트를 수행합니다:

- "피싱 사이트"
- "보안 위협" 
- "악성 링크"

각 검색 결과는 유사도 점수, 제목, URL, 날짜, 내용 미리보기를 포함합니다. 