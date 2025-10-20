from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

def criar_evento(usuario_logado):
    dados = carregar_dados()
    console.print(Panel("Criação de Evento", style="bold cyan"))

    nome = input("Nome do evento: ")
    descricao = input("Descrição: ")
    data = input("Data (dd/mm/aaaa): ")
    cidade = input("Cidade: ")

    evento = {
        "nome": nome,
        "descricao": descricao,
        "data": data,
        "cidade": cidade,
        "criado_por": usuario_logado["nome"],
        "tipo_criador": usuario_logado["tipo"]
    }

    dados["eventos"].append(evento)

    if usuario_logado["tipo"] == "ong":
        for ong in dados["ongs"]:
            if ong["email"] == usuario_logado["email"]:
                ong["eventos_criados"].append(nome)
                break

    salvar_dados(dados)
    console.print("[bold green]Evento criado com sucesso![/bold green]")
