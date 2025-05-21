import tkinter as tk
from login import LoginTela
from janelas import Janelas  # Importe sua tela principal

def abrir_janelas(usuario_logado):
    # Fecha a tela de login e abre a tela principal
    for widget in root.winfo_children():
        widget.destroy()
    Janelas(root, usuario_logado)  # Mostra a tela principal, que já abre na página "Inicio"

if __name__ == "__main__":
    root = tk.Tk()
    # Passe a função abrir_janelas para o LoginTela
    login_tela = LoginTela(root, on_login=abrir_janelas)
    root.mainloop()