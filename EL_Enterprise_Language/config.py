import tkinter as tk
import webbrowser

class PainelControle:
    def __init__(self, master):
        self.frame = tk.Frame(master, bg="#1E3A5F")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        tk.Label(self.frame, text="Painel de Controle", font=("Arial", 28), bg="#1E3A5F", fg="white").grid(row=0, column=0, columnspan=5, pady=(0, 20))

        # Cabeçalho
        tk.Label(self.frame, text="Categorias", font=("Arial", 14, "bold"), bg="#1E3A5F", fg="white").grid(row=1, column=1, sticky="w", padx=10)
        tk.Label(self.frame, text="Configuração dentro da Categoria", font=("Arial", 14, "bold"), bg="#1E3A5F", fg="white").grid(row=1, column=3, sticky="w", padx=10)

        categorias = [
            ("I.", "Contas de Usuário", "👤", "Ferramentas Administrativas", "🛠️"),
            ("II.", "Programas", "📦", "Grupo Doméstico", "🌐"),
            ("III.", "Rede e Internet", "🌐", "Gadgets da Área de Trabalho", "🖥️"),
            ("IV.", "Sistema e Segurança", "🔒", "Gerenciador de Credenciais", "🔑"),
        ]

        for i, (num, cat, icat, conf, iconf) in enumerate(categorias, start=2):
            # Numeração romana
            tk.Label(self.frame, text=num, font=("Arial", 12, "bold"), bg="#1E3A5F", fg="white").grid(row=i, column=0, sticky="e", padx=(10,0))
            # Categoria com ícone
            tk.Label(self.frame, text=icat, font=("Arial", 18), bg="#1E3A5F", fg="white").grid(row=i, column=1, sticky="e", padx=(0,0))
            tk.Button(self.frame, text=cat, font=("Arial", 12), bg="#2C5EAA", fg="white", relief="flat", 
                      command=lambda c=cat: self.acao_categoria(c)).grid(row=i, column=2, sticky="w", padx=(0,10), pady=5)
            # Espaço para "()" (radio button visual)
            tk.Label(self.frame, text="( )", font=("Arial", 14), bg="#1E3A5F", fg="white").grid(row=i, column=3, sticky="e")
            # Configuração dentro da categoria com ícone
            tk.Label(self.frame, text=iconf, font=("Arial", 18), bg="#1E3A5F", fg="white").grid(row=i, column=4, sticky="e", padx=(10,0))
            tk.Button(self.frame, text=conf, font=("Arial", 12), bg="#D9A87E", fg="black", relief="flat", 
                      command=lambda c=conf: self.acao_configuracao(c)).grid(row=i, column=5, sticky="w", padx=(0,10), pady=5)

        # Ajuste de colunas
        for col in range(6):
            self.frame.grid_columnconfigure(col, weight=0)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(5, weight=1)

    def acao_categoria(self, categoria):
        print(f"Clicou na categoria: {categoria}")

    def acao_configuracao(self, configuracao):
        print(f"Clicou na configuração: {configuracao}")

    def abrir_pagina_web(self):
        url = "https://www.exemplo.com"
        webbrowser.open_new_tab(url)

