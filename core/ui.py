import os
import sys
import time
import random
import unicodedata
import re

RED = "\033[1;31m"
BRIGHT_RED = "\033[1;91m"
ORANGE = "\033[38;5;208m"
WHITE = "\033[1;37m"
GRAY = "\033[1;30m"
LIGHT_GRAY = "\033[0;37m"
CYAN = "\033[1;36m"
BLUE = "\033[1;34m"
BRIGHT_CYAN = "\033[1;96m"
DARK_GRAY = "\033[1;30m"
DIM_GREEN = "\033[2;32m"
BRIGHT_GREEN = "\033[1;92m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def strip_ansi(text):
    return ANSI_ESCAPE.sub('', text)

def char_width(char):
    if unicodedata.combining(char):
        return 0
    if unicodedata.east_asian_width(char) in ("W", "F"):
        return 2
    return 1

def visible_width(text):
    clean_text = strip_ansi(text)
    return sum(char_width(c) for c in clean_text)

def type_writer(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")

def freyy_boot():
    sys.stdout.write("\033[?25h")
    clear()

    # === PÁGINA 1: ATENÇÃO & TERMOS ===
    print(f"{DARK_GRAY}┌─── {BRIGHT_RED}[ ATENÇÃO ]{DARK_GRAY} ───────────────────┐{RESET}\n")

    p1_lines = [
        f"{BRIGHT_RED} O toolkit FREYY é destinado apenas{RESET}",
        f"{BRIGHT_RED} para testes de segurança autorizados{RESET}",
        f"{BRIGHT_RED} e para fins educacionais.{RESET}\n",
        f"{WHITE} > O uso não autorizado é crime.{RESET}",
        f"{WHITE} > O operador assume total responsabilidade.{RESET}\n",
        f"{DARK_GRAY}────────────────────────────────────{RESET}",
        f"{YELLOW} [!] Ciente dos termos para avançar.{RESET}\n"
    ]

    for line in p1_lines:
        type_writer(line, delay=0.008)

    input(f"{DARK_GRAY}[ ENTER para continuar ]{RESET}")

    clear()

    # === PÁGINA 2: FERRAMENTAS ===
    print(f"{DARK_GRAY}┌─── {BRIGHT_CYAN}[ FERRAMENTAS ]{DARK_GRAY} ───────────────┐{RESET}\n")

    p2_lines = [
        f"{WHITE}  ► FREYY OSINT{RESET}",
        f"{WHITE}  ► NETWORK{RESET}",
        f"{WHITE}  ► WEB SECURITY{RESET}",
        f"{WHITE}  ► VULNERABILITY{RESET}",
        f"{WHITE}  ► NETWORK MONITOR{RESET}",
        f"{WHITE}  ► FILE ANALYZER{RESET}",
        f"{WHITE}  ► FREYY TOOLS{RESET}",
        f"{WHITE}  ► CHAT FREYY{RESET}\n",
        f"{DARK_GRAY}────────────────────────────────────{RESET}",
        f"{BRIGHT_GREEN} ✔ MÓDULOS VERIFICADOS COM SUCESSO.{RESET}\n"
    ]

    for line in p2_lines:
        type_writer(line, delay=0.008)

    input(f"{DARK_GRAY}[ ENTER para abrir o menu ]{RESET}")
    clear()

def banner():
    ascii_logo = [
        "@@@@@@@@  @@@@@@@   @@@@@@@@  @@@ @@@  @@@ @@@",
        "@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@ @@@  @@@ @@@",
        "@@!       @@!  @@@  @@!       @@! !@@  @@! !@@",
        "!@!       !@!  @!@  !@!       !@! @!!  !@! @!!",
        "@!!!:!    @!@!!@!   @!!!:!     !!@!    !!@!",
        "!!!!!:    !!@!@!    !!!!!:      @!!!     @!!!",
        "!!:       !!: :!!   !!:         !!:      !!",
        ":!:       :!:  :!   :!:         :!:      !:",
        " ::       ::   :::   :: ::::     ::       ::",
        " :         :   : :  : :: ::      :        :",
    ]

    print()
    print(f"{BRIGHT_RED}")

    for line in ascii_logo:
        print(line)

    print(f"{RESET}")
    print(f"{WHITE}FREYY SECURITY TOOLKIT{RESET}")
    print()
def main_menu():
    clear()

    banner()

    boot_lines = [
        "> INIT FREYY... OK",
        "> LOAD CORE....... OK",
        "> LOAD MODULES.... OK",
    ]

    for line in boot_lines:
        print(f"{DARK_GRAY}{line}{RESET}")
        time.sleep(0.08)

    print()

    print(f"{LIGHT_GRAY}MODULES{RESET}")
    print()

    modules = [
        ("[1]", "OSINT", "[5]", "NET MONITOR"),
        ("[2]", "NETWORK", "[6]", "FILE ANALYZER"),
        ("[3]", "WEB SECURITY", "[7]", "FREYY TOOLS"),
        ("[4]", "VULNERABILITY", "[8]", "CHAT AI"),
    ]

    for left_num, left_name, right_num, right_name in modules:
        print(
            f"{DARK_GRAY}├─{RESET} "
            f"{LIGHT_GRAY}{left_num} {left_name:<18}{RESET}"
            f"{DARK_GRAY}├─{RESET} "
            f"{LIGHT_GRAY}{right_num} {right_name}{RESET}"
        )
        time.sleep(0.045)

    print()

    print(f"{DARK_GRAY}{'─' * 40}{RESET}")
    print()
    print(f"{DARK_GRAY}[1-8] SELECT     [X] EXIT{RESET}")
    print()


def draw_static_menu():
    clear()
    main_menu()

def module_banner(title):
    print(f"\n{RED}┌{'─' * 32}┐")
    print(f"│{WHITE}{title:^32}{RED}│")
    print(f"└{'─' * 32}┘{RESET}\n")
