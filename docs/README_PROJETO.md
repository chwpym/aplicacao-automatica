# Gerenciador de Aplicações de Peças

Uma aplicação Python com interface gráfica para buscar e gerenciar aplicações de peças automotivas de diferentes provedores de dados.

## Funcionalidades

- **Busca de Aplicações**: Busca aplicações de peças por ID em múltiplos provedores
- **Provedores Suportados**:
  - **Authomix**: API GraphQL
  - **Sabo**: API GraphQL  
  - **Catálogo Nakata**: API REST com parsing HTML
- **Gerenciamento de Siglas**: Sistema para mapear nomes completos de marcas para siglas
- **Filtros de Palavras**: Remove palavras/frases específicas dos resultados
- **Exportação**: Exporta resultados para CSV ou copia para área de transferência
- **Temas**: Interface com múltiplos temas visuais
- **Tabelas Estruturadas**: Exibe resultados em tabelas organizadas

## Instalação

1. Clone ou baixe o projeto
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Dependências

- `requests`: Para requisições HTTP
- `pyperclip`: Para copiar dados para área de transferência
- `ttkthemes`: Para temas visuais
- `beautifulsoup4`: Para parsing HTML (provedores REST)
- `lxml`: Parser XML/HTML para BeautifulSoup

## Como Usar

### Executar a Aplicação
```bash
python src/app_catalogo.py
```

### Buscar Aplicações
1. Digite o ID da peça no campo "ID da Peça"
2. Selecione o provedor desejado
3. Marque os campos que deseja incluir nos resultados
4. Clique em "Buscar Aplicações"

### Gerenciar Provedores
- Acesse **Ações > Gerenciar Provedores**
- Adicione, edite ou remova provedores
- Configure URLs, headers e tipos de API

### Provedor Nakata
O provedor Nakata usa uma API REST que retorna páginas HTML. A aplicação faz parsing automático do HTML para extrair:
- Marca do veículo
- Modelo
- Ano de fabricação
- Motor

**URL Padrão**: `https://www.nakata.com.br/catalogo/aplicacao/{id}`

### Gerenciar Siglas
- Acesse **Ações > Gerenciar Siglas**
- Adicione mapeamentos de nomes completos para siglas
- Ex: "VOLKSWAGEN" → "VW"

### Gerenciar Palavras para Remover
- Acesse **Ações > Gerenciar Palavras para Remover**
- Configure palavras/frases que devem ser removidas de campos específicos
- Útil para limpar dados desnecessários

### Exportar Dados
- **Copiar Texto Formatado**: Copia aplicações formatadas para área de transferência
- **Copiar Tabela em Texto**: Copia tabela formatada para área de transferência
- **Exportar para CSV**: Salva dados em arquivo CSV

## Estrutura de Diretórios

```
├── src/                  # Código-fonte principal
│   ├── app_catalogo.py         # Arquivo principal
│   ├── app_catalogo_bkp.py     # Backup do código anterior
│   └── authomix_scraper.py
├── tests/                # Testes automatizados e diagnósticos
│   ├── test_caixa_alta.py
│   ├── test_formato.py
│   ├── test_nakata.py
│   ├── test_providers.py
│   └── diagnostico_*.txt
├── docs/                 # Documentação, exemplos e scripts auxiliares
│   ├── README.md
│   ├── README_PROJETO.md
│   ├── GUIA_PROVEDORES_LOCAIS.md
│   ├── GUIA_CORRECOES.md
│   ├── DISTRIBUICAO.md
│   ├── COMO_INSTALAR.md
│   ├── README_INSTALACAO.md
│   ├── RESUMO_NAKATA.md
│   ├── ajuda_provedores.md
│   ├── exemplo_nakata.json
│   ├── nakata_debug.html
│   ├── installer.py
│   ├── diagnostico.py
│   ├── instalar.bat
│   ├── atualizar.bat
│   ├── desinstalar.bat
│   └── uninstall.py
├── provedores.json       # Configuração de provedores de dados (usado pelo sistema)
├── siglas.json           # Configuração de siglas de marcas (usado pelo sistema)
├── palavras_remover.json # Configuração de palavras para remover (usado pelo sistema)
├── requirements.txt      # Dependências do projeto
└── ...                   # Outros arquivos
```

> **Atenção:** Os arquivos `provedores.json`, `siglas.json`, `palavras_remover.json` e `requirements.txt` devem estar na raiz do projeto, pois o sistema os acessa diretamente.

## Provedores REST

Para adicionar novos provedores REST:

1. Configure o provedor no gerenciador
2. Defina o tipo como "rest"
3. Use `{id}` na URL para substituir pelo ID da peça
4. A aplicação fará parsing automático do HTML

### Exemplo de Configuração REST:
```json
{
  "nome": "Meu Provedor",
  "url": "https://exemplo.com/aplicacao/{id}",
  "tipo": "rest",
  "ativo": true,
  "headers": {
    "origin": "https://exemplo.com",
    "referer": "https://exemplo.com/"
  }
}
```

## Suporte

Para problemas ou dúvidas:
1. Verifique se todas as dependências estão instaladas
2. Confirme se o ID da peça está correto
3. Teste com diferentes provedores
4. Verifique a conectividade com a internet

## Desenvolvimento

A aplicação é modular e extensível:
- Novos provedores podem ser adicionados facilmente
- Novos tipos de parsing podem ser implementados
- Novos campos podem ser adicionados aos resultados 