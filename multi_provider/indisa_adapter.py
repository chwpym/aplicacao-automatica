import requests

def buscar_uuid_indisa_por_codigo(codigo_peca):
    url = f"https://indisa.catalogofraga.com.br/resultado?busca={codigo_peca}"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        # print(f"[DEBUG] Indisa: erro HTTP {resp.status_code} ao buscar UUID para {codigo_peca}")
        return None
    from bs4 import BeautifulSoup, Tag
    soup = BeautifulSoup(resp.text, "lxml")
    # DEBUG: Salvar HTML para análise
    # with open("debug_indisa_resultado.html", "w", encoding="utf-8") as f:
    #     f.write(resp.text)
    link = soup.find("a", href=lambda x: isinstance(x, str) and "/produto/" in x)
    href = None
    if link and isinstance(link, Tag) and hasattr(link, 'attrs') and 'href' in link.attrs:
        href = link.attrs['href']
    if not href or not isinstance(href, str):
        # print(f"[DEBUG] Indisa: não encontrou link de produto para {codigo_peca}")
        return None
    uuid = href.split("/")[-1]
    # print(f"[DEBUG] Indisa: UUID encontrado para {codigo_peca}: {uuid}")
    return uuid

def is_uuid(s):
    return isinstance(s, str) and '-' in s and len(s) >= 32

def buscar_aplicacoes_indisa(codigo_peca):
    # 1. Buscar UUID se necessário
    uuid = codigo_peca if is_uuid(codigo_peca) else buscar_uuid_indisa_por_codigo(codigo_peca)
    if not uuid:
        # print(f"[DEBUG] Indisa: Nenhum UUID encontrado para {codigo_peca}")
        return []
    # 2. Buscar aplicações via GraphQL
    # print(f"[DEBUG] Indisa: Buscando GraphQL para UUID: {uuid}")
    url = "https://bff.catalogofraga.com.br/gateway/graphql"
    query = """
    query GetProductById($id: String!, $market: MarketType!) {
      product(id: $id, market: $market) {
        vehicles {
          brand
          name
          model
          engineName
          engineConfiguration
          endYear
          note
          only
          restriction
          startYear
        }
      }
    }
    """
    variables = {"id": uuid, "market": "BRA"}
    headers = {
        "Origin": "https://indisa.catalogofraga.com.br",
        "Referer": "https://indisa.catalogofraga.com.br/",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }
    try:
        resp = requests.post(url, json={"query": query, "variables": variables}, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        # print(f"[DEBUG] Indisa: erro ao acessar GraphQL: {e}")
        return []
    # print(f"[DEBUG] Indisa: Status GraphQL {resp.status_code} para UUID {uuid}")
    if resp.status_code != 200:
        # print(f"[DEBUG] Indisa: erro HTTP {resp.status_code} na consulta GraphQL para {uuid}")
        return []
    data = resp.json()
    vehicles = data.get("data", {}).get("product", {}).get("vehicles", [])
    results = []
    for v in vehicles:
        results.append({
            "montadora": v.get("brand", ""),
            "modelo": v.get("name", ""),
            "motor": v.get("engineName", ""),
            "configuracao_motor": v.get("engineConfiguration", ""),
            "ano_inicio": v.get("startYear", ""),
            "ano_fim": v.get("endYear", ""),
            "observacao": v.get("note", ""),
            "fonte": "Indisa"
        })
    # print(f"[DEBUG] {len(results)} aplicações encontradas na Indisa.")
    return results 