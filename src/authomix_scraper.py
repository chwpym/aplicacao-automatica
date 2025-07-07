import requests
import pyperclip
import json # Para trabalhar com JSON

def buscar_aplicacoes_authomix_graphql(id_peca, requested_output_fields):
    # URL do endpoint GraphQL
    graphql_url = "https://bff.catalogofraga.com.br/gateway/graphql"

    # A query GraphQL
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
      name # Adicionado para pegar o nome específico do modelo
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

    # As variáveis que a query espera
    graphql_variables = {
        "id": id_peca,
        "market": "BRA" # Corrigido para "BRA"
    }

    # Cabeçalhos da requisição (simulando um navegador)
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

    # Corpo da requisição POST
    payload = json.dumps({
        "query": graphql_query,
        "variables": graphql_variables
    })

    aplicacoes_formatadas = []
    try:
        response = requests.post(graphql_url, headers=headers, data=payload)
        response.raise_for_status()

        data = response.json()

        if 'errors' in data:
            print(f"Erro na resposta GraphQL: {data['errors']}")
            return []

        product_data = data.get('data', {}).get('product', {})
        vehicles = product_data.get('vehicles', [])

        if not vehicles:
            print("Nenhuma aplicação de veículo encontrada para esta peça.")
            return []

        for vehicle in vehicles:
            # Extrair todos os campos potenciais
            brand = vehicle.get('brand', '')
            name = vehicle.get('name', '') # Nome específico do modelo (ex: "PALIO WEEKEND")
            model = vehicle.get('model', '') # Nome genérico do modelo (ex: "PALIO")
            engine_name = vehicle.get('engineName', '')
            engine_config = vehicle.get('engineConfiguration', '')
            brake_system = vehicle.get('brakeSystem', '')
            start_year = vehicle.get('startYear', '')
            end_year = vehicle.get('endYear', '')
            note = vehicle.get('note', '')
            only = vehicle.get('only', '')
            restriction = vehicle.get('restriction', '')

            # Combinar anos em uma única string no formato "AAAA...AAAA" ou "AAAA..."
            ano_str = ""
            if start_year and end_year:
                if str(start_year) == str(end_year):
                    ano_str = str(start_year)
                else:
                    ano_str = f"{start_year}...{end_year}"
            elif start_year:
                ano_str = f"{start_year}..."
            elif end_year:
                ano_str = f"...{end_year}"

            # Definir um mapeamento de nomes amigáveis para os valores extraídos
            # Prioriza 'name' para 'modelo', e 'engine_name' para 'motor'
            field_values = {
                'marca': brand,
                'modelo': name if name else model, # Usa 'name' se disponível, senão 'model'
                'motor': engine_name if engine_name else engine_config, # Usa 'engine_name' se disponível, senão 'engine_config'
                'ano': ano_str,
                'observacao': note,
                'sistema_freio': brake_system,
                'restricao': restriction,
                'apenas': only
            }

            # Construir a string formatada com base nos campos solicitados
            output_parts = []
            for field_key in requested_output_fields:
                value = field_values.get(field_key)
                if value: # Adiciona apenas se o valor não for vazio
                    output_parts.append(str(value))
            
            # Juntar as partes com um espaço, como no seu exemplo "VW AMAROK 10..."
            aplicacao_formatada = " ".join(output_parts).strip()
            if aplicacao_formatada: # Adiciona apenas se a string formatada não for vazia
                aplicacoes_formatadas.append(aplicacao_formatada)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API GraphQL do Authomix: {e}")
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON da API.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

    return aplicacoes_formatadas

# --- Função principal para executar o script ---
def main():
    id_peca_para_buscar = input("Digite o ID da peça do Authomix (ex: 5042ecad-dbcb-92314cc6-2fb6-6b213869-a827): ")

    if not id_peca_para_buscar:
        print("ID da peça não pode ser vazio.")
        return

    # Solicitar ao usuário quais campos incluir
    print("\nEscolha as informações que deseja incluir na aplicação (separadas por vírgula):")
    print("Opções disponíveis: marca, modelo, motor, ano, observacao, sistema_freio, restricao, apenas")
    print("Exemplo: marca, modelo, ano, observacao")
    
    user_input_fields = input("Suas opções: ").strip().lower()
    
    # Validar e processar as opções do usuário
    available_fields = ['marca', 'modelo', 'motor', 'ano', 'observacao', 'sistema_freio', 'restricao', 'apenas']
    requested_fields = []

    if not user_input_fields:
        print("Nenhuma opção selecionada. Usando padrão: marca, modelo, ano.")
        requested_fields = ['marca', 'modelo', 'ano']
    else:
        for field in user_input_fields.split(','):
            field = field.strip()
            if field in available_fields:
                requested_fields.append(field)
            else:
                print(f"Aviso: '{field}' não é uma opção válida e será ignorada.")
        
        if not requested_fields: # Se o usuário digitou opções inválidas
            print("Nenhuma opção válida selecionada. Usando padrão: marca, modelo, ano.")
            requested_fields = ['marca', 'modelo', 'ano']

    aplicacoes = buscar_aplicacoes_authomix_graphql(id_peca_para_buscar, requested_fields)

    if aplicacoes:
        # Ordenar as aplicações alfabeticamente
        aplicacoes_ordenadas = sorted(aplicacoes)

        print("\nAplicações encontradas e formatadas:")
        # Usar \r\n para compatibilidade com sistemas Windows/Delphi 7
        texto_para_copiar = "*** APLICAÇÃO ***\r\n" 
        for app in aplicacoes_ordenadas: # Iterar sobre a lista ordenada
            print(app)
            texto_para_copiar += app + "\r\n" # Usar \r\n aqui também
        
        try:
            # O .strip() remove a última quebra de linha extra no final, se houver
            pyperclip.copy(texto_para_copiar.strip())
            print("\nTexto copiado para a área de transferência! (Ctrl+V para colar no seu sistema)")
        except pyperclip.PyperclipException:
            print("\nNão foi possível copiar para a área de transferência. Certifique-se de que 'pyperclip' está instalado e funcionando.")
            print("Você pode copiar o texto acima manualmente.")
    else:
        print("Nenhuma aplicação encontrada ou erro na busca para esta peça no Authomix.")

if __name__ == "__main__":
    main()
