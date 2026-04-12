#!/usr/bin/env bash
# Axle CLI — Pre-flight installer
# Checks Python and pip before installing, explains what each requirement is for.

set -e

REPO="https://github.com/skpaul82/axle-cli.git"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=10
DOCS_URL="https://www.axle.sanjoypaul.com/docs"
PYTHON_URL="https://www.python.org/downloads/"

# ── colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

ok()   { echo -e "  ${GREEN}✅ $*${RESET}"; }
warn() { echo -e "  ${YELLOW}⚠️  $*${RESET}"; }
err()  { echo -e "  ${RED}❌ $*${RESET}"; }
info() { echo -e "  ${CYAN}ℹ  $*${RESET}"; }

# ── banner ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}======================================================${RESET}"
echo -e "${BOLD}  ⚙️  Axle CLI — Installer                            ${RESET}"
echo -e "${BOLD}======================================================${RESET}"
echo ""
echo -e "  Axle is a modular CLI platform for running Python"
echo -e "  microtools from a shared tools directory."
echo -e "  Run ANY Python tool by name or number — no contract needed."
echo ""
echo -e "  What this installer will do:"
echo -e "   1. Check your system requirements (Python, pip)"
echo -e "   2. Install Axle CLI from GitHub"
echo -e "   3. Verify the installation"
echo ""
echo -e "${BOLD}------------------------------------------------------${RESET}"

# ── OS detection ──────────────────────────────────────────────────────────────
OS="$(uname -s 2>/dev/null || echo "Unknown")"
case "$OS" in
  Darwin)  OS_NAME="macOS" ;;
  Linux)   OS_NAME="Linux" ;;
  MINGW*|MSYS*|CYGWIN*) OS_NAME="Windows" ;;
  *)       OS_NAME="$OS" ;;
esac

echo ""
echo -e "  ${BOLD}System:${RESET} $OS_NAME"

# ── Python check ──────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[1/3] Checking Python...${RESET}"
echo ""
echo -e "  ${CYAN}Why Python?${RESET}"
echo -e "  Axle and all its tools are written in Python."
echo -e "  Python 3.10+ is required to run them."
echo ""

PYTHON_CMD=""
for cmd in python3 python; do
  if command -v "$cmd" &>/dev/null; then
    ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>/dev/null || echo "")
    if [ -n "$ver" ]; then
      major=$(echo "$ver" | cut -d. -f1)
      minor=$(echo "$ver" | cut -d. -f2)
      if [ "$major" -ge "$MIN_PYTHON_MAJOR" ] && [ "$minor" -ge "$MIN_PYTHON_MINOR" ]; then
        PYTHON_CMD="$cmd"
        ok "Python $ver found ($cmd) — compatible ✓"
        break
      else
        warn "Python $ver found ($cmd) — too old. Need $MIN_PYTHON_MAJOR.$MIN_PYTHON_MINOR+"
      fi
    fi
  fi
done

if [ -z "$PYTHON_CMD" ]; then
  err "Python $MIN_PYTHON_MAJOR.$MIN_PYTHON_MINOR+ not found."
  echo ""
  echo -e "  ${BOLD}How to install Python:${RESET}"
  case "$OS_NAME" in
    macOS)
      echo -e "   • Homebrew (recommended):  brew install python"
      echo -e "   • Official installer:       $PYTHON_URL"
      echo -e "   • pyenv (version manager):  brew install pyenv && pyenv install 3.12"
      ;;
    Linux)
      echo -e "   • Ubuntu/Debian:  sudo apt update && sudo apt install python3.12"
      echo -e "   • Fedora/RHEL:    sudo dnf install python3.12"
      echo -e "   • Official:       $PYTHON_URL"
      ;;
    Windows)
      echo -e "   • Official installer: $PYTHON_URL"
      echo -e "   • winget:             winget install Python.Python.3.12"
      echo -e "   • Microsoft Store:    search 'Python 3.12'"
      echo -e "   ${YELLOW}Tip: check 'Add Python to PATH' during install!${RESET}"
      ;;
    *)
      echo -e "   • Official: $PYTHON_URL"
      ;;
  esac
  echo ""
  err "Please install Python $MIN_PYTHON_MAJOR.$MIN_PYTHON_MINOR+ and re-run this script."
  exit 1
