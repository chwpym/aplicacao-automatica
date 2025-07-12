import sys
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
import requests
import pyperclip
import json
import os
import csv
from ttkthemes import ThemedTk
import re
from bs4 import BeautifulSoup
import subprocess
import pdfplumber
from providers.rest import RESTProvider, buscar_provedor_generico
from providers.rest_parsers import (
    parse_wega_json,
    parse_ano_inicio,
    parse_ano_fim,
    parse_nakata_html,
    parse_nakata_html_legacy,
    extract_vehicle_info_from_text,
    parse_viemar_json,
    parse_generic_json,
    parse_generic_html,
    parse_schadek_json
)
from utils.config import (
    load_siglas, save_siglas,
    load_palavras_remover, save_palavras_remover,
    load_provedores, save_provedores,
    merge_year_ranges_overall, parse_ano_inicio, parse_ano_fim
)
from utils.limpeza import remover_palavras_avancado
from interface.layout_system import center_window
from providers.pdf import PDFProvider
#from providers.graphql import AuthomixGraphQLProvider
from providers import GenericGraphQLProvider
from providers.viemar import buscar_viemar_playwright

# --- Configuração do arquivo de siglas ---
SIGLAS_FILE = "siglas.json"

# --- Configuração do arquivo de palavras a remover ---
PALAVRAS_REMOVER_FILE = "palavras_remover.json"

# --- Configuração do arquivo de provedores ---
PROVEDORES_FILE = "provedores.json"

#TINHA FUNÇOES  E ESTA NO ARQUIVO TXT COPIA DAS FUNÇÕES COMENTADAS, ESSA PARTA FOI MODULARIZADA

def parse_generic_rest_html(soup):
    """Parse genérico para outros provedores REST"""
    vehicles = []
    
    try:
        # Procura por padrões comuns em páginas de aplicação de peças
        text = soup.get_text()
        
        # Extrai informações usando regex
        # Marca
        marca_match = re.search(r'\b(VW|FIAT|GM|FORD|CHEVROLET|HONDA|TOYOTA|HYUNDAI|NISSAN|RENAULT|PEUGEOT|CITROEN|BMW|MERCEDES|AUDI|VOLVO|SCANIA|IVECO|MERCEDES-BENZ)\b', text, re.IGNORECASE)
        marca = marca_match.group(1) if marca_match else ''
        
        # Modelo
        modelo_match = re.search(r'\b(GOL|PALIO|CORSA|CIVIC|COROLLA|HB20|SENTRA|CLIO|208|C3|X1|CLASSE|A3|S40|FH|DAILY|SPRINTER)\b', text, re.IGNORECASE)
        modelo = modelo_match.group(1) if modelo_match else ''
        
        # Ano
        ano_match = re.search(r'\b(19|20)\d{2}(?:[-/](19|20)\d{2})?\b', text)
        ano_str = ano_match.group(0) if ano_match else ''
        
        # Motor
        motor_match = re.search(r'\b\d+\.\d+\b', text)
        motor = motor_match.group(0) if motor_match else ''
        
        if marca or modelo or ano_str:
            vehicle = {
                'brand': marca,
                'name': modelo,
                'model': modelo,
                'engineName': motor,
                'engineConfiguration': '',
                'startYear': None,
                'endYear': None,
                'note': '',
                'only': '',
                'restriction': ''
            }
            
            # Processa o ano
            if ano_str:
                if '-' in ano_str or '/' in ano_str:
                    years = re.findall(r'\d{4}', ano_str)
                    if len(years) >= 2:
                        vehicle['startYear'] = int(years[0])
                        vehicle['endYear'] = int(years[1])
                    elif len(years) == 1:
                        vehicle['startYear'] = int(years[0])
                else:
                    vehicle['startYear'] = int(ano_str)
            
            vehicles.append(vehicle)
    
    except Exception as e:
        print(f"Erro ao fazer parsing genérico do HTML: {e}")
    
    return vehicles

# --- CLASSE PARA GERENCIAR SIGLAS ---
class SiglaManager(tk.Toplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.title("Gerenciar Siglas de Marcas")
        center_window(self, 500, 500)
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.save_and_close)

        self.siglas = load_siglas()
        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        input_frame = tk.LabelFrame(self, text="Adicionar/Editar Sigla", padx=10, pady=10)
        input_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(input_frame, text="Nome Completo:").grid(row=0, column=0, sticky="w", pady=2)
        self.full_name_entry = tk.Entry(input_frame, width=40)
        self.full_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        tk.Label(input_frame, text="Sigla:").grid(row=1, column=0, sticky="w", pady=2)
        self.acronym_entry = tk.Entry(input_frame, width=40)
        self.acronym_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        btn_add = tk.Button(input_frame, text="Adicionar", command=self.add_sigla)
        btn_add.grid(row=2, column=0, pady=5)
        btn_update = tk.Button(input_frame, text="Atualizar Selecionado", command=self.update_sigla)
        btn_update.grid(row=2, column=1, pady=5)

        self.tree = ttk.Treeview(self, columns=("Nome Completo", "Sigla"), show="headings")
        self.tree.heading("Nome Completo", text="Nome Completo")
        self.tree.heading("Sigla", text="Sigla")
        self.tree.column("Nome Completo", width=200)
        self.tree.column("Sigla", width=100)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.load_selected_sigla)

        action_frame = tk.Frame(self)
        action_frame.pack(pady=5, fill="x") 

        btn_delete = tk.Button(action_frame, text="Excluir Selecionado", command=self.delete_sigla)
        btn_delete.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        btn_save_close = tk.Button(action_frame, text="Salvar e Fechar", command=self.save_and_close)
        btn_save_close.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)

    def populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for full_name, acronym in sorted(self.siglas.items()):
            self.tree.insert("", "end", values=(full_name, acronym))

    def add_sigla(self):
        full_name = self.full_name_entry.get().strip().upper()
        acronym = self.acronym_entry.get().strip()

        if not full_name or not acronym:
            messagebox.showwarning("Entrada Inválida", "Nome completo e sigla não podem ser vazios.")
            return
        
        if full_name in self.siglas:
            if not messagebox.askyesno("Sigla Existente", f"'{full_name}' já existe. Deseja atualizar a sigla para '{acronym}'?"):
                return

        self.siglas[full_name] = acronym
        self.populate_tree()
        self.clear_entries()
        messagebox.showinfo("Sucesso", "Sigla adicionada/atualizada.")

    def update_sigla(self):
        selected_item_ids = self.tree.selection()
        if not selected_item_ids:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma sigla para atualizar.")
            return
        
        selected_item_id = selected_item_ids[0] 
        
        old_full_name = self.tree.item(selected_item_id, 'values')[0]
        new_full_name = self.full_name_entry.get().strip().upper()
        new_acronym = self.acronym_entry.get().strip()

        if not new_full_name or not new_acronym:
            messagebox.showwarning("Entrada Inválida", "Nome completo e sigla não podem ser vazios.")
            return
        
        if old_full_name != new_full_name: 
            if old_full_name in self.siglas:
                del self.siglas[old_full_name]

        self.siglas[new_full_name] = new_acronym
        self.populate_tree()
        self.clear_entries()
        messagebox.showinfo("Sucesso", "Sigla atualizada.")

    def delete_sigla(self):
        selected_item_ids = self.tree.selection()
        if not selected_item_ids:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma sigla para excluir.")
            return
        
        selected_item_id = selected_item_ids[0]

        full_name_to_delete = self.tree.item(selected_item_id, 'values')[0]
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a sigla para '{full_name_to_delete}'?"):
            if full_name_to_delete in self.siglas:
                del self.siglas[full_name_to_delete]
                self.populate_tree()
                self.clear_entries()
                messagebox.showinfo("Sucesso", "Sigla excluída.")
            else:
                messagebox.showwarning("Erro", "Sigla não encontrada para exclusão.")

    def load_selected_sigla(self, event):
        selected_item_ids = self.tree.selection()
        if selected_item_ids:
            selected_item_id = selected_item_ids[0] 
            values = self.tree.item(selected_item_id, 'values')
            self.full_name_entry.delete(0, tk.END)
            self.full_name_entry.insert(0, values[0])
            self.acronym_entry.delete(0, tk.END)
            self.acronym_entry.insert(0, values[1])

    def clear_entries(self):
        self.full_name_entry.delete(0, tk.END)
        self.acronym_entry.delete(0, tk.END)

    def save_and_close(self):
        save_siglas(self.siglas)
        self.on_save_callback()
        self.destroy()

