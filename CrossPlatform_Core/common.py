#!/usr/bin/env python3
# ==============================================================================
# COMMON - StarkTech Suite Çapraz Platform Çekirdek Yardımcı Kütüphanesi
# Tüm modüller platform algılama, renk ve güvenli komut çalıştırma için
# bu modülü kullanır. Amaç: aynı kodu her modülde tekrar tekrar yazmamak.
# ==============================================================================

import os
import sys
import shutil
import platform
import subprocess

# ------------------------------------------------------------------ Renkler --
_USE_COLOR = sys.stdout.isatty()
CYAN = '\033[0;36m' if _USE_COLOR else ''
GREEN = '\033[0;32m' if _USE_COLOR else ''
YELLOW = '\033[1;33m' if _USE_COLOR else ''
RED = '\033[0;31m' if _USE_COLOR else ''
MAGENTA = '\033[0;35m' if _USE_COLOR else ''
BLUE = '\033[0;34m' if _USE_COLOR else ''
BOLD = '\033[1m' if _USE_COLOR else ''
NC = '\033[0m' if _USE_COLOR else ''

# Windows'un eski cmd.exe konsollarında ANSI kodlarını etkinleştir.
if sys.platform == 'win32' and _USE_COLOR:
    try:
        os.system('')  # Windows 10+ konsolunda VT100 modunu açar
    except Exception:
        pass


# ------------------------------------------------------------- Platform ID --
def get_os():
    """Normalized platform name: 'Linux' | 'Windows' | 'macOS' | 'Other'."""
    system = platform.system().lower()
    if 'darwin' in system:
        return 'macOS'
    if 'win' in system:
        return 'Windows'
    if 'linux' in system:
        return 'Linux'
    return 'Other'


IS_WINDOWS = sys.platform == 'win32'
IS_MACOS = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')


def is_admin():
    """Kullanıcının yönetici/root yetkisine sahip olup olmadığını döndürür."""
    try:
        if IS_WINDOWS:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        return os.geteuid() == 0
    except Exception:
        return False


def unavailable(feature: str, reason: str = ""):
    """Bir özellik bu platformda desteklenmiyorsa standart, anlaşılır uyarı basar."""
    msg = f"{YELLOW}[!] Bu özellik bu sistemde kullanılamıyor: {feature}{NC}"
    if reason:
        msg += f"\n    {YELLOW}Sebep: {reason}{NC}"
    print(msg)


# ------------------------------------------------------- Güvenli komutlar --
def run(cmd, **kwargs):
    """
    subprocess.run için güvenli sarmalayıcı.
    - cmd bir liste OLMALI (shell=True kullanılmaz; komut enjeksiyonu önlenir).
    - Komut sistemde yoksa (FileNotFoundError) çökmek yerine None döner.
    """
    if isinstance(cmd, str):
        raise TypeError("run(): cmd bir liste olmalı, ham shell string değil (güvenlik).")
    kwargs.setdefault('capture_output', True)
    kwargs.setdefault('text', True)
    try:
        return subprocess.run(cmd, **kwargs)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"{RED}[!] Komut çalıştırma hatası ({cmd[0]}): {e}{NC}")
        return None


def tool_exists(name: str) -> bool:
    return shutil.which(name) is not None


def pkg_manager_linux():
    """Sistemde bulunan ilk paket yöneticisini döndürür: apt / dnf / pacman / zypper / None."""
    for mgr in ("apt-get", "apt", "dnf", "yum", "pacman", "zypper"):
        if tool_exists(mgr):
            return mgr
    return None


def elevate_hint():
    """Yönetici yetkisi olmadığında platforma uygun ipucu mesajı döndürür."""
    if IS_WINDOWS:
        return "Bu terminali 'Yönetici olarak çalıştır' ile yeniden açın."
    return "Bu komutu 'sudo' ile çalıştırmayı deneyin."


def show_module_status():
    """Her modülün sonunda üç platform için destek durumunu gösterir."""
    print(f"\n{CYAN}--------------------------------------------------------{NC}")
    print(f"{BOLD}Platform Desteği:{NC}  Linux: {GREEN}✅{NC}   "
          f"Windows: {GREEN}✅{NC}   macOS: {GREEN}✅{NC}")
    print(f"{CYAN}--------------------------------------------------------{NC}")
