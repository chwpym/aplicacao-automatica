# Funções de configuração serão movidas para cá 

import sys
import os
import json
import re
from tkinter import messagebox

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# Exemplo de uso:
provedores_path = resource_path("provedores.json")
siglas_path = resource_path("siglas.json")
palavras_remover_path = resource_path("palavras_remover.json")

# --- Utilitários de configuração e dados ---
def load_siglas(SIGLAS_FILE="siglas.json"):
    if os.path.exists(SIGLAS_FILE):
        try:
            with open(SIGLAS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showwarning("Erro de Leitura", f"Arquivo '{SIGLAS_FILE}' está corrompido ou vazio. Criando um novo.")
            return {}
    return {}

def save_siglas(siglas_data, SIGLAS_FILE="siglas.json"):
    with open(SIGLAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(siglas_data, f, indent=4, ensure_ascii=False)

PALAVRAS_REMOVER_FILE = "palavras_remover.json"
def load_palavras_remover(filename=PALAVRAS_REMOVER_FILE):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showwarning("Erro de Leitura", f"Arquivo '{filename}' está corrompido ou vazio. Criando um novo.")
            return {}
    return {}

def save_palavras_remover(data, filename=PALAVRAS_REMOVER_FILE):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

PROVEDORES_FILE = "provedores.json"
def load_provedores(filename=PROVEDORES_FILE):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showwarning("Erro de Leitura", f"Arquivo '{filename}' está corrompido ou vazio. Criando um novo.")
            return {}
    return {}

def save_provedores(provedores_data, filename=PROVEDORES_FILE):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(provedores_data, f, indent=4, ensure_ascii=False)

# --- Utilitário para intervalos de anos ---
def merge_year_ranges_overall(ranges):
    if not ranges:
        return None, None
    processed_ranges = []
    for s, e in ranges:
        start_val = s if s is not None else 0
        end_val = e if e is not None else 9999
        processed_ranges.append((start_val, end_val))
    if not processed_ranges:
        return None, None
    sorted_ranges = sorted(processed_ranges, key=lambda x: x[0])
    overall_min_start = sorted_ranges[0][0]
    overall_max_end = sorted_ranges[0][1]
    for i in range(1, len(sorted_ranges)):
        next_start, next_end = sorted_ranges[i]
        if next_start <= overall_max_end + 1:
            overall_max_end = max(overall_max_end, next_end)
        else:
            overall_max_end = max(overall_max_end, next_end)
    final_min_start = overall_min_start if overall_min_start != 0 else None
    final_max_end = overall_max_end if overall_max_end != 9999 else None
    return final_min_start, final_max_end 

    # --- NOVO: Funções auxiliares para parsing de ano ---
def parse_ano_inicio(ano_str):
    # Exemplo: "97 -- 99" ou "2007 -->"
    if not ano_str:
        return None
    anos = re.findall(r'\d{2,4}', ano_str)
    if not anos:
        return None
    ano_ini = int(anos[0])
    if len(anos[0]) == 2:
        ano_ini = 2000 + int(anos[0]) if int(anos[0]) < 50 else 1900 + int(anos[0])
    return ano_ini

def parse_ano_fim(ano_str):
    if not ano_str:
        return None
    anos = re.findall(r'\d{2,4}', ano_str)
    if not anos:
        return None
    ano_fim = int(anos[-1])
    if len(anos[-1]) == 2:
        ano_fim = 2000 + int(anos[-1]) if int(anos[-1]) < 50 else 1900 + int(anos[-1])
    return ano_fim

def exibir_ano(ano):
    """Exibe 'EM DIANTE' se ano for 9999, senão retorna o ano como string."""
    return "EM DIANTE" if str(ano) == "9999" else str(ano)