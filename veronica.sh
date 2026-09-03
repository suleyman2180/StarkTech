#!/usr/bin/env bash
# ==============================================================================
# VERONICA (HULKBUSTER) - Extreme Performance Booster
# ==============================================================================

CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}[VERONICA] Hulkbuster Protokolü için sudo gereklidir.${NC}"
        exec sudo "$0" "$@"
        exit 1
    fi
}

show_banner() {
    clear
    echo -e "${RED}${BOLD}"
    echo "  ======================================================="
    echo "   V E R O N I C A  -  H U L K B U S T E R   M O D E"
    echo "  =======================================================${NC}"
    echo ""
    echo -e "${YELLOW}[VERONICA] \"Deploying Hulkbuster Armor! Maksimum Performans Etkinleştiriliyor...\"${NC}"
    echo ""
}

run_hulkbuster() {
    check_root
    show_banner
    sleep 1

    echo -e "${GREEN}==> RAM Önbelleği Tamamen Boşaltılıyor...${NC}"
    sync && sysctl -w vm.drop_caches=3 > /dev/null 2>&1

    echo -e "${GREEN}==> CPU Governor Performance Moduna Alınıyor...${NC}"
    if [ -d "/sys/devices/system/cpu/cpu0/cpufreq" ]; then
        for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
            echo "performance" > "$g" 2>/dev/null || true
        done
        echo -e "${CYAN}[✓] Tüm CPU Çekirdekleri Maksimum Frekansa Kilitlendi.${NC}"
    fi

    echo -e "${GREEN}==> GameMode ve I/O Önceliği Optimize Ediliyor...${NC}"
    if command -v gamemoded &> /dev/null; then
        gamemoded -r 2>/dev/null || true
        echo -e "${CYAN}[✓] GameMode Daemon Aktif.${NC}"
    fi

    echo ""
    echo -e "${GREEN}${BOLD}[VERONICA] \"Go to sleep, go to sleep, go to sleep! Maksimum performans hazır, Bay Stark!\"${NC}"
}

run_hulkbuster
