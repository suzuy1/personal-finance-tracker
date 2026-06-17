from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Income, Expense, Transaction
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# TRIGGER AUTOMATIC DB GENERATION & DUMMY SEEDER
@app.before_request
def initialize_database():
    # Membuat tabel otomatis di cloud Supabase jika belum ada
    db.create_all()
    
    # Membuat user dummy otomatis untuk keperluan demo login
    if not User.query.filter_by(email="oriza@ubbg.ac.id").first():
        demo_user = User(username="Oriza", email="oriza@ubbg.ac.id")
        demo_user.balance = 12500000 # Mengeset nominal awal via Setter Enkapsulasi
        db.session.add(demo_user)
        db.session.commit()

# [READ] - Controller Dashboard Utama
@app.route('/')
@app.route('/dashboard')
def dashboard():
    current_user = User.query.filter_by(email="oriza@ubbg.ac.id").first()
    
    # Mengambil transaksi real-time dari Supabase khusus milik user ini
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
    
    return render_template('dashboard.html', user=current_user, transactions=user_transactions)

# [CREATE] - Controller Tambah Transaksi (Logika Polimorfisme Beraksi)
@app.route('/transaction/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        current_user = User.query.filter_by(email="oriza@ubbg.ac.id").first()
        
        tx_type = request.form.get('type') # 'income' atau 'expense'
        amount = float(request.form.get('amount'))
        category = request.form.get('category_id')
        description = request.form.get('description')

        try:
            # Polimorfisme: Membuat instance objek kelas secara dinamis sesuai pilihan form
            if tx_type == 'income':
                new_tx = Income(user_id=current_user.id, amount=amount, category=category, description=description)
            elif tx_type == 'expense':
                new_tx = Expense(user_id=current_user.id, amount=amount, category=category, description=description)
            else:
                return "Tipe transaksi tidak valid", 400

            # Eksekusi kalkulasi saldo lewat pilar Polimorfisme
            new_balance = new_tx.execute_financial_logic(current_user.balance)
            
            # Update data internal user via Setter Enkapsulasi
            current_user.balance = new_balance
            
            # Commit data ke server cloud Supabase secara atomik
            db.session.add(new_tx)
            db.session.commit()
            
            return redirect(url_for('dashboard'))

        except ValueError as e:
            db.session.rollback()
            return f"Gagal memproses logika bisnis: {str(e)}", 400

    return render_template('transaction_form.html')

# [DELETE] - Controller Hapus Transaksi dengan OOP Polymorphic Reverse Logic & Otorisasi
@app.route('/transaction/delete/<int:tx_id>')
def delete_transaction(tx_id):
    current_user = User.query.filter_by(email="oriza@ubbg.ac.id").first()
    
    # Cari transaksi berdasarkan ID, jika tidak ditemukan langsung return 404
    tx = Transaction.query.get_or_404(tx_id)
    
    # Keamanan Enterprise: Validasi kepemilikan transaksi (Mencegah IDOR)
    if tx.user_id != current_user.id:
        flash("Keamanan Enterprise: Anda tidak memiliki otorisasi untuk menghapus transaksi ini!", "danger")
        return redirect(url_for('dashboard'))
    
    try:
        # PBO/Business Logic: Eksekusi pembalikan saldo secara polimorfik lewat objek transaksi
        new_balance = tx.execute_reverse_logic(current_user.balance)
        current_user.balance = new_balance
        
        # Hapus data transaksi dari database
        db.session.delete(tx)
        db.session.commit()
        
        flash("Transaksi berhasil dihapus dan saldo telah disesuaikan.", "success")
        return redirect(url_for('dashboard'))
        
    except ValueError as e:
        db.session.rollback()
        flash(f"Gagal membatalkan transaksi: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)