import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json

class Vendas:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        label = tk.Label(self.frame, text="Receita da Empresa", font=("Arial", 24), bg="white")
        label.pack(pady=20)

        # Botão de adicionar nova venda
        btn_add = tk.Button(
            self.frame, text="Adicionar Nova Venda", bg="#2C5EAA", fg="white",
            font=("Arial", 12, "bold"), relief="raised", cursor="hand2",
            command=self.adicionar_venda
        )
        btn_add.pack(pady=(0, 10))

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

    def adicionar_venda(self):
        # Diálogo simples para adicionar nova venda
        produto = simpledialog.askstring("Novo Produto", "Nome do produto:")
        if not produto:
            return
        categoria = simpledialog.askstring("Categoria", "Categoria do produto:")
        if not categoria:
            return
        try:
            valor = float(simpledialog.askstring("Preço", "Preço de venda (R$):"))
        except (TypeError, ValueError):
            messagebox.showerror("Erro", "Preço inválido.")
            return
        try:
            estoque = int(simpledialog.askstring("Estoque", "Quantidade em estoque:"))
        except (TypeError, ValueError):
            messagebox.showerror("Erro", "Estoque inválido.")
            return

        # Carrega produtos existentes
        try:
            with open("produtos.json", "r", encoding="utf-8") as f:
                produtos = json.load(f)
        except Exception:
            produtos = []

        # Adiciona novo produto
        produtos.append({
            "Produto": produto,
            "Categoria": categoria,
            "Preço Venda": valor,
            "Estoque": estoque
        })

        # Salva no arquivo
        try:
            with open("produtos.json", "w", encoding="utf-8") as f:
                json.dump(produtos, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Sucesso", "Venda adicionada com sucesso!")
            self.carregar_receita()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")