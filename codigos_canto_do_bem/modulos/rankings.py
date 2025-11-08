import os
import sys
from datetime import datetime, date 

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados,salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

hoje = date.today()

class Rank:
    def __init__(self,nome,horas):
        self.nome = nome
        self.horas = horas

    def listar_semana(nome,horas):
        

def menu_rankings(usuario_logado):
    dados = carregar_dados()
    console.print(Panel("Menu de Rankings 🏆", style = "bold cyan"))
    console.print("1 - Ranking da Semana\n 2 - Ranking do mês\n 3 - Ranking all-time\n 4 - Sair")
    while True:
        try:
            opcao = int(input("Escolha uma opcão: "))
            if opcao == 1:
                