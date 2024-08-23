#!/bin/bash

# 가상 환경 생성
python3 -m venv .venv

# 가상 환경 실행
source .venv/bin/activate

# 패키지 설치
pip install -r requirements-dev.txt

# 패키지 설치 목록 확인
pip list

# commit-msg 훅 복사
cp scripts/commit-msg .git/hooks/commit-msg

# commit-msg 훅에 실행 권한 부여
chmod +x .git/hooks/commit-msg

python3 scripts/private_key.py

# .env 파일 생성
/bin/bash scripts/env.sh