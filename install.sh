#!/usr/bin/env bash

set -e

RED='\033[1;31m'
RESET='\033[0m'

clear

echo -e "${RED}"
cat << 'EOF'
███████╗██████╗ ███████╗███████╗   ██╗   ██╗
██╔════╝██╔══██╗██╔════╝╚══███╔╝   ╚██╗ ██╔╝
█████╗  ██████╔╝█████╗    ███╔╝     ╚████╔╝
██╔══╝  ██╔══██╗██╔══╝   ███╔╝       ╚██╔╝
██║     ██║  ██║███████╗███████╗      ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝
EOF
echo -e "${RESET}"

echo "              SECURITY TOOLKIT"
echo
echo "────────────────────────────────────────"
echo

# Detect system
if command -v pkg >/dev/null 2>&1; then

    echo "[+] Termux detected"
    echo "[+] Updating package lists..."

    if ! pkg update -y; then
        echo
        echo "[!] Termux repository update failed."
        echo
        echo "Run:"
        echo
        echo "    termux-change-repo"
        echo
        echo "Choose a working Main repository mirror,"
        echo "then run this installer again."
        echo
        exit 1
    fi

    echo
    echo "[+] Installing system dependencies..."
    pkg install -y python git nmap

    PYTHON_CMD="python"

    echo
    echo "[+] Creating FREYY command..."

    cat > "$PREFIX/bin/FREYY" << EOF
#!/data/data/com.termux/files/usr/bin/bash
exec $PYTHON_CMD "$(cd "$(dirname "$0")" && pwd)/freyy.py" "\$@"
EOF

    chmod +x "$PREFIX/bin/FREYY"

elif command -v apt >/dev/null 2>&1; then

    echo "[+] Debian/Ubuntu-based Linux detected"
    echo "[+] Updating package lists..."

    sudo apt update

    echo
    echo "[+] Installing system dependencies..."
    sudo apt install -y python3 python3-pip git nmap

    PYTHON_CMD="python3"

    echo
    echo "[+] Creating FREYY command..."

    INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"

    mkdir -p "$HOME/.local/bin"

    cat > "$HOME/.local/bin/FREYY" << EOF
#!/usr/bin/env bash
exec $PYTHON_CMD "$INSTALL_DIR/freyy.py" "\$@"
EOF

    chmod +x "$HOME/.local/bin/FREYY"

    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        export PATH="$HOME/.local/bin:$PATH"
    fi

else

    echo "[!] Unsupported system."
    echo
    echo "Supported systems:"
    echo "  - Termux"
    echo "  - Debian/Ubuntu-based Linux"
    echo
    exit 1

fi

echo
echo "[+] Installing Python dependencies..."

$PYTHON_CMD -m pip install -r requirements.txt

echo
echo "[+] Checking installation..."
echo

$PYTHON_CMD --version
nmap --version | head -n 1

echo
echo "────────────────────────────────────────"
echo -e "${RED}          FREYY READY${RESET}"
echo "────────────────────────────────────────"
echo
echo "Installation completed successfully."
echo
echo "Run FREYY with:"
echo
echo "    FREYY"
echo
