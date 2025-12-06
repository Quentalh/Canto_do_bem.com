import sys
import os
from datetime import datetime, timedelta, date
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

class Entidade:
    """Classe base para Usuarios e ONGs."""
    def __init__(self, dados_dict):
        self.dados = dados_dict
        self.email = dados_dict.get('email')
        self.nome = dados_dict.get('nome')
        self.tipo = dados_dict.get('tipo')
        
        self.dados.setdefault('cidade', '')
        self.dados.setdefault('estado', '')
        self.dados.setdefault('notificacoes', [])
        
        # Novos campos para Verificação de 2 Fatores
        self.dados.setdefault('email_verificado', False)
        self.dados.setdefault('codigo_verificacao', None)

        self.dados.setdefault('avaliacoes', []) # Lista de dicionários {autor, nota, comentario}
        self.dados.setdefault('nota_media', 0.0)


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
        """Adiciona uma nova notificação à lista."""
        nova_notificacao = {
            "mensagem": mensagem,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "lida": False
        }
        self.dados['notificacoes'].insert(0, nova_notificacao) # Adiciona no topo
        self.salvar()

    def ver_notificacoes(self):
        """Exibe as notificações e permite limpá-las."""
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

    def gerar_codigo_verificacao(self):
        codigo = str(random.randint(100000, 999999))
        self.dados['codigo_verificacao'] = codigo
        self.salvar()

        EMAIL_REMETENTE = "heitorquental321@gmail.com"
        SENHA_APP = "jaflflqgqxkapccs"

        console.print("[yellow]A preparar envio de e-mail seguro... aguarde.[/yellow]")

        try:
            if "seu_email_real" in EMAIL_REMETENTE:
                raise ValueError("E-mail de remetente não configurado no código.")

            msg = MIMEMultipart("alternative")
            msg['Subject'] = f'Seu Código de Verificação: {codigo}'
            msg['From'] = f"Canto do Bem <{EMAIL_REMETENTE}>"
            msg['To'] = self.email

            texto_simples = f"""\
            Olá {self.nome},
            
            O seu código de verificação para o Canto do Bem é: {codigo}
            
            Se não solicitou este código, por favor ignore este e-mail.
            """

            html_conteudo = f"""\
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                  <h2 style="color: #00bcd4; text-align: center;">Canto do Bem 🌍</h2>
                  <hr style="border: 0; border-top: 1px solid #eee;">
                  <p style="font-size: 16px; color: #333;">Olá, <strong>{self.nome}</strong>!</p>
                  <p style="font-size: 16px; color: #555;">Use o código abaixo para verificar a sua conta e aceder ao sistema:</p>
                  
                  <div style="background-color: #e0f7fa; padding: 15px; text-align: center; border-radius: 5px; margin: 20px 0;">
                    <span style="font-size: 24px; font-weight: bold; letter-spacing: 5px; color: #006064;">{codigo}</span>
                  </div>
                  
                  <p style="font-size: 14px; color: #777;">Este código é válido para o seu acesso atual.</p>
                  <hr style="border: 0; border-top: 1px solid #eee;">
                  <p style="font-size: 12px; color: #aaa; text-align: center;">© Canto do Bem - Sistema de Voluntariado</p>
                </div>
              </body>
            </html>
            """

            part1 = MIMEText(texto_simples, "plain")
            part2 = MIMEText(html_conteudo, "html")
            msg.attach(part1)
            msg.attach(part2)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA_APP)
                smtp.send_message(msg)
            
            console.print(f"[bold green]📧 E-mail enviado com sucesso para {self.email}![/bold green]")

        except Exception as e:
            console.print(f"[bold red]Falha ao enviar e-mail real: {e}[/bold red]")
            console.print("[yellow]Usando modo de simulação (Fallback):[/yellow]")
            console.print(Panel(
                f"📧 [bold]SIMULAÇÃO DE E-MAIL[/bold]\n\n"
                f"Para: {self.email}\n"
                f"Assunto: Código de Verificação\n\n"
                f"Código: [bold green]{codigo}[/bold green]",
                style="white on blue"
            ))
        
        return codigo

    def confirmar_email(self, codigo_usuario):
        if not self.dados.get('codigo_verificacao'):
            return False
            
        if str(codigo_usuario).strip() == str(self.dados['codigo_verificacao']):
            self.dados['email_verificado'] = True
            self.dados['codigo_verificacao'] = None 
            self.salvar()
            return True
        return False
    def adicionar_avaliacao_entidade(self, autor_nome, nota, comentario):
        """Adiciona uma avaliação e recalcula a média."""
        nova_avaliacao = {
            "autor": autor_nome,
            "nota": float(nota),
            "comentario": comentario,
            "data": datetime.now().strftime("%d/%m/%Y")
        }
        self.dados['avaliacoes'].insert(0, nova_avaliacao)
        
        # Recalcular média
        total_notas = sum(a['nota'] for a in self.dados['avaliacoes'])
        self.dados['nota_media'] = total_notas / len(self.dados['avaliacoes'])
        
        self.salvar()

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
        self.dados.setdefault('transparencia', [])
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

    def registrar_alocacao_doacao(self, valor: float, descricao: str, data: str):
        """Método POO para criar e adicionar um novo registro de alocação de doação."""
        registro = {
            "valor": valor,
            "descricao": descricao,
            "data": data
        }
        
        self.dados['transparencia'].insert(0, registro)

    def obter_relatorio_transparencia(self):
        """Retorna a lista de registros de transparência para exibição."""
        return self.dados.get('transparencia', [])
    