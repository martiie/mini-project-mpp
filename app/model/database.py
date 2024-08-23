import firebase_admin
from firebase_admin import credentials, firestore
import os 
file_path = os.path.join(os.getcwd(), 'app/model/API_keys_db.json')
cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_document(collection_name, document_id, data):
    """
    เพิ่มเอกสารใหม่ในคอลเลกชัน
    """
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    print(f'Document added with ID: {document_id}')

def primary_keys(collection_name):
    return str(db.collection('users').add({}).id) 

def get_all_documents(collection_name, asc=True):
    """
    ดึงเอกสารทั้งหมดจากคอลเลกชัน
    """
    docs = db.collection(collection_name).stream()
    result = []
    for doc in docs:
        doc_id = doc.id  # Firestore document IDs are alphanumeric strings
        doc_data = doc.to_dict()
        try:
            result.append({'id': int(doc_id), **doc_data})  # Keep doc_id as a string
        except:
            delete_document(collection_name, doc_id)
    result.sort(key=lambda x: x['id'], reverse=not asc)
    return result

def update_document(collection_name, document_id, updates):
    """
    อัปเดตเอกสารในคอลเลกชัน
    """
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.update(updates)
    print(f'Document {document_id} updated')

def delete_document(collection_name, document_id):
    """
    ลบเอกสารจากคอลเลกชัน
    """
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.delete()
    print(f'Document {document_id} deleted')

def delete_all_documents(collection_name):
    """
    ลบเอกสารทั้งหมดจากคอลเลกชัน
    """
    # Get a reference to the collection
    collection_ref = db.collection(collection_name)
    
    # Get all documents in the collection
    docs = collection_ref.stream()
    
    # Iterate over the documents and delete each one
    for doc in docs:
        doc.reference.delete()
        print(f'Document {doc.id} deleted')
    
    print(f'All documents in collection {collection_name} deleted')


# def get_paginated_documents(collection_name, page_size, page_number):
#     """
#     ดึงข้อมูลที่แบ่งหน้า
#     :param collection_name: ชื่อของคอลเลกชัน
#     :param page_size: ขนาดของแต่ละหน้า
#     :param page_number: หมายเลขหน้าที่ต้องการ (เริ่มจาก 1)
#     :return: ข้อมูลที่ดึงมา
#     """
#     collection_ref = db.collection(collection_name)
    
#     # คำนวณเอกสารที่ควรข้ามไป
#     start_after = (page_number - 1) * page_size

#     # เริ่มต้นการดึงข้อมูล
#     docs = collection_ref.limit(start_after + page_size).offset(start_after).stream()
    
#     results = []
#     for doc in docs:
#         results.append(doc.to_dict())
    
#     return results

def get_paginated_documents(collection_name, page_size=10, page_number=1, asc=True):
    """
    ดึงข้อมูลที่แบ่งหน้า จากผลลัพธ์ที่จัดเรียงแล้ว
    :param collection_name: ชื่อของคอลเลกชัน
    :param page_size: ขนาดของแต่ละหน้า
    :param page_number: หมายเลขหน้าที่ต้องการ (เริ่มจาก 1)
    :param asc: การจัดเรียงแบบเพิ่มขึ้น (True) หรือ ลดลง (False)
    :return: ข้อมูลที่ดึงมา
    """
    all_docs = get_all_documents(collection_name, asc)
    
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    
    paginated_docs = all_docs[start_index:end_index]
    
    return paginated_docs


def get_sorted_documents(collection_name, field_name, ascending=True):
    """
    ดึงเอกสารทั้งหมดจากคอลเลกชันและเรียงตามฟิลด์
    :param collection_name: ชื่อของคอลเลกชัน
    :param field_name: ชื่อฟิลด์ที่ใช้ในการเรียงข้อมูล
    :param ascending: เรียงจากน้อยไปมาก ถ้า False จะเรียงจากมากไปน้อย
    :return: ข้อมูลที่ดึงมา
    """
    collection_ref = db.collection(collection_name)
    query = collection_ref.order_by(field_name, direction='ASCENDING' if ascending else 'DESCENDING')
    docs = query.stream()
    
    results = []
    for doc in docs:
        results.append(doc.to_dict())
    
    return results

def get_euqual_documents(collection_name, field_name, value):
    """
    ดึงเอกสารที่มีค่าของฟิลด์ตรงกับค่าที่กำหนด
    :param collection_name: ชื่อของคอลเลกชัน
    :param field_name: ชื่อฟิลด์ที่ใช้ในการกรองข้อมูล
    :param value: ค่าที่ใช้กรองข้อมูล
    :return: ข้อมูลที่ดึงมา
    """
    collection_ref = db.collection(collection_name)
    query = collection_ref.where(field_name, '==', value)
    docs = query.stream()
    
    results = []
    for doc in docs:
        results.append(doc.to_dict())
    
    return results

def get_documents_in_range(collection_name, field_name, min_value, max_value, ascending=False):
    """
    ดึงเอกสารที่มีค่าของฟิลด์อยู่ในช่วงที่กำหนด
    :param collection_name: ชื่อของคอลเลกชัน
    :param field_name: ชื่อฟิลด์ที่ใช้ในการกรองข้อมูล
    :param min_value: ค่าต่ำสุดของช่วง
    :param max_value: ค่าสูงสุดของช่วง
    :return: ข้อมูลที่ดึงมา
    """
    collection_ref = db.collection(collection_name)
    query = collection_ref.where(field_name, '>=', min_value).where(field_name, '<=', max_value)
    query = query.order_by(field_name, direction='ASCENDING' if ascending else 'DESCENDING')
    docs = query.stream()
    
    results = []
    for doc in docs:
        results.append(doc.to_dict())
    
    return results

