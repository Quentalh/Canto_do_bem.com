from rich.console import Console
from rich.panel import Panel
from auxiliares.json_auxiliares import carregar_dados, salvar_dados
from modulos.classes import ONG 

console = Console()

def avaliar_ongs_pendentes(usuario_logado):
    dados = carregar_dados()
    
    while True:
        console.clear()
        console.print(Panel("Avaliar Experiências (ONGs)", style="bold cyan"))
        pendentes = []
        usuario_atualizado = next((u for u in dados['usuarios'] if u['email'] == usuario_logado['email']), usuario_logado)
        
        for evento in usuario_atualizado.get('historico_eventos', []):
            if evento.get('tipo_criador') == 'ong' and evento.get('status_avaliacao') == 'pendente':
                pendentes.append(evento)
        
        if not pendentes:
            console.print("[bold yellow]Você não tem avaliações pendentes no momento.[/bold yellow]")
            input("Pressione Enter para voltar...")
            return

        console.print("Eventos aguardando sua avaliação:")
        for idx, evento in enumerate(pendentes, 1):
            console.print(f"{idx} - {evento['nome']} (ONG: {evento.get('criado_por')}) - Data: {evento['data']}")
        
        console.print("0 - Voltar")
        
        try:
            opcao = int(input("\nEscolha o número do evento para avaliar: "))
            if opcao == 0:
                break
                
            if 1 <= opcao <= len(pendentes):
                evento_selecionado = pendentes[opcao - 1]
                nome_ong = evento_selecionado.get('criado_por')
                ong_alvo = next((o for o in dados['ongs'] if o['nome'] == nome_ong), None)
                
                if ong_alvo:
                    console.print(f"\n[bold]Avaliando a ONG: {nome_ong}[/bold]")
                    while True:
                        try:
                            nota = int(input("Nota (0-5): "))
                            if 0 <= nota <= 5: break
                            console.print("Nota deve ser entre 0 e 5.")
                        except ValueError: pass
                    
                    comentario = input("Comentário (opcional): ").strip()
                    

                    if 'avaliacoes' not in ong_alvo: ong_alvo['avaliacoes'] = []
                    
                    nova_avaliacao = {
                        "autor": usuario_logado['nome'],
                        "evento": evento_selecionado['nome'],
                        "nota": float(nota),
                        "comentario": comentario,
                        "data": evento_selecionado['data']
                    }
                    ong_alvo['avaliacoes'].insert(0, nova_avaliacao)
                    
                    # Recalcular média
                    total = sum(a['nota'] for a in ong_alvo['avaliacoes'])
                    ong_alvo['nota_media'] = total / len(ong_alvo['avaliacoes'])
                    evento_selecionado['status_avaliacao'] = "concluido"
                
                    salvar_dados(dados)
                    console.print("[bold green]Obrigado! Sua avaliação foi registrada.[/bold green]")
                    input("Enter para continuar...")
                else:
                    console.print("[red]Erro: ONG não encontrada no banco de dados.[/red]")
                    input("Enter...")
            else:
                console.print("[red]Opção inválida.[/red]")
        except ValueError:
            console.print("[red]Digite um número válido.[/red]")