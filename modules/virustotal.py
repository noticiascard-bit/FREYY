import hashlib
import os
import time

import requests


API_URL = "https://www.virustotal.com/api/v3"
KEY_FILE = os.path.expanduser("~/.freyy/virustotal_api_key")


def header(title="FREYY VIRUSTOTAL"):
    print()
    print("╔══════════════════════════════════════════╗")
    print(f"║ {title:^40} ║")
    print("╚══════════════════════════════════════════╝")
    print()


def pause():
    input("\nPressione ENTER para continuar...")


def load_api_key():
    if not os.path.isfile(KEY_FILE):
        return None

    try:
        with open(KEY_FILE, "r", encoding="utf-8") as f:
            key = f.read().strip()

        return key if key else None

    except OSError:
        return None


def calculate_sha256(path):
    sha256 = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def get_file_report(sha256, api_key):
    url = f"{API_URL}/files/{sha256}"

    headers = {
        "x-apikey": api_key
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

    except requests.RequestException as e:
        return None, f"Erro de conexão: {e}"

    if response.status_code == 200:
        try:
            return response.json(), None
        except ValueError:
            return None, "Resposta inválida do VirusTotal."

    if response.status_code == 404:
        return None, "Arquivo não encontrado no VirusTotal."

    if response.status_code == 401:
        return None, "API Key inválida ou não autorizada."

    if response.status_code == 429:
        return None, "Limite de requisições do VirusTotal atingido."

    try:
        data = response.json()

        message = (
            data.get("error", {})
            .get("message")
        )

        if message:
            return None, f"VirusTotal: {message}"

    except ValueError:
        pass

    return None, f"VirusTotal respondeu HTTP {response.status_code}."


def show_report(report):
    attributes = (
        report
        .get("data", {})
        .get("attributes", {})
    )

    stats = attributes.get(
        "last_analysis_stats",
        {}
    )

    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    undetected = stats.get("undetected", 0)
    harmless = stats.get("harmless", 0)

    total = (
        malicious
        + suspicious
        + undetected
        + harmless
    )

    print("RESULTADO VIRUSTOTAL")
    print("──────────────────────────────────────────")

    print(f"[!] Malicious : {malicious}")
    print(f"[!] Suspicious: {suspicious}")
    print(f"[✓] Undetected: {undetected}")
    print(f"[✓] Harmless  : {harmless}")

    if total:
        print(f"\nTotal de mecanismos: {total}")

    print()
    print("VEREDITO")
    print("──────────────────────────────────────────")

    if malicious >= 3:
        print("🔴 MÚLTIPLAS DETECÇÕES")
        print()
        print(
            "Vários mecanismos classificaram "
            "o arquivo como malicioso."
        )

    elif malicious > 0:
        print("🟡 DETECÇÃO ENCONTRADA")
        print()
        print(
            "Pelo menos um mecanismo detectou "
            "algo suspeito/malicioso."
        )

    elif suspicious > 0:
        print("🟡 SUSPEITO")
        print()
        print(
            "Existem classificações suspeitas, "
            "mas não há múltiplas detecções maliciosas."
        )

    else:
        print("🟢 SEM DETECÇÕES")
        print()
        print(
            "Nenhum mecanismo disponível "
            "classificou o arquivo como malicioso."
        )

    print()
    print("⚠️ IMPORTANTE:")
    print(
        "Ausência de detecções NÃO significa "
        "que o APK seja 100% seguro."
    )


def consult_hash(sha256):
    header("CONSULTA POR SHA-256")

    api_key = load_api_key()

    if not api_key:
        print("[!] API Key do VirusTotal não encontrada.")
        print()
        print("Arquivo esperado:")
        print(KEY_FILE)
        return

    print(f"SHA-256:")
    print(sha256)
    print()
    print("Consultando VirusTotal...")

    report, error = get_file_report(
        sha256,
        api_key
    )

    if report:
        print()
        show_report(report)
        return

    print()
    print(f"[!] {error}")

    if "não encontrado" in error.lower():
        print()
        print(
            "Esse arquivo ainda não possui "
            "um relatório disponível."
        )
        print()
        print(
            "Você poderá usar a opção de "
            "enviar o APK para análise."
        )


def upload_file(path, api_key):
    url = f"{API_URL}/files"

    headers = {
        "x-apikey": api_key
    }

    try:
        with open(path, "rb") as f:
            response = requests.post(
                url,
                headers=headers,
                files={
                    "file": (
                        os.path.basename(path),
                        f,
                        "application/vnd.android.package-archive"
                    )
                },
                timeout=120
            )

    except requests.RequestException as e:
        return None, f"Erro de conexão: {e}"

    except OSError as e:
        return None, f"Erro ao abrir arquivo: {e}"

    if response.status_code in (200, 201):
        try:
            return response.json(), None
        except ValueError:
            return None, "Resposta inválida do VirusTotal."

    if response.status_code == 401:
        return None, "API Key inválida ou não autorizada."

    if response.status_code == 429:
        return None, "Limite de requisições do VirusTotal atingido."

    try:
        data = response.json()

        message = (
            data.get("error", {})
            .get("message")
        )

        if message:
            return None, f"VirusTotal: {message}"

    except ValueError:
        pass

    return None, f"VirusTotal respondeu HTTP {response.status_code}."


def get_analysis(analysis_id, api_key):
    url = f"{API_URL}/analyses/{analysis_id}"

    headers = {
        "x-apikey": api_key
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=30
        )

    except requests.RequestException as e:
        return None, str(e)

    if response.status_code != 200:
        return None, f"HTTP {response.status_code}"

    try:
        return response.json(), None
    except ValueError:
        return None, "Resposta inválida."


def wait_analysis(analysis_id, api_key):
    print()
    print("Aguardando análise do VirusTotal...")

    for _ in range(12):
        data, error = get_analysis(
            analysis_id,
            api_key
        )

        if error:
            return None, error

        status = (
            data
            .get("data", {})
            .get("attributes", {})
            .get("status")
        )

        if status == "completed":
            return data, None

        print(".", end="", flush=True)

        time.sleep(5)

    print()

    return None, (
        "A análise ainda está processando. "
        "Consulte novamente depois."
    )


def upload_and_analyze(path):
    header("ENVIAR APK")

    api_key = load_api_key()

    if not api_key:
        print("[!] API Key do VirusTotal não encontrada.")
        print()
        print(KEY_FILE)
        return

    if not os.path.isfile(path):
        print("[!] Arquivo não encontrado.")
        return

    if not path.lower().endswith(".apk"):
        print("[!] O arquivo não parece ser um APK.")
        return

    size = os.path.getsize(path)

    print(f"Arquivo: {os.path.basename(path)}")
    print(f"Tamanho: {size / 1024 / 1024:.2f} MB")
    print()

    print("⚠️ ATENÇÃO")
    print(
        "Esta opção envia o APK ao VirusTotal "
        "para análise."
    )
    print()
    print(
        "Não envie arquivos privados ou "
        "sensíveis sem verificar as condições "
        "de compartilhamento do serviço."
    )

    confirm = input("\nEnviar mesmo assim? [s/N]: ").strip().lower()

    if confirm != "s":
        print("\nOperação cancelada.")
        return

    print()
    print("Enviando APK...")

    result, error = upload_file(
        path,
        api_key
    )

    if error:
        print()
        print(f"[!] {error}")
        return

    analysis_id = (
        result
        .get("data", {})
        .get("id")
    )

    if not analysis_id:
        print()
        print("[!] ID da análise não encontrado.")
        return

    print()
    print("Análise enviada.")
    print(f"ID: {analysis_id}")

    analysis, error = wait_analysis(
        analysis_id,
        api_key
    )

    if error:
        print()
        print(f"[!] {error}")
        return

    print()
    print("✓ Análise concluída.")

    sha256 = calculate_sha256(path)

    print()
    print("Consultando relatório final...")

    report, error = get_file_report(
        sha256,
        api_key
    )

    if error:
        print()
        print(f"[!] {error}")
        return

    print()
    show_report(report)


def virustotal_menu(apk_path=None):
    while True:
        header()

        print("[1] Consultar pelo SHA-256")
        print("[2] Enviar APK para análise")
        print("[0] Voltar")

        option = input("\nFREYY VT > ").strip()

        if option == "1":
            if apk_path and os.path.isfile(apk_path):
                sha256 = calculate_sha256(apk_path)
            else:
                sha256 = input("\nSHA-256: ").strip()

            if not sha256:
                print("[!] SHA-256 vazio.")
            else:
                consult_hash(sha256)

            pause()

        elif option == "2":
            path = apk_path

            if not path:
                path = input("\nCaminho do APK: ").strip()

            upload_and_analyze(path)

            pause()

        elif option == "0":
            break

        else:
            print("[!] Opção inválida.")
            time.sleep(1)


if __name__ == "__main__":
    virustotal_menu()
