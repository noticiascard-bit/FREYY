PHISHING_RULES = {
    "name": "FREYY Phishing Awareness",
    "purpose": "Teste autorizado de conscientização contra phishing",

    "collect": {
        "page_opened": True,
        "button_clicked": True,
        "form_interaction": True,
        "form_submitted": True
    },

    "never_collect": {
        "password": True,
        "email": True,
        "token": True,
        "cookie": True,
        "ip_address": True,
        "typed_content": True
    },

    "authorization_required": True
}


def show_phishing_rules():
    print("PHISHING AWARENESS")
    print()
    print("Modo: teste autorizado de conscientização")
    print()
    print("[✓] Eventos de interação podem ser registrados.")
    print("[✓] Nenhuma credencial deve ser armazenada.")
    print("[✓] Nenhum conteúdo digitado deve ser armazenado.")
    print("[✓] Autorização prévia é obrigatória.")
