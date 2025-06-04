import tkinter as tk
from tkinter import ttk, messagebox
import json # Adicionado para lidar com arquivos JSON nos mocks

# Assuming utils.py is in the same directory or accessible via PYTHONPATH
# We'll also modify the mocks to correctly handle the dictionary format.
try:
    from utils import carregar_dados, salvar_dados, abrir_janela_novo, remover_item
except ImportError:
    print("AVISO: Arquivo utils.py não encontrado. Usando mocks para teste.")
    # Mocks para as funções de utils para teste local, adaptados para lidar com dicionários
    def carregar_dados(arquivo_json, lista_dados, treeview):
        print(f"MOCK: Carregando dados de {arquivo_json}")
        # Popula com alguns dados de exemplo no formato de dicionário
        dados_exemplo = [
            {'Nome do Produto': 'fone', 'Categoria': 'acessorio', 'Preço': '34.99', 'Estoque': '12'},
            {'Nome do Produto': 'camisa', 'Categoria': 'acessorio', 'Preço': '29.99', 'Estoque': '210'},
            {'Nome do Produto': 'cama', 'Categoria': 'movel', 'Preço': '120.90', 'Estoque': '200'},
            {'Nome do Produto': 'Teclado Mecânico', 'Categoria': 'Periféricos', 'Preço': '150.00', 'Estoque': '50'},
            {'Nome do Produto': 'Mouse Sem Fio', 'Categoria': 'Periféricos', 'Preço': '75.00', 'Estoque': '80'},
        ]
        
        lista_dados.clear()
        for item in dados_exemplo:
            lista_dados.append(item)
        
        # Limpa treeview antes de popular
        for i in treeview.get_children():
            treeview.delete(i)
        
        # Insere dados no treeview, extraindo os valores do dicionário
        for item_data in lista_dados:
            # Garante a ordem correta dos valores para as colunas do treeview
            treeview.insert("", tk.END, values=(
                item_data.get('Nome do Produto', ''),
                item_data.get('Categoria', ''),
                item_data.get('Preço', ''),
                item_data.get('Estoque', '')
            ))
        
        # Tenta simular a leitura de um JSON para maior realismo no mock
        try:
            with open(arquivo_json, 'w') as f:
                json.dump(lista_dados, f, indent=4)
        except IOError:
            print(f"MOCK: Não foi possível escrever no arquivo {arquivo_json}")


    def abrir_janela_novo(parent, arquivo_json, lista_dados, treeview, campos):
        print(f"MOCK: Abrindo janela para novo item em {arquivo_json} com campos {campos}")
        
        # Cria uma janela mock para entrada de dados
        dialog = tk.Toplevel(parent)
        dialog.title("Novo Produto (Mock)")
        dialog.transient(parent)
        dialog.grab_set()

        entries = {}
        for i, campo in enumerate(campos):
            tk.Label(dialog, text=campo).grid(row=i, column=0, padx=5, pady=2)
            entry = ttk.Entry(dialog)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[campo] = entry

        def on_salvar():
            novo_item = {}
            for campo, entry in entries.items():
                novo_item[campo] = entry.get()
            
            # Adiciona o novo item à lista de dados
            lista_dados.append(novo_item)

            # Salva os dados no arquivo JSON (mock)
            try:
                with open(arquivo_json, 'w') as f:
                    json.dump(lista_dados, f, indent=4)
            except IOError:
                print(f"MOCK: Não foi possível escrever no arquivo {arquivo_json}")

            # Repopula o treeview
            for i in treeview.get_children():
                treeview.delete(i)
            for item_data in lista_dados:
                treeview.insert("", tk.END, values=(
                    item_data.get('Nome do Produto', ''),
                    item_data.get('Categoria', ''),
                    item_data.get('Preço', ''),
                    item_data.get('Estoque', '')
                ))
            messagebox.showinfo("Mock", "Novo produto adicionado (simulado).", parent=dialog)
            dialog.destroy()

        ttk.Button(dialog, text="Salvar", command=on_salvar).grid(row=len(campos), column=0, columnspan=2, pady=10)
        parent.wait_window(dialog) # Espera a janela fechar


    def remover_item(parent, arquivo_json, lista_dados, treeview):
        selected_item_iid = treeview.focus() # Obtém o IID do item focado/selecionado
        if not selected_item_iid:
            messagebox.showwarning("Remover", "Nenhum produto selecionado para remover.", parent=parent)
            return

        # Obtém os valores do item selecionado no Treeview
        item_values_tuple = treeview.item(selected_item_iid, 'values')
        
        # Converte os valores do treeview para um dicionário para comparação
        # Isso assume uma ordem e chaves consistentes com a forma como os dados são armazenados
        selected_product_dict_candidate = {
            'Nome do Produto': item_values_tuple[0],
            'Categoria': item_values_tuple[1],
            'Preço': item_values_tuple[2],
            'Estoque': item_values_tuple[3]
        }

        item_found = False
        # Itera sobre lista_dados para encontrar e remover o dicionário correspondente
        for i, produto_in_list in enumerate(lista_dados):
            # Compara dicionário por dicionário. Isso é mais robusto do que comparar listas de valores se a ordem puder variar.
            # No entanto, para fins de remoção, comparar os valores exibidos no treeview com os valores no dicionário original
            # é a forma mais direta, assumindo que as colunas do treeview correspondem às chaves do dicionário.
            if (produto_in_list.get('Nome do Produto') == selected_product_dict_candidate.get('Nome do Produto') and
                produto_in_list.get('Categoria') == selected_product_dict_candidate.get('Categoria') and
                produto_in_list.get('Preço') == selected_product_dict_candidate.get('Preço') and
                produto_in_list.get('Estoque') == selected_product_dict_candidate.get('Estoque')):
                
                del lista_dados[i]
                item_found = True
                break
        
        if item_found:
            print(f"MOCK: Removendo item correspondente a {item_values_tuple} de {arquivo_json}")
            # Salva os dados atualizados no arquivo JSON (mock)
            try:
                with open(arquivo_json, 'w') as f:
                    json.dump(lista_dados, f, indent=4)
            except IOError:
                print(f"MOCK: Não foi possível escrever no arquivo {arquivo_json}")
            
            # Repopula o treeview
            for i in treeview.get_children():
                treeview.delete(i)
            for item_data in lista_dados:
                treeview.insert("", tk.END, values=(
                    item_data.get('Nome do Produto', ''),
                    item_data.get('Categoria', ''),
                    item_data.get('Preço', ''),
                    item_data.get('Estoque', '')
                ))
            messagebox.showinfo("Mock", "Produto removido (simulado).", parent=parent)
        else:
            messagebox.showwarning("Remover", "Não foi possível encontrar o produto selecionado nos dados internos.", parent=parent)

