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