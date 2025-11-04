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

def checkar_presenca(usuario_logado):   
    while True:
        eventos_passados = []
        dados = carregar_dados()
        console.print(Panel("Checagem de presença ✔❌", style="bold cyan"))
        console.print("1 - Sair")
        console.print("Eventos disponiveis para checagem: ")
        
        eventos_criados = usuario_logado.get("eventos_criados", [])
        
        if not eventos_criados:
            console.print("[bold yellow]Você não possui nenhum evento criado.[/bold yellow]")
            input("Pressione Enter para voltar...")
            return

        for eventos in eventos_criados:
            try:
                evento_data = datetime.strptime(eventos['data'], "%d/%m/%Y").date()
                if evento_data < hoje:
                    eventos_passados.append(eventos)
            except (ValueError, KeyError):
                continue

        if not eventos_passados:
            console.print("[bold yellow]Nenhum evento passado encontrado para checagem.[/bold yellow]")
            input("Pressione Enter para voltar...")
            return

        for idx, eventop in enumerate(eventos_passados, 2):
            console.print(f"{idx}. {eventop['nome']}- {eventop['data']}")
        
        tamanho = len(eventos_passados)
        if len(eventos_passados) == 1:
            tamanho = len(eventos_passados) + 1 
        
        try:
            opcao = int(input("Digite o numero correspondente a um dos eventos. Ou saia pressionando 1: "))

            if opcao == 1:
                return
                
            elif 2 <= opcao <= tamanho:

                usuarios_presenca = []

                evento_escolhido = eventos_passados[opcao - 2] 
                

                for usuario in dados["usuarios"]:
                    for evento in usuario.get("historico_eventos", []): 

                        if evento.get('nome') == evento_escolhido.get('nome') and evento.get('data') == evento_escolhido.get('data'):

                            usuarios_presenca.append(usuario)
                

                if not usuarios_presenca:
                    console.print("[bold yellow]Nenhum usuário participou deste evento.[/bold yellow]")
                    input("Pressione Enter para continuar...")
                    continue 

                while True:
                    console.print("\n[bold cyan]Usuários para dar presença:[/bold cyan]")
                    console.print("0 - Voltar")
                    for idx, presenca in enumerate(usuarios_presenca, 1):
                        console.print(f"{idx}. {presenca['nome']} - {presenca['email']}")
                    
                    try:
                        escolha = int(input("Digite o numero correspondente ao usuário ou 0 para voltar: "))
                        
                        if escolha == 0:
                            break

                        if 1 <= escolha <= len(usuarios_presenca):

                            entregador = usuarios_presenca[escolha - 1]
                            
                            pontos_ganhos = evento_escolhido.get('horas_total')
                                
                            entregador['Pontos'] += pontos_ganhos
                            
                            console.print(f"[bold green]Presença confirmada! {entregador['nome']} ganhou {pontos_ganhos} pontos![/bold green]")
                            
                            usuarios_presenca.pop(escolha - 1)
                            
                            salvar_dados(dados) 
                            
                            if not usuarios_presenca:
                                console.print("[bold blue]Todos os participantes receberam pontos.[/bold blue]")
                                break

                        else: console.print("Opção inválida, tente novamente")

                    except ValueError: console.print("Apenas digitos são aceitos, tente novamente")

            else: console.print("Opção inválida, digite novamente")

        except ValueError: console.print("Apenas digitos são aceitos, tente novamente")