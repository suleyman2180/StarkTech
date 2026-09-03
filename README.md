# ⚡ StarkTech Suite

> **ÖTÜKEN Taktik Sistem Merkezi**
> Cross-platform sistem, ağ, güvenlik, bakım ve otomasyon araçları koleksiyonu.

StarkTech Suite; Linux, Windows ve macOS üzerinde çalışabilecek şekilde tasarlanan, modüler bir sistem yönetim ve güvenlik araçları paketidir.

Tüm araçlar tek bir merkezden **ÖTÜKEN** üzerinden yönetilebilir.

---

## 🧠 ÖTÜKEN

ÖTÜKEN, StarkTech Suite'in ana kontrol merkezidir.

```text
=======================================================
              ÖTÜKEN - TAKTİK SİSTEM MERKEZİ
=======================================================

[J.A.R.V.I.S.] "Hoş geldiniz. Ötüken çekirdeği aktif.
                Tüm sistemler hazır."
-------------------------------------------------------

1) FALCÃO       — Ağ cihaz taraması ve risk analizi
2) SOMBRA       — Gereksiz / kullanılmayan dosya temizliği
3) KOR          — Batarya ve güç durumu
4) MIRAGE       — Dosya ve medya dönüştürme
5) SHIELD       — Güvenlik duvarı yönetimi
6) FRIDAY       — Bildirim merkezi
7) JARVIS       — Yazılım / paket yöneticisi
8) CÓDIGO       — AES-256 güvenlik kasası
9) VISION       — Büyük ve yinelenen dosya analizi
10) MARK85      — Zaman damgalı ZIP arşivleme
11) VERONICA    — Ağ tanılama ve performans araçları
```

---

# 🛰️ Modüller

## 🦅 FALCÃO

Ağ üzerindeki cihazları keşfetmek ve temel risk değerlendirmesi yapmak için kullanılır.

* Yerel ağ taraması
* Cihaz keşfi
* IP bilgileri
* Ağ analizi
* Risk değerlendirmesi

Dosya:

```text
CrossPlatform_Core/falcao.py
```

---

## 🌑 SOMBRA

Sistemdeki gereksiz veya kullanılmayan dosyaları tespit etmeye yardımcı olur.

* Gereksiz dosya analizi
* Boyut analizi
* Temizlik işlemleri
* Güvenli dosya yönetimi

Dosya:

```text
CrossPlatform_Core/sombra.py
```

---

## 🔥 KOR

Bilgisayarın güç ve batarya durumunu takip eder.

* Batarya yüzdesi
* Şarj durumu
* Güç durumu
* Platforma göre uyarlanmış kontroller

Dosya:

```text
CrossPlatform_Core/kor.py
```

---

## 🪞 MIRAGE

Dosya ve medya dönüştürme işlemleri için tasarlanmıştır.

* Dosya dönüştürme
* Medya işlemleri
* Format kontrolü
* Platform uyumluluğu

Dosya:

```text
CrossPlatform_Core/mirage.py
```

---

## 🛡️ SHIELD

Sistemin güvenlik duvarını yönetmek için kullanılır.

Linux, Windows ve macOS üzerinde işletim sistemine uygun yöntemleri kullanmaya çalışır.

Desteklenen sistemlere göre:

```text
Linux    → UFW / firewalld
Windows  → Windows Defender Firewall
macOS    → pf
```

Dosya:

```text
CrossPlatform_Core/shield.py
```

> ⚠️ Güvenlik duvarı işlemleri yönetici yetkisi gerektirebilir.

---

## 📡 FRIDAY

StarkTech Suite'in bildirim merkezidir.

Desteklenen bildirim sistemleri:

* Telegram
* E-mail / SMTP
* ntfy

Mimari:

```text
FALCÃO ─┐
SOMBRA ─┤
KOR ────┤
SHIELD ─┤
JARVIS ─┤
CÓDIGO ─┤
VISION ─┤
MARK85 ┤
VERONICA┘
    ↓
  FRIDAY
    ↓
 Bildirim
```

Dosya:

```text
CrossPlatform_Core/friday.py
```

### 🔐 FRIDAY yapılandırması

Gerçek API anahtarlarını veya şifreleri GitHub'a yüklemeyin.

Örnek yapılandırma:

```text
friday_config.example.json
```

Gerçek yapılandırma:

```text
friday_config.json
```

`friday_config.json` `.gitignore` içerisinde tutulmalıdır.

---

## 🤖 JARVIS

Yazılım ve paket yönetimi için kullanılan yardımcı modüldür.

İşletim sistemine göre uygun paket yöneticisini belirlemeye çalışır.

Örnek:

```text
Linux   → apt / dnf / pacman
Windows → winget
macOS   → brew
```

Dosya:

```text
CrossPlatform_Core/jarvis.py
```

---

## 🔐 CÓDIGO

StarkTech Suite'in güvenlik kasasıdır.

AES-256 tabanlı dosya şifreleme amacıyla tasarlanmıştır.

