#!/usr/bin/env bash
# ==============================================================================
# E.D.I.T.H. - Security & Tactical Defense Manager v1.5
# (Even Dead, I'm The Hero)
# ==============================================================================

CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}[E.D.I.T.H.] Bu savunma protokolü sudo yetkisi gerektirir.${NC}"
        exec sudo "$0" "$@"
        exit 1
    fi
}

show_banner() {
    clear
    echo -e "${RED}${BOLD}"
    echo "  ======================================================="
    echo "   _____ ____ _____ _____ _   _                         "
    echo "  | ____|  _ \_   _|_   _| | | |                        "
    echo "  |  _| | | | || |   | | | |_| |                        "
    echo "  | |___| |_| || |   | | |  _  |                        "
    echo "  |_____|____/ |_|   |_| |_| |_|                        "
    echo "                                                        "
    echo "       E.D.I.T.H. Tactical Defense & Security v1.5      "
    echo "  =======================================================${NC}"
    echo ""
    echo -e "${CYAN}[E.D.I.T.H.] \"Even Dead, I'm The Hero. Güvenlik ve Ağ Taraması Başlatılıyor...\"${NC}"
    echo ""
}

run_security_scan() {
    check_root
    show_banner
    sleep 1

    echo -e "${YELLOW}[1] UFW Güvenlik Duvarı Durumu:${NC}"
    if command -v ufw &> /dev/null; then
        ufw status verbose
    else
        echo -e "${RED}[!] UFW yüklü değil. Yükleniyor...${NC}"
        apt-get install -y ufw -qq && ufw enable
    fi
    echo ""
    sleep 1

    echo -e "${YELLOW}[2] Açık Dinlenen Ağ Portları (Listening Ports):${NC}"
    ss -tulpn | grep LISTEN || netstat -tulpn | grep LISTEN
    echo ""
    sleep 1

    echo -e "${YELLOW}[3] Aktif Kullanıcı Oturumları & SSH Bağlantıları:${NC}"
    who || w
    echo ""
    sleep 1

    echo -e "${YELLOW}[4] Hızlı Güvenlik Duvarı Yapılandırma Seçeneği:${NC}"
    echo " 1) Güvenlik Duvarını Etkinleştir (ufw enable)"
    echo " 2) SSH (Port 22) İzni Ver"
    echo " 3) HTTP/HTTPS (Port 80/443) İzni Ver"
    echo " 4) Minecraft (Port 25565) İzni Ver"
    echo " 0) Değişiklik Yapmadan Çık"
    echo ""
    read -p "Seçiminiz [0-4]: " sec

    case $sec in
        1) ufw enable ;;
        2) ufw allow 22/tcp ;;
        3) ufw allow 80/tcp && ufw allow 443/tcp ;;
        4) ufw allow 25565/tcp ;;
        0) echo "Çıkılıyor..." ;;
    esac

    echo -e "${GREEN}${BOLD}[E.D.I.T.H.] \"Güvenlik protokolü tamamlandı.\"${NC}"
}

run_security_scan
