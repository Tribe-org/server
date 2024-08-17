# server

# 개발 시작하기 전 필수 셋팅
## 개발 환경 실행 방법
### Mac
```bash
source ./setup-dev.sh
```

만약 권한 문제가 발생하면, 아래의 명령어를 먼저 실행 후 재시도
```bash
chmod +x ./setup-dev.sh
```

### Window
```bash
python3 -m venv .venv
./venv/bin/activate
pip install -r requirements-dev.txt
pip list
```

가상 환경 종료
```bash
deactivate
```

## 커밋 환경 설정
### Mac
`setup-dev.sh` 파일에 이미 들어있음

### Window
```bash
cp scripts/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

## 설치 패키지 (vscode 익스텐션)
- Python (https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- isort (https://marketplace.visualstudio.com/items?itemName=ms-python.isort)