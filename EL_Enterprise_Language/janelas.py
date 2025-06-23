import tkinter as tk
from tkinter import ttk
import base64
import urllib.request
import json

# Importações de módulos internos
from produtos import Produtos
from clientes import Clientes
from financeiro import Graficos
import vendas
from inicio import Inicio


class Janelas:
    def __init__(self, root, usuario_logado):
        self.root = root
        self.usuario_logado = usuario_logado

        # Cores do tema
        self.cor_principal = "#1E3A5F"
        self.cor_secundaria = "#2C5EAA"
        self.cor_destaque = "#D9A87E"
        self.cor_fonte = "white"

        # Estrutura principal
        self.main_frame = tk.Frame(self.root, bg=self.cor_principal)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(self.main_frame, bg=self.cor_secundaria, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(self.main_frame, bg="white")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.paginas = {}

        # Lista de botões/páginas
        self.botoes = ["Inicio", "Financeiro", "Vendas", "Clientes", "Produtos", "Configurações", "Conta"]

        for btn in self.botoes:
            self.criar_botao_personalizado(self.sidebar, btn)

        self.criar_paginas()
        self.mudar_pagina("Produtos")  # Página padrão ao iniciar

    def criar_botao_personalizado(self, parent, texto):
        botao = tk.Button(
            parent,
            text=texto,
            font=("Arial", 12),
            bg=self.cor_secundaria,
            fg=self.cor_fonte,
            relief="raised",
            command=lambda: self.mudar_pagina(texto)
        )
        botao.pack(fill=tk.X, padx=10, pady=5)

    def mudar_pagina(self, nome_pagina):
        # Oculta todas as páginas visíveis
        for pagina in self.paginas.values():
            pagina.pack_forget()

        # Exibe a página solicitada, se existir
        if nome_pagina in self.paginas:
            self.paginas[nome_pagina].pack(fill=tk.BOTH, expand=True)
        else:
            print(f"[AVISO] Página '{nome_pagina}' não foi encontrada.")

    def criar_paginas(self):
        # Páginas principais
        self.paginas["Inicio"] = Inicio(self.content_frame).frame
        self.paginas["Produtos"] = Produtos(self.content_frame).frame
        self.paginas["Clientes"] = Clientes(self.content_frame).frame

        # Página de Vendas
        try:
            self.paginas["Vendas"] = vendas.Vendas(self.content_frame).frame
        except Exception as e:
            print(f"[ERRO] Falha ao carregar a página de Vendas: {e}")
            self.paginas["Vendas"] = tk.Frame(self.content_frame, bg="white")

        # Página de Configurações
        self.criar_pagina_configuracoes()

        # Página Financeiro
        self.criar_pagina_financeiro()

        # Página Conta (criada dinamicamente)
        self.criar_pagina_conta()

    def criar_pagina_financeiro(self):
        frame_financeiro = tk.Frame(self.content_frame, bg="white")
        try:
            Graficos(frame_financeiro)
        except Exception as e:
            print(f"[ERRO] Falha ao carregar página Financeiro: {e}")
        self.paginas["Financeiro"] = frame_financeiro

        # Adiciona o frame financeiro à página
        frame_financeiro.pack(fill=tk.BOTH, expand=True)

    def criar_pagina_configuracoes(self):
        frame_config = tk.Frame(self.content_frame, bg="white")
        try:
            from config import PainelControle
            PainelControle(frame_config, abrir_func=self.abrir_pagina)
        except Exception as e:
            print(f"[ERRO] Falha ao carregar Painel de Configurações: {e}")
        self.paginas["Configurações"] = frame_config

    def criar_pagina_conta(self):
        frame_conta = tk.Frame(self.content_frame, bg="white")
        try:
            from conta_user import ContaUser
            conta = ContaUser(frame_conta, self.usuario_logado)
            self.paginas["Conta"] = conta.frame
        except Exception as e:
            print(f"[ERRO] Falha ao carregar página Conta: {e}")
            self.paginas["Conta"] = frame_conta

    def abrir_pagina(self, nome):
        self.mudar_pagina(nome)
