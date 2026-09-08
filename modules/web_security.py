import requests
import subprocess
import socket
from urllib.parse import urlparse


PURPLE = "\033[1;35m"
WHITE = "\033[1;37m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"


SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "Ajuda a controlar quais recursos o navegador pode carregar."
    ),
    "Strict-Transport-Security": (
        "Instrui o navegador a preferir conexões HTTPS."
    ),
    "X-Content-Type-Options": (
        "Ajuda a impedir interpretações incorretas do tipo de conteúdo."
    ),
    "X-Frame-Options": (
        "Ajuda a controlar carregamento dentro de frames."
    ),
    "Referrer-Policy": (
        "Controla quais informações de referência podem ser enviadas."
    ),
    "Permissions-Policy": (
        "Controla o acesso do navegador a recursos e APIs."
    ),
}


def web_banner():
    print()
    print(f"{RED}")
    print(" __        _______ ____    ____ ")
    print(" \\ \\      / / ____| __ )  |  _ \\")
    print("  \\ \\ /\\ / /|  _| |  _ \\  | |_) |")
    print("   \\ V  V / | |___| |_) | |  _ <")
    print("    \\_/\\_/  |_____|____/  |_| \\_\\")
    print(f"{RESET}")

    print(f"{WHITE}FREYY / WEB SECURITY{RESET}")
    print(f"{WHITE}WEB SECURITY MODULE{RESET}")
    print(f"{RED}{'─' * 40}{RESET}")
    print()
def normalize_url(url):
    url = url.strip()

    if not url:
        return None

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.hostname:
        return None

    return url


def get_domain(target):
    parsed = urlparse(target)

    if not parsed.hostname:
        return None

    return parsed.hostname.lower()


def request_site(target):
    return requests.get(
        target,
        timeout=10,
        allow_redirects=True,
        headers={
            "User-Agent": "FREYY-WebSecurity/1.0"
        }
    )


def print_http_summary(response):
    print(f"{WHITE}STATUS HTTP:{RESET} {response.status_code}")
    print(f"{WHITE}URL FINAL:{RESET} {response.url}")
    print(f"{WHITE}CONTENT-TYPE:{RESET} "
          f"{response.headers.get('Content-Type', 'Não informado')}")
    print()


def security_headers_scan():
    web_banner()

    print("SECURITY HEADERS")
    print()

    target = input("Digite um site autorizado: ").strip()
    target = normalize_url(target)

    if not target:
        print(f"\n{YELLOW}[!] URL inválida ou não informada.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Consultando: {target}")
    print()

    try:
        response = request_site(target)

        print_http_summary(response)

        present = 0
        missing = 0

        for header, explanation in SECURITY_HEADERS.items():
            value = response.headers.get(header)

            print("-" * 55)
            print(f"{WHITE}{header}{RESET}")

            if value:
                present += 1

                print(f"{GREEN}[✓] PRESENTE{RESET}")
                print(f"    Valor: {value}")
                print(f"    ↳ {explanation}")

            else:
                missing += 1

                print(f"{YELLOW}[-] AUSENTE{RESET}")
                print(f"    ↳ {explanation}")

        print()
        print("=" * 55)
        print(f"{PURPLE}RESUMO{RESET}")
        print("=" * 55)
        print(f"{GREEN}Headers presentes: {present}{RESET}")
        print(f"{YELLOW}Headers ausentes:  {missing}{RESET}")

        if present == len(SECURITY_HEADERS):
            print(
                f"\n{GREEN}"
                "[✓] Todos os headers analisados estão presentes."
                f"{RESET}"
            )

        elif present >= len(SECURITY_HEADERS) // 2:
            print(
                f"\n{CYAN}"
                "[i] Parte dos headers analisados está presente."
                f"{RESET}"
            )

        else:
            print(
                f"\n{YELLOW}"
                "[!] Vários headers de segurança não foram identificados."
                f"{RESET}"
            )

        print()
        print("A ausência de um header não prova uma vulnerabilidade.")
        print("A análise considera somente informações HTTP públicas.")
        print("Nenhuma exploração foi realizada.")

    except requests.exceptions.SSLError as error:
        print(f"\n{RED}[!] Erro de certificado TLS.{RESET}")
        print(f"    {error}")

    except requests.exceptions.Timeout:
        print(f"\n{RED}[!] A conexão expirou.{RESET}")

    except requests.RequestException as error:
        print(f"\n{RED}[!] Não foi possível consultar o site.{RESET}")
        print(f"    Erro: {error}")

    input("\nPressione ENTER para voltar...")


