import requests
from bs4 import BeautifulSoup, Tag

def buscar_aplicacoes_schadek(codigo_peca):
    # print(f"[DEBUG] Buscando na Schadek: {codigo_peca}")
    headers = {"User-Agent": "Mozilla/5.0"}

    # 1. Buscar produto para obter code interno e aplicações embutidas
    url_prod = f"https://schadek.com.br/api/domain/products/code/{codigo_peca}"
    try:
        resp_prod = requests.get(url_prod, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        # print(f"[DEBUG] Erro ao acessar {url_prod}: {e}")
        return []
    if resp_prod.status_code != 200:
        # print(f"[DEBUG] Erro HTTP {resp_prod.status_code} na Schadek (busca produto)")
        return []
    data_prod = resp_prod.json()
    if isinstance(data_prod, list):
        data_prod = data_prod[0]
    code_interno = data_prod.get("code")
    applications = data_prod.get("applications", {}).get("$values", [])

    # 2. Tenta buscar aplicações diretamente pelo code interno
    results = []
    if code_interno:
        url_app = f"https://schadek.com.br/api/domain/application/{code_interno}"
        try:
            resp_app = requests.get(url_app, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            # print(f"[DEBUG] Erro ao acessar {url_app}: {e}")
            resp_app = None
        if resp_app and resp_app.status_code == 200:
            apps = resp_app.json()
            if isinstance(apps, list) and apps and "automaker" in apps[0]:
                # print(f"[DEBUG] Aplicações encontradas pelo code interno {code_interno}")
                for app in apps:
                    results.append({
                        "montadora": app.get("automaker", ""),
                        "modelo": app.get("model", ""),
                        "motor": app.get("engineType", ""),
                        "configuracao_motor": "",
                        "ano_inicio": app.get("initialDate", ""),
                        "ano_fim": app.get("endDate", ""),
                        "observacao": app.get("comments", ""),
                        "fonte": "Schadek"
                    })
    # 3. Se não encontrou nada, busca no campo applications do produto
    if not results and applications:
        # print(f"[DEBUG] Aplicações encontradas no campo 'applications' do produto")
        for app in applications:
            results.append({
                "montadora": app.get("automaker", ""),
                "modelo": app.get("model", ""),
                "motor": app.get("engineType", ""),
                "configuracao_motor": "",
                "ano_inicio": app.get("initialDate", ""),
                "ano_fim": app.get("endDate", ""),
                "observacao": app.get("comments", ""),
                "fonte": "Schadek"
            })
    # 4. Fallback: busca via HTML se nada foi encontrado
    if not results and code_interno:
        # print("[DEBUG] Fallback: buscando aplicações via HTML")
        url_detail = f"https://schadek.com.br/ProductDetail/{code_interno}"
        try:
            resp_detail = requests.get(url_detail, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            # print(f"[DEBUG] Erro ao acessar {url_detail}: {e}")
            return []
        if resp_detail.status_code == 200:
            soup = BeautifulSoup(resp_detail.text, "lxml")
            table = soup.find("table")
            if table and isinstance(table, Tag):
                for row in table.find_all("tr")[1:]:
                    if not isinstance(row, Tag):
                        continue
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        results.append({
                            "montadora": cols[0].get_text(strip=True),
                            "modelo": cols[1].get_text(strip=True),
                            "motor": cols[2].get_text(strip=True),
                            "configuracao_motor": "",
                            "ano_inicio": cols[3].get_text(strip=True),
                            "ano_fim": "",
                            "observacao": cols[4].get_text(strip=True) if len(cols) > 4 else "",
                            "fonte": "Schadek"
                        })
                # print(f"[DEBUG] {len(results)} aplicações encontradas via HTML na Schadek.")
            else:
                # print("[DEBUG] Tabela de aplicações não encontrada no HTML.")
                pass
        else:
            # print(f"[DEBUG] Erro HTTP {resp_detail.status_code} ao buscar ProductDetail HTML.")
            pass
    if not results:
        # print("[DEBUG] Nenhuma aplicação encontrada na Schadek.")
        pass
    else:
        # print(f"[DEBUG] {len(results)} aplicações retornadas da Schadek.")
        pass
    return results 