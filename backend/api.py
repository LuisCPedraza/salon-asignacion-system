import http.server
import socketserver
import json
import urllib.parse
from http import HTTPStatus
from typing import Dict, Any
from models import Grupo, Usuario  # Integra con Usuario para auth/CRUD

PORT = 8000

class APIServerRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """GET endpoints."""
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/users':
            self._send_json_response(Usuario._db.get_all_entities('usuarios'), HTTPStatus.OK)  # Lista usuarios (HU1)
        elif parsed_path.path == '/grupos':
            groups = Grupo.get_all()  # HU4: Lista grupos
            self._send_json_response([g.__dict__ for g in groups], HTTPStatus.OK)  # Serializa dict
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
        elif parsed_path.path == '/grupos':
            group = Grupo.create(
                parsed_data.get('nombre'),
                parsed_data.get('nivel'),
                parsed_data.get('num_estudiantes', 0),
                parsed_data.get('caracteristicas', '')
            )
            if group:
                self._send_json_response({'id': group.id, 'message': 'Grupo creado'}, HTTPStatus.CREATED)
            else:
                self._send_json_response({'error': 'num_estudiantes <=0 inválido'}, HTTPStatus.BAD_REQUEST)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def do_PUT(self):
        """PUT /grupos/{id}: Update grupo (HU4)."""
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith('/grupos/'):
            group_id = parsed_path.path.split('/')[-1]  # Extrae id
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = json.loads(put_data)
            if Grupo.update_by_id(group_id, parsed_data):
                self._send_json_response({'message': 'Grupo actualizado'}, HTTPStatus.OK)
            else:
                self._send_json_response({'error': 'Grupo no encontrado'}, HTTPStatus.NOT_FOUND)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def do_DELETE(self):
        """DELETE /grupos/{id}: Desactiva grupo (HU4)."""
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith('/grupos/'):
            group_id = parsed_path.path.split('/')[-1]
            if Grupo.delete_by_id(group_id):
                self._send_json_response({'message': 'Grupo desactivado'}, HTTPStatus.OK)
            else:
                self._send_json_response({'error': 'Grupo no encontrado'}, HTTPStatus.NOT_FOUND)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def _send_json_response(self, data: Dict[str, Any], status: int):
        """Utilidad: Envía JSON con headers CORS para frontend (TH4: responsive)."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Simple CORS
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        """Maneja preflight CORS para POST/GET/PUT/DELETE (browser cross-origin)."""
        self.send_response(HTTPStatus.OK)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), APIServerRequestHandler) as httpd:
        print(f"API server corriendo en http://localhost:{PORT}")
        httpd.serve_forever()
        