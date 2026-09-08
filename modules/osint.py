import requests
import socket
import ipaddress


GRAY = "\033[1;37m"
WHITE = "\033[1;37m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"


def osint_banner():
    print()
    print(f"{RED}")
    print("   ___  _____ ___ _   _ _____")
    print("  / _ \\|  ___|_ _| \\ | |_   _|")
    print(" | | | | |_   | ||  \\| | | |")
    print(" | |_| |  _|  | || |\\  | | |")
    print("  \\___/|_|   |___|_| \\_| |_|")
    print(f"{RESET}")

    print(f"{WHITE}FREYY / OSINT{RESET}")
    print(f"{GRAY}OPEN-SOURCE INTELLIGENCE{RESET}")
    print(f"{GRAY}{'─' * 40}{RESET}")
    print()
def normalize_domain(domain):
    domain = domain.strip().lower()

    if domain.startswith("https://"):
        domain = domain[8:]

    elif domain.startswith("http://"):
        domain = domain[7:]

    domain = domain.split("/")[0]
    domain = domain.split(":")[0]

    return domain.strip(".")


def resolve_records(domain):
    records = {}

    record_types = {
        "IPv4": socket.AF_INET,
        "IPv6": socket.AF_INET6,
    }

    for name, family in record_types.items():
        try:
            results = socket.getaddrinfo(
                domain,
                None,
                family,
                socket.SOCK_STREAM
            )

            addresses = sorted(
                {result[4][0] for result in results}
            )

            if addresses:
                records[name] = addresses

        except socket.gaierror:
            pass

    return records


def username_scan():
    osint_banner()

    print()
    print("USERNAME OSINT")
    print()

    username = input("Digite um username público: ").strip()

    if not username:
        print(f"\n{YELLOW}[!] Username não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    username = username.lstrip("@").strip()

    if not username:
        print(f"\n{YELLOW}[!] Username inválido.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Procurando presença pública de: @{username}")
    print()

    url = f"https://github.com/{username}"

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "FREYY-OSINT/1.0"
            }
        )

        if response.status_code == 200:
            print(f"{GREEN}[✓] Perfil público encontrado.{RESET}")
            print("    Plataforma: GitHub")
            print(f"    Username:   @{username}")
            print(f"    URL:        {url}")

        elif response.status_code == 404:
            print(f"{YELLOW}[-] Perfil não encontrado no GitHub.{RESET}")

        else:
            print(
                f"{YELLOW}[!] Não foi possível verificar o GitHub."
                f"{RESET}"
            )
            print(f"    HTTP: {response.status_code}")

    except requests.Timeout:
        print(f"{YELLOW}[!] Tempo limite excedido.{RESET}")

    except requests.RequestException:
        print(
            f"{RED}[!] Não foi possível consultar o GitHub."
            f"{RESET}"
        )

    print()
    print(
        f"{CYAN}[i] Um resultado público não comprova "
        f"que uma conta pertence a uma pessoa específica.{RESET}"
    )

    input("\nPressione ENTER para voltar...")


