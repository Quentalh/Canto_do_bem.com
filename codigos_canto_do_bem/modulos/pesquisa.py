import os
import sys

CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()

class Usuario_encontrado:
    def __init__ (self, nome, email, cidade, estado):
        self.nome = nome
        self.email = email
        self.cidade = cidade
        self.estado = estado
    def exibir(self):
        return console.print(f"Nome: {self.nome}\nEmail: {self.email}\nLocal: {self.cidade} - {self.estado}")

class Ong_encontrada:
    def __init__(self, nome, email, logradouro, bairro, cidade, estado, cep):
        self.nome = nome
        self.email = email
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
    def exibir(self):
        return console.print(f"Nome: {self.nome}\nEmail: {self.email}\nLocal: {self.logradouro} - {self.bairro} - {self.cidade} - {self.estado}\nCEP: {self.cep}")



def listar_estados_unicos():
    dados = carregar_dados()
    estados = set()
    
    for entidade in dados.get("usuarios", []) + dados.get("ongs", []):
        estado = entidade.get("estado")
        if estado:
            estados.add(estado)
            
    return (list(estados))

def listar_cidades_unicas_por_estado(estado_escolhido):
    dados = carregar_dados()
    cidades = set()
    
    for entidade in dados.get("usuarios", []) + dados.get("ongs", []):
        if entidade.get("estado") == estado_escolhido:
            cidade = entidade.get("cidade")
            if cidade:
                cidades.add(cidade)
                
    return (list(cidades))

def listar_entidades_por_local(estado, cidade):
    dados = carregar_dados()
    entidades_encontradas = {
        "usuarios": [],
        "ongs": []
    }

    for usuario in dados.get("usuarios", []):
        if usuario.get("estado") == estado and usuario.get("cidade") == cidade:
            entidades_encontradas["usuarios"].append(usuario)
    
    for ong in dados.get("ongs", []):
        if ong.get("estado") == estado and ong.get("cidade") == cidade:
            entidades_encontradas["ongs"].append(ong)
            
    return entidades_encontradas


def pesquisa_local():
    console.print(Panel("Pesquisa por Localização", style="bold cyan"))

    estados_disponiveis = listar_estados_unicos()
    while True:
        if not estados_disponiveis:
            console.print("[bold yellow]Nenhum estado encontrado no cadastro de usuários ou ONGs.[/bold yellow]")

        console.print("\n[bold]Passo 1: Escolha o Estado[/bold]")
        for idx, estado in enumerate(estados_disponiveis, 1):
            console.print(f"{idx}. {estado}")

        try:
            escolha_estado_idx = int(input("\nDigite o número do estado: ").strip())
            if not (1 <= escolha_estado_idx <= len(estados_disponiveis)):
                console.print("[bold red]Número inválido.[/bold red]")
                return

            estado_selecionado = estados_disponiveis[escolha_estado_idx - 1]

        except ValueError:
            console.print("[bold red]Entrada inválida. Por favor, use um número.[/bold red]")
            return

        cidades_disponiveis = listar_cidades_unicas_por_estado(estado_selecionado)

        console.print(f"\n[bold]Passo 2: Escolha a Cidade em {estado_selecionado}[/bold]")
        for idx, cidade in enumerate(cidades_disponiveis, 1):
            console.print(f"{idx}. {cidade}")

        try:
            escolha_cidade_idx = int(input("\nDigite o número da cidade: ").strip())
            if not (1 <= escolha_cidade_idx <= len(cidades_disponiveis)):
                console.print("[bold red]Número inválido.[/bold red]")
                return

            cidade_selecionada = cidades_disponiveis[escolha_cidade_idx - 1]

        except ValueError:
            console.print("[bold red]Entrada inválida. Por favor, use um número.[/bold red]")
            return
        
        console.print(f"\n--- Resultados para [bold green]{cidade_selecionada}, {estado_selecionado}[/bold green] ---")

        resultados = listar_entidades_por_local(estado_selecionado, cidade_selecionada)

        while True:
            try:
                console.print("Digite qual o tipo de usuário você deseja encontrar: \n\n1- Usuário comum \n2- ONG")
                escolha_tipo = int(input("Digite o numero correspondente a uma das opções: "))
                if escolha_tipo == 1:
                    console.print("\n[bold cyan]Usuários encontrados:[/bold cyan]")
                    for idx, usuario in enumerate(resultados["usuarios"], 1):
                        console.print(f"{idx} - {usuario['nome']} (Email: {usuario['email']})")
                    try:
                        escolha = int(input("Digite o número do usuário para ver mais informações: "))
                        if 1 <= escolha <= len(resultados["usuarios"]):
                            usuario_escolhido = resultados["usuarios"][escolha - 1]
                            usuario_exibir = Usuario_encontrado(usuario_escolhido.get("nome"), usuario_escolhido.get("email"), usuario_escolhido.get("cidade"), usuario_escolhido.get("estado"))
                            console.print(f"[bold green]Usuário encontrado![/bold green]")
                            usuario_exibir.exibir()
                            return
                        else:
                            console.print("[bold red]Número inválido.[/bold red]")
                    except ValueError:
                        console.print("[bold red]Entrada inválida.[/bold red]")
                    break

                elif escolha_tipo == 2:
                    console.print("\n[bold cyan]ONGs encontradas:[/bold cyan]")
                    for idx, ong in enumerate(resultados["ongs"], 1):
                        console.print(f"{idx} - {ong['nome']} (Email: {ong['email']})")
                    try:
                        escolha = int(input("Digite o número da ONG para ver mais informações: "))
                        if 1 <= escolha <= len(resultados["ongs"]):
                            ong_escolhida = resultados["ongs"][escolha - 1]
                            ong_exibir = Ong_encontrada(ong_escolhida.get("nome"), ong_escolhida.get("email"), ong_escolhida.get("logradouro"), ong_escolhida.get("bairro"), ong_escolhida.get("cidade"), ong_escolhida.get("estado"), ong_escolhida.get("cep"))
                            console.print(f"[bold green]ONG encontrada![/bold green]")
                            ong_exibir.exibir()
                            return
                        else:
                            console.print("[bold red]Número inválido.[/bold red]")
                    except ValueError:
                        console.print("[bold red]Entrada inválida.[/bold red]")
                    break
                else:
                    console.print("[bold red]Opção inválida.[/bold red]")
            except ValueError:
                console.print("Opção inválida")
            break

