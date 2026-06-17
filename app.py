from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import csv
import io
from models import db, User, Income, Expense, Transaction
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def initialize_database():
    db.create_all() # Otomatis update skema tabel SQLite nambah kolom password_hash
    
    # Proteksi Session Tampering / Invalidation setelah database dihapus/di-reset
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if not user:
            session.pop('user_id', None) # Bersihkan sesi kadaluarsa
            flash('Sesi Anda tidak valid atau akun telah dihapus. Silakan login kembali.', 'error')

# ==========================================
# CONTROLLER 1: AUTHENTICATION (LOGIN, REGISTER, LOGOUT)
# ==========================================

@app.route('/auth', methods=['GET'])
def auth_page():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('auth.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter((User.email == email) | (User.username == username)).first():
        flash('Username atau Email sudah terdaftar!', 'error')
        return redirect(url_for('auth_page'))

    new_user = User(username=username, email=email)
    new_user.set_password(password) # Enkapsulasi: hashing password otomatis via OOP Method
    new_user.balance = 10000000 # Kasih modal awal Rp10 Juta otomatis via Setter

    db.session.add(new_user)
    db.session.commit()
    
    flash('Akun berhasil dibuat! Silakan login.', 'success')
    return redirect(url_for('auth_page'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        session['user_id'] = user.id # Simpan ID user ke Session Browser
        return redirect(url_for('dashboard'))
    
    flash('Email atau password Anda salah!', 'error')
    return redirect(url_for('auth_page'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth_page'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Menggunakan session untuk validasi sementara (mencegah URL parameter tampering di Demo Mode)
            session['reset_email'] = email
            return redirect(url_for('reset_password'))
        
        flash('Alamat email tidak ditemukan di database!', 'error')
        return redirect(url_for('forgot_password'))
        
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    # Validasi keberadaan session reset_email sebelum mengizinkan ubah password
    email = session.get('reset_email')
    if not email:
        flash('Akses tidak sah atau sesi pemulihan telah kadaluarsa!', 'error')
        return redirect(url_for('auth_page'))
        
    user = User.query.filter_by(email=email).first_or_404()
    
    if request.method == 'POST':
        new_password = request.form.get('password')
        
        # Menggunakan enkapsulasi method OOP untuk hashing password terbaru
        user.set_password(new_password)
        db.session.commit()
        
        # Bersihkan session reset setelah berhasil diubah
        session.pop('reset_email', None)
        
        flash('Password berhasil diperbarui! Silakan masuk kembali.', 'success')
        return redirect(url_for('auth_page'))
        
    return render_template('reset_password.html', email=email)

# ==========================================
# CONTROLLER 2: FINANCIAL LOGIC (SUDAH MULTI-USER)
# ==========================================

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))
    
    current_user = User.query.get(session['user_id'])
    
    # Ambil semua transaksi milik user untuk kalkulasi total dan tren
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
    
    # LOGIKA ANALYTICS: Hitung total masuk dan keluar secara real-time
    total_income = sum(float(tx.amount) for tx in user_transactions if tx.type == 'income')
    total_expense = sum(float(tx.amount) for tx in user_transactions if tx.type == 'expense')
    
    # LOGIKA TREN SALDO HISTORIS: Hitung mundur pergerakan saldo dari saldo saat ini
    running_balance = float(current_user.balance)
    temp_balance = running_balance
    history = []
    
    for tx in user_transactions:
        # Format label tanggal (misal: "17 Jun")
        history.append((tx.created_at.strftime('%d %b'), temp_balance))
        if tx.type == 'income':
            temp_balance -= float(tx.amount)
        elif tx.type == 'expense':
            temp_balance += float(tx.amount)
            
    # Balikkan agar urutan kronologis dari terlama ke terbaru untuk grafik
    history.reverse()
    
    if not history:
        chart_data = [running_balance]
        chart_labels = ['Sekarang']
    else:
        chart_data = [item[1] for item in history]
        chart_labels = [item[0] for item in history]
        
    # Hitung persentase pemakaian budget
    budget_limit = float(current_user.budget_limit)
    budget_percentage = (total_expense / budget_limit) * 100 if budget_limit > 0 else 0
    if budget_percentage > 100: 
        budget_percentage = 100
        
    return render_template(
        'dashboard.html', 
        user=current_user, 
        transactions=user_transactions,
        total_income=total_income,
        total_expense=total_expense,
        chart_data=chart_data,
        chart_labels=chart_labels,
        budget_percentage=round(budget_percentage, 1)
    )

# [READ ALL] - Halaman Khusus Riwayat Transaksi Lengkap
@app.route('/transactions')
def transaction_list():
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))
    
    current_user = User.query.get(session['user_id'])
    # Mengambil seluruh transaksi user dari yang paling baru
    all_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
    
    return render_template('transactions.html', user=current_user, transactions=all_transactions)

@app.route('/transaction/add', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))

    if request.method == 'POST':
        current_user = User.query.get(session['user_id'])
        tx_type = request.form.get('type')
        amount = float(request.form.get('amount'))
        category = request.form.get('category_id')
        description = request.form.get('description')

        try:
            if tx_type == 'income':
                new_tx = Income(user_id=current_user.id, amount=amount, category=category, description=description)
            elif tx_type == 'expense':
                new_tx = Expense(user_id=current_user.id, amount=amount, category=category, description=description)
            else:
                return "Tipe tidak valid", 400

            current_user.balance = new_tx.execute_financial_logic(current_user.balance)
            
            db.session.add(new_tx)
            db.session.commit()
            return redirect(url_for('dashboard'))

        except ValueError as e:
            db.session.rollback()
            return f"Error: {str(e)}", 400

    return render_template('transaction_form.html')

