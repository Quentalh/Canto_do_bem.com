from rich.console import Console
from rich.panel import Panel
from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from datetime import datetime, date 

console = Console()
hoje = date.today()



def ver_calendario(usuario_logado):
    console.print(Panel(f"Calendário de {usuario_logado['nome']}", style="bold cyan"))

    if not usuario_logado.get("historico_eventos",[]):
        console.print("[bold yellow]Você ainda não adicionou nenhum evento.[/bold yellow]")
    else:
        console.print('Eventos marcados:')
        eventos_marcados = []
        for  evento in usuario_logado.get("historico_eventos",[]):
            evento_data = datetime.strptime(evento['data'], "%d/%m/%Y").date()
            if evento_data > hoje:
                eventos_marcados.append(evento)
        for idx,disponivel in enumerate(eventos_marcados,1):
            console.print(f"{idx}. {disponivel['nome']} - Criado por: {disponivel['criado_por']} (Data: {disponivel['data']} Horário: {disponivel['inicio']} até {disponivel["fim"]})")


    input("\nPressione ENTER para voltar...")


def adicionar_evento_calendario(usuario_logado):
    dados = carregar_dados()

    console.print(Panel("Adicionar evento ao calendário", style="bold cyan"))

    todos_eventos = dados.get("eventos", [])
    if not todos_eventos:
        console.print("[bold yellow]Nenhum evento disponível ainda.[/bold yellow]")
        return

    console.print("Eventos disponíveis:")
    eventos_disponiveis = []
    for  evento in todos_eventos:
        evento_data = datetime.strptime(evento['data'], "%d/%m/%Y").date()
        if evento_data > hoje:
            eventos_disponiveis.append(evento)
    for idx,disponivel in enumerate(eventos_disponiveis,1):
        console.print(f"{idx}. {disponivel['nome']} - Criado por: {disponivel['criado_por']} Data: {disponivel['data']} Horário: {disponivel['inicio']} até {disponivel["fim"]} ")

    escolha = input("\nDigite o número do evento que deseja adicionar: ").strip()

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(todos_eventos):
        console.print("[bold red]Escolha inválida![/bold red]")
        return

    evento_escolhido_obj = todos_eventos[int(escolha) - 1]
    nome_evento_escolhido = evento_escolhido_obj["nome"]

    ja_participa = False
    for item in usuario_logado["historico_eventos"]:
        nome_na_lista = ""
        nome_na_lista = item.get("nome")

        if nome_na_lista == nome_evento_escolhido:
            ja_participa = True
            break

    if ja_participa:
        console.print("[bold yellow]Você já está participando deste evento.[/bold yellow]")
        return

    evento_para_adicionar = {
        "nome": evento_escolhido_obj["nome"],
        "data": evento_escolhido_obj["data"]
    }

    usuario_logado["historico_eventos"].append(evento_para_adicionar)

    for u in dados["usuarios"]:
        if u["email"] == usuario_logado["email"]:
            u.update(usuario_logado)
            break

    salvar_dados(dados)
    console.print(f"[bold green]Evento '{nome_evento_escolhido}' adicionado ao seu calendário![/bold green]")