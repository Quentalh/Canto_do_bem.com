from rich.console import Console
from rich.panel import Panel
from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from datetime import datetime

console = Console()
hoje = datetime.now().date()

def ver_calendario(usuario_logado):
    console.clear()
    console.print(Panel(f"Calendário de {usuario_logado['nome']}", style="bold cyan"))

    if not usuario_logado.get("eventos_marcados",[]):
        console.print("[bold yellow]Você ainda não adicionou nenhum evento.[/bold yellow]")
    else:
        console.print('Eventos marcados:')
        for idx in range(len(usuario_logado.get('eventos_marcados',[])) - 1, -1, -1):
            evento = usuario_logado.get('eventos_marcados',[])[idx]
            evento_data_obj = datetime.strptime(evento['data'], "%d/%m/%Y")
            diferenca = hoje - evento_data_obj.date()
            if diferenca.days > 5:
                usuario_logado.get('eventos_marcados',[]).pop(idx)
                
        for idx,disponivel in enumerate(usuario_logado["eventos_marcados"],1):
            console.print(f"{idx}. {disponivel['nome']} - Criado por: {disponivel['criado_por']} (Data: {disponivel['data']} Horário: {disponivel['inicio']} até {disponivel['fim']})")

    input("\nPressione ENTER para voltar...")
    console.clear()

def adicionar_evento_calendario(usuario_logado):
    dados = carregar_dados()
    console.clear()
    console.print(Panel("Adicionar evento ao calendário", style="bold cyan"))

    todos_eventos = dados.get("eventos", [])
    if not todos_eventos:
        console.print("[bold yellow]Nenhum evento disponível ainda.[/bold yellow]")
        input("Enter...")
        return

    console.print("Eventos disponíveis:")
    eventos_disponiveis = []
    for evento in todos_eventos:
        evento_data = datetime.strptime(evento['data'], "%d/%m/%Y").date()
        if evento_data > hoje:
            eventos_disponiveis.append(evento)
            
    for idx,disponivel in enumerate(eventos_disponiveis,1):
        console.print(f"{idx}. {disponivel['nome']} - {disponivel['data']} ({disponivel['inicio']}-{disponivel['fim']})")

    escolha = input("\nDigite o número do evento (ou algo não numérico para sair): ").strip()

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(eventos_disponiveis):
        console.print("[bold red]Saindo...[/bold red]")
        return

    evento_escolhido_obj = eventos_disponiveis[int(escolha) - 1]
    nome_evento_escolhido = evento_escolhido_obj["nome"]

    ja_participa = any(item.get("nome") == nome_evento_escolhido for item in usuario_logado["eventos_marcados"])

    if ja_participa:
        console.print("[bold yellow]Você já está participando deste evento.[/bold yellow]")
        input("Enter...")
        console.clear()
        return
    
    usuario_logado["eventos_marcados"].append(evento_escolhido_obj)

    for u in dados["usuarios"]:
        if u["email"] == usuario_logado["email"]:
            u.update(usuario_logado)
            break

    salvar_dados(dados)
    console.print(f"[bold green]Evento '{nome_evento_escolhido}' adicionado ao seu calendário![/bold green]")
    input("Pressione ENTER para voltar...")
    console.clear()