#!/bin/bash
echo -e "\033[34m.env 파일 생성을 시작합니다.\033[0m"

# .env 파일에서 GPG_EMAIL과 GPG_PASSWORD 값 읽기
GPG_EMAIL=$(grep -w "GPG_EMAIL" .env | cut -d '=' -f2)
GPG_PASSWORD=$(grep -w "GPG_PASSWORD" .env | cut -d '=' -f2)

# GPG_EMAIL 또는 GPG_PASSWORD가 존재하지 않으면 오류 처리
if [ -z "$GPG_EMAIL" ] || [ -z "$GPG_PASSWORD" ]; then
    echo -e "\033[31m에러: .env 파일에 GPG_EMAIL 또는 GPG_PASSWORD가 설정되어 있지 않습니다.\033[0m"
    exit 1
fi

# gpg-agent 설정 파일 생성
mkdir -p ~/.gnupg
chmod 700 ~/.gnupg
echo "allow-loopback-pinentry" > ~/.gnupg/gpg-agent.conf

# gpg-agent 재시작
gpg-connect-agent reloadagent /bye

# 비밀번호를 gpg-agent에 캐싱
echo "$GPG_PASSWORD" | gpg --batch --yes --passphrase-fd 0 --pinentry-mode loopback --import my_private_key.asc

# 개인 키 임포트 성공 여부 확인
if [ $? -ne 0 ]; then
    echo -e "\033[31m에러: 개인 키 import에 실패했습니다.\033[0m"
    exit 1
fi

echo -e "\033[32m개인 키를 성공적으로 import 했습니다.\033[0m"

# git secret reveal 실행 (비대화식으로 처리)
git secret reveal -v -p $GPG_PASSWORD

# git secret reveal 실패 시 오류 처리
if [ $? -ne 0 ]; then
    echo -e "\033[31m에러: git secret reveal에 실패했습니다. 파일을 수정하지 않습니다.\033[0m"
    exit 1
fi

# .secrets.secret 파일이 텍스트 파일인지 확인
file_type=$(file --mime-type -b .secrets)

if [[ "$file_type" != "text/plain" ]]; then
    echo -e "\033[31m에러: .secrets.secret 파일이 텍스트 형식이 아닙니다.\033[0m"
    exit 1
fi

# .secrets 파일 확인 및 .env 덮어쓰기
if [ -f ".secrets" ]; then
    # 임시 파일에 GPG_EMAIL과 GPG_PASSWORD 저장
    echo "GPG_EMAIL=$GPG_EMAIL" > .env.tmp
    echo "GPG_PASSWORD=$GPG_PASSWORD" >> .env.tmp
    echo "" >> .env.tmp  # 개행 추가

    # .secrets 파일의 내용을 임시 파일에 추가
    cat .secrets >> .env.tmp

    # .env.tmp 파일을 .env 파일로 덮어쓰기
    mv .env.tmp .env

    echo -e "\033[32m.env 파일이 성공적으로 수정되었습니다.\033[0m"
else
    echo -e "\033[31m에러: .secrets 파일을 찾을 수 없습니다.\033[0m"
    exit 1
fi