def https_check():
    web_banner()

    print("HTTPS / TLS")
    print()

    target = input("Digite um site autorizado: ").strip()
    target = normalize_url(target)

    if not target:
        print(f"\n{YELLOW}[!] URL inválida ou não informada.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Verificando: {target}")
    print()

    try:
        response = request_site(target)

        final_url = response.url

        print(f"{WHITE}URL INFORMADA:{RESET} {target}")
        print(f"{WHITE}URL FINAL:{RESET}     {final_url}")
        print(f"{WHITE}STATUS HTTP:{RESET}   {response.status_code}")
        print()

        if final_url.lower().startswith("https://"):
            print(f"{GREEN}[✓] HTTPS está sendo utilizado.{RESET}")

            if target.lower().startswith("http://"):
                print(
                    f"{GREEN}[✓] O site redirecionou HTTP para HTTPS.{RESET}"
                )

        else:
            print(f"{YELLOW}[!] A URL final não utiliza HTTPS.{RESET}")

        print()
        print(f"{PURPLE}RESUMO{RESET}")
        print("=" * 55)
        print("O FREYY verificou somente HTTP/HTTPS")
        print("e os redirecionamentos observáveis.")

    except requests.exceptions.SSLError as error:
        print(f"\n{RED}[!] Falha na validação TLS.{RESET}")
        print(f"    {error}")

    except requests.exceptions.Timeout:
        print(f"\n{RED}[!] A conexão expirou.{RESET}")

    except requests.RequestException as error:
        print(f"\n{RED}[!] Não foi possível consultar o site.{RESET}")
        print(f"    Erro: {error}")

    input("\nPressione ENTER para voltar...")


def cookie_security_scan():
    web_banner()

    print("COOKIE SECURITY")
    print()

    target = input("Digite um site autorizado: ").strip()
    target = normalize_url(target)

    if not target:
        print(f"\n{YELLOW}[!] URL inválida ou não informada.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Analisando cookies públicos de: {target}")
    print()

    try:
        response = request_site(target)

        cookie_headers = response.raw.headers.get_all("Set-Cookie")

        if not cookie_headers:
            print(
                f"{YELLOW}"
                "[-] Nenhum cookie enviado diretamente nesta resposta."
                f"{RESET}"
            )

            print()
            print("Isso não significa que o site não utilize cookies.")
            print("Cookies podem ser criados por outras respostas")
            print("ou por JavaScript.")

            input("\nPressione ENTER para voltar...")
            return

        print(
            f"{GREEN}[✓] {len(cookie_headers)} "
            f"cookie(s) encontrado(s).{RESET}"
        )
        print()

        for number, cookie in enumerate(cookie_headers, 1):
            parts = [part.strip() for part in cookie.split(";")]

            name = parts[0].split("=", 1)[0]

            attributes = {
                part.lower().split("=", 1)[0].strip()
                for part in parts[1:]
            }

            secure = "secure" in attributes
            httponly = "httponly" in attributes

            samesite = any(
                attr.startswith("samesite")
                for attr in attributes
            )

            print("-" * 55)
            print(f"{WHITE}COOKIE #{number}: {name}{RESET}")
            print()

            if secure:
                print(f"{GREEN}[✓] Secure{RESET}")
            else:
                print(f"{YELLOW}[-] Secure ausente{RESET}")

            if httponly:
                print(f"{GREEN}[✓] HttpOnly{RESET}")
            else:
                print(f"{YELLOW}[-] HttpOnly ausente{RESET}")

            if samesite:
                print(f"{GREEN}[✓] SameSite definido{RESET}")
            else:
                print(f"{YELLOW}[-] SameSite ausente{RESET}")

        print()
        print("=" * 55)
        print(f"{PURPLE}RESUMO{RESET}")
        print("=" * 55)
        print("Foram analisados somente os atributos")
        print("presentes nos cabeçalhos Set-Cookie.")
        print()
        print("A ausência de um atributo isoladamente")
        print("não significa que exista uma vulnerabilidade.")

    except requests.exceptions.Timeout:
        print(f"\n{RED}[!] A conexão expirou.{RESET}")

    except requests.RequestException as error:
        print(f"\n{RED}[!] Não foi possível consultar o site.{RESET}")
        print(f"    Erro: {error}")

    input("\nPressione ENTER para voltar...")


