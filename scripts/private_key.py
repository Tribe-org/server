import getpass
import subprocess
import sys


def get_gpg_key_by_email(email):
    try:
        # gpg --list-keys 명령을 사용해 이메일과 관련된 키 목록을 검색
        result = subprocess.run(
            ["gpg", "--list-keys", "--with-colons", email],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            print(f"Error listing keys: {result.stderr}")
            return None

        # 결과에서 키 ID 추출 (pub 키 정보가 포함된 줄을 필터링)
        for line in result.stdout.splitlines():
            if line.startswith("pub"):
                key_id = line.split(":")[4]  # 키 ID는 콜론으로 구분된 5번째 필드
                return key_id

        # 키가 없는 경우
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def export_private_key(key_id):
    max_attempts = 3  # 최대 시도 횟수
    attempts = 0  # 현재 시도 횟수

    while attempts < max_attempts:
        # 사용자로부터 GPG 비밀번호 입력받기 (비밀번호가 터미널에 표시되지 않음)
        password = getpass.getpass(
            f"Enter your GPG password (Attempt {attempts + 1}/{max_attempts}): "
        )

        # gpg --export-secret-keys 명령을 사용해 개인 키를 추출
        result = subprocess.run(
            [
                "gpg",
                "--pinentry-mode",
                "loopback",
                "--passphrase",
                password,
                "--export-secret-keys",
                "--armor",
                key_id,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # 비밀번호가 맞는 경우, 개인 키를 파일로 저장
        if result.returncode == 0:
            with open("my_private_key.asc", "w") as f:
                f.write(result.stdout)
            print(
                "\033[92mPrivate key successfully exported to my_private_key.asc.\033[0m"
            )
            return True

        # 비밀번호가 맞지 않는 경우
        print("\033[91mWrong password.\033[0m")
        attempts += 1

    # 시도 횟수를 초과한 경우
    print("\033[91mMaximum attempts exceeded. Private key was not exported.\033[0m")
    return False


def main():
    # 사용자로부터 이메일 입력받기 (엔터를 누르면 입력 종료)
    print("Enter the GPG email address. Press Enter when finished.")
    email = sys.stdin.readline().strip()

    # 해당 이메일로 GPG 키 검색
    key_id = get_gpg_key_by_email(email)

    if key_id:
        print(f"Found GPG key: {key_id}")

        # 키 ID를 사용해 개인 키 추출
        success = export_private_key(key_id)

        if not success:
            print("Failed to export private key.")
    else:
        print("\033[91mNo GPG key found for the provided email.\033[0m")


if __name__ == "__main__":
    main()
