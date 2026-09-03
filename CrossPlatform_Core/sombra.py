#!/usr/bin/env python3
# ==============================================================================
# G.H.O.S.T. - Orphan File & Registry Remnant Finder
# Supported OS: Windows, macOS, Linux
# ==============================================================================

import os
import sys
import shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, NC, get_os, show_module_status

def get_dir_size(path):
    total = 0
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                if not os.path.islink(fp):
                    total += os.path.getsize(fp)
    except Exception:
        pass
    return total

def scan_windows_remnants():
    print(f"{CYAN}==> Windows AppData & Registry Kalıntı Taraması Başlatılıyor...{NC}")
    remnants = []
    
    appdata_local = os.environ.get('LOCALAPPDATA', '')
    appdata_roaming = os.environ.get('APPDATA', '')
    
    scan_paths = [appdata_local, appdata_roaming]
    
    for base in scan_paths:
        if base and os.path.exists(base):
            for item in os.listdir(base):
                item_path = os.path.join(base, item)
                if os.path.isdir(item_path):
                    # Kalıntı testi: Boş klasör veya eski cache dizini
                    size = get_dir_size(item_path)
                    if size < 1024 * 1024 and ('cache' in item.lower() or 'temp' in item.lower() or 'old' in item.lower()):
                        remnants.append((item_path, size))

    # Registry Taraması (HKCU Software)
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software", 0, winreg.KEY_READ)
        print(f"{GREEN}[✓] HKCU\\Software Registry Anahtarları Yüklendi.{NC}")
        winreg.CloseKey(key)
    except Exception:
        pass

    return remnants

def scan_mac_remnants():
    print(f"{CYAN}==> macOS ~/Library Application Support & Cache Kalıntı Taraması...{NC}")
    remnants = []
    home = os.path.expanduser('~')
    mac_paths = [
        os.path.join(home, 'Library', 'Application Support'),
        os.path.join(home, 'Library', 'Caches'),
        os.path.join(home, 'Library', 'LaunchAgents')
    ]
    
    for base in mac_paths:
        if os.path.exists(base):
            for item in os.listdir(base):
                item_path = os.path.join(base, item)
                size = get_dir_size(item_path)
                if 'cache' in item.lower() or 'tmp' in item.lower() or size == 0:
                    remnants.append((item_path, size))

    return remnants

def scan_linux_remnants():
    print(f"{CYAN}==> Linux ~/.config, ~/.cache Kalıntı Taraması...{NC}")
    remnants = []
    home = os.path.expanduser('~')
    linux_paths = [
        os.path.join(home, '.cache'),
        os.path.join(home, '.config'),
        '/var/cache'
    ]
    
    for base in linux_paths:
        if os.path.exists(base):
            try:
                for item in os.listdir(base):
                    item_path = os.path.join(base, item)
                    size = get_dir_size(item_path)
                    if 'cache' in item.lower() or 'tmp' in item.lower() or size == 0:
                        remnants.append((item_path, size))
            except PermissionError:
                continue

    return remnants

def scan_remnants():
    system = get_os()
    print(f"{CYAN}")
    print("  =======================================================")
    print("     G.H.O.S.T.  -  ORPHAN FILE & REMNANT FINDER v1.0    ")
    print("  =======================================================")
    print(f"{NC}")
    print(f"{GREEN}[G.H.O.S.T.] Kaldırılmış yazılımlara ait artık dosya ve kayıtlar taranıyor...{NC}\n")

    if system == 'Windows':
        remnants = scan_windows_remnants()
    elif system == 'macOS':
        remnants = scan_mac_remnants()
    else:
        remnants = scan_linux_remnants()

    if not remnants:
        print(f"{GREEN}[✓] Temizlenecek herhangi bir artık dosya veya kalıntı bulunamadı.{NC}")
        show_module_status()
        return

    print(f"\n{YELLOW}[!] Bulunan Artık Klasörler ve Önbellekler:{NC}\n")
    total_reclaimable = 0
    for idx, (path, sz) in enumerate(remnants, 1):
        sz_mb = sz / (1024 * 1024)
        total_reclaimable += sz
        print(f"  {idx:2d}) [{sz_mb:6.2f} MB]  {path}")

    total_mb = total_reclaimable / (1024 * 1024)
    print(f"\n{GREEN}[✓] Toplam Kazanılabilir Alan: {total_mb:.2f} MB{NC}")

    confirm = input(f"\n{RED}Bulunan artık dosyaları silmek istiyor musunuz? (e/n): {NC}").strip().lower()
    if confirm in ['e', 'evet', 'y', 'yes']:
        deleted = 0
        for path, _ in remnants:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                deleted += 1
            except Exception as e:
                print(f"{RED}[!] Silinemedi ({path}): {e}{NC}")
        print(f"\n{GREEN}[✓] {deleted} adet artık klasör/dosya başarıyla temizlendi.{NC}")
    else:
        print(f"{YELLOW}[i] Silme işlemi iptal edildi.{NC}")
    show_module_status()

if __name__ == '__main__':
    scan_remnants()
