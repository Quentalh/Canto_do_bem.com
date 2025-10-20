import json

CAMINHO_ARQUIVO = "base_de_dados/dados.json"

def carregar_dados():
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"usuarios": [], "ongs": [], "eventos": []}

def salvar_dados(dados):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
