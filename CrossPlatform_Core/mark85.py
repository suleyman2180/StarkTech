#!/usr/bin/env python3
# ==============================================================================
# MARK 85 - Çapraz Platform Nanotek Arşiv ve Yedekleme Protokolü
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================

import os
import sys
import zipfile
import datetime
import hashlib
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, NC, show_module_status


def calculate_sha256(filepath: Path):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def create_backup(source_dir, output_dir=None):
    source_path = Path(source_dir).resolve()
    if not source_path.exists():
        print(f"{RED}[!] Kaynak yol mevcut değil: {source_path}{NC}")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = source_path.name or "Yedek"
    zip_name = f"{folder_name}_MARK85_{timestamp}.zip"

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        zip_path = out_path / zip_name
    else:
        zip_path = source_path.parent / zip_name

    print(f"{CYAN}==> '{source_path}' arşivleniyor -> '{zip_path}' ...{NC}")

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        if source_path.is_file():
            zipf.write(source_path, source_path.name)
            file_count = 1
        else:
            for root, _dirs, files in os.walk(source_path):
                for file in files:
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(source_path)
                    zipf.write(full_path, str(rel_path))
                    file_count += 1

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    sha256_hash = calculate_sha256(zip_path)

    print(f"{GREEN}[✓] Yedekleme Başarıyla Oluşturuldu!{NC}")
    print(f"{YELLOW} Arşiv Dosyası : {zip_path}{NC}")
    print(f"{YELLOW} Toplam Dosya  : {file_count}{NC}")
    print(f"{YELLOW} Arşiv Boyutu  : {size_mb:.2f} MB{NC}")
    print(f"{YELLOW} SHA256 Hash   : {sha256_hash}{NC}")


def extract_backup(zip_path, target_dir):
    zip_p = Path(zip_path)
    if not zip_p.exists():
        print(f"{RED}[!] ZIP arşivi bulunamadı: {zip_p}{NC}")
        return

    target_p = Path(target_dir)
    target_p.mkdir(parents=True, exist_ok=True)
    print(f"{CYAN}==> '{zip_p}' çıkartılıyor -> '{target_p}' ...{NC}")

    with zipfile.ZipFile(zip_p, "r") as zipf:
        zipf.extractall(target_p)

    print(f"{GREEN}[✓] Çıkartma Tamamlandı: {target_p}{NC}")


def main():
    print(YELLOW)
    print("  =======================================================")
    print("      MARK 85 Çapraz Platform Yedekleme ve Arşiv Süiti   ")
    print("  =======================================================")
    print(NC)

    while True:
        print()
        print("MARK-85 Protokol İşlemi Seçin:")
        print(" 1) Zaman Damgalı ZIP Yedek Arşivi Oluştur")
        print(" 2) ZIP Arşivini Çıkart")
        print(" 0) Çıkış")
        print()
        choice = input("Seçim [0-2]: ").strip()

        if choice == "1":
            src = input("Yedeklenecek klasör veya dosya yolu: ").strip().strip('"')
            out = input("Hedef klasör (boş bırakılırsa aynı dizin): ").strip().strip('"')
            if src:
                create_backup(src, out if out else None)
        elif choice == "2":
            zp = input("ZIP dosyasının yolu: ").strip().strip('"')
            tg = input("Çıkartma hedef dizini: ").strip().strip('"')
            if zp and tg:
                extract_backup(zp, tg)
        elif choice == "0":
            print(f"{GREEN}[MARK-85] Nanotek yedekleme protokolü tamamlandı.{NC}")
            show_module_status()
            break


if __name__ == '__main__':
    main()
