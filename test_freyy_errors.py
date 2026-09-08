import importlib
import pathlib
import tempfile


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


def test_security_invalid():
    section("1. CORE SECURITY — ENTRADAS INVÁLIDAS")

    try:
        security = importlib.import_module("core.security")
        normalize_target = security.normalize_target

        invalid_inputs = [
            "",
            "   ",
        ]

        for value in invalid_inputs:
            try:
                result = normalize_target(value)

                test(
                    f"Entrada inválida rejeitada: {value!r}",
                    result is None
                )

            except Exception as error:
                test(
                    f"Entrada inválida: {value!r}",
                    False,
                    f"{type(error).__name__}: {error}"
                )

    except Exception as error:
        test(
            "Core Security disponível",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_osint_invalid():
    section("2. OSINT — ENTRADAS INVÁLIDAS")

    try:
        osint = importlib.import_module("modules.osint")
        normalize_domain = osint.normalize_domain

        values = [
            "",
            "   ",
            "not a domain",
        ]

        for value in values:
            try:
                result = normalize_domain(value)

                test(
                    f"normalize_domain não quebrou: {value!r}",
                    result is None or isinstance(result, str)
                )

            except Exception as error:
                test(
                    f"normalize_domain: {value!r}",
                    False,
                    f"{type(error).__name__}: {error}"
                )

    except Exception as error:
        test(
            "OSINT disponível",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_file_analyzer_invalid():
    section("3. FILE ANALYZER — ARQUIVO INEXISTENTE")

    try:
        analyzer = importlib.import_module(
            "modules.file_analyzer"
        )

        calculate_hashes = getattr(
            analyzer,
            "calculate_hashes",
            None
        )

        fake_file = pathlib.Path(
            tempfile.gettempdir()
        ) / "freyy_file_that_does_not_exist.bin"

        fake_file.unlink(missing_ok=True)

        test(
            "calculate_hashes existe",
            callable(calculate_hashes)
        )

        if callable(calculate_hashes):
            try:
                result = calculate_hashes(fake_file)

                test(
                    "Arquivo inexistente tratado",
                    result is None,
                    "A função deveria retornar None para arquivo inexistente."
                )

            except Exception as error:
                test(
                    "Arquivo inexistente tratado sem exceção",
                    False,
                    f"{type(error).__name__}: {error}"
                )

    except Exception as error:
        test(
            "File Analyzer disponível",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_ip_invalid():
    section("4. IP — ENTRADAS INVÁLIDAS")

    import ipaddress

    values = [
        "",
        "999.999.999.999",
        "not-an-ip",
    ]

    for value in values:
        try:
            ipaddress.ip_address(value)

            test(
                f"IP inválido rejeitado: {value!r}",
                False
            )

        except ValueError:
            test(
                f"IP inválido rejeitado: {value!r}",
                True
            )

        except Exception as error:
            test(
                f"IP inválido: {value!r}",
                False,
                f"{type(error).__name__}: {error}"
            )


def test_web_invalid():
    section("5. WEB SECURITY — URL INVÁLIDA")

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

            values = [
                "",
                "   ",
            ]

            for value in values:
                try:
                    result = normalize_url(value)

                    test(
                        f"URL vazia tratada: {value!r}",
                        result is None
                        or isinstance(result, str)
                    )

                except Exception as error:
                    test(
                        f"URL inválida: {value!r}",
                        False,
                        f"{type(error).__name__}: {error}"
                    )

    except Exception as error:
        test(
            "Web Security disponível",
            False,
            f"{type(error).__name__}: {error}"
        )


def test_zip_invalid():
    section("6. ZIP — ARQUIVO NÃO-ZIP")

    try:
        import zipfile

        with tempfile.NamedTemporaryFile(
            suffix=".zip",
            delete=False
        ) as file:

            path = pathlib.Path(file.name)

            file.write(
                b"THIS IS NOT A ZIP FILE"
            )

        try:
            try:
                zipfile.ZipFile(path)

                test(
                    "Arquivo falso rejeitado como ZIP",
                    False
                )

            except zipfile.BadZipFile:
                test(
                    "Arquivo falso rejeitado corretamente",
                    True
                )

        finally:
            path.unlink(missing_ok=True)

    except Exception as error:
        test(
            "Teste de ZIP",
            False,
            f"{type(error).__name__}: {error}"
        )


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║             FREYY ERROR HANDLING TEST                     ║
╚════════════════════════════════════════════════════════════╝
""")

    test_security_invalid()
    test_osint_invalid()
    test_file_analyzer_invalid()
    test_ip_invalid()
    test_web_invalid()
    test_zip_invalid()

    section("RESULTADO FINAL")

    total = PASS + FAIL

    print(f"Testes executados: {total}")
    print(f"PASS: {PASS}")
    print(f"FAIL: {FAIL}")

    if FAIL == 0:
        print()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║          TESTE DE ERROS: TODOS PASSARAM                 ║")
        print("╚════════════════════════════════════════════════════════════╝")

        return 0

    print()
    print("[!] Existem comportamentos que precisam ser revisados.")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
