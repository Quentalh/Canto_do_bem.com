import os
import sys
CAMINHO_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CAMINHO_RAIZ not in sys.path:
    sys.path.append(CAMINHO_RAIZ)

from auxiliares.json_auxiliares import carregar_dados,salvar_dados
from rich.console import Console
from rich.panel import Panel
from modulos.transparencia import visualizar_transparencia_ong_publico

console = Console()

class Usuario_encontrado:
    def __init__ (self, nome, email, cidade, estado, dados_completos):
        self.nome = nome
        self.email = email
        self.cidade = cidade
        self.estado = estado
        self.dados = dados_completos

    def exibir(self):
        console.clear()
        # Obtém a nota média, padrão é 0.0 se não existir
        nota = self.dados.get('nota_media', 0.0)
        estrelas = "⭐" * int(nota)
        
        console.print(f"Nome: {self.nome}")
        console.print(f"Email: {self.email}")
        console.print(f"Local: {self.cidade} - {self.estado}")
        console.print(f"Nota: {nota:.1f} {estrelas}")
        
        console.print("\n1 - Ver Avaliações recebidas")
        console.print("2 - Voltar")
        
        opt = input("Opção: ").strip()
        if opt == "1":
            self.listar_avaliacoes()

    def listar_avaliacoes(self):
        console.clear()
        console.print(Panel(f"Avaliações de {self.nome}", style="bold yellow"))
        avaliacoes = self.dados.get('avaliacoes', [])
        
        if not avaliacoes:
            console.print("Nenhuma avaliação ainda.")
        else:
            for av in avaliacoes:
                console.print(Panel(
                    f"[bold]{av['autor']}[/bold] - Nota: {av['nota']} ⭐\n"
                    f"\"{av['comentario']}\"",
                    title=av.get('data', '')
                ))
        input("\nEnter para voltar...")

class Ong_encontrada:
    def __init__(self, nome, email, logradouro, bairro, cidade, estado, cep, dados_completos):
        self.nome = nome
        self.email = email
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.doacoes = 0
        self.dados = dados_completos

    def exibir(self):
        console.clear()
        nota = self.dados.get('nota_media', 0.0)
        estrelas = "⭐" * int(nota)
        
        console.print(f"Nome: {self.nome} {estrelas} ({nota:.1f})")
        console.print(f"Email: {self.email}")
        console.print(f"Local: {self.logradouro} - {self.bairro} - {self.cidade} - {self.estado}")
        console.print(f"CEP: {self.cep}")
        
        console.print("\n1 - Detalhes/Voltar")
        console.print("2 - Ver Avaliações")
        
        opt = input("Opção: ").strip()
        if opt == "2":
            self.listar_avaliacoes()

    def listar_avaliacoes(self):
        console.clear()
        console.print(Panel(f"Avaliações de {self.nome}", style="bold yellow"))
        avaliacoes = self.dados.get('avaliacoes', [])
        
        if not avaliacoes:
            console.print("Nenhuma avaliação ainda.")
        else:
            for av in avaliacoes:
                console.print(Panel(
                    f"[bold]{av['autor']}[/bold] (Evento: {av.get('evento', 'Geral')}) - Nota: {av['nota']} ⭐\n"
                    f"\"{av['comentario']}\"",
                    title=av.get('data', '')
                ))
        input("\nEnter para voltar...")

    def doar(self,usuario_logado):
        console.print(f"Seus Pontos: {usuario_logado['Pontos']}")
        console.print("[bold yellow]Lembrete: 1 Ponto = R$ 0,50 [/bold yellow]")
        while True:
            try:    
                qnt = int(input(f"Quantos pontos doar para {self.nome}? (Letra para voltar): "))
                if usuario_logado['Pontos'] >= qnt:
                    usuario_logado['Pontos'] -= qnt
                    self.doacoes = qnt / 2
                    console.print(f"[bold green]Parabéns! você doou {qnt} pontos para {self.nome}[/bold green]")
                    input("Enter...")
                    return
                else:
                    console.print("Pontos insuficientes.")
            except ValueError:
                return

def listar_estados_unicos():
    dados = carregar_dados()
    estados = set()
    for entidade in dados.get("usuarios", []) + dados.get("ongs", []):
        if entidade.get("estado"): estados.add(entidade.get("estado"))
    return list(estados)

def listar_cidades_unicas_por_estado(estado_escolhido):
    dados = carregar_dados()
    cidades = set()
    for entidade in dados.get("usuarios", []) + dados.get("ongs", []):
        if entidade.get("estado") == estado_escolhido and entidade.get("cidade"):
            cidades.add(entidade.get("cidade"))
    return list(cidades)

def listar_entidades_por_local(estado, cidade):
    dados = carregar_dados()
    entidades = {"usuarios": [], "ongs": []}
    for u in dados.get("usuarios", []):
        if u.get("estado") == estado and u.get("cidade") == cidade: entidades["usuarios"].append(u)
    for o in dados.get("ongs", []):
        if o.get("estado") == estado and o.get("cidade") == cidade: entidades["ongs"].append(o)
    return entidades

