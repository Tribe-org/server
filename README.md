# server

# 개발 환경 실행 방법
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
.\venv\Scripts\activate
pip install -r requirements-dev.txt
pip list
```

가상 환경 종료
```bash
deactivate
```