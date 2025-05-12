import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Suporte:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)

        botao_suporte = tk.Button(self.frame, text="Suporte", font=("Arial", 12), bg="#2C5EAA",
                                  command=self.abrir_janela_suporte)
        botao_suporte.pack(pady=20)

    def abrir_janela_suporte(self):
        janela_suporte = tk.Toplevel(self.parent)
        janela_suporte.title("Suporte")
        janela_suporte.geometry("400x300")

        label_email_destino = tk.Label(janela_suporte, text="Para:", font=("Arial", 14))
        label_email_destino.pack(pady=5)
        entry_email_destino = tk.Entry(janela_suporte, font=("Arial", 12))
        entry_email_destino.pack(pady=5)

        label_assunto = tk.Label(janela_suporte, text="Assunto:", font=("Arial", 14))
        label_assunto.pack(pady=5)
        entry_assunto = tk.Entry(janela_suporte, font=("Arial", 12))
        entry_assunto.pack(pady=5)

        label_mensagem = tk.Label(janela_suporte, text="Mensagem:", font=("Arial", 14))
        label_mensagem.pack(pady=5)
        text_mensagem = tk.Text(janela_suporte, font=("Arial", 12), height=5, width=30)
        text_mensagem.pack(pady=5)

        def enviar_email():
            email_destino = entry_email_destino.get().strip()
            assunto = entry_assunto.get().strip()
            mensagem = text_mensagem.get("1.0", tk.END).strip()

            if not email_destino or not assunto or not mensagem:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            # Configurações do servidor de email (Gmail no exemplo)
            remetente = "seu_email@gmail.com"  # Insira seu email
            senha_email = "sua_senha"  # Insira sua senha (ou use uma senha de aplicativo)
            servidor_smtp = "smtp.gmail.com"
            porta_smtp = 587

            # Monta a mensagem
            msg = MIMEMultipart()
            msg["From"] = remetente
            msg["To"] = email_destino
            msg["Subject"] = assunto
            msg.attach(MIMEText(mensagem, "plain"))

            try:
                # Inicia a conexão com o servidor
                server = smtplib.SMTP(servidor_smtp, porta_smtp)
                server.starttls()  # Criptografa a conexão
                server.login(remetente, senha_email)  # Faz o login
                server.sendmail(remetente, email_destino, msg.as_string())  # Envia o email
                server.quit()  # Encerra a conexão

                messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
                janela_suporte.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao enviar email: {e}")

        botao_enviar = tk.Button(janela_suporte, text="Enviar", font=("Arial", 12), command=enviar_email)
        botao_enviar.pack(pady=10)