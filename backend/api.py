import http.server
import socketserver
import json
import urllib.parse
from http import HTTPStatus
from typing import Dict, Any
from models import Usuario  # Integra con Usuario para auth/CRUD

PORT = 8000

class APIServerRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """GET endpoints."""
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/users':
            self._send_json_response(Usuario._db.data, HTTPStatus.OK)  # Lista usuarios (HU1)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def do_POST(self):
        """POST endpoints."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = json.loads(post_data)
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == '/login':
            email = parsed_data.get('email')
            password = parsed_data.get('password')
            if Usuario.autenticar(email, password):
                user = Usuario.get_by_email(email)
                response = {'success': True, 'rol': user.get_rol()}  # HU2: Respuesta por rol
            else:
                response = {'success': False, 'error': 'Credenciales inválidas'}
            self._send_json_response(response, HTTPStatus.OK if response['success'] else HTTPStatus.UNAUTHORIZED)
        elif parsed_path.path == '/users':
            user = Usuario.create(
                parsed_data.get('nombre'),
                parsed_data.get('email'),
                parsed_data.get('password'),
                parsed_data.get('rol')
            )
            if user:
                self._send_json_response({'id': user.id, 'message': 'Usuario creado'}, HTTPStatus.CREATED)
            else:
                self._send_json_response({'error': 'Email duplicado'}, HTTPStatus.CONFLICT)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def _send_json_response(self, data: Dict[str, Any], status: int):
        """Utilidad: Envía JSON con headers CORS para frontend (TH4: responsive)."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Simple CORS
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), APIServerRequestHandler) as httpd:
        print(f"API server corriendo en http://localhost:{PORT}")
        httpd.serve_forever()
        