import sys
import os
from tkinter import scrolledtext, messagebox, ttk, filedialog


def buscar_viemar_playwright(codigo):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        messagebox.showerror(
            "Dependência Ausente",
            "Playwright não está instalado. Instale com: pip install playwright",
        )
        return []
    campos = [
        "linha_produto",
        "veiculo",
        "ano",
        "posicao",
        "detalhes",
        "referencia_cruzada",
        "referencia",
        "imagem",
        "informacoes",
        "onde_comprar",
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://catalogo.viemar.com.br/")
        messagebox.showinfo(
            "Viemar",
            "Digite o código, clique na lupa e aguarde os resultados.\n\nQuando a tabela aparecer, volte ao app e clique em OK para extrair os dados.",
        )
        linhas = page.query_selector_all("table tbody tr")
        lista_dicts = []
        for linha in linhas:
            colunas = linha.query_selector_all("td")
            dados = [col.inner_text().strip() for col in colunas]
            lista_dicts.append(dict(zip(campos, dados)))
        browser.close()
    # Adapta para o formato padrão do app
    vehicles = []
    for item in lista_dicts:
        vehicles.append(
            {
                "brand": item.get("veiculo", "").replace("\n", " "),
                "name": item.get("linha_produto", ""),
                "model": item.get("linha_produto", ""),
                "engineName": "",
                "engineConfiguration": "",
                "startYear": item.get("ano", ""),
                "endYear": item.get("ano", ""),
                "note": item.get("referencia_cruzada", ""),
                "only": "",
                "restriction": "",
                "position": item.get("posicao", "").replace("\n", " "),
                "side": "",
                "steering": "",
            }
        )
    return vehicles
