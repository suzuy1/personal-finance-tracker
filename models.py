from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ====================================================
# 1. ENKAPSULASI: Class User dengan Protected Atribut
# ====================================================
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # Kolom baru untuk password terenkripsi
    _balance = db.Column('balance', db.Numeric(15, 2), default=0.0) # Protected field

    # Getter untuk mengambil saldo dengan aman
    @property
    def balance(self):
        return float(self._balance)

    # Setter untuk memodifikasi saldo dengan validasi bisnis murni
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Sistem Enterprise: Saldo akun tidak boleh negatif!")
        self._balance = amount

    # Helper Method OOP untuk Enkapsulasi Keamanan Password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ====================================================
# 2. INHERITANCE: Parent Class untuk Skema Transaksi
# ====================================================
class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20)) # Kolom pembeda kelas (discriminator)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'transaction'
    }

    # POLYMORPHISM: Method abstract yang wajib di-override di subclass anak
    def execute_financial_logic(self, current_balance):
        raise NotImplementedError("Subclass wajib mengimplementasikan fungsi logika keuangan ini!")

    # POLYMORPHISM: Method abstract untuk membalikkan efek finansial transaksi yang dihapus
    def execute_reverse_logic(self, current_balance):
        raise NotImplementedError("Subclass wajib mengimplementasikan fungsi logika pembalikan ini!")


# ====================================================
# 3. POLYMORPHISM: Subclass Anak (Income & Expense)
# ====================================================
class Income(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'income'}

    def execute_financial_logic(self, current_balance):
        # Polimorfisme: Income mengembalikan hasil pertambahan saldo
        return current_balance + float(self.amount)

    def execute_reverse_logic(self, current_balance):
        # Polimorfisme: Jika pemasukan dihapus, saldo dikurangi.
        # Validasi agar pembatalan pemasukan tidak membuat saldo akhir menjadi negatif.
        new_balance = current_balance - float(self.amount)
        if new_balance < 0:
            raise ValueError("Pembatalan pemasukan dibatalkan: Saldo tidak boleh negatif setelah dikurangi!")
        return new_balance


class Expense(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'expense'}

    def execute_financial_logic(self, current_balance):
        # Polimorfisme: Expense melakukan validasi limit lalu mengurangi saldo
        if current_balance < float(self.amount):
            raise ValueError("Saldo Anda tidak mencukupi untuk memproses pengeluaran ini!")
        return current_balance - float(self.amount)

    def execute_reverse_logic(self, current_balance):
        # Polimorfisme: Jika pengeluaran dihapus, saldo dikembalikan (ditambah)
        return current_balance + float(self.amount)