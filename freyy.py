import sys
import os
import time

from core.ui import freyy_boot, draw_static_menu, RED, BRIGHT_CYAN, RESET, module_banner, clear

from modules.osint import open_osint
from modules.network import open_network, network_monitor
from modules.web_security import open_web_security
from modules.vulnerability import open_vulnerability
from modules.file_analyzer import open_file_analyzer
from modules.apk_analyzer import open_apk_analyzer
from modules.chat_freyy import open_chat_freyy


def execute_module(func, name):
    clear()
    module_banner(name)
    if func:
        try:
            func()
        except Exception as e:
            print(f"\n{RED}[!] Erro ao executar o módulo {name}: {e}{RESET}")
    else:
        print(f"\n{RED}[!] O módulo {name} não possui uma função de execução padrão mapeada.{RESET}")

    input(f"\n{BRIGHT_CYAN}[ Pressione ENTER para voltar ao menu... ]{RESET}")


def main():
    freyy_boot()
    while True:
        draw_static_menu()
        try:
            choice = input(f"{RED}freyy{BRIGHT_CYAN}@sec{RESET}:{RED}~#{RESET} ").strip().lower()

            if choice == '1':
                execute_module(open_osint, "FREYY OSINT")
            elif choice == '2':
                execute_module(open_network, "NETWORK SUITE")
            elif choice == '3':
                execute_module(open_web_security, "WEB SECURITY")
            elif choice == '4':
                execute_module(open_vulnerability, "VULNERABILITY SUITE")
            elif choice == '5':
                execute_module(network_monitor, "NETWORK MONITOR")
            elif choice == '6':
                execute_module(open_file_analyzer, "FILE ANALYZER")
            elif choice == '7':
                execute_module(open_apk_analyzer, "FREYY TOOLS")
            elif choice == '8':
                execute_module(open_chat_freyy, "CHAT FREYY AI")
            elif choice in ['x', '0', 'exit', 'sair']:
                print(f"\n{RED}[!] Encerrando FREYY...{RESET}")
                break
            else:
                input(f"\n{RED}[!] Opção inválida! Pressione ENTER para tentar novamente...{RESET}")

        except (KeyboardInterrupt, EOFError):
            print(f"\n{RED}[!] Saindo...{RESET}")
            break

if __name__ == "__main__":
    main()
