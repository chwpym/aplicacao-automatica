# Catálogo Automotivo 

Sistema desktop em Python para consulta de catálogos automotivos, integrando múltiplos provedores de dados (REST, GraphQL, SOAP e PDFs locais), com interface gráfica Tkinter.

## Funcionalidades

- **Busca de peças e aplicações** em múltiplos provedores (REST, GraphQL, SOAP, PDF local)
- **Limpeza avançada de palavras/frases** nos resultados
- **Backup automático** dos arquivos de configuração ao fechar o app
- **Busca em PDFs locais** com seleção de arquivos pela interface
- **Interface intuitiva** com Tkinter
- **Suporte a novos provedores** de forma modular

## Instalação

1. **Clone o repositório:**
   ```sh
   git clone git@github.com:chwpym/aplicacao-automatica.git
   cd aplicacao-automatica
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Execute o sistema:**
   ```sh
   python app.py
   ```

## Como usar

- Selecione o(s) provedor(es) desejado(s) na interface.
- Realize buscas por código, descrição ou aplicação.
- Para PDFs locais, selecione os arquivos desejados na lista.
- O sistema faz backup automático dos arquivos de configuração ao fechar.

## Estrutura do Projeto

```
aplicacao-automatica/
│
├── src/
│   └── app_catalogo.py         # Arquivo principal da aplicação
│
├── providers/                  # Módulos dos provedores (REST, GraphQL, PDF, etc.)
│   ├── rest.py
│   ├── graphql.py
│   ├── generic_provider.py
│   ├── ...
│
├── interface/                  # Componentes da interface gráfica (Tkinter)
│   ├── main_window.py
│   ├── results_table.py
│   ├── search_bar.py
│   └── layout_system.py
│
├── utils/                      # Utilitários e funções auxiliares
│   ├── config.py
│   ├── backup.py
│   └── limpeza.py
│
├── backups/                    # Backups automáticos dos arquivos de configuração
│
├── docs/                       # Documentação e scripts auxiliares
│
├── tests/                      # Testes automatizados
│   ├── test_nakata.py
│   ├── test_providers.py
│   └── ...
│
├── catalogos_pdf/              # Catálogos PDF locais para busca
│
├── palavras_remover.json       # Lista de palavras/frases para limpeza
├── provedores.json             # Configuração dos provedores
├── siglas.json                 # Mapa de siglas
├── requirements.txt            # Dependências do projeto
└── README.md                   # Este arquivo
```

## Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue antes para discutir o que você gostaria de modificar.

## Licença

[MIT](LICENSE) 