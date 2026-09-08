import os
import socket
import subprocess
import time

import requests

from utils.nmap_parser import parse_nmap
from utils.service_info import get_service_info


BLUE = "\033[1;34m"
WHITE = "\033[1;37m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


# ============================================================
# NETWORK BANNER
# ============================================================

def network_banner():
    print()
    print(f"{RED}")
    print("   _   _ _____ _____        ___  ______")
    print("  | \\ | | ____|_   _|      / _ \\|  ____|")
    print("  |  \\| |  _|   | | _____ | | | | |__")
    print("  | |\\  | |___  | ||_____|| |_| |  __|")
    print("  |_| \\_|_____| |_|        \\___/|_|")
    print(f"{RESET}")

    print(f"{WHITE}FREYY / NETWORK{RESET}")
    print(f"{WHITE}NETWORK MODULE{RESET}")
    print(f"{BLUE}{'─' * 40}{RESET}")
    print()
# ============================================================

# VALIDAÇÃO DE PORTAS
# ============================================================

def validate_ports(port_input):
    parts = port_input.replace(" ", "").split(",")

    if not parts or any(not part for part in parts):
        return False

    for part in parts:
        if "-" in part:
            values = part.split("-")

            if len(values) != 2:
                return False

            try:
                start = int(values[0])
                end = int(values[1])
            except ValueError:
                return False

            if start < 1 or end > 65535 or start > end:
                return False

        else:
            try:
                port = int(part)
            except ValueError:
                return False

            if port < 1 or port > 65535:
                return False

    return True


# ============================================================
# MOSTRAR RESULTADOS DO NMAP
# ============================================================

def show_results(parsed):
    print(f"{BLUE}RESULTADOS{RESET}")
    print("=" * 50)

    if not parsed:
        print("Nenhum serviço aberto foi identificado.")
        return

    for item in parsed:
        port = item["port"]
        state = item["state"]
        state_explanation = item["state_explanation"]
        service = item["service"]
        version = item["version"]

        info = get_service_info(service)

        print()
        print(f"PORTA:       {port}")

        if state.lower() == "open":
            print(f"ESTADO:      {GREEN}{state.upper()}{RESET}")
        else:
            print(f"ESTADO:      {state.upper()}")

        print(f"             ↳ {state_explanation}")
        print(f"SERVIÇO:     {service.upper()}")
        print(f"VERSÃO:      {version}")

        if info:
            print()
            print(f"{BLUE}O QUE É?{RESET}")
            print(f"└─ {info['what_is']}")

            print()
            print(f"{BLUE}O QUE SIGNIFICA?{RESET}")
            print(f"└─ {info['meaning']}")
        else:
            print()
            print(f"{BLUE}INFORMAÇÃO{RESET}")
            print("└─ O FREYY ainda não possui uma explicação")
            print("   específica para este serviço.")

        print()
        print("-" * 50)

    print()
    print(
        f"{YELLOW}[!] Uma porta aberta NÃO significa automaticamente"
        f"{RESET}"
    )
    print("    que existe uma vulnerabilidade.")


# ============================================================
# SCAN BÁSICO
# ============================================================

