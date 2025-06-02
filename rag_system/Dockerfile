FROM python:3.11-slim

WORKDIR /app

# 시스템 dependency 설치
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependency 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# ChromaDB 데이터 디렉토리 생성
RUN mkdir -p /app/chroma_db

# 포트 노출
EXPOSE 8000

# 서비스 실행
CMD ["python", "api.py"] 