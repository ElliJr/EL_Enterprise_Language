import tkinter as tk
import webbrowser

class Suporte:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Suporte")
        self.frame.destroy()  # Remove o frame anterior, se existir
        self.frame = tk.Frame(self.parent, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(
            self.frame,
            text="Fale conosco por aqui",
            font=("Arial", 16, "bold"),
            fg="#0e7490",
            bg="white"
        )
        label.pack(pady=(20))

        botao_suporte = tk.Button(
            self.frame,
            text="Abrir Suporte",
            font=("Arial", 12, "bold"),
            bg="#0e7490",
            fg="white",
            activebackground="#38bdf8",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.abrir_pagina_suporte
        )
        botao_suporte.pack(pady=8)

    def abrir_pagina_suporte(self):
        url = "https://forms.gle/EXEMPLO"  # Coloque aqui o link da sua página de suporte
        webbrowser.open_new_tab(url)