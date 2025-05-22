import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graficos:
    def __init__(self, parent=None):
        # Se parent for None, cria uma janela própria
        self.is_standalone = parent is None
        self.parent = parent if parent else tk.Tk()
        if self.is_standalone:
            self.parent.title("Pie Chart Generator")
            self.parent.geometry("400x200")
        self.build_interface()

    def build_interface(self):
        label = tk.Label(self.parent, text="Digite os valores separados por vírgula:")
        label.pack(pady=10)

        self.entry = tk.Entry(self.parent, width=50)
        self.entry.pack(pady=10)

        submit_button = tk.Button(self.parent, text="Gerar Gráfico de Pizza", command=self.submit_values)
        submit_button.pack(pady=20)

    def submit_values(self):
        try:
            input_values = self.entry.get().split(',')
            values = [float(value.strip()) for value in input_values]
            if any(v < 0 for v in values):
                raise ValueError("Valores devem ser não-negativos.")
            self.generate_pie_chart(values)
        except ValueError as e:
            messagebox.showerror("Erro de entrada", str(e))

    @staticmethod
    def generate_pie_chart(self, values):
        from matplotlib import pyplot as plt
        labels = [f'Valor {i+1}' for i in range(len(values))]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title('Gráfico de Pizza')
        ax.axis('equal')
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Para testar isoladamente:
# if __name__ == "__main__":
#     Graficos()
#     tk.mainloop()