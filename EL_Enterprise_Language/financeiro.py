import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graficos:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(bg="#1E3A5F")

        # Header
        header = tk.Label(
            parent, text="Enterprise Dashboard",
            font=("Segoe UI", 26, "bold"),
            bg="#1E3A5F", fg="#00f7ff", pady=16
        )
        header.pack(fill="x")

        # Cards Frame
        cards_frame = tk.Frame(parent, bg="#081A31")
        cards_frame.pack(fill="x", pady=(30, 10), padx=40)

        card_bg = "#1E3A5F"
        card_fg = "#00f7ff"
        card_font = ("Segoe UI", 28, "bold")
        card_label_font = ("Segoe UI", 13)
        card_padx = 30

        self.card_vendas = self._criar_card(cards_frame, "1200", "Vendas", card_bg, card_fg, card_font, card_label_font)
        self.card_usuarios = self._criar_card(cards_frame, "340", "Usuários", card_bg, card_fg, card_font, card_label_font)
        self.card_faturamento = self._criar_card(cards_frame, "R$ 48.000", "Faturamento", card_bg, card_fg, card_font, card_label_font)

        self.card_vendas.pack(side="left", expand=True, fill="both", padx=(0, card_padx))
        self.card_usuarios.pack(side="left", expand=True, fill="both", padx=(0, card_padx))
        self.card_faturamento.pack(side="left", expand=True, fill="both")

        # Gráfico
        self.chart_frame = tk.Frame(parent, bg="#1E3A5F")
        self.chart_frame.pack(fill="both", expand=True, padx=40, pady=(10, 30))

        self.labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        self.valores = [200, 300, 400, 350, 450, 500]
        self._criar_grafico()

        # Notificações
        self.notif_container = tk.Frame(parent, bg="", highlightthickness=0)
        self.notif_container.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

        # Atualização automática
        self._atualizar_grafico()

    def _criar_card(self, parent, valor, texto, bg, fg, font, label_font):
        frame = tk.Frame(parent, bg=bg, bd=0, relief="flat")
        tk.Label(frame, text=valor, font=font, bg=bg, fg=fg).pack(pady=(10, 0))
        tk.Label(frame, text=texto, font=label_font, bg=bg, fg="#66fcf1").pack(pady=(0, 10))
        return frame

    def _criar_grafico(self):
        # Limpa gráfico anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(7, 3.5), facecolor="#1E3A5F")
        bars = ax.bar(
            self.labels, self.valores,
            color="#00f7ffcc", edgecolor="#00f7ff", linewidth=2
        )
        ax.set_facecolor("#1E3A5F")
        ax.tick_params(colors="#66fcf1", labelsize=12)
        ax.spines['bottom'].set_color('#00f7ff')
        ax.spines['left'].set_color('#00f7ff')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_title("Vendas Mensais", color="#00f7ff", fontsize=16)
        for label in ax.get_xticklabels():
            label.set_color("#66fcf1")
        for label in ax.get_yticklabels():
            label.set_color("#66fcf1")
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _atualizar_grafico(self):
        # Atualiza os dados com valores aleatórios
        self._criar_grafico()
        self._mostrar_notificacao("Gráfico atualizado com novos dados de vendas!")
        # Atualiza a cada 3 segundos
        self.parent.after(3000, self._atualizar_grafico)

    def _mostrar_notificacao(self, msg):
        notif = tk.Label(
            self.notif_container, text=msg,
            font=("Arial", 11, "bold"),
            bg="#232323", fg="#D9A87E",
            bd=2, relief="ridge", padx=16, pady=8
        )
        notif.pack(anchor="se", pady=5)
        # Remove após 4.2 segundos, se ainda existir
        def destroy_if_exists():
            if notif.winfo_exists():
                notif.destroy()
        notif.after(4200, destroy_if_exists)


# Para testar isolada