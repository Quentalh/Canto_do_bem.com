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
hoje = date.today()

class Produto:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

class LojaDePontos:
    def __init__(self, usuario_obj):
        self.usuario = usuario_obj
        self.catalogos = {
            1: {
                "nome": "Nossos Produtos",
                "itens": [
                    Produto("Ecopen", 10), Produto("Ecobag", 15), 
                    Produto("Camisa", 17), Produto("Caneca", 12), Produto("Garrafa", 15)
                ]
            },
            2: {
                "nome": "Cupons de Desconto",
                "itens": [
                    Produto("Café", 20), Produto("Almoço", 35), 
                    Produto("Livraria", 40), Produto("Mercado", 30), Produto("Workshop", 35)
                ]
            },
            3: {
                "nome": "Ingressos",
                "itens": [
                    Produto("Teatro", 40), Produto("Cinema", 40), 
                    Produto("Museu", 30), Produto("Parque", 35), 
                    Produto("Show", 45), Produto("Palestra", 25)
                ]
            },
            4: {
                "nome": "Produtos Parceiros",
                "itens": [
                    Produto("Livro", 20), Produto("Comida", 25), 
                    Produto("Manicure", 40), Produto("Sobremesa", 30), 
                    Produto("Arte", 45), Produto("Powerbank", 30)
                ]
            }
        }

    def abrir_loja(self):
        while True:
            console.clear()
            console.print(Panel(
                f"Loja de pontos 💰 \nSeu saldo atual: {self.usuario.pontos} pontos\n"
                f"*Todos os itens oferecidos por empresas parceiras", 
                style="bold cyan"
            ))
            
            for chave, categoria in self.catalogos.items():
                console.print(f"{chave} - {categoria['nome']}")
            console.print("5 - Sair")

            try:
                opcao = int(input("\nEscolha uma opção: "))
                
                if opcao == 5:
                    console.clear()
                    return
                elif opcao in self.catalogos:
                    self.exibir_e_comprar(self.catalogos[opcao])
                else:
                    console.print("[bold red]Opção inválida[/bold red]")
                    input("Pressione Enter...")

            except ValueError:
                console.print("[bold red]Apenas dígitos são aceitos.[/bold red]")
                input("Pressione Enter...")

    def exibir_e_comprar(self, categoria):
        itens = categoria["itens"]
        nome_categoria = categoria["nome"]

        while True:
            console.clear()
            console.print(Panel(f"Categoria: {nome_categoria}", style="bold magenta"))
            for idx, produto in enumerate(itens, 1):
                console.print(f"{idx}. {produto.nome} - $ {produto.valor}")
            console.print(f"{len(itens) + 1}. Voltar")

            try:
                escolha = int(input("\nEscolha um item: "))
                
                if escolha == len(itens) + 1:
                    console.clear()
                    return 

                if 1 <= escolha <= len(itens):
                    produto_escolhido = itens[escolha - 1]
                    self.processar_transacao(produto_escolhido)
                else:
                    console.print("[bold red]Opção inválida, tente novamente.[/bold red]")
                    input("Pressione Enter...")
            
            except ValueError:
                console.print("[bold red]Valor inválido (digite um número).[/bold red]")
                input("Pressione Enter...")

    def processar_transacao(self, produto):
        try:
            qnt = int(input(f"Quantidade de '{produto.nome}': "))
            if qnt <= 0:
                console.print("Quantidade deve ser maior que zero.")
                input("Pressione Enter...")
                return

            custo_total = produto.valor * qnt

            if self.usuario.pontos >= custo_total:
                sucesso = self.usuario.descontar_pontos(custo_total)
                
                if sucesso:
                    self.usuario.adicionar_historico_compra(f"{qnt}x {produto.nome}, custo = {custo_total}")
                    console.print(f"[bold green]Compra realizada com sucesso! Novo saldo: {self.usuario.pontos}[/bold green]")
                    input("Pressione Enter para continuar...")
                    console.clear()
                    return 
            else:
                console.print(f"[bold red]Saldo insuficiente. Você precisa de {custo_total}, mas tem {self.usuario.pontos}.[/bold red]")
                input("Pressione Enter...")
        
        except ValueError:
            console.print("[bold red]Quantidade inválida.[/bold red]")
            input("Pressione Enter...")


