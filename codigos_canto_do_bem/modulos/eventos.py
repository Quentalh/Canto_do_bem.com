from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel
from datetime import datetime, date

console = Console()

def criar_evento(usuario_logado):
    dados = carregar_dados()
    console.print(Panel("📌 Criação de Evento/Voluntariado", style="bold cyan"))

    nome = input("Nome do evento: ").strip()
    descricao = input("Descrição do evento: ").strip()

    # Data do evento
    while True:
        data_input = input("Data (dd/mm/aaaa): ").strip()
        hoje = date.today()
        try:
            data_evento = datetime.strptime(data_input, "%d/%m/%Y").date()
            if data_evento < hoje:
                console.print("[bold red]Não é possível registrar um evento em uma data passada.[/bold red]")
            else:
                break
        except ValueError:
            console.print("[bold red]Formato de data inválido! Use dd/mm/aaaa.[/bold red]")

    # Cidade
    cidade = input("Cidade: ").strip()

    # NOVO: Endereço completo
    endereco = input("Endereço do evento: ").strip()

    evento = {
        "nome": nome,
        "descricao": descricao,
        "data": data_input,
        "cidade": cidade,
        "endereco": endereco,        # NOVO CAMPO
        "criado_por": usuario_logado["nome"],
        "tipo_criador": usuario_logado["tipo"]
    }

    dados["eventos"].append(evento)

    # Se ONG, adiciona na lista de eventos criados
    if usuario_logado["tipo"] == "ong":
        for ong in dados["ongs"]:
            if ong["email"] == usuario_logado["email"]:
                if "eventos_criados" not in ong:
                    ong["eventos_criados"] = []
                ong["eventos_criados"].append(nome)
                break

    salvar_dados(dados)
    console.print(f"[bold green]Evento '{nome}' criado com sucesso![/bold green]")