Özellikler:

* Dosya şifreleme
* Dosya çözme
* Güvenli anahtar kullanımı
* Cross-platform çalışma

Dosya:

```text
CrossPlatform_Core/codigo.py
```

> 🔒 Şifreleme anahtarlarınızı ve hassas dosyalarınızı GitHub'a yüklemeyin.

---

## 👁️ VISION

Disk üzerindeki büyük ve yinelenen dosyaları analiz eder.

* Büyük dosya tespiti
* Yinelenen dosya analizi
* Disk kullanım analizi
* Dosya boyutu karşılaştırması

Dosya:

```text
CrossPlatform_Core/vision.py
```

---

## ⚙️ MARK85

Dosyaları zaman damgalı ZIP arşivlerine dönüştürür.

Örnek:

```text
backup_2026-09-04_23-15-42.zip
```

Dosya:

```text
CrossPlatform_Core/mark85.py
```

---

## 📶 VERONICA

Ağ tanılama ve performans analiz modülüdür.

* IP bilgisi
* Gateway
* DNS
* Ağ arayüzleri
* Ping
* Bağlantı durumu
* Ağ performansı

Dosya:

```text
CrossPlatform_Core/veronica.py
```

> VERONICA, FALCÃO'dan farklı olarak ağ keşfinden ziyade **ağ tanılama ve performans** görevlerine odaklanır.

---

# 💻 Desteklenen Platformlar

| Platform         | Durum |
| ---------------- | ----- |
| 🐧 Linux         | ✅     |
| 🪟 Windows 10/11 | ✅     |
| 🍎 macOS         | ✅     |

Bazı özellikler işletim sistemine bağlı olarak kullanılamayabilir.

StarkTech Suite bu durumda işlemi güvenli şekilde sonlandırmaya ve kullanıcıya bilgi vermeye çalışır.

---

# 🚀 Kurulum

Projeyi klonlayın:

```bash
git clone https://github.com/suleyman2180/StarkTech.git
cd StarkTech
```

Python sürümünü kontrol edin:

```bash
python3 --version
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

---

# ▶️ Kullanım

Ana kontrol merkezini başlatın:

```bash
python3 otuken.py
```

veya Linux üzerinde:

```bash
./otuken.sh
```

Gerekirse çalıştırma izni verin:

```bash
chmod +x otuken.sh
```

---

# 📁 Proje Yapısı

```text
StarkTech/
│
├── CrossPlatform_Core/
│   ├── falcao.py
│   ├── sombra.py
│   ├── kor.py
│   ├── mirage.py
│   ├── shield.py
│   ├── friday.py
│   ├── jarvis.py
│   ├── codigo.py
│   ├── vision.py
│   ├── mark85.py
│   └── veronica.py
│
├── otuken.py
├── otuken.sh
├── friday.sh
├── jarvis.sh
├── veronica.sh
├── edith.sh
├── mark85.sh
│
├── common.py
├── requirements.txt
├── DEGISIKLIKLER.md
├── .gitignore
└── README.md
```

---

# 🔒 Güvenlik

StarkTech Suite güvenlik odaklı geliştirilmiştir.

Projeye hassas bilgileri eklemeyin:

```text
❌ API key
❌ Telegram bot token
❌ SMTP şifresi
❌ AES anahtarı
❌ kişisel şifreler
❌ gerçek yapılandırma dosyaları
```

Bunun yerine örnek yapılandırma dosyaları kullanın.

---

# 🧩 Tasarım Felsefesi

StarkTech Suite'in amacı tek bir dev uygulama oluşturmak yerine, farklı görevleri yerine getiren **modüler sistem araçlarını tek bir çekirdekte birleştirmektir.**

```text
                 ┌─────────────┐
                 │   ÖTÜKEN    │
                 │ CORE SYSTEM │
                 └──────┬──────┘
                        │
       ┌────────────────┼────────────────┐
       │                │                │
   SYSTEM            NETWORK          SECURITY
       │                │                │
   SOMBRA             FALCÃO           SHIELD
   KOR                VERONICA         CÓDIGO
   MIRAGE
   VISION
   MARK85
       │
       └──────────── FRIDAY ────────────┘
                        │
                   NOTIFICATION
```

---

# 🛠️ Teknolojiler

StarkTech Suite ağırlıklı olarak:

* Python
* Bash
* JSON
* ZIP
* AES-256
* Network utilities
* Platform-specific system APIs

kullanır.

---

# 📜 Lisans

Bu proje **MIT License** altında lisanslanmıştır.

Detaylar için [`LICENSE`](LICENSE) dosyasına bakabilirsiniz.


---

# ⚡ StarkTech

**Built with Python. Powered by ÖTÜKEN.**

> *"Sistemler hazır. Görev bekleniyor."*

```text
[J.A.R.V.I.S.]
ÖTÜKEN CORE ONLINE
ALL SYSTEMS NOMINAL
```
