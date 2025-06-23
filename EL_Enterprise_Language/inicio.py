import tkinter as tk

class Inicio:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#1E3A5F")  # Cor principal do sistema

        # Banner superior (simula uma imagem de fundo com cor)
        self.banner = tk.Frame(self.frame, bg="#2C5EAA", height=200)
        self.banner.pack(fill=tk.X, side=tk.TOP)

        # Texto principal (com animação de fade-in)
        self.titulo = tk.Label(
            self.banner,
            text="Bem-vindo à Enterprise Language",
            font=("Arial", 28, "bold"),
            bg="#2C5EAA",
            fg="#ffffff"
        )
        self.titulo.place(relx=0.05, rely=0.2, anchor="w")

        self.subtitulo = tk.Label(
            self.banner,
            text="Com mais de 500 projetos desenvolvidos nos últimos 7 anos,\n"
                 "a Enterprise Language oferece soluções digitais sob medida.",
            font=("Arial", 14),
            bg="#2C5EAA",
            fg="#e0e0e0"
        )
        self.subtitulo.place(relx=0.05, rely=0.55, anchor="w")
        
        # Botão de ação
        self.botao = tk.Button(
            self.banner,
            text="Conheça nosso site",
            font=("Arial", 12, "bold"),
            bg="#22c55e",
            fg="white",
            relief="flat",
            activebackground="#16a34a",
            activeforeground="white",
            command=self.acao_planos
        )
        self.botao.place(relx=0.05, rely=0.8, anchor="w")

        # Seção inferior
        self.secao = tk.Frame(self.frame, bg="white")
        self.secao.pack(fill=tk.BOTH, expand=True)

        self.texto_secao = tk.Label(
            self.secao,
            text="A Enterprise Language é uma empresa de tecnologia\n"
                 "especializada em desenvolvimento de software e\n",
            font=("Arial", 22),
            bg="white",
            fg="#1E3A5F"
        )
        self.texto_secao.pack(pady=40)

        # Animação simples: fade-in do título
        self.titulo.after(100, self.fade_in, 0)

    def acao_planos(self):
        # Aqui você pode abrir uma página interna ou mostrar uma mensagem
        print("Botão 'CONHEÇA NOSSOS PLANOS' clicado!")
        # Exemplo: abrir uma nova janela ou página

    def fade_in(self, step):
        # Animação simples de fade-in no texto do título
        if step <= 20:
            cor = f'#{step*12:02x}{step*12:02x}{step*12:02x}'
            self.titulo.config(fg=cor)
            self.titulo.after(30, self.fade_in, step+1)
        else:
            self.titulo.config(fg="#ffffff")

# Para testar isoladamente:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Início - Enterprise Language")
    Inicio(root).frame.pack(fill=tk.BOTH, expand=True)
    root.geometry("900x500")
    root.mainloop()