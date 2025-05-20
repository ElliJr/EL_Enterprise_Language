# # filepath: graficos-piechart/src/graficos.py

# import tkinter as tk
# from tkinter import messagebox
# import matplotlib.pyplot as plt

# def generate_pie_chart(values):
#     labels = [f'Value {i+1}' for i in range(len(values))]
#     plt.figure(figsize=(8, 6))
#     plt.pie(values, labels=labels, autopct='%1.1f%%')
#     plt.title('Pie Chart')
#     plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
#     plt.show()

# def submit_values():
#     try:
#         input_values = entry.get().split(',')
#         values = [float(value.strip()) for value in input_values]
#         if any(v < 0 for v in values):
#             raise ValueError("Values must be non-negative.")
#         generate_pie_chart(values)
#     except ValueError as e:
#         messagebox.showerror("Input Error", str(e))

# app = tk.Tk()
# app.title("Pie Chart Generator")

# label = tk.Label(app, text="Enter values separated by commas:")
# label.pack(pady=10)

# entry = tk.Entry(app, width=50)
# entry.pack(pady=10)

# submit_button = tk.Button(app, text="Generate Pie Chart", command=submit_values)
# submit_button.pack(pady=20)

# app.mainloop()