fi

# ── pip check ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[2/3] Checking pip...${RESET}"
echo ""
echo -e "  ${CYAN}Why pip?${RESET}"
echo -e "  pip is Python's package manager. It downloads and installs"
echo -e "  Axle and its dependencies (pandas, requests, spaCy, etc.)."
echo ""

PIP_CMD=""
for cmd in pip3 pip; do
  if command -v "$cmd" &>/dev/null; then
    pip_ver=$("$cmd" --version 2>/dev/null | awk '{print $2}' || echo "")
    if [ -n "$pip_ver" ]; then
      PIP_CMD="$cmd"
      ok "pip $pip_ver found ($cmd)"
      break
    fi
  fi
done

# Fallback: try python -m pip
if [ -z "$PIP_CMD" ]; then
  pip_ver=$("$PYTHON_CMD" -m pip --version 2>/dev/null | awk '{print $2}' || echo "")
  if [ -n "$pip_ver" ]; then
    PIP_CMD="$PYTHON_CMD -m pip"
    ok "pip $pip_ver available via '$PYTHON_CMD -m pip'"
  fi
fi

if [ -z "$PIP_CMD" ]; then
  err "pip not found."
  echo ""
  echo -e "  ${BOLD}How to install pip:${RESET}"
  echo -e "   • Run:  $PYTHON_CMD -m ensurepip --upgrade"
  echo -e "   • Or:   curl https://bootstrap.pypa.io/get-pip.py | $PYTHON_CMD"
  case "$OS_NAME" in
    Linux)
      echo -e "   • Ubuntu/Debian:  sudo apt install python3-pip"
      echo -e "   • Fedora/RHEL:    sudo dnf install python3-pip"
      ;;
  esac
  echo ""
  err "Please install pip and re-run this script."
  exit 1
fi

# ── install ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}[3/3] Installing Axle CLI...${RESET}"
echo ""
echo -e "  Source: ${CYAN}$REPO${RESET}"
echo ""

if [ "$PIP_CMD" = "$PYTHON_CMD -m pip" ]; then
  $PYTHON_CMD -m pip install "git+$REPO"
else
  $PIP_CMD install "git+$REPO"
fi

# ── verify ────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}------------------------------------------------------${RESET}"
if command -v axle &>/dev/null; then
  AXLE_VER=$(axle -V 2>/dev/null || echo "installed")
  ok "Axle installed — $AXLE_VER"
  echo ""
  echo -e "${BOLD}${GREEN}  ✅ All done! Get started:${RESET}"
  echo ""
  echo -e "   ${BOLD}axle${RESET}                     # interactive tool picker"
  echo -e "   ${BOLD}axle list${RESET}                # list all tools"
  echo -e "   ${BOLD}axle <tool_name>${RESET}         # see tool examples"
  echo -e "   ${BOLD}axle <tool_name> --flags${RESET} # run a tool directly"
  echo -e "   ${BOLD}axle doctor${RESET}              # check your environment"
  echo ""
  echo -e "  📖 Docs:      $DOCS_URL"
  echo -e "  ⭐ GitHub:    https://github.com/skpaul82/axle-cli"
  echo -e "  🐦 Follow:    https://x.com/_skpaul82"
else
  warn "Axle installed but 'axle' command not found in PATH."
  echo ""
  info "Your pip scripts directory may not be in PATH."
  echo ""
  echo -e "  ${BOLD}Fix for $OS_NAME:${RESET}"
  case "$OS_NAME" in
    macOS|Linux)
      echo -e "   Add to your shell profile (~/.zshrc or ~/.bashrc):"
      echo -e "   ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
      echo -e "   Then run: source ~/.zshrc  (or restart terminal)"
      ;;
    Windows)
      echo -e "   Add the Python Scripts folder to your PATH in System Settings."
      ;;
  esac
fi

echo ""
echo -e "${BOLD}======================================================${RESET}"
echo ""
