# Funções de configuração serão movidas para cá 

import os
import json
from tkinter import messagebox

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