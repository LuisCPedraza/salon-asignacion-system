import json
import os
import uuid
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_file: str = 'db_data/usuarios.json'):
        self.db_file = db_file
        self.data: List[Dict] = self._load_data()

    def _load_data(self) -> List[Dict]:
        """Carga datos desde JSON (simula SELECT * FROM usuario)."""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return []  # BD vacía inicial

    def _save_data(self):
        """Guarda datos a JSON (simula INSERT/UPDATE)."""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def create_user(self, user_data: Dict) -> Optional[str]:
        """HU1: Crea usuario (verifica email único, simula UNIQUE constraint)."""
        # Simula UK check
        if any(u['email'] == user_data['email'] for u in self.data):
            return None  # Error: duplicado
        user_data['id'] = user_data.get('id', str(uuid.uuid4()))  # UUID si no proporcionado
        user_data['created_at'] = user_data.get('created_at', None)
        user_data['updated_at'] = user_data.get('updated_at', None)
        self.data.append(user_data)
        self._save_data()
        return user_data['id']

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """HU2: Busca por email (simula SELECT WHERE email)."""
        for user in self.data:
            if user['email'] == email:
                return user
        return None

    def update_user(self, user_id: str, updates: Dict) -> bool:
        """HU1: Actualiza (e.g., desactivar: set activo=False)."""
        for user in self.data:
            if user['id'] == user_id:
                user.update(updates)
                user['updated_at'] = None  # Timestamp en real BD
                self._save_data()
                return True
        return False

    def delete_user(self, user_id: str) -> bool:
        """HU1: Desactiva (soft delete: set activo=False)."""
        return self.update_user(user_id, {'activo': False})
    