from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ----------------------------------------------------
# 1. ENKAPSULASI: Class User dengan Private/Protected Attribute
# ----------------------------------------------------
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _balance = db.Column('balance', db.Numeric(15, 2), default=0.0) # Protected field

    # Getter untuk Balance (Encapsulation)
    @property
    def balance(self):
        return float(self._balance)

    # Setter untuk Modifikasi Saldo dengan Validasi Bisnis
    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Enterprise Alert: Saldo tidak boleh negatif!")
        self._balance = amount

# ----------------------------------------------------
# 2. INHERITANCE: Parent Class untuk Pola Transaksi
# ----------------------------------------------------
class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20)) # Discriminator untuk polimorfisme

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'transaction'
    }

    # POLIMORFISME: Method abstrak yang akan di-override oleh Child Class
    def execute_financial_logic(self, current_balance):
        raise NotImplementedError("Method wajib diimplementasi di subclass!")

# ----------------------------------------------------
# 3. POLYMORPHISM: Child Class dengan Override Logika Bisnis Berbeda
# ----------------------------------------------------
class Income(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'income'}

    def execute_financial_logic(self, current_balance):
        # Pemasukan sifatnya menambahkan saldo keseluruhan
        return current_balance + float(self.amount)

class Expense(Transaction):
    __mapper_args__ = {'polymorphic_identity': 'expense'}

    def execute_financial_logic(self, current_balance):
        # Pengeluaran sifatnya mengurangi saldo, lakukan validasi limit di sini
        if current_balance < float(self.amount):
            raise ValueError("Saldo Anda tidak mencukupi untuk melakukan pengeluaran ini!")
        return current_balance - float(self.amount)