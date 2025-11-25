from rich.console import Console
from rich.panel import Panel
from auxiliares.json_auxiliares import carregar_dados, salvar_dados
import uuid
import datetime

console = Console()


class TransparenciaEntry:
    def __init__(self, categoria, valor, descricao, destino="", data=None, id=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.data = data or datetime.date.today().strftime("%d/%m/%Y")
        # normaliza tipo
        self.categoria = categoria.strip()
        try:
            self.valor = float(valor)
        except Exception:
            self.valor = 0.0
        self.descricao = descricao.strip()
        self.destino = destino.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "categoria": self.categoria,
            "valor": self.valor,
            "descricao": self.descricao,
            "destino": self.destino,
        }


class PortalTransparencia:
    """Portal de transparência para uma ONG.

    Usa o JSON central via `carregar_dados`/`salvar_dados`. A ONG passada é um dicionário lido do JSON;
    para persistir, o portal busca a ONG pelo e-mail no JSON e atualiza o campo `transparencia`.
    """

    def __init__(self, ong_dict):
        self.console = console
        self.ong = ong_dict

    def _encontrar_ong_no_banco(self, dados):
        """Retorna tupla (indice, ong_dict) ou (None, None) se não encontrar."""
        for idx, o in enumerate(dados.get("ongs", [])):
            if o.get("email") == self.ong.get("email"):
                return idx, o
        return None, None

    def _garantir_campo(self, dados, idx):
        if "transparencia" not in dados["ongs"][idx]:
            dados["ongs"][idx]["transparencia"] = []

    def add_entry(self, categoria, valor, descricao, destino="", data=None):
        dados = carregar_dados()
        idx, _ = self._encontrar_ong_no_banco(dados)
        if idx is None:
            self.console.print("[bold red]ONG não encontrada no banco de dados. Salve a ONG antes de usar o portal de transparência.[/bold red]")
            return False

        self._garantir_campo(dados, idx)
        entry = TransparenciaEntry(categoria, valor, descricao, destino=destino, data=data)
        dados["ongs"][idx]["transparencia"].append(entry.to_dict())
        salvar_dados(dados)
        self.console.print(f"[bold green]Entrada de transparência adicionada (id: {entry.id})[/bold green]")
        # atualiza objeto local também
        self.ong = dados["ongs"][idx]
        return True

    def listar_entries(self):
        dados = carregar_dados()
        idx, ong_db = self._encontrar_ong_no_banco(dados)
        if idx is None:
            self.console.print("[bold red]ONG não encontrada no banco de dados.[/bold red]")
            return []

        transparencia = ong_db.get("transparencia", [])
        if not transparencia:
            self.console.print(Panel("Nenhuma destinação registrada ainda.", title=f"Transparência - {ong_db.get('nome')}", style="bold cyan"))
            return []

        self.console.print(Panel(f"Transparências registradas - {ong_db.get('nome')}", style="bold cyan"))
        for idx_e, e in enumerate(transparencia, 1):
            self.console.print(f"{idx_e}. [{e.get('data')}] {e.get('categoria')} - R$ {e.get('valor'):.2f} -> {e.get('destino')}")
            self.console.print(f"    {e.get('descricao')} (id: {e.get('id')})")

        return transparencia

    def menu(self):
        while True:
            self.console.print(Panel(f"Portal de Transparência - {self.ong.get('nome')}", style="bold cyan"))
            self.console.print("1 - Listar destinações")
            self.console.print("2 - Adicionar destinação")
            self.console.print("3 - Voltar")

            opcao = input("\nEscolha uma opção: ").strip()
            if opcao == "1":
                self.listar_entries()
                input("\nPressione ENTER para voltar...")
            elif opcao == "2":
                categoria = input("Categoria (ex: projetos, administração, infraestrutura): ").strip()
                valor = input("Valor (use ponto para decimais): R$").strip()
                descricao = input("Descrição breve da destinação: ").strip()
                destino = input("Destino/Beneficiário (opcional): ").strip()
                sucesso = self.add_entry(categoria, valor, descricao, destino=destino)
                if sucesso:
                    input("\nRegistro salvo. Pressione ENTER para continuar...")
            elif opcao == "3":
                break
            else:
                self.console.print("[bold red]Opção inválida.[/bold red]")
