import os
import sys
CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados
from rich.console import Console
from rich.panel import Panel
from modulos.classes import Usuario, ONG

console = Console()

def login():
    dados = carregar_dados()
    console.clear()
    console.print(Panel("🔐 Login", style="bold cyan"))

    while True:
        email = input("E-mail: ").strip()
        senha = input("Senha: ").strip()

        usuario_dict = next((u for u in dados["usuarios"] if u["email"] == email and u["senha"] == senha), None)
        tipo_obj = "usuario"
        
        if not usuario_dict:
            usuario_dict = next((o for o in dados["ongs"] if o["email"] == email and o["senha"] == senha), None)
            tipo_obj = "ong"

        if usuario_dict:

            if tipo_obj == "usuario":
                obj = Usuario(usuario_dict)
            else:
                obj = ONG(usuario_dict)

            if not obj.dados.get('email_verificado'):
                console.clear()
                console.print("[bold yellow]⚠️ Sua conta ainda não foi verificada![/bold yellow]")
                console.print(f"Um código de verificação será enviado para: {obj.email}")
                input("Pressione Enter para enviar o código...")
                
                obj.gerar_codigo_verificacao()
                
                while True:
                    codigo = input("\nDigite o código recebido no e-mail (ou 'sair' para cancelar): ").strip()
                    
                    if codigo.lower() == 'sair':
                        console.print("[red]Login cancelado.[/red]")
                        input("Pressione Enter para voltar...")
                        return None
                        
                    if obj.confirmar_email(codigo):
                        console.print("[bold green]✅ Conta verificada com sucesso![/bold green]")
                        input("Pressione Enter para entrar...")
                        break 
                    else:
                        console.print("[bold red]Código incorreto. Tente novamente.[/bold red]")
            
            console.clear()
            console.print(f"[bold green]Login realizado com sucesso! Bem-vindo(a) {obj.nome}[/bold green]")
            input("Pressione Enter para entrar...")
            console.clear()
            
            return obj 
        else:
            console.print("[bold red]E-mail ou senha incorretos! Tente novamente.[/bold red]")

if __name__ == "__main__":
    login()