def menu_pesquisa():
    dados = carregar_dados() 

    while True:
        console.print(Panel("Menu de Pesquisa", style="bold cyan"))
        console.print("1- Pesquisar por Nome (Usuário)")
        console.print("2- Pesquisar por Nome (ONG)")
        console.print("3- Pesquisar por Localização (Estado -> Cidade)")
        console.print("4- Voltar ao menu anterior")

        try:
            opcao = int(input("\nEscolha uma opção: ").strip())
            
            if opcao == 1:
                console.print(Panel("Pesquisa de Usuário por Nome/Email", style="bold cyan" ))
                nome = input("\nNome do usuário: ").strip()
                email = input("\nE-mail do usuário: ").strip()
                
                usuariop = next((u for u in dados["usuarios"] if u["email"] == email and u["nome"] == nome), None)
                
                if usuariop:
                        usuario_exibir = Usuario_encontrado(usuariop.get("nome"), usuariop.get("email"), usuariop.get("cidade"), usuariop.get("estado"))
                        console.print(f"[bold green]Usuário encontrado![/bold green]")
                        usuario_exibir.exibir()
                else: 
                    console.print('\n[bold red]Nenhum usuário encontrado[/bold red]\n')

            elif opcao == 2:
                console.print(Panel("Pesquisa de ONG por Nome/Email", style="bold cyan" ))
                nome = input("\nNome da ONG: ").strip()
                email = input("\nE-mail público da ONG: ").strip()

                ongp = next((o for o in dados["ongs"] if o["email"] == email and o["nome"] == nome), None)
                
                if ongp:
                        ong_exibir = Ong_encontrada(ongp.get("nome"), ongp.get("email"), ongp.get("logradouro"), ongp.get("bairro"), ongp.get("cidade"), ongp.get("estado"), ongp.get("cep"))
                        console.print(f"[bold green]ONG encontrada![/bold green]")
                        ong_exibir.exibir()
                else: 
                    console.print('\n[bold red]Nenhuma ONG encontrada[/bold red]\n')
            
            elif opcao == 3:
                pesquisa_local()
            
            elif opcao == 4:
                break
            
            else:
                console.print("[bold red]Opção inválida.[/bold red]")
        
        except ValueError:
            console.print("[bold red]Entrada inválida. Por favor, digite um número (1-4).[/bold red]")

if __name__ == "__main__":
    opcao = int(input("Qual função vc quer testar? \n1-listar_estados_unicos \n2-pesquisa_local \n3-menu_pesquisa"))
    try:
        if opcao == 1:
            listar_estados_unicos()
        elif opcao == 2:
            pesquisa_local()
        elif opcao == 3:
            menu_pesquisa()
    except ValueError:
            console.print("Opção invalida")