import tkinter as tk
from tkinter import messagebox
import json


class ContaUser:
    def __init__(self, parent, usuario_logado):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.usuario_logado = usuario_logado # Recebe o usuario logado

        self.criar_pagina_conta()

    def criar_pagina_conta(self):
        # frame = self.paginas["Conta"]

        # Certifique-se de que um usuário está logado
        if not self.usuario_logado:
            messagebox.showerror("Erro", "Nenhum usuário logado.")
            return

        label_user = tk.Label(self.frame, text=f"Bem vindo(a) {self.usuario_logado}", font=("Arial", 24), bg="white")
        label_user.pack(pady=20)

        # carrega os dados do usuario
        dados_usuario = self.carregar_dados("usuarios.json")
        # Procura os dados do usuário logado
        usuario_logado = next((u for u in dados_usuario if u["usuario"] == self.usuario_logado), None)

        if usuario_logado:
            label_nome = tk.Label(self.frame, text=f"Nome: {usuario_logado['usuario']}", font=("Arial", 14), bg="white")
            label_nome.pack(pady=10)
            label_email = tk.Label(self.frame, text=f"Email: {usuario_logado['email']}", font=("Arial", 14), bg="white")
            label_email.pack(pady=10)
        else:
            label_nome = tk.Label(self.frame, text="Usuário não encontrado", font=("Arial", 14), bg="white")
            label_nome.pack(pady=10)

        tk.Button(self.frame, text="Editar Conta", font=("Arial", 12), bg="#2C5EAA", fg="white",
                  command=self.abrir_janela_editar_conta).pack(pady=20)

    def abrir_janela_editar_conta(self):
        nova_janela = tk.Toplevel(self.parent)
        nova_janela.title("Editar Conta")
        nova_janela.geometry("400x300")

        # carrega os dados do usuario
        dados_usuario = self.carregar_dados("usuarios.json")
        # Procura os dados do usuário logado
        usuario_logado = next((u for u in dados_usuario if u["usuario"] == self.usuario_logado), None)

        label_nome = tk.Label(nova_janela, text="Nome:", font=("Arial", 14))
        label_nome.pack(pady=5)
        entry_nome = tk.Entry(nova_janela, font=("Arial", 12))
        entry_nome.insert(0, usuario_logado["usuario"])
        entry_nome.pack(pady=5)

        label_email = tk.Label(nova_janela, text="Email:", font=("Arial", 14))
        label_email.pack(pady=5)
        entry_email = tk.Entry(nova_janela, font=("Arial", 12))
        entry_email.insert(0, usuario_logado["email"])
        entry_email.pack(pady=5)

        label_senha = tk.Label(nova_janela, text="Senha:", font=("Arial", 14))
        label_senha.pack(pady=5)
        entry_senha = tk.Entry(nova_janela, font=("Arial", 12), show="*")
        entry_senha.insert(0, usuario_logado["senha"])
        entry_senha.pack(pady=5)

        def salvar_edicoes():
            novo_nome = entry_nome.get().strip()
            novo_email = entry_email.get().strip()
            nova_senha = entry_senha.get().strip()

            if not novo_nome or not novo_email or not nova_senha:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            # Atualiza os dados do usuário na lista
            for u in dados_usuario:
                if u["usuario"] == self.usuario_logado:
                    u["usuario"] = novo_nome
                    u["email"] = novo_email
                    u["senha"] = nova_senha # Por questões de segurança a senha deve ser criptografada
                    break

            # Salva a lista atualizada no arquivo
            self.salvar_dados("usuarios.json", dados_usuario)
            messagebox.showinfo("Sucesso", "Dados da conta atualizados com sucesso!")
            nova_janela.destroy()
            self.criar_pagina_conta()  # Atualiza a página de conta

        botao_salvar = tk.Button(nova_janela, text="Salvar", font=("Arial", 12), command=salvar_edicoes)
        botao_salvar.pack(pady=10)

    def carregar_dados(self, arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as file:
                dados = json.load(file)
                return dados if isinstance(dados, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar_dados(self, arquivo, dados):
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)