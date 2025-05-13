import http.server
import socketserver
import urllib.parse
import json
import os

PORT = 3000
HOST = "127.0.0.1"  # Ou "0.0.0.0" para ouvir em todas as interfaces
DATA_FILE = "usuarios_servidor.json" # Nome do arquivo para salvar os dados

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Trata requisições GET.  Por enquanto, apenas retorna "Hello World!".
        """
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Ta online men\n")  # Envia a resposta como bytes

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        post_data = self.rfile.read(content_length)
        dados_decodificados = post_data.decode('utf-8')
        print(f"Dados recebidos no POST: {dados_decodificados}")

        # Interpreta os dados como URL encoded
        dados_parsed = urllib.parse.parse_qs(dados_decodificados)
        # Transforma a estrutura do dicionário para algo mais amigável
        dados = {
            "usuario": dados_parsed.get('usuario', [''])[0],
            "email": dados_parsed.get('email', [''])[0],
            "senha": dados_parsed.get('senha', [''])[0],
        }

        # Rota para cadastro
        if self.path == '/cadastro':
            self.processar_cadastro(dados)
        # Rota para login
        elif self.path == '/login':
            self.processar_login(dados)
        else:
            self.send_error(404, "Rota não encontrada")

    def processar_cadastro(self, dados):
        """Processa o cadastro de um novo usuário."""
        # Validação básica dos dados
        if not dados["usuario"] or not dados["email"] or not dados["senha"]:
            self.send_error(400, "Todos os campos são obrigatórios")
            return

        # Carrega os usuários existentes, adiciona o novo e salva
        usuarios = self.carregar_usuarios()
        # Verifica se o usuário já existe
        for usuario_existente in usuarios: # Alterado de usuario para usuario_existente
            if usuario_existente["usuario"] == dados["usuario"]:
                self.send_error(400, "Usuário já existe")
                return
        usuarios.append(dados)
        self.salvar_usuarios(usuarios)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Usuario cadastrado com sucesso!\n")

    def processar_login(self, dados):
        """Processa o login de um usuário."""
        if not dados["usuario"] or not dados["senha"]:
            self.send_error(400, "Usuário e senha são obrigatórios")
            return

        usuarios = self.carregar_usuarios()
        for usuario in usuarios:
            if usuario["usuario"] == dados["usuario"] and usuario["senha"] == dados["senha"]:
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Login realizado com sucesso!\n")
                return

        self.send_error(401, "Usuario ou senha incorretos")

    def carregar_usuarios(self):
        """Carrega a lista de usuários do arquivo JSON."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        else:
            return []

    def salvar_usuarios(self, usuarios):
        """Salva a lista de usuários no arquivo JSON."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")
            self.send_error(500, "Erro ao salvar dados".encode('utf-8')) # Codifica a string para bytes

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), MyHandler) as httpd:
        print(f"Servindo em http://{HOST}:{PORT}")
        httpd.serve_forever()