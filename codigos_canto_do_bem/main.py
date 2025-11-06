from rich.console import Console
from rich.panel import Panel

# Importações dos módulos
from modulos.cadastro import cadastrar_usuario, cadastrar_ong
from modulos.login import login
from modulos.eventos import criar_evento
from modulos.perfil import editar_perfil
from modulos.calendario import ver_calendario, adicionar_evento_calendario
from modulos.pesquisa import menu_pesquisa
from modulos.sistema_de_pontos import checkar_presenca,loja_de_pontos

console = Console()


def menu_principal():
    while True:
        console.print(Panel("🌍 [bold cyan]Canto do Bem - Sistema de Voluntariado[/bold cyan]", expand=False))
        console.print("1 - Cadastrar Usuário")
        console.print("2 - Cadastrar ONG")
        console.print("3 - Fazer Login")
        console.print("4 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            cadastrar_ong()
        elif opcao == "3":
            usuario_logado = login()
            if usuario_logado:
                if usuario_logado["tipo"] == "usuario":
                    menu_usuario(usuario_logado)
                elif usuario_logado["tipo"] == "ong":
                    menu_ong(usuario_logado)
        elif opcao == "4":
            console.print("[bold yellow]Saindo do sistema... Até logo![/bold yellow]")
            break
        else:
            console.print("[bold red]Opção inválida![/bold red]")


def menu_usuario(usuario_logado):
    while True:
        console.print(Panel(f"👤 Menu do Usuário - {usuario_logado['nome']}", style="bold cyan"))
        console.print("1 - Editar Perfil")
        console.print("2 - Ver Calendário Pessoal")
        console.print("3 - Adicionar Evento ao Calendário")
        console.print("4 - Criar Evento (como voluntário)")
        console.print('5 - Pesquisar por um usuário/ONG')
        console.print("6 - Checagem de presença")
        console.print("7 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            editar_perfil(usuario_logado)
        elif opcao == "2":
            ver_calendario(usuario_logado)
        elif opcao == "3":
            adicionar_evento_calendario(usuario_logado)
        elif opcao == "4":
            criar_evento(usuario_logado)
        elif opcao == "5":
            menu_pesquisa()
        elif opcao == "6":
            checkar_presenca(usuario_logado)
        elif opcao == "7":
            loja_de_pontos(usuario_logado)
        elif opcao == '8':
            console.print('Sair')
            break
        else:
            console.print("[bold red]Opção inválida![/bold red]")


def menu_ong(ong_logada):
    while True:
        console.print(Panel(f"🏢 Menu da ONG - {ong_logada['nome']}", style="bold cyan"))
        console.print("1 - Criar Evento/Voluntariado")
        console.print("2 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            criar_evento(ong_logada)
        elif opcao == "2":
            console.print("[bold yellow]Voltando ao menu principal...[/bold yellow]")
            break
        else:
            console.print("[bold red]Opção inválida![/bold red]")


if __name__ == "__main__":
    menu_principal()