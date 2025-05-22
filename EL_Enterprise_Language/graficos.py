import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graficos:
    def __init__(self, parent):
        self.parent = parent
        self.build_interface()

    def build_interface(self):
        label = tk.Label(self.parent, text="Digite os valores separados por vírgula:", bg="white")
        label.pack(pady=10)

        self.entry = tk.Entry(self.parent, width=50)
        self.entry.pack(pady=10)

        submit_button = tk.Button(self.parent, text="Gerar Gráfico de Pizza", command=self.submit_values, bg="#2C5EAA", fg="white")
        submit_button.pack(pady=10)

        # Frame onde o gráfico será exibido
        self.frame_grafico = tk.Frame(self.parent, bg="white")
        self.frame_grafico.pack(pady=10, fill=tk.BOTH, expand=True)

    def submit_values(self):
        # Limpa o gráfico anterior, se houver
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        try:
            input_values = self.entry.get().split(',')
            values = [float(value.strip()) for value in input_values]
            if any(v < 0 for v in values):
                raise ValueError("Valores devem ser não-negativos.")
            self.generate_pie_chart(values)
        except ValueError as e:
            messagebox.showerror("Erro de entrada", str(e))

    def generate_pie_chart(self, values):
        labels = [f'Valor {i+1}' for i in range(len(values))]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title('Gráfico de Pizza')
        ax.axis('equal')
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Exemplo de uso isolado:
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="white")
    root.title("Dashboard Financeiro")
    Graficos(root)
    root.geometry("700x500")
    root.mainloop()