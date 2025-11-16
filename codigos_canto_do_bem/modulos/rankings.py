import os
import sys
from datetime import datetime, date, timedelta
import calendar

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados,salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

hoje = date.today()

init_semana = hoje

if init_semana.weekday() != 6:
    dias_para_recuar = (init_semana.weekday() + 1) % 7
    init_semana = init_semana - timedelta(days=dias_para_recuar)
fim_semana = init_semana + timedelta(days=6)

num_dias_mes = calendar.monthrange(hoje.year, hoje.month)

init_mes = date(hoje.year, hoje.month, 1)

fim_mes = date(hoje.year, hoje.month, num_dias_mes[1])

dados = carregar_dados()
usuarios = dados['usuarios']

def ranking(usuario_logado,n,m):
    pontos_semana = []
    init_p = n
    fim_p = m


    for x in usuarios:
        pontuacao = 0
        eventos_p = []
        if n == 0 and m == 0:
            for i in x['historico_eventos']:
                eventos_p.append(i)
            for pnts in eventos_p:
                pontuacao = pnts['horas_total'] + pontuacao
            pontos_semana.append([x,pontuacao])
        else:
            for i in x['historico_eventos']:
                data_user = datetime.strptime(i['data'], "%d/%m/%Y")
                if data_user.date() >= init_p and data_user.date() <= fim_p:
                    eventos_p.append(i)
            for pnts in eventos_p:
                pontuacao = pnts['horas_total'] + pontuacao
            pontos_semana.append([x,pontuacao])
    pontos_semana.sort(key=lambda x: x[1],reverse=True)
    diferenca = m - n
    if isinstance(diferenca,timedelta):
        if diferenca.days == 6  :
            p = "Ranking Semanal: "
        else:
            p = "Ranking Mensal: "
    else:
        p = "Ranking All-Time: "
    for r in pontos_semana:
        if r[0]['email'] == usuario_logado['email']:
            break
    console.print(Panel(f"{p}\n\nPressione ENTER para voltar...",style = "bold cyan"))
    console.print(f"Sua posição: {pontos_semana.index(r) + 1}º - {r[0]['nome']}: Pontos {r[1]}")
    for idx,user in enumerate(pontos_semana,1):
        console.print(f"{idx}º - {user[0]['nome']}: Pontos {user[1]}")                                                                                            
    input("\nPressione ENTER para voltar...")
    console.clear()
    return
    


def menu_rankings(usuario_logado):
    while True:
            console.print(Panel("Menu de Rankings 🏆", style = "bold cyan"))
            console.print("1 - Ranking da Semana\n2 - Ranking do mês\n3 - Ranking all-time\n4 - Sair")
            try:
                opcao = int(input("Escolha uma opcão: "))
                console.clear()
                if opcao == 1:
                    ranking(usuario_logado,0,0)
                elif opcao == 2:
                    ranking(usuario_logado,init_semana,fim_semana)
                elif opcao == 3:
                    ranking(usuario_logado,init_mes,fim_mes)
                elif opcao == 4:
                    return
                else:
                    raise ValueError
            except ValueError:
                console.print("Opção inválida. Tente novamente")
            
if __name__ == "__main__":
    opcao = int(input("Qual função vc quer testar?"))
    console.clear()
    if opcao == 1:
        ranking(0,0)
    elif opcao == 2:
        ranking(init_semana,fim_semana)
    elif opcao == 3:
        ranking(init_mes,fim_mes)
