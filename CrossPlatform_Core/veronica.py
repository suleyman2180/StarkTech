#!/usr/bin/env python3
# ==============================================================================
# VERONICA (HULKBUSTER) - Çapraz Platform Ağ Teşhis Kiti
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================

import os
import socket
import subprocess
import sys
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, NC, IS_WINDOWS, show_module_status

def get_public_ip():
    try:
        req = urllib.request.urlopen("https://api.ipify.org", timeout=5)
        return req.read().decode('utf-8')
    except:
        return "Kullanılamıyor"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def ping_host(host):
    param = '-n' if IS_WINDOWS else '-c'
    cmd = ['ping', param, '3', host]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0, res.stdout
    except Exception as e:
        return False, str(e)

def scan_ports(target_host, ports=[21, 22, 80, 443, 3306, 8080, 25565]):
    print(f"\n{CYAN}==> '{target_host}' hedefi taranıyor, açık portlar aranıyor...{NC}")
    try:
        target_ip = socket.gethostbyname(target_host)
        print(f"{YELLOW}Çözümlenen IP: {target_ip}{NC}\n")
    except Exception as e:
        print(f"{RED}[!] Alan adı çözümlemesi başarısız: {e}{NC}")
        return

    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        res = s.connect_ex((target_ip, p))
        if res == 0:
            print(f"{GREEN}[✓] Port {p:<5} : AÇIK{NC}")
        else:
            print(f"{RED}[x] Port {p:<5} : KAPALI / FİLTRELİ{NC}")
        s.close()

def main():
    print(f"{RED}")
    print("  =======================================================")
    print("     VERONICA Çapraz Platform Taktik Ağ Kiti             ")
    print("  =======================================================")
    print(f"{NC}")

    while True:
        print("\nVERONICA İşlemi Seçin:")
        print(" 1) IP Adreslerini Göster (Yerel ve Genel)")
        print(" 2) Ping Gecikme Testi (Google, Cloudflare)")
        print(" 3) Hızlı Port Tarayıcı")
        print(" 4) DNS Alan Adı Çözümleyici")
        print(" 0) Çıkış")

        choice = input("\nSeçim [0-4]: ").strip()

        if choice == '1':
            print(f"\n{CYAN}Yerel IP Adresi  :{NC} {get_local_ip()}")
            print(f"{CYAN}Genel IP Adresi  :{NC} {get_public_ip()}")
        elif choice == '2':
            for h in ["8.8.8.8", "1.1.1.1", "google.com"]:
                print(f"\n{CYAN}{h} ping atılıyor...{NC}")
                ok, output = ping_host(h)
                if ok:
                    print(f"{GREEN}[✓] Ping Başarılı:{NC}")
                    print(output.splitlines()[-1] if output else "TAMAM")
                else:
                    print(f"{RED}[x] {h} ping başarısız{NC}")
        elif choice == '3':
            host = input("Hedef alan adı veya IP [varsayılan localhost]: ").strip() or "localhost"
            scan_ports(host)
        elif choice == '4':
            dom = input("Alan adı girin (örn: serup.com.tr): ").strip()
            if dom:
                try:
                    ip = socket.gethostbyname(dom)
                    print(f"{GREEN}[✓] '{dom}' -> {ip}{NC}")
                except Exception as e:
                    print(f"{RED}[!] Çözümleme hatası: {e}{NC}")
        elif choice == '0':
            print(f"{GREEN}[VERONICA] Ağ teşhisi tamamlandı.{NC}")
            show_module_status()
            break

if __name__ == '__main__':
    main()
