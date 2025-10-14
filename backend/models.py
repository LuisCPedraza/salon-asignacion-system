import uuid
import hashlib
from typing import List, Optional, Dict
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

class Profesor:
    _db = DatabaseManager()  # Usa global para todas tablas

    def __init__(self, id=None, usuario_id=None, especialidades=None, hoja_vida_url=None, activo=True, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.usuario_id = usuario_id  # FK UK a usuario.id (rol PROFESOR)
        self.especialidades = especialidades  # TEXT
        self.hoja_vida_url = hoja_vida_url  # VARCHAR(255)
        self.activo = activo  # TINYINT(1)
        self.created_at = created_at or None
        self.updated_at = updated_at or None

    @classmethod
    def create(cls, usuario_id: str, especialidades: str = '', hoja_vida_url: str = '') -> Optional['Profesor']:
        """HU7: Crea profesor persistente (valida usuario_id existe y rol PROFESOR)."""
        # Stub valida: Asume usuario_id válido (futuro query Usuario.get_by_id, rol == 'PROFESOR')
        if not usuario_id:
            return None
        profesor_data = {
            'usuario_id': usuario_id,
            'especialidades': especialidades,
            'hoja_vida_url': hoja_vida_url,
            'activo': True
        }
        profesor_id = cls._db.create_entity('profesores', profesor_data, ['usuario_id'])  # Unique 'usuario_id'
        if profesor_id:
            profesor_data['id'] = profesor_id
            return cls(**profesor_data)
        return None  # Fallo: usuario_id duplicado

    @classmethod
    def get_by_id(cls, profesor_id: str) -> Optional['Profesor']:
        """HU8: Carga por ID."""
        profesor_data = cls._db.get_entity_by_id('profesores', profesor_id)
        if profesor_data:
            return cls(**profesor_data)
        return None

    @classmethod
    def get_all(cls) -> list['Profesor']:
        """HU8: Lista todos profesores."""
        profesores_data = cls._db.get_all_entities('profesores')
        return [cls(**p) for p in profesores_data]

    @classmethod
    def update_by_id(cls, profesor_id: str, updates: Dict) -> bool:
        """Update by ID (para API)."""
        profesor_data = cls._db.get_entity_by_id('profesores', profesor_id)
        if profesor_data:
            return cls._db.update_entity('profesores', profesor_id, updates)
        return False

    @classmethod
    def delete_by_id(cls, profesor_id: str) -> bool:
        """Delete by ID (soft)."""
        return cls._db.delete_entity('profesores', profesor_id)

    def update(self, updates: Dict) -> bool:
        """HU8: Actualiza."""
        if not self.id:
            return False
        updates['updated_at'] = None
        return self._db.update_entity('profesores', self.id, updates)

    def delete(self) -> bool:
        """HU8: Desactiva."""
        if not self.id:
            return False
        return self.update({'activo': False})

    def es_activo(self):
        return self.activo

class ParametroSistema:
    _db = DatabaseManager()  # Usa global para todas tablas

    def __init__(self, id=None, clave=None, valor=None, scope=None, activo=True, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.clave = clave  # VARCHAR(120) UK
        self.valor = valor  # JSON
        self.scope = scope  # VARCHAR(60)
        self.activo = activo  # TINYINT(1)
        self.created_at = created_at or None
        self.updated_at = updated_at or None

    @classmethod
    def create(cls, clave: str, valor: Dict, scope: str = '') -> Optional['ParametroSistema']:
        """HU19: Crea parámetro persistente (valida clave única)."""
        if not clave:
            return None
        param_data = {
            'clave': clave,
            'valor': valor,
            'scope': scope,
            'activo': True
        }
        param_id = cls._db.create_entity('parametros', param_data, ['clave'])  # Unique 'clave'
        if param_id:
            param_data['id'] = param_id
            return cls(**param_data)
        return None  # Fallo: clave duplicada

    @classmethod
    def get_by_id(cls, param_id: str) -> Optional['ParametroSistema']:
        """HU19: Carga por ID."""
        param_data = cls._db.get_entity_by_id('parametros', param_id)
        if param_data:
            return cls(**param_data)
        return None

    @classmethod
    def get_all(cls) -> list['ParametroSistema']:
        """HU19: Lista todos parámetros."""
        params_data = cls._db.get_all_entities('parametros')
        return [cls(**p) for p in params_data]

    @classmethod
    def update_by_id(cls, param_id: str, updates: Dict) -> bool:
        """Update by ID (para API)."""
        param_data = cls._db.get_entity_by_id('parametros', param_id)
        if param_data:
            return cls._db.update_entity('parametros', param_id, updates)
        return False

    @classmethod
    def delete_by_id(cls, param_id: str) -> bool:
        """Delete by ID (soft)."""
        return cls._db.delete_entity('parametros', param_id)

    def update(self, updates: Dict) -> bool:
        """HU19: Actualiza."""
        if not self.id:
            return False
        updates['updated_at'] = None
        return self._db.update_entity('parametros', self.id, updates)

    def delete(self) -> bool:
        """HU19: Desactiva."""
        if not self.id:
            return False
        return self.update({'activo': False})

    def es_activo(self):
        return self.activo

class Asignacion:
    _db = DatabaseManager()  # Usa global para todas tablas

    def __init__(self, id=None, grupo_id=None, salon_id=None, profesor_id=None, bloque_id=None, periodo_id=None, estado='Propuesta', origen='Manual', score=0.0, created_by=None, activo=True, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.grupo_id = grupo_id  # FK grupo.id
        self.salon_id = salon_id  # FK salon.id
        self.profesor_id = profesor_id  # FK profesor.id
        self.bloque_id = bloque_id  # FK bloque_horario.id
        self.periodo_id = periodo_id  # FK periodo_academico.id
        self.estado = estado  # ENUM 'Propuesta/Confirmada/Anulada'
        self.origen = origen  # ENUM 'Manual/Automática'
        self.score = score  # FLOAT
        self.created_by = created_by  # FK usuario.id
        self.activo = activo  # TINYINT(1)
        self.created_at = created_at or None
        self.updated_at = updated_at or None

    @classmethod
    def create(cls, grupo_id: str, salon_id: str, profesor_id: str, bloque_id: str, periodo_id: str, origen: str = 'Manual', created_by: str = '') -> Optional['Asignacion']:
        """HU11: Crea asignación manual (stub valida FKs existen)."""
        # Stub valida: Asume IDs válidos (futuro query models)
        if not all([grupo_id, salon_id, profesor_id, bloque_id, periodo_id]):
            return None
        asignacion_data = {
            'grupo_id': grupo_id,
            'salon_id': salon_id,
            'profesor_id': profesor_id,
            'bloque_id': bloque_id,
            'periodo_id': periodo_id,
            'estado': 'Propuesta',
            'origen': origen,
            'score': 0.0,
            'created_by': created_by,
            'activo': True
        }
        asignacion_id = cls._db.create_entity('asignaciones', asignacion_data, [])  # No unique por doc (futuro UNIQUE grupo/bloque/periodo)
        if asignacion_id:
            asignacion_data['id'] = asignacion_id
            return cls(**asignacion_data)
        return None

    @classmethod
    def get_by_id(cls, asignacion_id: str) -> Optional['Asignacion']:
        """HU12: Carga por ID."""
        asignacion_data = cls._db.get_entity_by_id('asignaciones', asignacion_id)
        if asignacion_data:
            return cls(**asignacion_data)
        return None

    @classmethod
    def get_all(cls) -> list['Asignacion']:
        """HU12: Lista todas asignaciones."""
        asignaciones_data = cls._db.get_all_entities('asignaciones')
        return [cls(**a) for a in asignaciones_data]

    @classmethod
    def update_by_id(cls, asignacion_id: str, updates: Dict) -> bool:
        """Update by ID (para API)."""
        asignacion_data = cls._db.get_entity_by_id('asignaciones', asignacion_id)
        if asignacion_data:
            return cls._db.update_entity('asignaciones', asignacion_id, updates)
        return False  

    @classmethod
    def delete_by_id(cls, asignacion_id: str) -> bool:
        """Delete by ID (soft)."""
        return cls._db.delete_entity('asignaciones', asignacion_id)
    
    @classmethod
    def auto_assign(cls, parametros_prioridades: Dict = None) -> List[str]:
        """HU9-HU10: Algoritmo automático stub (random matching con score, considera cap/disponibilidad stub)."""
        if parametros_prioridades is None:
            parametros_prioridades = {"prioridad_cap": 0.5, "prioridad_prox": 0.3, "minimizar_cambios": True}  # Stub from /parametros

        # Stub: Get active data (futuro filter disponibilidad)
        grupos = Grupo.get_all()
        salones = Salon.get_all()
        profesores = Profesor.get_all()

        active_grupos = [g for g in grupos if g.es_activo()]
        active_salones = [s for s in salones if s.es_activo()]
        active_profesores = [p for p in profesores if p.es_activo()]

        if not (active_grupos and active_salones and active_profesores):
            return []  # No data

        asign_ids = []
        import random  # Stdlib for stub random

        for grupo in active_grupos:
            # Stub random assign (futuro optimización con prioridades, e.g., sort by score)
            salon = random.choice(active_salones)
            profesor = random.choice(active_profesores)
            if grupo.num_estudiantes <= salon.capacidad:  # Considera capacidad
                # Stub bloque/periodo (futuro from parametros)
                dummy_bloque = 'dummy-bloque-uuid'
                dummy_periodo = 'dummy-periodo-uuid'
                dummy_created_by = 'auto-system'
                score = random.uniform(0, 1) * parametros_prioridades["prioridad_cap"]  # Stub score

                asignacion = cls.create(grupo.id, salon.id, profesor.id, dummy_bloque, dummy_periodo, 'Automática', dummy_created_by)
                if asignacion:
                    asignacion.score = score
                    asignacion.update({'score': score})
                    asign_ids.append(asignacion.id)
            else:
                # Skip if no match (futuro conflict log)
                pass

        return asign_ids  # Return IDs created    

    def update(self, updates: Dict) -> bool:
        """HU12: Actualiza (e.g., confirmar estado)."""
        if not self.id:
            return False
        updates['updated_at'] = None
        return self._db.update_entity('asignaciones', self.id, updates)

    def delete(self) -> bool:
        """HU12: Desactiva."""
        if not self.id:
            return False
        return self.update({'activo': False})

    def es_activo(self):
        return self.activo
