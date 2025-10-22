from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

def ver_calendario(usuario):
    """
    Mostra todos os eventos que o usuário está participando.
    """
    dados = carregar_dados()
    console.print(Panel("📅 Seu Calendário", style="bold cyan"))

    eventos_usuario = usuario.get("eventos_participando", [])
    if not eventos_usuario:
        console.print("[bold yellow]Você não possui eventos cadastrados.[/bold yellow]")
        return

    for idx, evento_nome in enumerate(eventos_usuario, start=1):
        console.print(f"{idx}. {evento_nome}")


def adicionar_evento_calendario(usuario):
    """
    Permite ao usuário adicionar um evento existente ao seu calendário pessoal.
    """
    dados = carregar_dados()
    console.print(Panel("📌 Adicionar Evento ao Calendário", style="bold cyan"))

    todos_eventos = dados.get("eventos", [])
    if not todos_eventos:
        console.print("[bold yellow]Não há eventos disponíveis para adicionar.[/bold yellow]")
        return

    # Mostra todos os eventos disponíveis
    for idx, evento in enumerate(todos_eventos, start=1):
        console.print(f"{idx}. {evento.get('nome','Sem nome')} - Criado por: {evento.get('criado_por','Desconhecido')}")

    while True:
        escolha = input("Digite o número do evento que deseja adicionar: ").strip()
        if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(todos_eventos):
            console.print("[bold red]Escolha inválida. Tente novamente.[/bold red]")
        else:
            evento_escolhido = todos_eventos[int(escolha) - 1]["nome"]
            break

    # Adiciona o evento ao calendário do usuário
    if "eventos_participando" not in usuario:
        usuario["eventos_participando"] = []

    if evento_escolhido in usuario["eventos_participando"]:
        console.print("[bold yellow]Você já está participando deste evento.[/bold yellow]")
    else:
        usuario["eventos_participando"].append(evento_escolhido)
        # Atualiza o usuário no JSON
        for idx, u in enumerate(dados["usuarios"]):
            if u["email"] == usuario["email"]:
                dados["usuarios"][idx] = usuario
                break
        salvar_dados(dados)
        console.print(f"[bold green]Evento '{evento_escolhido}' adicionado ao seu calendário com sucesso![/bold green]")
