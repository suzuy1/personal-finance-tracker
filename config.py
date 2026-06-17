import os

class Config:
    # Pakai SQLite lokal, langsung otomatis bikin file 'finance.db' di folder lo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///finance.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'rahasia-kelompok-lima'