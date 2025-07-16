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

## Como ativar/desativar provedores (exemplo: Iguaçu)

Os provedores disponíveis no sistema são configurados no arquivo `provedores.json` na raiz do projeto. Para ativar ou desativar um provedor (por exemplo, o Iguaçu) na interface gráfica:

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

## Como ativar/desativar provedores (exemplo: MTE Thomson)

O provedor MTE Thomson também pode ser ativado ou desativado no arquivo `provedores.json`:

```json
"mte_thomson": {
    "nome": "MTE",
    "tipo": "mte_thomson",
    "ativo": true
}
```

- Para **ativar** o provedor, defina `"ativo": true`.
- Para **desativar** o provedor, defina `"ativo": false`.
- Salve o arquivo e reinicie a aplicação para que a alteração tenha efeito.

> **Observação:** O provedor MTE Thomson permite buscar aplicações diretamente do catálogo online da MTE. Apenas provedores com `"ativo": true` aparecem na lista de seleção da interface.

## Estrutura do Projeto

```