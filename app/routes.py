from app import app
from flask import render_template, request,redirect, url_for
from app.model import database as db
# import pymysql
# def conDB():
#     return pymysql.connect(
#             host='sql.freedb.tech',
#             port=3306,
#             user='freedb_TOPCMU',
#             password='#6apSzfG!!wjq@T',
#             database='freedb_MPP001',
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/show')
def show():
    page_size = 10 
    page_number = int(request.args.get('page', 1)) 

    rows = db.get_paginated_documents('users', page_size, page_number)
    total_docs = len(db.get_all_documents('users'))
    total_pages = (total_docs + page_size - 1) // page_size

    has_previous = page_number > 1
    has_next = page_number < total_pages
    
    return render_template('show.html', rows=rows, page_number=page_number, has_previous=has_previous, has_next=has_next)

@app.route('/add_user_page', methods=['GET', 'POST'])
def add_user_page():

    return render_template('adduser.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        email = request.form['email']
        
        doc_id = str(len(db.get_all_documents('users'))+1)
        
        db.add_document('users', doc_id, {
            'name': name,
            'age': age,
            'email': email
        })
        
        return redirect(url_for('show'))  # Redirect to another route (e.g., show user list)
    
    return render_template('index.html')

@app.route('/delete_all')
def delete_all():
    db.delete_all_documents('users')
    return render_template('index.html')
# @app.route('/show')
# def show():
#     conn = conDB()
#     cursor = conn.cursor()
#     # ดึงข้อมูลทั้งหมดจากตาราง test001
#     select_query = "SELECT * FROM test001"
#     cursor.execute(select_query)
#     # ดึงข้อมูลทั้งหมดจากผลลัพธ์
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     # print(rows)
#     # ส่งข้อมูลไปยังเทมเพลต
#     return render_template('show.html', rows=rows)
