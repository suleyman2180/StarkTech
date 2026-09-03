#!/usr/bin/env python3
# ==============================================================================
# V.I.S.I.O.N. - Kuantum Dosya ve Kopya Analiz Protokolü
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================

import os
import sys
import hashlib
from pathlib import Path
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, NC, show_module_status

def get_file_hash(filepath, block_size=65536):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except Exception:
        return None

def find_duplicates(target_dir):
    print(f"\n{CYAN}==> '{target_dir}' içinde kopya dosyalar taranıyor...{NC}")
    size_map = defaultdict(list)

    for root, _, files in os.walk(target_dir):
        for f in files:
            full_path = os.path.join(root, f)
            try:
                if not os.path.islink(full_path):
                    sz = os.path.getsize(full_path)
                    if sz > 0:
                        size_map[sz].append(full_path)
            except Exception:
                continue

    potential_duplicates = [paths for sz, paths in size_map.items() if len(paths) > 1]

    hash_map = defaultdict(list)
    for path_list in potential_duplicates:
        for p in path_list:
            h = get_file_hash(p)
            if h:
                hash_map[h].append(p)

    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}

    if not duplicates:
        print(f"{GREEN}[✓] Kopya dosya bulunamadı!{NC}")
        return

    print(f"{YELLOW}[!] {len(duplicates)} kopya dosya seti bulundu:{NC}\n")
    total_wasted = 0
    for h, paths in duplicates.items():
        sz = os.path.getsize(paths[0])
        wasted_size = sz * (len(paths) - 1)
        total_wasted += wasted_size
        print(f"{CYAN}Kopya Seti (Boyut: {sz / (1024*1024):.2f} MB):{NC}")
        for p in paths:
            print(f"  - {p}")
        print()

    print(f"{GREEN}[✓] Toplam Boşa Giden Disk Alanı: {total_wasted / (1024*1024):.2f} MB{NC}")

def find_large_files(target_dir, min_size_mb=50):
    min_bytes = min_size_mb * 1024 * 1024
    print(f"\n{CYAN}==> '{target_dir}' içinde {min_size_mb} MB'dan büyük dosyalar taranıyor...{NC}")
    large_files = []

    for root, _, files in os.walk(target_dir):
        for f in files:
            full_path = os.path.join(root, f)
            try:
                if not os.path.islink(full_path):
                    sz = os.path.getsize(full_path)
                    if sz >= min_bytes:
                        large_files.append((full_path, sz))
            except Exception:
                continue

    large_files.sort(key=lambda x: x[1], reverse=True)

    if not large_files:
        print(f"{GREEN}[✓] {min_size_mb} MB'dan büyük dosya bulunamadı.{NC}")
        return

    print(f"{YELLOW}[!] {len(large_files)} büyük dosya bulundu:{NC}\n")
    for path, sz in large_files[:20]:
        print(f"  - {sz / (1024*1024):.2f} MB  ->  {path}")

def main():
    print(f"{CYAN}")
    print("  =======================================================")
    print("     V.I.S.I.O.N. Kuantum Dosya ve Kopya Analizcisi      ")
    print("  =======================================================")
    print(f"{NC}")

    while True:
        print("\nV.I.S.I.O.N. Protokol İşlemi Seçin:")
        print(" 1) Kopya Dosya Bul (SHA/MD5 Sağlama)")
        print(" 2) Büyük Dosya Bul (>50 MB)")
        print(" 0) Çıkış")

        choice = input("\nSeçim [0-2]: ").strip()

        if choice == '1':
            td = input("Taranacak dizini girin [varsayılan mevcut]: ").strip().strip('"') or "."
            find_duplicates(td)
        elif choice == '2':
            td = input("Taranacak dizini girin [varsayılan mevcut]: ").strip().strip('"') or "."
            try:
                mb = int(input("Minimum boyut MB olarak [varsayılan 50]: ") or 50)
            except:
                mb = 50
            find_large_files(td, mb)
        elif choice == '0':
            print(f"{GREEN}[V.I.S.I.O.N.] Zihin Taşı analizi tamamlandı.{NC}")
            show_module_status()
            break

if __name__ == '__main__':
    main()
