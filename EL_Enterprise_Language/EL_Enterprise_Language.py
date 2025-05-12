# # Estrutura do Projeto

# A ideia é dividir o sistema em vários arquivos para facilitar a manutenção e o desenvolvimento. A estrutura geral seria:

# -   `main.py`: Ponto de entrada do sistema.
# -   `login.py`: Lógica da tela de login e cadastro.
# -   `janelas.py`: Criação das janelas da aplicação (chat, suporte, etc.).
# -   `conta_user.py`: Lógica da página de conta do usuário.
# -   `produtos.py`: Lógica da página de produtos.
# -   `clientes.py`: Lógica da página de clientes.
# -   `suporte.py`: Lógica da página de suporte.
# -   `utils.py`: Funções utilitárias (carregar/salvar dados, etc.).

# ## main.py

# ```python
# import tkinter as tk
# from login import LoginTela
# # from janelas import Janelas  # Removido para evitar dependência circular

# if __name__ == "__main__":
#     root = tk.Tk()
#     login_tela = LoginTela(root) # Instancia a tela de login
#     root.mainloop()
# ```

# ## login.py

# ```python
# import tkinter as tk
# from tkinter import messagebox
# import json
# import os
# # from janelas import Janelas # Importado dinamicamente dentro da classe
# from conta_user import ContaUser  # Importa a classe ContaUser

# class LoginTela:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("EL Enterprise Language⚙️")
#         self.root.geometry("1300x800")
#         self.cor_principal = "#1E3A5F"
#         self.cor_secundaria = "#2C5EAA"
#         self.cor_destaque = "#D9A87E"
#         self.cor_fonte = "white"
#         self.login_tela()

#     def login_tela(self):
#         self.login_frame = tk.Frame(self.root, bg=self.cor_principal)
#         self.login_frame.pack(fill=tk.BOTH, expand=True)

#         label_titulo = tk.Label(self.login_frame, text="Sistema de Gerenciamento", font=("Arial", 24), fg=self.cor_fonte, bg=self.cor_principal)
#         label_titulo.pack(pady=20)

#         label_usuario = tk.Label(self.login_frame, text="Usuário:", font=("Arial", 14), fg=self.cor_fonte, bg=self.cor_principal)
#         label_usuario.pack(pady=5)
#         self.entry_usuario = tk.Entry(self.login_frame, font=("Arial", 14))
#         self.entry_usuario.pack(pady=5)

#         label_senha = tk.Label(self.login_frame, text="Senha:", font=("Arial", 14), fg=self.cor_fonte, bg=self.cor_principal)
#         label_senha.pack(pady=5)
#         self.entry_senha = tk.Entry(self.login_frame, font=("Arial", 14), show="*")
#         self.entry_senha.pack(pady=5)

#         botao_entrar = tk.Button(self.login_frame, text="Entrar", font=("Arial", 14), bg=self.cor_secundaria, fg=self.cor_fonte, command=self.verificar_login)
#         botao_entrar.pack(pady=20)

#         botao_cadastro = tk.Button(self.login_frame, text="Cadastrar", font=("Arial", 14), bg=self.cor_secundaria, fg=self.cor_fonte, command=self.cadastro_tela)
#         botao_cadastro.pack(pady=10)

#     def verificar_login(self):
#         usuario = self.entry_usuario.get().strip()
#         senha = self.entry_senha.get().strip()
#         usuarios = self.carregar_usuarios()

#         for u in usuarios:
#             if u["usuario"] == usuario:
#                 if u["senha"] == senha:
#                     self.usuario_logado = usuario
#                     self.login_frame.pack_forget()
#                     # Importa Janelas dinamicamente para evitar dependência circular
#                     from janelas import Janelas
#                     janelas = Janelas(self.root, self.usuario_logado) # Passa o root para a classe Janelas
#                     return
#                 else:
#                     messagebox.showerror("Erro", "Senha incorreta.")
#                     return
#         messagebox.showerror("Erro", "Usuário não encontrado.")

#     def cadastro_tela(self):
#         nova_janela = tk.Toplevel(self.root)
#         nova_janela.title("Cadastro de Conta")
#         nova_janela.geometry("400x300")

#         label_usuario = tk.Label(nova_janela, text="Usuário:", font=("Arial", 14))
#         label_usuario.pack(pady=5)
#         entry_usuario = tk.Entry(nova_janela, font=("Arial", 14))
#         entry_usuario.pack(pady=5)

