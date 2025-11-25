from auxiliares.json_auxiliares import carregar_dados
from modulos.transparencia import PortalTransparencia


def main():
    dados = carregar_dados()
    # tenta encontrar a ONG de exemplo
    ong = next((o for o in dados.get("ongs", []) if o.get("nome") == "ONG Esperança"), None)
    if not ong:
        print("ONG 'ONG Esperança' não encontrada no banco de dados. Rode o cadastro primeiro.")
        return

    portal = PortalTransparencia(ong)
    # adiciona uma entrada de teste
    sucesso = portal.add_entry("projetos sociais", 1500.50, "Compra de materiais escolares", destino="Crianças da comunidade")
    if sucesso:
        print("Entrada adicionada com sucesso. Listando entradas:")
        portal.listar_entries()


if __name__ == "__main__":
    main()
