import json
import tkinter as tk
from tkinter import messagebox
import config

def carregar_dados(arquivo, lista, tree):
    """Carrega dados de um arquivo JSON e exibe em uma Treeview."""
    try:
        with open(arquivo, "r", encoding="utf-8") as file:
            dados = json.load(file)
            lista.extend(dados)
            for item in dados:
                tree.insert("", "end", values=list(item.values()))
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar o arquivo JSON '{arquivo}'. Verifique se o formato está correto.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar os dados: {e}")

def salvar_dados(arquivo, lista_de_dados):
    """Salva uma lista de dados em um arquivo JSON."""
    try:
        with open(arquivo, "w", encoding="utf-8") as file:
            json.dump(lista_de_dados, file, indent=4, ensure_ascii=False)
        print(f"Dados salvos com sucesso em '{arquivo}'.")
    except Exception as e:
        print(f"Erro ao salvar os dados em '{arquivo}': {e}")
        messagebox.showerror("Erro ao Salvar", f"Ocorreu um erro ao salvar os dados: {e}")

def abrir_janela_novo(parent, arquivo_salvar, lista_dados, treeview, labels):
    """Abre uma janela para adicionar um novo item."""
    nova_janela = tk.Toplevel(parent)
    nova_janela.title("Adicionar Novo Item")

    entradas = {}
    for i, label_texto in enumerate(labels):
        label = tk.Label(nova_janela, text=label_texto)
        label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
        entrada = tk.Entry(nova_janela)
        entrada.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        entradas[label_texto] = entrada

    def adicionar_item():
        novo_item = {label: entrada.get() for label, entrada in entradas.items()}
        lista_dados.append(novo_item)
        treeview.insert("", "end", values=list(novo_item.values()))
        salvar_dados(arquivo_salvar, lista_dados) # Chama a função salvar_dados aqui
        nova_janela.destroy()

    botao_adicionar = tk.Button(nova_janela, text="Adicionar", command=adicionar_item)
    botao_adicionar.grid(row=len(labels), columnspan=2, pady=10)

def remover_item(parent, arquivo_salvar, lista_dados, treeview):
    """Remove o item selecionado da Treeview e da lista de dados."""
    item_selecionado = treeview.selection()
    if not item_selecionado:
        messagebox.showinfo("Seleção Necessária", "Por favor, selecione um item para remover.")
        return

    item = treeview.item(item_selecionado)['values']
    indice = -1
    for i, produto in enumerate(lista_dados):
        if list(produto.values()) == list(item):
            indice = i
            break

    if indice != -1:
        del lista_dados[indice]
        treeview.delete(item_selecionado)
        salvar_dados(arquivo_salvar, lista_dados) # Chama a função salvar_dados aqui
    else:
        messagebox.showerror("Erro", "Não foi possível encontrar o item na lista de dados.")

def aplicar_tema(root):
    tema = config.get_tema()
    if tema == "Claro":
        root.config(bg="white")
        # Configure as cores dos outros widgets para o tema claro
    elif tema == "Escuro":
        root.config(bg="#333333")
        # Configure as cores dos outros widgets para o tema escuro
    # Adicione mais temas conforme necessário
# Outras funções que você possa ter em utils.py