import uuid
import hashlib

class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password_hash=None, rol=None, activo=True, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())  # Simula CHAR(36) UUID
        self.nombre = nombre  # VARCHAR(120)
        self.email = email  # VARCHAR(160), UNIQUE en BD real
        self.password_hash = password_hash  # VARCHAR(255), hashed
        self.rol = rol  # ENUM: 'ADMIN', 'COORDINADOR', 'PROFESOR', 'coord_INFRA'
        self.activo = activo  # TINYINT(1)
        self.created_at = created_at or None  # DATETIME
        self.updated_at = updated_at or None  # DATETIME

    def autenticar(self, email, password):
        """Método para HU2: Valida credenciales. Retorna True si coincide."""
        if not self.email == email or not self.activo:
            return False
        # Simula hash check (en real: bcrypt; aquí simple para vanilla)
        expected_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.password_hash == expected_hash

    def set_password(self, password):
        """Hash simple para nueva contraseña (HU1: crear/editar)."""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.updated_at = None  # Se seteará en BD

    def get_rol(self):
        """Getter para rol (usado en flujos por rol, e.g., DFD)."""
        return self.rol

    def es_activo(self):
        """Verifica si activo (para validaciones)."""
        return self.activo
    