# --- Classe para gerenciar palavras a remover (mover para antes do Application) ---
class PalavrasRemoverManager(tk.Toplevel):
    def __init__(self, parent, campos, on_save_callback):
        super().__init__(parent)
        self.parent = parent
        self.campos = list(campos)  # lista de campos possíveis
        self.on_save_callback = on_save_callback
        self.title("Gerenciar Palavras para Remover")
        center_window(self, 400, 400)
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.save_and_close)

        self.palavras_remover = load_palavras_remover()
        if not self.palavras_remover:
            # Inicializa com campos vazios
            for campo in self.campos:
                self.palavras_remover[campo] = []

        self.selected_campo = tk.StringVar(value=self.campos[0])
        self.create_widgets()
        self.populate_listbox()

    def create_widgets(self):
        frame_top = tk.Frame(self, bg="#f0f4f8")
        frame_top.pack(padx=10, pady=10, fill="x")
        tk.Label(frame_top, text="Campo:", bg="#f0f4f8", fg="#333").pack(side="left")
        self.combo_campo = ttk.Combobox(frame_top, textvariable=self.selected_campo, values=self.campos, state="readonly")
        self.combo_campo.pack(side="left", padx=5)
        self.combo_campo.bind("<<ComboboxSelected>>", lambda e: self.populate_listbox())

        frame_list = tk.LabelFrame(self, text="Palavras/frases cadastradas", bg="#e3eaf2", fg="#222")
        frame_list.pack(padx=10, pady=10, fill="both", expand=True)
        self.listbox = tk.Listbox(frame_list, bg="#fff", fg="#222")
        self.listbox.pack(fill="both", expand=True, padx=5, pady=5)

        btn_remove = tk.Button(frame_list, text="Remover Selecionado", command=self.remove_selected, bg="#e57373", fg="#fff", activebackground="#c62828")
        btn_remove.pack(pady=5)

        frame_add = tk.Frame(self, bg="#f0f4f8")
        frame_add.pack(padx=10, pady=5, fill="x")
        tk.Label(frame_add, text="Nova palavra/frase:", bg="#f0f4f8", fg="#333").pack(side="left")
        self.entry_nova = tk.Entry(frame_add)
        self.entry_nova.pack(side="left", padx=5, fill="x", expand=True)
        btn_add = tk.Button(frame_add, text="Adicionar", command=self.add_palavra, bg="#64b5f6", fg="#fff", activebackground="#1976d2")
        btn_add.pack(side="left", padx=5)

        btn_save = tk.Button(self, text="Salvar e Fechar", command=self.save_and_close, bg="#388e3c", fg="#fff", activebackground="#1b5e20")
        btn_save.pack(pady=10)

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        campo = self.selected_campo.get()
        for palavra in self.palavras_remover.get(campo, []):
            self.listbox.insert(tk.END, palavra)

    def add_palavra(self):
        campo = self.selected_campo.get()
        nova = self.entry_nova.get().strip()
        if not nova:
            messagebox.showwarning("Entrada Inválida", "Digite uma palavra ou frase para adicionar.")
            return
        if campo not in self.palavras_remover:
            self.palavras_remover[campo] = []
        if nova in self.palavras_remover[campo]:
            messagebox.showinfo("Já Existe", "Esta palavra/frase já está cadastrada para este campo.")
            return
        self.palavras_remover[campo].append(nova)
        self.populate_listbox()
        self.entry_nova.delete(0, tk.END)

    def remove_selected(self):
        campo = self.selected_campo.get()
        selecionado = self.listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma palavra/frase para remover.")
            return
        idx = selecionado[0]
        palavra = self.listbox.get(idx)
        if campo not in self.palavras_remover:
            self.palavras_remover[campo] = []
        self.palavras_remover[campo].remove(palavra)
        self.populate_listbox()

    def save_and_close(self):
        save_palavras_remover(self.palavras_remover)
        self.on_save_callback()
        self.destroy()