def pesquisa_local(usuario_logado):
    dados = carregar_dados()
    
    estados = listar_estados_unicos()
    while True:
        console.clear()
        console.print(Panel("Pesquisa por Localização", style="bold cyan"))
        if not estados:
            console.print("Nenhum estado encontrado.")
            input("Enter...")
            return

        console.print("Passo 1: Escolha o Estado")
        for idx, estado in enumerate(estados, 1): console.print(f"{idx}. {estado}")
        
        try:
            idx = int(input("\nNúmero do estado (0 sair): ").strip())
            if idx == 0: return
            if not (1 <= idx <= len(estados)): continue
            estado_sel = estados[idx - 1]
        except ValueError: continue

        cidades = listar_cidades_unicas_por_estado(estado_sel)
        console.clear()
        console.print(f"Passo 2: Escolha a Cidade em {estado_sel}")
        for idx, cidade in enumerate(cidades, 1): console.print(f"{idx}. {cidade}")

        try:
            idx = int(input("\nNúmero da cidade: ").strip())
            if not (1 <= idx <= len(cidades)): continue
            cidade_sel = cidades[idx - 1]
        except ValueError: continue
        
        while True:
            console.clear()
            resultados = listar_entidades_por_local(estado_sel, cidade_sel)
            console.print(f"--- {cidade_sel}, {estado_sel} ---")
            console.print("1- Usuário comum \n2- ONG \n3- Voltar")
            try:
                tipo = int(input("Opção: "))
                if tipo == 3: break
                
                if tipo == 1:
                    console.clear()
                    for i, u in enumerate(resultados["usuarios"], 1):
                        console.print(f"{i} - {u['nome']} ({u['email']})")
                    sel = int(input("Ver info de nº (0 voltar): "))
                    if 1 <= sel <= len(resultados["usuarios"]):
                        u_sel = resultados["usuarios"][sel-1]
                        # AQUI ESTAVA O ERRO 1: Adicionado u_sel no final
                        Usuario_encontrado(u_sel["nome"], u_sel["email"], u_sel["cidade"], u_sel["estado"], u_sel).exibir()

                elif tipo == 2:
                    console.clear()
                    for i, o in enumerate(resultados["ongs"], 1):
                        console.print(f"{i} - {o['nome']} ({o['email']})")
                    sel = int(input("Ver info de nº (0 voltar): "))
                    if 1 <= sel <= len(resultados["ongs"]):
                        o_sel = resultados["ongs"][sel-1]
                        # AQUI ESTAVA O ERRO 2: Adicionado o_sel no final
                        ong_obj = Ong_encontrada(o_sel["nome"], o_sel["email"], o_sel["logradouro"], o_sel["bairro"], o_sel["cidade"], o_sel["estado"], o_sel["cep"], o_sel)
                        
                        console.clear()
                        # A classe Ong_encontrada agora tem o menu de avaliações, mas mantemos o menu de ações aqui
                        console.print("1 - Detalhes e Avaliações\n2 - Doar\n3 - Voltar")
                        acao = int(input("Opção: "))
                        if acao == 1: ong_obj.exibir()
                        elif acao == 2:
                            ong_obj.doar(usuario_logado)
                            # Atualiza dados globais após doação
                            for o_global in dados["ongs"]:
                                if o_global["email"] == o_sel["email"]:
                                    o_global['doacoes_recebidas'] = ong_obj.doacoes
                            for u_global in dados["usuarios"]:
                                if u_global["email"] == usuario_logado["email"]:
                                    u_global.update(usuario_logado)
                            salvar_dados(dados)

            except ValueError: pass

def menu_pesquisa(usuario_logado):
    dados = carregar_dados() 
    while True:
        console.clear()
        console.print(Panel("Menu de Pesquisa", style="bold cyan"))
        console.print("1- Pesquisar por Nome (Usuário)")
        console.print("2- Pesquisar por Nome (ONG)")
        console.print("3- Pesquisar por Localização")
        console.print("4- Voltar")

        try:
            opcao = int(input("\nOpção: ").strip())
            
            if opcao == 1:
                console.clear()
                nome = input("Nome: ").strip()
                email = input("Email: ").strip()
                u = next((x for x in dados["usuarios"] if x["email"] == email and x["nome"] == nome), None)
                if u: 
                    
                    Usuario_encontrado(u["nome"], u["email"], u["cidade"], u["estado"], u).exibir()
                else: 
                    console.print("[red]Não encontrado[/red]")
                    input("Enter...")

            elif opcao == 2:
                console.clear()
                nome = input("Nome ONG: ").strip()
                email = input("Email: ").strip()
                o = next((x for x in dados["ongs"] if x["email"] == email and x["nome"] == nome), None)
                if o:
                    ong = Ong_encontrada(o["nome"], o["email"], o["logradouro"], o["bairro"], o["cidade"], o["estado"], o["cep"], o)
                    
                    console.print("1-Exibir/Avaliações 2-Doar 3-Portal de Transparência")
                    
                    sub_opcao = input("Opção: ").strip()
                    
                    if sub_opcao == "1": 
                        ong.exibir()
                    elif sub_opcao == "2":
                        ong.doar(usuario_logado)
                        salvar_dados(dados)
                    elif sub_opcao == "3":
                        
                        visualizar_transparencia_ong_publico(o)
                    else:
                        console.print("[red]Opção inválida.[/red]")
                        input("Enter...")
                else:
                    console.print("[red]Não encontrado[/red]")
                    input("Enter...")
            
            elif opcao == 3: pesquisa_local(usuario_logado)
            elif opcao == 4: break
        
        except ValueError: pass