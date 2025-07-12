from .base import BaseProvider
import requests
import json

class AuthomixGraphQLProvider(BaseProvider):
    """
    Provedor para busca de aplicações via GraphQL (Authomix).
    Implementa o método 'buscar' para consultar o endpoint GraphQL.
    """
    def buscar(self, termo):
        graphql_url = "https://bff.catalogofraga.com.br/gateway/graphql"
        graphql_query = """
query GetProductById($id: String!, $market: MarketType! ) {
  product(id: $id, market: $market) {
    id
    partNumber
    brand {
      name
      imageUrl
      __typename
    }
    applicationDescription
    images {
      imageUrl
      thumbnailUrl
      category
      __typename
    }
    specifications {
      id
      category
      description
      value
      important
      __typename
    }
    crossReferences {
      brand {
        id
        name
        __typename
      }
      partNumber
      __typename
    }
    videos
    vehicles {
      brand
      name
      model
      engineName
      engineConfiguration
      brakeSystem
      endYear
      note
      only
      restriction
      startYear
      brand
      __typename
    }
    components {
      partNumber
      productGroup
      applicationDescription
      activeCatalog
      status
      __typename
    }
    distributors {
      code
      distributor {
        name
        __typename
      }
      __typename
    }
    status
    containsUniversalApplication
    billOfMaterial {
      imageUrl
      products {
        productId
        partNumber
        amount
        description
        note
        coordinates {
          coordinateX
          coordinateY
          __typename
        }
        __typename
      }
      __typename
    }
    links {
      category
      description
      title
      url
      distributor {
        id
        name
        __typename
      }
      __typename
    }
    productGroup {
      name
      __typename
    }
    market {
      name
      __typename
    }
    __typename
  }
}
        """
        graphql_variables = {
            "id": termo,
            "market": "BRA"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://catalogo.authomix.com.br",
            "Referer": "https://catalogo.authomix.com.br/",
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A )Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site"
        }
        payload = json.dumps({
            "query": graphql_query,
            "variables": graphql_variables
        })
        aplicacoes_formatadas = []
        try:
            response = requests.post(graphql_url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()
            print("[DEBUG] JSON retornado da API:", json.dumps(data, indent=2, ensure_ascii=False))
            if 'errors' in data:
                print(f"Erro na resposta GraphQL: {data['errors']}")
                return []
            product_data = data.get('data', {}).get('product', {})
            vehicles = product_data.get('vehicles', [])
            print("[DEBUG] Campo vehicles:", vehicles)
            if not vehicles:
                print("Nenhuma aplicação de veículo encontrada para esta peça.")
                return []
            for vehicle in vehicles:
                brand = vehicle.get('brand', '')
                name = vehicle.get('name', '')
                model = vehicle.get('model', '')
                engine_name = vehicle.get('engineName', '')
                engine_config = vehicle.get('engineConfiguration', '')
                brake_system = vehicle.get('brakeSystem', '')
                start_year = vehicle.get('startYear', '')
                end_year = vehicle.get('endYear', '')
                note = vehicle.get('note', '')
                only = vehicle.get('only', '')
                restriction = vehicle.get('restriction', '')
                field_values = {
                    'brand': brand,
                    'name': name,
                    'model': model,
                    'engineName': engine_name,
                    'engineConfiguration': engine_config,
                    'brakeSystem': brake_system,
                    'startYear': start_year,
                    'endYear': end_year,
                    'note': note,
                    'only': only,
                    'restriction': restriction
                }
                aplicacoes_formatadas.append(field_values)
            print("[DEBUG] Resultado final retornado:", aplicacoes_formatadas)
            return aplicacoes_formatadas
        except Exception as e:
            print(f"Erro na requisição GraphQL: {e}")
            return [] 