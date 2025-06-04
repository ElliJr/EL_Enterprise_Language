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
    # A LoginTela define o título e a geometria da janela, então não é estritamente necessário aqui,
    # mas é bom ter um título padrão.
    root.title("Aplicação de Gestão Financeira") 
    # A LoginTela define a geometria para 1300x800, então esta linha pode ser redundante
    # ou servir como um fallback inicial antes da LoginTela assumir o controle.
    root.geometry("550x500") 

    # Cria uma instância da tela de login, passando a função de callback
    # O parâmetro 'on_login' da LoginTela é usado para a função que será chamada após um login bem-sucedido.
    login_tela = LoginTela(root, on_login=abrir_janelas) 
    
    root.mainloop()
