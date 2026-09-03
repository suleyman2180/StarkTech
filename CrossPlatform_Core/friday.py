#!/usr/bin/env python3
# ==============================================================================
# F.R.I.D.A.Y.-Notify - Uyarı ve Bildirim Merkezi
# Telegram + SMTP E-Posta + ntfy Entegrasyonu
# Desteklenen Sistemler: Windows, macOS, Linux
# ==============================================================================

import os
import sys
import json
import urllib.request
import urllib.parse
import smtplib
from email.mime.text import MIMEText

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from common import CYAN, GREEN, YELLOW, RED, NC, show_module_status

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "friday_config.json"
)

DEFAULT_CONFIG = {
    "telegram": {
        "enabled": False,
        "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
    },
    "email": {
        "enabled": False,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your_email@gmail.com",
        "sender_password": "your_app_password",
        "receiver_email": "receiver@gmail.com"
    },
    "ntfy": {
        "enabled": False,
        "server": "https://ntfy.sh",
        "topic": "YOUR_PRIVATE_NTFY_TOPIC"
    }
}


class FridayNotify:

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
            return DEFAULT_CONFIG

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Eski config dosyaları için ntfy bölümünü otomatik ekle
            if "ntfy" not in config:
                config["ntfy"] = DEFAULT_CONFIG["ntfy"]

            return config

        except Exception:
            return DEFAULT_CONFIG

    # ==========================================================================
    # TELEGRAM
    # ==========================================================================

    def send_telegram(self, message: str) -> bool:
        tg_conf = self.config.get("telegram", {})

        if not tg_conf.get("enabled"):
            print(
                f"{YELLOW}[F.R.I.D.A.Y.-Notify] "
                f"Telegram bildirimleri pasif.{NC}"
            )
            return False

        token = tg_conf.get("bot_token")
        chat_id = tg_conf.get("chat_id")

        if (
            not token
            or not chat_id
            or token == "YOUR_TELEGRAM_BOT_TOKEN"
        ):
            print(
                f"{RED}[!] Telegram bot token veya "
                f"chat_id yapılandırılmamış.{NC}"
            )
            return False

        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"

            data = urllib.parse.urlencode({
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }).encode("utf-8")

            req = urllib.request.Request(url, data=data)

            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    print(
                        f"{GREEN}[✓] Telegram bildirimi "
                        f"başarıyla gönderildi.{NC}"
                    )
                    return True

        except Exception as e:
            print(
                f"{RED}[!] Telegram gönderim hatası: "
                f"{e}{NC}"
            )

        return False

    # ==========================================================================
    # E-POSTA
    # ==========================================================================

    def send_email(self, subject: str, body: str) -> bool:
        em_conf = self.config.get("email", {})

        if not em_conf.get("enabled"):
            print(
                f"{YELLOW}[F.R.I.D.A.Y.-Notify] "
                f"E-posta bildirimleri pasif.{NC}"
            )
            return False

        try:
            msg = MIMEText(body, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = em_conf['sender_email']
            msg['To'] = em_conf['receiver_email']

            server = smtplib.SMTP(
                em_conf['smtp_server'],
                em_conf['smtp_port']
            )

            server.starttls()

            server.login(
                em_conf['sender_email'],
                em_conf['sender_password']
            )

            server.send_message(msg)
            server.quit()

            print(
                f"{GREEN}[✓] E-posta bildirimi gönderildi: "
                f"{em_conf['receiver_email']}{NC}"
            )

            return True

        except Exception as e:
            print(
                f"{RED}[!] E-posta gönderim hatası: "
                f"{e}{NC}"
            )

            return False

    # ==========================================================================
    # NTFY
    # ==========================================================================

    def send_ntfy(self, title: str, message: str) -> bool:
        ntfy_conf = self.config.get("ntfy", {})

        if not ntfy_conf.get("enabled"):
            print(
                f"{YELLOW}[F.R.I.D.A.Y.-Notify] "
                f"ntfy bildirimleri pasif.{NC}"
            )
            return False

        server = ntfy_conf.get(
            "server",
            "https://ntfy.sh"
        ).rstrip("/")

        topic = ntfy_conf.get("topic")

        if (
            not topic
            or topic == "YOUR_PRIVATE_NTFY_TOPIC"
        ):
            print(
                f"{RED}[!] ntfy topic yapılandırılmamış.{NC}"
            )
            return False

        try:
            url = f"{server}/{topic}"

            data = message.encode("utf-8")

            req = urllib.request.Request(
                url,
                data=data,
                method="POST"
            )

            req.add_header(
                "Title",
                title
            )

            req.add_header(
                "Priority",
                "default"
            )

            req.add_header(
                "Tags",
                "warning"
            )

            with urllib.request.urlopen(
                req,
                timeout=10
            ) as resp:

                if 200 <= resp.status < 300:
                    print(
                        f"{GREEN}[✓] ntfy bildirimi "
                        f"başarıyla gönderildi.{NC}"
                    )
                    return True

        except Exception as e:
            print(
                f"{RED}[!] ntfy gönderim hatası: "
                f"{e}{NC}"
            )

        return False

    # ==========================================================================
    # TÜM BİLDİRİM KANALLARI
    # ==========================================================================

    def notify(self, title: str, text: str):

        full_msg = f"🚨 *{title}*\n\n{text}"

        print(
            f"\n{CYAN}"
            f"[F.R.I.D.A.Y.-Notify] "
            f"Bildirim İşleniyor: {title}"
            f"{NC}"
        )

        self.send_telegram(full_msg)
        self.send_email(title, text)
        self.send_ntfy(title, text)


# ==============================================================================
# ANA MENÜ
# ==============================================================================

def main():

    print(f"{CYAN}")
    print("  =======================================================")
    print("     F.R.I.D.A.Y.-Notify - UYARI ve BİLDİRİM MERKEZİ")
    print("  =======================================================")
    print(f"{NC}")

    notifier = FridayNotify()

    print(
        f"Yapılandırma Dosyası: "
        f"{CONFIG_FILE}\n"
    )

    print(" 1) Test Telegram Bildirimi Gönder")
    print(" 2) Test E-Posta Gönder")
    print(" 3) Test ntfy Bildirimi Gönder")
    print(" 4) Konfigürasyon Dosyasını Göster")
    print(" 0) Çıkış")

    choice = input("\nSeçiminiz [0-4]: ").strip()

    if choice == '1':

        msg = (
            input("Gönderilecek mesaj: ").strip()
            or "FRIDAY-Notify Telegram Test Bildirimi"
        )

        notifier.send_telegram(msg)

    elif choice == '2':

        subj = (
            input("E-Posta Konusu: ").strip()
            or "FRIDAY Test Uyarısı"
        )

        body = (
            input("E-Posta İçeriği: ").strip()
            or "Bu bir test e-postasıdır."
        )

        notifier.send_email(subj, body)

    elif choice == '3':

        title = (
            input("Bildirim başlığı: ").strip()
            or "FRIDAY Test"
        )

        msg = (
            input("Bildirim mesajı: ").strip()
            or "FRIDAY ntfy test bildirimi."
        )

        notifier.send_ntfy(title, msg)

    elif choice == '4':

        print(
            json.dumps(
                notifier.config,
                indent=4,
                ensure_ascii=False
            )
        )

    show_module_status()


if __name__ == '__main__':
    main()
