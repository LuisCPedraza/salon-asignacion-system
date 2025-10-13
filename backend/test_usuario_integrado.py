import unittest
from models import Usuario

class TestUsuarioIntegrado(unittest.TestCase):
    def setUp(self):
        # Crea instancia de DB para test y reemplaza la global de Usuario (isola estado)
        from database import DatabaseManager
        self.test_db = DatabaseManager('db_data/test_usuarios_integrado.json')
        self.test_db.data = []  # Reset in-memory
        self.original_db = Usuario._db  # Backup global
        Usuario._db = self.test_db  # Patch para este test run

    def tearDown(self):
        # Restaura global post-test (buena práctica para aislamiento)
        Usuario._db = self.original_db

    def test_create_y_autenticar(self):
        """HU1+HU2: Crea persistente y auth."""
        user = Usuario.create("Test User", "test@int.com", "pass123", "ADMIN")
        self.assertIsNotNone(user)
        self.assertTrue(Usuario.autenticar("test@int.com", "pass123"))
        self.assertEqual(user.get_rol(), "ADMIN")

    def test_autenticar_fallido(self):
        """HU2: Fallo con usuario existente."""
        Usuario.create("Test", "fail@test.com", "pass", "ADMIN")
        self.assertFalse(Usuario.autenticar("fail@test.com", "wrong"))
        self.assertFalse(Usuario.autenticar("nonexist@test.com", "pass"))

    def test_update_delete(self):
        """HU1: Actualiza y desactiva."""
        user = Usuario.create("Update", "update@test.com", "pass", "ADMIN")
        self.assertIsNotNone(user)  # Asegura create OK antes de update
        self.assertTrue(user.update({'nombre': 'Updated'}))
        loaded = Usuario.get_by_email("update@test.com")
        self.assertEqual(loaded.nombre, 'Updated')
        self.assertTrue(user.delete())
        loaded = Usuario.get_by_email("update@test.com")
        self.assertFalse(loaded.es_activo())

if __name__ == '__main__':
    unittest.main()
    