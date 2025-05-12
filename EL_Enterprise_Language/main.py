import tkinter as tk
from login import LoginTela
import config
from utils import aplicar_tema  
# from janelas import Janelas  # Removido para evitar dependência circular

if __name__ == "__main__":
    root = tk.Tk()
    config.get_tema() # Carrega o tema salvo (se existir)
    aplicar_tema(root) # Aplica o tema inicial
    login_tela = LoginTela(root)
    root.mainloop()