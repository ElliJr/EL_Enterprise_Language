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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

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

        # Input para valores
        label_input = tk.Label(frame_financeiro, text="Digite os valores separados por vírgula:", bg="white")
        label_input.pack(pady=5)
        entry_valores = tk.Entry(frame_financeiro, width=40)
        entry_valores.pack(pady=5)

        # Frame para o gráfico
        frame_grafico = tk.Frame(frame_financeiro, bg="white")
        frame_grafico.pack(pady=10, fill=tk.BOTH, expand=True)

        def desenhar_grafico():
            # Limpa o gráfico anterior, se houver
            for widget in frame_grafico.winfo_children():
                widget.destroy()
            try:
                valores = [float(v.strip()) for v in entry_valores.get().split(",") if v.strip()]
                if not valores:
                    raise ValueError("Digite ao menos um valor.")
                labels = [f'Valor {i+1}' for i in range(len(valores))]
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.pie(valores, labels=labels, autopct='%1.1f%%')
                ax.set_title('Gráfico de Pizza')
                ax.axis('equal')
                canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
                canvas.draw()
                canvas.get_tk_widget().pack()
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Valores inválidos: {e}")

        btn_gerar = tk.Button(frame_financeiro, text="Gerar Gráfico de Pizza", command=desenhar_grafico, bg="#2C5EAA", fg="white")
        btn_gerar.pack(pady=10)

        self.paginas["Financeiro"] = frame_financeiro

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
        self.criar_pagina_financeiro()

                    # Configure header colors if needed

    def abrir_pagina(self, nome):
        self.mudar_pagina(nome)

Graficos()  # Abre a janela de gráficos
