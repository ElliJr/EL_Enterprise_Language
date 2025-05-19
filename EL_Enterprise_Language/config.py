# config.py
import json
import os
import tkinter as tk

tema_atual = "Claro"
CONFIG_FILE = "config.json"

def get_tema():
    global tema_atual
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                tema_atual = data.get("tema", "Claro")
        except (FileNotFoundError, json.JSONDecodeError):
            pass # Mantém o tema padrão se houver erro ao carregar
    return tema_atual

def set_tema(novo_tema):
    global tema_atual
    tema_atual = novo_tema
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"tema": tema_atual}, f)
    except Exception as e:
        print(f"Erro ao salvar a configuração do tema: {e}")

# Exemplo de layout para tela de configurações
class ConfiguracoesTela:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        titulo = tk.Label(self.frame, text="Configurações", font=("Arial", 28))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        btn_claro = tk.Button(self.frame, text="Tema Claro")
        btn_claro.grid(row=1, column=0, pady=5, sticky="ew")

        btn_escuro = tk.Button(self.frame, text="Tema Escuro")
        btn_escuro.grid(row=2, column=0, pady=5, sticky="ew")

        btn_padrao = tk.Button(self.frame, text="Tema Padrão")
        btn_padrao.grid(row=3, column=0, pady=5, sticky="ew")

        # Expande os botões para ocupar toda a largura do frame
        self.frame.grid_columnconfigure(0, weight=1)

# Para testar isoladamente:
if __name__ == "__main__":
    root = tk.Tk()
    ConfiguracoesTela(root)
    root.minsize(400, 300)
    root.mainloop()