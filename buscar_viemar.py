from playwright.sync_api import sync_playwright

def buscar_viemar():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Abre o navegador visível
        page = browser.new_page()
        page.goto("https://catalogo.viemar.com.br/")

        print("ATENÇÃO:")
        print("1. Digite o código da peça (ex: 680730) no campo de busca.")
        print("2. Clique na lupa ou pressione Enter.")
        print("3. Aguarde os resultados aparecerem na tabela.")
        print("4. Volte ao terminal e pressione ENTER para extrair os dados.")
        input()

        # Extrai os dados da tabela
        linhas = page.query_selector_all('table tbody tr')
        for linha in linhas:
            colunas = linha.query_selector_all('td')
            dados = [col.inner_text().strip() for col in colunas]
            print(dados)

        browser.close()

if __name__ == "__main__":
    buscar_viemar()