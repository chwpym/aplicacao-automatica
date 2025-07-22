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
            return parse_nakata_html_legacy(soup)
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
            start_year, end_year = None, None
            ano_match = re.match(r"(\d{2})/(\d{2})\s*-\s*(\d{2})/(\d{2})", ano_raw)
            if ano_match:
                _, start_yy, _, end_yy = ano_match.groups()
                start_year = int("20" + start_yy) if int(start_yy) < 50 else int("19" + start_yy)
                end_year = int("20" + end_yy) if int(end_yy) < 50 else int("19" + end_yy)
            else:
                anos = re.findall(r"\d{2}/(\d{2})", ano_raw)
                if anos:
                    start_year = end_year = int("20" + anos[0]) if int(anos[0]) < 50 else int("19" + anos[0])
            combined_notes = []
            if observacao and observacao != "-":
                combined_notes.append(observacao)
            if posicao and posicao != "-":
                combined_notes.append(f"Posição: {posicao}")
            if lado and lado != "-":
                combined_notes.append(f"Lado: {lado}")
            if direcao and direcao != "-":
                combined_notes.append(f"Direção: {direcao}")
            vehicles.append({
                'brand': brand,
                'name': model,
                'model': model,
                'engineName': '',
                'engineConfiguration': '',
                'startYear': start_year,
                'endYear': end_year,
                'note': '; '.join(combined_notes),
                'only': '',
                'restriction': '',
                'position': posicao,
                'side': lado,
                'steering': direcao
            })
    except Exception as e:
        print(f"Erro ao fazer parsing do HTML da Nakata: {e}")
        return parse_nakata_html_legacy(soup)
    return vehicles


def parse_nakata_html_legacy(soup):
    vehicles = []
    try:
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 2:
                    continue
                cell_texts = [cell.get_text(strip=True) for cell in cells]
                row_text = ' '.join(cell_texts)
                vehicle_info = extract_vehicle_info_from_text(row_text)
                if vehicle_info:
                    vehicles.append(vehicle_info)
        if not vehicles:
            divs = soup.find_all('div', class_=lambda x: x and any(word in x.lower() for word in ['aplicacao', 'veiculo', 'modelo', 'marca']))
            for div in divs:
                text = div.get_text(strip=True)
                vehicle_info = extract_vehicle_info_from_text(text)
                if vehicle_info:
                    vehicles.append(vehicle_info)
        if not vehicles:
            text = soup.get_text()
            vehicle_info = extract_vehicle_info_from_text(text)
            if vehicle_info:
                vehicles.append(vehicle_info)
    except Exception as e:
        print(f"Erro ao fazer parsing legado do HTML da Nakata: {e}")
    return vehicles


def extract_vehicle_info_from_text(text):
    marca_patterns = [
        r'\b(VW|VOLKSWAGEN)\b',
        r'\b(FIAT)\b',
        r'\b(GM|CHEVROLET)\b',
        r'\b(FORD)\b',
        r'\b(HONDA)\b',
        r'\b(TOYOTA)\b',
        r'\b(HYUNDAI)\b',
        r'\b(NISSAN)\b',
        r'\b(RENAULT)\b',
        r'\b(PEUGEOT)\b',
        r'\b(CITROEN)\b',
        r'\b(BMW)\b',
        r'\b(MERCEDES|MERCEDES-BENZ)\b',
        r'\b(AUDI)\b',
        r'\b(VOLVO)\b',
        r'\b(SCANIA)\b',
        r'\b(IVECO)\b',
    ]
    # ... restante da função ...
    return None  # Placeholder


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


