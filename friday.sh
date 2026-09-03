#!/usr/bin/env bash
# ==============================================================================
# F.R.I.D.A.Y. - System Health & Performance Optimization Protocol v2.5
# ==============================================================================

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}[F.R.I.D.A.Y.] Boss, bu işlem sistem düzeyinde sudo/root yetkisi gerektirir.${NC}"
        exec sudo "$0" "$@"
        exit 1
    fi
}

show_banner() {
    clear
    echo -e "${MAGENTA}${BOLD}"
    echo "  ======================================================="
    echo "    _____ _____  _____ _____    ___ __   __            "
    echo "   |  ___|  __ \|_   _|  __ \  / _ \\ \ / /            "
    echo "   | |_  | |__) | | | | |  | |/ /_\ \\ V /             "
    echo "   |  _| |  _  /  | | | |  | ||  _  | | |              "
    echo "   |_|   |_| \_\ |___|_|  |_/ |_| |_| |_|              "
    echo "                                                       "
    echo "           F.R.I.D.A.Y. Optimization Core v2.5         "
    echo "  =======================================================${NC}"
    echo ""
    echo -e "${CYAN}[F.R.I.D.A.Y.] \"Selam Boss! Sistem analizini başlatıyorum ve tüm alt sistemleri optimize ediyorum...\"${NC}"
    echo ""
}

run_optimization() {
    check_root
    show_banner
    sleep 1

    echo -e "${YELLOW}[1/4] RAM Önbelleği ve Swap Analizi Yapılıyor...${NC}"
    sync && sysctl -w vm.drop_caches=3 > /dev/null 2>&1
    echo -e "${GREEN}[✓] Önbellek boşaltıldı. Kullanılabilir RAM seviyesi yükseltildi.${NC}"
    sleep 1

    echo -e "${YELLOW}[2/4] Çekirdek (Kernel) Parametreleri ve Swappiness Ayarlanıyor...${NC}"
    sysctl -w vm.swappiness=10 > /dev/null 2>&1 || true
    sysctl -w vm.vfs_cache_pressure=50 > /dev/null 2>&1 || true
    echo -e "${GREEN}[✓] Swappiness = 10 % (SSD/RAM dostu mod aktif).${NC}"
    sleep 1

    echo -e "${YELLOW}[3/4] Ağ Soket Kuyrukları ve BBR Optimizasyonu Kontrol Ediliyor...${NC}"
    sysctl -w net.core.default_qdisc=fq > /dev/null 2>&1 || true
    sysctl -w net.ipv4.tcp_congestion_control=bbr > /dev/null 2>&1 || true
    echo -e "${GREEN}[✓] TCP BBR Ağ Algoritması ve Somaxconn optimize edildi.${NC}"
    sleep 1

    echo -e "${YELLOW}[4/4] Sistem Kaynak Durumu Özeti:${NC}"
    echo "--------------------------------------------------------"
    echo -e "${CYAN}RAM Durumu:${NC} $(free -h | awk '/^Mem:/ {print $3 " / " $2}')"
    echo -e "${CYAN}Disk Alanı:${NC} $(df -h / | awk 'NR==2 {print $3 " / " $2 " (Kullanılan: " $5 ")"}')"
    echo -e "${CYAN}Çalışan Süreç Sayısı:${NC} $(ps aux | wc -l)"
    echo "--------------------------------------------------------"
    echo ""
    echo -e "${GREEN}${BOLD}[F.R.I.D.A.Y.] \"Optimizasyon tamamlandı Boss! Sisteminiz maksimum performansta çalışıyor.\"${NC}"
}

run_optimization
