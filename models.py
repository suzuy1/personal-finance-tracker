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
    
    # KOLOM BARU: Batas Anggaran Pengeluaran (Default: Rp 5 Juta)
    budget_limit = db.Column(db.Numeric(15, 2), default=5000000.0)

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
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'income' atau 'expense'
    icon = db.Column(db.String(10), default='📦')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL = default, ada value = custom user
    is_default = db.Column(db.Boolean, default=False)
    
    # Relationship
    user = db.relationship('User', backref='custom_categories')
    
    def __repr__(self):
        return f'<Category {self.icon} {self.name}>'


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20)) # Kolom pembeda kelas (discriminator)

    # Relationship
    category = db.relationship('Category', backref='transactions')

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
