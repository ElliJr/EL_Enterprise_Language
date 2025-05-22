import tkinter as tk
from tkinter import ttk
# from suporte import Suporte  # Importado dinamicamente
# from conta_user import ContaUser # Importado dinamicamente
from produtos import Produtos
from clientes import Clientes
from financeiro import Graficos
# Importe o módulo financeiro
import vendas
import base64
import urllib.request
import json
from inicio import Inicio

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

        botoes = ["Inicio","Financeiro", "Vendas", "Clientes", "Produtos", "Configurações", "Conta"]
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

    def criar_pagina_financeiro(self):
        frame_financeiro = tk.Frame(self.content_frame, bg="white")
        label_titulo = tk.Label(frame_financeiro, text="Gráficos", font=("Arial", 24), bg="white")
        label_titulo.pack(pady=20)

        # Crie os widgets para exibir os gráficos (Labels para as imagens)
        self.label_rendimento = tk.Label(frame_financeiro, bg="white")
        self.label_rendimento.pack(pady=10)
        self.label_faturamento = tk.Label(frame_financeiro, bg="white")
        self.label_faturamento.pack(pady=10)

        # Botão para atualizar os gráficos
        btn_atualizar_graficos = tk.Button(frame_financeiro, text="Atualizar Gráficos", command=self.atualizar_graficos)
        btn_atualizar_graficos.pack(pady=10)

        # Botão para abrir gráfico de pizza
        btn_piechart = tk.Button(
            frame_financeiro,
            text="Abrir Gráfico de Pizza",
            bg="#2C5EAA",
            fg="white",
            font=("Arial", 12),
            command=self.abrir_grafico_pizza
        )
        btn_piechart.pack(pady=10)

        self.paginas["Financeiro"] = frame_financeiro
        self.atualizar_graficos()

    def abrir_grafico_pizza(self):
        # Exemplo: valores fictícios, troque por dados reais do seu sistema se quiser
       Graficos.generate_pie_chart([10, 20, 30])

    def criar_pagina_configuracoes(self):
        # Cria um frame para a página de configurações
        frame_config = tk.Frame(self.content_frame, bg="white")
        # Instancia o PainelControle dentro desse frame
        from config import PainelControle
        painel = PainelControle(frame_config, abrir_func=self.abrir_pagina)
        # Adiciona o frame à lista de páginas
        self.paginas["Configurações"] = frame_config

    def criar_paginas(self):
        # Cria a página Inicio personalizada
        self.paginas["Inicio"] = Inicio(self.content_frame).frame

        # Cria a página Vendas (pode ser personalizada também)
        frame_vendas = tk.Frame(self.content_frame, bg="white")
        label_vendas = tk.Label(frame_vendas, text="Vendas", font=("Arial", 24), bg="white")
        label_vendas.pack(pady=20)
        self.paginas["Vendas"] = frame_vendas

        self.criar_pagina_configuracoes()  # Página de configurações

        # Cria as páginas de Clientes e Produtos usando as classes separadas
        self.paginas["Produtos"] = Produtos(self.content_frame).frame
        self.paginas["Clientes"] = Clientes(self.content_frame).frame
        self.paginas["Vendas"] = vendas.Vendas(self.content_frame).frame

        # Criação das páginas Suporte e Conta (importadas dinamicamente)
        def criar_pagina_conta():
            from conta_user import ContaUser
            self.paginas["Conta"] = ContaUser(self.content_frame, self.usuario_logado).frame

        for nome_botao, funcao_criar in [("Conta", criar_pagina_conta)]:
            botao = self.sidebar.winfo_children()[["Inicio","Financeiro", "Vendas", "Clientes", "Produtos", "Configurações", "Conta"].index(nome_botao)]
            botao.config(command=lambda nome=nome_botao, func=funcao_criar: [func(), self.mudar_pagina(nome)])
        criar_pagina_conta()

        # Cria a página Financeiro

                    # Configure header colors if needed

    def abrir_pagina(self, nome):
        self.mudar_pagina(nome)

  # Abre a janela de gráficos