#         label_email = tk.Label(nova_janela, text="Email:", font=("Arial", 14))
#         label_email.pack(pady=5)
#         entry_email = tk.Entry(nova_janela, font=("Arial", 14))
#         entry_email.pack(pady=5)

#         label_senha = tk.Label(nova_janela, text="Senha:", font=("Arial", 14))
#         label_senha.pack(pady=5)
#         entry_senha = tk.Entry(nova_janela, font=("Arial", 14), show="*")
#         entry_senha.pack(pady=5)

#         def salvar_usuario():
#             usuario = entry_usuario.get().strip()
#             email = entry_email.get().strip()
#             senha = entry_senha.get().strip()

#             if not usuario or not senha:
#                 messagebox.showerror("Erro", "Preencha todos os campos.")
#                 return

#             usuarios = self.carregar_usuarios()
#             if usuario in usuarios:
#                 messagebox.showerror("Erro", "Usuário já existe.")
#                 return

#             usuarios.append({"usuario": usuario, "email": email, "senha": senha})
#             self.salvar_usuarios(usuarios)

#             messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
#             nova_janela.destroy()

#         botao_salvar = tk.Button(nova_janela, text="Cadastrar", font=("Arial", 14), command=salvar_usuario)
#         botao_salvar.pack(pady=20)

#     def carregar_usuarios(self):
#         try:
#             with open("usuarios.json", "r", encoding="utf-8") as file:
#                 dados = json.load(file)
#                 return dados if isinstance(dados, list) else []
#         except (FileNotFoundError, json.JSONDecodeError):
#             return []

#     def salvar_usuarios(self, usuarios):
#         with open("usuarios.json", "w", encoding="utf-8") as file:
#             json.dump(usuarios, file, indent=4, ensure_ascii=False)
# ```

# ## janelas.py

# ```python
# import tkinter as tk
# from tkinter import ttk
# # from suporte import Suporte  # Importado dinamicamente
# # from conta_user import ContaUser # Importado dinamicamente
# from produtos import Produtos
# from clientes import Clientes


# class Janelas:
#     def __init__(self, root, usuario_logado):
#         self.root = root
#         self.usuario_logado = usuario_logado
#         self.cor_principal = "#1E3A5F"
#         self.cor_secundaria = "#2C5EAA"
#         self.cor_destaque = "#D9A87E"
#         self.cor_fonte = "white"
#         self.main_frame = tk.Frame(self.root, bg=self.cor_principal)
#         self.main_frame.pack(fill=tk.BOTH, expand=True)

#         self.sidebar = tk.Frame(self.main_frame, bg=self.cor_secundaria, width=200)
#         self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

#         self.content_frame = tk.Frame(self.main_frame, bg="white")
#         self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         self.paginas = {}

#         botoes = ["Financeiro", "Vendas", "Compras", "Clientes", "Produtos", "Relatórios", "Configurações", "Suporte", "Conta"]
#         for btn in botoes:
#             self.criar_botao_personalizado(self.sidebar, btn)

#         self.criar_paginas()
#         self.mudar_pagina("Produtos")

#     def criar_botao_personalizado(self, parent, texto):
#         botao = tk.Button(parent, text=texto, font=("Arial", 12), bg=self.cor_secundaria, fg=self.cor_fonte,
#                           relief="raised", command=lambda: self.mudar_pagina(texto))
#         botao.pack(fill=tk.X, padx=10, pady=5)

#     def mudar_pagina(self, nome_pagina):
#         for pagina in self.paginas.values():
#             pagina.pack_forget()
#         self.paginas[nome_pagina].pack(fill=tk.BOTH, expand=True)

#     def criar_paginas(self):
#         for nome in ["Financeiro", "Vendas", "Compras", "Relatórios", "Configurações"]:
#             frame = tk.Frame(self.content_frame, bg="white")
#             label = tk.Label(frame, text=nome, font=("Arial", 24), bg="white")
#             label.pack(pady=20)
#             self.paginas[nome] = frame

#         # Cria as páginas de Clientes e Produtos usando as classes separadas
#         self.paginas["Produtos"] = Produtos(self.content_frame).frame
#         self.paginas["Clientes"] = Clientes(self.content_frame).frame