class Produtos:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="white")
        # self.frame.pack(fill=tk.BOTH, expand=True) # Packing of self.frame is usually done by the caller

        # --- Seção de Pesquisa ---
        self.frame_pesquisa = tk.Frame(self.frame, bg="white")
        self.frame_pesquisa.pack(fill=tk.X, padx=10, pady=(10, 0))

        lbl_pesquisa = tk.Label(self.frame_pesquisa, text="Pesquisar Produto:", font=("Arial", 11), bg="white")
        lbl_pesquisa.pack(side=tk.LEFT, padx=(0, 5))

        self.texto_pesquisa = tk.StringVar()
        # Adiciona um "trace" que chama self.filtrar_produtos_callback sempre que self.texto_pesquisa mudar
        self.texto_pesquisa.trace_add("write", self.filtrar_produtos_callback) 
        
        self.entry_pesquisa = ttk.Entry(self.frame_pesquisa, textvariable=self.texto_pesquisa, font=("Arial", 11), width=40)
        self.entry_pesquisa.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # --- Treeview para exibir produtos ---
        self.tree_produtos = ttk.Treeview(self.frame, columns=("Produto", "Categoria", "Preço Venda", "Estoque"), show="headings")
        self.tree_produtos.heading("Produto", text="Nome do Produto") # Alterado para refletir a chave no dicionário
        self.tree_produtos.heading("Categoria", text="Categoria")
        self.tree_produtos.heading("Preço Venda", text="Preço") # Alterado
        self.tree_produtos.heading("Estoque", text="Estoque")

        # Ajustar largura das colunas (opcional, mas recomendado)
        self.tree_produtos.column("Produto", width=200, minwidth=150, stretch=tk.YES)
        self.tree_produtos.column("Categoria", width=150, minwidth=100, stretch=tk.YES)
        self.tree_produtos.column("Preço Venda", width=100, minwidth=80, stretch=tk.NO, anchor=tk.E) # Preço à direita
        self.tree_produtos.column("Estoque", width=80, minwidth=60, stretch=tk.NO, anchor=tk.E)  # Estoque à direita
        
        self.tree_produtos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.produtos = [] # Lista mestre de todos os produtos
        # carregar_dados deve popular self.produtos e também o self.tree_produtos inicialmente
        carregar_dados("produtos.json", self.produtos, self.tree_produtos)

        # --- Seção de Botões ---
        self.secao_botoes_produtos = tk.Frame(self.frame, bg="white")
        self.secao_botoes_produtos.pack(pady=10)

        tk.Button(self.secao_botoes_produtos, text="+ Novo", font=("Arial", 12), bg="#D9A87E", fg="white",
                  command=self.abrir_janela_novo_produto_wrapper).grid(row=0, column=0, padx=10, pady=10)
        
        tk.Button(self.secao_botoes_produtos, text="Remover", font=("Arial", 12), bg="#D9A87E", fg="white",
                  command=self.remover_produto_wrapper).grid(row=0, column=1, padx=10, pady=10)

    def filtrar_produtos_callback(self, *args):
        """
        Chamado automaticamente quando o texto na entry de pesquisa muda.
        Filtra os produtos exibidos no Treeview.
        """
        termo_pesquisa = self.texto_pesquisa.get().lower().strip()
        
        # Limpa o Treeview antes de re-popular
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)
            
        if not termo_pesquisa: # Se a pesquisa estiver vazia, mostra todos os produtos
            for produto_data in self.produtos:
                if isinstance(produto_data, dict): # Garante que é um dicionário
                    self.tree_produtos.insert("", tk.END, values=(
                        produto_data.get('Nome do Produto', ''),
                        produto_data.get('Categoria', ''),
                        produto_data.get('Preço', ''),
                        produto_data.get('Estoque', '')
                    ))
        else:
            # Filtra os produtos da lista mestre (self.produtos)
            for produto_data in self.produtos:
                if isinstance(produto_data, dict): # Garante que é um dicionário
                    # Assumindo que a pesquisa é pelo 'Nome do Produto'
                    nome_produto = produto_data.get('Nome do Produto', '').lower()
                    if termo_pesquisa in nome_produto:
                        self.tree_produtos.insert("", tk.END, values=(
                            produto_data.get('Nome do Produto', ''),
                            produto_data.get('Categoria', ''),
                            produto_data.get('Preço', ''),
                            produto_data.get('Estoque', '')
                        ))
    
    def abrir_janela_novo_produto_wrapper(self):
        """
        Wrapper para a função de abrir janela de novo produto,
        garantindo que o filtro seja reaplicado após a adição.
        """
        # Os campos devem corresponder às chaves no dicionário de produto
        campos_novo_produto = ["Nome do Produto", "Categoria", "Preço", "Estoque"]
        # A função abrir_janela_novo deve atualizar self.produtos e o arquivo json,
        # e também repopular self.tree_produtos com a lista completa atualizada.
        abrir_janela_novo(self.parent, "produtos.json", self.produtos, self.tree_produtos, campos_novo_produto)
        
        # Após a adição e repopulação total do treeview pela util,
        # reaplica o filtro para manter a visualização filtrada se houver texto na pesquisa.
        self.filtrar_produtos_callback() 

    def remover_produto_wrapper(self):
        """
        Wrapper para a função de remover item,
        garantindo que o filtro seja reaplicado após a remoção.
        """
        # A função remover_item deve atualizar self.produtos e o arquivo json,
        # e também repopular self.tree_produtos com a lista completa atualizada.
        remover_item(self.parent, "produtos.json", self.produtos, self.tree_produtos)
        
        # Após a remoção e repopulação total do treeview pela util,
        # reaplica o filtro.
        self.filtrar_produtos_callback()

# Exemplo de como usar a classe Produtos (coloque isso no seu arquivo principal da aplicação)
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Teste da Página de Produtos")
    root.geometry("700x500")
    
    # Cria uma instância da página de Produtos, passando o root como 'parent'
    pagina_produtos = Produtos(root)
    # O frame principal da classe Produtos (pagina_produtos.frame) precisa ser empacotado
    pagina_produtos.frame.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()