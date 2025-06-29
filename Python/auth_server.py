import pyodbc
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# تنظیمات اتصال به SQL Server
SERVER_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': 'DESKTOP-IPNPIA8',
    'trusted_connection': 'yes',
    'encrypt': 'yes',
    'trust_server_certificate': 'yes'
}

DATABASE_NAME = 'PYTHONLOGIN'
JWT_SECRET = "YourSuperSecretKeyHereAtLeast32Characters"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

# Claim Type برای شناسه کاربر
NAME_IDENTIFIER_CLAIM = "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"

def get_db_connection():
    conn_str = f"""
        DRIVER={{{SERVER_CONFIG['driver']}}};
        SERVER={SERVER_CONFIG['server']};
        DATABASE={DATABASE_NAME};
        Trusted_Connection={SERVER_CONFIG['trusted_connection']};
        Encrypt={SERVER_CONFIG['encrypt']};
        TrustServerCertificate={SERVER_CONFIG['trust_server_certificate']};
    """
    return pyodbc.connect(conn_str)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def generate_jwt_token(user_id):
    payload = {
        'sub': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES),
        'iat': datetime.utcnow(),
        'iss': 'python-auth-service',
        # اضافه کردن claim مورد نیاز برای سی شارپ
        NAME_IDENTIFIER_CLAIM: str(user_id)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = [
        'first_name', 'last_name', 'age', 
        'phone', 'address', 'email', 
        'password', 'confirm_password'
    ]
    
    # اعتبارسنجی فیلدهای اجباری
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'فیلد {field} الزامی است'}), 400
    
    # اعتبارسنجی ایمیل
    if '@' not in data['email']:
        return jsonify({'error': 'فرمت ایمیل نامعتبر است'}), 400
    
    # اعتبارسنجی تطابق رمز عبور
    if data['password'] != data['confirm_password']:
        return jsonify({'error': 'رمز عبور و تکرار آن مطابقت ندارند'}), 400
    
    # اعتبارسنجی طول رمز عبور
    if len(data['password']) < 8:
        return jsonify({'error': 'رمز عبور باید حداقل ۸ کاراکتر باشد'}), 400
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # بررسی تکراری نبودن ایمیل
            cursor.execute("SELECT Email FROM Users WHERE Email = ?", data['email'])
            if cursor.fetchone():
                return jsonify({'error': 'این ایمیل قبلاً ثبت شده است'}), 400
            
            # هش کردن رمز عبور
            hashed_password = hash_password(data['password'])
            
            # ذخیره کاربر در دیتابیس
            cursor.execute("""
            INSERT INTO Users (
                FirstName, LastName, Age, 
                PhoneNumber, Address, 
                Email, PasswordHash
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data['first_name'],
                data['last_name'],
                data['age'],
                data['phone'],
                data['address'],
                data['email'],
                hashed_password
            ))
            
            conn.commit()
            return jsonify({'message': 'ثبت نام با موفقیت انجام شد'}), 201
    
    except Exception as e:
        return jsonify({'error': f'خطای سرور: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'ایمیل و رمز عبور الزامی هستند'}), 400
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT UserID, PasswordHash FROM Users WHERE Email = ?", data['email'])
            user = cursor.fetchone()
            
            if not user:
                return jsonify({'error': 'کاربری با این ایمیل یافت نشد'}), 404
            
            if not check_password(user.PasswordHash, data['password']):
                return jsonify({'error': 'رمز عبور نادرست است'}), 401
            
            cursor.execute("INSERT INTO Logins (UserID) VALUES (?)", user.UserID)
            conn.commit()
            
            token = generate_jwt_token(user.UserID)
            return jsonify({
                'message': 'ورود به سیستم موفقیت آمیز بود',
                'token': token,
                'user_id': user.UserID  # اضافه کردن user_id به پاسخ
            }), 200
    
    except Exception as e:
        return jsonify({'error': f'خطای سرور: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)