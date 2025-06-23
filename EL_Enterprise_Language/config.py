import tkinter as tk
import webbrowser

class PainelControle:
    def __init__(self, master, abrir_func=None):
        self.abrir_func = abrir_func  # Função para abrir páginas do sistema, se necessário
        self.frame = tk.Frame(master, bg="#1E3A5F")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(self.frame, text="Painel de Controle", font=("Arial", 28), bg="#1E3A5F", fg="white").grid(row=0, column=0, columnspan=6, pady=(0, 20))
        tk.Label(self.frame, text="Categorias", font=("Arial", 14, "bold"), bg="#1E3A5F", fg="white").grid(row=1, column=1, sticky="w", padx=10)
        tk.Label(self.frame, text="Configuração dentro da Categoria", font=("Arial", 14, "bold"), bg="#1E3A5F", fg="white").grid(row=1, column=4, sticky="w", padx=10)

        categorias = [
            # (Num, Categoria, Emoji, Configuração, Emoji, função_categoria, função_config)
            ("I.", "Contas de Usuário", "👤", "Ferramentas Administrativas", "🛠️", self.abrir_contas_usuario, self.abrir_ferramentas_admin),
            ("II.", "Programas", "📦", "Grupos", "🌐", self.abrir_programas, self.abrir_grupo_domestico),
            ("III.", "Rede e Internet", "🌐", "Suporte", "🖥️", self.abrir_rede_internet, self.abrir_gadgets),
            ("IV.", "Sistema e Segurança", "🔒", "Gerenciador de Credenciais", "🔑", self.abrir_sistema_seguranca, self.abrir_gerenciador_credenciais),
        ]

        for i, (num, cat, icat, conf, iconf, func_cat, func_conf) in enumerate(categorias, start=2):
            tk.Label(self.frame, text=num, font=("Arial", 12, "bold"), bg="#1E3A5F", fg="white").grid(row=i, column=0, sticky="e", padx=(10,0))
            tk.Label(self.frame, text=icat, font=("Arial", 18), bg="#1E3A5F", fg="white").grid(row=i, column=1, sticky="e", padx=(0,0))
            tk.Button(self.frame, text=cat, font=("Arial", 12), bg="#2C5EAA", fg="white", relief="flat", 
                      command=func_cat).grid(row=i, column=2, sticky="w", padx=(0,10), pady=5)
            tk.Label(self.frame, text="( )", font=("Arial", 14), bg="#1E3A5F", fg="white").grid(row=i, column=3, sticky="e")
            tk.Label(self.frame, text=iconf, font=("Arial", 18), bg="#1E3A5F", fg="white").grid(row=i, column=4, sticky="e", padx=(10,0))
            tk.Button(self.frame, text=conf, font=("Arial", 12), bg="#D9A87E", fg="black", relief="flat", 
                      command=func_conf).grid(row=i, column=5, sticky="w", padx=(0,10), pady=5)

        for col in range(6):
            self.frame.grid_columnconfigure(col, weight=0)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(5, weight=1)

    # Agora, cada função chama uma funcionalidade do seu sistema:
    def abrir_contas_usuario(self):
        # Exemplo: abrir tela de contas de usuário do sistema
        if self.abrir_func:
            self.abrir_func("Conta")
        else:
            print("Abrir tela de contas de usuário do sistema Enterprise Language")

    def abrir_ferramentas_admin(self):
        # Exemplo: abrir tela de ferramentas administrativas do sistema
        if self.abrir_func:
            self.abrir_func("Ferramentas")
        else:
            print("Abrir ferramentas administrativas do sistema Enterprise Language")

    def abrir_programas(self):
        # Exemplo: abrir tela de programas do sistema
        if self.abrir_func:
            self.abrir_func("Programas")
        else:
            print("Abrir tela de programas do sistema Enterprise Language")

    def abrir_grupo_domestico(self):
        # Exemplo: abrir tela de grupo doméstico do sistema
        if self.abrir_func:
            self.abrir_func("GrupoDomestico")
        else:
            print("Abrir grupo doméstico do sistema Enterprise Language")

    def abrir_rede_internet(self):
        webbrowser.open_new_tab("file:///C:/Users/ellij/OneDrive/Documentos/EL_Enterprise_Language/EL_Enterprise_Language/financeiro.html")

    def abrir_gadgets(self):
        webbrowser.open_new_tab("https://www.google.com/search?q=gadgets+windows")

    def abrir_sistema_seguranca(self):
        # Exemplo: abrir tela de sistema e segurança do sistema
        if self.abrir_func:
            self.abrir_func("SistemaSeguranca")
        else:
            print("Abrir sistema e segurança do sistema Enterprise Language")

    def abrir_gerenciador_credenciais(self):
        # Exemplo: abrir tela de gerenciador de credenciais do sistema
        if self.abrir_func:
            self.abrir_func("Credenciais")
        else:
            print("Abrir gerenciador de credenciais do sistema Enterprise Language")

# No seu janelas.py

# Exemplo de uso isolado:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Painel de Controle")
    root.configure(bg="#1E3A5F")
    PainelControle(root)
    root.minsize(800, 400)
    root.mainloop()