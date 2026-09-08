import hashlib
import importlib
import ipaddress
import pathlib
import tempfile
import zipfile


ROOT = pathlib.Path(__file__).resolve().parent


PASS = 0
FAIL = 0


def test(name, condition, detail=""):
    global PASS, FAIL

    if condition:
        print(f"[✓] {name}")
        PASS += 1
    else:
        print(f"[✗] {name}")
        if detail:
            print(f"    {detail}")
        FAIL += 1


def section(name):
    print()
    print("=" * 60)
    print(name)
    print("=" * 60)


def test_security():
    section("1. CORE SECURITY")

    try:
        security = importlib.import_module("core.security")

        normalize_target = getattr(
            security,
            "normalize_target",
            None
        )

        test(
            "normalize_target existe",
            callable(normalize_target)
        )

        if callable(normalize_target):
            result = normalize_target("example.com")

            test(
                "Domínio normalizado",
                isinstance(result, str)
                and result.startswith("https://")
            )

            empty = normalize_target("")

            test(
                "Entrada vazia rejeitada",
                empty is None
            )

    except Exception as error:
        test(
            "Core Security executado",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_osint():
    section("2. OSINT")

    try:
        osint = importlib.import_module("modules.osint")

        normalize_domain = getattr(
            osint,
            "normalize_domain",
            None
        )

        resolve_records = getattr(
            osint,
            "resolve_records",
            None
        )

        test(
            "normalize_domain existe",
            callable(normalize_domain)
        )

        test(
            "resolve_records existe",
            callable(resolve_records)
        )

        if callable(normalize_domain):
            result = normalize_domain("https://example.com/path")

            test(
                "Normalização de domínio",
                result == "example.com"
            )

    except Exception as error:
        test(
            "OSINT executado",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_file_analyzer():
    section("3. FILE ANALYZER")

    try:
        analyzer = importlib.import_module(
            "modules.file_analyzer"
        )

        calculate_hashes = getattr(
            analyzer,
            "calculate_hashes",
            None
        )

        identify_magic = getattr(
            analyzer,
            "identify_magic",
            None
        )

        test(
            "calculate_hashes existe",
            callable(calculate_hashes)
        )

        test(
            "identify_magic existe",
            callable(identify_magic)
        )

        with tempfile.NamedTemporaryFile(
            mode="wb",
            delete=False
        ) as file:

            path = pathlib.Path(file.name)
            data = b"FREYY functional test"

            file.write(data)

        try:
            if callable(calculate_hashes):
                hashes = calculate_hashes(path)

                expected = hashlib.sha256(data).hexdigest()

                test(
                    "SHA-256 calculado corretamente",
                    isinstance(hashes, dict)
                    and hashes.get("SHA-256") == expected
                )

        finally:
            path.unlink(missing_ok=True)

    except Exception as error:
        test(
            "File Analyzer executado",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_apk_modules():
    section("4. APK ANALYZER")

    modules = [
        "modules.apk_analyzer",
        "modules.apk_indicators",
        "modules.apk_manifest",
    ]

    for module_name in modules:
        try:
            importlib.import_module(module_name)

            test(
                f"{module_name} importado",
                True
            )

        except Exception as error:
            test(
                f"{module_name} importado",
                False,
                f"{type(error).__name__}: {error}"
            )


def test_network_utils():
    section("5. NETWORK / UTILS")

    try:
        ip = ipaddress.ip_address("8.8.8.8")

        test(
            "IPv4 válido reconhecido",
            ip.version == 4
        )

        test(
            "IP público reconhecido",
            ip.is_global
        )

    except Exception as error:
        test(
            "Teste de IP",
            False,
            f"{type(error).__name__}: {error}"
        )

    for module_name in [
        "utils.nmap_parser",
        "utils.service_info",
        "utils.vulnerability_info",
    ]:

        try:
            importlib.import_module(module_name)

            test(
                f"{module_name} importado",
                True
            )

        except Exception as error:
            test(
                f"{module_name} importado",
                False,
                f"{type(error).__name__}: {error}"
            )


def test_vulnerability():
    section("6. VULNERABILITY")

    try:
        vulnerability = importlib.import_module(
            "modules.vulnerability"
        )

        request_target = getattr(
            vulnerability,
            "request_target",
            None
        )

        print_finding = getattr(
            vulnerability,
            "print_finding",
            None
        )

        test(
            "request_target existe",
            callable(request_target)
        )

        test(
            "print_finding existe",
            callable(print_finding)
        )

    except Exception as error:
        test(
            "Vulnerability executado",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_web_security():
    section("7. WEB SECURITY")

    try:
        web = importlib.import_module(
            "modules.web_security"
        )

        normalize_url = getattr(
            web,
            "normalize_url",
            None
        )

        test(
            "normalize_url existe",
            callable(normalize_url)
        )

        if callable(normalize_url):
            result = normalize_url("example.com")

            test(
                "URL normalizada",
                isinstance(result, str)
                and result.startswith("https://")
            )

    except Exception as error:
        test(
            "Web Security executado",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_zip_structure():
    section("8. ARQUIVO ZIP DE TESTE")

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".zip",
            delete=False
        ) as file:

            path = pathlib.Path(file.name)

        with zipfile.ZipFile(
            path,
            "w"
        ) as archive:

            archive.writestr(
                "freyy_test.txt",
                "FREYY TEST"
            )

        with zipfile.ZipFile(path, "r") as archive:

            names = archive.namelist()

        test(
            "ZIP criado corretamente",
            "freyy_test.txt" in names
        )

        path.unlink(missing_ok=True)

    except Exception as error:
        test(
            "Teste ZIP",
            False,
            f"{type(error).__name__}: {error}"
        )


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║              FREYY FUNCTIONAL TEST                       ║
╚════════════════════════════════════════════════════════════╝
""")

    test_security()
    test_osint()
    test_file_analyzer()
    test_apk_modules()
    test_network_utils()
    test_vulnerability()
    test_web_security()
    test_zip_structure()

    section("RESULTADO")

    total = PASS + FAIL

    print(f"Testes executados: {total}")
    print(f"PASS: {PASS}")
    print(f"FAIL: {FAIL}")

    if FAIL == 0:
        print()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║             TODOS OS TESTES PASSARAM                     ║")
        print("╚════════════════════════════════════════════════════════════╝")
        return 0

    print()
    print("[!] Existem testes que precisam de revisão.")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
