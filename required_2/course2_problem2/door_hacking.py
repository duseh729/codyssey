import zipfile
import time
import os

def unlock_zip():
    zip_filename = os.path.join(os.path.dirname(__file__), "emergency_storage_key.zip")
    charset = [chr(c) for c in range(ord('a'), ord('z') + 1)] + [str(d) for d in range(10)]
    # charset = ['m', 'a', 'r', 's', '0', '6']
    max_length = 6
    total = len(charset) ** max_length

    try:
        with zipfile.ZipFile(zip_filename) as zf:
            print(f"[+] ZIP 파일 '{zip_filename}'을(를) 열었습니다.")
            start_time = time.time()
            attempts = 0

            for i in range(total):
                password = number_to_password(i, charset, max_length)
                attempts += 1

                try:
                    zf.setpassword(bytes(password, 'utf-8'))
                    if zf.testzip() is None:  # 암호가 맞으면 None 반환
                        elapsed = time.time() - start_time
                        print(f"\n[✓] 암호 찾음: {password}")
                        print(f"[✓] 시도 횟수: {attempts}")
                        print(f"[✓] 소요 시간: {elapsed:.2f}초")

                        with open(os.path.join(os.path.dirname(__file__), "password.txt"), "w") as f:
                            f.write(password)

                        return
                except:
                    pass

                elapsed = time.time() - start_time
                print(f"[{attempts}회 시도 중] 경과 시간: {elapsed:.2f}초")

            print("[-] 암호를 찾지 못했습니다.")

    except FileNotFoundError:
        print(f"[-] 파일 '{zip_filename}'이(가) 존재하지 않습니다.")

def number_to_password(num, charset, length):
    base = len(charset)
    password = ""
    for _ in range(length):
        password = charset[num % base] + password
        num //= base
    return password.zfill(length)  # 앞에 0 채움

def caesar_cipher_decode(target_text):
    print("\n[!] 카이사르 복호화 시작 (0~25 shift 시도)\n")
    decoded_results = []

    for shift in range(26):
        decoded = ""
        for char in target_text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded += chr((ord(char) - base - shift) % 26 + base)
            else:
                decoded += char
        print(f"{shift:2d}: {decoded}")
        decoded_results.append(decoded)

    while True:
        try:
            index = int(input("\n[?] 해독된 문장이 보이는 shift 번호를 입력하세요: "))
            if 0 <= index < 26:
                result = decoded_results[index]
                with open(os.path.join(os.path.dirname(__file__), "result.txt"), "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"[✓] 결과를 'result.txt'에 저장했습니다.")
                break
            else:
                print("[-] 0부터 25 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("[-] 숫자를 입력해주세요.")

if __name__=="__main__":
    # unlock_zip()
    password_path = os.path.join(os.path.dirname(__file__), "password.txt")
    if os.path.exists(password_path):
        with open(password_path, "r", encoding="utf-8") as f:
            encrypted_text = f.read().strip()
        caesar_cipher_decode(encrypted_text)