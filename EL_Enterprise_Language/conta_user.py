import tkinter as tk
from tkinter import messagebox
import json
import requests  # Importe a biblioteca requests

class ContaUser:
    def __init__(self, parent, usuario_logado):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="#181818")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.usuario_logado = usuario_logado # Recebe o usuario logado

        self.criar_pagina_conta()

    def criar_pagina_conta(self):
        # Certifique-se de que um usuário está logado
        if not self.usuario_logado:
            messagebox.showerror("Erro", "Nenhum usuário logado.")
            return

        # Limpa o frame antes de adicionar novos widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Carrega os dados do usuário
        usuario_logado = self.carregar_dados(self.usuario_logado)

        # Se vier uma lista, pega o primeiro elemento
        if isinstance(usuario_logado, list) and usuario_logado:
            usuario_logado = usuario_logado[0]

        if usuario_logado and isinstance(usuario_logado, dict):
            # Frame de perfil centralizado
            perfil_frame = tk.Frame(self.frame, bg="#181818", bd=2, relief="groove")
            perfil_frame.place(relx=0.5, rely=0.3, anchor="center", relwidth=0.5)


            # Nome do usuário
            label_nome = tk.Label(
                perfil_frame,
                text=usuario_logado.get('usuario', 'Desconhecido'),
                font=("Arial", 22, "bold"),
                bg="#181818",
                fg="#D9A87E"
            )
            label_nome.pack(pady=(0, 8))

            # Linha divisória
            divider = tk.Frame(perfil_frame, bg="#D9A87E", height=2)
            divider.pack(fill="x", padx=40, pady=(0, 12))

            # Email do usuário
            label_email = tk.Label(
                perfil_frame,
                text=f"Email: {usuario_logado.get('email', 'Não informado')}",
                font=("Arial", 14),
                bg="#181818",
                fg="#FFFFFF"
            )
            label_email.pack(pady=(0, 20))

            # Exemplo: mostrar mais dados se existirem
            if 'nome' in usuario_logado:
                label_nome_completo = tk.Label(
                    perfil_frame,
                    text=f"Nome completo: {usuario_logado.get('nome', '')}",
                    font=("Arial", 12),
                    bg="#181818",
                    fg="#FFFFFF"
                )
                label_nome_completo.pack(pady=(0, 10))

        else:
            label_nome = tk.Label(
                self.frame,
                text="Usuário não encontrado",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="red"
            )
            label_nome.pack(pady=30)


    def carregar_dados(self, usuario):
        try:
            response = requests.post(
                "https://ellidev21.pythonanywhere.com/conta", 
                data={"usuario": usuario}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return []

    def salvar_dados(self, arquivo, dados):
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)