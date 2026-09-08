import hashlib
import os
import re
import zipfile
from modules.apk_manifest import parse_manifest, show_manifest
from modules.apk_indicators import find_indicators, show_indicators
from modules.virustotal import consult_hash, upload_and_analyze


def calculate_sha256(path):
    sha256 = hashlib.sha256()

    with open(path, "rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(block)

    return sha256.hexdigest()


def format_size(size):
    units = ["B", "KB", "MB", "GB"]
    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024

    return f"{value:.2f} TB"


def find_urls(data):
    pattern = rb"https?://[A-Za-z0-9.-]+(?:/[A-Za-z0-9._~:/?#\[\]@!$&\x27()*+,;=%-]*)?"
    matches = re.findall(pattern, data)

    urls = set()

    for match in matches:
        try:
            url = match.decode("utf-8", errors="ignore").strip()

            if len(url) > 500:
                continue

            parsed = re.match(
                r"^https?://([A-Za-z0-9-]+\.)+[A-Za-z]{2,63}(?::\d+)?(?:/[^\s]*)?$",
                url,
                re.IGNORECASE
            )

            if not parsed:
                continue

            host = (
                url.split("//", 1)[1]
                .split("/", 1)[0]
                .split(":", 1)[0]
                .lower()
            )

            if host in {"schemas.android.com"}:
                continue

            urls.add(url)

        except Exception:
            pass

    return sorted(urls)


def analyze_apk(path):
    print("\n╔══════════════════════════════════════════╗")
    print("║           APK SECURITY ANALYZER          ║")
    print("╚══════════════════════════════════════════╝")

    if not os.path.isfile(path):
        print("\n[!] Arquivo não encontrado.")
        return

    if not path.lower().endswith(".apk"):
        print("\n[!] O arquivo não possui extensão .apk.")
        return

    print("\n[+] Arquivo:", os.path.basename(path))
    print("[+] Caminho:", os.path.abspath(path))

    size = os.path.getsize(path)

    print("[+] Tamanho:", format_size(size))

    print("\n[*] Calculando SHA-256...")
    sha256 = calculate_sha256(path)
    print("[+] SHA-256:", sha256)

    print("\n[*] Verificando estrutura do APK...")

    if not zipfile.is_zipfile(path):
        print("[!] O arquivo não parece ser um APK válido.")
        return

    print("[+] Estrutura ZIP válida.")

    try:
        with zipfile.ZipFile(path, "r") as apk:
            files = apk.namelist()

            print("[+] Arquivos internos:", len(files))

            manifest = "AndroidManifest.xml" in files

            dex_files = [
                name
                for name in files
                if name.startswith("classes") and name.endswith(".dex")
            ]

            native_libs = [
                name
                for name in files
                if name.endswith(".so")
            ]

            print("\nESTRUTURA")
            print("──────────────────────────────────────────")

            print(
                "[{}] AndroidManifest.xml".format(
                    "✓" if manifest else "!"
                )
            )

            print(
                "[{}] Arquivos DEX: {}".format(
                    "✓" if dex_files else "!",
                    len(dex_files)
                )
            )

            print(
                "[{}] Bibliotecas nativas (.so): {}".format(
                    "✓" if native_libs else "!",
                    len(native_libs)
                )
            )
            if manifest:
                print("\n[*] Analisando AndroidManifest.xml...")

                try:
                    manifest_data = apk.read(
                        "AndroidManifest.xml"
                    )

                    manifest_info = parse_manifest(
                        manifest_data
                    )

                    show_manifest(
                        manifest_info
                    )

                except Exception as error:
                    print(
                        "\n[!] Falha ao analisar o Manifest:",
                        error
                    )
            print("\n[*] Procurando URLs e indicadores...")

            urls = set()
            all_indicators = []

            for name in files:
                try:
                    info = apk.getinfo(name)

                    if info.file_size > 10 * 1024 * 1024:
                        continue

                    data = apk.read(name)

                    urls.update(find_urls(data))

                    indicators = find_indicators(data, name)

                    all_indicators.extend(indicators)

                except Exception:
                    continue

            if urls:
                print(f"[!] URLs encontradas: {len(urls)}")

                for url in sorted(urls)[:30]:
                    print("    ", url)

                if len(urls) > 30:
                    print(
                        f"    ... e mais {len(urls) - 30}"
                    )

            else:
                print("[✓] Nenhuma URL encontrada.")

            show_indicators(all_indicators)

            print("\nRESUMO")
            print("──────────────────────────────────────────")
            print("[✓] APK analisado sem execução.")
            print("[✓] Indicadores estáticos processados.")

            if all_indicators:
                print(
                    f"[!] Ocorrências de indicadores: "
                    f"{len(all_indicators)}"
                )
            else:
                print("[✓] Nenhum indicador conhecido encontrado.")

            print(
                "[!] Indicadores encontrados não significam malware."
            )
            print("[!] Esta é uma análise estática.")
            print("\nVIRUSTOTAL")
            print("──────────────────────────────────────────")
            print("[1] Consultar SHA-256")
            print("[2] Enviar APK para análise")
            print("[0] Continuar")

            vt_choice = input("\nVirusTotal > ").strip()

            if vt_choice == "1":
                consult_hash(sha256)
                input("\nPressione ENTER para continuar...")

            elif vt_choice == "2":
                upload_and_analyze(path)
                input("\nPressione ENTER para continuar...")

    except zipfile.BadZipFile:
        print("\n[!] Falha ao abrir o APK como ZIP.")

    except Exception as error:
        print("\n[!] Erro durante a análise:", error)


def open_apk_analyzer():

    while True:

        print()
        print("\033[1;31m")
        print("   ___  ____  _  __")
        print("  / _ \\/ __ \\/ |/ /")
        print(" / , _/ /_/ /    /")
        print("/_/|_|\\____/_/|_/")
        print("\033[0m")

        print("\033[1;37mFREYY / APK ANALYZER\033[0m")
        print("\033[1;31m────────────────────────────────────────\033[0m")
        print()

        print("\033[1;37mTOOLS\033[0m")
        print()

        print("\033[1;31m├─\033[0m \033[1;37m[1] ANALISAR APK\033[0m")
        print("\033[1;31m└─\033[0m \033[1;37m[0] BACK\033[0m")

        print()
        print("\033[1;31m────────────────────────────────────────\033[0m")
        print()
        print("\033[1;31m[1] SELECT     [0] BACK\033[0m")
        print()

        choice = input("Escolha: ").strip()

        if choice == "0":

            return

        elif choice == "1":

            path = input(
                "\nCaminho do APK: "
            ).strip()

            analyze_apk(path)

            input(
                "\nPressione ENTER para continuar..."
            )

        else:

            print(
                "\n\033[1;33m[!] Opção inválida.\033[0m"
            )
