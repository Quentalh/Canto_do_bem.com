import sys
import os
CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)
from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from rich.console import Console
from rich.panel import Panel

console = Console()


def validar_email(email):
    """Valida se o e-mail contém '@' e um formato simples"""
    return "@" in email and "." in email


def validar_senha(senha):
    """Verifica se a senha tem pelo menos 6 caracteres,
    uma letra maiúscula, uma minúscula e um número."""
    if len(senha) < 6:
        return False
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    return tem_maiuscula and tem_minuscula and tem_numero


def cadastrar_usuario():
    dados = carregar_dados()
    console.print(Panel("Cadastro de Usuário", style="bold cyan"))

    # valida nome (não pode repetir)
    while True:
        nome = input("Nome: ").strip()
        if any(u["nome"].lower() == nome.lower() for u in dados["usuarios"]):
            console.print("[bold red]Já existe um usuário com esse nome.[/bold red]")
        elif nome == "":
            console.print("[bold red]O nome não pode ser vazio.[/bold red]")
        else:
            break

    # valida e-mail
    while True:
        email = input("E-mail: ").strip()
        if not validar_email(email):
            console.print("[bold red]E-mail inválido! Deve conter '@' e um formato válido.[/bold red]")
        elif any(u["email"] == email for u in dados["usuarios"]):
            console.print("[bold red]E-mail já cadastrado.[/bold red]")
        else:
            break

    # valida senha
    while True:
        senha = input("Senha: ").strip()
        if not validar_senha(senha):
            console.print("[bold red]Senha inválida![/bold red]")
            console.print("A senha deve ter:")
            console.print("- Pelo menos 6 caracteres")
            console.print("- Uma letra maiúscula, uma minúscula e um número")
        else:
            break

    novo_usuario = {
        "tipo": "usuario",
        "nome": nome,
        "email": email,
        "senha": senha,
        "interesses": [],
        "eventos_participando": [] 
    }

    dados["usuarios"].append(novo_usuario)
    salvar_dados(dados)
    console.print("[bold green]Usuário cadastrado com sucesso![/bold green]")


def cadastrar_ong():
    dados = carregar_dados()
    console.print(Panel("Cadastro de ONG", style="bold cyan"))

    # valida nome (não pode repetir)
    while True:
        nome = input("Nome da ONG: ").strip()
        # Verifica na lista de 'ongs'
        if any(o["nome"].lower() == nome.lower() for o in dados["ongs"]):
            console.print("[bold red]Já existe uma ONG com esse nome.[/bold red]")
        elif nome == "":
            console.print("[bold red]O nome não pode ser vazio.[/bold red]")
        else:
            break

    # valida e-mail (Esta era a parte com o erro)
    while True:
        email = input("E-mail: ").strip()
        if not validar_email(email):
            console.print("[bold red]E-mail inválido! Deve conter '@' e um formato válido.[/bold red]")
        # Verifica se o e-mail já existe na lista 'ongs'
        elif any(o["email"] == email for o in dados["ongs"]):
            console.print("[bold red]E-mail já cadastrado.[/bold red]")
        else:
            break # <-- A LINHA QUE FALTAVA!

    # --- RESTANTE DA FUNÇÃO QUE FALTAVA ---

    # valida senha (lógica copiada de 'cadastrar_usuario')
    while True:
        senha = input("Senha: ").strip()
        if not validar_senha(senha):
            console.print("[bold red]Senha inválida![/bold red]")
            console.print("A senha deve ter:")
            console.print("- Pelo menos 6 caracteres")
            console.print("- Uma letra maiúscula, uma minúscula e um número")
        else:
            break
            
    # Pede a descrição (campo específico da ONG)
    descricao = input("Descreva a ONG: ").strip()

    # Cria o novo dicionário da ONG
    nova_ong = {
        "tipo": "ong",
        "nome": nome,
        "email": email,
        "senha": senha,
        "descricao": descricao,
        "eventos_criados": []
    }

    # Adiciona a nova ONG à lista 'ongs' e salva
    dados["ongs"].append(nova_ong)
    salvar_dados(dados)
    console.print("[bold green]ONG cadastrada com sucesso![/bold green]")