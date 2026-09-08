FREYY

Security Toolkit for Termux & Linux

FREYY é um toolkit de segurança desenvolvido para Termux e Linux, reunindo ferramentas de análise, diagnóstico de rede, segurança web, vulnerabilidades, monitoramento e análise de arquivos em uma única interface de terminal.

Features

Module| Description
OSINT| Coleta e análise de informações públicas
NETWORK| Diagnóstico e análise de rede
WEB SECURITY| Análise básica de segurança web
VULNERABILITY| Verificações relacionadas a vulnerabilidades
NET MONITOR| Monitoramento de conexões e rede
FILE ANALYZER| Análise de arquivos
FREYY TOOLS| Ferramentas adicionais, incluindo análise de APK
CHAT AI| Assistente de IA integrado

Requirements

- Termux ou Debian/Ubuntu-based Linux
- Python 3
- Git
- Conexão com a internet durante a instalação

O instalador configura automaticamente as principais dependências do projeto.

Installation

Termux

git clone https://github.com/noticiascard-bit/FREYY.git
cd FREYY
./install.sh

Depois da instalação:

FREYY

Debian / Ubuntu

git clone https://github.com/noticiascard-bit/FREYY.git
cd FREYY
./install.sh

Depois:

FREYY

Usage

Após a instalação, execute:

FREYY

O menu principal permite acessar os módulos disponíveis.

Chat AI

O FREYY possui um módulo de Chat AI integrado.

Para utilizar esse recurso, é necessário configurar uma chave de API do Google Gemini.

A chave pode ser fornecida através da variável de ambiente:

export GEMINI_API_KEY="SUA_CHAVE"

Ou através do arquivo:

~/.freyy/gemini_api_key

Nunca publique sua chave de API no GitHub.

Project Structure

FREYY/
├── core/
├── modules/
├── utils/
├── freyy.py
├── install.sh
├── requirements.txt
└── README.md

Testing

O projeto possui testes para verificar partes importantes do toolkit.

Para executar os testes disponíveis:

python test_freyy.py

Security & Responsible Use

O FREYY foi desenvolvido para fins educacionais, pesquisa e administração de sistemas.

Utilize as ferramentas somente em sistemas, redes, aplicações e arquivos para os quais você possui autorização.

Não utilize o projeto para acessar, interferir ou analisar sistemas de terceiros sem permissão.

Project Status

FREYY está em desenvolvimento ativo.

Novos módulos, melhorias na interface e correções podem ser adicionados ao projeto ao longo do tempo.

License

Este projeto ainda não possui uma licença open-source definida.

Author

noticiascard-bit

GitHub:
https://github.com/noticiascard-bit