#         # Criação das páginas Suporte e Conta (importadas dinamicamente)
#         def criar_pagina_suporte():
#             from suporte import Suporte
#             self.paginas["Suporte"] = Suporte(self.content_frame).frame # instancia e pega o frame
#         def criar_pagina_conta():
#             from conta_user import ContaUser
#             self.paginas["Conta"] = ContaUser(self.content_frame, self.usuario_logado).frame # instancia e pega o frame

#         # Adiciona os comandos de criação de página aos botões
#         for nome_botao, funcao_criar in [("Suporte", criar_pagina_suporte), ("Conta", criar_pagina_conta)]:
#             botao = self.sidebar.winfo_children()[["Financeiro", "Vendas", "Compras", "Clientes", "Produtos", "Relatórios", "Configurações", "Suporte", "Conta"].index(nome_botao)] # Pega o botão da sidebar
#             botao.config(command=lambda nome=nome_botao, func=funcao_criar: [func(), self.mudar_pagina(nome)]) # Atualiza o comando do botão

#         criar_pagina_suporte() # Cria a página de suporte inicialmente
#         criar_pagina_conta() # Cria a página conta inicialmente

# ```

# ## produtos.py

# ```python
# import tkinter as tk
# from tkinter import ttk

# from utils import carregar_dados, salvar_dados, abrir_janela_novo, remover_item


# class Produtos:
#     def __init__(self, parent):
#         self.parent = parent
#         self.frame = tk.Frame(self.parent, bg="white")

#         self.tree_produtos = ttk.Treeview(self.frame, columns=("#1", "#2", "#3", "#4", "#5"), show="headings")
#         self.tree_produtos.heading("#1", text="Cód")
#         self.tree_produtos.heading("#2", text="Produto")
#         self.tree_produtos.heading("#3", text="Categoria")
#         self.tree_produtos.heading("#4", text="Preço Venda")
#         self.tree_produtos.heading("#5", text="Estoque")

#         self.tree_produtos.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         self.produtos = []
#         carregar_dados("produtos.json", self.produtos, self.tree_produtos)

#         self.secao_botoes_produtos = tk.Frame(self.frame, bg="white")
#         self.secao_botoes_produtos.pack(pady=10)

#         tk.Button(self.secao_botoes_produtos, text="+ Novo", font=("Arial", 12), bg="#D9A87E", fg="white",
#                   command=lambda: abrir_janela_novo(self.parent, "produtos.json", self.produtos, self.tree_produtos,
#                                                    ["Nome do Produto", "Categoria", "Preço", "Estoque"])).grid(row=0,
#                                                                                                               column=0,
#                                                                                                               padx=10,
#                                                                                                               pady=10)
#         tk.Button(self.secao_botoes_produtos, text="Remover", font=("Arial", 12), bg="#D9A87E", fg="white",
#                   command=lambda: remover_item(self.parent, "produtos.json", self.produtos,
#                                                self.tree_produtos)).grid(row=0, column=1, padx=10, pady=10)
# ```

# ## clientes.py

# ```python
# import tkinter as tk
# from tkinter import ttk
# from utils import carregar_dados, salvar_dados, abrir_janela_novo, remover_item


# class Clientes:
#     def __init__(self, parent):
#         self.parent = parent
#         self.frame = tk.Frame(self.parent, bg="white")

#         self.tree_clientes = ttk.Treeview(self.frame, columns=("#1", "#2", "#3", "#4"), show="headings")
#         self.tree_clientes.heading("#1", text="Nome")
#         self.tree_clientes.heading("#2", text="CPF")
#         self.tree_clientes.heading("#3", text="Email")
#         self.tree_clientes.heading("#4", text="Telefone")

#         self.tree_clientes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         self.clientes = []
#         carregar_dados("clientes.json", self.clientes, self.tree_clientes)

#         self.secao_botoes_clientes = tk.Frame(self.frame, bg="white")
#         self.secao_botoes_clientes.pack(pady=10)

#         tk.Button(self.secao_botoes_clientes, text="+ Novo", font=("Arial", 12), bg="#2C5EAA", fg="white",
#                   command=lambda: abrir_janela_novo(self.parent, "clientes.json", self.clientes, self.tree_clientes,
#                                                    ["Nome", "CPF", "Email", "Telefone"])).grid(row=0, column=0, padx=10,
#                                                                                                pady=10)
#         tk.Button(self.secao_botoes_clientes, text="- Remover", font=("Arial", 12), bg="#2C5EAA", fg="white",
#                   command=lambda: remover_item(self.parent, "clientes.json", self.clientes,
#                                                self.tree_clientes)).grid(row=0, column=1, padx=10, pady=10)
# ```

