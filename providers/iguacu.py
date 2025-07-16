import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any, cast

class IguacuProvider:
    BASE_URL = "https://www.iguacu.ind.br"

    @staticmethod
    def buscar_codigo_autocomplete(codigo: str) -> List[str]:
        url = f"{IguacuProvider.BASE_URL}/AutoComplete.asmx/GetProd"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }
        data = {"d": [codigo]}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("d", [])

    @staticmethod
    def buscar_produto(codigo: str) -> List[Dict[str, Any]]:
        session = requests.Session()
        url_busca = f"{IguacuProvider.BASE_URL}/busca"
        # 1. GET para pegar os campos ocultos
        resp_get = session.get(url_busca)
        soup = BeautifulSoup(resp_get.text, "html.parser")

        def get_value(name: str) -> str:
            tag = soup.find("input", {"name": name})
            if isinstance(tag, Tag) and tag.has_attr("value"):
                value = tag["value"]
                return str(value)
            return ""

        # 2. Montar o payload completo
        payload = {
            "script": "UpdatePanel2|BtnPesquisa",
            "TxtPesquisaVeiculo": "",
            "txtWKtxt1_ClientState": "",
            "ddlCategoria": "0",
            "ddlMontadora": "-1",
            "ddlVeiculos": "-1",
            "ddlCombustivel": "-1",
            "ddlMotor": "-1",
            "ddlAnoVeiculo": "-1",
            "TxtPesquisaCatalogo": codigo,
            "TextBoxWatermarkExtender1_ClientState": "",
            "chks": "RB_Iguacu",
            "hiddenInputToUpdateATBuffer_CommonToolkitScripts": "1",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": get_value("__VIEWSTATE"),
            "__VIEWSTATEGENERATOR": get_value("__VIEWSTATEGENERATOR"),
            "__EVENTVALIDATION": get_value("__EVENTVALIDATION"),
            "__ASYNCPOST": "true",
            "BtnPesquisa": "Pesquisar"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url_busca,
            "Origin": "https://www.iguacu.ind.br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        }

        # 3. POST para buscar
        response = session.post(url_busca, data=payload, headers=headers)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")
        tabela = soup.find("table", {"id": "GridReferencia"})
        resultados = []
        if isinstance(tabela, Tag):
            linhas = tabela.find_all("tr")[1:]  # Pular header
            for linha in linhas:
                if isinstance(linha, Tag):
                    colunas = linha.find_all("td")
                    if len(colunas) >= 9:
                        img_tag = None
                        if isinstance(colunas[0], Tag):
                            img_tag = cast(Tag, colunas[0]).find("img")
                        imagem = img_tag["src"] if isinstance(img_tag, Tag) and img_tag.has_attr("src") else None
                        resultados.append({
                            "montadora": colunas[1].get_text(strip=True),
                            "referencia": colunas[2].get_text(strip=True),
                            "codigo_iguacu": colunas[3].get_text(strip=True),
                            "veiculo": colunas[4].get_text(strip=True),
                            "motor": colunas[5].get_text(strip=True),
                            "combustivel": colunas[6].get_text(strip=True),
                            "obs": colunas[7].get_text(strip=True),
                            "ano": colunas[8].get_text(strip=True),
                            "imagem": imagem,
                        })
        # Adapta para o formato padrão da interface
        return parse_iguacu_html(resultados)

# --- Parser específico para adaptar o resultado ao formato padrão ---
def parse_iguacu_html(resultados_iguacu):
    """
    Adapta a lista de dicionários retornada pelo provider Iguaçu
    para o formato padrão esperado pela interface.
    """
    vehicles = []
    for item in resultados_iguacu:
        # Exemplo de parsing do campo 'ano' (ex: "13->" ou "06-12")
        ano_raw = item.get("ano", "")
        start_year, end_year = None, None
        if "->" in ano_raw:
            # Ex: "13->" significa de 2013 em diante
            start_year = int("20" + ano_raw[:2]) if len(ano_raw) >= 2 and ano_raw[:2].isdigit() else None
        elif "-" in ano_raw:
            # Ex: "06-12" significa de 2006 a 2012
            anos = ano_raw.split("-")
            if len(anos) == 2 and anos[0].isdigit() and anos[1].isdigit():
                start_year = int("20" + anos[0]) if len(anos[0]) == 2 else int(anos[0])
                end_year = int("20" + anos[1]) if len(anos[1]) == 2 else int(anos[1])
        else:
            # Tenta pegar um único ano
            if ano_raw.isdigit():
                start_year = end_year = int(ano_raw)

        vehicles.append({
            "brand": item.get("montadora", ""),
            "name": item.get("veiculo", ""),
            "model": item.get("veiculo", ""),
            "engineName": item.get("motor", ""),
            "engineConfiguration": "",
            "startYear": start_year,
            "endYear": end_year,
            "note": item.get("obs", ""),
            "only": "",
            "restriction": "",
            "position": "",
            "side": "",
            "steering": "",
            "image": item.get("imagem", ""),
            "reference": item.get("referencia", ""),
            "codigo_iguacu": item.get("codigo_iguacu", ""),
            "combustivel": item.get("combustivel", "")
        })
    return vehicles