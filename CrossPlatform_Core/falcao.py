#!/usr/bin/env python3
# ==============================================================================
# R.E.C.O.N. - Tam Ağ Cihaz Taraması ve Risk Değerlendirmesi
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================

import os
import sys
import socket
import subprocess
import threading
import urllib.request
import json
import re
from concurrent.futures import ThreadPoolExecutor

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import (CYAN, GREEN, YELLOW, RED, MAGENTA, BLUE, BOLD, NC,
                     is_admin, tool_exists, unavailable, show_module_status)

TARGET_PORTS = [21, 22, 23, 80, 443, 445, 3389, 8080, 8443]
vendor_cache = {}

def show_banner():
    print(f"{CYAN}{BOLD}")
    print("  =======================================================")
    print("     R.E.C.O.N.  -  TAM AĞ CİHAZ VE PORT TARAYICI v2.0   ")
    print("  =======================================================")
    print(f"{NC}")
    print(f"{GREEN}[R.E.C.O.N.] \"Yerel ağ üzerindeki tüm cihazlar ve açık portlar taranıyor...\"{NC}\n")

def get_local_ip_and_subnet():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        parts = ip.split('.')
        base_ip = f"{parts[0]}.{parts[1]}.{parts[2]}"
        return ip, base_ip
    except Exception:
        return "127.0.0.1", "127.0.0"

def get_mac_vendor(mac):
    if not mac or mac == "Bilinmiyor":
        return "Bilinmiyor"
    
    clean_mac = mac.upper().replace(':', '').replace('-', '')[:6]
    if clean_mac in vendor_cache:
        return vendor_cache[clean_mac]
    
    try:
        url = f"https://api.macvendors.com/{mac}"
        req = urllib.request.Request(url, headers={'User-Agent': 'RECON-Scanner/2.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            vendor = response.read().decode('utf-8').strip()
            vendor_cache[clean_mac] = vendor
            return vendor
    except Exception:
        vendor_cache[clean_mac] = "Bilinmeyen Üretici"
        return "Bilinmeyen Üretici"

def ping_host(ip):
    param = '-n' if sys.platform == 'win32' else '-c'
    wait_flag = '-w' if sys.platform == 'win32' else '-W'
    wait_time = '500' if sys.platform == 'win32' else '1'
    cmd = ['ping', param, '1', wait_flag, wait_time, ip]
    
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False

def get_arp_table():
    devices = {}
    if not tool_exists('arp'):
        unavailable("ARP/MAC Tablosu Çözümleme", "'arp' komutu bu sistemde bulunamadı.")
        return devices
    try:
        cmd = ['arp', '-a']
        res = subprocess.run(cmd, capture_output=True, text=True, errors='ignore')
        output = res.stdout

        for line in output.splitlines():
            match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+([0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2}[:-][0-9a-fa-f]{2})', line, re.IGNORECASE)
            if match:
                ip, mac = match.group(1), match.group(2)
                mac_formatted = mac.replace('-', ':').upper()
                if not ip.startswith('224.') and not ip.startswith('239.') and ip != '255.255.255.255':
                    devices[ip] = mac_formatted
    except Exception:
        pass
    return devices

def get_hostname(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except Exception:
        return "Bilinmiyor"

def scan_single_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    res = s.connect_ex((ip, port))
    s.close()
    return port if res == 0 else None

def scan_open_ports(ip):
    open_ports = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(scan_single_port, ip, p) for p in TARGET_PORTS]
        for f in futures:
            res = f.result()
            if res:
                open_ports.append(res)
    return open_ports

def scan_network():
    local_ip, base_ip = get_local_ip_and_subnet()
    show_banner()
    
    print(f"{YELLOW}[*] Yerel IP          : {local_ip}{NC}")
    print(f"{YELLOW}[*] Ağ Taraması Alanı  : {base_ip}.1 - {base_ip}.254{NC}")
    print(f"{YELLOW}[*] Yönetici Yetkisi   : {'EVET' if is_admin() else 'HAYIR (Daha kapsamlı sonuç için sudo/admin ile çalıştırın)'}{NC}\n")

    print(f"{CYAN}==> 1/3 Hızlı Cihaz Keşfi (Ping Sweep) başlatılıyor...{NC}")
    
    active_ips = []
    def check_ip(i):
        ip = f"{base_ip}.{i}"
        if ping_host(ip):
            active_ips.append(ip)

    with ThreadPoolExecutor(max_workers=50) as executor:
        for i in range(1, 255):
            executor.submit(check_ip, i)

    print(f"{GREEN}[✓] {len(active_ips)} aktif IP tespit edildi.{NC}\n")
    print(f"{CYAN}==> 2/3 MAC Tablosu ve Cihaz Detayları Çözümleniyor...{NC}")

    arp_table = get_arp_table()

    if local_ip not in active_ips:
        active_ips.append(local_ip)

    results = []

    print(f"{CYAN}==> 3/3 Port ve Risk Analizi Yapılıyor...{NC}\n")
    
    for ip in sorted(active_ips, key=lambda x: [int(part) for part in x.split('.')]):
        mac = arp_table.get(ip, "Bilinmiyor")
        hostname = get_hostname(ip)
        vendor = get_mac_vendor(mac) if mac != "Bilinmiyor" else ("Yerel Cihaz" if ip == local_ip else "Bilinmiyor")
        open_ports = scan_open_ports(ip)

        risk = "DÜŞÜK"
        risk_color = GREEN
        if 23 in open_ports or 445 in open_ports or 3389 in open_ports:
            risk = "YÜKSEK (SMB/Telnet/RDP)"
            risk_color = RED
        elif open_ports:
            risk = "ORTA"
            risk_color = YELLOW

        results.append({
            "ip": ip,
            "mac": mac,
            "hostname": hostname,
            "vendor": vendor,
            "ports": open_ports,
            "risk": risk,
            "risk_color": risk_color
        })

    print(f"{CYAN}" + "="*105 + f"{NC}")
    print(f"{BOLD}{'IP Adresi':<16} | {'MAC Adresi':<18} | {'Üretici / Cihaz':<22} | {'Açık Portlar':<18} | {'Risk Seviyesi'}{NC}")
    print(f"{CYAN}" + "="*105 + f"{NC}")

    for r in results:
        ports_str = ', '.join(map(str, r['ports'])) if r['ports'] else 'Yok'
        print(f"{r['ip']:<16} | {r['mac']:<18} | {r['vendor']:<22.22} | {ports_str:<18} | {r['risk_color']}{r['risk']}{NC}")

    print(f"{CYAN}" + "="*105 + f"{NC}\n")
    print(f"{GREEN}[✓] R.E.C.O.N. Ağ Taraması Başarıyla Tamamlandı! Toplam Cihaz: {len(results)}{NC}")
    show_module_status()

    return results

if __name__ == '__main__':
    scan_network()
