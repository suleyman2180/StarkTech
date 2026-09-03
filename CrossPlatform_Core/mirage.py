#!/usr/bin/env python3
# ==============================================================================
# M.I.R.A.G.E. - Evrensel Dosya Formatı ve Medya Dönüştürücü
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================

import os
import sys
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import (CYAN, GREEN, YELLOW, RED, MAGENTA, NC,
                     tool_exists, unavailable, show_module_status)

def convert_images_pil(folder_path, target_ext):
    try:
        from PIL import Image
    except ImportError:
        print(f"{YELLOW}[i] PIL (Pillow) kütüphanesi yükleniyor...{NC}")
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
        from PIL import Image

    supported_exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')
    target_ext = target_ext.lower().replace('.', '')

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]
    if not files:
        print(f"{YELLOW}[!] Dönüştürülecek resim dosyası bulunamadı.{NC}")
        return

    out_dir = os.path.join(folder_path, f"donusturulen_{target_ext}")
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{CYAN}==> {len(files)} adet resim .{target_ext} formatına dönüştürülüyor...{NC}")
    converted = 0
    for f in files:
        src = os.path.join(folder_path, f)
        base = os.path.splitext(f)[0]
        dst = os.path.join(out_dir, f"{base}.{target_ext}")
        try:
            with Image.open(src) as img:
                if target_ext in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.save(dst)
                converted += 1
                print(f"{GREEN}[✓] {f} -> {base}.{target_ext}{NC}")
        except Exception as e:
            print(f"{RED}[!] Dönüştürme hatası ({f}): {e}{NC}")

    print(f"\n{GREEN}[✓] Toplam {converted} resim dönüştürüldü. Klasör: {out_dir}{NC}")

def convert_media_ffmpeg(folder_path, target_ext):
    if not tool_exists("ffmpeg"):
        unavailable("Medya/Video/Ses Dönüştürme", "ffmpeg bulunamadı. Lütfen ffmpeg yükleyin.")
        return

    target_ext = target_ext.lower().replace('.', '')
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    out_dir = os.path.join(folder_path, f"donusturulen_{target_ext}")
    os.makedirs(out_dir, exist_ok=True)

    for f in files:
        src = os.path.join(folder_path, f)
        base = os.path.splitext(f)[0]
        dst = os.path.join(out_dir, f"{base}.{target_ext}")
        cmd = ['ffmpeg', '-i', src, '-y', dst]
        print(f"{CYAN}Dönüştürülüyor: {f} -> {target_ext}{NC}")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print(f"{MAGENTA}")
    print("  =======================================================")
    print("     M.I.R.A.G.E.  -  DOSYA FORMAT DÖNÜŞTÜRÜCÜ SÜİTİ     ")
    print("  =======================================================")
    print(f"{NC}")

    print("Dönüştürme Türünü Seçiniz:")
    print(" 1) Toplu Resim Formatı Dönüştürücü (PNG, JPG, WEBP, BMP)")
    print(" 2) Toplu Medya / Video / Ses Dönüştürücü (FFmpeg)")
    print(" 0) Çıkış")

    choice = input("\nSeçiminiz [0-2]: ").strip()

    if choice == '1':
        folder = input("Resimlerin bulunduğu klasör yolu: ").strip().strip('"')
        if os.path.exists(folder):
            fmt = input("Hedef Format (jpg / png / webp / bmp): ").strip()
            convert_images_pil(folder, fmt)
        else:
            print(f"{RED}[!] Klasör bulunamadı.{NC}")
    elif choice == '2':
        folder = input("Medya dosyalarının bulunduğu klasör yolu: ").strip().strip('"')
        if os.path.exists(folder):
            fmt = input("Hedef Format (mp4 / mp3 / mkv / avi): ").strip()
            convert_media_ffmpeg(folder, fmt)
        else:
            print(f"{RED}[!] Klasör bulunamadı.{NC}")

    show_module_status()

if __name__ == '__main__':
    main()
