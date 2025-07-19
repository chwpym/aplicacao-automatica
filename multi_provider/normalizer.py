import json
import os
from utils.limpeza import remover_palavras_avancado
from utils.config import load_palavras_remover

# Carrega o siglas.json uma vez
SIGLAS_PATH = os.path.join(os.path.dirname(__file__), '..', 'siglas.json')
try:
    with open(SIGLAS_PATH, 'r', encoding='utf-8') as f:
        SIGLAS_MAP = {k.upper(): v.upper() for k, v in json.load(f).items()}
except Exception:
    SIGLAS_MAP = {}

# Carrega o palavras_remover.json uma vez
PALAVRAS_REMOVER = load_palavras_remover()

def aplicar_sigla(valor):
    v = str(valor).strip().upper()
    return SIGLAS_MAP.get(v, v)

def norm_limpo(x, campo):
    val = aplicar_sigla(x) if x is not None else ""
    palavras = PALAVRAS_REMOVER.get(campo, [])
    return remover_palavras_avancado(val, palavras)

def normalize_aplicacao(d):
    def norm_ano(x):
        s = str(x).strip().upper() if x is not None else ""
        return "9999" if s in ("EM DIANTE", "EMDIANTE") else s
    return {
        "montadora": norm_limpo(d.get("montadora", ""), "marca"),
        "modelo": norm_limpo(d.get("modelo", ""), "modelo"),
        "motor": norm_limpo(d.get("motor", ""), "motor"),
        "configuracao_motor": norm_limpo(d.get("configuracao_motor", ""), "configuracao_motor"),
        "ano_inicio": norm_ano(d.get("ano_inicio", "")),
        "ano_fim": norm_ano(d.get("ano_fim", "")),
    } 