#!/usr/bin/env python3
# ==============================================================================
# J.A.R.V.I.S. - Evrensel Çapraz Platform Paket ve Çalışma Alanı Yükleyici
# Desteklenen Sistemler: Windows, macOS, Linux (apt/dnf/pacman otomatik algılama)
# ==============================================================================

import os
import sys
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, NC, get_os, run, tool_exists, pkg_manager_linux, show_module_status


def show_banner():
    os_type = get_os()
    print(f"{CYAN}")
    print("  =======================================================")
    print("     J.A.R.V.I.S. Çapraz Platform Yazılım Yükleyici      ")
    print("  =======================================================")
    print(f"{NC}")
    print(f'{GREEN}[J.A.R.V.I.S.] "İyi günler, Efendim. Tespit Edilen İşletim Sistemi: {os_type}"{NC}\n')


def run_cmd(cmd):
    """cmd bir liste olmalı; shell=True kullanılmaz (komut enjeksiyonuna karşı güvenli)."""
    print(f"{YELLOW}[KOMUT] {' '.join(cmd)}{NC}")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print(f"{RED}[!] Komut bulunamadı: {cmd[0]}{NC}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}[!] Komut hatayla sonuçlandı (kod {e.returncode}): {' '.join(cmd)}{NC}")
    except Exception as e:
        print(f"{RED}[!] Komut çalıştırma hatası: {e}{NC}")


def install_mac():
    print(f"{CYAN}macOS üzerinde Homebrew kontrol ediliyor...{NC}")
    if not tool_exists("brew"):
        print(f"{YELLOW}Homebrew bulunamadı. Lütfen önce şu adresten kurun: https://brew.sh{NC}")
        return

    tools = ["git", "python", "node", "docker", "visual-studio-code", "vlc", "htop"]
    print("\nHomebrew ile kurulacak yazılımları seçin:")
    for idx, t in enumerate(tools, 1):
        print(f" {idx}) {t}")

    sel = input("\nKurulacak numaraları boşlukla ayırarak girin (örn: 1 2 5): ").strip().split()
    for s in sel:
        if s.isdigit() and 1 <= int(s) <= len(tools):
            tool = tools[int(s) - 1]
            print(f"\n{GREEN}{tool} yükleniyor...{NC}")
            res = subprocess.run(["brew", "install", tool])
            if res.returncode != 0:
                run_cmd(["brew", "install", "--cask", tool])


def install_win():
    print(f"{CYAN}Windows üzerinde Winget kontrol ediliyor...{NC}")
    if not tool_exists("winget"):
        print(f"{YELLOW}[!] winget bulunamadı. Windows 10 1709+ / Windows 11 ve App Installer gereklidir.{NC}")
        return

    tools = [
        ("Git.Git", "Git for Windows"),
        ("Python.Python.3.12", "Python 3.12"),
        ("Microsoft.VisualStudioCode", "VS Code"),
        ("Docker.DockerDesktop", "Docker Desktop"),
        ("Google.Chrome", "Google Chrome"),
        ("VideoLAN.VLC", "VLC Media Player"),
    ]
    print("\nWinget ile kurulacak yazılımları seçin:")
    for idx, (pkg, name) in enumerate(tools, 1):
        print(f" {idx}) {name} [{pkg}]")

    sel = input("\nKurulacak numaraları boşlukla ayırarak girin (örn: 1 3): ").strip().split()
    for s in sel:
        if s.isdigit() and 1 <= int(s) <= len(tools):
            pkg, name = tools[int(s) - 1]
            print(f"\n{GREEN}{name} yükleniyor...{NC}")
            run_cmd(["winget", "install", "--id", pkg, "-e",
                      "--accept-source-agreements", "--accept-package-agreements"])


# Her paket yöneticisi için: (kurulum bayrağı, güncelleme komutu)
_LINUX_INSTALL = {
    "apt-get": (["install", "-y"], ["update"]),
    "apt": (["install", "-y"], ["update"]),
    "dnf": (["install", "-y"], None),
    "yum": (["install", "-y"], None),
    "pacman": (["-S", "--noconfirm"], ["-Sy"]),
    "zypper": (["install", "-y"], None),
}

# Paket adları dağıtıma göre değişebilir; en yaygın (Debian/Ubuntu) isimler
# varsayılan olarak kullanılır. DNF/pacman/zypper'da bazı paket adları farklı
# olabilir; bulunamazsa J.A.R.V.I.S. hatayı gösterip devam eder.
_LINUX_TOOLS = ["build-essential", "git", "curl", "wget", "python3-pip",
                 "python3-venv", "docker.io", "code", "vlc", "htop", "fastfetch"]


def install_linux():
    mgr = pkg_manager_linux()
    if not mgr:
        print(f"{RED}[!] Desteklenen bir paket yöneticisi bulunamadı "
              f"(apt/dnf/yum/pacman/zypper).{NC}")
        return

    print(f"{CYAN}Linux üzerinde {mgr} Paket Yöneticisi tespit edildi.{NC}")
    print("\nKurulacak yazılımları seçin:")
    for idx, t in enumerate(_LINUX_TOOLS, 1):
        print(f" {idx}) {t}")

    sel = input("\nKurulacak numaraları boşlukla ayırarak girin (örn: 1 2 3): ").strip().split()
    selected_pkgs = [_LINUX_TOOLS[int(s) - 1] for s in sel
                      if s.isdigit() and 1 <= int(s) <= len(_LINUX_TOOLS)]

    if not selected_pkgs:
        return

    install_flags, update_cmd = _LINUX_INSTALL[mgr]
    needs_sudo = os.geteuid() != 0 if hasattr(os, 'geteuid') else False
    sudo_prefix = ["sudo"] if needs_sudo else []

    if update_cmd:
        print(f"\n{CYAN}Paket listesi güncelleniyor...{NC}")
        run_cmd(sudo_prefix + [mgr] + update_cmd)

    print(f"\n{GREEN}Seçilen paketler kuruluyor: {', '.join(selected_pkgs)}{NC}")
    run_cmd(sudo_prefix + [mgr] + install_flags + selected_pkgs)


def main():
    show_banner()
    os_type = get_os()
    if os_type == 'macOS':
        install_mac()
    elif os_type == 'Windows':
        install_win()
    elif os_type == 'Linux':
        install_linux()
    else:
        print(f"{RED}[!] Bilinmeyen/desteklenmeyen platform.{NC}")

    print(f'\n{GREEN}[J.A.R.V.I.S.] "Kurulum protokolü tamamlandı, Efendim."{NC}')
    show_module_status()


if __name__ == '__main__':
    main()
