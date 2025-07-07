import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import requests
import pyperclip
import json
import os

# --- Configuração do arquivo de siglas ---
SIGLAS_FILE = "siglas.json"

# --- Funções para carregar/salvar siglas ---
def load_siglas():
    if os.path.exists(SIGLAS_FILE):
        try:
            with open(SIGLAS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showwarning("Erro de Leitura", f"Arquivo '{SIGLAS_FILE}' está corrompido ou vazio. Criando um novo.")
            return {}
    return {}

def save_siglas(siglas_data):
    with open(SIGLAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(siglas_data, f, indent=4, ensure_ascii=False)

# --- FUNÇÃO PARA CONSOLIDAR INTERVALOS DE ANOS ---
def merge_year_ranges_overall(ranges):
    """
    Consolida uma lista de intervalos de anos (start, end) em um único intervalo abrangente (min_start, max_end).
    Trata anos None como intervalos abertos (0 para início, 9999 para fim).
    """
    if not ranges:
        return None, None

    # Converte None para valores sentinela para ordenação e cálculo
    # e filtra ranges completamente vazios
    processed_ranges = []
    for s, e in ranges:
        start_val = s if s is not None else 0
        end_val = e if e is not None else 9999
        processed_ranges.append((start_val, end_val))

    if not processed_ranges:
        return None, None

    # Ordena os intervalos pelo ano de início
    sorted_ranges = sorted(processed_ranges, key=lambda x: x[0])

    overall_min_start = sorted_ranges[0][0]
    overall_max_end = sorted_ranges[0][1]

    for i in range(1, len(sorted_ranges)):
        next_start, next_end = sorted_ranges[i]

        # Se o próximo intervalo se sobrepõe ou é consecutivo ao intervalo atual
        if next_start <= overall_max_end + 1:
            overall_max_end = max(overall_max_end, next_end)
        else:
            # Se há uma lacuna, ainda queremos o ano final mais alto geral
            overall_max_end = max(overall_max_end, next_end)
            # Se quiséssemos múltiplos intervalos separados por lacunas, a lógica seria diferente aqui.
            # Mas para um único intervalo abrangente, continuamos atualizando o max_end.
    
    # Converte os valores sentinela de volta para None se necessário para a exibição
    final_min_start = overall_min_start if overall_min_start != 0 else None
    final_max_end = overall_max_end if overall_max_end != 9999 else None

    return final_min_start, final_max_end


# --- FUNÇÃO DE BUSCA GRAPHQL (RETORNA DADOS BRUTOS) ---
def buscar_dados_veiculos_authomix_graphql(id_peca):
    graphql_url = "https://bff.catalogofraga.com.br/gateway/graphql"
    graphql_query = """
query GetProductById($id: String!, $market: MarketType! ) {
  product(id: $id, market: $market) {
    id
    partNumber
    brand {
      name
      imageUrl
      __typename
    }
    applicationDescription
    images {
      imageUrl
      thumbnailUrl
      category
      __typename
    }
    specifications {
      id
      category
      description
      value
      important
      __typename
    }
    crossReferences {
      brand {
        id
        name
        __typename
      }
      partNumber
      __typename
    }
    videos
    vehicles {
      brand
      name
      model
      engineName
      engineConfiguration
      brakeSystem
      endYear
      note
      only
      restriction
      startYear
      brand
      __typename
    }
    components {
      partNumber
      productGroup
      applicationDescription
      activeCatalog
      status
      __typename
    }
    distributors {
      code
      distributor {
        name
        __typename
      }
      __typename
    }
    status
    containsUniversalApplication
    billOfMaterial {
      imageUrl
      products {
        productId
        partNumber
        amount
        description
        note
        coordinates {
          coordinateX
          coordinateY
          __typename
        }
        __typename
      }
      __typename
    }
    links {
      category
      description
      title
      url
      distributor {
        id
        name
        __typename
      }
      __typename
    }
    productGroup {
      name
      __typename
    }
    market {
      name
      __typename
    }
    __typename
  }
}
    """
    graphql_variables = {
        "id": id_peca,
        "market": "BRA"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://catalogo.authomix.com.br",
        "Referer": "https://catalogo.authomix.com.br/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A )Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site"
    }
    payload = json.dumps({
        "query": graphql_query,
        "variables": graphql_variables
    })

    try:
        response = requests.post(graphql_url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            messagebox.showerror("Erro GraphQL", f"Erro na resposta GraphQL: {data['errors']}")
            return []

        product_data = data.get('data', {}).get('product', {})
        vehicles = product_data.get('vehicles', [])
        
        return vehicles # Retorna a lista de dicionários de veículos brutos

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro de Conexão", f"Erro ao acessar a API GraphQL do Authomix: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Erro de Dados", "Erro ao decodificar a resposta JSON da API.")
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro inesperado: {e}")

    return []

# --- CLASSE PARA GERENCIAR SIGLAS ---
class SiglaManager(tk.Toplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.parent = parent
        self.on_save_callback = on_save_callback
        self.title("Gerenciar Siglas de Marcas")
        self.geometry("500x500")
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

# --- CLASSE DA APLICAÇÃO PRINCIPAL ---
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Aplicações de Peças")
        
        window_width = 800 # Aumentado a largura para a tabela
        window_height = 650

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.siglas_map = load_siglas()
        self.create_widgets()

    def create_widgets(self):
        frame_id = tk.LabelFrame(self, text="ID da Peça (Authomix)", padx=10, pady=10)
        frame_id.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_id, text="ID:").pack(side="left", padx=5)
        self.id_entry = tk.Entry(frame_id, width=50)
        self.id_entry.pack(side="left", expand=True, fill="x", padx=5)
        self.id_entry.insert(0, "5042ecad-dbcb-92314cc6-2fb6-6b213869-a827") # Exemplo de ID FIAT

        frame_fields = tk.LabelFrame(self, text="Campos da Aplicação", padx=10, pady=10)
        frame_fields.pack(padx=10, pady=5, fill="x")

        self.field_vars = {}
        self.available_fields = {
            'marca': 'Marca',
            'modelo': 'Modelo',
            'motor': 'Motor',
            'ano': 'Ano',
            'observacao': 'Observação',
            'sistema_freio': 'Sistema de Freio',
            'restricao': 'Restrição',
            'apenas': 'Apenas'
        }
        
        default_checked_fields = ['marca', 'modelo', 'motor', 'ano'] 

        col = 0
        row = 0
        for key, text in self.available_fields.items():
            var = tk.BooleanVar(value=(key in default_checked_fields)) 
            self.field_vars[key] = var
            chk = tk.Checkbutton(frame_fields, text=text, variable=var)
            chk.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            col += 1
            if col > 2:
                col = 0
                row += 1

        frame_buttons = tk.Frame(self)
        frame_buttons.pack(pady=10)

        btn_search = tk.Button(frame_buttons, text="Buscar Aplicações", command=self.perform_search)
        btn_search.pack(side="left", padx=5)

        btn_clear = tk.Button(frame_buttons, text="Limpar Tudo", command=self.clear_all)
        btn_clear.pack(side="left", padx=5)

        btn_copy = tk.Button(frame_buttons, text="Copiar Texto Formatado", command=self.copy_to_clipboard) # Texto do botão alterado
        btn_copy.pack(side="left", padx=5)

        btn_manage_siglas = tk.Button(frame_buttons, text="Gerenciar Siglas", command=self.open_sigla_manager)
        btn_manage_siglas.pack(side="left", padx=5)

        frame_results = tk.LabelFrame(self, text="Resultados da Aplicação", padx=10, pady=10)
        frame_results.pack(padx=10, pady=5, fill="both", expand=True)

        # --- NOVO: Treeview para exibir resultados em tabela ---
        self.tree_results = ttk.Treeview(frame_results, show="headings")
        self.tree_results.pack(fill="both", expand=True)

        # Scrollbar para o Treeview
        vsb = ttk.Scrollbar(frame_results, orient="vertical", command=self.tree_results.yview)
        vsb.pack(side='right', fill='y')
        self.tree_results.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(frame_results, orient="horizontal", command=self.tree_results.xview)
        hsb.pack(side='bottom', fill='x')
        self.tree_results.configure(xscrollcommand=hsb.set)

        # --- NOVO: ScrolledText para o texto formatado para cópia ---
        # Este será usado apenas para gerar o texto que vai para o clipboard
        self.formatted_text_for_clipboard = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=1, height=1)
        # Não empacotar, apenas manter para uso interno para gerar o texto para o clipboard
        # self.formatted_text_for_clipboard.pack_forget() # Certifica-se de que não está visível

    def perform_search(self):
        id_peca = self.id_entry.get().strip()
        if not id_peca:
            messagebox.showwarning("Entrada Inválida", "Por favor, digite o ID da peça.")
            return

        requested_fields_keys = [key for key, var in self.field_vars.items() if var.get()]
        
        if not requested_fields_keys:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione pelo menos um campo para a aplicação.")
            return

        # Limpa a Treeview antes de uma nova busca
        for item in self.tree_results.get_children():
            self.tree_results.delete(item)
        self.tree_results.config(columns=[]) # Limpa as colunas
        self.formatted_text_for_clipboard.delete(1.0, tk.END) # Limpa o texto interno

        self.update_idletasks() # Atualiza a interface para mostrar que está buscando

        raw_vehicles = buscar_dados_veiculos_authomix_graphql(id_peca)
        
        if not raw_vehicles:
            messagebox.showinfo("Sem Aplicações", "Nenhuma aplicação encontrada ou erro na busca.")
            return

        # Dicionário para agrupar as aplicações por (Marca, Modelo, Motor)
        # Cada entrada conterá uma lista de intervalos de anos e um set de observações
        grouped_applications_by_base = {} 

        for vehicle in raw_vehicles:
            brand = vehicle.get('brand', '')
            name = vehicle.get('name', '')
            model = vehicle.get('model', '')
            engine_name = vehicle.get('engineName', '')
            engine_config = vehicle.get('engineConfiguration', '')
            brake_system = vehicle.get('brakeSystem', '')
            start_year = vehicle.get('startYear') # Manter como int ou None
            end_year = vehicle.get('endYear')     # Manter como int ou None
            note = vehicle.get('note', '')
            only = vehicle.get('only', '')
            restriction = vehicle.get('restriction', '')

            # Aplicar sigla à marca, se existir no mapeamento
            display_brand = self.siglas_map.get(brand.upper(), brand)
            display_model = name if name else model
            display_motor = engine_config if engine_config else engine_name

            # Chave de agrupamento base: Marca, Modelo, Motor
            group_key_base = (display_brand, display_model, display_motor)

            # Coleta as observações para este veículo
            current_observations = []
            if note: current_observations.append(note)
            if only: current_observations.append(only)
            if restriction: current_observations.append(restriction)
            
            # Inicializa o grupo se não existir
            if group_key_base not in grouped_applications_by_base:
                grouped_applications_by_base[group_key_base] = {
                    'year_ranges': [], # Lista para armazenar tuplas (start_year, end_year)
                    'observations': set(), # Usar set para evitar observações duplicadas
                    'original_data_sample': vehicle # Manter uma amostra dos dados originais para outros campos
                }
            
            # Adiciona o intervalo de ano
            grouped_applications_by_base[group_key_base]['year_ranges'].append((start_year, end_year))
            
            # Adiciona as observações ao set
            for obs in current_observations:
                grouped_applications_by_base[group_key_base]['observations'].add(obs)

        # Lista para armazenar os dicionários de aplicações formatadas para a tabela
        applications_for_table = []
        # Lista para armazenar as strings formatadas para o clipboard
        applications_for_clipboard = []

        for key_base, data in grouped_applications_by_base.items():
            display_brand, display_model, display_motor = key_base
            
            # Consolida os intervalos de anos
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

            combined_observations = "; ".join(sorted(list(data['observations']))) # Ordena e junta observações

            # Usa a amostra de dados originais para pegar outros campos que não são agrupados
            original_sample = data['original_data_sample']

            # Dicionário com todos os valores possíveis para a linha da tabela
            full_field_values = {
                'marca': display_brand,
                'modelo': display_model,
                'motor': display_motor,
                'ano': ano_str,
                'observacao': combined_observations,
                'sistema_freio': original_sample.get('brakeSystem', ''),
                'restricao': original_sample.get('restriction', ''),
                'apenas': original_sample.get('only', '')
            }
            applications_for_table.append(full_field_values)

            # Prepara a string para o clipboard (usa apenas os campos selecionados)
            output_parts_clipboard = []
            for field_key in requested_fields_keys:
                value = full_field_values.get(field_key)
                if value:
                    output_parts_clipboard.append(str(value))
            
            aplicacao_formatada_clipboard = " ".join(output_parts_clipboard).strip()
            if aplicacao_formatada_clipboard:
                applications_for_clipboard.append(aplicacao_formatada_clipboard)

        # Ordena as aplicações para a tabela e para o clipboard
        # A ordenação aqui é pela string formatada para o clipboard, para manter consistência
        applications_for_clipboard_sorted = sorted(applications_for_clipboard)
        
        # Ordena as aplicações para a tabela com base na marca, modelo, motor e ano
        applications_for_table_sorted = sorted(applications_for_table, 
                                               key=lambda x: (x.get('marca', ''), x.get('modelo', ''), x.get('motor', ''), x.get('ano', '')))


        # --- NOVO: Configura e preenche a Treeview ---
        # Mapeia as chaves dos campos para os nomes de exibição
        display_names = [self.available_fields[key] for key in requested_fields_keys]
        
        self.tree_results.config(columns=requested_fields_keys) # Define as colunas internas
        
        for col_key, display_name in zip(requested_fields_keys, display_names):
            self.tree_results.heading(col_key, text=display_name)
            # CORREÇÃO: Substituído ttk.DEFAULT_WIDTH por um valor numérico
            self.tree_results.column(col_key, width=120, anchor='w') # Largura padrão, alinhado à esquerda

        # Ajusta a largura das colunas para caber o conteúdo
        for col_key in requested_fields_keys:
            max_width = 0
            # Calcula a largura do cabeçalho
            header_width = len(self.available_fields[col_key]) * 8 # Estimativa
            max_width = max(max_width, header_width)

            # Calcula a largura do conteúdo
            for app_data in applications_for_table_sorted:
                content_width = len(str(app_data.get(col_key, ''))) * 8 # Estimativa
                max_width = max(max_width, content_width)
            
            self.tree_results.column(col_key, width=max_width + 10) # Adiciona um padding

        for app_data in applications_for_table_sorted:
            # Pega os valores na ordem das colunas selecionadas
            values_for_row = [app_data.get(key, '') for key in requested_fields_keys]
            self.tree_results.insert("", "end", values=values_for_row)

        # Prepara o texto para o clipboard
        if applications_for_clipboard_sorted:
            formatted_output_clipboard = "*** APLICAÇÃO ***\r\n"
            for app_str in applications_for_clipboard_sorted:
                formatted_output_clipboard += app_str + "\r\n"
            self.formatted_text_for_clipboard.insert(tk.END, formatted_output_clipboard)
            pyperclip.copy(formatted_output_clipboard)
            messagebox.showinfo("Sucesso", "Aplicações encontradas e copiadas para a área de transferência!")
        else:
            messagebox.showinfo("Sem Aplicações", "Nenhuma aplicação encontrada após agrupamento e filtragem.")


    def copy_to_clipboard(self):
        text_to_copy = self.formatted_text_for_clipboard.get(1.0, tk.END).strip()
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
    
    def open_sigla_manager(self):
        SiglaManager(self, self.reload_siglas_map)

    def reload_siglas_map(self):
        self.siglas_map = load_siglas()
        messagebox.showinfo("Siglas Atualizadas", "O mapa de siglas foi recarregado.")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
