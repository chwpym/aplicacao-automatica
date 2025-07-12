"""
Módulo responsável pela janela principal da interface gráfica (Tkinter).
Aqui será implementada a classe MainWindow e widgets customizados.
"""
import tkinter as tk
from tkinter import ttk
from .layout_system import center_window
from .search_bar import SearchBar
from .results_table import ResultsTable
from utils.config import load_provedores
from src.app_catalogo import buscar_provedor_generico

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catálogo de Aplicações")
        self.geometry("1200x800")
        center_window(self, 1200, 800)
        self.provedores = load_provedores()
        self._create_widgets()
        self._configure_layout()

    def _create_widgets(self):
        # ComboBox para seleção de provedor
        self.provedor_var = tk.StringVar()
        provedores_ativos = [p['nome'] for p in self.provedores.values() if p.get('ativo')]
        self.provedor_combo = ttk.Combobox(self, textvariable=self.provedor_var, values=provedores_ativos, state='readonly')
        if provedores_ativos:
            self.provedor_combo.current(0)
        self.provedor_combo.pack(fill=tk.X, padx=10, pady=(10, 0))

        self.search_bar = SearchBar(self, self.on_search)
        self.search_bar.pack(fill=tk.X, padx=10, pady=10)
        self.results_table = ResultsTable(self)
        self.results_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))
        # Aqui você irá instanciar e posicionar outros componentes principais
        pass

    def _configure_layout(self):
        # Defina o layout (grid, pack, place) dos widgets principais
        pass

    def on_search(self, termo):
        provedor_nome = self.provedor_var.get()
        provedor_config = next((p for p in self.provedores.values() if p['nome'] == provedor_nome), None)
        if not provedor_config:
            print("Provedor não encontrado!")
            return
        resultados = buscar_provedor_generico(termo, provedor_config)
        self.results_table.set_data(resultados)

    def run(self):
        self.mainloop() 