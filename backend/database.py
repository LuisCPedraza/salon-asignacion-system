import json
import os
from typing import Dict, List, Optional, Any
import uuid

class DatabaseManager:
    def __init__(self, base_dir: str = 'db_data'):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        self.data: Dict[str, List[Dict]] = self._load_all_data()

    def _load_all_data(self) -> Dict[str, List[Dict]]:
        """Carga todas tablas desde JSON (usuarios.json, grupos.json, etc.)."""
        tables = {}
        for filename in os.listdir(self.base_dir):
            if filename.endswith('.json'):
                table_name = filename[:-5]  # e.g., usuarios.json → 'usuarios'
                file_path = os.path.join(self.base_dir, filename)
                with open(file_path, 'r') as f:
                    tables[table_name] = json.load(f)
        # Inicializa tablas vacías si no existen
        if 'usuarios' not in tables:
            tables['usuarios'] = []
        if 'grupos' not in tables:
            tables['grupos'] = []
        return tables

    def _save_table(self, table_name: str):
        """Guarda tabla específica a JSON."""
        file_path = os.path.join(self.base_dir, f"{table_name}.json")
        with open(file_path, 'w') as f:
            json.dump(self.data.get(table_name, []), f, indent=2)

    def create_entity(self, table: str, entity_data: Dict[str, Any], unique_fields: List[str] = []) -> Optional[str]:
        """Generic create (HU1/HU3: Valida unique si fields)."""
        if unique_fields:
            for field in unique_fields:
                if any(e.get(field) == entity_data.get(field) for e in self.data.get(table, [])):
                    return None  # Duplicado
        entity_id = entity_data.get('id', str(uuid.uuid4()))  # UUID
        entity_data['id'] = entity_id
        entity_data['created_at'] = entity_data.get('created_at', None)
        entity_data['updated_at'] = entity_data.get('updated_at', None)
        if table not in self.data:
            self.data[table] = []
        self.data[table].append(entity_data)
        self._save_table(table)
        return entity_id

    def get_entity_by_id(self, table: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Generic get by ID."""
        for entity in self.data.get(table, []):
            if entity['id'] == entity_id:
                return entity
        return None

    def get_all_entities(self, table: str) -> List[Dict[str, Any]]:
        """Generic list all (para /users GET)."""
        return self.data.get(table, [])

    def update_entity(self, table: str, entity_id: str, updates: Dict[str, Any]) -> bool:
        """Generic update."""
        for entity in self.data.get(table, []):
            if entity['id'] == entity_id:
                entity.update(updates)
                entity['updated_at'] = None
                self._save_table(table)
                return True
        return False

    def delete_entity(self, table: str, entity_id: str) -> bool:
        """Generic soft delete (set activo=False)."""
        return self.update_entity(table, entity_id, {'activo': False})

# Backward compat for Usuario (reemplaza calls)
def create_user(user_data: Dict) -> Optional[str]:
    dm = DatabaseManager()
    return dm.create_entity('usuarios', user_data, ['email'])

def get_user_by_email(email: str) -> Optional[Dict]:
    dm = DatabaseManager()
    for user in dm.get_all_entities('usuarios'):
        if user['email'] == email:
            return user
    return None

def update_user(user_id: str, updates: Dict) -> bool:
    dm = DatabaseManager()
    return dm.update_entity('usuarios', user_id, updates)
