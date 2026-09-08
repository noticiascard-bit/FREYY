import importlib
import os
import py_compile


MODULES = {
    "OSINT": ("modules.osint", "open_osint"),
    "NETWORK": ("modules.network", "open_network"),
    "WEB SECURITY": ("modules.web_security", "open_web_security"),
    "VULNERABILITY": ("modules.vulnerability", "open_vulnerability"),
    "FILE ANALYZER": ("modules.file_analyzer", "open_file_analyzer"),
    "APK ANALYZER": ("modules.apk_analyzer", "open_apk_analyzer"),
    "APK INDICATORS": ("modules.apk_indicators", None),
    "APK MANIFEST": ("modules.apk_manifest", None),
    "CHAT FREYY": ("modules.chat_freyy", "open_chat_freyy"),
    "VIRUSTOTAL": ("modules.virustotal", "virustotal_menu"),
    "PHISHING": ("modules.phishing", "show_phishing_rules"),
}


def check_module(name, module_name, entry_point):
    try:
        module = importlib.import_module(module_name)

        if entry_point is None:
            return True, "import OK"

        function = getattr(module, entry_point, None)

        if function is None:
            return False, f"função ausente: {entry_point}"

        if not callable(function):
            return False, f"{entry_point} não é chamável"

        return True, f"{entry_point} OK"

    except Exception as error:
        return False, f"{type(error).__name__}: {error}"


def main():
    print()
    print("=" * 56)
    print("              FREYY MODULE TESTER")
    print("=" * 56)
    print()

    total = 0
    passed = 0
    failed = 0

    for name, (module_name, entry_point) in MODULES.items():
        total += 1
        ok, message = check_module(name, module_name, entry_point)

        if ok:
            passed += 1
            print(f"[✓] {name:<18} {message}")
        else:
            failed += 1
            print(f"[✗] {name:<18} {message}")

    print()
    print("-" * 56)
    print(f"Módulos testados : {total}")
    print(f"OK               : {passed}")
    print(f"Erros            : {failed}")
    print("-" * 56)

    print()
    print("Verificando sintaxe do projeto...")

    syntax_errors = 0

    files = [
        "freyy.py",
        "core/ui.py",
    ]

    files += [
        os.path.join("modules", filename)
        for filename in os.listdir("modules")
        if filename.endswith(".py")
    ]

    for filename in sorted(set(files)):
        try:
            py_compile.compile(filename, doraise=True)
        except Exception as error:
            syntax_errors += 1
            print(f"[✗] Sintaxe: {filename}")
            print(f"    {error}")

    if syntax_errors == 0:
        print("[✓] Sintaxe: todos os arquivos OK")

    print()
    print("=" * 56)

    if failed == 0 and syntax_errors == 0:
        print("              RESULTADO: TUDO OK")
    else:
        print("              RESULTADO: ATENÇÃO")
        print("              Existem problemas para corrigir.")

    print("=" * 56)
    print()


if __name__ == "__main__":
    main()
