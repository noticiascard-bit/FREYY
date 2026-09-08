import os
import hashlib
import mimetypes
from datetime import datetime


GRAY = "\033[1;37m"
WHITE = "\033[1;37m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"


def file_banner():
    print(f"""
{GRAY}
        ███████╗██╗██╗     ███████╗
        ██╔════╝██║██║     ██╔════╝
        █████╗  ██║██║     █████╗
        ██╔══╝  ██║██║     ██╔══╝
        ██║     ██║███████╗███████╗
        ╚═╝     ╚═╝╚══════╝╚══════╝

{WHITE}                 FILE ANALYZER{RESET}
""")


def calculate_hashes(path):
    hashes = {
        "MD5": hashlib.md5(),
        "SHA-1": hashlib.sha1(),
        "SHA-256": hashlib.sha256()
    }

    try:
        with open(path, "rb") as file:
            while True:
                data = file.read(1024 * 1024)

                if not data:
                    break

                for algorithm in hashes.values():
                    algorithm.update(data)

        return {
            name: algorithm.hexdigest()
            for name, algorithm in hashes.items()
        }

    except (OSError, PermissionError):
        return None


def calculate_sha256(path):
    hashes = calculate_hashes(path)

    if hashes:
        return hashes["SHA-256"]

    return None


