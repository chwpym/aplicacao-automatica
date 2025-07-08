import re
from bs4 import BeautifulSoup


# --- PARSERS JSON ---
def parse_wega_json(data):
    """
    Parser específico para o JSON da Wega.
    Use um parser específico quando o formato do provedor for único ou complexo.
    """
    vehicles = []
    detail_apl = data.get("Obj", {}).get("DetailApl", [])
    for item in detail_apl:
        vehicles.append(
            {
                "brand": item.get("Montadora", ""),
                "name": item.get("Modelo", ""),
                "model": item.get("Modelo", ""),
                "engineName": item.get("Motor", ""),
                "engineConfiguration": "",
                "startYear": parse_ano_inicio(item.get("Ano", "")),
                "endYear": parse_ano_fim(item.get("Ano", "")),
                "note": item.get("DescModelo", ""),
                "only": "",
                "restriction": "",
                "position": "",
                "side": "",
                "steering": "",
            }
        )
    return vehicles


# Exemplo de parser genérico para JSON
# Use este parser se o JSON já vier no formato esperado ou for simples de adaptar
# Adapte conforme necessário para seu padrão de dados


def parse_generic_json(data):
    """
    Parser genérico para respostas JSON padronizadas.
    Use este parser para provedores REST que retornam listas de veículos já no formato esperado.
    """
    return data.get("vehicles", []) if isinstance(data, dict) else data


def parse_viemar_json(data):
    """
    Parser específico para o JSON da Viemar.
    Use este parser para provedores Viemar.
    """
    vehicles = []
    for catalog in data.get("catalog", []):
        brand = catalog.get("brand", {}).get("value", "")
        model = catalog.get("model", {}).get("value", "")
        year = catalog.get("year", {}).get("value", "")
        product_line = catalog.get("productLine", {}).get("value", "")
        cross_ref = catalog.get("crossReference", {}).get("valueList", [])
        cross_ref_str = ", ".join([x.get("value", "") for x in cross_ref])
        for app in catalog.get("application", []):
            vehicles.append(
                {
                    "brand": brand,
                    "name": model,
                    "model": model,
                    "engineName": "",
                    "engineConfiguration": "",
                    "startYear": app.get("ano_inicial", year),
                    "endYear": app.get("ano_final", year),
                    "note": cross_ref_str,
                    "only": "",
                    "restriction": "",
                    "position": app.get("posicao", {}).get("default_value", ""),
                    "side": "",
                    "steering": "",
                }
            )
    return vehicles


def parse_schadek_json(data):
    vehicles = []

    def to_int(val):
        try:
            return int(val)
        except (TypeError, ValueError):
            return None

    # Caso 1: lista de aplicações direto
    if isinstance(data, list) and data and "automaker" in data[0]:
        for app in data:
            vehicles.append(
                {
                    "brand": app.get("automaker", ""),
                    "name": "",  # Não tem nome do produto nesse endpoint
                    "model": app.get("model", ""),
                    "engineName": app.get("engineType", ""),
                    "engineConfiguration": "",
                    "startYear": to_int(app.get("initialDate", "")),
                    "endYear": to_int(app.get("endDate", "")),
                    "note": app.get("comments", ""),
                    "only": "",
                    "restriction": "",
                    "position": "",
                    "side": "",
                    "steering": "",
                }
            )
        return vehicles

    # Caso 2: lista de produtos com applications
    produtos = data if isinstance(data, list) else [data]
    for produto in produtos:
        applications = produto.get("applications", {}).get("$values", [])
        for app in applications:
            vehicles.append(
                {
                    "brand": app.get("automaker", ""),
                    "name": produto.get("name", ""),
                    "model": app.get("model", ""),
                    "engineName": app.get("engineType", ""),
                    "engineConfiguration": "",
                    "startYear": to_int(app.get("initialDate", "")),
                    "endYear": to_int(app.get("endDate", "")),
                    "note": produto.get("observation", "") or app.get("comments", ""),
                    "only": "",
                    "restriction": "",
                    "position": "",
                    "side": "",
                    "steering": "",
                }
            )
    return vehicles


# --- PARSERS HTML ---
def parse_nakata_html(soup):
    """
    Parser específico para o HTML da Nakata.
    Use um parser específico quando o HTML do provedor for único ou complexo.
    """
    vehicles = []
    try:
        table = None
        for t in soup.find_all("table"):
            headers = [th.get_text(strip=True).lower() for th in t.find_all("th")]
            if "veículo" in headers or "veiculo" in headers:
                table = t
                break
        if not table:
            return vehicles
        tbody = table.find("tbody")
        if not tbody:
            return vehicles
        for row in tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 7:
                continue
            brand = cells[0].get_text(strip=True)
            model = cells[1].get_text(strip=True)
            ano_raw = cells[2].get_text(strip=True)
            posicao = cells[3].get_text(strip=True)
            lado = cells[4].get_text(strip=True)
            direcao = cells[5].get_text(strip=True)
            observacao = cells[6].get_text(strip=True)
            vehicles.append(
                {
                    "brand": brand,
                    "name": model,
                    "model": model,
                    "engineName": "",
                    "engineConfiguration": "",
                    "startYear": None,  # Adapte se necessário
                    "endYear": None,
                    "note": observacao,
                    "only": "",
                    "restriction": "",
                    "position": posicao,
                    "side": lado,
                    "steering": direcao,
                }
            )
    except Exception:
        pass
    return vehicles


# Exemplo de parser genérico para HTML
# Use este parser para provedores REST que retornam tabelas HTML simples e padronizadas


def parse_generic_html(soup):
    """
    Parser genérico para HTML padronizado.
    Use este parser para provedores REST que retornam tabelas HTML simples.
    Adapte conforme necessário para seu padrão de dados.
    """
    vehicles = []
    # Exemplo: busca por todas as linhas de tabela
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue
            vehicles.append(
                {
                    "brand": cells[0].get_text(strip=True) if len(cells) > 0 else "",
                    "name": cells[1].get_text(strip=True) if len(cells) > 1 else "",
                    "model": cells[1].get_text(strip=True) if len(cells) > 1 else "",
                    "engineName": "",
                    "engineConfiguration": "",
                    "startYear": None,
                    "endYear": None,
                    "note": "",
                    "only": "",
                    "restriction": "",
                    "position": "",
                    "side": "",
                    "steering": "",
                }
            )
    return vehicles


# --- Funções auxiliares para parsing de ano (usadas por parsers específicos) ---
def parse_ano_inicio(ano_str):
    if not ano_str:
        return None
    anos = re.findall(r"\d{2,4}", ano_str)
    if not anos:
        return None
    ano_ini = int(anos[0])
    if len(anos[0]) == 2:
        ano_ini = 2000 + int(anos[0]) if int(anos[0]) < 50 else 1900 + int(anos[0])
    return ano_ini


def parse_ano_fim(ano_str):
    if not ano_str:
        return None
    anos = re.findall(r"\d{2,4}", ano_str)
    if not anos:
        return None
    ano_fim = int(anos[-1])
    if len(anos[-1]) == 2:
        ano_fim = 2000 + int(anos[-1]) if int(anos[-1]) < 50 else 1900 + int(anos[-1])
    return ano_fim


# --- DICA DE USO ---
# Sempre que um novo provedor REST retornar dados em formato diferente,
# crie um parser específico (ex: parse_nomeprovdor_json ou parse_nomeprovdor_html).
# Se o formato for igual ao padrão, use os parsers genéricos.
