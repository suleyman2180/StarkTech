#!/usr/bin/env python3
# ==============================================================================
# S.H.I.E.L.D. - Güvenlik Duvarı & Taktik Savunma Yöneticisi
# Desteklenen Sistemler: Windows (netsh), macOS (pfctl/socketfilterfw), Linux (ufw)
# ==============================================================================

import os
import sys
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, YELLOW, RED, BLUE, NC, get_os, is_admin, tool_exists, unavailable, show_module_status


def show_banner():
    print(f"{BLUE}")
    print("  =======================================================")
    print("     S.H.I.E.L.D.  -  GÜVENLİK DUVARI YÖNETİCİSİ v1.0   ")
    print("  =======================================================")
    print(f"{NC}")


def _valid_port(port: str) -> bool:
    """Sadece rakam veya rakam/tcp|udp biçimini kabul eder (komut enjeksiyonunu önler)."""
    if not port:
        return False
    core = port.split('/')[0]
    return core.isdigit() and 1 <= int(core) <= 65535


def run_list(cmd):
    """Liste tabanlı, shell=True KULLANMAYAN güvenli komut çalıştırıcı."""
    print(f"{YELLOW}[KOMUT] {' '.join(cmd)}{NC}")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0 and res.stderr:
            print(f"{RED}{res.stderr}{NC}")
    except FileNotFoundError:
        print(f"{RED}[!] Komut bulunamadı: {cmd[0]}{NC}")
    except Exception as e:
        print(f"{RED}[!] Hata: {e}{NC}")


def win_firewall():
    if not tool_exists("netsh"):
        unavailable("Windows Güvenlik Duvarı Yönetimi", "netsh bulunamadı.")
        return

    print(f"{CYAN}==> Windows Güvenlik Duvarı (netsh advfirewall) Menüsü{NC}")
    print(" 1) Kuralları Listele")
    print(" 2) Port İzni Ekle (Gelen - İzin Ver)")
    print(" 3) Port Engel Ekle (Gelen - Engelle)")
    print(" 4) Güvenlik Duvarı Durumunu Göster")
    choice = input("\nSeçiminiz [1-4]: ").strip()

    if choice == '1':
        run_list(["netsh", "advfirewall", "firewall", "show", "rule", "name=all"])
    elif choice == '2':
        port = input("İzin verilecek Port (ör: 8080): ").strip()
        if not _valid_port(port):
            print(f"{RED}[!] Geçersiz port. Yalnızca 1-65535 arası sayı girin.{NC}")
            return
        name = input("Kural Adı: ").strip() or f"ALLOW_PORT_{port}"
        run_list(["netsh", "advfirewall", "firewall", "add", "rule",
                   f"name={name}", "dir=in", "action=allow", "protocol=TCP", f"localport={port}"])
    elif choice == '3':
        port = input("Engellenecek Port (ör: 445): ").strip()
        if not _valid_port(port):
            print(f"{RED}[!] Geçersiz port. Yalnızca 1-65535 arası sayı girin.{NC}")
            return
        name = input("Kural Adı: ").strip() or f"BLOCK_PORT_{port}"
        run_list(["netsh", "advfirewall", "firewall", "add", "rule",
                   f"name={name}", "dir=in", "action=block", "protocol=TCP", f"localport={port}"])
    elif choice == '4':
        run_list(["netsh", "advfirewall", "show", "allprofiles"])


def mac_firewall():
    socketfilterfw = "/usr/libexec/ApplicationFirewall/socketfilterfw"
    if not os.path.exists(socketfilterfw):
        unavailable("macOS Uygulama Güvenlik Duvarı", f"{socketfilterfw} bulunamadı.")
        return

    print(f"{CYAN}==> macOS Güvenlik Duvarı (socketfilterfw) Menüsü{NC}")
    run_list(["sudo", socketfilterfw, "--getglobalstate"])
    print("\n 1) Güvenlik Duvarını Aç")
    print(" 2) Güvenlik Duvarını Kapat")
    choice = input("Seçiminiz: ").strip()
    if choice == '1':
        run_list(["sudo", socketfilterfw, "--setglobalstate", "on"])
    elif choice == '2':
        run_list(["sudo", socketfilterfw, "--setglobalstate", "off"])


def linux_firewall():
    if not tool_exists("ufw"):
        unavailable("Linux Güvenlik Duvarı (UFW) Yönetimi",
                     "ufw bulunamadı. iptables/firewalld ile manuel yönetim gerekebilir.")
        return

    print(f"{CYAN}==> Linux Güvenlik Duvarı (UFW) Menüsü{NC}")
    run_list(["sudo", "ufw", "status", "verbose"])
    print("\n 1) Port İzni Ekle (ufw allow)")
    print(" 2) Port Engelle (ufw deny)")
    print(" 3) Güvenlik Duvarını Aç (ufw enable)")
    print(" 4) Güvenlik Duvarını Kapat (ufw disable)")
    choice = input("\nSeçiminiz [1-4]: ").strip()

    if choice == '1':
        port = input("İzin verilecek Port / Servis (ör: 22 veya 80/tcp): ").strip()
        if not _valid_port(port):
            print(f"{RED}[!] Geçersiz port/servis biçimi.{NC}")
            return
        run_list(["sudo", "ufw", "allow", port])
    elif choice == '2':
        port = input("Engellenecek Port / Servis (ör: 23): ").strip()
        if not _valid_port(port):
            print(f"{RED}[!] Geçersiz port/servis biçimi.{NC}")
            return
        run_list(["sudo", "ufw", "deny", port])
    elif choice == '3':
        run_list(["sudo", "ufw", "enable"])
    elif choice == '4':
        run_list(["sudo", "ufw", "disable"])


def main():
    show_banner()
    if not is_admin():
        print(f"{YELLOW}[!] UYARI: Güvenlik duvarı kural değişiklikleri için "
              f"Yönetici (Sudo / Admin) yetkisi gereklidir.{NC}\n")

    system = get_os()
    if system == 'Windows':
        win_firewall()
    elif system == 'macOS':
        mac_firewall()
    elif system == 'Linux':
        linux_firewall()
    else:
        unavailable("Güvenlik Duvarı Yönetimi", "Bilinmeyen işletim sistemi.")
    show_module_status()


if __name__ == '__main__':
    main()
