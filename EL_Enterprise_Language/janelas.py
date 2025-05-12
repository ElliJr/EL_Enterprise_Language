import tkinter as tk
from tkinter import ttk
# from suporte import Suporte  # Importado dinamicamente
# from conta_user import ContaUser # Importado dinamicamente
from produtos import Produtos
from clientes import Clientes
import config

class Janelas:
    def __init__(self, root, usuario_logado):
        self.root = root
        self.usuario_logado = usuario_logado
        self.cor_principal = "#1E3A5F"
        self.cor_secundaria = "#2C5EAA"
        self.cor_destaque = "#D9A87E"
        self.cor_fonte = "white"
        self.main_frame = tk.Frame(self.root, bg=self.cor_principal)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_frame, bg=self.cor_secundaria, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(self.main_frame, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.paginas = {}

        botoes = ["Financeiro", "Vendas", "Compras", "Clientes", "Produtos", "Relatórios", "Configurações", "Suporte", "Conta"]
        for btn in botoes:
            self.criar_botao_personalizado(self.sidebar, btn)

        self.criar_paginas()
        self.mudar_pagina("Produtos")

    def criar_botao_personalizado(self, parent, texto):
        botao = tk.Button(parent, text=texto, font=("Arial", 12), bg=self.cor_secundaria, fg=self.cor_fonte,
                          relief="raised", command=lambda: self.mudar_pagina(texto))
        botao.pack(fill=tk.X, padx=10, pady=5)

    def mudar_pagina(self, nome_pagina):
        for pagina in self.paginas.values():
            pagina.pack_forget()
        self.paginas[nome_pagina].pack(fill=tk.BOTH, expand=True)
    
    def criar_pagina_configuracoes(self):
        frame_config = tk.Frame(self.content_frame, bg="white")
        label_titulo = tk.Label(frame_config, text="Configurações", font=("Arial", 24), bg="white")
        label_titulo.pack(pady=20)

        def mudar_para_claro():
            config.set_tema("Claro")
            from utils import aplicar_tema
            aplicar_tema(self.root)
            # Recarregue as cores dos widgets abertos, se necessário

            botao_claro = tk.Button(frame_config, text="Tema Claro", command=mudar_para_claro)
            botao_claro.pack(pady=10)

        def mudar_para_escuro():
            config.set_tema("Escuro")
            from utils import aplicar_tema
            aplicar_tema(self.root)
            # Recarregue as cores dos widgets abertos, se necessário

            botao_escuro = tk.Button(frame_config, text="Tema Escuro", command=mudar_para_escuro)
            botao_escuro.pack(pady=10)

        self.paginas["Configurações"] = frame_config
    
    def criar_paginas(self):
        for nome in ["Financeiro", "Vendas", "Compras", "Relatórios", "Configurações"]:
            frame = tk.Frame(self.content_frame, bg="white")
            label = tk.Label(frame, text=nome, font=("Arial", 24), bg="white")
            label.pack(pady=20)
            self.paginas[nome] = frame

        # Cria as páginas de Clientes e Produtos usando as classes separadas
        self.paginas["Produtos"] = Produtos(self.content_frame).frame
        self.paginas["Clientes"] = Clientes(self.content_frame).frame

        # Criação das páginas Suporte e Conta (importadas dinamicamente)
        def criar_pagina_suporte():
            from suporte import Suporte
            self.paginas["Suporte"] = Suporte(self.content_frame).frame # instancia e pega o frame
        def criar_pagina_conta():
            from conta_user import ContaUser
            self.paginas["Conta"] = ContaUser(self.content_frame, self.usuario_logado).frame # instancia e pega o frame

        # Adiciona os comandos de criação de página aos botões
        for nome_botao, funcao_criar in [("Suporte", criar_pagina_suporte), ("Conta", criar_pagina_conta)]:
            botao = self.sidebar.winfo_children()[["Financeiro", "Vendas", "Compras", "Clientes", "Produtos", "Relatórios", "Configurações", "Suporte", "Conta"].index(nome_botao)] # Pega o botão da sidebar
            botao.config(command=lambda nome=nome_botao, func=funcao_criar: [func(), self.mudar_pagina(nome)]) # Atualiza o comando do botão

        criar_pagina_suporte() # Cria a página de suporte inicialmente
        criar_pagina_conta() # Cria a página conta inicialmente