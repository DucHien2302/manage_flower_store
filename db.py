import mysql.connector
import uuid

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='doanpython'  # Đảm bảo đúng tên database
    )

def get_cart_id(user_id):
    # Sinh CartId duy nhất cho mỗi user (có thể dùng user_id dạng chuỗi hoặc hash)
    return str(user_id)  # Đơn giản hóa: dùng user_id làm CartId
