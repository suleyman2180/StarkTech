#!/usr/bin/env bash
# ==============================================================================
# MARK 85 - Nanotech Deep Disk Purge Protocol
# ==============================================================================

CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}[MARK-85] Nanotech Temizleme için sudo yetkisi gereklidir.${NC}"
        exec sudo "$0" "$@"
        exit 1
    fi
}

show_banner() {
    clear
    echo -e "${YELLOW}${BOLD}"
    echo "  ======================================================="
    echo "   __  __    _    ____  _  __    ___  ____  "
    echo "  |  \/  |  / \  |  _ \| |/ /   ( _ )| ___| "
    echo "  | |\/| | / _ \ | |_) | ' /    / _ \|___ \ "
    echo "  | |  | |/ ___ \|  _ <| . \   | (_) |__) |"
    echo "  |_|  |_/_/   \_\_| \_\_|\_\   \___/____/ "
    echo "                                            "
    echo "       MARK 85 Nanotech Purge & Clean v1.0  "
    echo "  =======================================================${NC}"
    echo ""
    echo -e "${CYAN}[MARK-85] Nanoteknoloji temizlik protokolü başlatılıyor...${NC}"
    echo ""
}

run_purge() {
    check_root
    show_banner
    sleep 1

    BEFORE_DISK=$(df / -h | awk 'NR==2 {print $4}')

    echo -e "${GREEN}==> Paket Yöneticisi Önbelleği (APT) Temizleniyor...${NC}"
    apt-get autoremove -y -qq
    apt-get autoclean -y -qq
    apt-get clean -y -qq

    echo -e "${GREEN}==> Geçici Sistem Dosyaları ve Loglar Siliniyor...${NC}"
    rm -rf /tmp/* /var/tmp/* 2>/dev/null || true
    journalctl --vacuum-time=2d > /dev/null 2>&1 || true

    echo -e "${GREEN}==> Kullanıcı Küçük Resim ve Önbellekleri Temizleniyor...${NC}"
    rm -rf /home/*/.cache/thumbnails/* /root/.cache/thumbnails/* 2>/dev/null || true

    AFTER_DISK=$(df / -h | awk 'NR==2 {print $4}')

    echo ""
    echo -e "${YELLOW}--------------------------------------------------------${NC}"
    echo -e "${CYAN}Önceki Boş Alan : $BEFORE_DISK${NC}"
    echo -e "${CYAN}Şimdiki Boş Alan: $AFTER_DISK${NC}"
    echo -e "${YELLOW}--------------------------------------------------------${NC}"
    echo -e "${GREEN}${BOLD}[MARK-85] \"I am Iron Man.\" Temizlik başarıyla tamamlandı!${NC}"
}

run_purge
