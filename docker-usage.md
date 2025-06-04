# Docker Compose 사용 가이드

## 환경 설정

먼저 환경 변수 파일을 생성하세요:

```bash
# .env 파일 생성
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

## 서비스 실행

### 1. RAG 시스템 상시 실행

```bash
# RAG 시스템만 실행 (상시 작동)
docker-compose up -d rag-system
```

RAG API는 `http://localhost:8000`에서 접근 가능합니다.

### 2. 웹 크롤러 수동 실행

```bash
# 크롤러 실행 (일회성)
docker-compose --profile manual run --rm web-crawler
```

### 3. 데이터 파이프라인 실행

크롤러 실행 후 CSV를 RAG 시스템에 넣기:

```bash
# 파이프라인 실행 (크롤러 실행 후)
docker-compose --profile manual run --rm data-pipeline
```

### 4. 전체 워크플로우 실행

```bash
# 1단계: RAG 시스템 시작
docker-compose up -d rag-system

# 2단계: 크롤러 실행
docker-compose --profile manual run --rm web-crawler

# 3단계: 파이프라인 실행  
docker-compose --profile manual run --rm data-pipeline
```

## API 사용법

### 문서 검색

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "피싱 사이트", "top_k": 5}'
```

### 통계 조회

```bash
curl "http://localhost:8000/stats"
```

### 문서 추가

```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '[{
    "id": "test_1",
    "text": "테스트 문서입니다",
    "metadata": {"source": "manual"}
  }]'
```

## 데이터 관리

### 볼륨 확인

```bash
# 볼륨 목록
docker volume ls

# ChromaDB 데이터 볼륨
docker volume inspect lang_chain_chroma_data
```

### 데이터 초기화

```bash
# 모든 서비스 중지
docker-compose down

# 볼륨 삭제 (데이터 완전 삭제)
docker-compose down -v
```

## 문제 해결

### 서비스 상태 확인

```bash
# 실행 중인 서비스 확인
docker-compose ps

# 로그 확인
docker-compose logs rag-system
docker-compose logs web-crawler
docker-compose logs data-pipeline
```

### 개별 서비스 재시작

```bash
# RAG 시스템 재시작
docker-compose restart rag-system
```

### 컨테이너 내부 접근

```bash
# RAG 시스템 컨테이너 접근
docker-compose exec rag-system /bin/bash
``` 