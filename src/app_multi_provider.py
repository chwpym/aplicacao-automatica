import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from multi_provider.aggregator import buscar_multi_provedores, agrupar_aplicacoes_por_modelo_ano
from utils.config import load_provedores
from interface.layout_system import center_window

def get_provedores_ativos():
    provedores = load_provedores()
    return [p['nome'] for p in provedores.values() if p.get('ativo', False)]

class BuscaFrame(ttk.Frame):
    def __init__(self, master, remove_callback, provedores):
        super().__init__(master)
        self.codigo_var = tk.StringVar()
        self.provedor_var = tk.StringVar(value=provedores[0] if provedores else "")
        ttk.Label(self, text="Código:").pack(side="left")
        ttk.Entry(self, textvariable=self.codigo_var, width=18).pack(side="left", padx=2)
        ttk.Label(self, text="Provedor:").pack(side="left")
        ttk.Combobox(self, textvariable=self.provedor_var, values=provedores, width=18, state="readonly").pack(side="left", padx=2)
        btn_remover = ttk.Button(self, text="Remover", command=self._remover)
        btn_remover.pack(side="left", padx=2)
        self.remove_callback = remove_callback
    def _remover(self):
        self.remove_callback(self)
    def get_busca(self):
        return {"codigo": self.codigo_var.get().strip(), "provedor": self.provedor_var.get().strip()}

class MultiProviderTestApp(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__()
        self.title("Teste Multi-Provedores Dinâmico")
        self.geometry("1100x600")
        center_window(self, 1100, 600)
        self.busca_frames = []
        self.provedores = get_provedores_ativos()
        self.create_widgets()
    def create_widgets(self):
        frame_top = ttk.Frame(self)
        frame_top.pack(padx=10, pady=10, fill="x")
        btn_add = ttk.Button(frame_top, text="Adicionar Busca", command=self.add_busca_frame)
        btn_add.pack(side="left")
        btn_buscar = ttk.Button(frame_top, text="Buscar", command=self.buscar)
        btn_buscar.pack(side="left", padx=5)
        btn_buscar_agrupado = ttk.Button(frame_top, text="Buscar (Agrupado)", command=self.buscar_agrupado)
        btn_buscar_agrupado.pack(side="left", padx=5)
        self.buscas_container = ttk.Frame(self)
        self.buscas_container.pack(padx=10, pady=5, fill="x")
        # Adiciona dois campos de busca por padrão
        self.add_busca_frame()
        self.add_busca_frame()
        self.tree = ttk.Treeview(self, columns=("montadora", "modelo", "motores", "ano_inicio", "ano_fim", "observacoes", "fontes"), show="headings")
        for col, label in zip(self.tree["columns"], ["Montadora", "Modelo", "Motores", "Ano Início", "Ano Fim", "Obs.", "Fontes"]):
            self.tree.heading(col, text=label)
            self.tree.column(col, width=140, anchor="w")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.txt_log = scrolledtext.ScrolledText(self, height=5)
        self.txt_log.pack(padx=10, pady=5, fill="x")
    def add_busca_frame(self):
        frame = BuscaFrame(self.buscas_container, self.remove_busca_frame, self.provedores)
        frame.pack(pady=2, fill="x")
        self.busca_frames.append(frame)
    def remove_busca_frame(self, frame):
        frame.destroy()
        self.busca_frames.remove(frame)
    def buscar(self):
        buscas = [f.get_busca() for f in self.busca_frames if f.get_busca()["codigo"]]
        if not buscas:
            messagebox.showwarning("Entrada Inválida", "Adicione pelo menos uma busca com código.")
            return
        self.tree.delete(*self.tree.get_children())
        self.txt_log.delete(1.0, tk.END)
        try:
            resultados = buscar_multi_provedores(buscas)
            if not resultados:
                self.txt_log.insert(tk.END, "Nenhuma aplicação encontrada.\n")
                return
            for r in resultados:
                self.tree.insert("", "end", values=(
                    r.get("montadora", ""),
                    r.get("modelo", ""),
                    r.get("motor", ""),
                    r.get("configuracao_motor", ""),
                    r.get("ano_inicio", ""),
                    r.get("ano_fim", ""),
                    r.get("observacao", ""),
                    r.get("fonte", ""),
                    r.get("_provedor", "")
                ))
            self.txt_log.insert(tk.END, f"{len(resultados)} aplicações agregadas.\n")
        except Exception as e:
            self.txt_log.insert(tk.END, f"Erro: {e}\n")
            messagebox.showerror("Erro", str(e))
    def buscar_agrupado(self):
        buscas = [f.get_busca() for f in self.busca_frames if f.get_busca()["codigo"]]
        if not buscas:
            messagebox.showwarning("Entrada Inválida", "Adicione pelo menos uma busca com código.")
            return
        self.tree.delete(*self.tree.get_children())
        self.txt_log.delete(1.0, tk.END)
        try:
            resultados = buscar_multi_provedores(buscas)
            agrupados = agrupar_aplicacoes_por_modelo_ano(resultados)
            if not agrupados:
                self.txt_log.insert(tk.END, "Nenhuma aplicação encontrada.\n")
                return
            for r in agrupados:
                self.tree.insert("", "end", values=(
                    r.get("montadora", ""),
                    r.get("modelo", ""),
                    r.get("motores", ""),
                    r.get("ano_inicio", ""),
                    r.get("ano_fim", ""),
                    r.get("observacoes", ""),
                    r.get("fontes", "")
                ))
            self.txt_log.insert(tk.END, f"{len(agrupados)} aplicações agrupadas.\n")
        except Exception as e:
            self.txt_log.insert(tk.END, f"Erro: {e}\n")
            messagebox.showerror("Erro", str(e))

'''if __name__ == "__main__":
    app = MultiProviderTestApp()
    app.mainloop() '''