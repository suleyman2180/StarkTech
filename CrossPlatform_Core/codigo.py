#!/usr/bin/env python3
# ==============================================================================
# C.O.D.I.G.O. (eski E.D.I.T.H.) - Çapraz Platform Güvenlik Kasası ve Kripto Aracı
# Gerçek AES-256-GCM (authenticated encryption) kullanır.
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================
#
# NOT: Bu dosyanın önceki sürümü "AES-256" olarak etiketlenmişti ama aslında
# basit bir XOR akış şifrelemesi kullanıyordu (bilinen-açık-metin saldırılarına
# ve bit çevirmeye açık, kriptografik olarak zayıf). Artık `cryptography`
# kütüphanesi ile GERÇEK AES-256-GCM kullanılıyor. .edith uzantılı eski
# dosyalar bu sürümle UYUMLU DEĞİLDİR (farklı format/algoritma).
# ==============================================================================

import os
import sys
import hashlib
import secrets
import string

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, NC, run, show_module_status

MAGIC = b"CODIGO1"  # format imzası (7 bayt)
SALT_LEN = 16
NONCE_LEN = 12


def _ensure_cryptography():
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # noqa
        return True
    except ImportError:
        print(f"{YELLOW}[i] 'cryptography' kütüphanesi bulunamadı, yükleniyor...{NC}")
        res = run([sys.executable, "-m", "pip", "install", "cryptography", "-q"],
                  capture_output=False)
        if res is None or res.returncode != 0:
            print(f"{RED}[!] 'cryptography' kütüphanesi yüklenemedi. "
                  f"Manuel olarak kurun: pip install cryptography{NC}")
            return False
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM  # noqa
            return True
        except ImportError:
            return False


def derive_key(passphrase: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac('sha256', passphrase.encode('utf-8'), salt, 200_000, 32)


def encrypt_file(filepath: str, passphrase: str):
    if not os.path.exists(filepath):
        print(f"{RED}[!] Dosya bulunamadı: {filepath}{NC}")
        return
    if not _ensure_cryptography():
        return

    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    salt = secrets.token_bytes(SALT_LEN)
    nonce = secrets.token_bytes(NONCE_LEN)
    key = derive_key(passphrase, salt)
    aesgcm = AESGCM(key)

    with open(filepath, 'rb') as f:
        data = f.read()

    ciphertext = aesgcm.encrypt(nonce, data, None)  # ciphertext içinde 16 baytlık GCM tag'i dahildir

    out_path = filepath + ".codigo"
    with open(out_path, 'wb') as f:
        f.write(MAGIC + salt + nonce + ciphertext)

    print(f"{GREEN}[✓] Dosya AES-256-GCM ile şifrelendi: {out_path}{NC}")


def decrypt_file(filepath: str, passphrase: str):
    if not os.path.exists(filepath):
        print(f"{RED}[!] Dosya bulunamadı: {filepath}{NC}")
        return
    if not _ensure_cryptography():
        return

    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag

    with open(filepath, 'rb') as f:
        content = f.read()

    if len(content) < len(MAGIC) + SALT_LEN + NONCE_LEN or not content.startswith(MAGIC):
        print(f"{RED}[!] Geçersiz veya tanınmayan şifrelenmiş dosya formatı.{NC}")
        return

    offset = len(MAGIC)
    salt = content[offset:offset + SALT_LEN]
    offset += SALT_LEN
    nonce = content[offset:offset + NONCE_LEN]
    offset += NONCE_LEN
    ciphertext = content[offset:]

    key = derive_key(passphrase, salt)
    aesgcm = AESGCM(key)

    try:
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        print(f"{RED}[!] Şifre çözülemedi: yanlış parola veya dosya bozulmuş/değiştirilmiş.{NC}")
        return
    except Exception as e:
        print(f"{RED}[!] Şifre çözme hatası: {e}{NC}")
        return

    out_path = filepath[:-7] if filepath.endswith(".codigo") else filepath + ".cozuldu"
    with open(out_path, 'wb') as f:
        f.write(decrypted)

    print(f"{GREEN}[✓] Dosya başarıyla çözüldü ve doğrulandı: {out_path}{NC}")


def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(chars) for _ in range(length))


def hash_text(text: str):
    sha256 = hashlib.sha256(text.encode('utf-8')).hexdigest()
    sha512 = hashlib.sha512(text.encode('utf-8')).hexdigest()
    return sha256, sha512


def main():
    print(f"{RED}")
    print("  =======================================================")
    print("      C.O.D.I.G.O. Güvenlik Kasası ve AES-256 Kripto     ")
    print("  =======================================================")
    print(f"{NC}")

    while True:
        print("\nC.O.D.I.G.O. Güvenlik İşlemi Seçin:")
        print(" 1) Dosya Şifrele (AES-256-GCM, .codigo)")
        print(" 2) Dosya Şifresini Çöz (.codigo)")
        print(" 3) Yüksek Entropili Güvenli Parola Oluştur")
        print(" 4) Metin Hash'le (SHA-256 / SHA-512)")
        print(" 0) Çıkış")

        choice = input("\nSeçim [0-4]: ").strip()

        if choice == '1':
            fp = input("Dosya yolunu girin: ").strip().strip('"')
            pw = input("Şifreleme parolasını girin: ").strip()
            if fp and pw:
                encrypt_file(fp, pw)
        elif choice == '2':
            fp = input("Şifrelenmiş (.codigo) dosya yolunu girin: ").strip().strip('"')
            pw = input("Şifre çözme parolasını girin: ").strip()
            if fp and pw:
                decrypt_file(fp, pw)
        elif choice == '3':
            try:
                l = int(input("Parola uzunluğu [varsayılan 16]: ") or 16)
            except Exception:
                l = 16
            pwd = generate_password(l)
            print(f"\n{GREEN}[✓] Oluşturulan Güvenli Parola: {pwd}{NC}")
        elif choice == '4':
            txt = input("Hash'lenecek metni girin: ")
            s256, s512 = hash_text(txt)
            print(f"\n{CYAN}SHA-256:{NC} {s256}")
            print(f"{CYAN}SHA-512:{NC} {s512}")
        elif choice == '0':
            print(f"{GREEN}[C.O.D.I.G.O.] Kasa güvenli. Hoşça kalın!{NC}")
            show_module_status()
            break


if __name__ == '__main__':
    main()