def parse_tubacabos_json(response_data):
    """
    Parser específico para a API da TubaCabos.
    
    Estrutura da resposta:
    {
        "status": 200,
        "response": "Consultado com sucesso", 
        "data": [
            {
                "codigo_tuba": "6403",
                "produto_nome": "CABO DE EMBREAGEM",
                "comprimento": "690",
                "codigo_original": "46.740.889",
                "nome_carro": "PALIO CITY",
                "ano_inicial": "98...01",
                "montadora_nome": "FIAT",
                "aplicacao": "Motor 1.6 8v / 16v Spi",
                "linha_nome": "LINHA LEVE"
            },
            ...
        ]
    }
    """
    vehicles = []
    
    try:
        # Verifica se a resposta foi bem-sucedida
        if response_data.get('status') != 200:
            return vehicles
            
        data_items = response_data.get('data', [])
        
        for item in data_items:
            # Extrai informações básicas
            brand = item.get('montadora_nome', '').strip()
            name = item.get('nome_carro', '').strip()
            model = name  # TubaCabos usa nome_carro como modelo
            
            # Processa anos
            ano_str = item.get('ano_inicial', '')
            start_year, end_year = parse_tubacabos_year_range(ano_str)
            
            # Motor/aplicação
            engine_name = item.get('aplicacao', '').strip()
            
            # Informações do produto
            produto_nome = item.get('produto_nome', '').strip()
            codigo_original = item.get('codigo_original', '').strip()
            comprimento = item.get('comprimento', '').strip()
            linha = item.get('linha_nome', '').strip()
            
            # Cria nota com informações adicionais
            note_parts = []
            if produto_nome:
                note_parts.append(f"Produto: {produto_nome}")
            if codigo_original:
                note_parts.append(f"Código Original: {codigo_original}")
            if comprimento:
                note_parts.append(f"Comprimento: {comprimento}mm")
            if linha:
                note_parts.append(f"Linha: {linha}")
            
            note = " | ".join(note_parts)
            
            vehicle = {
                'brand': brand,
                'name': name,
                'model': model,
                'engineName': engine_name,
                'engineConfiguration': '',  # TubaCabos não fornece essa info separadamente
                'startYear': start_year,
                'endYear': end_year,
                'note': note,
                'only': '',
                'restriction': ''
            }
            
            vehicles.append(vehicle)
            
    except Exception as e:
        print(f"Erro ao processar resposta da TubaCabos: {e}")
        
    return vehicles

def parse_tubacabos_year_range(ano_str):
    """
    Parser específico para anos da TubaCabos.
    
    Exemplos:
    - "98...01" -> (1998, 2001)
    - "97...01/00" -> (1997, 2001) 
    - "99...01/00" -> (1999, 2001)
    """
    if not ano_str:
        return None, None
        
    try:
        # Remove caracteres extras como barra, mas preserva os anos
        # "97...01/00" -> "97...01" (remove tudo após a barra)
        if '/' in ano_str:
            clean_str = ano_str.split('/')[0]
        else:
            clean_str = ano_str
            
        # Substitui ... por -
        clean_str = clean_str.replace('...', '-')
        
        if '-' in clean_str:
            parts = clean_str.split('-')
            start_str = parts[0].strip()
            end_str = parts[1].strip() if len(parts) > 1 else start_str
            
            # Converte anos de 2 dígitos para 4 dígitos
            start_year = None
            end_year = None
            
            if start_str.isdigit():
                start_year = int(start_str)
                if start_year < 50:
                    start_year += 2000
                elif start_year < 100:
                    start_year += 1900
                    
            if end_str.isdigit():
                end_year = int(end_str)
                if end_year < 50:
                    end_year += 2000
                elif end_year < 100:
                    end_year += 1900
                    
            return start_year, end_year
            
    except Exception as e:
        print(f"Erro ao processar ano da TubaCabos '{ano_str}': {e}")
        
    return None, None

# --- DICA DE USO ---
# Sempre que um novo provedor REST retornar dados em formato diferente,
# crie um parser específico (ex: parse_nomeprovdor_json ou parse_nomeprovdor_html).
# Se o formato for igual ao padrão, use os parsers genéricos.
 