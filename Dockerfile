# ใช้ Python 3.12 slim image เป็น base image
FROM python:3.12-slim

# ตั้งค่า directory ที่ทำงานใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt ไปยัง /app
COPY ./requirements.txt /app

# ติดตั้ง dependencies ที่ระบุใน requirements.txt
RUN pip install -r requirements.txt

# คัดลอกไฟล์ทั้งหมดจาก directory ปัจจุบันไปยัง /app
COPY . .

# เปิดพอร์ต 8011 สำหรับแอป Flask
EXPOSE 8011

# คำสั่งเริ่มต้นที่รัน Flask app และระบุพอร์ตที่ใช้
CMD ["flask", "run", "--host=0.0.0.0", "--port=8011"]
