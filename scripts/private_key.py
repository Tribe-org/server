import os
import subprocess

from dotenv import load_dotenv

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()

# 환경 변수에서 GPG 비밀번호와 이메일을 가져옵니다.
GPG_EMAIL = os.getenv("GPG_EMAIL")
GPG_PASSWORD = os.getenv("GPG_PASSWORD")


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
    if not GPG_PASSWORD:
        print("\033[91mError: GPG_PASSWORD environment variable is not set.\033[0m")
        return False

    try:
        # gpg --export-secret-keys 명령을 사용해 개인 키를 추출
        result = subprocess.run(
            [
                "gpg",
                "--pinentry-mode",
                "loopback",
                "--passphrase",
                GPG_PASSWORD,
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

        # 비밀번호가 맞지 않거나 다른 문제가 발생한 경우
        print(f"\033[91mError exporting private key: {result.stderr}\033[0m")
        return False

    except Exception as e:
        print(f"\033[91mAn error occurred: {e}\033[0m")
        return False


def main():
    # 환경변수에서 이메일을 불러옵니다.
    if not GPG_EMAIL:
        print("\033[91mError: GPG_EMAIL environment variable is not set.\033[0m")
        return

    print(
        f"\033[94mStarting the process to extract the necessary private key for the project using email: {GPG_EMAIL}...\033[0m"
    )

    # 해당 이메일로 GPG 키 검색
    key_id = get_gpg_key_by_email(GPG_EMAIL)

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
