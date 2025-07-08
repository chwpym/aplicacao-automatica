# Catálogo Automotivo Manus

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
├── app.py                # Arquivo principal da aplicação
├── providers/            # Módulos dos provedores (REST, SOAP, GraphQL, PDF)
├── config/               # Arquivos de configuração e backups
├── assets/               # Imagens e recursos visuais
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## Contribuição

Pull requests são bem-vindos! Para grandes mudanças, abra uma issue antes para discutir o que você gostaria de modificar.

## Licença

[MIT](LICENSE) 