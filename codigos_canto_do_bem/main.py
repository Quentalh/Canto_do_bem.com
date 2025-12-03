from rich.console import Console
from rich.panel import Panel
from datetime import datetime
import locale

from modulos.classes import Usuario, ONG
from modulos.cadastro import cadastrar_usuario, cadastrar_ong
from modulos.login import login
from modulos.eventos import criar_evento
from modulos.perfil import editar_perfil
from modulos.calendario import ver_calendario, adicionar_evento_calendario
from modulos.pesquisa import menu_pesquisa
from modulos.sistema_de_pontos import checkar_presenca, LojaDePontos
from modulos.rankings import menu_rankings, atualizar_rankings_sistema
from modulos.avaliacoes import avaliar_ongs_pendentes
from modulos.transparencia import menu_gerenciar_transparencia

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR')
    except:
        locale.setlocale(locale.LC_ALL, '')

console = Console()
ano_passado = datetime.now().year - 1

def menu_principal():
    while True:
        console.clear()
        console.print(Panel("🌍 [bold cyan]Canto do Bem - Sistema de Voluntariado[/bold cyan]", expand=False))
        console.print("1 - Cadastrar Usuário\n2 - Cadastrar ONG\n3 - Login\n4 - Sair")
        
        opcao = input("\nOpção: ").strip()

        if opcao == "1": 
            cadastrar_usuario()
            input("Pressione Enter para continuar...")
        elif opcao == "2": 
            cadastrar_ong()
            input("Pressione Enter para continuar...")
        elif opcao == "3":
            entidade_logada = login()
            
            if entidade_logada:
                if entidade_logada.tipo == 'usuario':
                    bonus = entidade_logada.processar_recompensas_anuais(ano_passado)
                    
                    if bonus > 0:
                        console.print(f"[bold green]Parabéns! Recebeu {bonus} pontos de bónus do ano passado![/bold green]")
                        input("Pressione Enter para continuar...")
                    
                    menu_usuario(entidade_logada)
                    
                elif entidade_logada.tipo == 'ong':
                    menu_ong(entidade_logada)
            else:
                console.print("Verificação falhou e login não pode ser concluido")
        elif opcao == "4": 
            console.clear()
            break
        else: 
            console.print("[bold red]Inválido![/bold red]")
            input("Pressione Enter para continuar...")

def menu_usuario(user):
    user.verificar_lembretes_agenda()
    
    while True:
        console.clear()
        qtd_novas = len([n for n in user.dados.get('notificacoes', []) if not n['lida']])
        aviso_notif = f" [red]({qtd_novas} novas)[/red]" if qtd_novas > 0 else ""

        console.print(Panel(f"👤 Menu do Usuário - {user.nome}", style="bold cyan"))
        console.print(f"1 - Notificações 🔔{aviso_notif}")
        console.print("2 - Editar Perfil")
        console.print("3 - Ver Calendário Pessoal")
        console.print("4 - Adicionar Evento ao Calendário")
        console.print("5 - Criar Evento (como voluntário)")
        console.print('6 - Pesquisar por um usuário/ONG')
        console.print("7 - Checagem de presença")
        console.print("8 - Loja de pontos")
        console.print("9 - Verificar Rankings")
        console.print("10 - Ver suas Medalhas")
        console.print("11 - Avaliar ONGs (Pendentes)")
        console.print("12 - Sair")

        opt = input("\nOpção: ").strip()

        if opt == "1":
            user.ver_notificacoes()
        elif opt == "2":
            editar_perfil(user.dados)
        elif opt == "3":
            ver_calendario(user.dados)
        elif opt == "4":
            adicionar_evento_calendario(user.dados)
        elif opt == "5":
            criar_evento(user.dados)
            user.adicionar_notificacao("Você criou um evento novo.")
            input("Pressione Enter para continuar...")
        elif opt == "6":
            menu_pesquisa(user.dados)
        elif opt == "7":
            checkar_presenca(user)
        elif opt == "8":
            loja = LojaDePontos(user)
            loja.abrir_loja()
        elif opt == "9":
            menu_rankings(user.dados)
        elif opt == "10": 
            console.clear()
            resumo = user.calcular_medalhas()
            console.print(Panel(f"Medalhas de {user.nome}\n\n"
                                f"Semanais (Total): {resumo['semanais']}\n"
                                f"Mensais (Ouro/Prata/Bronze): {resumo['mensais']}\n"
                                f"Anuais (Ouro/Prata/Bronze): {resumo['anuais']}", style="bold yellow"))
        elif opt == "11":
             avaliar_ongs_pendentes(user.dados)
        elif opt == "12":
            console.clear()
            break
        else:
            console.print("[bold red]Opção inválida![/bold red]")
            input("Pressione Enter...")

def menu_ong(ong):
    while True:
        console.clear()
        console.print(Panel(f"🏢 Menu ONG - {ong.nome}", style="bold cyan"))
        console.print("1 - Criar Evento")
        console.print("2 - Checagem de Presença")
        console.print("3 - Gerenciar Portal de Transparência 📊") 
        console.print("4 - Sair") 
        
        opt = input("\nOpção: ").strip()

        if opt == "1": 
            criar_evento(ong.dados)
            input("Pressione Enter para continuar...")
        elif opt == "2": 
            checkar_presenca(ong)
        elif opt == "3": 
            menu_gerenciar_transparencia(ong.dados)
        elif opt == "4": 
            console.clear()
            break
        else:
            console.print("[bold red]Opção inválida![/bold red]")
            input("Pressione Enter...")

if __name__ == "__main__":
    atualizar_rankings_sistema(ano_passado)
    menu_principal()