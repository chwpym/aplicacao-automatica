from .base import BaseProvider
import requests
import json

class GenericGraphQLProvider(BaseProvider):
    """
    Provedor GraphQL genérico, configurável via JSON.
    """
    def __init__(self, nome, url, query, headers=None):
        self.nome = nome
        self.url = url
        self.query = query
        self.headers = headers or {}
        # Headers padrão para GraphQL
        self.default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def buscar(self, termo):
        # Variáveis padrão para queries do tipo GetProductById
        graphql_variables = {
            "id": termo,
            "market": "BRA"
        }
        # Monta headers finais
        headers = self.default_headers.copy()
        headers.update(self.headers)
        payload = json.dumps({
            "query": self.query,
            "variables": graphql_variables
        })
        try:
            response = requests.post(self.url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()
            if 'errors' in data:
                print(f"[GenericGraphQLProvider] Erro na resposta GraphQL: {data['errors']}")
                return []
            # Tenta extrair vehicles do caminho padrão
            product_data = data.get('data', {}).get('product', {})
            vehicles = product_data.get('vehicles', [])
            if not vehicles:
                print(f"[GenericGraphQLProvider] Nenhuma aplicação de veículo encontrada para '{termo}' em '{self.nome}'.")
                return []
            aplicacoes_formatadas = []
            for vehicle in vehicles:
                aplicacoes_formatadas.append({
                    'brand': vehicle.get('brand', ''),
                    'name': vehicle.get('name', ''),
                    'model': vehicle.get('model', ''),
                    'engineName': vehicle.get('engineName', ''),
                    'engineConfiguration': vehicle.get('engineConfiguration', ''),
                    'brakeSystem': vehicle.get('brakeSystem', ''),
                    'startYear': vehicle.get('startYear', ''),
                    'endYear': vehicle.get('endYear', ''),
                    'note': vehicle.get('note', ''),
                    'only': vehicle.get('only', ''),
                    'restriction': vehicle.get('restriction', '')
                })
            return aplicacoes_formatadas
        except Exception as e:
            print(f"[GenericGraphQLProvider] Erro na requisição GraphQL: {e}")
            return [] 