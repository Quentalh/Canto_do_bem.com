import sys
import os
from datetime import datetime, date 

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

def criar_evento(usuario_logado):
    dados = carregar_dados()
    console.print(Panel("Criação de Evento", style="bold cyan"))

    nome = input("Nome do evento: ").strip()
    descricao = input("Descrição: ").strip()

    while True:
        data_input = input("Data (dd/mm/aaaa): ").strip()
        hoje = date.today()

        try:
            data_evento = datetime.strptime(data_input, "%d/%m/%Y").date()

            if data_evento < hoje:
                console.print("[bold red]Não é possível registar um evento numa data que já passou.[/bold red]")
                console.print("[bold red]Por favor, insira uma data futura.[/bold red]")
            else:
                break

        except ValueError:

            console.print("[bold red]Formato de data inválido! Use dd/mm/aaaa.[/bold red]")
    while True:
        try:
            hora_inicio = datetime.strptime(input("Digite o horário em que o evento inicia"), "%H:%M").time()

            hora_fim = datetime.strptime(input("Digite o horário em que o evento encerra"), "%H:%M").time()

            if hora_inicio == hora_fim:
                console.print("Você repetiu o mesmo hórario para o inicio e fim do evento!\nTente novamente")
            else:
                dt_inicio = datetime.combine(date.today(), hora_inicio)
                dt_fim = datetime.combine(date.today(), hora_fim)
                
                duracao = dt_fim - dt_inicio
                total_segundos = duracao.total_seconds()
                horas_total = total_segundos / 3600

                break
            

        except ValueError:
            console.print("Formato de horário inválido. Digite um horário dentro de 24 horas no formato h:m")

    cidade = input("Cidade: ").strip()

    evento = {
        "nome": nome,
        "descricao": descricao,
        "inicio": hora_inicio.isoformat(),
        "fim": hora_fim.isoformat(),
        "horas_total": horas_total,
        "data": data_input,
        "cidade": cidade,
        "criado_por": usuario_logado["nome"],
        "tipo_criador": usuario_logado["tipo"]
    }

    dados["eventos"].append(evento)

    if usuario_logado["tipo"] == "usuario":
        for usuario in dados["usuarios"]:
            if usuario["email"] == usuario_logado["email"]:
                if "eventos_criados" not in usuario:
                    usuario["eventos_criados"] = []
                usuario["eventos_criados"].append(evento)

    if usuario_logado["tipo"] == "ong":
        for ong in dados["ongs"]:
            if ong["email"] == usuario_logado["email"]:
                # Garante que a lista 'eventos_criados' existe
                if "eventos_criados" not in ong:
                    ong["eventos_criados"] = []
                ong["eventos_criados"].append(evento)
                break

    salvar_dados(dados)
    console.print("[bold green]Evento criado com sucesso![/bold green]")