@app.route('/transaction/delete/<int:tx_id>')
def delete_transaction(tx_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))

    current_user = User.query.get(session['user_id'])
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()
    
    try:
        # PBO/Business Logic: Eksekusi pembalikan saldo secara polimorfik lewat objek transaksi
        new_balance = tx.execute_reverse_logic(current_user.balance)
        current_user.balance = new_balance
        
        db.session.delete(tx)
        db.session.commit()
        
        flash("Transaksi berhasil dihapus dan saldo telah disesuaikan.", "success")
        return redirect(url_for('dashboard'))
        
    except ValueError as e:
        db.session.rollback()
        flash(f"Gagal membatalkan transaksi: {str(e)}", "danger")
        return redirect(url_for('dashboard'))

# [UPDATE] - Controller Edit Transaksi (Form & Proses Update)
@app.route('/transaction/edit/<int:tx_id>', methods=['GET', 'POST'])
def edit_transaction(tx_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))

    current_user = User.query.get(session['user_id'])
    # Pastikan transaksi yang diedit ada dan benar-benar milik user yang login
    tx = Transaction.query.filter_by(id=tx_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        new_type = request.form.get('type')
        new_amount = float(request.form.get('amount'))
        new_category = request.form.get('category_id')
        new_description = request.form.get('description')

        try:
            # Jika user mengubah jenis transaksi (misal dari income ke expense)
            if tx.type != new_type:
                return "Sistem Enterprise: Mengubah struktur rumpun kelas OOP secara langsung tidak diizinkan. Silakan hapus dan buat baru jika salah tipe!", 400

            # 1. REVERSE LOGIC secara polimorfik (OOP/PBO Compliance!)
            # Membatalkan efek saldo dari transaksi LAMA secara dinamis
            temp_balance = tx.execute_reverse_logic(current_user.balance)

            # 2. UPDATE DATA: Simpan nilai lama untuk rollback memori jika validasi gagal
            old_amount = tx.amount
            tx.amount = new_amount
            
            try:
                # 3. APPLY LOGIC secara polimorfik
                # Menerapkan nominal BARU ke saldo sementara untuk divalidasi
                new_balance = tx.execute_financial_logic(temp_balance)
                
                # Jika semua validasi saldo aman, terapkan perubahan & simpan
                current_user.balance = new_balance
                tx.category = new_category
                tx.description = new_description
                db.session.commit()
                return redirect(url_for('dashboard'))
            except ValueError as e:
                # Rollback nilai amount ke yang lama di memori objek SQLAlchemy
                tx.amount = old_amount
                raise e

        except ValueError as e:
            db.session.rollback()
            return f"Gagal memperbarui logika keuangan: {str(e)}", 400

    # GET: Tampilkan halaman edit dengan membawa data lama (Auto-fill)
    return render_template('edit_transaction.html', tx=tx)

# FITUR PREMIUM 1: Update Limit Budget bulanan
@app.route('/update-budget', methods=['POST'])
def update_budget():
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))
    
    current_user = User.query.get(session['user_id'])
    new_budget = request.form.get('budget_limit')
    
    if new_budget:
        try:
            budget_val = float(new_budget)
            if budget_val < 0:
                flash('Batas anggaran tidak boleh negatif!', 'error')
                return redirect(url_for('dashboard'))
            current_user.budget_limit = budget_val
            db.session.commit()
            flash('Batas anggaran berhasil diperbarui.', 'success')
        except ValueError:
            flash('Nominal anggaran tidak valid!', 'error')
        
    return redirect(url_for('dashboard'))

# FITUR PREMIUM 2: Export Data Transaksi ke File CSV (Excel)
@app.route('/transactions/export')
def export_csv():
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))
        
    current_user = User.query.get(session['user_id'])
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
    
    # Menggunakan io.StringIO dan csv.writer untuk menangani karakter koma atau baris baru pada deskripsi secara aman
    output_stream = io.StringIO()
    writer = csv.writer(output_stream, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Tulis header CSV
    writer.writerow(["Tanggal", "Keterangan", "Kategori ID", "Jenis", "Nominal"])
    
    # Tulis baris data
    for tx in user_transactions:
        jenis = "Pemasukan" if tx.type == 'income' else "Pengeluaran"
        writer.writerow([
            tx.created_at.strftime('%Y-%m-%d'),
            tx.description if tx.description else 'Tanpa keterangan',
            tx.category,
            jenis,
            float(tx.amount)
        ])
    
    # Bungkus response sebagai file unduhan
    response = make_response(output_stream.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=Laporan_Finansial_{current_user.username}.csv"
    response.headers["Content-type"] = "text/csv"
    return response

if __name__ == '__main__':
    app.run(debug=True)