def domain_scan():
    osint_banner()

    print()
    print("DOMAIN OSINT")
    print()

    domain = input("Digite um domínio autorizado: ").strip()

    if not domain:
        print(f"\n{YELLOW}[!] Domínio não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    domain = normalize_domain(domain)

    if not domain:
        print(f"\n{RED}[!] Domínio inválido.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Consultando: {domain}")
    print()

    records = resolve_records(domain)

    if not records:
        print(f"{RED}[!] Domínio não resolvido.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print(f"{GREEN}[✓] DNS resolvido.{RESET}")

    if "IPv4" in records:
        print()
        print("IPv4")
        for address in records["IPv4"]:
            print(f"    {address}")

    if "IPv6" in records:
        print()
        print("IPv6")
        for address in records["IPv6"]:
            print(f"    {address}")

    try:
        hostname, aliases, addresses = socket.gethostbyaddr(
            records.get("IPv4", records.get("IPv6"))[0]
        )

        print()
        print(f"{GREEN}[✓] DNS reverso encontrado.{RESET}")
        print(f"    Hostname: {hostname}")

        if aliases:
            print(f"    Aliases:  {', '.join(aliases)}")

    except (socket.herror, socket.gaierror, IndexError):
        print()
        print(f"{YELLOW}[-] Nenhum DNS reverso encontrado.{RESET}")

    input("\nPressione ENTER para voltar...")


def ip_scan():
    osint_banner()

    print()
    print("IP OSINT")
    print()

    ip = input("Digite um IP público: ").strip()

    if not ip:
        print(f"\n{YELLOW}[!] IP não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    try:
        address = ipaddress.ip_address(ip)

    except ValueError:
        print(f"\n{RED}[!] IP inválido.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Consultando: {ip}")
    print()

    print(f"{GREEN}[✓] IP válido.{RESET}")
    print(f"    Versão: IPv{address.version}")

    if address.is_private:
        print(f"    Tipo:    Rede privada")

    elif address.is_loopback:
        print(f"    Tipo:    Loopback")

    elif address.is_reserved:
        print(f"    Tipo:    Reservado")

    elif address.is_link_local:
        print(f"    Tipo:    Link-local")

    else:
        print(f"    Tipo:    Endereço público")

    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip)

        print()
        print(f"{GREEN}[✓] Reverse DNS encontrado.{RESET}")
        print(f"    Hostname: {hostname}")

        if aliases:
            print(f"    Aliases:  {', '.join(aliases)}")

    except socket.herror:
        print()
        print(f"{YELLOW}[-] Nenhum hostname reverso encontrado.{RESET}")

    except socket.gaierror:
        print()
        print(f"{YELLOW}[-] Não foi possível consultar o reverse DNS.{RESET}")

    input("\nPressione ENTER para voltar...")


def public_info_scan():
    osint_banner()

    print()
    print("INFORMAÇÕES PÚBLICAS")
    print()

    target = input("Digite um domínio público: ").strip()

    if not target:
        print(f"\n{YELLOW}[!] Alvo não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    target = normalize_domain(target)

    if not target:
        print(f"\n{RED}[!] Domínio inválido.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Analisando: {target}")
    print()

    records = resolve_records(target)

    if not records:
        print(f"{RED}[!] Não foi possível resolver o domínio.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print(f"{GREEN}[✓] RESOLUÇÃO DNS{RESET}")
    print("────────────────────────────")

    if "IPv4" in records:
        print("IPv4:")
        for address in records["IPv4"]:
            print(f"    {address}")

    if "IPv6" in records:
        print("IPv6:")
        for address in records["IPv6"]:
            print(f"    {address}")

    reverse_hostname = None

    addresses = records.get("IPv4", []) + records.get("IPv6", [])

    if addresses:
        try:
            hostname, aliases, _ = socket.gethostbyaddr(
                addresses[0]
            )

            reverse_hostname = hostname

        except (socket.herror, socket.gaierror):
            pass

    print()
    print(f"{GREEN}[✓] DNS REVERSO{RESET}")
    print("────────────────────────────")

    if reverse_hostname:
        print(f"Hostname: {reverse_hostname}")
    else:
        print("Nenhum hostname reverso encontrado.")

    print()
    print("RESUMO")
    print("────────────────────────────")
    print(f"Domínio analisado: {target}")
    print(f"IPv4 encontrados:  {len(records.get('IPv4', []))}")
    print(f"IPv6 encontrados:  {len(records.get('IPv6', []))}")

    if reverse_hostname:
        print("Reverse DNS:       encontrado")
    else:
        print("Reverse DNS:       não encontrado")

    print()
    print(
        f"{CYAN}Nenhuma exploração foi realizada. "
        f"Somente informações públicas de resolução DNS foram consultadas.{RESET}"
    )

    input("\nPressione ENTER para voltar...")


def open_osint():
    while True:
        osint_banner()

        print("""
[1] Username
[2] Domínio
[3] IP público
[4] Informações públicas

[0] Voltar
""")

        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            username_scan()

        elif choice == "2":
            domain_scan()

        elif choice == "3":
            ip_scan()

        elif choice == "4":
            public_info_scan()

        elif choice == "0":
            break

        else:
            print(
                f"\n{YELLOW}"
                "[!] Opção inválida."
                f"{RESET}"
            )
            input("\nPressione ENTER para continuar...")