# ## suporte.py

# ```python
# import tkinter as tk
# from tkinter import messagebox
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart


# class Suporte:
#     def __init__(self, parent):
#         self.parent = parent
#         self.frame = tk.Frame(self.parent, bg="white")
#         self.frame.pack(fill=tk.BOTH, expand=True)

#         botao_suporte = tk.Button(self.frame, text="Suporte", font=("Arial", 12), bg="#2C5EAA",
#                                   command=self.abrir_janela_suporte)
#         botao_suporte.pack(pady=20)

#     def abrir_janela_suporte(self):
#         janela_suporte = tk.Toplevel(self.parent)
#         janela_suporte.title("Suporte")
#         janela_suporte.geometry("400x300")

#         label_email_destino = tk.Label(janela_suporte, text="Para:", font=("Arial", 14))
#         label_email_destino.pack(pady=5)
#         entry_email_destino = tk.Entry(janela_suporte, font=("Arial", 12))
#         entry_email_destino.pack(pady=5)

#         label_assunto = tk.Label(janela_suporte, text="Assunto:", font=("Arial", 14))
#         label_assunto.pack(pady=5)
#         entry_assunto = tk.Entry(janela_suporte, font=("Arial", 12))
#         entry_assunto.pack(pady=5)

#         label_mensagem = tk.Label(janela_suporte, text="Mensagem:", font=("Arial", 14))
#         label_mensagem.pack(pady=5)
#         text_mensagem = tk.Text(janela_suporte, font=("Arial", 12), height=5, width=30)
#         text_mensagem.pack(pady=5)

#         def enviar_email():
#             email_destino = entry_email_destino.get().strip()
#             assunto = entry_assunto.get().strip()
#             mensagem = text_mensagem.get("1.0", tk.END).strip()

#             if not email_destino or not assunto or not mensagem:
#                 messagebox.showerror("Erro", "Preencha todos os campos.")
#                 return

#             # Configurações do servidor de email (Gmail no exemplo)
#             remetente = "seu_email@gmail.com"  # Insira seu email
#             senha_email = "sua_senha"  # Insira sua senha (ou use uma senha de aplicativo)
#             servidor_smtp = "smtp.gmail.com"
#             porta_smtp = 587

#             # Monta a mensagem
#             msg = MIMEMultipart()
#             msg["From"] = remetente
#             msg["To"] = email_destino
#             msg["Subject"] = assunto
#             msg.attach(MIMEText(mensagem, "plain"))

#             try:
#                 # Inicia a conexão com o servidor
#                 server = smtplib.SMTP(servidor_smtp, porta_smtp)
#                 server.starttls()  # Criptografa a conexão
#                 server.login(remetente, senha_email)  # Faz o login
#                 server.sendmail(remetente, email_destino, msg.as_string())  # Envia o email
#                 server.quit()  # Encerra a conexão

#                 messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
#                 janela_suporte.destroy()
#             except Exception as e:
#                 messagebox.showerror("Erro", f"Erro ao enviar email: {e}")

#         botao_enviar = tk.Button(janela_suporte, text="Enviar", font=("Arial", 12), command=enviar_email)
#         botao_enviar.pack(pady=10)
# ```

# ## conta_user.py

# ```python
# import tkinter as tk
# from tkinter import messagebox
# import json


# class ContaUser:
#     def __init__(self, parent, usuario_logado):
#         self.parent = parent
#         self.frame = tk.Frame(self.parent, bg="white")
#         self.frame.pack(fill=tk.BOTH, expand=True)
#         self.usuario_logado = usuario_logado # Recebe o usuario logado

#         self.criar_pagina_conta()

#     def criar_pagina_conta(self):
#         # frame = self.paginas["Conta"]

#         # Certifique-se de que um usuário está logado
#         if not self.usuario_logado:
#             messagebox.showerror("Erro", "Nenhum usuário logado.")
#             return

#         label_user = tk.Label(self.frame, text=f"Bem vindo(a) {self.usuario_logado}", font=("Arial", 24), bg="white")
#         label_user.pack(pady=20)

