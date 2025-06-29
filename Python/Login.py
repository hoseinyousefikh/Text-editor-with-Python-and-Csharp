import pyodbc
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

# تنظیمات اتصال به سرور SQL
SERVER_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': 'DESKTOP-IPNPIA8',
    'trusted_connection': 'yes',
    'encrypt': 'yes',
    'trust_server_certificate': 'yes'
}

# نام دیتابیس مورد نظر
DATABASE_NAME = 'PYTHONLOGIN'

# تنظیمات JWT
JWT_SECRET = "YourSuperSecretKeyHereAtLeast32Characters"  # باید با سی شارپ مشترک باشد
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60  # زمان انقضای توکن (دقیقه)

# تابع ایجاد اتصال به سرور (بدون دیتابیس خاص)
def get_server_connection():
    conn_str = f"""
        DRIVER={{{SERVER_CONFIG['driver']}}};
        SERVER={SERVER_CONFIG['server']};
        Trusted_Connection={SERVER_CONFIG['trusted_connection']};
        Encrypt={SERVER_CONFIG['encrypt']};
        TrustServerCertificate={SERVER_CONFIG['trust_server_certificate']};
    """
    return pyodbc.connect(conn_str, autocommit=True)

# تابع ایجاد اتصال به دیتابیس خاص
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

# تابع ایجاد دیتابیس (در صورت عدم وجود)
def create_database():
    try:
        with get_server_connection() as conn:
            cursor = conn.cursor()
            
            # بررسی وجود دیتابیس
            cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{DATABASE_NAME}'")
            if not cursor.fetchone():
                # ایجاد دیتابیس جدید
                cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
                print(f"دیتابیس '{DATABASE_NAME}' با موفقیت ایجاد شد")
            else:
                print(f"دیتابیس '{DATABASE_NAME}' از قبل وجود دارد")
                
    except Exception as e:
        print(f"خطا در ایجاد دیتابیس: {str(e)}")

# تابع ایجاد جداول در دیتابیس
def create_tables():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # ایجاد جدول کاربران
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
            CREATE TABLE Users (
                UserID INT IDENTITY(1,1) PRIMARY KEY,
                FirstName NVARCHAR(50) NOT NULL,
                LastName NVARCHAR(50) NOT NULL,
                Age INT NOT NULL,
                PhoneNumber NVARCHAR(20) NOT NULL,
                Address NVARCHAR(255) NOT NULL,
                Email NVARCHAR(100) UNIQUE NOT NULL,
                PasswordHash VARBINARY(128) NOT NULL,
                CreatedAt DATETIME DEFAULT GETDATE()
            )
            """)
            
            # ایجاد جدول لاگین‌ها
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Logins' AND xtype='U')
            CREATE TABLE Logins (
                LoginID INT IDENTITY(1,1) PRIMARY KEY,
                UserID INT NOT NULL,
                LoginTime DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (UserID) REFERENCES Users(UserID)
            )
            """)
            
            conn.commit()
            print("جداول با موفقیت ایجاد شدند")
    except Exception as e:
        print(f"خطا در ایجاد جداول: {str(e)}")

# تابع هش کردن رمز عبور
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# تابع بررسی تطابق رمز عبور
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

# تابع تولید توکن JWT
def generate_jwt_token(user_id):
    """تولید توکن JWT برای کاربر"""
    payload = {
        'sub': user_id,  # شناسه کاربر
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES),
        'iat': datetime.utcnow(),  # زمان ایجاد توکن
        'iss': 'python-auth-service'  # صادرکننده توکن
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# ====================
# مسیرهای API
# ====================

@app.route('/register', methods=['POST'])
def register():
    data = request.json
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
    data = request.json
    
    # اعتبارسنجی فیلدهای اجباری
    if 'email' not in data or 'password' not in data:
        return jsonify({'error': 'ایمیل و رمز عبور الزامی هستند'}), 400
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # دریافت اطلاعات کاربر
            cursor.execute("""
            SELECT UserID, PasswordHash 
            FROM Users 
            WHERE Email = ?
            """, data['email'])
            
            user = cursor.fetchone()
            if not user:
                return jsonify({'error': 'کاربری با این ایمیل یافت نشد'}), 404
            
            # بررسی رمز عبور
            if not check_password(user.PasswordHash, data['password']):
                return jsonify({'error': 'رمز عبور نادرست است'}), 401
            
            # ثبت زمان لاگین
            cursor.execute("""
            INSERT INTO Logins (UserID) 
            VALUES (?)
            """, user.UserID)
            
            conn.commit()
            
            # تولید توکن JWT
            token = generate_jwt_token(user.UserID)
            
            return jsonify({
                'message': 'ورود به سیستم موفقیت آمیز بود',
                'token': token
            }), 200
    
    except Exception as e:
        return jsonify({'error': f'خطای سرور: {str(e)}'}), 500

# ====================
# اجرای برنامه
# ====================
if __name__ == '__main__':
    # ایجاد دیتابیس و جداول به صورت خودکار
    create_database()
    create_tables()
    
    # اجرای سرور با HTTPS
    app.run(debug=True, ssl_context='adhoc', port=5000)