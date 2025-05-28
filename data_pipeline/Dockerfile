FROM python:3.11-slim

WORKDIR /app

# Python dependency 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 기본 명령어
CMD ["python", "csv_to_rag.py"] 