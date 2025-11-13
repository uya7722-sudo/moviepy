# Aircraft Job Card Database Application

Aplikasi web untuk mengelola database Job Card pesawat menggunakan Python Flask.

## Fitur

- **CRUD Operations**: Tambah, Edit, Hapus job card
- **Filter & Search**: Filter berdasarkan Check Type dan Aircraft Registration
- **Search**: Pencarian berdasarkan Card Number, Task Reference, Task Title, Description, dan Zone
- **Export**: Export data yang difilter ke Excel
- **Multi-Aircraft Support**: Kelola status job card untuk 7 pesawat (PK-YSV, PK-YSG, PK-YSZ, PK-YSH, PK-YSN, PK-YRD, PK-YST)
- **Web-Based Interface**: Akses melalui browser dengan UI yang modern dan responsif

## Struktur Database

Database Excel memiliki 4 sheet:
1. **Sheet1**: Database utama job card (1673+ records)
2. **Sheet2**: Data registrasi pesawat (7 aircraft)
3. **Sheet3**: Template job card
4. **Sheet4**: Interface input

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

atau

```bash
python3 -m pip install -r requirements.txt
```

2. Pastikan file `Aircraft_Jobcard_Database.xlsm` ada di folder `uploads/`

## Cara Menjalankan

1. Jalankan aplikasi Flask:
```bash
python app.py
```

atau

```bash
python3 app.py
```

2. Buka browser dan akses:
```
http://localhost:5000
```

## Penggunaan

### Menambah Job Card
1. Klik tombol "➕ Add Job Card"
2. Isi form dengan data job card
3. Klik "Save"

### Mengedit Job Card
1. Klik tombol "Edit" pada row job card yang ingin diedit
2. Edit data yang diperlukan
3. Klik "Save"

### Menghapus Job Card
1. Klik tombol "Delete" pada row job card yang ingin dihapus
2. Konfirmasi penghapusan

### Filter Data
- **Check Type**: Pilih tipe check dari dropdown (1A CHECK, 2A CHECK, 4A CHECK, 8A CHECK)
- **Aircraft**: Pilih registrasi pesawat dari dropdown
- **Search**: Ketik keyword untuk mencari di Card Number, Task Reference, Task Title, Description, atau Zone
- **Clear Filters**: Klik untuk menghapus semua filter

### Export Data
1. Filter data sesuai kebutuhan
2. Klik tombol "📥 Export"
3. File Excel akan otomatis terdownload

### Menyimpan Perubahan
- Klik tombol "💾 Save Changes" untuk menyimpan semua perubahan ke database Excel

### Refresh Data
- Klik tombol "🔄 Refresh" untuk memuat ulang data dari database

## Struktur Kode

```
.
├── app.py                  # Flask application (API endpoints)
├── models.py              # Data models (JobCard, Aircraft)
├── database.py            # Database handler untuk operasi Excel
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── app.js         # Frontend JavaScript
└── uploads/
    └── Aircraft_Jobcard_Database.xlsm  # Database Excel
```

## API Endpoints

- `GET /` - Main page
- `GET /api/jobcards` - Get all job cards (with optional filters)
- `GET /api/jobcards/<index>` - Get single job card
- `POST /api/jobcards` - Add new job card
- `PUT /api/jobcards/<index>` - Update job card
- `DELETE /api/jobcards/<index>` - Delete job card
- `POST /api/save` - Save changes to database
- `GET /api/metadata` - Get metadata (check types, aircraft)
- `POST /api/export` - Export filtered data to Excel

## Requirements

- Python 3.7+
- Flask >= 2.3.0
- openpyxl >= 3.1.0
- pandas >= 2.0.0

## Teknologi

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Database**: Excel (.xlsm) dengan openpyxl dan pandas
- **UI**: Modern gradient design dengan responsive layout

## Catatan

- Aplikasi berjalan di port 5000 secara default
- Data disimpan dalam format Excel (.xlsm)
- Backup database secara berkala untuk menghindari kehilangan data
- Pastikan file Excel tidak dibuka di aplikasi lain saat menggunakan aplikasi ini
- Aplikasi ini menggunakan web interface, tidak memerlukan Tkinter

## Troubleshooting

### Error: Database file not found
Pastikan file `Aircraft_Jobcard_Database.xlsm` ada di folder `uploads/`

### Error: Permission denied
Tutup file Excel jika sedang dibuka di aplikasi lain (Microsoft Excel, LibreOffice, dll)

### Error loading data
Periksa format file Excel dan pastikan sheet names sesuai (Sheet1, Sheet2 , Sheet3, Sheet4 )

### Port already in use
Jika port 5000 sudah digunakan, edit `app.py` dan ubah port di baris:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## Screenshot

Aplikasi menampilkan:
- Header dengan gradient background
- Filter controls (Check Type, Aircraft, Search)
- Action buttons (Add, Save, Export, Refresh)
- Tabel data job cards dengan pagination
- Modal dialog untuk add/edit job card
- Status bar untuk feedback

## Lisensi

Aplikasi ini dibuat untuk mengelola Aircraft Job Card Database.
