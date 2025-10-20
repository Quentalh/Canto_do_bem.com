from auxiliares.json_auxiliares import carregar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

def login():
    dados = carregar_dados()
    console.print(Panel("Login", style="bold cyan"))
    email = input("E-mail: ")
    senha = input("Senha: ")

    for tipo in ["usuarios", "ongs"]:
        for usuario in dados[tipo]:
            if usuario["email"] == email and usuario["senha"] == senha:
                console.print(f"[bold green]Login bem-sucedido! Bem-vindo(a), {usuario['nome']}![/bold green]")
                return usuario

    console.print("[bold red]E-mail ou senha incorretos.[/bold red]")
    return None
