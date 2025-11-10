import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import csv
import os

# .env 로드 (EMAIL_ADDRESS, EMAIL_PASSWORD 포함)
load_dotenv()

# =============================
# 설정
# =============================
CSV_FILE = 'mail_target_list.csv'
print(f'📄 대상 파일: {CSV_FILE}')
USE_NAVER = False  # True면 네이버 SMTP 사용, False면 Gmail SMTP 사용

# SMTP 서버 정보
# =============================
if USE_NAVER:
    smtp_server = 'smtp.naver.com'
    smtp_port = 587
else:
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

# =============================
# 사용자 정보
# =============================
sender_email = os.getenv('EMAIL_ADDRESS')
password = os.getenv('EMAIL_PASSWORD')

# =============================
# 메일 내용 (HTML)
# =============================
subject = '안녕하세요! Python으로 보내는 HTML 메일입니다.'
html_body = """
<html>
  <body>
    <h2 style="color:#2F855A;">Python SMTP 메일 테스트</h2>
    <p>안녕하세요, <b>{name}</b>님!</p>
    <p>이 메일은 <span style="color:blue;">HTML 형식</span>으로 전송되었습니다.</p>
    <hr>
    <p>감사합니다.<br>Python SMTP 드림 🐍</p>
  </body>
</html>
"""

# =============================
# CSV 읽기
# =============================
def read_mail_targets(csv_file):
    targets = []
    with open(csv_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['이름'].strip()
            email = row['이메일'].strip()
            targets.append((name, email))
    return targets

# =============================
# 메일 전송 함수 (1명씩)
# =============================
def send_mail_individual(targets):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        for name, email in targets:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = email

            body = html_body.format(name=name)
            msg.attach(MIMEText(body, 'html', 'utf-8'))

            server.sendmail(sender_email, email, msg.as_string())
            print(f'✅ {name}({email}) 에게 메일 전송 완료')

    except smtplib.SMTPAuthenticationError:
        print('❌ 로그인 실패: 이메일 또는 비밀번호를 확인하세요.')
    except smtplib.SMTPConnectError:
        print('❌ 서버 연결 실패: 네트워크 상태를 확인하세요.')
    except Exception as e:
        print('❌ 오류 발생:', e)
    finally:
        server.quit()

# =============================
# 메일 전송 함수 (한 번에 여러명)
# =============================
def send_mail_batch(targets):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = ', '.join([email for _, email in targets])

        body = html_body.format(name='모든 수신자')
        msg.attach(MIMEText(body, 'html', 'utf-8'))

        server.sendmail(sender_email, [email for _, email in targets], msg.as_string())
        print(f'✅ 전체 {len(targets)}명에게 메일 일괄 전송 완료')

    except Exception as e:
        print('❌ 오류 발생:', e)
    finally:
        server.quit()

# =============================
# 메인 실행
# =============================
if __name__ == '__main__':
    targets = read_mail_targets(CSV_FILE)
    print(f'📋 {len(targets)}명의 대상 로드 완료')

    # (1) 한 명씩 반복 전송
    send_mail_individual(targets)

    # (2) 또는 한 번에 일괄 전송
    # send_mail_batch(targets)
