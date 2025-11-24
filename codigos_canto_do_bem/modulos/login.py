import os
import sys
CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

def login():
    dados = carregar_dados()
    console.clear() 
    console.print(Panel("🔐 Login", style="bold cyan"))

    while True:
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()

        usuario = next((u for u in dados["usuarios"] if u["email"] == email and u["senha"] == senha), None)
        
        if not usuario:
            usuario = next((o for o in dados["ongs"] if o["email"] == email and o["senha"] == senha), None)

        if usuario:
            console.clear()
            console.print(f"[bold green]Login realizado com sucesso! Bem-vindo(a) {usuario['nome']}[/bold green]")
            input("Pressione Enter para entrar...")
            console.clear()
            return usuario
        else:
            console.print("[bold red]E-mail ou senha incorretos! Tente novamente.[/bold red]")

if __name__ == "__main__":
    login()