# --- Classe para gerenciar provedores (mover para antes do Application) ---
class ProvedorManager(tk.Toplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.title("Gerenciar Provedores de Dados")
        center_window(self, 900, 700)
        self.grab_set()
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.save_and_close)

        self.provedores = load_provedores()
        if not self.provedores:
            # Inicializa com provedores padrão
            self.provedores = {
                "authomix": {
                    "nome": "Authomix",
                    "url": "https://bff.catalogofraga.com.br/gateway/graphql",
                    "ativo": True,
                    "tipo": "graphql",
                    "headers": {
                        "origin": "https://catalogo.authomix.com.br",
                        "referer": "https://catalogo.authomix.com.br/"
                    },
                    "query": """query GetProductById($id: String!, $market: MarketType!) {
  product(id: $id, market: $market) {
    vehicles {
      brand
      name
      model
      engineName
      engineConfiguration
      endYear
      note
      only
      restriction
      startYear
      __typename
    }
  }
}"""
                },
                "sabo": {
                    "nome": "Sabo",
                    "url": "https://bff.catalogofraga.com.br/gateway/graphql",
                    "ativo": True,
                    "tipo": "graphql",
                    "headers": {
                        "origin": "https://catalogo.sabo.com.br",
                        "referer": "https://catalogo.sabo.com.br/"
                    },
                    "query": """query GetProductById($id: String!, $market: MarketType!) {
  product(id: $id, market: $market) {
    vehicles {
      engineConfiguration
      transmissionManufacturer
      brand
      model
      engineName
      name
      transmissionType
      endYear
      note
      only
      restriction
      startYear
      __typename
    }
  }
}"""
                },
                "nakata": {
                    "nome": "Catálogo Nakata",
                    "url": "https://www.nakata.com.br/catalogo/aplicacao/{id}",
                    "ativo": True,
                    "tipo": "rest",
                    "headers": {
                        "origin": "https://www.nakata.com.br",
                        "referer": "https://www.nakata.com.br/"
                    },
                    "query": ""
                }
            }
        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        # Menu de ajuda
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="📚 Guia de Cadastro", command=self.abrir_guia_cadastro)
        menu_ajuda.add_command(label="🔧 Como Descobrir Informações", command=self.mostrar_dicas_descoberta)
        menu_ajuda.add_separator()
        menu_ajuda.add_command(label="💡 Exemplos Rápidos", command=self.mostrar_exemplos_rapidos)
        menu_ajuda.add_command(label="⚠️ Solução de Problemas", command=self.mostrar_solucao_problemas)

        # Frame de entrada
        input_frame = ttk.LabelFrame(self, text="Adicionar/Editar Provedor", padding=(10, 10))
        input_frame.pack(padx=10, pady=10, fill="x")

        # Nome do provedor
        ttk.Label(input_frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=2)
        self.nome_entry = ttk.Entry(input_frame, width=30)
        self.nome_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # URL
        ttk.Label(input_frame, text="URL:").grid(row=1, column=0, sticky="w", pady=2)
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # Tipo de API
        ttk.Label(input_frame, text="Tipo:").grid(row=2, column=0, sticky="w", pady=2)
        self.tipo_var = tk.StringVar(value="graphql")
        tipo_combo = ttk.Combobox(input_frame, textvariable=self.tipo_var, values=["graphql", "rest", "soap", "local"], state="readonly")
        tipo_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=2)
        tipo_combo.bind("<<ComboboxSelected>>", self.on_tipo_change)

        # Ativo
        self.ativo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Ativo", variable=self.ativo_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        # Frame para campos específicos do tipo
        self.campos_frame = ttk.LabelFrame(input_frame, text="Configurações Específicas", padding=(5, 5))
        self.campos_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        # Campos para provedores web (graphql/rest/soap)
        self.web_frame = ttk.Frame(self.campos_frame)
        
        ttk.Label(self.web_frame, text="Origin:").grid(row=0, column=0, sticky="w", pady=2)
        self.origin_entry = ttk.Entry(self.web_frame, width=50)
        self.origin_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        ttk.Label(self.web_frame, text="Referer:").grid(row=1, column=0, sticky="w", pady=2)
        self.referer_entry = ttk.Entry(self.web_frame, width=50)
        self.referer_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # Campos para provedores locais
        self.local_frame = ttk.Frame(self.campos_frame)
        
        ttk.Label(self.local_frame, text="Executável:").grid(row=0, column=0, sticky="w", pady=2)
        self.executavel_entry = ttk.Entry(self.local_frame, width=50)
        self.executavel_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        
        btn_browse = ttk.Button(self.local_frame, text="📁 Procurar", command=self.browse_executavel)
        btn_browse.grid(row=0, column=2, padx=5, pady=2)

        ttk.Label(self.local_frame, text="Comando:").grid(row=1, column=0, sticky="w", pady=2)
        self.comando_entry = ttk.Entry(self.local_frame, width=50)
        self.comando_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        self.comando_entry.insert(0, "buscar {id}")

        # Inicializa com campos web
        self.web_frame.pack(fill="x", expand=True)

        # Botões
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        
        btn_add = ttk.Button(btn_frame, text="➕ Adicionar", command=self.add_provedor)
        btn_add.pack(side="left", padx=5)
        
        btn_update = ttk.Button(btn_frame, text="✏️ Atualizar Selecionado", command=self.update_provedor)
        btn_update.pack(side="left", padx=5)
        
        btn_clear = ttk.Button(btn_frame, text="🧹 Limpar Campos", command=self.clear_entries)
        btn_clear.pack(side="left", padx=5)
        
        btn_test = ttk.Button(btn_frame, text="🧪 Testar Provedor", command=self.test_provedor)
        btn_test.pack(side="left", padx=5)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("Nome", "URL", "Tipo", "Ativo"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Ativo", text="Ativo")
        self.tree.column("Nome", width=150)
        self.tree.column("URL", width=250)
        self.tree.column("Tipo", width=80)
        self.tree.column("Ativo", width=60)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.load_selected_provedor)

        # Botões de ação
        action_frame = ttk.Frame(self)
        action_frame.pack(pady=5, fill="x")

        btn_delete = ttk.Button(action_frame, text="🗑️ Excluir Selecionado", command=self.delete_provedor)
        btn_delete.pack(side="left", padx=5)

        btn_save_close = ttk.Button(action_frame, text="💾 Salvar e Fechar", command=self.save_and_close)
        btn_save_close.pack(side="right", padx=5)

    def abrir_guia_cadastro(self):
        """Abre o arquivo de documentação"""
        try:
            import subprocess
            import platform
            
            arquivo_ajuda = "ajuda_provedores.md"
            if os.path.exists(arquivo_ajuda):
                if platform.system() == "Windows":
                    os.startfile(arquivo_ajuda)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", arquivo_ajuda])
                else:  # Linux
                    subprocess.run(["xdg-open", arquivo_ajuda])
            else:
                messagebox.showwarning("Arquivo não encontrado", f"O arquivo '{arquivo_ajuda}' não foi encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo de ajuda: {e}")

    def mostrar_dicas_descoberta(self):
        """Mostra dicas de como descobrir informações dos provedores"""
        dicas = """
🔧 COMO DESCOBRIR INFORMAÇÕES DOS PROVEDORES

📱 Para Sites Web:
1. Abra o site do catálogo
2. Pressione F12 (Ferramentas do Desenvolvedor)
3. Vá na aba "Network" (Rede)
4. Faça uma busca no catálogo
5. Observe as requisições para descobrir:
   • URL da API
   • Headers (Origin, Referer)
   • Tipo de requisição (GET/POST)

💻 Para Programas Locais:
1. Abra o programa do catálogo
2. Verifique se ele abre no navegador (HTML local)
3. Anote o caminho onde o programa está instalado
4. Teste se consegue acessar via file:///

📋 Exemplos de Caminhos Locais:
• file:///C:/Programas/Catalogo/aplicacao.html?id={id}
• file:///D:/Catálogos/MeuCatalogo/index.html?parte={id}
• file:///C:/Users/SeuUsuario/Documents/Catalogo/aplicacao.php?id={id}
        """
        messagebox.showinfo("🔧 Dicas de Descoberta", dicas)

    def mostrar_exemplos_rapidos(self):
        """Mostra exemplos rápidos de configuração"""
        exemplos = """
💡 EXEMPLOS RÁPIDOS DE CONFIGURAÇÃO

🔗 GraphQL - Authomix:
Nome: Authomix
URL: https://bff.catalogofraga.com.br/gateway/graphql
Tipo: graphql
Origin: https://catalogo.authomix.com.br
Referer: https://catalogo.authomix.com.br/

🔗 GraphQL - Sabo:
Nome: Sabo
URL: https://bff.catalogofraga.com.br/gateway/graphql
Tipo: graphql
Origin: https://catalogo.sabo.com.br
Referer: https://catalogo.sabo.com.br/

🌐 REST - Nakata:
Nome: Catálogo Nakata
URL: https://www.nakata.com.br/catalogo/aplicacao/{id}
Tipo: rest
Origin: https://www.nakata.com.br
Referer: https://www.nakata.com.br/

💻 Local - Meu Catálogo:
Nome: Meu Catálogo Local
URL: file:///C:/Programas/Catalogo/aplicacao.html?id={id}
Tipo: rest
Origin: file:///C:/Programas/Catalogo/
Referer: file:///C:/Programas/Catalogo/
        """
        messagebox.showinfo("💡 Exemplos Rápidos", exemplos)

    def mostrar_solucao_problemas(self):
        """Mostra soluções para problemas comuns"""
        solucoes = """
⚠️ SOLUÇÃO DE PROBLEMAS

❌ Provedor não funciona:
✅ Verifique se a URL está correta
✅ Confirme se o Origin e Referer estão certos
✅ Teste se o site/programa está acessível
✅ Verifique se o tipo (graphql/rest) está correto

🌐 Erro de conexão:
✅ Verifique sua conexão com a internet
✅ Confirme se o site não está bloqueado
✅ Teste se o programa local está funcionando

🔍 Nenhum resultado encontrado:
✅ Use um ID válido de peça
✅ Verifique se o provedor está ativo
✅ Confirme se a estrutura de dados está correta

💻 Para programas locais:
✅ Certifique-se que o caminho está correto
✅ Teste se o arquivo existe no local especificado
✅ Verifique se o programa está funcionando
        """
        messagebox.showinfo("⚠️ Solução de Problemas", solucoes)

    def test_provedor(self):
        """Testa o provedor atual"""
        nome = self.nome_entry.get().strip()
        url = self.url_entry.get().strip()
        tipo = self.tipo_var.get()
        origin = self.origin_entry.get().strip()
        referer = self.referer_entry.get().strip()

        if not nome or not url:
            messagebox.showwarning("Campos Vazios", "Preencha pelo menos Nome e URL para testar.")
            return

        # Cria configuração temporária para teste
        test_config = {
            "nome": nome,
            "url": url,
            "tipo": tipo,
            "ativo": True,
            "headers": {
                "origin": origin,
                "referer": referer
            },
            "query": ""
        }

        # ID de teste
        test_id = "teste-123"
        
        try:
            from app_catalogo import buscar_provedor_generico
            vehicles = buscar_provedor_generico(test_id, test_config)
            
            if vehicles:
                messagebox.showinfo("✅ Teste Bem-sucedido", 
                    f"Provedor '{nome}' funcionando!\n"
                    f"Encontrados: {len(vehicles)} veículos\n"
                    f"Primeiro resultado: {vehicles[0].get('brand', '')} {vehicles[0].get('name', '')}")
            else:
                messagebox.showwarning("⚠️ Teste sem Resultados", 
                    f"Provedor '{nome}' conectou, mas não retornou dados.\n"
                    f"Isso pode ser normal se o ID de teste não existir.")
                
        except Exception as e:
            messagebox.showerror("❌ Erro no Teste", f"Erro ao testar provedor '{nome}':\n{str(e)}")

    def populate_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for key, provedor in self.provedores.items():
            self.tree.insert("", "end", values=(
                provedor.get('nome', ''),
                provedor.get('url', ''),
                provedor.get('tipo', ''),
                'Sim' if provedor.get('ativo', False) else 'Não'
            ), tags=(key,))

    def add_provedor(self):
        nome = self.nome_entry.get().strip()
        url = self.url_entry.get().strip()
        tipo = self.tipo_var.get()
        ativo = self.ativo_var.get()
        origin = self.origin_entry.get().strip()
        referer = self.referer_entry.get().strip()

        if not nome or not url:
            messagebox.showwarning("Entrada Inválida", "Nome e URL não podem ser vazios.")
            return

        # Gera chave única baseada no nome
        key = nome.lower().replace(' ', '_')
        if key in self.provedores:
            if not messagebox.askyesno("Provedor Existente", f"'{nome}' já existe. Deseja atualizar?"):
                return

        # Query padrão baseada no tipo
        default_query = """query GetProductById($id: String!, $market: MarketType!) {
  product(id: $id, market: $market) {
    vehicles {
      brand
      name
      model
      engineName
      engineConfiguration
      endYear
      note
      only
      restriction
      startYear
      __typename
    }
  }
}"""

        self.provedores[key] = {
            "nome": nome,
            "url": url,
            "tipo": tipo,
            "ativo": ativo,
            "headers": {
                "origin": origin,
                "referer": referer
            },
            "query": default_query
        }
        self.populate_tree()
        self.clear_entries()
        messagebox.showinfo("Sucesso", "Provedor adicionado/atualizado.")

    def update_provedor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nenhuma Seleção", "Selecione um provedor para atualizar.")
            return

        item = selected[0]
        old_key = self.tree.item(item, 'tags')[0]
        
        nome = self.nome_entry.get().strip()
        url = self.url_entry.get().strip()
        tipo = self.tipo_var.get()
        ativo = self.ativo_var.get()
        origin = self.origin_entry.get().strip()
        referer = self.referer_entry.get().strip()

        if not nome or not url:
            messagebox.showwarning("Entrada Inválida", "Nome e URL não podem ser vazios.")
            return

        new_key = nome.lower().replace(' ', '_')
        if old_key != new_key and new_key in self.provedores:
            messagebox.showwarning("Erro", "Já existe um provedor com este nome.")
            return

        # Mantém a query existente ou usa padrão
        existing_query = self.provedores.get(old_key, {}).get('query', '')
        default_query = """query GetProductById($id: String!, $market: MarketType!) {
  product(id: $id, market: $market) {
    vehicles {
      brand
      name
      model
      engineName
      engineConfiguration
      endYear
      note
      only
      restriction
      startYear
      __typename
    }
  }
}"""

        # Remove o antigo e adiciona o novo
        if old_key in self.provedores:
            del self.provedores[old_key]

        self.provedores[new_key] = {
            "nome": nome,
            "url": url,
            "tipo": tipo,
            "ativo": ativo,
            "headers": {
                "origin": origin,
                "referer": referer
            },
            "query": existing_query if existing_query else default_query
        }
        self.populate_tree()
        self.clear_entries()
        messagebox.showinfo("Sucesso", "Provedor atualizado.")

    def delete_provedor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nenhuma Seleção", "Selecione um provedor para excluir.")
            return

        item = selected[0]
        key = self.tree.item(item, 'tags')[0]
        nome = self.tree.item(item, 'values')[0]

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o provedor '{nome}'?"):
            if key in self.provedores:
                del self.provedores[key]
                self.populate_tree()
                self.clear_entries()
                messagebox.showinfo("Sucesso", "Provedor excluído.")

    def load_selected_provedor(self, event):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            key = self.tree.item(item, 'tags')[0]
            provedor = self.provedores.get(key, {})
            
            self.nome_entry.delete(0, tk.END)
            self.nome_entry.insert(0, provedor.get('nome', ''))
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, provedor.get('url', ''))
            self.tipo_var.set(provedor.get('tipo', 'graphql'))
            self.ativo_var.set(provedor.get('ativo', True))
            
            headers = provedor.get('headers', {})
            self.origin_entry.delete(0, tk.END)
            self.origin_entry.insert(0, headers.get('origin', ''))
            self.referer_entry.delete(0, tk.END)
            self.referer_entry.insert(0, headers.get('referer', ''))

    def clear_entries(self):
        self.nome_entry.delete(0, tk.END)
        self.url_entry.delete(0, tk.END)
        self.origin_entry.delete(0, tk.END)
        self.referer_entry.delete(0, tk.END)
        self.tipo_var.set("graphql")
        self.ativo_var.set(True)

    def save_and_close(self):
        save_provedores(self.provedores)
        self.on_save_callback()
        self.destroy()

    def on_tipo_change(self, event):
        """Muda os campos baseado no tipo selecionado"""
        tipo = self.tipo_var.get()
        
        # Remove todos os frames
        for widget in self.campos_frame.winfo_children():
            widget.pack_forget()
        
        if tipo == "local":
            # Mostra campos para provedores locais
            self.local_frame.pack(fill="x", expand=True)
            # Muda label da URL para Executável
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, "Caminho do executável...")
        else:
            # Mostra campos para provedores web
            self.web_frame.pack(fill="x", expand=True)
            # Restaura label da URL
            if not self.url_entry.get() or "executável" in self.url_entry.get():
                self.url_entry.delete(0, tk.END)

    def browse_executavel(self):
        """Abre diálogo para selecionar executável"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Selecionar Executável",
            filetypes=[
                ("Executáveis", "*.exe"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if filename:
            self.executavel_entry.delete(0, tk.END)
            self.executavel_entry.insert(0, filename)
            # Também atualiza o campo URL
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, filename)

# --- CLASSE DA APLICAÇÃO PRINCIPAL ---
class Application(ttk.Frame):
    def __init__(self, master=None, themed_root=None):
        super().__init__(master)
        self.root = self.winfo_toplevel()
        self.themed_root = themed_root
        self.root.title("Gerenciador de Aplicações de Peças")
        window_width = 800
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.pack(fill="both", expand=True)
        self.siglas_map = load_siglas()
        self.create_widgets()

    def create_widgets(self):
        # MenuBar para ações menos frequentes
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menu_acao = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ações", menu=menu_acao)
        menu_acao.add_command(label="Copiar Tabela em Texto", command=self.copy_table_as_text)
        menu_acao.add_command(label="Exportar para CSV", command=self.export_to_csv)
        menu_acao.add_separator()
        menu_acao.add_command(label="Gerenciar Siglas", command=self.open_sigla_manager)
        menu_acao.add_command(label="Gerenciar Palavras para Remover", command=self.open_palavras_remover_manager)
        menu_acao.add_command(label="Gerenciar Provedores", command=self.open_provedor_manager)
        menu_acao.add_separator()
        menu_acao.add_command(label="🔍 Testar Provedores Locais", command=self.test_provedores_locais)
        menu_acao.add_command(label="📚 Abrir Guia de Ajuda", command=self.abrir_guia_ajuda)

        frame_id = ttk.LabelFrame(self, text="ID da Peça", padding=(10, 10))
        frame_id.pack(padx=10, pady=5, fill="x")
        ttk.Label(frame_id, text="ID:").pack(side="left", padx=5)
        self.id_entry = ttk.Entry(frame_id, width=50)
        self.id_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.id_entry.insert(0, "Ex: 5042ecad-dbcb-92314cc6-2fb6-6b213869-a827")
        self.id_entry.bind("<FocusIn>", lambda e: self._clear_placeholder())
        self.id_entry.bind("<FocusOut>", lambda e: self._add_placeholder())
        self._placeholder_active = True

        # Frame para seleção de provedor
        frame_provedor = ttk.LabelFrame(self, text="Provedor de Dados", padding=(10, 10))
        frame_provedor.pack(padx=10, pady=5, fill="x")
        ttk.Label(frame_provedor, text="Provedor:").pack(side="left", padx=5)
        self.provedor_var = tk.StringVar()
        self.provedor_combo = ttk.Combobox(frame_provedor, textvariable=self.provedor_var, state="readonly")
        self.provedor_combo.pack(side="left", expand=True, fill="x", padx=5)
        self.update_provedor_combo()

        # Criação do checkbox da Schadek ANTES de chamar on_provedor_change
        self.schadek_use_products_var = tk.BooleanVar(value=True)
        self.schadek_checkbox = ttk.Checkbutton(
            frame_provedor, text="Buscar Produto + Aplicações (Schadek)",
            variable=self.schadek_use_products_var
        )
        self.schadek_checkbox.pack(side="left", padx=5)
        self.schadek_checkbox.pack_forget()

        self.provedor_combo.bind("<<ComboboxSelected>>", self.on_provedor_change)
        self.on_provedor_change()

        # NOVO: Listbox para seleção de PDFs (só aparece para PDF Local)
        self.frame_pdf_list = ttk.LabelFrame(frame_provedor, text="PDFs disponíveis para busca", padding=(8, 8))
        self.label_pdf_list = ttk.Label(self.frame_pdf_list, text="Selecione os PDFs para buscar:")
        self.label_pdf_list.pack(anchor="w", padx=5, pady=(0, 4))
        listbox_frame = ttk.Frame(self.frame_pdf_list)
        listbox_frame.pack(fill="x")
        self.listbox_pdfs = tk.Listbox(listbox_frame, selectmode="multiple", height=8, width=60, borderwidth=2, relief="groove")
        self.listbox_pdfs.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.listbox_pdfs.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox_pdfs.config(yscrollcommand=scrollbar.set)
        self.frame_pdf_list.pack(padx=10, pady=5, fill="x")
        self.frame_pdf_list.pack_forget()  # Esconde por padrão

        # Botões principais para ações rápidas
        frame_quick = ttk.Frame(self)
        frame_quick.pack(pady=5)
        btn_search = ttk.Button(frame_quick, text="🔍 Buscar Aplicações", command=self.perform_search)
        btn_search.pack(side="left", padx=5)
        btn_clear = ttk.Button(frame_quick, text="🧹 Limpar Tudo", command=self.clear_all)
        btn_clear.pack(side="left", padx=5)
        btn_copy = ttk.Button(frame_quick, text="📋 Copiar Texto Formatado", command=self.copy_to_clipboard)
        btn_copy.pack(side="left", padx=5)

        frame_fields = ttk.LabelFrame(self, text="Campos da Aplicação", padding=(10, 10))
        frame_fields.pack(padx=10, pady=5, fill="x")
        self.field_vars = {}
        self.available_fields = {
            'marca': 'Marca',
            'modelo': 'Modelo',
            'motor': 'Motor',
            'configuracao_motor': 'Configuração Motor',
            'ano': 'Ano',
            'observacao': 'Observação',
            'sistema_freio': 'Sistema de Freio',
            'restricao': 'Restrição',
            'apenas': 'Apenas',
            'posicao': 'Posição',
            'lado': 'Lado',
            'direcao': 'Direção'
        }
        default_checked_fields = ['marca', 'modelo', 'motor', 'ano']
        
        # Checkbox "Selecionar Tudo"
        self.select_all_var = tk.BooleanVar()
        select_all_chk = ttk.Checkbutton(frame_fields, text="☑️ Selecionar Tudo", variable=self.select_all_var, command=self.toggle_select_all)
        select_all_chk.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        
        # Separador
        separator = ttk.Separator(frame_fields, orient='horizontal')
        separator.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        col = 0
        row = 2
        for key, text in self.available_fields.items():
            var = tk.BooleanVar(value=(key in default_checked_fields))
            self.field_vars[key] = var
            chk = ttk.Checkbutton(frame_fields, text=text, variable=var, command=self.update_select_all_state)
            chk.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1
        frame_results = ttk.LabelFrame(self, text="Resultados da Aplicação", padding=(10, 10))
        frame_results.pack(padx=10, pady=5, fill="both", expand=True)
        self.tree_results = ttk.Treeview(frame_results, show="headings")
        self.tree_results.pack(fill="both", expand=True)
        self.formatted_text_for_clipboard = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=1, height=1)

        # Label para mostrar o tema atual
        theme_name = self.themed_root.get_theme() if self.themed_root and hasattr(self.themed_root, 'get_theme') else 'desconhecido'
        self.theme_label = ttk.Label(self, text=f"Tema: {theme_name}")
        self.theme_label.pack(side="bottom", anchor="e", padx=10, pady=2)

    def _clear_placeholder(self):
        if self._placeholder_active:
            self.id_entry.delete(0, tk.END)
            self._placeholder_active = False

    def _add_placeholder(self):
        if not self.id_entry.get():
            self.id_entry.insert(0, "Ex: 5042ecad-dbcb-92314cc6-2fb6-6b213869-a827")
            self._placeholder_active = True

    def on_provedor_change(self, event=None):
        provedor_nome = self.provedor_var.get()
        provedores = load_provedores()
        provedor = None
        for key, p in provedores.items():
            if p['nome'] == provedor_nome:
                provedor = p
                break
        if provedor_nome.lower() == "schadek":
            self.schadek_checkbox.pack(side="left", padx=5)
        else:
            self.schadek_checkbox.pack_forget()
        if provedor and provedor.get('tipo') == 'pdf_local':
            pasta = provedor.get('pasta', 'catalogos_pdf')
            self.listbox_pdfs.delete(0, tk.END)
            if not os.path.exists(pasta):
                if hasattr(self, 'frame_pdf_list') and self.frame_pdf_list is not None:
                    self.frame_pdf_list.pack_forget()   
                messagebox.showwarning("Pasta não encontrada", f"A pasta '{pasta}' não existe. Crie a pasta e coloque os PDFs nela.")
                return
            pdfs = [f for f in os.listdir(pasta) if f.lower().endswith('.pdf')]
            if not pdfs:
                if hasattr(self, 'frame_pdf_list') and self.frame_pdf_list is not None:
                    self.frame_pdf_list.pack_forget()   
                messagebox.showinfo("Nenhum PDF encontrado", f"Nenhum arquivo PDF foi encontrado na pasta '{pasta}'.")
                return
            for pdf in pdfs:
                self.listbox_pdfs.insert(tk.END, pdf)
            self.frame_pdf_list.pack(padx=10, pady=8, fill="x")
            self.frame_pdf_list.lift()
        else:
            if hasattr(self, 'frame_pdf_list') and self.frame_pdf_list is not None:
                    self.frame_pdf_list.pack_forget()   

    def perform_search(self):
        id_peca = self.id_entry.get().strip()
        if not id_peca:
            messagebox.showwarning("Entrada Inválida", "Por favor, digite o ID da peça.")
            return
        provedor_nome = self.provedor_var.get()
        if not provedor_nome:
            messagebox.showwarning("Provedor Inválido", "Por favor, selecione um provedor de dados.")
            return
        provedores = load_provedores()
        provedor = None
        for key, p in provedores.items():
            if p['nome'] == provedor_nome:
                provedor = p
                break
        if not provedor:
            messagebox.showerror("Erro", "Provedor não encontrado.")
            return
        # NOVO: Se for PDF Local, buscar só nos PDFs selecionados
        if provedor.get('tipo') == 'pdf_local':
            pasta = provedor.get('pasta', 'catalogos_pdf')
            selecionados = self.listbox_pdfs.curselection()
            if not selecionados:
                messagebox.showwarning("Seleção de PDF", "Selecione pelo menos um PDF para buscar.")
                return
            pdfs_escolhidos = [self.listbox_pdfs.get(i) for i in selecionados]
            pdf_provider = PDFProvider()
            resultados_pdf = pdf_provider.buscar_em_pdfs_especificos(id_peca, pdfs_escolhidos, pasta)
            vehicles = []
            for r in resultados_pdf:
                vehicles.append({
                    'brand': '',
                    'name': '',
                    'model': '',
                    'engineName': '',
                    'engineConfiguration': '',
                    'startYear': '',
                    'endYear': '',
                    'note': f"Arquivo: {r['arquivo']} | Página: {r['pagina']} | Trecho: {r['linha']}",
                    'only': '',
                    'restriction': '',
                    'position': '',
                    'side': '',
                    'steering': ''
                })
            raw_vehicles = vehicles
        elif provedor.get('tipo') == 'viemar':
            raw_vehicles = buscar_viemar_playwright(id_peca)
            #raw_vehicles = parse_viemar_json(id_peca)
        elif provedor.get('tipo') == 'schadek':
            import requests
            if hasattr(self, 'schadek_use_products_var') and self.schadek_use_products_var.get():
                url = provedor.get('url_products', '').replace('{codigo}', id_peca)
            else:
                url = provedor.get('url_applications', '').replace('{codigo}', id_peca)
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                raw_vehicles = parse_schadek_json(data)
            except Exception as e:
                messagebox.showerror("Erro Schadek", f"Erro ao buscar na Schadek: {e}")
                return
        else:
            raw_vehicles = buscar_provedor_generico(id_peca, provedor)
            if not raw_vehicles:
                messagebox.showinfo("Sem Aplicações", "Nenhuma aplicação encontrada ou erro na busca.")
                return

        # Limpa a Treeview antes de uma nova busca
        for item in self.tree_results.get_children():
            self.tree_results.delete(item)
        self.tree_results.config(columns=[])
        self.formatted_text_for_clipboard.delete(1.0, tk.END)
        self.update_idletasks()

        grouped_applications_by_base = {}
        for vehicle in raw_vehicles:
            brand = vehicle.get('brand', '')
            name = vehicle.get('name', '')
            model = vehicle.get('model', '')
            engine_name = vehicle.get('engineName', '')
            engine_config = vehicle.get('engineConfiguration', '')
            brake_system = vehicle.get('brakeSystem', '')
            start_year = vehicle.get('startYear')
            end_year = vehicle.get('endYear')
            note = vehicle.get('note', '')
            only = vehicle.get('only', '')
            restriction = vehicle.get('restriction', '')

            display_brand = self.siglas_map.get(brand.upper(), brand)
            display_model = name if name else model
            display_motor = engine_name
            display_config_motor = engine_config

            group_key_base = (display_brand, display_model, display_motor, display_config_motor)

            current_observations = []
            if note: current_observations.append(note)
            if only: current_observations.append(only)
            if restriction: current_observations.append(restriction)
            
            if group_key_base not in grouped_applications_by_base:
                grouped_applications_by_base[group_key_base] = {
                    'year_ranges': [],
                    'observations': set(),
                    'original_data_sample': vehicle
                }
            grouped_applications_by_base[group_key_base]['year_ranges'].append((start_year, end_year))
            for obs in current_observations:
                grouped_applications_by_base[group_key_base]['observations'].add(obs)

        applications_for_table = []
        applications_for_clipboard = []
        for key_base, data in grouped_applications_by_base.items():
            display_brand, display_model, display_motor, display_config_motor = key_base
            min_start_year, max_end_year = merge_year_ranges_overall(data['year_ranges'])
            ano_str = ""
            if min_start_year is not None and max_end_year is not None:
                if min_start_year == max_end_year:
                    ano_str = str(min_start_year)
                else:
                    ano_str = f"{min_start_year}...{max_end_year}"
            elif min_start_year is not None:
                ano_str = f"{min_start_year}..."
            elif max_end_year is not None:
                ano_str = f"...{max_end_year}"
            combined_observations = "; ".join(sorted(list(data['observations'])))
            original_sample = data['original_data_sample']
            full_field_values = {
                'marca': display_brand,
                'modelo': display_model,
                'motor': display_motor,
                'configuracao_motor': display_config_motor,
                'ano': ano_str,
                'observacao': combined_observations,
                'sistema_freio': original_sample.get('brakeSystem', ''),
                'restricao': original_sample.get('restriction', ''),
                'apenas': original_sample.get('only', ''),
                'posicao': original_sample.get('position', ''),
                'lado': original_sample.get('side', ''),
                'direcao': original_sample.get('steering', '')
            }
            applications_for_table.append(full_field_values)
            output_parts_clipboard = []
            for field_key in self.field_vars.keys():
                if self.field_vars[field_key].get():  # Só inclui se o campo estiver selecionado
                    value = full_field_values.get(field_key)
                    if value:
                        output_parts_clipboard.append(str(value))
            aplicacao_formatada_clipboard = " ".join(output_parts_clipboard).strip().upper()
            if aplicacao_formatada_clipboard:
                applications_for_clipboard.append(aplicacao_formatada_clipboard)
        applications_for_clipboard_sorted = sorted(applications_for_clipboard)
        applications_for_table_sorted = sorted(applications_for_table, 
                                               key=lambda x: tuple(x.get(k, '') for k in self.field_vars.keys()))
        
        # Filtra apenas os campos selecionados para a tabela
        field_vars = self.field_vars if self.field_vars is not None else {}
        available_fields = self.available_fields if self.available_fields is not None else {}
        selected_fields = [key for key in field_vars.keys() if field_vars[key].get()]
        display_names = [available_fields[key] for key in selected_fields]
        
        self.tree_results.config(columns=selected_fields)
        for col_key, display_name in zip(selected_fields, display_names):
            self.tree_results.heading(col_key, text=display_name)
            self.tree_results.column(col_key, width=120, anchor='w')
        for col_key in selected_fields:
            max_width = 0
            header_width = len(available_fields[col_key]) * 8
            max_width = max(max_width, header_width)
            for app_data in applications_for_table_sorted:
                content_width = len(str(app_data.get(col_key, ''))) * 8
                max_width = max(max_width, content_width)
            self.tree_results.column(col_key, width=max_width + 10)
        for app_data in applications_for_table_sorted:
            values_for_row = [app_data.get(key, '') for key in selected_fields]
            self.tree_results.insert("", "end", values=values_for_row)
        if applications_for_clipboard_sorted:
            formatted_output_clipboard = ""
            for app_str in applications_for_clipboard_sorted:
                formatted_output_clipboard += app_str + "\r\n"
            self.formatted_text_for_clipboard.insert(tk.END, formatted_output_clipboard)
            pyperclip.copy(formatted_output_clipboard)
            messagebox.showinfo("Sucesso", "Aplicações encontradas e copiadas para a área de transferência!")
        else:
            messagebox.showinfo("Sem Aplicações", "Nenhuma aplicação encontrada após agrupamento e filtragem.")

    def copy_to_clipboard(self):
        palavras_remover = load_palavras_remover()
        columns = self.tree_results.cget('columns')
        if not columns:
            messagebox.showwarning("Sem Dados", "Não há dados para copiar.")
            return
        data = []
        for item in self.tree_results.get_children():
            values = [str(v) for v in self.tree_results.item(item, 'values')]
            for i, col in enumerate(columns):
                values[i] = remover_palavras_avancado(values[i], {col: palavras_remover.get(col, [])})
            data.append(values)
        data_unicas = []
        vistos = set()
        for row in data:
            row_tuple = tuple(row)
            if row_tuple not in vistos:
                data_unicas.append(row)
                vistos.add(row_tuple)
        formatted_output = ""
        for row in data_unicas:
            formatted_output += " ".join(row).upper() + "\r\n"
        self.formatted_text_for_clipboard.delete(1.0, tk.END)
        self.formatted_text_for_clipboard.insert(tk.END, formatted_output)
        text_to_copy = formatted_output.strip()
        if text_to_copy:
            try:
                pyperclip.copy(text_to_copy)
                messagebox.showinfo("Copiado", "Texto copiado para a área de transferência!")
            except pyperclip.PyperclipException:
                messagebox.showerror("Erro ao Copiar", "Não foi possível copiar para a área de transferência. Verifique a instalação do pyperclip.")
        else:
            messagebox.showwarning("Nada para Copiar", "Não há texto nos resultados para copiar.")

    def clear_all(self):
        self.id_entry.delete(0, tk.END)
        # Limpa a Treeview
        for item in self.tree_results.get_children():
            self.tree_results.delete(item)
        self.tree_results.config(columns=[]) # Limpa as colunas
        self.formatted_text_for_clipboard.delete(1.0, tk.END) # Limpa o texto interno
        
        default_checked_fields = ['marca', 'modelo', 'motor', 'ano']
        for key, var in self.field_vars.items():
            if key in default_checked_fields:
                var.set(True)
            else:
                var.set(False)
        
        # Atualiza o estado do checkbox "Selecionar Tudo"
        self.update_select_all_state()

    def open_sigla_manager(self):
        SiglaManager(self, self.reload_siglas_map)

    def reload_siglas_map(self):
        self.siglas_map = load_siglas()
        messagebox.showinfo("Siglas Atualizadas", "O mapa de siglas foi recarregado.")

    def export_to_csv(self):
        columns = self.tree_results.cget('columns')
        if not columns:
            messagebox.showwarning("Sem Dados", "Não há dados para exportar.")
            return
        data = []
        for item in self.tree_results.get_children():
            values = self.tree_results.item(item, 'values')
            data.append(values)
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Salvar como CSV")
        if not file_path:
            return
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Corrigido capitalize para evitar erro de None
                writer.writerow([(self.available_fields.get(col) or col).capitalize() for col in columns])
                for row in data:
                    writer.writerow(row)
            messagebox.showinfo("Exportação Concluída", f"Dados exportados com sucesso para {file_path}")
        except Exception as e:
            messagebox.showerror("Erro ao Exportar", f"Erro ao exportar para CSV: {e}")

    # NOVO: Função para copiar tabela em texto
    def copy_table_as_text(self):
        palavras_remover = load_palavras_remover()
        columns = self.tree_results.cget('columns')
        if not columns:
            messagebox.showwarning("Sem Dados", "Não há dados para copiar.")
            return
        headers = [(self.available_fields.get(col) or col).upper() for col in columns]
        data = []
        for item in self.tree_results.get_children():
            values = [str(v) for v in self.tree_results.item(item, 'values')]
            for i, col in enumerate(columns):
                values[i] = remover_palavras_avancado(values[i], {col: palavras_remover.get(col, [])})
            data.append(values)
        data_unicas = []
        vistos = set()
        for row in data:
            row_tuple = tuple(row)
            if row_tuple not in vistos:
                data_unicas.append(row)
                vistos.add(row_tuple)
        col_widths = [len(h) for h in headers]
        for row in data_unicas:
            for i, v in enumerate(row):
                col_widths[i] = max(col_widths[i], len(v))
        def fmt_row(row):
            return '| ' + ' | '.join((v.ljust(col_widths[i]) + '  ') for i, v in enumerate(row)) + '|'
        sep = '+-' + '-+-'.join('-'*w for w in col_widths) + '-+'
        lines = [sep, fmt_row(headers), sep]
        for row in data_unicas:
            lines.append(fmt_row(row))
        lines.append(sep)
        table_text = '\r\n'.join(lines)
        try:
            pyperclip.copy(table_text)
            messagebox.showinfo("Tabela Copiada", "Tabela em texto copiada para a área de transferência!")
        except pyperclip.PyperclipException:
            messagebox.showerror("Erro ao Copiar", "Não foi possível copiar a tabela para a área de transferência.")

    def open_palavras_remover_manager(self):
        # Garante que todos os campos disponíveis estão presentes, inclusive 'configuracao_motor'
        campos = list(self.available_fields.keys())
        PalavrasRemoverManager(self, campos, self.reload_palavras_remover)

    def reload_palavras_remover(self):
        # Pode ser usado para recarregar as palavras a remover se necessário futuramente
        pass

    def update_provedor_combo(self):
        provedores = load_provedores()
        ativos = [p['nome'] for p in provedores.values() if p.get('ativo', False)]
        self.provedor_combo['values'] = ativos
        if ativos:
            self.provedor_var.set(ativos[0])

    def open_provedor_manager(self):
        ProvedorManager(self, self.reload_provedores)

    def reload_provedores(self):
        self.update_provedor_combo()
        messagebox.showinfo("Provedores Atualizados", "A lista de provedores foi recarregada.")

    def test_provedores_locais(self):
        """Abre o testador de provedores locais"""
        messagebox.showinfo("Função não disponível", "O testador de provedores locais foi removido nesta versão focada apenas em provedores web.")

    def abrir_guia_ajuda(self):
        """Abre o arquivo de documentação"""
        try:
            import subprocess
            import platform
            
            arquivo_ajuda = os.path.join("docs", "ajuda_provedores.md")
            if os.path.exists(arquivo_ajuda):
                if platform.system() == "Windows":
                    os.startfile(arquivo_ajuda)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", arquivo_ajuda])
                else:  # Linux
                    subprocess.run(["xdg-open", arquivo_ajuda])
            else:
                messagebox.showwarning("Arquivo não encontrado", 
                    f"O arquivo '{arquivo_ajuda}' não foi encontrado.\n"
                    "Verifique se o arquivo de ajuda existe no diretório.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo de ajuda: {e}")

    def toggle_select_all(self):
        for key, var in self.field_vars.items():
            var.set(self.select_all_var.get())

    def update_select_all_state(self):
        all_selected = all(var.get() for var in self.field_vars.values())
        self.select_all_var.set(all_selected)

def remover_palavras_avancado(texto, palavras_remover):
    todas_palavras = []
    for lista in palavras_remover.values():
        todas_palavras.extend(lista)
    todas_palavras = sorted(set(todas_palavras), key=len, reverse=True)
    for palavra in todas_palavras:
        if not palavra.strip():
            continue
        padrao = r'(?i)(?<!\w){}(?!\w)'.format(re.escape(palavra.strip()))
        texto = re.sub(padrao, ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

if __name__ == "__main__":
    # Inicializa janela com tema padrão do ttkthemes
    app = ThemedTk(theme="arc")
    # Cria a aplicação principal como Frame, passando themed_root=app
    application = Application(master=app, themed_root=app)
    # Adiciona menu de temas em ordem alfabética
    def set_theme(theme_name):
        app.set_theme(theme_name)
        application.theme_label.config(text=f"Tema: {theme_name}")
    menubar = app.nametowidget(app['menu']) if 'menu' in app.keys() else None
    if menubar is None:
        menubar = tk.Menu(app)
        app.config(menu=menubar)
    menu_temas = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Temas", menu=menu_temas)
    for theme in sorted(app.get_themes()):
        menu_temas.add_command(label=theme, command=lambda t=theme: set_theme(t))

    # Backup automático ao fechar
    def backup_ao_fechar():
        try:
            subprocess.run(["python", "backup_config.py"], check=True)
        except Exception as e:
            print(f"[AVISO] Não foi possível executar o backup automático ao fechar: {e}")
        app.destroy()
    app.protocol("WM_DELETE_WINDOW", backup_ao_fechar)
    app.mainloop()
