import tkinter as tk
from tkinter import messagebox
import requests  # Importe a biblioteca requests

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

        label_titulo = tk.Label(self.login_frame, text="EL Enterprise Language⚙️", font=("Arial", 24), fg=self.cor_fonte,
                                 bg=self.cor_principal)
        label_titulo.pack(pady=20)

        # Frame interno para os campos de entrada e botões
        login_content_frame = tk.Frame(self.login_frame, bg=self.cor_principal)
        login_content_frame.pack(expand=True)  # Centraliza o frame no espaço restante

        label_usuario = tk.Label(login_content_frame, text="Usuário:", font=("Arial", 14), fg=self.cor_fonte,
                                  bg=self.cor_principal)
        label_usuario.pack(pady=5)
        self.entry_usuario = tk.Entry(login_content_frame, font=("Arial", 14))
        self.entry_usuario.pack(pady=5)

        label_senha = tk.Label(login_content_frame, text="Senha:", font=("Arial", 14), fg=self.cor_fonte,
                                bg=self.cor_principal)
        label_senha.pack(pady=5)
        self.entry_senha = tk.Entry(login_content_frame, font=("Arial", 14), show="*")
        self.entry_senha.pack(pady=5)

        botao_entrar = tk.Button(login_content_frame, text="Entrar", font=("Arial", 14), bg=self.cor_secundaria,
                                  fg=self.cor_fonte, command=self.verificar_login)
        botao_entrar.pack(pady=20)

        botao_cadastro = tk.Button(login_content_frame, text="Cadastrar", font=("Arial", 14), bg=self.cor_secundaria,
                                   fg=self.cor_fonte, command=self.cadastro_tela)
        botao_cadastro.pack(pady=10)

    def verificar_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        dados = {
            "usuario": usuario,
            "senha": senha,
        }

        try:
            # Envia os dados para o servidor na rota /login
            print(f"Tentando logar com usuário: {usuario}, senha: {senha}")
            response = requests.post("http://127.0.0.1:3000/login", data=dados)
            print(f"Resposta do servidor: {response.status_code}, {response.text}")

            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.login_frame.pack_forget()
                # Importa Janelas dinamicamente para evitar dependência circular
                from janelas import Janelas
                janelas = Janelas(self.root, usuario)  # Passa o root para a classe Janelas
                # self.root.destroy() # Removi esta linha para evitar erro
            else:
                messagebox.showerror("Erro", f"Erro ao fazer login: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro de conexão: {e}")

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

        botao_salvar = tk.Button(nova_janela, text="Cadastrar", font=("Arial", 14), command=lambda: self.salvar_usuario(nova_janela, entry_usuario, entry_email, entry_senha))
        botao_salvar.pack(pady=20)

    def salvar_usuario(self, nova_janela, entry_usuario, entry_email, entry_senha): # Passando nova_janela
        usuario = entry_usuario.get().strip()
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()

        if not usuario or not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        # Dados a serem enviados no corpo da requisição POST
        dados = {
            "usuario": usuario,
            "email": email,
            "senha": senha,
        }

        try:
            # Envia os dados para o servidor na rota /cadastro
            response = requests.post("http://127.0.0.1:3000/cadastro", data=dados)

            # Verifica se a requisição foi bem-sucedida (código 200)
            if response.status_code == 200:
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
                nova_janela.destroy()
            else:
                messagebox.showerror("Erro", f"Erro ao cadastrar: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro de conexão: {e}")
