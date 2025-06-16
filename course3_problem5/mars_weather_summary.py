import pymysql
import csv
import os

# MySQL 연결 설정
conn = pymysql.connect(
    host='localhost',
    user='root',      
    password='987548',
    database='mars',
    charset='utf8mb4',
    autocommit=True
)
cursor = conn.cursor()

# CSV 파일 읽기
with open(os.path.join(os.path.dirname(__file__), 'mars_weathers_data.CSV'), newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        mars_date = row['mars_date']
        temp = int(float(row['temp'])) if row['temp'] else None
        stom = int(row['stom']) if row['stom'] else None

        print(f"mars_date: {mars_date}, temp: {temp}, stom: {stom}")

        sql = """
            INSERT INTO mars_weather (mars_date, temp, stom)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (mars_date, temp, stom))

print("✅ 데이터 삽입 완료")
cursor.close()
conn.close()
