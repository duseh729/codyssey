# sendmail.py
import smtplib
from email.mime.text import MIMEText
import os

def send_mail():
    try:
        # 1. SMTP 서버 정보
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # 2. 사용자 정보
        sender_email = os.getenv('EMAIL_ADDRESS')
        receiver_email = "보내고 싶은 이메일 작성"
        password = os.getenv('EMAIL_PASSWORD')

        # 3. 메일 내용 작성
        subject = '테스트 메일'
        body = '안녕하세요. Python SMTP를 이용한 테스트 메일입니다.'

        # 4. MIMEText 객체 생성
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # 5. 서버 연결 및 로그인
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # TLS 암호화 시작
        server.login(sender_email, password)

        # 6. 메일 전송
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print('메일이 성공적으로 전송되었습니다.')

    except smtplib.SMTPAuthenticationError:
        print('로그인 실패: 이메일 또는 비밀번호를 확인하세요.')
    except smtplib.SMTPConnectError:
        print('서버 연결 실패: 네트워크 상태를 확인하세요.')
    except Exception as e:
        print('메일 전송 중 오류 발생:', e)
    finally:
        server.quit()

if __name__ == '__main__':
    send_mail()
