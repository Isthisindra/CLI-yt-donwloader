#!/usr/bin/env python3
"""
YTMP3 - YouTube MP3 Downloader & Splitter
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
SETTINGS_FILE = BASE_DIR / "settings.json"
TIMESTAMP_FILE = BASE_DIR / "timestamp.json"

# ─── Default Settings ─────────────────────────────────────────────────────────
DEFAULT_SETTINGS = {
    "language": "id",
    "output_path": str(Path.home() / "Music"),
    "audio_quality": "0",
    "naming_format": "%(autonumber)02d_%(title)s",
    "autonumber_start": 1,
    "version": "1.0.0"
}

# ─── Translations ─────────────────────────────────────────────────────────────
LANG = {
    "id": {
        "welcome": "=== YTMP3 - Downloader & Splitter MP3 ===",
        "select_lang": "Pilih bahasa / Select language:",
        "lang_id": "1. Indonesia",
        "lang_en": "2. English",
        "lang_choice": "Pilihan (1/2): ",
        "menu_title": "=== MENU UTAMA ===",
        "menu_1": "1. Download MP3 dari YouTube",
        "menu_2": "2. Split MP3 berdasarkan Timestamp",
        "menu_3": "3. Pengaturan",
        "menu_4": "4. Keluar",
        "menu_choice": "Pilihan: ",
        "invalid_choice": "Pilihan tidak valid!",
        "enter_urls": "Masukkan URL YouTube (pisah dengan koma untuk banyak URL):",
        "url_prompt": "URL: ",
        "enter_output": "Folder output (kosongkan untuk pakai default): ",
        "enter_start_num": "Nomor awal file (contoh: 6 untuk mulai dari 06): ",
        "downloading": "Mendownload",
        "download_done": "Download selesai!",
        "download_fail": "Download gagal!",
        "checking_deps": "Mengecek dependensi...",
        "found": "ditemukan",
        "not_found": "tidak ditemukan",
        "install_ask": "Apakah ingin menginstall {dep}? (y/n): ",
        "installing": "Menginstall {dep}...",
        "install_ok": "Berhasil diinstall!",
        "install_fail": "Gagal install! Install manual dulu.",
        "install_cancel": "Install dibatalkan. Program membutuhkan {dep} untuk berjalan.",
        "deps_ok": "Semua dependensi siap!",
        "timestamp_not_found": "File timestamp.json tidak ditemukan di folder ini!",
        "timestamp_hint": "Buat file timestamp.json dulu. Contoh format ada di bawah.",
        "timestamp_example": '''Contoh timestamp.json:
{
    "input_file": "D:\\\\musik\\\\kompilasi.mp3",
    "output_folder": "D:\\\\musik\\\\split",
    "start_number": 1,
    "tracks": [
        {"title": "Judul Lagu 1", "start": "00:00"},
        {"title": "Judul Lagu 2", "start": "04:30"},
        {"title": "Judul Lagu 3", "start": "08:30"}
    ]
}''',
        "splitting": "Memproses split...",
        "split_track": "Split track",
        "split_done": "Split selesai! File tersimpan di:",
        "split_fail": "Gagal split track:",
        "input_not_found": "File input tidak ditemukan:",
        "settings_title": "=== PENGATURAN ===",
        "settings_lang": "1. Ganti bahasa (sekarang: {lang})",
        "settings_output": "2. Ganti folder output default (sekarang: {path})",
        "settings_quality": "3. Ganti kualitas audio (sekarang: {q})",
        "settings_start": "4. Ganti nomor awal default (sekarang: {n})",
        "settings_back": "5. Kembali",
        "settings_saved": "Pengaturan tersimpan!",
        "new_value": "Nilai baru: ",
        "goodbye": "Sampai jumpa!",
        "press_enter": "Tekan Enter untuk lanjut...",
        "quality_hint": "Kualitas (0=terbaik, 9=terburuk): ",
        "current_settings": "Pengaturan saat ini:",
        "no_urls": "Tidak ada URL yang dimasukkan!",
    },
    "en": {
        "welcome": "=== YTMP3 - YouTube MP3 Downloader & Splitter ===",
        "select_lang": "Select language / Pilih bahasa:",
        "lang_id": "1. Indonesia",
        "lang_en": "2. English",
        "lang_choice": "Choice (1/2): ",
        "menu_title": "=== MAIN MENU ===",
        "menu_1": "1. Download MP3 from YouTube",
        "menu_2": "2. Split MP3 by Timestamp",
        "menu_3": "3. Settings",
        "menu_4": "4. Exit",
        "menu_choice": "Choice: ",
        "invalid_choice": "Invalid choice!",
        "enter_urls": "Enter YouTube URL(s) (separate multiple with commas):",
        "url_prompt": "URL: ",
        "enter_output": "Output folder (leave empty for default): ",
        "enter_start_num": "Starting number (e.g. 6 to start from 06): ",
        "downloading": "Downloading",
        "download_done": "Download complete!",
        "download_fail": "Download failed!",
        "checking_deps": "Checking dependencies...",
        "found": "found",
        "not_found": "not found",
        "install_ask": "Do you want to install {dep}? (y/n): ",
        "installing": "Installing {dep}...",
        "install_ok": "Successfully installed!",
        "install_fail": "Installation failed! Please install manually.",
        "install_cancel": "Installation cancelled. {dep} is required to run.",
        "deps_ok": "All dependencies ready!",
        "timestamp_not_found": "timestamp.json not found in this folder!",
        "timestamp_hint": "Please create a timestamp.json file first. See example format below.",
        "timestamp_example": '''Example timestamp.json:
{
    "input_file": "D:\\\\music\\\\compilation.mp3",
    "output_folder": "D:\\\\music\\\\split",
    "start_number": 1,
    "tracks": [
        {"title": "Song Title 1", "start": "00:00"},
        {"title": "Song Title 2", "start": "04:30"},
        {"title": "Song Title 3", "start": "08:30"}
    ]
}''',
        "splitting": "Processing split...",
        "split_track": "Splitting track",
        "split_done": "Split complete! Files saved at:",
        "split_fail": "Failed to split track:",
        "input_not_found": "Input file not found:",
        "settings_title": "=== SETTINGS ===",
        "settings_lang": "1. Change language (current: {lang})",
        "settings_output": "2. Change default output folder (current: {path})",
        "settings_quality": "3. Change audio quality (current: {q})",
        "settings_start": "4. Change default start number (current: {n})",
        "settings_back": "5. Back",
        "settings_saved": "Settings saved!",
        "new_value": "New value: ",
        "goodbye": "Goodbye!",
        "press_enter": "Press Enter to continue...",
        "quality_hint": "Quality (0=best, 9=worst): ",
        "current_settings": "Current settings:",
        "no_urls": "No URLs entered!",
    }
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def load_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            s = json.load(f)
        # Merge with defaults for any missing keys
        for k, v in DEFAULT_SETTINGS.items():
            if k not in s:
                s[k] = v
        return s
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def t(key, settings, **kwargs):
    lang = settings.get("language", "id")
    text = LANG[lang].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

def check_dep(name):
    return shutil.which(name) is not None

def install_dep(name, settings):
    lang = settings.get("language", "id")
    print(f"  {name}: {t('not_found', settings)}")
    ans = input(t("install_ask", settings, dep=name)).strip().lower()
    if ans not in ("y", "ya", "yes"):
        print(t("install_cancel", settings, dep=name))
        return False

    print(t("installing", settings, dep=name))
    if name == "yt-dlp":
        result = subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], capture_output=True)
    elif name == "ffmpeg":
        if os.name == "nt":
            print("  ffmpeg: Download dari https://ffmpeg.org/download.html dan tambahkan ke PATH")
            print("  Atau install via winget: winget install ffmpeg")
            return False
        else:
            result = subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], capture_output=True)

    if result.returncode == 0:
        print(f"  {t('install_ok', settings)}")
        return True
    else:
        print(f"  {t('install_fail', settings)}")
        return False

def check_all_deps(settings):
    print(t("checking_deps", settings))
    deps = ["yt-dlp", "ffmpeg"]
    all_ok = True
    for dep in deps:
        if check_dep(dep):
            print(f"  {dep}: {t('found', settings)} ✓")
        else:
            ok = install_dep(dep, settings)
            if not ok:
                all_ok = False
    if all_ok:
        print(t("deps_ok", settings))
    return all_ok

def timestamp_to_seconds(ts):
    """Convert MM:SS or HH:MM:SS to seconds"""
    parts = ts.strip().split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return 0

def seconds_to_hhmmss(s):
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}"

# ─── Features ─────────────────────────────────────────────────────────────────

def feature_download(settings):
    clear()
    print(t("enter_urls", settings))
    raw = input(t("url_prompt", settings)).strip()
    if not raw:
        print(t("no_urls", settings))
        input(t("press_enter", settings))
        return

    urls = [u.strip() for u in raw.split(",") if u.strip()]

    out = input(t("enter_output", settings)).strip()
    if not out:
        out = settings["output_path"]

    start_raw = input(t("enter_start_num", settings)).strip()
    try:
        start_num = int(start_raw)
    except:
        start_num = int(settings.get("autonumber_start", 1))

    offset = start_num - 1
    quality = settings.get("audio_quality", "0")

    os.makedirs(out, exist_ok=True)

    for i, url in enumerate(urls):
        print(f"\n{t('downloading', settings)} ({i+1}/{len(urls)}): {url}")
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", quality,
            "--autonumber-start", str(start_num + i),
            "-o", os.path.join(out, f"%(autonumber)02d_%(title)s.%(ext)s"),
            url
        ]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print(t("download_done", settings))
        else:
            print(t("download_fail", settings))

    input(t("press_enter", settings))

def feature_split(settings):
    clear()
    if not TIMESTAMP_FILE.exists():
        print(t("timestamp_not_found", settings))
        print(t("timestamp_hint", settings))
        print()
        print(t("timestamp_example", settings))
        input(t("press_enter", settings))
        return

    with open(TIMESTAMP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    input_file = data.get("input_file", "")
    output_folder = data.get("output_folder", settings["output_path"])
    tracks = data.get("tracks", [])
    start_number = data.get("start_number", int(settings.get("autonumber_start", 1)))

    if not os.path.exists(input_file):
        print(f"{t('input_not_found', settings)} {input_file}")
        input(t("press_enter", settings))
        return

    os.makedirs(output_folder, exist_ok=True)
    print(t("splitting", settings))

    for i, track in enumerate(tracks):
        title = track["title"]
        start = timestamp_to_seconds(track["start"])

        if i + 1 < len(tracks):
            end = timestamp_to_seconds(tracks[i + 1]["start"])
            duration = end - start
            time_args = ["-ss", seconds_to_hhmmss(start), "-t", str(duration)]
        else:
            time_args = ["-ss", seconds_to_hhmmss(start)]

        num = start_number + i
        safe_title = "".join(c for c in title if c not in r'\/:*?"<>|')
        out_file = os.path.join(output_folder, f"{num:02d}_{safe_title}.mp3")

        print(f"  {t('split_track', settings)} {num:02d}: {title}")

        cmd = ["ffmpeg", "-y"] + time_args + ["-i", input_file, "-c", "copy", out_file]
        result = subprocess.run(cmd, capture_output=True)

        if result.returncode != 0:
            print(f"  {t('split_fail', settings)} {title}")

    print(f"\n{t('split_done', settings)}")
    print(f"  {output_folder}")
    input(t("press_enter", settings))

def feature_settings(settings):
    while True:
        clear()
        lang_name = "Indonesia" if settings["language"] == "id" else "English"
        print(t("settings_title", settings))
        print(t("settings_lang", settings, lang=lang_name))
        print(t("settings_output", settings, path=settings["output_path"]))
        print(t("settings_quality", settings, q=settings["audio_quality"]))
        print(t("settings_start", settings, n=settings["autonumber_start"]))
        print(t("settings_back", settings))
        print()
        choice = input(t("menu_choice", settings)).strip()

        if choice == "1":
            print("1. Indonesia\n2. English")
            l = input(t("lang_choice", settings)).strip()
            if l == "1":
                settings["language"] = "id"
            elif l == "2":
                settings["language"] = "en"
        elif choice == "2":
            val = input(t("new_value", settings)).strip()
            if val:
                settings["output_path"] = val
        elif choice == "3":
            val = input(t("quality_hint", settings)).strip()
            if val.isdigit() and 0 <= int(val) <= 9:
                settings["audio_quality"] = val
        elif choice == "4":
            val = input(t("new_value", settings)).strip()
            if val.isdigit():
                settings["autonumber_start"] = int(val)
        elif choice == "5":
            break
        else:
            print(t("invalid_choice", settings))

        save_settings(settings)
        print(t("settings_saved", settings))

    return settings

def select_language(settings):
    """First run language selection"""
    clear()
    print("=== YTMP3 ===")
    print()
    print("Pilih bahasa / Select language:")
    print("1. Indonesia")
    print("2. English")
    print()
    choice = input("Pilihan / Choice (1/2): ").strip()
    if choice == "2":
        settings["language"] = "en"
    else:
        settings["language"] = "id"
    save_settings(settings)
    return settings

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    settings = load_settings()

    # First run - select language
    if not SETTINGS_FILE.exists():
        settings = select_language(settings)
        save_settings(settings)

    # Check dependencies
    clear()
    print(t("welcome", settings))
    print()
    if not check_all_deps(settings):
        sys.exit(1)

    # Main loop
    while True:
        clear()
        print(t("welcome", settings))
        print()
        print(t("menu_title", settings))
        print(t("menu_1", settings))
        print(t("menu_2", settings))
        print(t("menu_3", settings))
        print(t("menu_4", settings))
        print()
        choice = input(t("menu_choice", settings)).strip()

        if choice == "1":
            feature_download(settings)
        elif choice == "2":
            feature_split(settings)
        elif choice == "3":
            settings = feature_settings(settings)
        elif choice == "4":
            print(t("goodbye", settings))
            break
        else:
            print(t("invalid_choice", settings))
            input(t("press_enter", settings))

if __name__ == "__main__":
    main()
