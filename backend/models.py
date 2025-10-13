import uuid
import hashlib
from typing import Optional, Dict
from database import DatabaseManager  # Importa para integración

class Usuario:
    _db = DatabaseManager()  # Instancia global para simplicidad

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
        """HU1: Crea usuario persistente (integra DB genérica)."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user_data = {
            'nombre': nombre,
            'email': email,
            'password_hash': password_hash,
            'rol': rol,
            'activo': True
        }
        user_id = cls._db.create_entity('usuarios', user_data, ['email'])  # Genérico con unique 'email'
        if user_id:
            user_data['id'] = user_id
            return cls(**user_data)
        return None  # Fallo: email duplicado

    @classmethod
    def get_by_email(cls, email: str) -> Optional['Usuario']:
        """HU2: Carga desde DB por email (usa genérico get_all + filter)."""
        for user_data in cls._db.get_all_entities('usuarios'):
            if user_data['email'] == email:
                return cls(**user_data)
        return None

    @classmethod
    def autenticar(cls, email: str, password: str) -> bool:
        """HU2: Refactor: Usa DB para validar (carga por email genérica)."""
        user = cls.get_by_email(email)
        if not user:
            return False
        if not user.activo:
            return False
        expected_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.password_hash == expected_hash

    def update(self, updates: Dict) -> bool:
        """HU1: Actualiza persistente (genérica)."""
        if not self.id:
            return False
        updates['updated_at'] = None
        return self._db.update_entity('usuarios', self.id, updates)

    def delete(self) -> bool:
        """HU1: Desactiva persistente (genérica)."""
        if not self.id:
            return False
        return self._db.update_entity('usuarios', self.id, {'activo': False})

    def set_password(self, password: str):
        """Hash y actualiza (integra update genérica)."""
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

    @classmethod
    def update_by_id(cls, group_id: str, updates: Dict) -> bool:
        """Update by ID (para API)."""
        group_data = cls._db.get_entity_by_id('grupos', group_id)
        if group_data:
            return cls._db.update_entity('grupos', group_id, updates)
        return False

    @classmethod
    def delete_by_id(cls, group_id: str) -> bool:
        """Delete by ID (soft)."""
        return cls._db.delete_entity('grupos', group_id)        

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

class Salon:
    _db = DatabaseManager()  # Usa global para todas tablas

    def __init__(self, id=None, codigo=None, capacidad=None, ubicacion=None, activo=True, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.codigo = codigo  # VARCHAR(60) UK
        self.capacidad = capacidad  # INT >0
        self.ubicacion = ubicacion  # VARCHAR(160)
        self.activo = activo  # TINYINT(1)
        self.created_at = created_at or None
        self.updated_at = updated_at or None

    @classmethod
    def create(cls, codigo: str, capacidad: int, ubicacion: str) -> Optional['Salon']:
        """HU5: Crea salón persistente (valida capacidad >0, codigo único)."""
        if capacidad <= 0:
            return None  # Simula CHECK
        salon_data = {
            'codigo': codigo,
            'capacidad': capacidad,
            'ubicacion': ubicacion,
            'activo': True
        }
        salon_id = cls._db.create_entity('salones', salon_data, ['codigo'])  # Unique 'codigo'
        if salon_id:
            salon_data['id'] = salon_id
            return cls(**salon_data)
        return None  # Fallo: codigo duplicado

    @classmethod
    def get_by_id(cls, salon_id: str) -> Optional['Salon']:
        """HU6: Carga por ID."""
        salon_data = cls._db.get_entity_by_id('salones', salon_id)
        if salon_data:
            return cls(**salon_data)
        return None

    @classmethod
    def get_all(cls) -> list['Salon']:
        """HU6: Lista todos salones."""
        salones_data = cls._db.get_all_entities('salones')
        return [cls(**s) for s in salones_data]

    @classmethod
    def update_by_id(cls, salon_id: str, updates: Dict) -> bool:
        """Update by ID (para API)."""
        salon_data = cls._db.get_entity_by_id('salones', salon_id)
        if salon_data:
            return cls._db.update_entity('salones', salon_id, updates)
        return False

    @classmethod
    def delete_by_id(cls, salon_id: str) -> bool:
        """Delete by ID (soft)."""
        return cls._db.delete_entity('salones', salon_id)

    def update(self, updates: Dict) -> bool:
        """HU6: Actualiza."""
        if not self.id:
            return False
        updates['updated_at'] = None
        return self._db.update_entity('salones', self.id, updates)

    def delete(self) -> bool:
        """HU6: Desactiva."""
        if not self.id:
            return False
        return self.update({'activo': False})

    def es_activo(self):
        return self.activo