def basic_scan():
    network_banner()

    print()
    print("SCAN BÁSICO")
    print()

    target = input(
        "Digite um IP ou domínio autorizado: "
    ).strip()

    if not target:
        print(f"\n{YELLOW}[!] Alvo não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print("\n[+] Executando análise...\n")

    try:
        result = subprocess.run(
            ["nmap", "-sV", "-T3", target],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"{RED}[!] O Nmap retornou um erro.{RESET}")
            print(result.stderr)
            input("\nPressione ENTER para voltar...")
            return

        parsed = parse_nmap(result.stdout)
        show_results(parsed)

    except FileNotFoundError:
        print(f"\n{RED}[!] Nmap não está instalado.{RESET}")
        print("    Instale com: pkg install nmap")

    except subprocess.TimeoutExpired:
        print(
            f"\n{YELLOW}[!] A análise demorou demais "
            f"e foi interrompida.{RESET}"
        )

    input("\nPressione ENTER para voltar...")


# ============================================================
# PORT SCAN
# ============================================================

def port_scan():
    network_banner()

    print()
    print("SCANNER DE PORTAS")
    print()

    target = input(
        "Digite um IP ou domínio autorizado: "
    ).strip()

    if not target:
        print(f"\n{YELLOW}[!] Alvo não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    ports = input(
        "Digite as portas (ex: 22,80,443 ou 8000-8080): "
    ).strip()

    if not ports:
        print(f"\n{YELLOW}[!] Nenhuma porta informada.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    if not validate_ports(ports):
        print(f"\n{YELLOW}[!] Formato de porta inválido.{RESET}")
        print("    Exemplos válidos:")
        print("    22")
        print("    22,80,443")
        print("    8000-8080")
        input("\nPressione ENTER para voltar...")
        return

    print("\n[+] Verificando portas...\n")

    try:
        result = subprocess.run(
            ["nmap", "-sV", "-T3", "-p", ports, target],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"{RED}[!] O Nmap retornou um erro.{RESET}")
            print(result.stderr)
            input("\nPressione ENTER para voltar...")
            return

        parsed = parse_nmap(result.stdout)
        show_results(parsed)

    except FileNotFoundError:
        print(f"\n{RED}[!] Nmap não está instalado.{RESET}")
        print("    Instale com: pkg install nmap")

    except subprocess.TimeoutExpired:
        print(
            f"\n{YELLOW}[!] A análise demorou demais "
            f"e foi interrompida.{RESET}"
        )

    input("\nPressione ENTER para voltar...")


# ============================================================
# SERVICE SCAN
# ============================================================

def service_scan():
    network_banner()

    print()
    print("IDENTIFICADOR DE SERVIÇOS")
    print()

    target = input(
        "Digite um IP ou domínio autorizado: "
    ).strip()

    if not target:
        print(f"\n{YELLOW}[!] Alvo não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print("\n[+] Identificando serviços...\n")

    try:
        result = subprocess.run(
            ["nmap", "-sV", "-T3", target],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"{RED}[!] O Nmap retornou um erro.{RESET}")
            print(result.stderr)
            input("\nPressione ENTER para voltar...")
            return

        parsed = parse_nmap(result.stdout)
        show_results(parsed)

    except FileNotFoundError:
        print(f"\n{RED}[!] Nmap não está instalado.{RESET}")
        print("    Instale com: pkg install nmap")

    except subprocess.TimeoutExpired:
        print(
            f"\n{YELLOW}[!] A análise demorou demais "
            f"e foi interrompida.{RESET}"
        )

    input("\nPressione ENTER para voltar...")


# ============================================================
# TRACEROUTE
# ============================================================

def traceroute_scan():
    network_banner()

    print()
    print("TRACEROUTE")
    print()

    target = input(
        "Digite um IP ou domínio autorizado: "
    ).strip()

    if not target:
        print(f"\n{YELLOW}[!] Destino não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print("\n[+] Rastreando rota...\n")

    try:
        result = subprocess.run(
            ["traceroute", target],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.stdout:
            print(result.stdout)

        if result.returncode != 0 and result.stderr:
            print(f"{YELLOW}{result.stderr}{RESET}")

    except FileNotFoundError:
        print(f"\n{RED}[!] Traceroute não está instalado.{RESET}")
        print("    No Termux, tente:")
        print("    pkg install traceroute")

    except subprocess.TimeoutExpired:
        print(
            f"\n{YELLOW}[!] O traceroute demorou demais "
            f"e foi interrompido.{RESET}"
        )

    input("\nPressione ENTER para voltar...")


# ============================================================
# NETWORK MONITOR
# ============================================================

def connectivity_test():
    print(f"{BLUE}TESTE DE CONECTIVIDADE{RESET}")
    print("=" * 50)
    print()

    target = input(
        "Digite um domínio ou IP autorizado: "
    ).strip()

    if not target:
        print(f"\n{YELLOW}[!] Destino não informado.{RESET}")
        return

    print()
    print(f"[+] Testando {target}...")

    try:
        result = subprocess.run(
            ["ping", "-c", "4", "-W", "3", target],
            capture_output=True,
            text=True,
            timeout=20
        )

        print()

        if result.stdout:
            print(result.stdout)

        if result.returncode == 0:
            print(
                f"{GREEN}[+] Conectividade confirmada.{RESET}"
            )
        else:
            print(
                f"{YELLOW}[!] O destino não respondeu "
                f"como esperado.{RESET}"
            )

            if result.stderr:
                print(result.stderr)

    except FileNotFoundError:
        print(
            f"{RED}[!] O comando ping não está disponível.{RESET}"
        )

    except subprocess.TimeoutExpired:
        print(
            f"{YELLOW}[!] O teste demorou demais "
            f"e foi interrompido.{RESET}"
        )


def dns_lookup():
    print(f"{BLUE}CONSULTA DNS{RESET}")
    print("=" * 50)
    print()

    domain = input(
        "Digite um domínio: "
    ).strip()

    if not domain:
        print(f"\n{YELLOW}[!] Domínio não informado.{RESET}")
        return

    print()
    print(f"[+] Consultando {domain}...")

    try:
        addresses = socket.getaddrinfo(
            domain,
            None
        )

        unique_addresses = []

        for item in addresses:
            address = item[4][0]

            if address not in unique_addresses:
                unique_addresses.append(address)

        print()

        if unique_addresses:
            print(f"{GREEN}[+] Endereços encontrados:{RESET}")

            for address in unique_addresses:
                print(f"    └─ {address}")

        else:
            print(
                f"{YELLOW}[!] Nenhum endereço encontrado.{RESET}"
            )

    except socket.gaierror:
        print(
            f"{RED}[!] Não foi possível resolver o domínio.{RESET}"
        )

    except OSError as error:
        print(
            f"{RED}[!] Erro durante a consulta: {error}{RESET}"
        )


def get_public_ip():
    print(f"{BLUE}IP PÚBLICO{RESET}")
    print("=" * 50)
    print()

    print("[+] Consultando IP público...")

    services = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
    ]

    for url in services:

        try:
            response = requests.get(
                url,
                timeout=10
            )

            response.raise_for_status()

            ip = response.text.strip()

            if ip:
                print()
                print(
                    f"{GREEN}[+] IP público: {ip}{RESET}"
                )
                return

        except requests.RequestException:
            continue

    print()
    print(
        f"{YELLOW}[!] Não foi possível obter "
        f"o IP público.{RESET}"
    )


def network_monitor():

    while True:

        network_banner()

        print(f"{WHITE}NETWORK MONITOR{RESET}")
        print(f"{BLUE}{'─' * 40}{RESET}")
        print()

        print(f"{WHITE}STATUS TOOLS{RESET}")
        print()

        print(f"{BLUE}├─{RESET} {WHITE}[1] TESTE DE CONECTIVIDADE{RESET}")
        print(f"{BLUE}├─{RESET} {WHITE}[2] CONSULTA DNS{RESET}")
        print(f"{BLUE}├─{RESET} {WHITE}[3] IP PÚBLICO{RESET}")
        print(f"{BLUE}└─{RESET} {WHITE}[4] ATUALIZAR PAINEL{RESET}")

        print()
        print(f"{BLUE}{'─' * 40}{RESET}")
        print()
        print(f"{BLUE}[1-4] SELECT     [0] BACK{RESET}")
        print()

        choice = input("Escolha: ").strip()

        if choice == "1":

            clear_screen()
            network_banner()
            connectivity_test()
            input("\nPressione ENTER para voltar...")

        elif choice == "2":

            clear_screen()
            network_banner()
            dns_lookup()
            input("\nPressione ENTER para voltar...")

        elif choice == "3":

            clear_screen()
            network_banner()
            get_public_ip()
            input("\nPressione ENTER para voltar...")

        elif choice == "4":

            clear_screen()
            network_banner()

            print()
            print(f"{WHITE}ATUALIZANDO PAINEL...{RESET}")
            print()

            print(f"{BLUE}CONECTIVIDADE{RESET}")
            print("-" * 50)

            try:
                result = subprocess.run(
                    ["ping", "-c", "1", "-W", "3", "1.1.1.1"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    print(
                        f"{GREEN}[ONLINE] Internet acessível{RESET}"
                    )
                else:
                    print(
                        f"{YELLOW}[OFFLINE] "
                        f"Sem resposta de teste{RESET}"
                    )

            except (FileNotFoundError, subprocess.TimeoutExpired):
                print(
                    f"{YELLOW}[!] Não foi possível "
                    f"realizar o teste.{RESET}"
                )

            print()
            print(f"{BLUE}DNS LOCAL{RESET}")
            print("-" * 50)

            try:
                addresses = socket.getaddrinfo(
                    "google.com",
                    None
                )

                if addresses:
                    print(
                        f"{GREEN}[OK] Resolução DNS funcionando{RESET}"
                    )
                else:
                    print(
                        f"{YELLOW}[!] DNS não retornou resultados{RESET}"
                    )

            except socket.gaierror:
                print(
                    f"{YELLOW}[!] Falha na resolução DNS{RESET}"
                )

            print()
            print(f"{BLUE}IP PÚBLICO{RESET}")
            print("-" * 50)

            try:
                response = requests.get(
                    "https://api.ipify.org",
                    timeout=10
                )

                response.raise_for_status()

                print(
                    f"{GREEN}{response.text.strip()}{RESET}"
                )

            except requests.RequestException:
                print(
                    f"{YELLOW}[!] IP público indisponível{RESET}"
                )

            print()
            input("Pressione ENTER para voltar...")

        elif choice == "0":

            break

        else:

            print(
                f"\n{YELLOW}[!] Opção inválida.{RESET}"
            )

            time.sleep(1)


# ============================================================
# MENU NETWORK
# ============================================================

def open_network():

    while True:

        network_banner()

        print(f"{WHITE}NETWORK MODULE{RESET}")
        print(f"{BLUE}{'─' * 40}{RESET}")
        print()

        print(f"{WHITE}TOOLS{RESET}")
        print()

        print(f"{BLUE}├─{RESET} {WHITE}[1] BASIC SCAN{RESET}")
        print(f"{BLUE}├─{RESET} {WHITE}[2] PORT SCAN{RESET}")
        print(f"{BLUE}├─{RESET} {WHITE}[3] SERVICE SCAN{RESET}")
        print(f"{BLUE}├─{RESET} {WHITE}[4] TRACEROUTE{RESET}")
        print(f"{BLUE}└─{RESET} {WHITE}[5] NETWORK MONITOR{RESET}")

        print()
        print(f"{BLUE}{'─' * 40}{RESET}")
        print()
        print(f"{BLUE}[1-5] SELECT     [0] BACK{RESET}")
        print()

        choice = input("Escolha: ").strip()

        if choice == "1":

            basic_scan()

        elif choice == "2":

            port_scan()

        elif choice == "3":

            service_scan()

        elif choice == "4":

            traceroute_scan()

        elif choice == "5":

            network_monitor()

        elif choice == "0":

            break

        else:

            print(
                f"\n{YELLOW}"
                "[!] Essa função ainda está em desenvolvimento."
                f"{RESET}"
            )

            input("\nPressione ENTER para continuar...")


# ============================================================
# LIMPAR TERMINAL
# ============================================================

def clear_screen():
    os.system("clear")
