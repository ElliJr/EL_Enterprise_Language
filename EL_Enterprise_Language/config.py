# config.py
import json
import os

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