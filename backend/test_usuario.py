import unittest
from models import Usuario  # Importa la clase (ajusta si es necesario)

class TestUsuario(unittest.TestCase):
    def setUp(self):
        """Prepara instancia para cada test (TDD: setup limpio)."""
        self.usuario = Usuario(
            nombre="Admin Test",
            email="admin@test.com",
            rol="ADMIN",
            activo=True
        )
        self.usuario.set_password("password123")  # Hash inicial

    def test_creacion_y_get_rol(self):
        """Prueba creación y getter (HU1: gestionar usuarios)."""
        self.assertEqual(self.usuario.nombre, "Admin Test")
        self.assertEqual(self.usuario.email, "admin@test.com")
        self.assertEqual(self.usuario.get_rol(), "ADMIN")
        self.assertTrue(self.usuario.es_activo())

    def test_autenticacion_exitosa(self):
        """Prueba HU2: auth válida."""
        self.assertTrue(self.usuario.autenticar("admin@test.com", "password123"))

    def test_autenticacion_fallida_email(self):
        """Prueba auth fallida por email (HU2: inválida)."""
        self.assertFalse(self.usuario.autenticar("wrong@test.com", "password123"))

    def test_autenticacion_fallida_password(self):
        """Prueba auth fallida por password (HU2: inválida)."""
        self.assertFalse(self.usuario.autenticar("admin@test.com", "wrongpass"))

    def test_usuario_inactivo(self):
        """Prueba desactivación (HU1: desactivar cuenta)."""
        self.usuario.activo = False
        self.assertFalse(self.usuario.autenticar("admin@test.com", "password123"))
        self.assertFalse(self.usuario.es_activo())

if __name__ == '__main__':
    unittest.main()
    