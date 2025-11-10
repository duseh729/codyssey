#!/usr/bin/env python3
from socket import *
import threading
import sys

IP = "127.0.0.1"
PORT = 12345

def recv_loop(sock: socket) -> None:
    """서버에서 오는 메시지를 계속 수신"""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("서버 연결이 종료되었습니다.")
                break
            print(data.decode("utf-8") + "\n> ", end="")
    except OSError:
        pass
    finally:
        sock.close()

def send_loop(sock: socket) -> None:
    """사용자 입력을 계속 전송"""
    try:
        while True:
            msg = input("> ")
            if not msg:
                continue
            sock.sendall(msg.encode("utf-8"))
            if msg == "/종료":          # 종료 명령어
                break
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        try:
            sock.shutdown(SHUT_RDWR)
        except OSError:
            pass
        sock.close()

def main() -> None:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print(f"서버({IP}:{PORT})에 연결되었습니다. '/종료' 입력 시 종료됩니다.")

    # 서버 메시지 수신 스레드
    threading.Thread(target=recv_loop, args=(client_socket,), daemon=True).start()

    # 메인 스레드에서 송신 루프
    send_loop(client_socket)

if __name__ == "__main__":
    main()
