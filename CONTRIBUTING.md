# 🤝 Panduan Kontribusi

Terima kasih atas minat Anda untuk berkontribusi dalam proyek **FinTrack**! 

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
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### 5. Instal Dependensi
```bash
pip install -r requirements.txt
```

---

## 🌿 Branching Strategy

### Jenis Branch

| Branch | Keterangan | Contoh |
|--------|------------|--------|
| `main` | Branch utama (stable) | - |
| `develop` | Branch untuk development | - |
| `feature/*` | Fitur baru | `feature/dark-mode` |
| `fix/*` | Perbaikan bug | `fix/login-error` |
| `docs/*` | Dokumentasi | `docs/update-readme` |
| `refactor/*` | Refactor kode | `refactor/cleanup-routes` |

### Workflow

```bash
# 1. Pastikan selalu update dari upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Buat branch baru dari main
git checkout -b feature/nama-fitur

# 3. Kerjakan perubahan dan commit
git add .
git commit -m "feat: tambahkan fitur baru"

# 4. Push ke fork Anda
git push origin feature/nama-fitur

# 5. Buka Pull Request di GitHub
```

---

## 📝 Conventional Commits

Format commit message:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type

| Type | Keterangan | Contoh |
|------|------------|--------|
| `feat` | Fitur baru | `feat(auth): tambahkan login dengan Google` |
| `fix` | Perbaikan bug | `fix(dashboard): koreksi error grafik` |
| `docs` | Dokumentasi | `docs: update README.md` |
| `style` | Formatting (tidak mempengaruhi kode) | `style: perbaiki indentasi` |
| `refactor` | Refactor kode | `refactor(models): optimasi query` |
| `test` | Penambahan/pengubahan test | `test: tambahkan test login` |
| `chore` | Maintenance | `chore: update dependencies` |
| `perf` | Optimasi performa | `perf: cache query database` |
| `ci` | CI/CD | `ci: tambahkan GitHub Actions` |
| `build` | Build system | `build: tambahkan Dockerfile` |

### Scope (Opsional)

- `auth` - Autentikasi
- `dashboard` - Dashboard
- `transaction` - Transaksi
- `models` - Model database
- `config` - Konfigurasi
- `templates` - Template HTML

### Contoh Lengkap

```bash
git commit -m "feat(auth): tambahkan rate limiting untuk login"

git commit -m "fix(transaction): koreksi perhitungan saldo

- Perbaiki logika pengurangan saldo
- Tambahkan validasi saldo mencukupi

Closes #42"

git commit -m "docs: tambahkan CONTRIBUTING.md"
```

---

## 🔄 Pull Request Process

### Sebelum Membuat PR

1. **Pastikan kode berjalan**
   ```bash
   python app.py
   ```

2. **Update dari upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

3. **Tulis commit message yang jelas**

### Format PR

```markdown
## Deskripsi
[Penjelasan singkat tentang perubahan]

## Tipe Perubahan
- [ ] 🐛 Bug Fix
- [ ] ✨ Fitur Baru
- [ ] 📝 Dokumentasi
- [ ] 🎨 Style/UI
- [ ] ♻️ Refactor
- [ ] ⚡ Performance

## Screenshot (jika ada)
[Upload screenshot perubahan UI]

## Checklist
- [ ] Kode berjalan tanpa error
- [ ] Tidak ada print statement yang tertinggal
- [ ] Komentar sudah ditambahkan jika diperlukan
- [ ] Dokumentasi sudah diupdate (jika perlu)
```

---

## 💻 Coding Standards

### Python
- Ikuti [PEP 8](https://peps.python.org/pep-0008/) style guide
- Gunakan 4 spasi untuk indentasi
- Maksimal 79 karakter per baris
- Gunakan docstring untuk fungsi dan kelas

```python
def get_user_balance(user_id):
    """
    Mendapatkan saldo pengguna berdasarkan user_id.
    
    Args:
        user_id (int): ID pengguna
        
    Returns:
        float: Saldo pengguna
        
    Raises:
        UserNotFoundError: Jika pengguna tidak ditemukan
    """
    pass
```

### HTML/Jinja2
- Gunakan 2 spasi untuk indentasi
- Gunakan semantic HTML
- Pastikan template responsive

### JavaScript
- Gunakan `const` dan `let` (hindari `var`)
- Gunakan camelCase untuk variabel dan fungsi
- Tambahkan komentar untuk kode kompleks

### Git
- Branch naming: `feature/nama-fitur`, `fix/nama-bug`
- Commit message: Gunakan Conventional Commits
- Satu commit untuk satu perubahan logis

---

## 🐛 Laporan Bug

### Template Laporan Bug

```markdown
## Deskripsi Bug
[Penjelasan singkat tentang bug]

## Steps to Reproduce
1. Buka halaman '...'
2. Klik tombol '...'
3. Scroll ke '...'
4. Error muncul

## Expected Behavior
[Seharusnya apa yang terjadi]

## Actual Behavior
[Apa yang sebenarnya terjadi]

## Screenshots
[Jika ada, upload screenshot]

## Environment
- OS: [contoh: Windows 11]
- Browser: [contoh: Chrome 120]
- Python Version: [contoh: 3.11]
```

---

## 💡 Feature Request

### Template Feature Request

```markdown
## Deskripsi Fitur
[Penjelasan singkat tentang fitur yang diinginkan]

## Use Case
[Mengapa fitur ini dibutuhkan?]

## Proposed Solution
[Bagaimana Anda bayangkan fitur ini bekerja]

## Alternatives Considered
[Alternatif lain yang pernah dipertimbangkan]

## Additional Context
[Konteks tambahan jika ada]
```

---

## ❓ Pertanyaan?

Jika ada pertanyaan, buka [GitHub Discussions](https://github.com/suzuy1/personal-finance-tracker/discussions) atau hubungi maintainers.

---

## 🙏 Terima Kasih!

Kontribusi Anda sangat berharga. Terima kasih sudah membantu mengembangkan **FinTrack**! 🚀
