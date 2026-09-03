#!/usr/bin/env python3
# ==============================================================================
# ÖTÜKEN - ANA KONTROL PANELİ v6.0 (Çapraz Platform / Python)
# Linux, Windows ve macOS üzerinde bash gerektirmeden çalışır.
# ==============================================================================

import os
import sys
import platform
import subprocess

CORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CrossPlatform_Core")
sys.path.insert(0, CORE_DIR)

from common import CYAN, RED, GREEN, YELLOW, MAGENTA, BLUE, BOLD, NC, get_os  # noqa: E402

MODULES = [
    ("falcao.py",  CYAN,    "Tam Ağ Cihaz Taraması ve Risk Değerlendirmesi"),
    ("sombra.py",  GREEN,   "Artık Dosya ve Kalıntı Temizleyicisi"),
    ("kor.py",     YELLOW,  "Pil ve Güç Sağlığı Raporlayıcısı"),
    ("mirage.py",  MAGENTA, "Dosya Formatı ve Medya Dönüştürücü Süiti"),
    ("shield.py",  BLUE,    "Güvenlik Duvarı Kural Yöneticisi"),
    ("friday.py",  RED,     "Telegram, E-Posta ve ntfy Bildirim Merkezi"),
    ("jarvis.py",  CYAN,    "Otomatik Yazılım ve Paket Yükleyicisi"),
    ("codigo.py",  RED,     "Güvenlik Kasası ve AES-256 Dosya Şifreleyici"),
    ("vision.py",  BLUE,    "Mükerrer ve Büyük Dosya Analizcisi"),
    ("mark85.py",  YELLOW,  "Zaman Damgalı Otomatik ZIP Arşivleyici"),
    ("veronica.py", RED,    "Ağ Teşhis ve Hızlı Performans Kiti"),
]


def show_platform_banner():
    print(f"[ÖTÜKEN] Platform: {get_os()}")
    print(f"[ÖTÜKEN] Architecture: {platform.machine()}")
    print(f"{GREEN}[ÖTÜKEN] Cross-Platform Core: ONLINE{NC}\n")


def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{RED}{BOLD}")
    print("  =======================================================")
    print("             ÖTÜKEN - TAKTİK SİSTEM MERKEZİ v6.0       ")
    print("  =======================================================")
    print(NC)
    show_platform_banner()
    print(f'{GREEN}[J.A.R.V.I.S.] "Hoş geldiniz. Ötüken çekirdeği aktif. Tüm sistemler hazır."{NC}')
    print("--------------------------------------------------------------------------------")
    for idx, (fname, color, desc) in enumerate(MODULES, 1):
        print(f" {idx:2d}) {color}{fname:<12}{NC} — {desc}")
    print(" 0) Çıkış")
    print("--------------------------------------------------------------------------------")


def run_module(fname):
    path = os.path.join(CORE_DIR, fname)
    if not os.path.exists(path):
        print(f"{RED}[!] Modül bulunamadı: {path}{NC}")
        return
    try:
        subprocess.run([sys.executable, path])
    except Exception as e:
        print(f"{RED}[!] Modül çalıştırılamadı: {e}{NC}")


def main():
    while True:
        show_menu()
        choice = input("\nLütfen Bir Protokol Seçin [0-11]: ").strip()

        if choice == '0':
            print(f'{GREEN}[J.A.R.V.I.S.] "Ötüken güvenli şekilde kapatılıyor. İyi günler."{NC}')
            sys.exit(0)

        if choice.isdigit() and 1 <= int(choice) <= len(MODULES):
            run_module(MODULES[int(choice) - 1][0])
        else:
            print(f"{RED}Geçersiz seçim!{NC}")

        input("\nDevam etmek için Enter'a basın...")


if __name__ == '__main__':
    main()