def dns_lookup(target, record_type):
    try:
        result = subprocess.run(
            ["nslookup", f"-type={record_type}", target],
            capture_output=True,
            text=True,
            timeout=10
        )

        return result.stdout

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def extract_dns_values(output, record_type):
    values = []

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        if record_type in ("A", "AAAA") and line.startswith("Address:"):
            value = line.split(":", 1)[1].strip()

            if "#" in value:
                value = value.split("#")[0]

            if record_type == "A" and ":" not in value:
                values.append(value)

            elif record_type == "AAAA" and ":" in value:
                values.append(value)

        elif record_type == "MX" and "mail exchanger =" in line:
            value = line.split("mail exchanger =", 1)[1].strip()
            values.append(value)

        elif record_type == "NS" and "nameserver =" in line:
            value = line.split("nameserver =", 1)[1].strip()
            values.append(value)

        elif record_type == "TXT" and "text =" in line:
            value = line.split("text =", 1)[1].strip()
            values.append(value)

    return list(dict.fromkeys(values))


def dns_security_scan():
    web_banner()

    print("DNS SECURITY")
    print()

    target = input("Digite um domínio autorizado: ").strip().lower()

    if not target:
        print(f"\n{YELLOW}[!] Domínio não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    if target.startswith("https://"):
        target = target[8:]

    elif target.startswith("http://"):
        target = target[7:]

    target = target.split("/")[0].split(":")[0]

    print()
    print(f"[+] Analisando DNS público de: {target}")
    print()

    record_types = ["A", "AAAA", "MX", "NS", "TXT"]
    found_records = 0

    for record_type in record_types:
        print("-" * 55)
        print(f"{WHITE}REGISTROS {record_type}{RESET}")
        print()

        output = dns_lookup(target, record_type)

        if not output:
            print(f"{YELLOW}[-] Nenhuma resposta encontrada.{RESET}")
            continue

        values = extract_dns_values(output, record_type)

        if not values:
            print(f"{YELLOW}[-] Nenhum registro identificado.{RESET}")
            continue

        found_records += len(values)

        for value in values:
            print(f"{GREEN}[✓] {value}{RESET}")

    print()
    print("=" * 55)
    print(f"{PURPLE}RESUMO{RESET}")
    print("=" * 55)
    print(f"{GREEN}Registros identificados: {found_records}{RESET}")
    print()
    print("A = IPv4")
    print("AAAA = IPv6")
    print("MX = servidores de e-mail")
    print("NS = servidores DNS")
    print("TXT = informações públicas de texto")
    print()
    print("Nenhuma alteração ou exploração DNS foi realizada.")

    input("\nPressione ENTER para voltar...")


def http_information_scan():
    web_banner()

    print("HTTP INFORMATION")
    print()

    target = input("Digite um site autorizado: ").strip()
    target = normalize_url(target)

    if not target:
        print(f"\n{YELLOW}[!] URL inválida ou não informada.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Consultando: {target}")
    print()

    try:
        response = request_site(target)

        print("=" * 55)
        print(f"{PURPLE}INFORMAÇÕES DA RESPOSTA{RESET}")
        print("=" * 55)

        print(f"{WHITE}STATUS HTTP:{RESET} "
              f"{response.status_code}")
        print(f"{WHITE}MÉTODO:{RESET} "
              f"{response.request.method}")
        print(f"{WHITE}URL FINAL:{RESET} "
              f"{response.url}")
        print(f"{WHITE}CONTENT-TYPE:{RESET} "
              f"{response.headers.get('Content-Type', 'Não informado')}")
        print(f"{WHITE}CONTENT-LENGTH:{RESET} "
              f"{response.headers.get('Content-Length', 'Não informado')}")
        print(f"{WHITE}SERVER:{RESET} "
              f"{response.headers.get('Server', 'Não informado')}")

        print()
        print("=" * 55)
        print(f"{PURPLE}REDIRECIONAMENTOS{RESET}")
        print("=" * 55)

        if response.history:
            print(
                f"{GREEN}[✓] {len(response.history)} "
                f"redirecionamento(s).{RESET}"
            )

            for number, redirect in enumerate(response.history, 1):
                print(
                    f"    {number}. "
                    f"{redirect.status_code} → {redirect.url}"
                )

        else:
            print(f"{GREEN}[✓] Nenhum redirecionamento.{RESET}")

        print()
        print("=" * 55)
        print(f"{PURPLE}HEADERS PRINCIPAIS{RESET}")
        print("=" * 55)

        important_headers = [
            "Date",
            "Cache-Control",
            "ETag",
            "Last-Modified",
            "Location",
            "Vary",
            "Connection"
        ]

        found = 0

        for header in important_headers:
            value = response.headers.get(header)

            if value:
                found += 1
                print(f"{WHITE}{header}:{RESET} {value}")

        if found == 0:
            print(f"{YELLOW}[-] Nenhum header adicional.{RESET}")

        print()
        print("A análise utiliza somente informações HTTP")
        print("publicamente acessíveis.")

    except requests.exceptions.Timeout:
        print(f"\n{RED}[!] A conexão expirou.{RESET}")

    except requests.RequestException as error:
        print(f"\n{RED}[!] Não foi possível consultar o site.{RESET}")
        print(f"    Erro: {error}")

    input("\nPressione ENTER para voltar...")


def redirect_domain_check():
    web_banner()

    print("REDIRECT & DOMAIN CHECK")
    print()

    target = input("Digite um site autorizado: ").strip()
    target = normalize_url(target)

    if not target:
        print(f"\n{YELLOW}[!] URL inválida ou não informada.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print(f"[+] Analisando redirecionamentos de: {target}")
    print()

    try:
        response = request_site(target)

        print("=" * 55)
        print(f"{PURPLE}DOMÍNIO / URL{RESET}")
        print("=" * 55)

        print(f"{WHITE}URL informada:{RESET}")
        print(f"  {target}")

        print()
        print(f"{WHITE}URL final:{RESET}")
        print(f"  {response.url}")

        print()
        print(f"{WHITE}Status final:{RESET} {response.status_code}")

        print()
        print("=" * 55)
        print(f"{PURPLE}CADEIA DE REDIRECIONAMENTO{RESET}")
        print("=" * 55)

        if response.history:
            for number, redirect in enumerate(response.history, 1):
                print(
                    f"{number}. "
                    f"{redirect.status_code} → {redirect.url}"
                )

            print()
            print(
                f"{GREEN}[✓] {len(response.history)} "
                f"redirecionamento(s).{RESET}"
            )

        else:
            print(
                f"{GREEN}[✓] Nenhum redirecionamento HTTP.{RESET}"
            )

        print()
        print("=" * 55)
        print(f"{PURPLE}HTTPS{RESET}")
        print("=" * 55)

        if response.url.lower().startswith("https://"):
            print(f"{GREEN}[✓] URL final utiliza HTTPS.{RESET}")
        else:
            print(f"{YELLOW}[!] URL final não utiliza HTTPS.{RESET}")

        print()
        print("=" * 55)
        print(f"{PURPLE}RESUMO{RESET}")
        print("=" * 55)

        if response.url == target:
            print("A URL final é igual à URL informada.")

        else:
            print("A URL final é diferente da URL informada.")
            print("O servidor realizou uma mudança de destino.")

        print()
        print("Nenhuma exploração foi realizada.")

    except requests.exceptions.Timeout:
        print(f"\n{RED}[!] A conexão expirou.{RESET}")

    except requests.RequestException as error:
        print(f"\n{RED}[!] Não foi possível consultar o site.{RESET}")
        print(f"    Erro: {error}")

    input("\nPressione ENTER para voltar...")


def open_web_security():
    while True:
        web_banner()

        print("""
[1] Security Headers
[2] HTTPS / TLS
[3] Cookie Security
[4] DNS Security
[5] HTTP Information
[6] Redirect & Domain Check

[0] Voltar
""")

        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            security_headers_scan()

        elif choice == "2":
            https_check()

        elif choice == "3":
            cookie_security_scan()

        elif choice == "4":
            dns_security_scan()

        elif choice == "5":
            http_information_scan()

        elif choice == "6":
            redirect_domain_check()

        elif choice == "0":
            break

        else:
            print(
                f"\n{YELLOW}"
                "[!] Opção inválida."
                f"{RESET}"
            )

            input("\nPressione ENTER para continuar...")
