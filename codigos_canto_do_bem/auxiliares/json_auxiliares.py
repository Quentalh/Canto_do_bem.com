import json
import os 

CAMINHO_ATUAL = os.path.abspath(__file__)

PASTA_AUXILIARES = os.path.dirname(CAMINHO_ATUAL)

CAMINHO_RAIZ_PROJETO = os.path.dirname(PASTA_AUXILIARES)

CAMINHO_ARQUIVO = os.path.join(CAMINHO_RAIZ_PROJETO, 'base_de_dados', 'dados.json')

def carregar_dados():

    try:

        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except FileNotFoundError:

        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        
        dados_iniciais = {"usuarios": [], "eventos": []}
        
        salvar_dados(dados_iniciais)
        
        return dados_iniciais

def salvar_dados(dados):

    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)