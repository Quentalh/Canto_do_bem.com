import os
import sys
from datetime import datetime, date, timedelta
import calendar

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()
hoje = date.today()

def _calcular_pontos_filtrados(usuarios, filtro_data):
    ranking = []
    for usuario in usuarios:
        pontos = 0
        for evento in usuario.get('historico_eventos', []):
            try:
                dt = datetime.strptime(evento['data'], "%d/%m/%Y").date()
                if filtro_data(dt):
                    pontos += evento.get('horas_total', 0)
            except ValueError: continue
        if pontos > 0:
            ranking.append([usuario['nome'], pontos])
    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking

def _notificar_vencedores(dados, categoria, nome_periodo, ranking):
    if not ranking: return

    medalhas = ["🥇 Ouro", "🥈 Prata", "🥉 Bronze"]
    
    for i in range(min(len(ranking), 3)):
        nome_vencedor = ranking[i][0]
        tipo_medalha = medalhas[i]
        
        for usuario in dados['usuarios']:
            if usuario['nome'] == nome_vencedor:
                if 'notificacoes' not in usuario: usuario['notificacoes'] = []
                
                msg = f"🏆 Você ganhou a Medalha de {tipo_medalha} no Ranking {categoria} ({nome_periodo})!"
                
                ja_notificado = any(n['mensagem'] == msg for n in usuario['notificacoes'])
                
                if not ja_notificado:
                    nova_notificacao = {
                        "mensagem": msg,
                        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "lida": False
                    }
                    usuario['notificacoes'].insert(0, nova_notificacao)
                break

def atualizar_rankings_sistema(ano_passado):
    dados = carregar_dados()
    usuarios = dados['usuarios']
    
    if 'rankings_mensais' not in dados: dados['rankings_mensais'] = {}
    for mes in range(1, hoje.month):
        nome_mes = calendar.month_name[mes].capitalize()
        rank = _calcular_pontos_filtrados(
            usuarios, lambda d: d.year == hoje.year and d.month == mes
        )
        dados['rankings_mensais'][nome_mes] = rank
        _notificar_vencedores(dados, "Mensal", nome_mes, rank)

    if 'rankings_semanais' not in dados: dados['rankings_semanais'] = {}
    dia_do_ano = datetime.now().timetuple().tm_yday
    n, semana = 1, 1
    while n + 6 < dia_do_ano:
        nome_semana = f'Semana {semana}'
        rank = _calcular_pontos_filtrados(
            usuarios, lambda d: d.year == hoje.year and n <= d.timetuple().tm_yday <= n + 6
        )
        dados['rankings_semanais'][nome_semana] = rank
        if rank: _notificar_vencedores(dados, "Semanal", nome_semana, [rank[0]])
        n += 7; semana += 1

    str_ano = str(ano_passado)
    if str_ano not in dados.get('rankings_anos', {}):
        if 'rankings_anos' not in dados: dados['rankings_anos'] = {}
        rank_ano = {"ranking_anual": [], "rankings_mensais": {}, "rankings_semanais": {}}
        
        rank = _calcular_pontos_filtrados(usuarios, lambda d: d.year == ano_passado)
        rank_ano['ranking_anual'] = rank
        _notificar_vencedores(dados, "Anual", str_ano, rank)
        
        for mes in range(1, 13):
            nome = calendar.month_name[mes].capitalize()
            rank_ano['rankings_mensais'][nome] = _calcular_pontos_filtrados(
                usuarios, lambda d: d.year == ano_passado and d.month == mes
            )
        n, sem = 1, 1
        while n <= 366:
            rank_ano['rankings_semanais'][f"{sem}ª Semana"] = _calcular_pontos_filtrados(
                usuarios, lambda d: d.year == ano_passado and n <= d.timetuple().tm_yday <= n + 6
            )
            n += 7; sem += 1
            
        dados['rankings_anos'][str_ano] = rank_ano

    salvar_dados(dados)

init_semana = hoje
if init_semana.weekday() != 6:
    dias_recuar = (init_semana.weekday() + 1) % 7
    init_semana = init_semana - timedelta(days=dias_recuar)
fim_semana = init_semana + timedelta(days=6)
num_dias_mes = calendar.monthrange(hoje.year, hoje.month)
init_mes = date(hoje.year, hoje.month, 1)
fim_mes = date(hoje.year, hoje.month, num_dias_mes[1])

def ranking(usuario_dados, n, m):
    console.clear()
    pontos_semana = []
    usuarios = carregar_dados()['usuarios']

    for x in usuarios:
        pontuacao = 0
        eventos_p = []
        if n == 0 and m == 0:
            for i in x.get('historico_eventos', []): eventos_p.append(i)
            for pnts in eventos_p: pontuacao += pnts.get('horas_total', 0)
            if pontuacao <= 0: continue
            pontos_semana.append([x, pontuacao])
        else:
            for i in x.get('historico_eventos', []):
                try:
                    data_user = datetime.strptime(i['data'], "%d/%m/%Y").date()
                    if n <= data_user <= m: eventos_p.append(i)
                except ValueError: continue
            for pnts in eventos_p: pontuacao += pnts.get('horas_total', 0)
            if pontuacao <= 0: continue
            pontos_semana.append([x, pontuacao])
            
    pontos_semana.sort(key=lambda x: x[1], reverse=True)
    
    msg = "Ranking All-Time:"
    if isinstance(m, date): msg = "Ranking do Período:"

    r = None
    for item in pontos_semana:
        if item[0]['email'] == usuario_dados['email']:
            r = item
            break

    console.print(Panel(f"{msg}\n\nEnter para voltar...", style="bold cyan"))
    if r:
        console.print(f"Sua posição: {pontos_semana.index(r) + 1}º - {r[0]['nome']}: {r[1]} pts")
    
    for idx, user in enumerate(pontos_semana, 1):
        console.print(f"{idx}º - {user[0]['nome']}: {user[1]} pts")              
    
    input()
    console.clear()

def menu_rankings(usuario_dados):
    while True:
        console.clear()
        console.print(Panel("Menu de Rankings 🏆", style="bold cyan"))
        console.print("1 - Ranking da Semana\n2 - Ranking do mês\n3 - Ranking all-time\n4 - Sair")
        try:
            opcao = int(input("Opção: "))
            
            if opcao == 1: ranking(usuario_dados, init_semana, fim_semana)
            elif opcao == 2: ranking(usuario_dados, init_mes, fim_mes)
            elif opcao == 3: ranking(usuario_dados, 0, 0)
            elif opcao == 4: 
                console.clear()
                return
        except ValueError:
            console.print("Opção inválida.")
            input("Pressione Enter...")