def checkar_presenca(usuario_obj):
    while True:
        console.clear()
        eventos_passados = []
        dados = carregar_dados()
        console.print(Panel("Checagem de presença ✔❌", style="bold cyan"))
        console.print("1 - Sair")
        console.print("Eventos disponiveis para checagem: ")
        
        eventos_criados = usuario_obj.dados.get("eventos_criados", [])
        
        if not eventos_criados:
            console.print("[bold yellow]Você não possui nenhum evento criado.[/bold yellow]")
            input("Pressione Enter para voltar...")
            console.clear()
            return

        for eventos in eventos_criados:
            try:
                evento_data = datetime.strptime(eventos['data'], "%d/%m/%Y").date()
                if evento_data < hoje:
                    eventos_passados.append(eventos)
            except (ValueError, KeyError):
                continue

        if not eventos_passados:
            console.print("[bold yellow]Nenhum evento passado encontrado para checagem.[/bold yellow]")
            input("Pressione Enter para voltar...")
            console.clear()
            return

        for idx, eventop in enumerate(eventos_passados, 2):
            console.print(f"{idx}. {eventop['nome']}- {eventop['data']}")
        
        tamanho = len(eventos_passados) + 1
        
        try:
            opcao = int(input("Digite o numero correspondente a um dos eventos. Ou saia pressionando 1: "))

            if opcao == 1:
                console.clear()
                return
                
            elif 2 <= opcao <= tamanho:

                usuarios_presenca = []
                evento_escolhido = eventos_passados[opcao - 2] 
                
                for usuario in dados["usuarios"]:
                    for evento in usuario.get("eventos_marcados", []): 
                        if evento.get('nome') == evento_escolhido.get('nome') and evento.get('data') == evento_escolhido.get('data'):
                            usuarios_presenca.append(usuario)
                
                if not usuarios_presenca:
                    console.print("[bold yellow]Nenhum usuário participou deste evento.[/bold yellow]")
                    input("Pressione Enter para continuar...")
                    continue 

                while True:
                    console.clear()
                    console.print("\n[bold cyan]Usuários para confirmar presença:[/bold cyan]")
                    console.print("0 - Voltar")
                    for idx, presenca in enumerate(usuarios_presenca, 1):
                        console.print(f"{idx}. {presenca['nome']} - {presenca['email']}")
                    
                    try:
                        escolha = int(input("Digite o numero correspondente ao usuário ou 0 para voltar: "))
                        
                        if escolha == 0:
                            break

                        if 1 <= escolha <= len(usuarios_presenca):
                            entregador = usuarios_presenca[escolha - 1]
                            pontos_ganhos = evento_escolhido.get('horas_total', 0)
                                
                            entregador['Pontos'] += pontos_ganhos
                            entregador['Horas_de_servico'] += pontos_ganhos
                            
                            if 'notificacoes' not in entregador:
                                entregador['notificacoes'] = []
                            
                            nova_msg = {
                                "mensagem": f"✅ Presença confirmada em '{evento_escolhido['nome']}'. Você ganhou {pontos_ganhos} pontos!",
                                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                "lida": False
                            }
                            entregador['notificacoes'].insert(0, nova_msg)

                            console.print(f"[bold green]Presença confirmada! {entregador['nome']} ganhou {pontos_ganhos} pontos![/bold green]")
                            input("Pressione Enter para continuar...")

                            for idx, evento_remover in enumerate(entregador['eventos_marcados']):
                                if evento_remover == evento_escolhido:
                                    entregador['historico_eventos'].insert(0, evento_escolhido)
                                    entregador['eventos_marcados'].pop(idx)
                                    break
                            
                            usuarios_presenca.pop(escolha - 1)

                            for u in dados["usuarios"]:
                                if u["email"] == entregador["email"]:
                                    u.update(entregador)

                            if usuario_obj.tipo == "usuario":
                                for i in dados["usuarios"]:
                                    if i["email"] == usuario_obj.email:
                                        i.update(usuario_obj.dados)
                                        
                            if usuario_obj.tipo == "ong":
                                for o in dados["ongs"]:
                                    if o["email"] == usuario_obj.email:
                                        o.update(usuario_obj.dados)

                            salvar_dados(dados)
                            
                            if not usuarios_presenca:
                                console.print("[bold blue]Todos os participantes receberam pontos.[/bold blue]")
                                input("Pressione Enter para voltar...")
                                break

                        else: 
                            console.print("Opção inválida, tente novamente")
                            input("Pressione Enter...")

                    except ValueError: 
                        console.print("Apenas digitos são aceitos, tente novamente")
                        input("Pressione Enter...")

            else: 
                console.print("Opção inválida, digite novamente")
                input("Pressione Enter...")

        except ValueError: 
            console.print("Apenas digitos são aceitos, tente novamente")
            input("Pressione Enter...")