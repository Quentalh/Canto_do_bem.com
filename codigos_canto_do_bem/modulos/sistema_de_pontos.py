import os
import sys
from datetime import datetime, date 

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados,salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

hoje = date.today()

class Prod:
    def __init__(self,nome,valor):
        self.nome = nome
        self.valor = valor

def criar_dic(**produto):
    lista = {}
    i = 1
    for chave,valor in produto.items():
        x = Prod(chave,valor)
        lista[f"{i}"] = x
        i = i + 1
    return lista
        

def checkar_presenca(usuario_logado):   
    while True:
        eventos_passados = []
        dados = carregar_dados()
        console.print(Panel("Checagem de presença ✔❌", style="bold cyan"))
        console.print("1 - Sair")
        console.print("Eventos disponiveis para checagem: ")
        
        eventos_criados = usuario_logado.get("eventos_criados", [])
        
        if not eventos_criados:
            console.print("[bold yellow]Você não possui nenhum evento criado.[/bold yellow]")
            input("Pressione Enter para voltar...")
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
            return

        for idx, eventop in enumerate(eventos_passados, 2):
            console.print(f"{idx}. {eventop['nome']}- {eventop['data']}")
        
        tamanho = len(eventos_passados) + 1
        
        try:
            opcao = int(input("Digite o numero correspondente a um dos eventos. Ou saia pressionando 1: "))

            if opcao == 1:
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
                            
                            pontos_ganhos = evento_escolhido.get('horas_total')
                                
                            entregador['Pontos'] += pontos_ganhos

                            entregador['Horas_de_servico'] += pontos_ganhos
                            
                            console.print(f"[bold green]Presença confirmada! {entregador['nome']} ganhou {pontos_ganhos} pontos![/bold green]")

                            for idx,evento_remover in enumerate(entregador['eventos_marcados']):
                                if evento_remover == evento_escolhido:
                                    entregador['historico_eventos'].insert(0,evento_escolhido)
                                    entregador['eventos_marcados'].pop(idx)
                                    break
                            
                            usuarios_presenca.pop(escolha - 1)

                            for u in dados["usuarios"]:
                                if u["email"] == entregador["email"]:
                                    u.update(entregador)

                            if usuario_logado["tipo"] == "usuario":
                                for i in dados["usuarios"]:
                                    if i["email"] == usuario_logado["email"]:
                                        i.update(usuario_logado)
                                        
                            if usuario_logado["tipo"] == "ong":
                                for o in dados["ongs"]:
                                    if o["email"] == usuario_logado["email"]:
                                        o.update(usuario_logado)

                            salvar_dados(dados)
                            
                            if not usuarios_presenca:
                                console.print("[bold blue]Todos os participantes receberam pontos.[/bold blue]")
                                break

                        else: console.print("Opção inválida, tente novamente")

                    except ValueError: console.print("Apenas digitos são aceitos, tente novamente")

            else: console.print("Opção inválida, digite novamente")

        except ValueError: console.print("Apenas digitos são aceitos, tente novamente")


def loja_de_pontos(usuario_logado):
    while True:
        console.print(Panel(f"Loja de pontos 💰 \nSeu número atual dee pontos: {usuario_logado.get('Pontos',0)}\n *Todos os itens oferecidos por empresas parceiras", style = "bold cyan"))
        console.print("1 - Nossos produtos\n2 - Cupons de Descontoz\n3 - Ingressos\n4 - Produtos de nosso parceiros\n5 - Sair")
        try: 
            opcao = int(input("\nEscolha uma opção: "))
            console.clear()

            if opcao == 1: 
                lista_de_produtos(usuario_logado)
            elif opcao == 2:
                lista_de_cupons(usuario_logado)
            elif opcao == 3:
                lista_de_ingressos(usuario_logado)
            elif opcao == 4:
                lista_de_produtos_parceiros(usuario_logado)
            elif opcao == 5:
                return
            else: 
                console.print("Opção inválida")

        except ValueError: console.print("Opção invalida, lembre-se: apenas digitos são aceitos e apenas as opções dee 1 a 5 são aceitas")      

def lista_de_produtos(usuario_logado):
    dados = carregar_dados()
    produtos = criar_dic(Ecopen = 10, Ecobag = 15, Camisa = 17, Caneca = 12, Garrafa = 15)
    for idx,produto in enumerate(produtos,1):
        console.print(f"{idx}. {produtos[f'{produto}'].nome} do bem $ {produtos[f'{produto}'].valor}")
    console.print(f"{idx + 1}. Sair")
    while True:
        try: 
            opcao = int(input("\nEscolha uma opcão: "))
            if opcao == idx + 1:
                return
            if not (1 <= opcao <= len(produtos)):
                console.print("Opção inválida, tente novamente")
            produto_escolhido = produtos[f"{opcao}"]
            while True:
                qnt = int(input("Quantidade: "))
                custo = produto_escolhido.valor * qnt
                if usuario_logado.get("Pontos",0) >= custo:
                    valor_novo = usuario_logado.get('Pontos',0) - custo
                    usuario_logado['Pontos'] = valor_novo
                    usuario_logado['historico_de_compras'].append(f"{qnt}x {produto_escolhido.nome}, custo = {custo}")
                    console.print("[bold green] Compra realizada com sucesso! [/bold green]")
                    for u in dados["usuarios"]:
                        if u["email"] == usuario_logado["email"]:
                            u.update(usuario_logado)
                            break
                    salvar_dados(dados)
                    return
                else:
                    console.print("Você não tem pontos suficientes para realizar essa transação.")
                    break
        except ValueError: console.print("Valor inválido (digite um numero)")
  
    
