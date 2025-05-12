import tkinter as tk
from tkinter import messagebox
import json
import os
# from janelas import Janelas # Importado dinamicamente dentro da classe
from conta_user import ContaUser  # Importa a classe ContaUser

class LoginTela:
    def __init__(self, root):
        self.root = root
        self.root.title("EL Enterprise Language⚙️")
        self.root.geometry("1300x800")
        self.cor_principal = "#1E3A5F"
        self.cor_secundaria = "#2C5EAA"
        self.cor_destaque = "#D9A87E"
        self.cor_fonte = "white"
        self.login_tela()

    def login_tela(self):
        self.login_frame = tk.Frame(self.root, bg=self.cor_principal)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        label_titulo = tk.Label(self.login_frame, text="Sistema de Gerenciamento", font=("Arial", 24), fg=self.cor_fonte, bg=self.cor_principal)
        label_titulo.pack(pady=20)

        label_usuario = tk.Label(self.login_frame, text="Usuário:", font=("Arial", 14), fg=self.cor_fonte, bg=self.cor_principal)
        label_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(self.login_frame, font=("Arial", 14))
        self.entry_usuario.pack(pady=5)

        label_senha = tk.Label(self.login_frame, text="Senha:", font=("Arial", 14), fg=self.cor_fonte, bg=self.cor_principal)
        label_senha.pack(pady=5)
        self.entry_senha = tk.Entry(self.login_frame, font=("Arial", 14), show="*")
        self.entry_senha.pack(pady=5)

        botao_entrar = tk.Button(self.login_frame, text="Entrar", font=("Arial", 14), bg=self.cor_secundaria, fg=self.cor_fonte, command=self.verificar_login)
        botao_entrar.pack(pady=20)

        botao_cadastro = tk.Button(self.login_frame, text="Cadastrar", font=("Arial", 14), bg=self.cor_secundaria, fg=self.cor_fonte, command=self.cadastro_tela)
        botao_cadastro.pack(pady=10)

    def verificar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        usuarios = self.carregar_usuarios()

        for u in usuarios:
            if u["usuario"] == usuario:
                if u["senha"] == senha:
                    self.usuario_logado = usuario
                    self.login_frame.pack_forget()
                    # Importa Janelas dinamicamente para evitar dependência circular
                    from janelas import Janelas
                    janelas = Janelas(self.root, self.usuario_logado) # Passa o root para a classe Janelas
                    return
                else:
                    messagebox.showerror("Erro", "Senha incorreta.")
                    return
        messagebox.showerror("Erro", "Usuário não encontrado.")

    def cadastro_tela(self):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Cadastro de Conta")
        nova_janela.geometry("400x300")

        label_usuario = tk.Label(nova_janela, text="Usuário:", font=("Arial", 14))
        label_usuario.pack(pady=5)
        entry_usuario = tk.Entry(nova_janela, font=("Arial", 14))
        entry_usuario.pack(pady=5)

        label_email = tk.Label(nova_janela, text="Email:", font=("Arial", 14))
        label_email.pack(pady=5)
        entry_email = tk.Entry(nova_janela, font=("Arial", 14))
        entry_email.pack(pady=5)

        label_senha = tk.Label(nova_janela, text="Senha:", font=("Arial", 14))
        label_senha.pack(pady=5)
        entry_senha = tk.Entry(nova_janela, font=("Arial", 14), show="*")
        entry_senha.pack(pady=5)

        def salvar_usuario():
            usuario = entry_usuario.get().strip()
            email = entry_email.get().strip()
            senha = entry_senha.get().strip()

            if not usuario or not senha:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            usuarios = self.carregar_usuarios()
            if usuario in usuarios:
                messagebox.showerror("Erro", "Usuário já existe.")
                return

            usuarios.append({"usuario": usuario, "email": email, "senha": senha})
            self.salvar_usuarios(usuarios)

            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            nova_janela.destroy()

        botao_salvar = tk.Button(nova_janela, text="Cadastrar", font=("Arial", 14), command=salvar_usuario)
        botao_salvar.pack(pady=20)

    def carregar_usuarios(self):
        try:
            with open("usuarios.json", "r", encoding="utf-8") as file:
                dados = json.load(file)
                return dados if isinstance(dados, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar_usuarios(self, usuarios):
        with open("usuarios.json", "w", encoding="utf-8") as file:
            json.dump(usuarios, file, indent=4, ensure_ascii=False)