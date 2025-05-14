import tkinter as tk
from tkinter import ttk
# from suporte import Suporte  # Importado dinamicamente
# from conta_user import ContaUser # Importado dinamicamente
from produtos import Produtos
from clientes import Clientes
import config
# Importe o módulo financeiro
import financeiro
import base64
import urllib.request
import json

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

    def criar_pagina_financeiro(self):
        """Cria a página Financeiro e exibe os gráficos."""
        frame_financeiro = tk.Frame(self.content_frame, bg="white")
        label_titulo = tk.Label(frame_financeiro, text="Financeiro", font=("Arial", 24), bg="white")
        label_titulo.pack(pady=20)

        # Crie os widgets para exibir os gráficos (Labels para as imagens)
        self.label_rendimento = tk.Label(frame_financeiro, bg="white")
        self.label_rendimento.pack(pady=10)
        self.label_faturamento = tk.Label(frame_financeiro, bg="white")
        self.label_faturamento.pack(pady=10)

        # Botão para atualizar os gráficos
        btn_atualizar_graficos = tk.Button(frame_financeiro, text="Atualizar Gráficos", command=self.atualizar_graficos)
        btn_atualizar_graficos.pack(pady=10)

        self.paginas["Financeiro"] = frame_financeiro
        self.atualizar_graficos() #carrega os gráficos assim que a página é criada

    def atualizar_graficos(self):
        """Obtém os gráficos do servidor e os exibe na página."""
        # Tipo de gráfico (mês ou ano) - você pode adicionar uma forma de o usuário escolher
        tipo_grafico = "mes"

        # URL do servidor para obter os gráficos
        url = f"http://127.0.0.1:3000/graficos?tipo_grafico={tipo_grafico}"

        try:
            # Envia a requisição para o servidor
            with urllib.request.urlopen(url) as response:
                if response.getcode() == 200:
                    # Carrega a resposta JSON
                    graficos_json = json.loads(response.read().decode('utf-8'))

                    # Decodifica as imagens base64 e exibe nos Labels
                    imagem_rendimento_base64 = graficos_json["rendimento"]
                    imagem_faturamento_base64 = graficos_json["faturamento"]

                    # Exibe o gráfico de rendimento
                    if imagem_rendimento_base64:  # Verifica se a string não está vazia
                        imagem_rendimento_bytes = base64.b64decode(imagem_rendimento_base64)
                        imagem_rendimento_tk = tk.PhotoImage(data=imagem_rendimento_bytes)
                        self.label_rendimento.config(image=imagem_rendimento_tk)
                        self.label_rendimento.image = imagem_rendimento_tk  # Garante que a imagem não seja coletada pelo GC

                    # Exibe o gráfico de faturamento
                    if imagem_faturamento_base64:
                        imagem_faturamento_bytes = base64.b64decode(imagem_faturamento_base64)
                        imagem_faturamento_tk = tk.PhotoImage(data=imagem_faturamento_bytes)
                        self.label_faturamento.config(image=imagem_faturamento_tk)
                        self.label_faturamento.image = imagem_faturamento_tk

                else:
                    print(f"Erro ao obter gráficos do servidor: {response.getcode()}")
                    tk.messagebox.showerror("Erro", f"Erro ao obter gráficos: {response.getcode()}")

        except Exception as e:
            print(f"Erro ao conectar com o servidor: {e}")
            tk.messagebox.showerror("Erro", f"Erro ao conectar com o servidor: {e}")

    def criar_pagina_configuracoes(self):
        frame_config = tk.Frame(self.content_frame, bg="white")
        label_titulo = tk.Label(frame_config, text="Configurações", font=("Arial", 24), bg="white")
        label_titulo.pack(pady=20)

        def mudar_para_claro():
            config.set_tema("Claro")
            from utils import aplicar_tema
            aplicar_tema(self.root)
            # Recarregue as cores dos widgets abertos, se necessário
            self.aplicar_cores_tema()  # Chama a função para atualizar as cores

        botao_claro = tk.Button(frame_config, text="Tema Claro", command=mudar_para_claro)
        botao_claro.pack(pady=10)

        def mudar_para_escuro():
            config.set_tema("Escuro")
            from utils import aplicar_tema
            aplicar_tema(self.root)
            # Recarregue as cores dos widgets abertos, se necessário
            self.aplicar_cores_tema()  # Chama a função para atualizar as cores

        botao_escuro = tk.Button(frame_config, text="Tema Escuro", command=mudar_para_escuro)
        botao_escuro.pack(pady=10)

        def mudar_para_padrao():
            config.set_tema("Padrao")
            from utils import aplicar_tema
            aplicar_tema(self.root)
            # Recarregue as cores dos widgets abertos, se necessário
            self.aplicar_cores_tema()  # Chama a função para atualizar as cores

        botao_padrao = tk.Button(frame_config, text="Tema Padrao", command=mudar_para_padrao)
        botao_padrao.pack(pady=10)

        self.paginas["Configurações"] = frame_config

    def criar_paginas(self):
        for nome in ["Vendas", "Compras", "Relatórios"]:
            frame = tk.Frame(self.content_frame, bg="white")
            label = tk.Label(frame, text=nome, font=("Arial", 24), bg="white")
            label.pack(pady=20)
            self.paginas[nome] = frame

        self.criar_pagina_configuracoes()  # Chamando a função para criar a página de configurações

        # Cria as páginas de Clientes e Produtos usando as classes separadas
        self.paginas["Produtos"] = Produtos(self.content_frame).frame
        self.paginas["Clientes"] = Clientes(self.content_frame).frame

        # Criação das páginas Suporte e Conta (importadas dinamicamente)
        def criar_pagina_suporte():
            from suporte import Suporte
            self.paginas["Suporte"] = Suporte(self.content_frame).frame  # instancia e pega o frame

        def criar_pagina_conta():
            from conta_user import ContaUser
            self.paginas["Conta"] = ContaUser(self.content_frame, self.usuario_logado).frame  # instancia e pega o frame

        # Adiciona os comandos de criação de página aos botões
        for nome_botao, funcao_criar in [("Suporte", criar_pagina_suporte), ("Conta", criar_pagina_conta)]:
            botao = self.sidebar.winfo_children()[["Financeiro", "Vendas", "Compras", "Clientes", "Produtos", "Relatórios", "Configurações", "Suporte", "Conta"].index(nome_botao)]  # Pega o botão da sidebar
            botao.config(command=lambda nome=nome_botao, func=funcao_criar: [func(), self.mudar_pagina(nome)])  # Atualiza o comando do botão

        criar_pagina_suporte()  # Cria a página de suporte inicialmente
        criar_pagina_conta()  # Cria a página conta inicialmente

        # Cria a página Financeiro
        frame_financeiro = tk.Frame(self.content_frame, bg="white")
        # Instancia a classe Financeiro e obtém o frame
        financeiro_content = financeiro.Financeiro(frame_financeiro)
        self.paginas["Financeiro"] = financeiro_content.frame # Atribui o frame à página "Financeiro"

    def aplicar_cores_tema(self):
        tema = config.get_tema()
        if tema == "Claro":
            self.root.config(bg="white")
            self.main_frame.config(bg="#f0f0f0")
            self.sidebar.config(bg="#e0e0e0")
            self.content_frame.config(bg="white")
            for btn in self.sidebar.winfo_children():
                if isinstance(btn, tk.Button):
                    btn.config(bg="#e0e0e0", fg="black")
            for pagina in self.paginas.values():
                pagina.config(bg="white")
                for widget in pagina.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg="white", fg="black")
                    elif isinstance(widget, tk.Button):
                        widget.config(bg="#e0e0e0", fg="black")
                    elif isinstance(widget, ttk.Treeview):
                        widget.config(background="white", foreground="black")
                    # Configure header colors if needed
        elif tema == "Escuro":
            self.root.config(bg="#333333")
            self.main_frame.config(bg="#222222")
            self.sidebar.config(bg="#444444")
            self.content_frame.config(bg="#333333")
            for btn in self.sidebar.winfo_children():
                if isinstance(btn, tk.Button):
                    btn.config(bg="#444444", fg="white")
            for pagina in self.paginas.values():
                pagina.config(bg="#333333")
                for widget in pagina.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg="#333333", fg="white")  # 333333
                    elif isinstance(widget, tk.Button):
                        widget.config(bg="#444444", fg="white")
                    elif isinstance(widget, ttk.Treeview):
                        widget.config(background="#333333", foreground="white")
                    # Configure header colors if needed
        elif tema == "Padrao":
            self.root.config(bg="white")
            self.main_frame.config(bg="#1E3A5F")
            self.sidebar.config(bg="#2C5EAA")
            self.content_frame.config(bg="white")
            for btn in self.sidebar.winfo_children():
                if isinstance(btn, tk.Button):
                    btn.config(bg="#2C5EAA", fg="white")
            for pagina in self.paginas.values():
                pagina.config(bg="white")
                for widget in pagina.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg="white", fg="black")
                    elif isinstance(widget, tk.Button):
                        widget.config(bg="white", fg="black")
                    elif isinstance(widget, ttk.Treeview):
                        widget.config(background="white", foreground="black")
                    # Configure header colors if needed
