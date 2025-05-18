import http.server
import socketserver
import urllib.parse
import json
import os
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import base64
from datetime import datetime
import socket  # Importe o módulo socket para tratar erros de endereço
import html # Importe o módulo html


PORT = 3000
HOST = "127.0.0.1"
DATA_FILE = "usuarios_servidor.json"
MAX_REQUEST_SIZE = 1024 * 1024  # 1MB max request size



class MyHandler(http.server.BaseHTTPRequestHandler):
    sessions = {}  # Inicializa o dicionário sessions
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """
        Trata requisições GET.
        """
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Servidor rodando!\n")
        except Exception as e:
            self.send_error(500, f"Erro ao processar requisição GET: {e}")

    def do_POST(self):
        """
        Trata requisições POST, com limite de tamanho.
        """
        try:
            content_length = int(self.headers.get('content-length', 0))

            if content_length > MAX_REQUEST_SIZE:
                self.send_error(413, "Request too large")
                return

            post_data = self.rfile.read(content_length)
            dados_decodificados = post_data.decode('utf-8')
            print(f"Dados recebidos no POST: {dados_decodificados}")

            dados_parsed = urllib.parse.parse_qs(dados_decodificados)
            dados = {
                "usuario": dados_parsed.get('usuario', [''])[0],
                "email": dados_parsed.get('email', [''])[0],
                "senha": dados_parsed.get('senha', [''])[0],
                "tipo_grafico": dados_parsed.get('tipo_grafico', [''])[0],  # Novo parâmetro
            }

            if self.path == '/cadastro':
                self.processar_cadastro(dados)
            elif self.path == '/login':
                self.processar_login(dados)
            elif self.path == '/conta':
                self.processar_conta(dados)
            elif self.path == '/graficos':  # Nova rota para gráficos
                self.gerar_graficos(dados["tipo_grafico"])
            else:
                self.send_error(404, "Rota não encontrada")
        except Exception as e:
            self.send_error(500, f"Erro ao processar requisição POST: {e}")

    def gerar_graficos(self, tipo_grafico):
        """
        Gera os gráficos de rendimento e faturamento e retorna como JSON.

        Args:
            tipo_grafico (str): O tipo de gráfico a ser gerado ('mes' ou 'ano').
        """
        try:
            if tipo_grafico not in ('mes', 'ano'):
                self.send_error(400, "Tipo de gráfico inválido. Use 'mes' ou 'ano'.".encode('utf-8'))
                return

            # Obtenha os dados de rendimento e faturamento
            rendimento_data, faturamento_data = self.obter_dados_vendas(tipo_grafico)

            # Crie os gráficos
            rendimento_grafico = self.criar_grafico_rendimento(rendimento_data, tipo_grafico)
            faturamento_grafico = self.criar_grafico_faturamento(faturamento_data, tipo_grafico)
        except Exception as e:
            self.send_error(500, f"Erro ao gerar gráficos: {e}".encode('utf-8'))
            return

        # Combine os gráficos em um dicionário para enviar como JSON
        graficos_base64 = {
            "rendimento": rendimento_grafico,
            "faturamento": faturamento_grafico,
        }

        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(graficos_base64).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erro ao enviar resposta JSON: {e}".encode('utf-8'))

    def obter_dados_vendas(self, tipo):
        """
        Obtém os dados de rendimento e faturamento do banco de dados ou outra fonte.
        Esta é uma função de exemplo que retorna dados fictícios.
        Você deve substituir esta função com sua lógica real de acesso aos dados.
        """
        if tipo == 'mes':
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            rendimento_mensal = [2000, 2500, 3000, 3200, 3500, 4000, 4500, 4200, 4000, 4300, 4600, 5000]
            faturamento_mensal = [5000, 5500, 6000, 6500, 7000, 7500, 8000, 7800, 7500, 8000, 8500, 9000]
            return (meses, rendimento_mensal), (meses, faturamento_mensal)
        elif tipo == 'ano':
            anos = ['Ano 1', 'Ano 2', 'Ano 3', 'Ano 4', 'Ano 5']
            rendimento_anual = [35000, 40000, 45000, 50000, 55000]
            faturamento_anual = [80000, 90000, 100000, 110000, 120000]
            return (anos, rendimento_anual), (anos, faturamento_anual)
        else:
            return [], []

    def criar_grafico_rendimento(self, dados, tipo):
        """
        Cria o gráfico de rendimento usando Matplotlib.

        Args:
            dados (tuple): Dados para o gráfico (rótulos e valores).
            tipo (str): Tipo do período ('mes' ou 'ano') para o título.

        Returns:
            str: A imagem do gráfico em base64.
        """
        try:
            plt.figure(figsize=(8, 4))
            plt.bar(dados[0], dados[1], color='#86efac', edgecolor='#22c55e')
            plt.title(f'Rendimento {tipo.capitalize()}', color='#0e7490', fontsize=16)
            plt.xlabel('Período', color='#4a5568', fontsize=12)
            plt.ylabel('Valor', color='#4a5568', fontsize=12)
            plt.xticks(color='#4a5568', fontsize=10)
            plt.yticks(color='#4a5568', fontsize=10)
            plt.grid(axis='y', linestyle='--', color='#e2e8f0')
            plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))  # Formatação

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            imagem_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            return imagem_base64
        except Exception as e:
            self.send_error(500, f"Erro ao criar gráfico de rendimento: {e}".encode('utf-8'))
            return None

    def criar_grafico_faturamento(self, dados, tipo):
        """
        Cria o gráfico de faturamento usando Matplotlib.

        Args:
            dados (tuple): Dados para o gráfico (rótulos e valores).
            tipo (str): Tipo do período ('mes' ou 'ano') para o título.

        Returns:
            str: A imagem do gráfico em base64.
        """
        try:
            plt.figure(figsize=(8, 4))
            plt.plot(dados[0], dados[1], color='#facc15', marker='o', linestyle='-', linewidth=2)
            plt.title(f'Faturamento {tipo.capitalize()}', color='#0e7490', fontsize=16)
            plt.xlabel('Período', color='#4a5568', fontsize=12)
            plt.ylabel('Valor', color='#4a5568', fontsize=12)
            plt.xticks(color='#4a5568', fontsize=10)
            plt.yticks(color='#4a5568', fontsize=10)
            plt.grid(axis='y', linestyle='--', color='#e2e8f0')
            plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))  # Formatação

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            imagem_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            return imagem_base64
        except Exception as e:
            self.send_error(500, f"Erro ao criar gráfico de faturamento: {e}".encode('utf-8'))
            return None

    def processar_cadastro(self, dados):
        """Processa o cadastro de um novo usuário."""
        try:
            if not dados["usuario"] or not dados["email"] or not dados["senha"]:
                self.send_error(400, "Todos os campos são obrigatórios".encode('utf-8'))
                return

            usuarios = self.carregar_usuarios()
            for usuario_existente in usuarios:
                if usuario_existente["usuario"] == dados["usuario"]:
                    self.send_error(400, "Usuário já existe".encode('utf-8'))
                    return
            usuarios.append(dados)
            self.salvar_usuarios(usuarios)

            # Envia os dados do usuário de volta para o cliente
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            response_data = {
                "mensagem": "Utilizador registado com sucesso!",
                "usuario": dados["usuario"],
                "email": dados["email"],
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erro ao processar cadastro: {e}".encode('utf-8'))

    def processar_login(self, dados):
        """Processa o login de um usuário e inicia a sessão."""
        try:
            if not dados["usuario"] or not dados["senha"]:
                self.send_error(400, "Utilizador e senha são obrigatórios")
                return

            usuarios = self.carregar_usuarios()
            for usuario_existente in usuarios:
                if usuario_existente["usuario"] == dados["usuario"] and usuario_existente["senha"] == dados["senha"]:
                    # Inicia a sessão (simplificado)
                    self.sessions[dados["usuario"]] = {"logado": True, "email": usuario_existente["email"]}
                    self.send_response(200)
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    dados_usuario = {
                        "usuario": usuario_existente["usuario"],
                        "email": usuario_existente["email"],
                    }
                    self.wfile.write(json.dumps(dados_usuario).encode('utf-8'))
                    return

            self.send_error(401, "Utilizador ou senha incorretos")
        except Exception as e:
            self.send_error(500, f"Erro ao processar login: {e}")

    def processar_conta(self, dados):
        """Retorna os dados do usuário, se a sessão for válida."""
        try:
            if not dados["usuario"]:
                self.send_error(400, "Utilizador é obrigatório".encode('utf-8'))
                return

            if dados["usuario"] in self.sessions:
                usuario_logado = self.sessions[dados["usuario"]]
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                dados_usuario = {
                    "usuario": dados["usuario"],
                    "email": usuario_logado["email"],
                }
                self.wfile.write(json.dumps(dados_usuario).encode('utf-8'))
            else:
                self.send_error(401, "Sessão inválida. Faça login novamente.".encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Erro ao processar login: {e}")

    def carregar_usuarios(self):
        """Carrega a lista de utilizadores do arquivo JSON."""
        try:
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        return json.load(f)
                except json.JSONDecodeError:
                    print(f"Erro ao decodificar JSON do arquivo {DATA_FILE}. Retornando lista vazia.")
                    return []
            else:
                print(f"Arquivo {DATA_FILE} não existe. Retornando lista vazia.")
                return []
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}. Retornando lista vazia.")
            return []  # Retorna uma lista vazia em caso de erro ao carregar

    def salvar_usuarios(self, usuarios):
        """Salva a lista de utilizadores no arquivo JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar utilizadores: {e}")
            self.send_error(500, "Erro ao salvar dados")


if __name__ == "__main__":
    try:
        # Tenta criar o socket e fazer o bind
        with socketserver.TCPServer((HOST, PORT), MyHandler) as httpd:
            print(f"Servindo em http://{HOST}:{PORT}")
            httpd.serve_forever()
    except socket.error as e:
        # Captura erros específicos de socket, como endereço em uso
        print(f"Erro ao iniciar o servidor: {e}")
    except Exception as e:
        # Captura outros erros que podem ocorrer ao iniciar o servidor
        print(f"Erro inesperado ao iniciar o servidor: {e}")