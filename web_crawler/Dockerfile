# Python 3.11 slim 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome 설치 (2024년 최신 방식)
RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

# ChromeDriver 설치 (selenium manager가 자동으로 처리하므로 제거)
# 최신 Selenium 버전에서는 ChromeDriver를 자동으로 다운로드하여 관리

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# output 디렉토리 생성 (결과 파일 저장용)
RUN mkdir -p output

# 비 root 사용자 생성 및 권한 설정
RUN useradd -m -u 1000 crawler && \
    chown -R crawler:crawler /app
USER crawler

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# 기본 실행 명령
CMD ["python", "main.py"] 