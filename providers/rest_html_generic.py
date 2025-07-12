import re

def parse_generic_rest_html(soup):
    """Parse genérico para outros provedores REST"""
    vehicles = []
    
    try:
        # Procura por padrões comuns em páginas de aplicação de peças
        text = soup.get_text()
        
        # Extrai informações usando regex
        # Marca
        marca_match = re.search(r'\b(VW|FIAT|GM|FORD|CHEVROLET|HONDA|TOYOTA|HYUNDAI|NISSAN|RENAULT|PEUGEOT|CITROEN|BMW|MERCEDES|AUDI|VOLVO|SCANIA|IVECO|MERCEDES-BENZ)\b', text, re.IGNORECASE)
        marca = marca_match.group(1) if marca_match else ''
        
        # Modelo
        modelo_match = re.search(r'\b(GOL|PALIO|CORSA|CIVIC|COROLLA|HB20|SENTRA|CLIO|208|C3|X1|CLASSE|A3|S40|FH|DAILY|SPRINTER)\b', text, re.IGNORECASE)
        modelo = modelo_match.group(1) if modelo_match else ''
        
        # Ano
        ano_match = re.search(r'\b(19|20)\d{2}(?:[-/](19|20)\d{2})?\b', text)
        ano_str = ano_match.group(0) if ano_match else ''
        
        # Motor
        motor_match = re.search(r'\b\d+\.\d+\b', text)
        motor = motor_match.group(0) if motor_match else ''
        
        if marca or modelo or ano_str:
            vehicle = {
                'brand': marca,
                'name': modelo,
                'model': modelo,
                'engineName': motor,
                'engineConfiguration': '',
                'startYear': None,
                'endYear': None,
                'note': '',
                'only': '',
                'restriction': ''
            }
            
            # Processa o ano
            if ano_str:
                if '-' in ano_str or '/' in ano_str:
                    years = re.findall(r'\d{4}', ano_str)
                    if len(years) >= 2:
                        vehicle['startYear'] = int(years[0])
                        vehicle['endYear'] = int(years[1])
                    elif len(years) == 1:
                        vehicle['startYear'] = int(years[0])
                else:
                    vehicle['startYear'] = int(ano_str)
            
            vehicles.append(vehicle)
    
    except Exception as e:
        print(f"Erro ao fazer parsing genérico do HTML: {e}")
    
    return vehicles