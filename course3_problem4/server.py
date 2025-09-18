from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

PORT = 8080

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # index.html 파일 읽기
        try:
            with open("index.html", "rb") as f:
                content = f.read()

            # 응답 코드 200 전송
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content)

            # 서버 쪽 로그 출력 (접속 시간 & IP 주소)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_ip = self.client_address[0]
            print(f"[{now}] 클라이언트 접속: {client_ip}")

        except FileNotFoundError:
            # index.html이 없는 경우 404 반환
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")

# 서버 실행
if __name__ == "__main__":
    server = HTTPServer(("", PORT), MyHandler)
    print(f"HTTP 서버가 {PORT}번 포트에서 시작되었습니다.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
        server.server_close()
