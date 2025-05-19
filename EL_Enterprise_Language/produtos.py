import tkinter as tk
from tkinter import ttk

from utils import carregar_dados, salvar_dados, abrir_janela_novo, remover_item


class Produtos:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="white")
        
        self.tree_produtos = ttk.Treeview(self.frame, columns=("#1", "#2", "#3", "#4", "#5"), show="headings")
        self.tree_produtos.heading("#1", text="Cód")
        self.tree_produtos.heading("#2", text="Produto")
        self.tree_produtos.heading("#3", text="Categoria")
        self.tree_produtos.heading("#4", text="Preço Venda")
        self.tree_produtos.heading("#5", text="Estoque")

        self.tree_produtos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.produtos = []
        carregar_dados("produtos.json", self.produtos, self.tree_produtos)

        self.secao_botoes_produtos = tk.Frame(self.frame, bg="white")
        self.secao_botoes_produtos.pack(pady=10)

        tk.Button(self.secao_botoes_produtos, text="+ Novo", font=("Arial", 12), bg="#D9A87E", fg="white",
                  command=lambda: abrir_janela_novo(self.parent, "produtos.json", self.produtos, self.tree_produtos,
                                                   ["Nome do Produto", "Categoria", "Preço", "Estoque"])).grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=10,
                                                                                                              pady=10)
        tk.Button(self.secao_botoes_produtos, text="Remover", font=("Arial", 12), bg="#D9A87E", fg="white",
                  command=lambda: remover_item(self.parent, "produtos.json", self.produtos,
                                               self.tree_produtos)).grid(row=0, column=1, padx=10, pady=10)