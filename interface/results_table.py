import tkinter as tk
from tkinter import ttk

class ResultsTable(ttk.Frame):
    def __init__(self, parent, columns=None):
        super().__init__(parent)
        self.columns = columns or [
            'brand', 'name', 'model', 'engineName', 'engineConfiguration',
            'brakeSystem', 'startYear', 'endYear', 'note', 'only', 'restriction'
        ]
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def set_data(self, data):
        # Limpa dados antigos
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insere novos dados
        for item in data:
            values = [item.get(col, '') for col in self.columns]
            self.tree.insert('', tk.END, values=values) 