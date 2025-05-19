import tkinter as tk
from tkinter import ttk, messagebox

class Vendas:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(self.frame, text="Vendas", font=("Arial", 24), bg="white")
        label.pack(pady=20)

        # Tabela de vendas
        self.tree = ttk.Treeview(self.frame, columns=("produto", "categoria", "valor", "data"), show="headings")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("valor", text="Valor (R$)")
        self.tree.heading("data", text="Data")
        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Botão para adicionar nova venda
        btn_add = tk.Button(self.frame, text="Adicionar Venda", font=("Arial", 12), bg="#22c55e", fg="white",
                            command=self.abrir_janela_adicionar)
        btn_add.pack(pady=10)

        # Carregar vendas (exemplo: lista fixa, depois pode ser de arquivo ou servidor)
        self.vendas = []
        self.carregar_vendas()

    def carregar_vendas(self):
        # Exemplo de vendas fixas (depois pode buscar de arquivo ou servidor)
        self.vendas = [
            {"produto": "Notebook", "categoria": "Eletrônicos", "valor": 3500, "data": "2025-05-18"},
            {"produto": "Camiseta", "categoria": "Presentes", "valor": 80, "data": "2025-05-17"},
        ]
        for venda in self.vendas:
            self.tree.insert("", tk.END, values=(venda["produto"], venda["categoria"], f'R$ {venda["valor"]:.2f}', venda["data"]))

    def abrir_janela_adicionar(self):
        janela = tk.Toplevel(self.frame)
        janela.title("Adicionar Venda")
        janela.geometry("350x250")

        tk.Label(janela, text="Produto:").pack(pady=5)
        entry_produto = tk.Entry(janela)
        entry_produto.pack(pady=5)

        tk.Label(janela, text="Categoria:").pack(pady=5)
        entry_categoria = tk.Entry(janela)
        entry_categoria.pack(pady=5)

        tk.Label(janela, text="Valor (R$):").pack(pady=5)
        entry_valor = tk.Entry(janela)
        entry_valor.pack(pady=5)

        tk.Label(janela, text="Data (AAAA-MM-DD):").pack(pady=5)
        entry_data = tk.Entry(janela)
        entry_data.pack(pady=5)

        def salvar():
            produto = entry_produto.get().strip()
            categoria = entry_categoria.get().strip()
            valor = entry_valor.get().strip()
            data = entry_data.get().strip()
            if not produto or not categoria or not valor or not data:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
            try:
                valor_float = float(valor.replace(",", "."))
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido.")
                return
            self.tree.insert("", tk.END, values=(produto, categoria, f'R$ {valor_float:.2f}', data))
            janela.destroy()

        tk.Button(janela, text="Salvar", bg="#22c55e", fg="white", font=("Arial", 12), command=salvar).pack(pady=10)