# 🤝 Panduan Kontribusi — FinTrack

Terima kasih atas minat Anda untuk berkontribusi dalam proyek **FinTrack**! 

FinTrack adalah aplikasi pencatat keuangan pribadi berbasis Flask yang menerapkan prinsip **OOP (Enkapsulasi, Inheritance, Polimorfisme)** dengan database SQLAlchemy dan antarmuka TailwindCSS.

## 📋 Daftar Isi

- [Persiapan Awal](#persiapan-awal)
- [Branching Strategy](#branching-strategy)
- [Conventional Commits](#conventional-commits)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Laporan Bug](#laporan-bug)
- [Feature Request](#feature-request)

---

## 🚀 Persiapan Awal

### 1. Fork Repository
```bash
# Buka halaman repository di GitHub
# Klik tombol "Fork" di pojok kanan atas
```

### 2. Clone Repository
```bash
git clone https://github.com/suzuy1/personal-finance-tracker.git
cd fintrack
```

### 3. Tambahkan Upstream
```bash
git remote add upstream https://github.com/suzuy1/personal-finance-tracker.git
```

### 4. Buat Virtual Environment
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 5. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 6. Buat File `.env` (Wajib!)
Buat file `.env` di root proyek:
```bash
echo "SECRET_KEY=your-super-secret-key-here" > .env
```
> **Catatan:** Jangan commit file `.env` ke repository. Pastikan sudah masuk `.gitignore`.

### 7. Jalankan Aplikasi (Test)
```bash
python app.py
```
Buka `http://localhost:5000` untuk memastikan semua berjalan lancar.

---

## 🌿 Branching Strategy

Gunakan branch berikut untuk menjaga stabilitas kode:

| Branch | Keterangan | Contoh |
|--------|------------|--------|
| `main` | Branch utama (stable) | - |
| `develop` | Branch untuk pengembangan | - |
| `feature/*` | Fitur baru | `feature/category-chart` |
| `fix/*` | Perbaikan bug | `fix/balance-calculation` |
| `docs/*` | Dokumentasi | `docs/update-readme` |
| `refactor/*` | Refaktor kode (OOP improvement) | `refactor/polymorphism-logic` |

### Workflow Standar
```bash
# 1. Update branch main dari upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Buat branch fitur baru
git checkout -b feature/nama-fitur

# 3. Kerjakan perubahan & commit
git add .
git commit -m "feat: tambahkan fitur baru"

# 4. Push ke fork Anda
git push origin feature/nama-fitur

# 5. Buat Pull Request di GitHub
```

---

## 📝 Conventional Commits

Gunakan format commit message yang konsisten:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Tipe (Type) yang Tersedia

| Type | Keterangan | Contoh |
|------|------------|--------|
| `feat` | Fitur baru | `feat(transaction): tambahkan bulk delete` |
| `fix` | Perbaikan bug | `fix(dashboard): koreksi perhitungan total expense` |
| `docs` | Dokumentasi | `docs: update README dengan setup .env` |
| `style` | Formatting (tidak mempengaruhi kode) | `style: perbaiki indentasi models.py` |
| `refactor` | Refaktor kode | `refactor(models): optimasi query dengan eager loading` |
| `test` | Penambahan/pengubahan test | `test: tambahkan unit test untuk Income.execute_financial_logic` |
| `chore` | Maintenance (dependencies, config) | `chore: update Flask ke 3.1.3` |
| `perf` | Optimasi performa | `perf: cache query kategori default` |

### Scope yang Direkomendasikan
- `auth` – Autentikasi (login, register, reset password)
- `dashboard` – Halaman dashboard & grafik
- `transaction` – CRUD transaksi, filter, export
- `category` – Kategori default & custom
- `models` – Model database (User, Transaction, Income, Expense, Category)
- `api` – Endpoint RESTful (search, bulk, categories)
- `templates` – Template HTML/Jinja2
- `config` – Konfigurasi & environment variables

### Contoh Commit Lengkap
```bash
git commit -m "feat(category): tambahkan endpoint API untuk kategori custom user

- Tambahkan route /api/categories/<type> untuk load kategori default + custom
- Tambahkan route /api/categories/add untuk menyimpan kategori baru
- Update transaction_form.html untuk support kategori custom via JavaScript

Closes #15"
```

---

## 🔄 Pull Request Process

### Sebelum Membuat PR
1. **Pastikan aplikasi berjalan tanpa error**
   ```bash
   python app.py
   ```
2. **Update branch dengan upstream terbaru**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
3. **Pastikan semua test (jika ada) lolos**
   ```bash
   pytest
   ```
4. **Cek style code (flake8)**
   ```bash
   flake8 --select=E,W
   ```

### Template Pull Request
```markdown
## 📌 Deskripsi
[Penjelasan singkat tentang perubahan yang dilakukan]

## 🏷️ Tipe Perubahan
- [ ] 🐛 Bug Fix
- [ ] ✨ Fitur Baru
- [ ] 📝 Dokumentasi
- [ ] 🎨 Style/UI
- [ ] ♻️ Refactor (OOP)
- [ ] ⚡ Performance

## 🧪 Testing
- [ ] Sudah diuji secara lokal
- [ ] Tidak merusak fitur existing (regression)

## 📸 Screenshot (jika ada perubahan UI)
[Upload screenshot di sini]

## ✅ Checklist
- [ ] Kode berjalan tanpa error
- [ ] Tidak ada `print()` atau `console.log()` yang tertinggal
- [ ] Komentar sudah ditambahkan untuk logika kompleks (terutama polimorfisme)
- [ ] Dokumentasi (README/CONTRIBUTING) sudah diupdate jika perlu
- [ ] File `.env` tidak ter-commit
```

---

## 💻 Coding Standards

### Python (PEP 8)
- Gunakan **4 spasi** untuk indentasi
- Maksimal **79 karakter** per baris (untuk komentar/docstring, 72 karakter)
- Gunakan **docstring** untuk semua kelas dan fungsi publik

#### Spesifik untuk Proyek FinTrack (OOP)
- **Enkapsulasi**: Gunakan `@property` dan `@setter` untuk atribut yang dilindungi (contoh: `_balance` di model `User`).
- **Inheritance & Polymorphism**: Pastikan method abstract (`execute_financial_logic`, `execute_reverse_logic`) diimplementasikan dengan benar di subclass (`Income`, `Expense`).
- **Type Hints**: Sangat dianjurkan (minimal untuk fungsi publik).

```python
# Contoh DOCSTRING dan Type Hints yang baik
from typing import Union

def calculate_new_balance(transaction: Transaction, current_balance: float) -> float:
    """
    Menghitung saldo baru berdasarkan jenis transaksi (income/expense).
    
    Args:
        transaction (Transaction): Objek transaksi (Income atau Expense).
        current_balance (float): Saldo saat ini.
    
    Returns:
        float: Saldo baru setelah transaksi diterapkan.
    
    Raises:
        ValueError: Jika saldo tidak mencukupi untuk pengeluaran.
    """
    return transaction.execute_financial_logic(current_balance)
```

### HTML / Jinja2
- Gunakan **2 spasi** untuk indentasi
- Manfaatkan `{% block %}` dan `{% extends %}` untuk menghindari duplikasi
- Pastikan aksesibilitas (label pada input, alt pada ikon)

### JavaScript
- Gunakan **`const`** dan **`let`** (hindari `var`)
- Gunakan **camelCase** untuk variabel/fungsi
- Gunakan **`async/await`** untuk request API (contoh: fetch ke `/api/transactions/search`)
- Tambahkan komentar untuk fungsi yang kompleks

### CSS / Tailwind
- **Jangan** menulis custom CSS jika bisa menggunakan utility Tailwind
- Simpan custom style di bagian `<style>` pada template atau file `.css` terpisah jika sangat diperlukan

### Git
- Branch naming: `feature/nama-fitur`, `fix/nama-bug`
- Commit message: **wajib** mengikuti Conventional Commits
- **Satu commit untuk satu perubahan logis** (jangan gabung refactor + bug fix dalam 1 commit)

---

## 🐛 Laporan Bug

### Template Laporan Bug
```markdown
## 🐛 Deskripsi Bug
[Penjelasan singkat tentang bug]

## 🔄 Steps to Reproduce
1. Login sebagai user
2. Buka halaman 'Transaksi'
3. Klik 'Export CSV'
4. Error muncul

## ✅ Expected Behavior
[Seharusnya file CSV terunduh]

## ❌ Actual Behavior
[Error 500 atau file corrupt]

## 📷 Screenshots
[Jika ada, upload screenshot]

## 💻 Environment
- OS: [Windows 11 / Ubuntu 22.04]
- Browser: [Chrome 120]
- Python Version: [3.11]

## 🔍 Log Error (jika ada)
[Tempelkan traceback error di sini]
```

---

## 💡 Feature Request

### Template Feature Request
```markdown
## 💡 Deskripsi Fitur
[Jelaskan fitur yang diinginkan]

## 🎯 Use Case
[Mengapa fitur ini dibutuhkan? Siapa yang akan menggunakannya?]

## 🛠️ Proposed Solution
[Bagaimana fitur ini bekerja? Berikan gambaran teknis sederhana]

## 🔄 Alternatif Lain
[Pendekatan lain yang pernah dipertimbangkan]

## 📝 Konteks Tambahan
[Screenshot, referensi, atau contoh dari aplikasi lain]
```

---

## 🧪 OOP Rules (Khusus untuk Proyek ini)

Karena proyek ini adalah tugas akhir **Pemrograman Berorientasi Objek**, kontribusi wajib memperhatikan aturan berikut:

1. **Jangan merusak prinsip Enkapsulasi** – Atribut seperti `_balance` harus tetap diakses via `@property`.
2. **Jangan menghilangkan Inheritance** – Semua transaksi harus mewarisi dari `Transaction`.
3. **Jangan menghilangkan Polymorphism** – Setiap subclass (`Income`, `Expense`) harus mengimplementasikan method `execute_financial_logic` dan `execute_reverse_logic`.
4. **Tambahkan validasi** – Setiap perubahan logika keuangan harus memiliki validasi (misal: saldo tidak boleh negatif).

---

## ❓ Ada Pertanyaan?

Jika ada pertanyaan, silakan buka [GitHub Discussions](https://github.com/suzuy1/personal-finance-tracker/discussions) atau hubungi maintainers.

---

## 🙏 Terima Kasih!

Kontribusi Anda sangat berharga. Terima kasih sudah membantu mengembangkan **FinTrack** dan mempraktikkan **PBO** dengan baik! 🚀