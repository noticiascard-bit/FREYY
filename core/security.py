import ipaddress
from urllib.parse import urlparse


def normalize_target(target):
    target = target.strip()

    if not target:
        return None

    if not target.startswith(("http://", "https://")):
        target = "https://" + target

    parsed = urlparse(target)

    if not parsed.hostname:
        return None

    return target


def is_local_target(target):
    try:
        hostname = urlparse(target).hostname

        if not hostname:
            return False

        if hostname == "localhost":
            return True

        ip = ipaddress.ip_address(hostname)

        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
        )

    except ValueError:
        return False


def authorization_warning(target):
    print()
    print("=" * 50)
    print("FREYY SECURITY CHECK")
    print("=" * 50)
    print()
    print("O FREYY deve ser usado somente em:")
    print("- sistemas próprios;")
    print("- ambientes de laboratório;")
    print("- sistemas para os quais você possui autorização.")
    print()
    print(f"Alvo: {target}")
    print()

    if is_local_target(target):
        print("[✓] Alvo local detectado.")
        print("[✓] Ambiente adequado para testes locais.")
        return True

    answer = input(
        "Você possui autorização para analisar este alvo? [s/N]: "
    ).strip().lower()

    if answer != "s":
        print()
        print("[!] Análise cancelada pelo Security Core.")
        return False

    print()
    print("[✓] Confirmação registrada para esta execução.")
    return True


def safe_request_options():
    return {
        "timeout": 10,
        "allow_redirects": True,
        "headers": {
            "User-Agent": "FREYY-Security/1.0"
        }
    }
