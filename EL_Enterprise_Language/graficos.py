# Exemplo de estrutura para navegação entre seções
import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.frames = {}

        # Menu lateral
        menu = tk.Frame(root, bg="#3969ad")
        menu.pack(side=tk.LEFT, fill=tk.Y)

        for nome in ["Financeiro", "Vendas", "Produtos"]:
            btn = tk.Button(menu, text=nome, width=15, command=lambda n=nome: self.mostrar_frame(n))
            btn.pack(pady=5)

        # Frames das seções
        self.frames["Financeiro"] = tk.Frame(root, bg="white")
        tk.Label(self.frames["Financeiro"], text="Financeiro", font=("Arial", 24)).pack()

        self.frames["Vendas"] = tk.Frame(root, bg="white")
        tk.Label(self.frames["Vendas"], text="Vendas", font=("Arial", 24)).pack()

        self.frames["Produtos"] = tk.Frame(root, bg="white")
        tk.Label(self.frames["Produtos"], text="Produtos", font=("Arial", 24)).pack()

        self.mostrar_frame("Financeiro")

    def mostrar_frame(self, nome):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[nome].pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    App(root)
    root.mainloop()