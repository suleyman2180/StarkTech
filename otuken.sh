#!/usr/bin/env bash
# ==============================================================================
# ÖTÜKEN - ANA KONTROL PANELİ v5.2 (TÜRKÇE)
# ==============================================================================

CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CORE_DIR="$SCRIPT_DIR/CrossPlatform_Core"

show_menu() {
    clear
    echo -e "${RED}${BOLD}"
    echo "  ======================================================="
    echo "             ÖTÜKEN - TAKTİK SİSTEM MERKEZİ v5.2       "
    echo "  =======================================================${NC}"
    echo ""
    echo -e "${GREEN}[J.A.R.V.I.S.] \"Hoş geldiniz. Ötüken çekirdeği aktif. Tüm sistemler hazır.\"${NC}"
    echo "--------------------------------------------------------------------------------"
    echo -e " 1) ${CYAN}falcao.py${NC}    — Tam Ağ Cihaz Taraması ve Risk Değerlendirmesi"
    echo -e " 2) ${GREEN}sombra.py${NC}    — Artık Dosya ve Kayıt Anahtarı Temizleyicisi"
    echo -e " 3) ${YELLOW}kor.py${NC}       — Pil ve Güç Sağlığı Raporlayıcısı"
    echo -e " 4) ${MAGENTA}mirage.py${NC}    — Dosya Formatı ve Medya Dönüştürücü Süiti"
    echo -e " 5) ${BLUE}shield.py${NC}    — Güvenlik Duvarı Kural Yöneticisi"
    echo -e " 6) ${RED}friday.py${NC}    — Telegram ve E-Posta Bildirim Merkezi"
    echo -e " 7) ${CYAN}jarvis.py${NC}    — Otomatik Yazılım ve Paket Yükleyicisi"
    echo -e " 8) ${RED}codigo.py${NC}    — Güvenlik Kasası ve AES-256 Dosya Şifreleyici"
    echo -e " 9) ${BLUE}vision.py${NC}    — Mükerrer ve Büyük Dosya Analizcisi"
    echo -e "10) ${YELLOW}mark85.py${NC}    — Zaman Damgalı Otomatik ZIP Arşivleyici"
    echo -e " 11) ${RED}veronica.py${NC}  — Ağ Teşhis ve Hızlı Performans Kiti"
    echo " 0) Çıkış"
    echo "--------------------------------------------------------------------------------"
}

while true; do
    show_menu
    read -p "Lütfen Bir Protokol Seçin [0-11]: " choice

    case $choice in
        1) python3 "$CORE_DIR/falcao.py" ;;
        2) python3 "$CORE_DIR/sombra.py" ;;
        3) python3 "$CORE_DIR/kor.py" ;;
        4) python3 "$CORE_DIR/mirage.py" ;;
        5) python3 "$CORE_DIR/shield.py" ;;
        6) python3 "$CORE_DIR/friday.py" ;;
        7) python3 "$CORE_DIR/jarvis.py" 2>/dev/null || sudo bash "$SCRIPT_DIR/jarvis.sh" ;;
        8) python3 "$CORE_DIR/codigo.py" ;;
        9) python3 "$CORE_DIR/vision.py" ;;
        10) python3 "$CORE_DIR/mark85.py" ;;
        11) python3 "$CORE_DIR/veronica.py" ;;
        0)
            echo -e "${GREEN}[J.A.R.V.I.S.] \"Ötüken güvenli şekilde kapatılıyor. İyi günler.\"${NC}"
            exit 0
            ;;
        *) echo -e "${RED}Geçersiz seçim!${NC}" ;;
    esac
    read -p "Devam etmek için Enter'a basın..."
done
