SERVICE_INFO = {
    "ssh": {
        "name": "SSH",
        "what_is": "Protocolo usado para acesso remoto a sistemas.",
        "meaning": "Existe um serviço SSH aceitando conexões nessa porta.",
    },

    "http": {
        "name": "HTTP",
        "what_is": "Protocolo utilizado por servidores web.",
        "meaning": "Existe um serviço web HTTP aceitando conexões.",
    },

    "https": {
        "name": "HTTPS",
        "what_is": "HTTP protegido por criptografia TLS.",
        "meaning": "Existe um serviço web HTTPS aceitando conexões.",
    },

    "ftp": {
        "name": "FTP",
        "what_is": "Protocolo utilizado para transferência de arquivos.",
        "meaning": "Existe um serviço FTP aceitando conexões.",
    },

    "smtp": {
        "name": "SMTP",
        "what_is": "Protocolo utilizado principalmente para envio de e-mails.",
        "meaning": "Existe um serviço SMTP aceitando conexões.",
    },

    "dns": {
        "name": "DNS",
        "what_is": "Sistema responsável por traduzir nomes de domínio em endereços IP.",
        "meaning": "Um serviço DNS foi detectado.",
    },

    "telnet": {
        "name": "Telnet",
        "what_is": "Protocolo antigo de acesso remoto.",
        "meaning": "Um serviço Telnet foi detectado.",
    },

    "mysql": {
        "name": "MySQL",
        "what_is": "Sistema de gerenciamento de banco de dados.",
        "meaning": "Um servidor MySQL foi detectado.",
    },

    "postgresql": {
        "name": "PostgreSQL",
        "what_is": "Sistema de gerenciamento de banco de dados relacional.",
        "meaning": "Um servidor PostgreSQL foi detectado.",
    },

    "rdp": {
        "name": "RDP",
        "what_is": "Protocolo utilizado para acesso remoto a sistemas.",
        "meaning": "Um serviço RDP foi detectado.",
    },
}


def get_service_info(service):
    return SERVICE_INFO.get(service.lower())
