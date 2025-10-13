import uuid
import hashlib
from typing import Optional, Dict
from database import DatabaseManager  # Importa para integración

class Usuario:
    _db = DatabaseManager()  # Instancia global para simplicidad (singleton-like; refactor a inyección después)

    def __init__(self, id=None, nombre=None, email=None, password_hash=None, rol=None, activo=True, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.rol = rol
        self.activo = activo
        self.created_at = created_at or None
        self.updated_at = updated_at or None

    @classmethod
    def create(cls, nombre: str, email: str, password: str, rol: str) -> Optional['Usuario']:
        """HU1: Crea usuario persistente (integra DB)."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user_data = {
            'nombre': nombre,
            'email': email,
            'password_hash': password_hash,
            'rol': rol,
            'activo': True
        }
        user_id = cls._db.create_user(user_data)
        if user_id:
            user_data['id'] = user_id
            return cls(**user_data)
        return None  # Fallo: email duplicado

    @classmethod
    def get_by_email(cls, email: str) -> Optional['Usuario']:
        """HU2: Carga desde DB por email."""
        user_data = cls._db.get_user_by_email(email)
        if user_data:
            return cls(**user_data)
        return None

    @classmethod
    def autenticar(cls, email: str, password: str) -> bool:
        """HU2: Refactor: Usa DB para validar (carga por email)."""
        user = cls.get_by_email(email)
        if not user:
            return False
        if not user.activo:
            return False
        expected_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.password_hash == expected_hash

    def update(self, updates: Dict) -> bool:
        """HU1: Actualiza persistente (e.g., desactivar)."""
        if not self.id:
            return False
        updates['updated_at'] = None  # Timestamp
        return self._db.update_user(self.id, updates)

    def delete(self) -> bool:
        """HU1: Desactiva persistente."""
        if not self.id:
            return False
        return self._db.update_user(self.id, {'activo': False})

    def set_password(self, password: str):
        """Hash y actualiza (integra update)."""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.update({'password_hash': self.password_hash})

    def get_rol(self):
        return self.rol

    def es_activo(self):
        return self.activo
class Grupo:
    _db = DatabaseManager()  # Usa global para todas tablas

    def __init__(self, id=None, nombre=None, nivel=None, num_estudiantes=None, caracteristicas=None, activo=True, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.nombre = nombre
        self.nivel = nivel
        self.num_estudiantes = num_estudiantes
        self.caracteristicas = caracteristicas
        self.activo = activo
        self.created_at = created_at or None
        self.updated_at = updated_at or None

    @classmethod
    def create(cls, nombre: str, nivel: str, num_estudiantes: int, caracteristicas: str = '') -> Optional['Grupo']:
        """HU3: Crea grupo persistente (valida num_estudiantes >0)."""
        if num_estudiantes <= 0:
            return None
        group_data = {
            'nombre': nombre,
            'nivel': nivel,
            'num_estudiantes': num_estudiantes,
            'caracteristicas': caracteristicas,
            'activo': True
        }
        group_id = cls._db.create_entity('grupos', group_data, [])  # No unique por doc
        if group_id:
            group_data['id'] = group_id
            return cls(**group_data)
        return None

    @classmethod
    def get_by_id(cls, group_id: str) -> Optional['Grupo']:
        """HU4: Carga por ID."""
        group_data = cls._db.get_entity_by_id('grupos', group_id)
        if group_data:
            return cls(**group_data)
        return None

    @classmethod
    def get_all(cls) -> list['Grupo']:
        """HU4: Lista todos grupos."""
        groups_data = cls._db.get_all_entities('grupos')
        return [cls(**g) for g in groups_data]

    def update(self, updates: Dict) -> bool:
        """HU4: Actualiza."""
        if not self.id:
            return False
        updates['updated_at'] = None
        return self._db.update_entity('grupos', self.id, updates)

    def delete(self) -> bool:
        """HU4: Desactiva."""
        if not self.id:
            return False
        return self.update({'activo': False})

    def es_activo(self):
        return self.activo