def get_line_count(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            return sum(1 for _ in file)

    except (OSError, PermissionError):
        return None


def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


def read_magic_bytes(path, amount=16):
    try:
        with open(path, "rb") as file:
            return file.read(amount)

    except (OSError, PermissionError):
        return None


def identify_magic(data):
    if not data:
        return "Desconhecido"

    signatures = [
        (b"PK\x03\x04", "ZIP / APK / DOCX / etc."),
        (b"\x7fELF", "ELF / Executável Linux"),
        (b"MZ", "PE / Executável Windows"),
        (b"\x89PNG\r\n\x1a\n", "PNG"),
        (b"\xff\xd8\xff", "JPEG"),
        (b"GIF87a", "GIF"),
        (b"GIF89a", "GIF"),
        (b"%PDF", "PDF"),
        (b"RIFF", "RIFF / WAV / AVI / WebP"),
        (b"SQLite format 3\x00", "SQLite"),
        (b"Rar!\x1a\x07\x00", "RAR"),
        (b"\x1f\x8b", "GZIP"),
        (b"BZh", "BZIP2"),
        (b"\xfd7zXZ\x00", "XZ"),
        (b"7z\xbc\xaf\x27\x1c", "7-Zip"),
    ]

    for signature, file_type in signatures:
        if data.startswith(signature):
            return file_type

    return "Desconhecido"


def extract_strings(path, minimum=4, limit=100):
    strings = []
    current = bytearray()

    try:
        with open(path, "rb") as file:
            while True:
                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                for byte in chunk:
                    if 32 <= byte <= 126:
                        current.append(byte)

                    else:
                        if len(current) >= minimum:
                            strings.append(current.decode("ascii", errors="ignore"))

                            if len(strings) >= limit:
                                return strings

                        current.clear()

            if len(current) >= minimum:
                strings.append(
                    current.decode("ascii", errors="ignore")
                )

        return strings

    except (OSError, PermissionError):
        return None


def compare_file_type(extension, magic_type):
    if magic_type == "Desconhecido":
        return None

    extension = extension.lower()

    known_extensions = {
        "PNG": [".png"],
        "JPEG": [".jpg", ".jpeg"],
        "GIF": [".gif"],
        "PDF": [".pdf"],
        "SQLite": [".db", ".sqlite", ".sqlite3"],
        "GZIP": [".gz"],
        "BZIP2": [".bz2"],
        "XZ": [".xz"],
        "7-Zip": [".7z"],
        "RAR": [".rar"],
        "PE / Executável Windows": [".exe", ".dll"],
        "ELF / Executável Linux": [".elf", ".so"],
    }

    for file_type, extensions in known_extensions.items():
        if file_type in magic_type:
            return extension in extensions

    if "ZIP" in magic_type:
        return extension in [
            ".zip",
            ".apk",
            ".jar",
            ".docx",
            ".xlsx",
            ".pptx"
        ]

    return None


def show_file_info(path):
    file_banner()

    print("ANÁLISE ESTÁTICA DO ARQUIVO")
    print("=" * 60)

    try:
        stat = os.stat(path)

    except FileNotFoundError:
        print(f"{RED}[!] Arquivo não encontrado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    except PermissionError:
        print(f"{RED}[!] Permissão negada para acessar o arquivo.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    filename = os.path.basename(path)
    extension = os.path.splitext(filename)[1]

    if not extension:
        extension = "Sem extensão"

    mime_type, _ = mimetypes.guess_type(path)

    if mime_type is None:
        mime_type = "Desconhecido"

    modified = datetime.fromtimestamp(stat.st_mtime)
    permissions = oct(stat.st_mode & 0o777)

    print(f"Nome:          {filename}")
    print(f"Caminho:       {os.path.abspath(path)}")
    print(f"Tamanho:       {format_size(stat.st_size)}")
    print(f"Extensão:      {extension}")
    print(f"Tipo MIME:     {mime_type}")
    print(f"Permissões:    {permissions}")
    print(f"Modificado:    {modified.strftime('%Y-%m-%d %H:%M:%S')}")

    if stat.st_size == 0:
        print(f"\n{YELLOW}[!] O arquivo está vazio.{RESET}")

    print()

    print(f"{CYAN}[+] Calculando hashes...{RESET}")

    hashes = calculate_hashes(path)

    if hashes:
        print(f"{GREEN}[✓] MD5:{RESET}")
        print(f"    {hashes['MD5']}")

        print(f"{GREEN}[✓] SHA-1:{RESET}")
        print(f"    {hashes['SHA-1']}")

        print(f"{GREEN}[✓] SHA-256:{RESET}")
        print(f"    {hashes['SHA-256']}")

    else:
        print(f"{RED}[!] Não foi possível calcular os hashes.{RESET}")

    print()

    magic_data = read_magic_bytes(path)

    if magic_data is not None:
        magic_type = identify_magic(magic_data)

        print(f"{CYAN}[+] Magic Bytes:{RESET}")
        print(f"    {magic_data.hex(' ')}")

        print(f"{CYAN}[+] Tipo identificado pelo conteúdo:{RESET}")
        print(f"    {magic_type}")

        comparison = compare_file_type(extension, magic_type)

        if comparison is False:
            print(
                f"\n{YELLOW}[!] Atenção: a extensão "
                f"não corresponde ao tipo identificado.{RESET}"
            )

        elif comparison is True:
            print(
                f"{GREEN}[✓] Extensão compatível com "
                f"o tipo identificado.{RESET}"
            )

    text_extensions = {
        ".txt",
        ".py",
        ".sh",
        ".json",
        ".xml",
        ".html",
        ".css",
        ".js",
        ".md",
        ".csv",
        ".log",
        ".ini",
        ".conf"
    }

    if extension.lower() in text_extensions:
        lines = get_line_count(path)

        if lines is not None:
            print(f"\nLinhas:        {lines}")

    print()

    print(f"{CYAN}[+] Extraindo strings...{RESET}")

    strings = extract_strings(path)

    if strings is not None:
        print(
            f"{GREEN}[✓] {len(strings)} strings "
            f"encontradas (máximo: 100).{RESET}"
        )

        if strings:
            print()
            print("STRINGS:")

            for index, string in enumerate(strings, 1):
                print(f"  {index:03d}: {string}")

    else:
        print(f"{YELLOW}[!] Não foi possível ler o arquivo.{RESET}")

    print()
    print(f"{GREEN}[✓] Análise estática concluída.{RESET}")
    print(f"{GRAY}    Nenhum arquivo foi executado ou enviado.{RESET}")

    input("\nPressione ENTER para voltar...")


def analyze_file():
    file_banner()

    print("ANALISAR ARQUIVO")
    print()

    path = input("Digite o caminho do arquivo: ").strip()

    if not path:
        print(f"\n{YELLOW}[!] Caminho não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    path = os.path.expanduser(path)

    if not os.path.isfile(path):
        print(
            f"\n{RED}"
            "[!] O caminho informado não é um arquivo válido."
            f"{RESET}"
        )
        input("\nPressione ENTER para voltar...")
        return

    show_file_info(path)


def calculate_hash():
    file_banner()

    print("SHA-256")
    print()

    path = input("Digite o caminho do arquivo: ").strip()

    if not path:
        print(f"\n{YELLOW}[!] Caminho não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    path = os.path.expanduser(path)

    if not os.path.isfile(path):
        print(f"\n{RED}[!] Arquivo não encontrado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    print()
    print("[+] Calculando SHA-256...")

    sha256 = calculate_sha256(path)

    if sha256:
        print()
        print(f"{GREEN}[✓] SHA-256 calculado.{RESET}")
        print()
        print(sha256)

    else:
        print(f"{RED}[!] Não foi possível calcular o hash.{RESET}")

    input("\nPressione ENTER para voltar...")


def file_info_menu():
    file_banner()

    print("INFORMAÇÕES DO ARQUIVO")
    print()

    path = input("Digite o caminho do arquivo: ").strip()

    if not path:
        print(f"\n{YELLOW}[!] Caminho não informado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    path = os.path.expanduser(path)

    if not os.path.isfile(path):
        print(f"\n{RED}[!] Arquivo não encontrado.{RESET}")
        input("\nPressione ENTER para voltar...")
        return

    try:
        stat = os.stat(path)

        print()
        print(f"{GREEN}[✓] Arquivo encontrado.{RESET}")
        print()
        print(f"Nome:       {os.path.basename(path)}")
        print(f"Tamanho:    {format_size(stat.st_size)}")
        print(f"Caminho:    {os.path.abspath(path)}")
        print(f"Permissões: {oct(stat.st_mode & 0o777)}")

    except PermissionError:
        print(f"\n{RED}[!] Permissão negada.{RESET}")

    input("\nPressione ENTER para voltar...")


def open_file_analyzer():

    while True:

        file_banner()

        print(f"{WHITE}FILE ANALYZER{RESET}")
        print(f"{RED}{'─' * 40}{RESET}")
        print()

        print(f"{WHITE}TOOLS{RESET}")
        print()

        print(f"{RED}├─{RESET} {WHITE}[1] ANALISAR ARQUIVO{RESET}")
        print(f"{RED}├─{RESET} {WHITE}[2] SHA-256{RESET}")
        print(f"{RED}└─{RESET} {WHITE}[3] INFORMAÇÕES DO ARQUIVO{RESET}")

        print()
        print(f"{RED}{'─' * 40}{RESET}")
        print()
        print(f"{RED}[1-3] SELECT     [0] BACK{RESET}")
        print()

        choice = input("Escolha: ").strip()

        if choice == "1":

            analyze_file()

        elif choice == "2":

            calculate_hash()

        elif choice == "3":

            file_info_menu()

        elif choice == "0":

            break

        else:

            print(
                f"\n{YELLOW}"
                "[!] Opção inválida."
                f"{RESET}"
            )

            input("\nPressione ENTER para continuar...")