def lista_de_cupons(usuario_logado):
    dados = carregar_dados()
    cupons = criar_dic(Café = 20, Almoço =35 , Livraria = 40,  Mercado = 30, Workshop = 35)
    for idx,produto in enumerate(cupons,1):
        console.print(f"{idx}. Cupom {cupons[f'{produto}'].nome} $ {cupons[f'{produto}'].valor}")
    console.print(f"{idx + 1}. Sair")
    while True:
        try: 
            opcao = int(input("\nEscolha uma opcão: "))
            if opcao == idx + 1:
                return
            if not (1 <= opcao <= len(cupons)):
                console.print("Opção inválida, tente novamente")
            cupom_escolhido = cupons[f"{opcao}"]
            while True:
                qnt = int(input("Quantidade: "))
                custo = cupom_escolhido.valor * qnt
                if usuario_logado.get("Pontos",0) >= custo:
                    valor_novo = usuario_logado.get('Pontos',0) - custo
                    usuario_logado['Pontos'] = valor_novo
                    usuario_logado['historico_de_compras'].append(f"{qnt}x {cupom_escolhido.nome}, custo = {custo}")
                    console.print("[bold green] Compra realizada com sucesso! [/bold green]")
                    for u in dados["usuarios"]:
                        if u["email"] == usuario_logado["email"]:
                            u.update(usuario_logado)
                            break
                    salvar_dados(dados)
                    return
                else:
                    console.print("Você não tem pontos suficientes para realizar essa transação.")
                    break
        except ValueError: console.print("Valor inválido (digite um numero)")

def lista_de_ingressos(usuario_logado):
    dados = carregar_dados()
    ingressos = criar_dic(Teatro = 40, Cinema = 40 , Museu = 30 ,  Parque = 35, Show = 45, Palestra = 25)
    for idx,produto in enumerate(ingressos,1):
        console.print(f"{idx}. Ingresso {ingressos[f'{produto}'].nome}  $ {ingressos[f'{produto}'].valor}")
    console.print(f"{idx + 1}. Sair")
    while True:
        try: 
            opcao = int(input("\nEscolha uma opcão: "))
            if opcao == idx + 1:
                return
            if not (1 <= opcao <= len(ingressos)):
                console.print("Opção inválida, tente novamente")
            ingresso_escolhido = ingressos[f"{opcao}"]
            while True:
                qnt = int(input("Quantidade: "))
                custo = ingresso_escolhido.valor * qnt
                if usuario_logado.get("Pontos",0) >= custo:
                    valor_novo = usuario_logado.get('Pontos',0) - custo
                    usuario_logado['Pontos'] = valor_novo
                    usuario_logado['historico_de_compras'].append(f"{qnt}x {ingresso_escolhido.nome}, custo = {custo}")
                    console.print("[bold green] Compra realizada com sucesso! [/bold green]")
                    for u in dados["usuarios"]:
                        if u["email"] == usuario_logado["email"]:
                            u.update(usuario_logado)
                            break
                    salvar_dados(dados)
                    return
                else:
                    console.print("Você não tem pontos suficientes para realizar essa transação.")
                    break
        except ValueError: console.print("Valor inválido (digite um numero)")


def lista_de_produtos_parceiros(usuario_logado):
    dados = carregar_dados()
    produtos_par = criar_dic(Livro = 20, Comida = 25 , Manicure = 40 ,  Sobremesa = 30, Arte = 45, Powerbank = 30)
    for idx,produto in enumerate(produtos_par,1):
        console.print(f"{idx}. {produtos_par[f'{produto}'].nome} do bem $ {produtos_par[f'{produto}'].valor}")
    console.print(f"{idx + 1}. Sair")
    while True:
        try: 
            opcao = int(input("\nEscolha uma opcão: "))
            if opcao == idx + 1:
                return
            if not (1 <= opcao <= len(produtos_par)):
                console.print("Opção inválida, tente novamente")
            produto_par_escolhido = produtos_par[f"{opcao}"]
            while True:
                qnt = int(input("Quantidade: "))
                custo = produto_par_escolhido.valor * qnt
                if usuario_logado.get("Pontos",0) >= custo:
                    valor_novo = usuario_logado.get('Pontos',0) - custo
                    usuario_logado['Pontos'] = valor_novo
                    usuario_logado['historico_de_compras'].append(f"{qnt}x {produto_par_escolhido.nome}, custo = {custo}")
                    console.print("[bold green] Compra realizada com sucesso! [/bold green]")
                    for u in dados["usuarios"]:
                        if u["email"] == usuario_logado["email"]:
                            u.update(usuario_logado)
                            break
                    salvar_dados(dados)
                    return
                else:
                    console.print("Você não tem pontos suficientes para realizar essa transação.")
                    break
        except ValueError: console.print("Valor inválido (digite um numero)")