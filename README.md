<div align="center">

# 🎵 YTMP3

**YouTube MP3 Downloader & Splitter — CLI Tool**

[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
[![ffmpeg](https://img.shields.io/badge/powered%20by-ffmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

Download MP3 dari YouTube, split kompilasi otomatis, auto numbering file — langsung dari terminal, tanpa iklan, tanpa upload ke mana-mana.

[📦 Download](#-instalasi) · [🚀 Cara Pakai](#-cara-pakai) · [⚙️ Konfigurasi](#%EF%B8%8F-konfigurasi)

</div>

---

## ✨ Fitur

| Fitur | Keterangan |
|-------|-----------|
| 🎵 Download MP3 | Download langsung dari YouTube, hasil MP3 berkualitas tinggi |
| 🔗 Multi URL | Input banyak URL sekaligus, pisah pakai koma |
| ✂️ Auto Split | Split file kompilasi jadi track terpisah via `timestamp.json` |
| 🔢 Auto Numbering | Penamaan file otomatis `01_judul.mp3`, bisa atur nomor awal |
| 🌐 Bilingual | Support Bahasa Indonesia & English |
| 🔍 Auto Detect | Cek & minta install `yt-dlp` dan `ffmpeg` otomatis kalau belum ada |
| ⚙️ Konfigurasi | Semua setelan tersimpan di `settings.json` |

---

## 📦 Instalasi

**Prasyarat:** Python 3.7+

```bash
# Clone repo
git clone git@github.com:Isthisindra/CLI-yt-donwloader.git
cd ytmp3

# Jalanin langsung — dependensi akan dicek otomatis
python ytmp3.py
```

> Pertama kali jalan, tool akan detect apakah `yt-dlp` dan `ffmpeg` sudah terinstall. Kalau belum, akan minta persetujuan install otomatis.

---

## 🚀 Cara Pakai

```bash
python ytmp3.py
```

### Menu Utama

```
=== YTMP3 - Downloader & Splitter MP3 ===

=== MENU UTAMA ===
1. Download MP3 dari YouTube
2. Split MP3 berdasarkan Timestamp
3. Pengaturan
4. Keluar
```

---

### 1️⃣ Download MP3

Input satu atau banyak URL sekaligus:

```
URL: https://youtu.be/abc123, https://youtu.be/def456, https://youtu.be/ghi789
```

Bisa atur nomor awal file, misalnya mulai dari `06`:
```
Nomor awal file: 6
→ Hasil: 06_Judul Lagu.mp3, 07_Judul Lagu.mp3, dst
```

---

### 2️⃣ Split Kompilasi via Timestamp

Buat file `timestamp.json` di folder yang sama dengan script:

```json
{
    "input_file": "D:\\musik\\kompilasi.mp3",
    "output_folder": "D:\\musik\\split",
    "start_number": 6,
    "tracks": [
        {"title": "Judul !", "start": "00:00"},
        {"title": "Judul 2", "start": "04:30"},
        {"title": "Judul 3", "start": "08:30"},
        {"title": "Judul 4", "start": "11:50"}
    ]
}
```

Jalanin menu **Split MP3** → otomatis jadi:
```
06_Judul 1.mp3
07_Judul 2.mp3
08_Judul 3.mp3
09_Judul 4.mp3
```

> 💡 Timestamp biasanya ada di deskripsi atau komentar video YouTube kompilasi.

---

## ⚙️ Konfigurasi

Semua setelan tersimpan di `settings.json`:

```json
{
    "language": "id",
    "output_path": "D:\\01_KUMPLAGU",
    "audio_quality": "0",
    "naming_format": "%(autonumber)02d_%(title)s",
    "autonumber_start": 1,
    "version": "1.0.0"
}
```

| Key | Nilai | Keterangan |
|-----|-------|-----------|
| `language` | `id` / `en` | Bahasa antarmuka |
| `output_path` | path folder | Folder output default |
| `audio_quality` | `0` – `9` | Kualitas MP3 (0 = terbaik) |
| `autonumber_start` | angka | Nomor awal default penamaan file |
| `version` | string | Versi app untuk pengembangan |

---

## 📁 Struktur File

```
ytmp3/
├── ytmp3.py          # Script utama
├── settings.json     # Setelan pengguna
├── timestamp.json    # Data split (dibuat sendiri)
└── README.md
```

---

## 🛠️ Dependensi

| Tool | Fungsi | Install |
|------|--------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download dari YouTube | `pip install yt-dlp` |
| [ffmpeg](https://ffmpeg.org) | Konversi & split audio | `winget install ffmpeg` |

> Keduanya akan dicek otomatis saat pertama kali menjalankan tool.

---

## 🤝 Kontribusi

Pull request welcome! Beberapa ide pengembangan:

- [ ] Auto detect silence untuk split tanpa timestamp
- [ ] Support platform lain (SoundCloud, dll)
- [ ] Batch processing dari file `.txt` berisi daftar URL
- [ ] Progress bar download
- [ ] GUI mode
- [ ] Support install ffmpeg di Mac, Linux, Termux/Android

---

## 📄 Lisensi

MIT License — bebas dipakai dan dikembangkan.

---

<div align="center">

Dibuat dengan ☕ dan `yt-dlp` + `ffmpeg`

*"Don't reinvent the wheel — just wrap it nicely"*

</div>
