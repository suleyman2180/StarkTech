#!/usr/bin/env python3
# ==============================================================================
# A.R.C. - Pil ve Güç Sağlığı Raporlayıcısı
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================

import os
import re
import sys
import xml.etree.ElementTree as ET

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, BOLD, NC, get_os, run, tool_exists, show_module_status


def get_battery_linux():
    bat_path = "/sys/class/power_supply/BAT0"
    if not os.path.exists(bat_path):
        bat_path = "/sys/class/power_supply/BAT1"
    if not os.path.exists(bat_path):
        return None

    def read_val(filename):
        p = os.path.join(bat_path, filename)
        if os.path.exists(p):
            with open(p, "r") as f:
                return f.read().strip()
        return None

    full_design = read_val("energy_full_design") or read_val("charge_full_design")
    full_actual = read_val("energy_full") or read_val("charge_full")
    cycle_count = read_val("cycle_count") or "Bilinmiyor"
    status = read_val("status") or "Bilinmiyor"
    capacity = read_val("capacity") or "Bilinmiyor"

    health_pct = 100.0
    if full_design and full_actual:
        try:
            health_pct = (float(full_actual) / float(full_design)) * 100
        except Exception:
            health_pct = 100.0

    return {
        "status": status,
        "capacity_pct": f"{capacity}%",
        "health_pct": health_pct,
        "cycle_count": cycle_count,
        "full_actual": f"{int(full_actual)/1000:.0f} mWh/mAh" if full_actual else "Bilinmiyor",
        "full_design": f"{int(full_design)/1000:.0f} mWh/mAh" if full_design else "Bilinmiyor"
    }


def get_battery_mac():
    res = run(["system_profiler", "SPPowerDataType"])
    if res is None or res.returncode != 0:
        return None
    out = res.stdout
    cycle_match = re.search(r"Cycle Count:\s*(\d+)", out)
    condition_match = re.search(r"Condition:\s*(.*)", out)
    max_cap_match = re.search(r"Full Charge Capacity \(mAh\):\s*(\d+)", out)
    charge_match = re.search(r"State of Charge \(%\):\s*(\d+)", out)

    if not cycle_match and not condition_match and not max_cap_match:
        return None  # Muhtemelen pilsiz bir masaüstü Mac

    cycles = cycle_match.group(1) if cycle_match else "Bilinmiyor"
    condition = condition_match.group(1).strip() if condition_match else "Bilinmiyor"
    max_cap = max_cap_match.group(1) if max_cap_match else None
    charge_pct = f"{charge_match.group(1)}%" if charge_match else "Bilinmiyor"

    health_pct = 100.0
    if condition and not condition.lower().startswith("normal") and condition != "Bilinmiyor":
        health_pct = 60.0  # "Service Recommended" / "Replace Now" vb.

    return {
        "status": condition,
        "capacity_pct": charge_pct,
        "health_pct": health_pct,
        "cycle_count": cycles,
        "full_actual": f"{max_cap} mAh" if max_cap else "Bilinmiyor",
        "full_design": "Bilinmiyor (macOS bu değeri açığa çıkarmıyor)"
    }


