import tkinter as tk
from tkinter import ttk

class SearchBar(ttk.Frame):
    def __init__(self, parent, on_search_callback):
        super().__init__(parent)
        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.button = ttk.Button(self, text="Buscar", command=self._on_search)
        self.button.pack(side=tk.LEFT)
        self.on_search_callback = on_search_callback

    def _on_search(self):
        termo = self.entry.get()
        if self.on_search_callback:
            self.on_search_callback(termo) 