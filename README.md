FREYY

Security Toolkit for Termux & Linux

FREYY é um toolkit de segurança desenvolvido em Python para Termux e Linux, reunindo diferentes módulos de análise em uma interface de terminal única e organizada.

O projeto é desenvolvido principalmente para Termux, mas também pode funcionar em ambientes Linux com os requisitos necessários.

O projeto foi desenvolvido com foco em aprendizado, análise e testes autorizados em ambientes próprios ou com permissão.

---

Features

Module| Description
OSINT| Ferramentas de coleta e análise de informações
Network| Análise e diagnóstico de rede
Web Security| Recursos para análise de segurança web
Vulnerability| Análise de possíveis vulnerabilidades
Net Monitor| Monitoramento de informações de rede
File Analyzer| Análise de arquivos
APK Analyzer| Análise de aplicações Android
Chat AI| Integração com Gemini

---

Requirements

- Android + Termux ou Linux
- Python 3
- Git
- Nmap

---

Installation

Clone o repositório e instale os requisitos:

git clone https://github.com/noticiascard-bit/FREYY.git
cd FREYY

# Termux
pkg update
pkg install python git nmap

# Linux Debian/Ubuntu
sudo apt update
sudo apt install python3 python3-pip git nmap

Depois execute:

# Termux
python freyy.py

# Linux
python3 freyy.py

«No Termux, execute os comandos da seção "Termux".
No Linux, execute os comandos da seção "Linux Debian/Ubuntu".»

---

Chat AI

O módulo Chat AI utiliza a API do Gemini.

Para manter sua chave protegida, nunca coloque uma API key diretamente no código ou publique uma chave no GitHub.

Configure a variável de ambiente:

export GEMINI_API_KEY="SUA_CHAVE_AQUI"

Ou utilize o método de configuração de chave suportado pelo FREYY.

---

Project Structure

FREYY/
├── core/
│   ├── security.py
│   └── ui.py
│
├── modules/
│   ├── apk_analyzer.py
│   ├── apk_indicators.py
│   ├── apk_manifest.py
│   ├── chat_freyy.py
│   ├── file_analyzer.py
│   ├── network.py
│   ├── osint.py
│   ├── phishing.py
│   ├── virustotal.py
│   ├── vulnerability.py
│   └── web_security.py
│
├── utils/
├── freyy.py
├── test_freyy.py
├── test_freyy_errors.py
├── test_modules.py
└── README.md

---

Testing

O projeto possui testes automatizados para diferentes partes do toolkit.

python test_freyy.py

python test_freyy_errors.py

python test_modules.py

---

Responsible Use

FREYY deve ser utilizado somente em sistemas, redes, aplicações e arquivos que você possui ou para os quais possui autorização para realizar testes.

O projeto tem finalidade educacional e de análise de segurança.

O usuário é responsável pela utilização da ferramenta.

---

Project Status

Development

O FREYY está em desenvolvimento. Novos recursos, melhorias e correções poderão ser adicionados ao longo do tempo.

---

License

Este projeto atualmente não possui uma licença open-source definida.

Uma licença poderá ser adicionada futuramente.

---

Author

noticiascard-bit

GitHub:

https://github.com/noticiascard-bit/FREYY