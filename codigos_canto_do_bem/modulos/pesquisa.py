import os
import sys
CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

def menu_pesquisa():
    dados = carregar_dados()

    console.print(Panel("Menu de Pesquisa \n\nPor qual tipo de usuário você procura?", style="bold cyan"))

    while True:
        console.print("1- Usuário comum\n2- ONG")

        try:
            opcao = int(input("\nEscolha uma opção: ").strip())
            if opcao == 1:
                console.print(Panel("Pesquisa de Usuário", style="bold cyan" ))
                console.print("Digite o nome e o email do usuário:")
                nome = input("\nNome do usuário: ").strip()
                email = input("\nE-mail do usuário: ").strip()
                usuariop = next((u for u in dados["usuarios"] if u["email"] == email and u["nome"] == nome), None)
                if usuariop:
                    interesses = usuariop.get("interesses")
                    eventos_p = usuariop.get("eventos_participando")
                    console.print(f"[bold green]Usuário encontrado![/bold green] \n {nome} \n {email} \n {interesses} \n {eventos_p}")
                    tipo ="usuario"
                    eventos_criados = [
                        evento for evento in dados.get("eventos", [])
                        if evento.get("criado_por") == nome and evento.get('tipo_criador') == tipo]
                    if eventos_criados:
                        console.print("\n[bold cyan]Eventos criados por este usuário:[/bold cyan]")
                        for evento in eventos_criados:
                            console.print(f"- {evento['nome']} (Data: {evento['data']})")
                    else:
                        console.print("\nNenhum evento criado por este usuário.")
                    return usuariop
                else: 
                    console.print('\n[bold red]Nenhum usuário encontrado[/bold red]\n')
            elif opcao == 2:
                console.print(Panel("Pesquisa de ONGs", style="bold cyan" ))
                console.print("Digite o nome da ONG: ")
                nome = input("\nNome da ONG: ").strip()
                email = input("\nE-mail público da ONG: ").strip()
                ongp = next((u for u in dados["ongs"] if u["email"] == email and u["nome"] == nome), None)
                if ongp:
                    desc = ongp.get("descricao")
                    console.print(f"[bold green]ONG encontrada![/bold green] \n{nome} \n{email} \nDescrição da ONG: {desc}")
                    tipo = "ong"
                    eventos_criados = [
                        evento for evento in dados.get("eventos", [])
                        if evento.get("criado_por") == nome and evento.get('tipo_criador') == tipo
                    ]
                    if eventos_criados:
                        console.print("\n[bold cyan]Eventos criados por esta ONG:[/bold cyan]")
                        for evento in eventos_criados:
                            console.print(f"- {evento['nome']} (Data: {evento['data']})")
                    else:
                        console.print("\nNenhum evento criado por esta ONG.")
                    return ongp
                else: 
                    console.print('\n[bold red]Nenhuma ONG encontrada[/bold red]\n')
        except: console.print("Opção inválida, tente novamente")
menu_pesquisa()

            

    
