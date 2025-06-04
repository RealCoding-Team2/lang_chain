# Docker Compose 워크플로우 가이드

## 개요
이 문서는 web_crawler → data_pipeline → rag_system의 순차적 실행을 위한 Docker Compose 워크플로우 사용법을 설명합니다.

## 실행 방법

### 1. 기본 RAG 시스템만 실행
```bash
docker-compose up rag-system
```

### 2. 전체 크롤링 워크플로우 실행 (권장)
```bash
# 워크플로우 초기화 및 전체 파이프라인 실행
docker-compose --profile crawler up --remove-orphans

# 또는 단계별 실행
docker-compose --profile workflow up workflow  # 초기화
docker-compose --profile crawler up web-crawler data-pipeline
```

### 3. 수동 단계별 실행
```bash
# 1단계: RAG 시스템 시작
docker-compose up -d rag-system

# 2단계: Web Crawler 실행
docker-compose run web-crawler

# 3단계: Data Pipeline 실행 (크롤러 완료 후)
docker-compose run data-pipeline
```

## 워크플로우 동작 방식

### 1. 의존성 체인
```
rag-system (상시 실행) 
    ↓
web-crawler (한 번 실행) 
    ↓ (완료 상태 파일 생성)
data-pipeline (대기 후 실행)
```

### 2. 상태 파일 관리
- `./status/crawler_status.txt`: web-crawler 완료 상태
- `./status/pipeline_status.txt`: data-pipeline 완료 상태
- `./status/workflow_status.txt`: 워크플로우 시작 상태

### 3. 공유 볼륨
- `shared_data`: 크롤링 결과 CSV 파일 공유
- `chroma_data`: ChromaDB 데이터 영속성
- `./status`: 실행 상태 파일 공유

## 프로파일 설명

### `crawler` 프로파일
- web-crawler와 data-pipeline을 순차 실행
- 한 번의 완전한 데이터 수집 및 처리 사이클

### `workflow` 프로파일  
- 워크플로우 초기화용
- 상태 파일 정리 및 초기 설정

## 환경 변수 설정

`.env` 파일 생성:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## 모니터링

### 실행 상태 확인
```bash
# 실행 중인 컨테이너 확인
docker-compose ps

# 로그 확인
docker-compose logs -f web-crawler
docker-compose logs -f data-pipeline

# 상태 파일 확인
ls -la status/
cat status/*.txt
```

### 볼륨 확인
```bash
# 공유 데이터 확인
docker-compose exec rag-system ls -la /app/
docker volume inspect lang_chain_shared_data
```

## 트러블슈팅

### 1. 워크플로우 재시작
```bash
# 모든 컨테이너 정리
docker-compose down --remove-orphans

# 상태 파일 정리
rm -f status/*.txt

# 재시작
docker-compose --profile crawler up
```

### 2. 개별 서비스 재시작
```bash
# 특정 서비스만 재시작
docker-compose restart rag-system
docker-compose run --rm web-crawler
```

### 3. 데이터 초기화
```bash
# 볼륨 데이터 삭제
docker-compose down -v

# 다시 시작
docker-compose up --build
```

## 개발 팁

### 로컬 개발 모드
```bash
# RAG 시스템만 실행하고 나머지는 로컬에서 개발
docker-compose up -d rag-system

# 로컬에서 크롤러 실행
cd web_crawler && python main.py

# 로컬에서 파이프라인 실행  
cd data_pipeline && python csv_to_rag.py
```

### 빠른 테스트
```bash
# 빌드 없이 실행 (이미지가 있는 경우)
docker-compose --profile crawler up --no-build

# 강제 재빌드
docker-compose --profile crawler up --build
``` 