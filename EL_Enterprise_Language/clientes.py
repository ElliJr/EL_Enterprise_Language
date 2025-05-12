import tkinter as tk
from tkinter import ttk
from utils import carregar_dados, salvar_dados, abrir_janela_novo, remover_item


class Clientes:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="white")

        self.tree_clientes = ttk.Treeview(self.frame, columns=("#1", "#2", "#3", "#4"), show="headings")
        self.tree_clientes.heading("#1", text="Nome")
        self.tree_clientes.heading("#2", text="CPF")
        self.tree_clientes.heading("#3", text="Email")
        self.tree_clientes.heading("#4", text="Telefone")

        self.tree_clientes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.clientes = []
        carregar_dados("clientes.json", self.clientes, self.tree_clientes)

        self.secao_botoes_clientes = tk.Frame(self.frame, bg="white")
        self.secao_botoes_clientes.pack(pady=10)

        tk.Button(self.secao_botoes_clientes, text="+ Novo", font=("Arial", 12), bg="#2C5EAA", fg="white",
                  command=lambda: abrir_janela_novo(self.parent, "clientes.json", self.clientes, self.tree_clientes,
                                                   ["Nome", "CPF", "Email", "Telefone"])).grid(row=0, column=0, padx=10,
                                                                                               pady=10)
        tk.Button(self.secao_botoes_clientes, text="- Remover", font=("Arial", 12), bg="#2C5EAA", fg="white",
                  command=lambda: remover_item(self.parent, "clientes.json", self.clientes,
                                               self.tree_clientes)).grid(row=0, column=1, padx=10, pady=10)