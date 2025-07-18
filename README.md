# Catálogo Automotivo

Sistema desktop em Python para consulta de catálogos automotivos, integrando múltiplos provedores de dados (REST, GraphQL, SOAP, HTML e PDFs locais), com interface gráfica Tkinter.

## Funcionalidades
- Busca de peças e aplicações em múltiplos provedores (REST, GraphQL, SOAP, PDF local)
- Limpeza avançada de palavras/frases nos resultados
- Backup automático dos arquivos de configuração ao fechar o app
- Busca em PDFs locais com seleção de arquivos pela interface
- Interface intuitiva com Tkinter
- Suporte a novos provedores de forma modular

## Instalação

1. **Clone o repositório:**
   ```sh
   git clone git@github.com:chwpym/aplicacao-automatica.git
   cd aplicacao-automatica
   ```

2. **(Opcional) Crie um ambiente virtual:**
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
   python src/app_catalogo.py
   ```
   ou rode o executável gerado (`app_catalogo.exe`) na pasta `dist`.

## Como usar
- Selecione o(s) provedor(es) desejado(s) na interface.
- Realize buscas por código, descrição ou aplicação.
- Para PDFs locais, selecione os arquivos desejados na lista.
- O sistema faz backup automático dos arquivos de configuração ao fechar.

## Provedores Especiais
- Provedores como **DS**, **Iguaçu** e **MTE Thomson** usam tipos específicos ("ds", "iguacu", "mte_thomson").
- Para cadastrar esses provedores pela interface, adicione o tipo correspondente no ComboBox de tipo de provedor.
- Os arquivos de configuração (`provedores.json`, `siglas.json`, `palavras_remover.json`) devem estar na mesma pasta do `.exe` para o sistema funcionar corretamente.

## Ativação/Desativação de Provedores
Os provedores disponíveis no sistema são configurados no arquivo `provedores.json` na raiz do projeto. Para ativar ou desativar um provedor:

1. Abra o arquivo `provedores.json` em um editor de texto.
2. Localize o bloco do provedor desejado. Exemplo para o Iguaçu:
   ```json
   "iguacu": {
       "nome": "Iguaçu",
       "tipo": "iguacu",
       "ativo": true
   }
   ```
3. Para **ativar** o provedor, defina `"ativo": true`.
4. Para **desativar** o provedor, defina `"ativo": false`.
5. Salve o arquivo e reinicie a aplicação para que a alteração tenha efeito.

> **Observação:** Apenas provedores com `"ativo": true` aparecem na lista de seleção da interface.

## Atualização de Dados
- Para atualizar provedores, siglas ou palavras para remover, basta substituir os arquivos `.json` na mesma pasta do `.exe`.
- Não é necessário recompilar o `.exe` para atualizar dados.

## Backup Automático
- O sistema faz backup automático dos arquivos de configuração ao fechar.
- Os backups ficam na pasta `backups/`.

## Estrutura do Projeto
```
aplicação_script/
├── providers/                # Parsers e provedores customizados
├── utils/                    # Utilitários e funções auxiliares
├── src/
│   └── app_catalogo.py       # Arquivo principal
├── provedores.json           # Configuração de provedores
├── siglas.json               # Configuração de siglas de marcas
├── palavras_remover.json     # Palavras para remover
├── requirements.txt          # Dependências do projeto
├── icons-apllication.ico     # Ícone do sistema
└── ...
```

## Dependências (requirements.txt)
- requests>=2.25.1
- pyperclip>=1.8.2
- ttkthemes>=3.2.2
- beautifulsoup4>=4.9.3
- lxml>=4.6.3

## Geração do Executável (.exe)
Para gerar o `.exe` com PyInstaller:

```sh
pyinstaller --noconfirm --onefile --windowed \
  --add-data "provedores.json;." \
  --add-data "siglas.json;." \
  --add-data "palavras_remover.json;." \
  --icon=icons-apllication.ico \
  --paths=. \
  src/app_catalogo.py
```
- O `.exe` será criado na pasta `dist`.
- Os arquivos `.json` e o ícone devem estar juntos do `.exe`.

## Compatibilidade com PyInstaller
Para garantir que os arquivos de dados sejam encontrados tanto no modo script quanto no modo `.exe`, use a função:

```python
import sys, os

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
```
E use `resource_path("provedores.json")` ao abrir os arquivos.

## Suporte
- Para dúvidas ou problemas, consulte a documentação ou entre em contato com o desenvolvedor.

---
**Versão:** 1.0
**Data:** 2025
