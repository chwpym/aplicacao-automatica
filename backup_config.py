import shutil
import os
from datetime import datetime

# Lista de arquivos importantes para backup
arquivos = [
    "provedores.json",
    "siglas.json",
    "palavras_remover.json"
]

# Pasta de destino do backup
backup_dir = f"bkp_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(backup_dir, exist_ok=True)

for arquivo in arquivos:
    if os.path.exists(arquivo):
        shutil.copy2(arquivo, backup_dir)
        print(f"Backup de {arquivo} realizado em {backup_dir}/")
    else:
        print(f"Arquivo {arquivo} não encontrado.")

print("Backup concluído!") 