def get_battery_win():
    """
    1) PowerShell + CIM (Win32_Battery): anlık şarj yüzdesi/durumu.
    2) powercfg /batteryreport /xml: tasarım/tam kapasite ve döngü sayısı
       (XML gerçekten ayrıştırılır; sabit/uydurma değer kullanılmaz).
    """
    if not (tool_exists("powershell") or tool_exists("powershell.exe")):
        return None

    status = "Bilinmiyor"
    capacity_pct = "Bilinmiyor"
    ps_cmd = [
        "powershell", "-NoProfile", "-Command",
        "(Get-CimInstance Win32_Battery | Select-Object -First 1 "
        "EstimatedChargeRemaining,BatteryStatus | ConvertTo-Json -Compress)"
    ]
    res = run(ps_cmd)
    if res and res.returncode == 0 and res.stdout.strip():
        try:
            import json
            data = json.loads(res.stdout.strip())
            if data:
                capacity_pct = f"{data.get('EstimatedChargeRemaining', '?')}%"
                bstatus = data.get('BatteryStatus')
                status_map = {1: "Boşalıyor", 2: "AC Güç (Tam)", 3: "Tam Şarjlı",
                              4: "Düşük", 5: "Kritik", 6: "Şarj Oluyor"}
                status = status_map.get(bstatus, f"Kod {bstatus}")
        except Exception:
            pass

    if capacity_pct == "Bilinmiyor" and status == "Bilinmiyor":
        return None  # Muhtemelen pilsiz masaüstü sistem

    cycle_count = "Bilinmiyor"
    full_actual = "Bilinmiyor"
    full_design = "Bilinmiyor"
    health_pct = 100.0

    try:
        report_path = os.path.join(os.environ.get("TEMP", "."), "starktech_battery_report.xml")
        run(["powercfg", "/batteryreport", "/xml", "/output", report_path])
        if os.path.exists(report_path):
            root = ET.parse(report_path).getroot()

            def find_first(tagname):
                for elem in root.iter():
                    if elem.tag.endswith(tagname):
                        return elem
                return None

            design_el = find_first("DesignCapacity")
            full_el = find_first("FullChargeCapacity")
            cycle_el = find_first("CycleCount")

            if design_el is not None and design_el.text:
                full_design = f"{int(design_el.text) / 1000:.0f} mWh"
            if full_el is not None and full_el.text:
                full_actual = f"{int(full_el.text) / 1000:.0f} mWh"
            if cycle_el is not None and cycle_el.text:
                cycle_count = cycle_el.text
            if design_el is not None and full_el is not None:
                try:
                    health_pct = (float(full_el.text) / float(design_el.text)) * 100
                except Exception:
                    pass
            try:
                os.remove(report_path)
            except Exception:
                pass
    except Exception:
        pass  # powercfg raporu bazı Windows sürümlerinde/izinlerde çalışmayabilir

    return {
        "status": status,
        "capacity_pct": capacity_pct,
        "health_pct": health_pct,
        "cycle_count": cycle_count,
        "full_actual": full_actual,
        "full_design": full_design
    }


def report_battery():
    system = get_os()
    print(CYAN)
    print("  =======================================================")
    print("     A.R.C.  -  PİL ve GÜÇ SAĞLIĞI RAPORLAYICISI v1.0     ")
    print("  =======================================================")
    print(NC)

    if system == "Windows":
        info = get_battery_win()
    elif system == "macOS":
        info = get_battery_mac()
    else:
        info = get_battery_linux()

    if not info:
        print(f"{YELLOW}[!] Bu cihazda pil (Batarya) tespit edilemedi veya Masaüstü sistem kullanılıyor.{NC}")
        show_module_status()
        return

    print(f"{CYAN}--- A.R.C. GÜÇ KONTROL RAPORU ---{NC}")
    print(f"{YELLOW} Şarj Durumu          :{NC} {info['status']} ({info['capacity_pct']})")
    print(f"{YELLOW} Pil Sağlığı Yüzdesi   :{NC} %{info['health_pct']:.1f}")
    print(f"{YELLOW} Pil Döngü Sayısı      :{NC} {info['cycle_count']}")
    print(f"{YELLOW} Mevcut Tam Kapasite   :{NC} {info['full_actual']}")
    print(f"{YELLOW} Tasarım Kapasitesi    :{NC} {info['full_design']}")
    print("--------------------------------------------------------")

    hp = info["health_pct"]
    if hp >= 85:
        recommendation = f"{GREEN}[✓] Pil Sağlığı Mükemmel. Değişime gerek yok.{NC}"
    elif hp >= 70:
        recommendation = f"{YELLOW}[!] Pil Sağlığı Orta Düzeyde (%{hp:.1f}). Kullanıma uygun.{NC}"
    else:
        recommendation = f"{RED}[!] UYARI: Pil Sağlığı Düşük (%{hp:.1f}). Yakın zamanda pil değişimi önerilir!{NC}"

    print(f"{BOLD}TEŞHİS & ÖNERİ:{NC} " + recommendation)
    print()
    show_module_status()


if __name__ == '__main__':
    report_battery()
