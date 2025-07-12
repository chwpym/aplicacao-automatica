from providers.generic_graphql import GenericGraphQLProvider
from providers.rest import RESTProvider
from providers.pdf import PDFProvider
from tkinter import messagebox
import requests
import json
from providers.rest_parsers import (
    parse_viemar_json, parse_wega_json, parse_generic_json, parse_nakata_html, parse_generic_html
)

def buscar_provedor_generico(id_peca, provedor_config):
    """Busca dados de um provedor específico usando sua configuração"""
    try:
        url = provedor_config.get('url', '')
        headers = provedor_config.get('headers', {})
        query = provedor_config.get('query', '')
        tipo = provedor_config.get('tipo', 'graphql')
        
        # Headers padrão que podem ser sobrescritos
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
        
        # Mescla headers padrão com headers específicos do provedor
        final_headers = {**default_headers, **headers}
        
        if tipo == 'graphql':
            graphql_provider = GenericGraphQLProvider(
                nome=provedor_config.get('nome', ''),
                url=url,
                query=query,
                headers=headers
            )
            return graphql_provider.buscar(id_peca)
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
            # --- Parsing da resposta REST ---
            # Se for JSON (ex: Wega, Viemar)
            if isinstance(response, dict):
                if 'viemar' in provedor_config.get('nome', '').lower() or 'viemar' in provedor_config.get('url', '').lower():
                    return parse_viemar_json(response)
                if 'wega' in provedor_config.get('nome', '').lower() or 'wega' in provedor_config.get('url', '').lower():
                    return parse_wega_json(response)
                else:
                    return parse_generic_json(response)
            # Se for HTML (ex: Nakata ou outros)
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
        # NOVO: Suporte para PDF Local
        elif tipo == 'pdf_local':
            pasta = provedor_config.get('pasta', 'catalogos_pdf')
            pdf_provider = PDFProvider()
            resultados_pdf = pdf_provider.buscar(id_peca, pasta)
            # Adapta para o formato esperado pela interface
            vehicles = []
            for r in resultados_pdf:
                vehicles.append({
                    'brand': '',
                    'name': '',
                    'model': '',
                    'engineName': '',
                    'engineConfiguration': '',
                    'startYear': '',
                    'endYear': '',
                    'note': f"Arquivo: {r['arquivo']} | Página: {r['pagina']} | Trecho: {r['linha']}",
                    'only': '',
                    'restriction': '',
                    'position': '',
                    'side': '',
                    'steering': ''
                })
            return vehicles
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