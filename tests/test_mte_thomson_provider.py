import sys
import os

# Garante que o Python encontre o pacote 'providers'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from providers.mte_thomson import MteThomsonProvider

if __name__ == "__main__":
    codigo = "4162"  # Substitua por outro código real se quiser testar outro produto
    resultado = MteThomsonProvider.buscar_produto(codigo)
    print("==== Aplicações ====")
    # Bloco antigo (comentado)
    # for app in resultado.get("aplicacoes", []):
    #     print(app)
    # print("\n==== OEMs ====")
    # for oem in resultado.get("oems", []):
    #     print(oem)
    # print("\n==== Atributos ====")
    # for k, v in resultado.get("atributos", {}).items():
    #     print(f"{k}: {v}")
    # print("\n==== Imagens ====")
    # for img in resultado.get("imagens", []):
    #     print(img)
    # print("\n==== Especificações ====")
    # for k, v in resultado.get("especificacoes", {}).items():
    #     print(f"{k}: {v}")
    # print("\n==== Descrição ====")
    # print(resultado.get("descricao", ""))
    # Novo bloco: resultado agora é uma lista
    for app in resultado:
        print(app)