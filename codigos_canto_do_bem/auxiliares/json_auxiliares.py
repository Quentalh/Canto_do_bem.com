import json
import os

# Caminho absoluto para o arquivo JSON, sempre baseado na raiz do projeto
CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_ARQUIVO = os.path.join(CAMINHO_RAIZ, "base_de_dados", "dados.json")


def carregar_dados():
    """Carrega os dados do arquivo JSON. Se não existir, cria estrutura inicial."""
    if not os.path.exists(CAMINHO_ARQUIVO):
        dados_iniciais = {"usuarios": [], "ongs": [], "eventos": [],"rankings_semanais":[],"rankings_mensais": [], "rankings_anos": {}}
        salvar_dados(dados_iniciais)
        return dados_iniciais

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Se o arquivo estiver corrompido ou vazio
            return {"usuarios": [], "ongs": [], "eventos": [],"rankings_semanais":[],"rankings_mensais": [], "rankings_anos": {}}


def salvar_dados(dados):
    """Salva o dicionário de dados no arquivo JSON."""
    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def limpar_dados():
    """Zera completamente o banco de dados."""
    dados_vazios = {"usuarios": [], "ongs": [], "eventos": [],"rankings_semanais":[],"rankings_mensais": [], "rankings_anos": {}}
    salvar_dados(dados_vazios)
    print("✅ Banco de dados limpo com sucesso!")
