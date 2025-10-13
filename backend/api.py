import http.server
import socketserver
import json
import urllib.parse
from http import HTTPStatus
from typing import Dict, Any
from models import Grupo, Profesor, Usuario, Salon

PORT = 8000

class APIServerRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """GET endpoints."""
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == '/users':
            self._send_json_response(Usuario._db.get_all_entities('usuarios'), HTTPStatus.OK)  # HU1
        elif parsed_path.path == '/grupos':
            groups = Grupo.get_all()  # HU4
            self._send_json_response([g.__dict__ for g in groups], HTTPStatus.OK)
        elif parsed_path.path == '/salones':
            salones = Salon.get_all()  # HU6
            self._send_json_response([s.__dict__ for s in salones], HTTPStatus.OK)
        elif parsed_path.path == '/profesores':
            profesores = Profesor.get_all()  # HU8: Lista profesores
            self._send_json_response([p.__dict__ for p in profesores], HTTPStatus.OK)
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
                response = {'success': True, 'rol': user.get_rol()}
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
        elif parsed_path.path == '/salones':
            salon = Salon.create(
                parsed_data.get('codigo'),
                parsed_data.get('capacidad', 0),
                parsed_data.get('ubicacion', '')
            )
            if salon:
                self._send_json_response({'id': salon.id, 'message': 'Salón creado'}, HTTPStatus.CREATED)
            else:
                self._send_json_response({'error': 'capacidad <=0 o codigo duplicado inválido'}, HTTPStatus.BAD_REQUEST)
        elif parsed_path.path == '/profesores':
            profesor = Profesor.create(
                parsed_data.get('usuario_id'),
                parsed_data.get('especialidades', ''),
                parsed_data.get('hoja_vida_url', '')
            )
            if profesor:
                self._send_json_response({'id': profesor.id, 'message': 'Profesor creado'}, HTTPStatus.CREATED)
            else:
                self._send_json_response({'error': 'usuario_id inválido o duplicado'}, HTTPStatus.BAD_REQUEST)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def do_PUT(self):
        """PUT /{entity}/{id}: Update (grupos/salones/profesores)."""
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.split('/')
        if len(path_parts) == 3 and path_parts[1] in ['grupos', 'salones', 'profesores']:
            entity = path_parts[1]
            entity_id = path_parts[2]
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = json.loads(put_data)
            if entity == 'grupos':
                success = Grupo.update_by_id(entity_id, parsed_data)
            elif entity == 'salones':
                success = Salon.update_by_id(entity_id, parsed_data)
            elif entity == 'profesores':
                success = Profesor.update_by_id(entity_id, parsed_data)
            if success:
                self._send_json_response({'message': f'{entity[:-1]} actualizado'}, HTTPStatus.OK)
            else:
                self._send_json_response({'error': f'{entity[:-1]} no encontrado'}, HTTPStatus.NOT_FOUND)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def do_DELETE(self):
        """DELETE /{entity}/{id}: Desactiva (grupos/salones/profesores)."""
        parsed_path = urllib.parse.urlparse(self.path)
        path_parts = parsed_path.path.split('/')
        if len(path_parts) == 3 and path_parts[1] in ['grupos', 'salones', 'profesores']:
            entity = path_parts[1]
            entity_id = path_parts[2]
            if entity == 'grupos':
                success = Grupo.delete_by_id(entity_id)
            elif entity == 'salones':
                success = Salon.delete_by_id(entity_id)
            elif entity == 'profesores':
                success = Profesor.delete_by_id(entity_id)
            if success:
                self._send_json_response({'message': f'{entity[:-1]} desactivado'}, HTTPStatus.OK)
            else:
                self._send_json_response({'error': f'{entity[:-1]} no encontrado'}, HTTPStatus.NOT_FOUND)
        else:
            self._send_json_response({'error': 'Endpoint no encontrado'}, HTTPStatus.NOT_FOUND)

    def _send_json_response(self, data: Dict[str, Any], status: int):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), APIServerRequestHandler) as httpd:
        print(f"API server corriendo en http://localhost:{PORT}")
        httpd.serve_forever()
