def explain_state(state):
    explanations = {
        "open": "Existe um serviço aceitando conexões nessa porta.",
        "closed": "A porta respondeu, mas não há um serviço aceitando conexões.",
        "filtered": "O Nmap não conseguiu determinar o estado porque algum mecanismo de filtragem pode estar bloqueando a resposta.",
    }

    return explanations.get(
        state.lower(),
        "Estado não reconhecido pelo FREYY."
    )


def parse_nmap(output):
    results = []

    for line in output.splitlines():
        parts = line.split()

        if len(parts) < 3:
            continue

        if "/" not in parts[0]:
            continue

        port = parts[0]
        state = parts[1]
        service = parts[2]

        version = "Não identificada"

        if len(parts) > 3:
            version = " ".join(parts[3:])

        results.append({
            "port": port,
            "state": state,
            "state_explanation": explain_state(state),
            "service": service,
            "version": version
        })

    return results
