
# server

  

# 개발 시작하기 전 필수 셋팅
## 개발 환경 설정
### 최초 설정

#### .env 파일 만들기
`.env` 파일을 만들어 아래와 같은 형식으로 내용을 설정합니다. (필수)

```bash
# GPG 키를 만들 때 설정했던 email. 부등호 기호는 넣지 않음
# ex) GPG_EMAIL=sample@example.com
GPG_EMAIL=<gpg_email>
# GPG 키를 만들 때 설정했던 비밀번호. 부등호 기호는 넣지 않음
# ex) GPG_PASSWORD=12345678
GPG_PASSWORD=<gpg_password>
```

#### gpg 키 생성하기
[컨플루언스_GPG_키_생성_가이드](https://tribe-forus.atlassian.net/wiki/spaces/PM/pages/13795548/.env#gpg-%ED%82%A4-%EB%A7%8C%EB%93%A4%EA%B8%B0) 참고

#### gpg 키 내보낸 후 기존 팀원에게 등록 요청
[컨플루언스_GPG_키_내보내기_가이드](https://tribe-forus.atlassian.net/wiki/spaces/PM/pages/13795548/.env#2%29-%EA%B3%B5%EA%B0%9C-%ED%82%A4-%EB%82%B4%EB%B3%B4%EB%82%B4%EA%B8%B0) 참고

### 개발 환경 설정 스크립트
#### Mac

```bash
source  ./setup-dev.sh
```

만약 권한 문제가 발생하면, 아래의 명령어를 먼저 실행 후 재시도

```bash
chmod  +x  ./setup-dev.sh
```

#### Window

```bash
python3  -m  venv  .venv
./venv/bin/activate
pip  install  -r  requirements-dev.txt
pip  list
```

#### 가상 환경 종료

```bash
deactivate
```

## 설치 패키지 (vscode 익스텐션)

- Python (https://marketplace.visualstudio.com/items?itemName=ms-python.python)

- isort (https://marketplace.visualstudio.com/items?itemName=ms-python.isort)