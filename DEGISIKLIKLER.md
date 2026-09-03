# StarkTech Suite — Cross-Platform Güncelleme Notları

## Ana giriş noktası

**Yeni:** `otuken.py` — Linux, Windows, macOS üzerinde `python3 otuken.py` ile
doğrudan çalışır, bash gerektirmez. Başlangıçta platformu ve mimariyi gösterir:

```
[ÖTÜKEN] Platform: Linux
[ÖTÜKEN] Architecture: x86_64
[ÖTÜKEN] Cross-Platform Core: ONLINE
```

`otuken.sh` Linux'ta olduğu gibi çalışmaya devam eder (davranışı korundu),
ama artık Windows/macOS için zorunlu değildir.

## Yeni ortak modül

`CrossPlatform_Core/common.py` — tüm modüllerin kullandığı tek noktadan
platform algılama, renkler, `is_admin()`, `run()` (güvenli, shell=True'suz
komut çalıştırma), paket yöneticisi algılama ve standart
"[!] Bu özellik bu sistemde kullanılamıyor" mesajı.

## Modül modül değişiklikler

| Modül | Durum |
|---|---|
| **falcao.py** | Zaten büyük ölçüde çapraz platformdu; ortak modüle taşındı, `arp` eksikse net uyarı eklendi. |
| **sombra.py** | Ortak modüle taşındı, davranış korundu. |
| **kor.py** | **Düzeltildi:** Windows pil raporu artık sahte/sabit değerler (`142`, `%85` vb.) döndürmüyordu — şimdi PowerShell/CIM ile anlık şarj durumunu, `powercfg /batteryreport /xml` ile gerçek tasarım/tam kapasite ve döngü sayısını okuyor (XML gerçekten ayrıştırılıyor). Pilsiz masaüstü sistemlerde artık düzgün "tespit edilemedi" mesajı veriyor. |
| **mirage.py** | Ortak modüle taşındı, ffmpeg eksikse net uyarı. |
| **shield.py** | **Güvenlik düzeltmesi:** Windows tarafında `shell=True` kullanımı kaldırıldı (liste tabanlı `subprocess.run`), port girdisi artık komuta eklenmeden önce doğrulanıyor (1-65535 sayı kontrolü) — komut enjeksiyonu riski kapatıldı. |
| **friday.py** | Zaten tam çapraz platformdu (urllib/smtplib); sadece ortak modüle taşındı, `friday_config.json` davranışı korundu. |
| **jarvis.py** | **Hata düzeltildi:** Orijinal dosyada Türkçe "akıllı tırnak" (" ") karakterleri f-string içinde kullanılmış ve **syntax hatası** oluşturuyordu (`SyntaxError`) — modül hiç çalışmıyordu. Düzeltildi. Ayrıca Linux tarafına apt/dnf/yum/pacman/zypper otomatik algılama eklendi (önceden sadece apt vardı). |
| **codigo.py** (eski edith.py) | **Kritik düzeltme:** Modül "AES-256" olarak adlandırılmıştı ama gerçekte zayıf, kriptografik olarak güvensiz bir **XOR akış şifrelemesi** kullanıyordu. Artık `cryptography` kütüphanesi ile **gerçek AES-256-GCM** (yetkilendirilmiş şifreleme — bütünlük kontrolü dahil) kullanıyor. Yeni dosya uzantısı: `.codigo` (eski `.edith` dosyalarıyla uyumlu değildir, format farklı). |
| **vision.py** | Ortak modüle taşındı, davranış korundu. |
| **mark85.py** | **Hata düzeltildi:** Orijinal dosyada string birleştirme hataları vardı — ekrana `"==>  + source_dir +  arşivleniyor..."` gibi kırık metinler basılıyordu (f-string yanlışlıkla düz string'e çevrilmişti). Ayrıca `pathlib.Path` kullanılarak Windows yol uyumluluğu netleştirildi. |
| **veronica.py** | Ortak modüle taşındı, davranış korundu. |

## Bash scriptleri (edith.sh, friday.sh, jarvis.sh, mark85.sh, veronica.sh)

Bunlar Linux'a özgü, sudo gerektiren "derin sistem" güçlendirme scriptleridir
(CPU governor, swappiness, journalctl vacuum, whiptail kurulum menüsü vb.).
Windows/macOS karşılıkları yoktur ve **olmamalıdır** — bu işlemler Linux
çekirdek parametreleridir. `otuken.py` bunları çağırmaz; sadece `otuken.sh`
üzerinden, Linux'ta, isteğe bağlı olarak kullanılabilirler. Bu, talimat
18'e ("Bash scriptleri Windows'ta zorunlu olmamalı") uygundur.

**Not:** `otuken.sh` içinde bulunan bir menü hatası da düzeltildi: 11 numaralı
seçenek yanlışlıkla `falcao.py`yi tekrar çağırıyordu (1 ile aynı) ve var
olmayan bir `falcao.sh`ye düşüyordu; artık doğru şekilde `veronica.py`yi
çağırıyor.

## Güvenlik notları (madde 20)

- `shell=True` sadece gerçekten gerekmeyen yerlerde kaldırıldı (shield.py).
- Kullanıcı girdisi (port numaraları) artık komut listesine eklenmeden önce doğrulanıyor.
- Şifre/token kod içine gömülmedi; `friday_config.json` aynı şekilde korunuyor.
- Mevcut config dosyaları (`friday_config.json`) değiştirilmedi.

---

## Test Komutları

### Linux
```bash
cd StarkTech_Suite_TR_Fixed
python3 otuken.py                      # yeni çapraz platform menü
# veya
bash otuken.sh                         # eski bash menü (düzeltilmiş)

# Tekil modül testleri
python3 CrossPlatform_Core/falcao.py
python3 CrossPlatform_Core/kor.py
python3 CrossPlatform_Core/codigo.py
python3 CrossPlatform_Core/shield.py
```

### Windows (PowerShell)
```powershell
cd StarkTech_Suite_TR_Fixed
python otuken.py

python CrossPlatform_Core\kor.py        # gerçek powercfg/CIM pil verisi
python CrossPlatform_Core\shield.py     # netsh tabanlı, liste-komut (shell=True yok)
python CrossPlatform_Core\jarvis.py     # winget ile kurulum
```

### macOS
```bash
cd StarkTech_Suite_TR_Fixed
python3 otuken.py

python3 CrossPlatform_Core/kor.py       # system_profiler tabanlı pil verisi
python3 CrossPlatform_Core/shield.py    # socketfilterfw tabanlı
python3 CrossPlatform_Core/jarvis.py    # brew ile kurulum
```

### Bağımlılıklar
```bash
pip install -r requirements.txt --break-system-packages   # Linux (PEP 668 ise)
pip install -r requirements.txt                            # Windows / macOS
```
