import requests
from .base import BaseProvider

class RESTProvider(BaseProvider):
    """
    Provedor REST genérico para busca de dados automotivos.
    Recebe configuração (url, headers, etc) e executa a busca.
    Suporta GET e POST.
    """
    def __init__(self, config):
        self.config = config
        self.url = config.get('url')
        self.headers = config.get('headers', {})
        self.query = config.get('query', '')
        self.method = config.get('method', 'GET').upper()

    def buscar(self, termo):
        url = self.url.replace('{id}', str(termo))
        if self.method == 'POST':
            # Para Viemar, o body deve ser {"code": termo}
            data = {"code": termo}
            response = requests.post(url, headers=self.headers, json=data)
        else:
            response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return response.json()
        else:
            return response.text

def buscar_provedor_generico(id_peca, provedor_config):
    """Busca dados de um provedor específico usando sua configuração"""
    import json
    from tkinter import messagebox
    try:
        url = provedor_config.get('url', '')
        headers = provedor_config.get('headers', {})
        query = provedor_config.get('query', '')
        tipo = provedor_config.get('tipo', 'graphql')
        default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A )Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site"
        }
        final_headers = {**default_headers, **headers}
        if tipo == 'graphql':
            final_headers["Content-Type"] = "application/json"
            variables = {
                "id": id_peca,
                "market": "BRA"
            }
            payload = json.dumps({
                "query": query,
                "variables": variables
            })
            response = requests.post(url, headers=final_headers, data=payload)
            response.raise_for_status()
            data = response.json()
            if 'errors' in data:
                messagebox.showerror("Erro GraphQL", f"Erro na resposta GraphQL: {data['errors']}")
                return []
            product_data = data.get('data', {}).get('product', {})
            vehicles = product_data.get('vehicles', [])
            return vehicles
        elif tipo == 'rest':
            rest = RESTProvider({
                'url': url,
                'headers': final_headers,
                'query': provedor_config.get('query', ''),
                'nome': provedor_config.get('nome', '')
            })
            try:
                response = rest.buscar(id_peca)
            except Exception as e:
                messagebox.showerror("Erro de Conexão", f"Erro ao acessar a API do provedor: {e}")
                return []
            from providers.rest_parsers import (
                parse_viemar_json, parse_wega_json, parse_generic_json, parse_schadek_json,
                parse_nakata_html, parse_generic_html, parse_tubacabos_json
            )
            if isinstance(response, dict):
                if 'viemar' in provedor_config.get('nome', '').lower() or 'viemar' in provedor_config.get('url', '').lower():
                    return parse_viemar_json(response)
                elif 'wega' in provedor_config.get('nome', '').lower() or 'wega' in provedor_config.get('url', '').lower():
                    return parse_wega_json(response)
                elif 'schadek' in provedor_config.get('nome', '').lower() or 'schadek' in provedor_config.get('url', '').lower():
                    return parse_schadek_json(response)
                elif 'tubacabos' in provedor_config.get('nome', '').lower() or 'tubacabos' in provedor_config.get('url', '').lower():
                    return parse_tubacabos_json(response)
                else:
                    return parse_generic_json(response)
            else:
                try:
                    from bs4 import BeautifulSoup
                except ImportError:
                    messagebox.showerror("Dependência Ausente", "BeautifulSoup4 é necessário para provedores REST. Instale com: pip install beautifulsoup4")
                    return []
                soup = BeautifulSoup(response, 'html.parser')
                provedor_nome = provedor_config.get('nome', '').lower()
                if 'nakata' in provedor_nome:
                    return parse_nakata_html(soup)
                else:
                    return parse_generic_html(soup)
        else:
            messagebox.showwarning("Tipo não suportado", f"Tipo de API '{tipo}' ainda não é suportado.")
            return []
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao acessar a API do provedor: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Erro de Dados", "Erro ao decodificar a resposta JSON da API.")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado: {e}")
    return [] 