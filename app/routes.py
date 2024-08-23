from app import app
from flask import render_template
import pymysql
def conDB():
    return pymysql.connect(
            host='sql.freedb.tech',
            port=3306,
            user='freedb_TOPCMU',
            password='#6apSzfG!!wjq@T',
            database='freedb_MPP001',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/show')
def show():
    conn = conDB()
    cursor = conn.cursor()
    # ดึงข้อมูลทั้งหมดจากตาราง test001
    select_query = "SELECT * FROM test001"
    cursor.execute(select_query)
    # ดึงข้อมูลทั้งหมดจากผลลัพธ์
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(rows)
    # ส่งข้อมูลไปยังเทมเพลต
    return render_template('show.html', rows=rows)
