from rich.console import Console
from rich.panel import Panel
from auxiliares.json_auxiliares import carregar_dados, salvar_dados

console = Console()


def ver_calendario(usuario_logado):
    console.print(Panel(f"Calendário de {usuario_logado['nome']}", style="bold cyan"))

    if not usuario_logado.get("eventos_participando"):
        console.print("[bold yellow]Você ainda não adicionou nenhum evento.[/bold yellow]")
    else:
        for evento in usuario_logado["eventos_participando"]:
            console.print(f"- {evento}")

    input("\nPressione ENTER para voltar...")


def adicionar_evento_calendario(usuario_logado):
    dados = carregar_dados()

    console.print(Panel("Adicionar evento ao calendário", style="bold cyan"))

    # listar eventos disponíveis
    todos_eventos = dados.get("eventos", [])
    if not todos_eventos:
        console.print("[bold yellow]Nenhum evento disponível ainda.[/bold yellow]")
        return

    console.print("Eventos disponíveis:")
    for idx, evento in enumerate(todos_eventos, 1):
        console.print(f"{idx}. {evento['nome']} - Criado por: {evento['criado_por']}")

    escolha = input("\nDigite o número do evento que deseja adicionar: ").strip()

    if not escolha.isdigit() or int(escolha) < 1 or int(escolha) > len(todos_eventos):
        console.print("[bold red]Escolha inválida![/bold red]")
        return

    evento_escolhido = todos_eventos[int(escolha) - 1]["nome"]

    if evento_escolhido in usuario_logado["eventos_participando"]:
        console.print("[bold yellow]Você já está participando deste evento.[/bold yellow]")
        return

    usuario_logado["eventos_participando"].append(evento_escolhido)

    # atualizar no JSON
    for u in dados["usuarios"]:
        if u["email"] == usuario_logado["email"]:
            u.update(usuario_logado)
            break

    salvar_dados(dados)
    console.print(f"[bold green]Evento '{evento_escolhido}' adicionado ao seu calendário![/bold green]")
