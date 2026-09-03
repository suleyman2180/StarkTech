#!/usr/bin/env bash
# ==============================================================================
# J.A.R.V.I.S. - Just A Rather Very Intelligent System
# Interactive Software Installation Protocol v3.0
# ==============================================================================

CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

LOG_FILE="/var/log/jarvis_installer.log"

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}[J.A.R.V.I.S.] Sir, bu protocol yetkili ayrıcalıklar (sudo) gerektiriyor.${NC}"
        exec sudo "$0" "$@"
        exit 1
    fi
}

show_banner() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "  ======================================================="
    echo "    _______  _______  _______  _______  _______ ._ _ _   "
    echo "   (  ___  )(  ___  )(  ____ )(  ____ \(  ____ \| | | |  "
    echo "   | (   ) || (   ) || (    )|| (    \/| (    \/| | | |  "
    echo "   | |   | || (___) || (____)|| (__    | (_____ | | | |  "
    echo "   | |   | ||  ___  ||  _____)|  __)   (_____  )| | | |  "
    echo "   | |   | || (   ) || (      | (            ) ||_|_|_|  "
    echo "   | (___) || )   ( || )      | (____/\/\____) | _ _ _   "
    echo "   (_______)|/     \||/       (_______/\_______)(_|_|_)  "
    echo "                                                         "
    echo "           J.A.R.V.I.S. Software Deployment v3.0         "
    echo "  =======================================================${NC}"
    echo ""
    echo -e "${GREEN}[J.A.R.V.I.S.] \"Günaydın Bay Stark. Hangi sistemleri kurmamı istersiniz?\"${NC}"
    echo ""
}

check_whiptail() {
    if ! command -v whiptail &> /dev/null; then
        echo -e "${YELLOW}[J.A.R.V.I.S.] Whiptail modülü yükleniyor...${NC}"
        apt-get update -qq && apt-get install -y whiptail -qq
    fi
}

run_installer() {
    check_whiptail

    CHOICES=$(whiptail --title "STARK TECH - J.A.R.V.I.S. Installer" \
        --checklist "\nSir, lütfen yüklemek istediğiniz yazılım paketlerini seçiniz:\n(Boşluk tuşu ile seçin, TAB ile Tamam'a geçin)" 20 78 8 \
        "VS_CODE" "Visual Studio Code (Geliştirici IDE)" ON \
        "DOCKER" "Docker & Docker Compose (Konteyner Motoru)" ON \
        "GIT_TOOLS" "Git, Curl, Wget, Build-Essential" ON \
        "PYTHON_DEV" "Python3, Pip, Venv, Python-Dev" ON \
        "CHROME" "Google Chrome Web Tarayıcısı" OFF \
        "DISCORD" "Discord İletişim Uygulaması" OFF \
        "MEDIA_TOOLS" "VLC Media Player & OBS Studio" OFF \
        "SYSTEM_UTILS" "Htop, Fastfetch, Tmux, Tree, Unzip" ON \
        "STEAM_GAMING" "Steam & GameMode (Oyun Platformu)" OFF \
        3>&1 1>&2 2>&3)

    exitstatus=$?
    if [ $exitstatus -ne 0 ]; then
        echo -e "${YELLOW}[J.A.R.V.I.S.] Protokol iptal edildi, Bay Stark.${NC}"
        exit 0
    fi

    show_banner
    echo -e "${BLUE}[J.A.R.V.I.S.] Seçilen paketlerin yüklemesi başlatılıyor...${NC}"
    apt-get update -qq

    for CHOICE in $CHOICES; do
        CLEAN_CHOICE=$(echo "$CHOICE" | sed 's/"//g')
        case "$CLEAN_CHOICE" in
            VS_CODE)
                echo -e "${GREEN}==> VS Code yükleniyor...${NC}"
                if ! command -v code &> /dev/null; then
                    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg
                    echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list
                    apt-get update -qq && apt-get install -y code -qq
                fi
                ;;
            DOCKER)
                echo -e "${GREEN}==> Docker & Compose yükleniyor...${NC}"
                apt-get install -y docker.io docker-compose-v2 -qq
                systemctl enable --now docker || true
                SUDO_USER_NAME="${SUDO_USER:-$USER}"
                [ "$SUDO_USER_NAME" != "root" ] && usermod -aG docker "$SUDO_USER_NAME" || true
                ;;
            GIT_TOOLS)
                echo -e "${GREEN}==> Geliştirme araçları yükleniyor...${NC}"
                apt-get install -y git curl wget build-essential software-properties-common jq -qq
                ;;
            PYTHON_DEV)
                echo -e "${GREEN}==> Python3 ortamı yükleniyor...${NC}"
                apt-get install -y python3 python3-pip python3-venv python3-dev -qq
                ;;
            CHROME)
                echo -e "${GREEN}==> Google Chrome yükleniyor...${NC}"
                wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb
                apt-get install -y /tmp/chrome.deb -qq
                rm -f /tmp/chrome.deb
                ;;
            DISCORD)
                echo -e "${GREEN}==> Discord yükleniyor...${NC}"
                wget -q "https://discord.com/api/download?platform=linux&format=deb" -O /tmp/discord.deb
                apt-get install -y /tmp/discord.deb -qq || apt-get install -f -y -qq
                rm -f /tmp/discord.deb
                ;;
            MEDIA_TOOLS)
                echo -e "${GREEN}==> VLC ve OBS Studio yükleniyor...${NC}"
                apt-get install -y vlc obs-studio -qq
                ;;
            SYSTEM_UTILS)
                echo -e "${GREEN}==> Sistem araçları yükleniyor...${NC}"
                apt-get install -y htop fastfetch tmux tree unzip zip p7zip-full -qq
                ;;
            STEAM_GAMING)
                echo -e "${GREEN}==> Steam ve GameMode yükleniyor...${NC}"
                dpkg --add-architecture i386 || true
                apt-get update -qq
                apt-get install -y steam gamemode -qq
                ;;
        esac
    done

    whiptail --title "J.A.R.V.I.S. Status" --msgbox "\n[✓] Tüm seçilen programlar başarıyla yüklendi, Bay Stark!\n\nSistem kullanıma hazırdır." 12 65
    echo -e "${GREEN}${BOLD}[J.A.R.V.I.S.] \"İşlem tamamlandı sir. Zırhınız tamamen güncel.\"${NC}"
}

check_root
run_installer "$@"
