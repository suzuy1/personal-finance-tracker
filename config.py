import os

class Config:
    # Pakai SQLite lokal, langsung otomatis bikin file 'finance.db' di folder lo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///finance.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ganti-dengan-string-random-yang-panjang-untuk-keamanan-2024'
    
    # Pengaturan keamanan session
    SESSION_COOKIE_SECURE = False  # Set True jika pakai HTTPS
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 1800  # 30 menit
