# --- PARSER ANTIGO (mantido para referência, agora comentado) ---
'''
from bs4 import BeautifulSoup, Tag

def parse_ds_html(html):
    """
    Parser exclusivo para DS: só retorna aplicações por veículo da tabela jq-apps.
    """
    soup = BeautifulSoup(html, "lxml")
    vehicles = []
    table_div = soup.find("div", class_="table jq-apps")
    if not isinstance(table_div, Tag):
        return vehicles
    table = table_div.find("table")
    if not isinstance(table, Tag):
        return vehicles
    rows = table.find_all("tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue
        ano_raw = cols[4].get_text(strip=True)
        start_year, end_year = None, None
        if ">" in ano_raw:
            anos = [a.strip() for a in ano_raw.split(">")]
            if len(anos) == 2:
                if anos[0].isdigit():
                    start_year = int("20" + anos[0]) if len(anos[0]) == 2 else int(anos[0])
                if anos[1].isdigit():
                    end_year = int("20" + anos[1]) if len(anos[1]) == 2 else int(anos[1])
        elif ano_raw.isdigit():
            start_year = end_year = int(ano_raw)
        vehicles.append({
            "brand": cols[0].get_text(strip=True),
            "name": cols[1].get_text(strip=True),
            "model": cols[1].get_text(strip=True),
            "engineName": cols[2].get_text(strip=True),
            "engineConfiguration": "",
            "startYear": start_year,
            "endYear": end_year,
            "note": cols[5].get_text(strip=True),
            "only": "",
            "restriction": "",
            "position": "",
            "side": "",
            "steering": "",
            "combustivel": cols[3].get_text(strip=True),
            "ano": ano_raw,
        })
    return vehicles 
'''

# --- NOVO PARSER: Somente tabela <div class="table jq-apps"> ---
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any

def parse_ds_html(html: str) -> List[Dict[str, Any]]:
    """
    Parser exclusivo para DS: retorna apenas aplicações por veículo da tabela <div class="table jq-apps">.
    Ignora qualquer outra tabela ou div.
    """
    soup = BeautifulSoup(html, "lxml")
    vehicles: List[Dict[str, Any]] = []
    table_div = soup.find("div", class_="table jq-apps")
    if not isinstance(table_div, Tag):
        return vehicles
    table = table_div.find("table")
    if not isinstance(table, Tag):
        return vehicles
    tbody = table.find("tbody")
    if not isinstance(tbody, Tag):
        return vehicles
    rows = tbody.find_all("tr")
    for row in rows:
        if not isinstance(row, Tag):
            continue
        cols = row.find_all("td")
        if len(cols) < 6:
            continue
        ano_raw = cols[4].get_text(strip=True)
        start_year, end_year = None, None
        if ">" in ano_raw:
            anos = [a.strip() for a in ano_raw.split(">")]
            if len(anos) == 2:
                if anos[0].isdigit():
                    start_year = int("20" + anos[0]) if len(anos[0]) == 2 else int(anos[0])
                if anos[1].isdigit():
                    end_year = int("20" + anos[1]) if len(anos[1]) == 2 else int(anos[1])
        elif ano_raw.isdigit():
            start_year = end_year = int(ano_raw)
        vehicles.append({
            "brand": cols[0].get_text(strip=True),
            "name": cols[1].get_text(strip=True),
            "model": cols[1].get_text(strip=True),
            "engineName": cols[2].get_text(strip=True),
            "engineConfiguration": "",
            "startYear": start_year,
            "endYear": end_year,
            "note": cols[5].get_text(strip=True),
            "only": "",
            "restriction": "",
            "position": "",
            "side": "",
            "steering": "",
            "combustivel": cols[3].get_text(strip=True),
            "ano": ano_raw,
        })
    return vehicles 