#         # carrega os dados do usuario
#         dados_usuario = self.carregar_dados("usuarios.json")
#         # Procura os dados do usuário logado
#         usuario_logado = next((u for u in dados_usuario if u["usuario"] == self.usuario_logado), None)

#         if usuario_logado:
#             label_nome = tk.Label(self.frame, text=f"Nome: {usuario_logado['usuario']}", font=("Arial", 14), bg="white")
#             label_nome.pack(pady=10)
#             label_email = tk.Label(self.frame, text=f"Email: {usuario_logado['email']}", font=("Arial", 14), bg="white")
#             label_email.pack(pady=10)
#         else:
#             label_nome = tk.Label(self.frame, text="Usuário não encontrado", font=("Arial", 14), bg="white")
#             label_nome.pack(pady=10)

#         tk.Button(self.frame, text="Editar Conta", font=("Arial", 12), bg="#2C5EAA", fg="white",
#                   command=self.abrir_janela_editar_conta).pack(pady=20)

#     def abrir_janela_editar_conta(self):
#         nova_janela = tk.Toplevel(self.parent)
#         nova_janela.title("Editar Conta")
#         nova_janela.geometry("400x300")

#         # carrega os dados do usuario
#         dados_usuario = self.carregar_dados("usuarios.json")
#         # Procura os dados do usuário logado
#         usuario_logado = next((u for u in dados_usuario if u["usuario"] == self.usuario_logado), None)

#         label_nome = tk.Label(nova_janela, text="Nome:", font=("Arial", 14))
#         label_nome.pack(pady=5)
#         entry_nome = tk.Entry(nova_janela, font=("Arial", 12))
#         entry_nome.insert(0, usuario_logado["usuario"])
#         entry_nome.pack(pady=5)

#         label_email = tk.Label(nova_janela, text="Email:", font=("Arial", 14))
#         label_email.pack(pady=5)
#         entry_email = tk.Entry(nova_janela, font=("Arial", 12))
#         entry_email.insert(0, usuario_logado["email"])
#         entry_email.pack(pady=5)

#         label_senha = tk.Label(nova_janela, text="Senha:", font=("Arial", 14))
#         label_senha.pack(pady=5)
#         entry_senha = tk.Entry(nova_janela, font=("Arial", 12), show="*")
#         entry_senha.insert(0, usuario_logado["senha"])
#         entry_senha.pack(pady=5)

#         def salvar_edicoes():
#             novo_nome = entry_nome.get().strip()
#             novo_email = entry_email.get().strip()
#             nova_senha = entry_senha.get().strip()

#             if not novo_nome or not novo_email or not nova_senha:
#                 messagebox.showerror("Erro", "Preencha todos os campos.")
#                 return

#             # Atualiza os dados do usuário na lista
#             for u in dados_usuario:
#                 if u["usuario"] == self.usuario_logado:
#                     u["usuario"] = novo_nome
#                     u["email"] = novo_email
#                     u["senha"] = nova_senha # Por questões de segurança a senha deve ser criptografada
#                     break

#             # Salva a lista atualizada no arquivo
#             self.salvar_dados("usuarios.json", dados_usuario)
#             messagebox.showinfo("Sucesso", "Dados da conta atualizados com sucesso!")
#             nova_janela.destroy()
#             self.criar_pagina_conta()  # Atualiza a página de conta

#         botao_salvar = tk.Button(nova_janela, text="Salvar", font=("Arial", 12), command=salvar_edicoes)
#         botao_salvar.pack(pady=10)

#     def carregar_dados(self, arquivo):
#         try:
#             with open(arquivo, "r", encoding="utf-8") as file:
#                 dados = json.load(file)
#                 return dados if isinstance(dados, list) else []
#         except (FileNotFoundError, json.JSONDecodeError):
#             return []

#     def salvar_dados(self, arquivo, dados):
#         with open(arquivo, "w", encoding="utf-8") as file:
#             json.dump(dados, file, indent=4, ensure_ascii=False)
# ```

# ## utils.py

# ```python
# import tkinter as tk
# from tkinter import messagebox
# import json

# def carregar_dados(arquivo, lista, tree):
#     """Carrega dados de um arquivo JSON e exibe em uma Treeview."""
#     try:
#         with open(arquivo, "r", encoding="utf-8") as file:
#             dados = js