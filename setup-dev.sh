#!/bin/bash

# 가상 환경 생성
python3 -m venv .venv

# 가상 환경 실행
source .venv/bin/activate

# 패키지 설치
pip install -r requirements-dev.txt

# 패키지 설치 목록 확인
pip list