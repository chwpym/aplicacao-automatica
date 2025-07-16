import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any, cast

def to_int(val):
    try:
        return int(val)
    except Exception:
        return None

class MteThomsonProvider:
    BASE_URL = "https://cate.mte-thomson.com.br"

    @staticmethod
    def buscar_produto(codigo: str) -> List[Dict[str, Any]]:
        url = f"{MteThomsonProvider.BASE_URL}/pt/br/produto/detalhes/{codigo}/plug-eletronico--agua"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        aplicacoes = []
        tabela = soup.find("table", {"id": "GridAplicacao_DXMainTable"})
        if isinstance(tabela, Tag):
            linhas = tabela.find_all("tr", class_="dxgvDataRow_mtethomson")
            for linha in linhas:
                if isinstance(linha, Tag):
                    colunas = linha.find_all("td")
                    if len(colunas) >= 14:
                        aplicacoes.append({
                            "brand": colunas[0].get_text(strip=True),
                            "model": colunas[1].get_text(strip=True),
                            "engineName": colunas[2].get_text(strip=True),
                            "engineConfiguration": colunas[3].get_text(strip=True),
                            "engineValves": colunas[4].get_text(strip=True),
                            "engineFuelType": colunas[5].get_text(strip=True),
                            "startYear": to_int(colunas[6].get_text(strip=True)),
                            "endYear": to_int(colunas[7].get_text(strip=True)),
                            "position": colunas[8].get_text(strip=True),
                            "version": colunas[9].get_text(strip=True),
                            "engineCode": colunas[10].get_text(strip=True),
                            "region": colunas[11].get_text(strip=True),
                            "transmission": colunas[12].get_text(strip=True),
                            "note": colunas[13].get_text(strip=True),
                        })
        return aplicacoes