import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from providers.iguacu import IguacuProvider

if __name__ == "__main__":
    codigo = "206.9006"  # Use um código real para teste
    resultados = IguacuProvider.buscar_produto(codigo)
    print("Resultados encontrados:")
    for item in resultados:
        print(item)
    if not resultados:
        print("Nenhum resultado encontrado para o código:", codigo)