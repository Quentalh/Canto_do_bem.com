from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from datetime import datetime, date

from auxiliares.json_auxiliares import carregar_dados, salvar_dados 
from modulos.classes import ONG 

console = Console()


def menu_gerenciar_transparencia(usuario_logado):
    """Permite à ONG adicionar e visualizar registros de alocação de doações."""
    
    dados = carregar_dados()
    
    dados_ong_atualizados = next((o for o in dados['ongs'] if o['email'] == usuario_logado['email']), None)
    
    if not dados_ong_atualizados:
        console.print("[bold red]Erro: Dados da ONG não encontrados.[/bold red]")
        input("Enter para continuar...")
        return
        
    ong_obj = ONG(dados_ong_atualizados) 
    
    while True:
        console.clear()
        console.print(Panel(f"Portal de Transparência - {ong_obj.nome}", style="bold magenta"))
        
        console.print("1 - Registrar Alocação de Doação (Destinação)")
        console.print("2 - Visualizar Meus Registros")
        console.print("0 - Voltar")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            registrar_alocacao(ong_obj, dados)
            
            usuario_logado.update(ong_obj.dados) 
        elif opcao == '2':
            visualizar_registros_ong(ong_obj)
        elif opcao == '0':
            break
        else:
            console.print("[bold red]Opção inválida.[/bold red]")
            input("Enter para continuar...")

def registrar_alocacao(ong_obj, dados):
    """Lógica para coletar dados e registrar uma nova alocação de doação."""
    console.clear()
    console.print(Panel("Registrar Nova Alocação", style="bold green"))
    
    while True:
        try:
            
            valor = float(input("Valor alocado (R$): ").replace(',', '.'))
            if valor <= 0:
                raise ValueError
            break
        except ValueError:
            console.print("[bold red]Valor inválido. Digite um número positivo.[/bold red]")

    descricao = input("Descrição da alocação (Ex: Compra de ração, Pagamento de aluguel): ").strip()
    
    data_str = date.today().strftime("%d/%m/%Y")
    
    
    
    ong_obj.registrar_alocacao_doacao(valor, descricao, data_str)
    
    
    for i, ong in enumerate(dados['ongs']):
        if ong['email'] == ong_obj.email:
            dados['ongs'][i] = ong_obj.dados 
            break
            
    salvar_dados(dados)
    
    console.print("[bold green]✅ Alocação registrada com sucesso no Portal de Transparência![/bold green]")
    input("Enter para continuar...")

def visualizar_registros_ong(ong_obj):
    """Exibe os registros de transparência da ONG para o próprio gestor."""
    _exibir_registros(ong_obj.nome, ong_obj.obter_relatorio_transparencia(), "bold blue", "blue")


def visualizar_transparencia_ong_publico(ong_dados):
    """Permite ao usuário visualizar os registros de transparência de uma ONG específica."""
    
    ong_obj = ONG(ong_dados)
    
    _exibir_registros(ong_obj.nome, ong_obj.obter_relatorio_transparencia(), "bold cyan", "cyan")


def _exibir_registros(nome_ong, registros, panel_style, table_style):
    """Função auxiliar para exibir a tabela de registros."""
    console.clear()
    console.print(Panel(f"Portal de Transparência de {nome_ong}", style=panel_style))
    
    if not registros:
        console.print(f"[yellow]A ONG {nome_ong} ainda não publicou registros de transparência.[/yellow]")
    else:
        table = Table(title="Detalhamento de Alocações Publicadas", style=table_style)
        table.add_column("Data", style="white", justify="left")
        table.add_column("Descrição", style="white", justify="left")
        table.add_column("Valor (R$)", style="green", justify="right")
        
        total_alocado = 0
        
        for r in registros:
            
            valor_formatado = f"{r['valor']:.2f}".replace('.', ',')
            table.add_row(r['data'], r['descricao'], valor_formatado)
            total_alocado += r['valor']
            
        console.print(table)
        
        total_formatado = f"{total_alocado:.2f}".replace('.', ',')
        console.print(f"\n[bold]Total Alocado Registrado: R$ {total_formatado}[/bold]")
        
    input("\nEnter para continuar...")