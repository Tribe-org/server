FROM python:3.12-slim

WORKDIR /app

# 필요한 패키지 설치 (gnupg와 git-secret 설치)
RUN apt-get update && apt-get install -y \
    gnupg \
    git \
    git-secret \
    man \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
# Python 의존성 설치
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# 프로젝트 루트의 모든 파일 복사
COPY ./app /app/app
COPY ./scripts /app/scripts
COPY .env /app/.env
COPY .git /app/.git
COPY .gitsecret /app/.gitsecret
COPY my_private_key.asc /app/my_private_key.asc
COPY .gitignore /app/.gitignore
COPY .secrets.secret /app/.secrets.secret


# 스크립트 권한 설정
RUN chmod +x /app/scripts/env.sh

# 환경 스크립트 실행
RUN python3 /app/scripts/private_key.py
RUN /bin/sh /app/scripts/env.sh

# 포트 설정
EXPOSE 8081

# CMD: 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]