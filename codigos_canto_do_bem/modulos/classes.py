import sys
import os
from datetime import datetime, timedelta, date

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

class Entidade:
    def __init__(self, dados_dict):
        self.dados = dados_dict
        self.email = dados_dict.get('email')
        self.nome = dados_dict.get('nome')
        self.tipo = dados_dict.get('tipo')
        
        self.dados.setdefault('cidade', '')
        self.dados.setdefault('estado', '')
        self.dados.setdefault('notificacoes', [])

    def salvar(self):
        todos_dados = carregar_dados()
        chave = "usuarios" if self.tipo == "usuario" else "ongs"
        
        encontrado = False
        for i, ent in enumerate(todos_dados[chave]):
            if ent['email'] == self.email:
                todos_dados[chave][i] = self.dados
                encontrado = True
                break
        
        if encontrado:
            salvar_dados(todos_dados)

    def adicionar_notificacao(self, mensagem):
        nova_notificacao = {
            "mensagem": mensagem,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "lida": False
        }
        self.dados['notificacoes'].insert(0, nova_notificacao)
        self.salvar()

    def ver_notificacoes(self):
        console.clear()
        notificacoes = self.dados.get('notificacoes', [])
        
        if not notificacoes:
            console.print("[bold yellow]Você não tem novas notificações.[/bold yellow]")
            input("Pressione Enter para voltar...")
            console.clear()
            return

        console.print(Panel(f"🔔 Notificações de {self.nome}", style="bold cyan"))
        
        for notif in notificacoes:
            notif['lida'] = True
        self.salvar()

        for idx, notif in enumerate(notificacoes, 1):
            console.print(f"{idx}. {notif['data']} - {notif['mensagem']}")

        console.print("\nOpções:")
        console.print("L - Limpar todas as notificações")
        console.print("V - Voltar")
        
        opcao = input("Escolha: ").strip().upper()
        
        if opcao == "L":
            self.dados['notificacoes'] = []
            self.salvar()
            console.print("[green]Notificações limpas![/green]")
            input("Pressione Enter...")
        
        console.clear()

class Usuario(Entidade):
    def __init__(self, dados_dict):
        super().__init__(dados_dict)
        self.dados.setdefault('Pontos', 0)
        self.dados.setdefault('historico_de_compras', [])
        self.dados.setdefault('anos_participados', [])
        self.dados.setdefault('historico_eventos', [])
        self.dados.setdefault('eventos_marcados', [])
        self.dados.setdefault('Medalhas', [])

    @property
    def pontos(self):
        return self.dados['Pontos']

    @pontos.setter
    def pontos(self, valor):
        self.dados['Pontos'] = valor

    def adicionar_historico_compra(self, item_str):
        self.dados['historico_de_compras'].append(item_str)
        self.salvar()

    def descontar_pontos(self, valor):
        if self.pontos >= valor:
            self.pontos -= valor
            self.adicionar_notificacao(f"Compra realizada: -{valor} pontos.")
            self.salvar()
            return True
        return False

    def calcular_medalhas(self):
        dados = carregar_dados()
        medalhas = {
            'semanais': 0, 'mensais': [0, 0, 0], 'anuais': [0, 0, 0],
            'mensais_ano': [0, 0, 0], 'semanais_ano': 0
        }

        def verificar_pos(lista, destino):
            if not lista: return
            if lista[0][0] == self.nome: destino[0] += 1
            if len(lista) > 1 and lista[1][0] == self.nome: destino[1] += 1
            if len(lista) > 2 and lista[2][0] == self.nome: destino[2] += 1

        for r in dados.get('rankings_semanais', {}).values():
            if r and r[0][0] == self.nome: medalhas['semanais'] += 1
        for r in dados.get('rankings_mensais', {}).values():
            verificar_pos(r, medalhas['mensais'])

        for y in dados.get('rankings_anos', {}).values():
            verificar_pos(y.get('ranking_anual', []), medalhas['anuais'])
            for r in y.get('rankings_semanais', {}).values():
                if r and r[0][0] == self.nome:
                    medalhas['semanais'] += 1
                    medalhas['semanais_ano'] += 1
            for r in y.get('rankings_mensais', {}).values():
                verificar_pos(r, medalhas['mensais'])
                verificar_pos(r, medalhas['mensais_ano'])
        
        return medalhas

    def processar_recompensas_anuais(self, ano_ref):
        tem_evento = False
        for ev in self.dados.get('historico_eventos', []):
            try:
                if datetime.strptime(ev['data'], "%d/%m/%Y").year == ano_ref:
                    tem_evento = True
                    break
            except ValueError: continue

        if tem_evento and ano_ref not in self.dados['anos_participados']:
            med = self.calcular_medalhas()
            bonus = (med['semanais_ano'] * 10) + \
                    (med['mensais_ano'][0] * 30) + (med['mensais_ano'][1] * 25) + (med['mensais_ano'][2] * 20) + \
                    (med['anuais'][0] * 50) + (med['anuais'][1] * 45) + (med['anuais'][2] * 40)
            
            if bonus > 0:
                self.pontos += bonus
                self.adicionar_notificacao(f"🎉 Parabéns! Você recebeu {bonus} pontos pelas medalhas de {ano_ref}!")
            
            self.dados['anos_participados'].insert(0, ano_ref)
            self.salvar()
            return bonus
        return 0

    def verificar_lembretes_agenda(self):
        amanha = date.today() + timedelta(days=1)
        
        for evento in self.dados.get('eventos_marcados', []):
            try:
                data_evento = datetime.strptime(evento['data'], "%d/%m/%Y").date()
                
                if data_evento == amanha:
                    msg = f"📅 Lembrete: O evento '{evento['nome']}' é amanhã ({evento['data']})!"
                    
                    ja_notificado = any(n['mensagem'] == msg for n in self.dados['notificacoes'])
                    
                    if not ja_notificado:
                        self.adicionar_notificacao(msg)
            except ValueError:
                continue

class ONG(Entidade):
    def __init__(self, dados_dict):
        super().__init__(dados_dict)
        self.dados.setdefault('eventos_criados', [])
        self.dados.setdefault('doacoes_recebidas', 0)
        self.dados.setdefault('descricao', '')
        self.dados.setdefault('logradouro', '')
        self.dados.setdefault('bairro', '')

    @property
    def descricao(self):
        return self.dados['descricao']

    @descricao.setter
    def descricao(self, texto):
        self.dados['descricao'] = texto
        self.salvar()

    @property
    def doacoes(self):
        return self.dados['doacoes_recebidas']

    def adicionar_evento(self, evento_dict):
        self.dados['eventos_criados'].append(evento_dict)
        self.adicionar_notificacao(f"Evento '{evento_dict['nome']}' criado com sucesso.")
        self.salvar()