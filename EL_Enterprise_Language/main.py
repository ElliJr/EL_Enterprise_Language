import tkinter as tk
from login import LoginTela # Importa a classe LoginTela
from janelas import Janelas     # Importa a classe Janelas (sua tela principal)

def abrir_janelas(usuario_logado):
    """
    Função chamada após um login bem-sucedido.
    Fecha a tela de login e abre a tela principal de gestão financeira.
    """
    for widget in root.winfo_children():
        widget.destroy()
    # Passe o nome do usuário logado para a tela principal
    Janelas(root, usuario_logado) 

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplicação de Gestão Financeira") 
    root.geometry("550x500") 

    # Define a cor de fundo da janela principal
    root.configure(bg="#181818")

    # Cria uma instância da tela de login, passando a função de callback
    login_tela = LoginTela(root, on_login=abrir_janelas) 
    
    root.mainloop()
