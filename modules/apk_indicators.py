import re


def clean_context(context):
    """
    Remove caracteres ilegíveis de dados binários
    e deixa o contexto mais fácil de ler.
    """

    context = context.replace("\n", " ")
    context = context.replace("\r", " ")
    context = context.replace("\t", " ")

    # Mantém caracteres imprimíveis básicos
    context = "".join(
        char if char.isprintable() else " "
        for char in context
    )

    # Remove espaços repetidos
    context = re.sub(r"\s+", " ", context)

    return context.strip()


def find_context(text, signature, radius=80):
    """
    Procura a assinatura e retorna um pequeno trecho
    ao redor dela.
    """

    text_lower = text.lower()
    signature_lower = signature.lower()

    position = text_lower.find(signature_lower)

    if position == -1:
        return None

    start = max(0, position - radius)
    end = min(
        len(text),
        position + len(signature) + radius
    )

    context = text[start:end]

    return clean_context(context)


def detect_occurrence_type(filename):
    """
    Estima o tipo de arquivo onde o indicador apareceu.
    """

    filename_lower = filename.lower()

    if filename_lower.endswith(".dex"):
        return "DEX / Código"

    if filename_lower.endswith(".arsc"):
        return "RESOURCE / Recursos"

    if filename_lower.endswith(".xml"):
        return "XML / Configuração"

    if filename_lower.endswith(".so"):
        return "NATIVE / Biblioteca"

    if filename_lower.endswith(".json"):
        return "JSON / Dados"

    if filename_lower.endswith(".txt"):
        return "TEXT / Texto"

    return "ARQUIVO"


def find_indicators(data, filename=""):
    """
    Analisa dados estáticos do APK.

    Nenhum arquivo é executado.
    """

    text = data.decode(
        "utf-8",
        errors="ignore"
    )

    text_lower = text.lower()

    indicators = []

    patterns = [
        (
            "Execução de comandos",
            [
                "runtime.exec",
                "processbuilder"
            ],
            "Pode iniciar processos. O contexto é importante.",
            "MODERADA"
        ),
        (
            "Acesso a shell",
            [
                "/system/bin/sh",
                "/bin/sh"
            ],
            "Referência a um shell do sistema. Pode ser legítima.",
            "BAIXA"
        ),
        (
            "Execução dinâmica",
            [
                "dexclassloader",
                "pathclassloader"
            ],
            "Pode carregar código dinamicamente e merece investigação.",
            "MODERADA"
        ),
        (
            "Carregamento de código nativo",
            [
                "system.loadlibrary",
                "system.load("
            ],
            "Carrega bibliotecas nativas. É comum em vários aplicativos.",
            "BAIXA"
        ),
        (
            "Acesso a identificadores",
            [
                "getdeviceid",
                "getsubscriberid",
                "getsimserialnumber"
            ],
            "Pode acessar identificadores do dispositivo ou SIM.",
            "BAIXA"
        ),
        (
            "Acesso à localização",
            [
                "locationmanager",
                "fusedlocationproviderclient"
            ],
            "API relacionada à localização. Pode ser legítima.",
            "BAIXA"
        ),
        (
            "Acesso a SMS",
            [
                "readsms",
                "receivesms",
                "sendsms"
            ],
            "Referência a funcionalidades relacionadas a SMS.",
            "MODERADA"
        ),
        (
            "Acesso a contatos",
            [
                "contactscontract"
            ],
            "Referência à agenda de contatos.",
            "BAIXA"
        ),
    ]

    for name, signatures, description, confidence in patterns:

        found = []

        for signature in signatures:

            if signature in text_lower:

                context = find_context(
                    text,
                    signature
                )

                occurrence_type = detect_occurrence_type(
                    filename
                )

                found.append(
                    (
                        signature,
                        context,
                        occurrence_type
                    )
                )

        if found:

            indicators.append(
                (
                    name,
                    description,
                    found,
                    confidence,
                    filename
                )
            )

    return indicators


def show_indicators(indicators):

    print("\nINDICADORES ESTÁTICOS")
    print("──────────────────────────────────────────")

    if not indicators:

        print(
            "[✓] Nenhum indicador conhecido encontrado."
        )

        return

    print(
        f"[!] Categorias encontradas: "
        f"{len(indicators)}"
    )

    for item in indicators:

        name, description, signatures, confidence, filename = item

        print(f"\n[!] {name}")
        print(f"    Confiança: {confidence}")
        print(f"    {description}")

        if filename:
            print(
                f"    Arquivo: {filename}"
            )

        for signature, context, occurrence_type in signatures:

            print(
                f"    Assinatura: {signature}"
            )

            print(
                f"    Tipo: {occurrence_type}"
            )

            if context:

                if len(context) > 180:
                    context = context[:180] + "..."

                print(
                    f"    Contexto: ...{context}..."
                )

    print("\n⚠️ IMPORTANTE")
    print(
        "Os indicadores não confirmam malware."
    )
    print(
        "A confiança representa apenas a força do sinal."
    )
    print(
        "O tipo indica onde a ocorrência foi encontrada."
    )
    print(
        "O contexto serve apenas como auxílio à investigação."
    )
    print(
        "A análise é exclusivamente estática."
    )
