from socket import *
import threading

HOST, PORT = "127.0.0.1", 12345
clients = []                  # 접속된 소켓 저장
clients_lock = threading.Lock()

def broadcast(message: str, sender: socket) -> None:
    """연결된 모든 클라이언트에게 메시지 전송"""
    data = message.encode("utf-8")
    with clients_lock:
        dead = []
        for c in clients:
            if c is sender:
                continue
            try:
                c.sendall(data)
            except OSError:
                dead.append(c)
        for c in dead:
            clients.remove(c)
            c.close()

def handle_client(conn: socket, addr: tuple[str, int]) -> None:
    print(f"{addr} 에서 접속했습니다.")
    with clients_lock:
        clients.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8").strip()
            print(f"{addr} >> {msg}")
            # 내 메시지를 전체 클라이언트에 뿌림
            broadcast(f"{addr} >> {msg}", sender=conn)
    except ConnectionResetError:
        print(f"{addr} 연결이 비정상 종료")
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"{addr} 연결을 닫았습니다.")

def main() -> None:
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"서버가 {HOST}:{PORT} 에서 대기 중입니다...")

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n서버 종료")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
