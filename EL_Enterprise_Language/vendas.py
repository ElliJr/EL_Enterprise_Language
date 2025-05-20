import tkinter as tk
from tkinter import ttk
import json

class Vendas:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        label = tk.Label(self.frame, text="Receita da Empresa", font=("Arial", 24), bg="white")
        label.pack(pady=20)

        # Tabela de receitas (produtos)
        self.tree = ttk.Treeview(self.frame, columns=("produto", "categoria", "valor", "estoque"), show="headings")
        self.tree.heading("produto", text="Produto")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("valor", text="Preço Venda (R$)")
        self.tree.heading("estoque", text="Estoque")
        self.tree.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Carregar produtos do JSON e exibir na tabela
        self.carregar_receita()

    def carregar_receita(self):
        try:
            with open("produtos.json", "r", encoding="utf-8") as f:
                produtos = json.load(f)
        except Exception:
            produtos = []

        # Limpa a tabela antes de preencher
        for item in self.tree.get_children():
            self.tree.delete(item)

        for p in produtos:
            self.tree.insert(
                "", tk.END,
                values=(
                    p.get("Produto", ""),
                    p.get("Categoria", ""),
                    f'R$ {float(p.get("Preço Venda", 0)):.2f}',
                    p.get("Estoque", "")
                )
            )