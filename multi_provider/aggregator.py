import re
from .schadek_adapter import buscar_aplicacoes_schadek
from .indisa_adapter import buscar_aplicacoes_indisa
from .normalizer import normalize_aplicacao
from .equivalencias import equivalente_motor, equivalente_modelo
from utils.config import merge_year_ranges_overall, exibir_ano

def motor_valido(m):
    m = m.strip()
    return m and re.search(r'[A-Za-z0-9]', m) and m not in {'.', ','}

def buscar_multi_provedores(buscas):
    # buscas: lista de dicts {codigo, provedor}
    resultados = []
    for busca in buscas:
        codigo = busca.get("codigo")
        provedor = busca.get("provedor")
        if not codigo or not provedor:
            continue
        if provedor.lower() == "schadek":
            res = buscar_aplicacoes_schadek(codigo)
        elif provedor.lower() == "indisa":
            res = buscar_aplicacoes_indisa(codigo)
        else:
            res = []
        for r in res:
            r["_provedor"] = provedor  # marca de onde veio
        resultados.extend(res)
    # Unifica por chave normalizada (ignorando configuracao_motor)
    vistos = {}
    for r in resultados:
        norm = normalize_aplicacao(r)
        chave = (
            norm["montadora"],
            norm["modelo"],
            norm["motor"],
            norm["ano_inicio"],
            norm["ano_fim"]
        )
        if chave not in vistos:
            novo = r.copy()
            novo["fontes"] = [r.get("fonte", r.get("_provedor", ""))]
            novo.pop("fonte", None)
            novo.pop("_provedor", None)
            vistos[chave] = novo
        else:
            fonte = r.get("fonte", r.get("_provedor", ""))
            if fonte and fonte not in vistos[chave]["fontes"]:
                vistos[chave]["fontes"].append(fonte)
    return list(vistos.values())

# --- Agrupamento avançado: por montadora, modelo (equivalente), ano, motores equivalentes ---
def agrupar_aplicacoes_por_modelo_ano(resultados):
    grupos = []
    for r in resultados:
        norm = normalize_aplicacao(r)
        # Tenta encontrar grupo existente com modelo e motor equivalentes
        achou = False
        for grupo in grupos:
            g = grupo["_norm"]
            if (
                norm["montadora"] == g["montadora"]
                and equivalente_modelo(norm["modelo"], g["modelo"])
                and equivalente_motor(norm["motor"], g["motor"])
            ):
                grupo["anos"].append((int(norm["ano_inicio"]), int(norm["ano_fim"])) if norm["ano_inicio"].isdigit() and norm["ano_fim"].isdigit() else (norm["ano_inicio"], norm["ano_fim"]))
                grupo["aplicacoes"].append(r)
                achou = True
                break
        if not achou:
            grupo = {
                "montadora": norm["montadora"],
                "modelo": norm["modelo"],
                "motor": norm["motor"],
                "anos": [
                    (int(norm["ano_inicio"]), int(norm["ano_fim"])) if norm["ano_inicio"].isdigit() and norm["ano_fim"].isdigit() else (norm["ano_inicio"], norm["ano_fim"])
                ],
                "aplicacoes": [r],
                "_norm": norm,
            }
            grupos.append(grupo)
    saida = []
    for grupo in grupos:
        menor, maior = merge_year_ranges_overall(grupo["anos"])
        if menor is None or maior is None:
            menor = grupo["anos"][0][0]
            maior = grupo["anos"][0][1]
        motores_unicos = sorted({str(a.get("motor", "")).strip() for a in grupo["aplicacoes"] if a.get("motor")})
        saida.append({
            "montadora": grupo["montadora"],
            "modelo": grupo["modelo"],
            "motores": ", ".join(motores_unicos),
            "ano_inicio": exibir_ano(menor),
            "ano_fim": exibir_ano(maior),
            "observacoes": ", ".join(sorted(set(a.get("observacao", "") for a in grupo["aplicacoes"] if a.get("observacao")))),
            "fontes": ", ".join(sorted(set(a.get("_provedor", "") for a in grupo["aplicacoes"]))),
            "aplicacoes": grupo["aplicacoes"],
        })
    saida.sort(key=lambda x: x["modelo"])
    return saida 