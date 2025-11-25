from rich.console import Console
from rich.panel import Panel
from auxiliares.json_auxiliares import carregar_dados, salvar_dados

console = Console()

def editar_perfil(usuario_logado):
    dados = carregar_dados()

    while True:
        console.clear()
        console.print(Panel(f"Editar Perfil - {usuario_logado['nome']}", style="bold cyan"))
        console.print("\nEscolha o que deseja editar:")
        console.print("1 - Nome")
        console.print("2 - Áreas de interesse")
        console.print("3 - Voltar")
        opcao = input("> ").strip()

        if opcao == "1":
            novo_nome = input("Novo nome: ").strip()
            if novo_nome:
                usuario_logado["nome"] = novo_nome
                console.print("[bold green]Nome atualizado com sucesso![/bold green]")
                input("Pressione Enter...")
            else:
                console.print("[bold red]Nome inválido.[/bold red]")
                input("Pressione Enter...")

        elif opcao == "2":
            console.print("\nDigite suas áreas de interesse separadas por vírgula.")
            console.print("Exemplo: ajudar animais, meio ambiente, educação")
            interesses_input = input("Interesses: ").strip()

            if interesses_input:
                interesses = [i.strip() for i in interesses_input.split(",") if i.strip()]
                usuario_logado["interesses"] = interesses
                console.print("[bold green]Áreas de interesse atualizadas![/bold green]")
                input("Pressione Enter...")
            else:
                console.print("[bold red]Nenhum interesse informado.[/bold red]")
                input("Pressione Enter...")

        elif opcao == "3":
            console.clear()
            break
        else:
            console.print("[bold red]Opção inválida.[/bold red]")
            input("Pressione Enter...")

        for u in dados["usuarios"]:
            if u["email"] == usuario_logado["email"]:
                u.update(usuario_logado)
                break

        salvar_dados(dados)