import unittest
import json
from database import DatabaseManager  # Ajusta import

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager('db_data/test_usuarios.json')
        self.db.data = []  # Limpia para test

    def test_create_user_exitoso(self):
        """HU1: Crea con email único."""
        user_data = {'nombre': 'Test', 'email': 'test@test.com', 'password_hash': 'hash', 'rol': 'ADMIN', 'activo': True}
        user_id = self.db.create_user(user_data)
        self.assertIsNotNone(user_id)
        loaded = self.db.get_user_by_email('test@test.com')
        self.assertEqual(loaded['nombre'], 'Test')

    def test_create_user_duplicado(self):
        """HU1: Falla por email duplicado (UK simulado)."""
        user_data = {'nombre': 'Test', 'email': 'dup@test.com', 'password_hash': 'hash', 'rol': 'ADMIN', 'activo': True}
        self.db.create_user(user_data)
        user_id = self.db.create_user(user_data)
        self.assertIsNone(user_id)

    def test_update_y_delete(self):
        """HU1: Actualiza y desactiva."""
        user_data = {'nombre': 'UpdateTest', 'email': 'update@test.com', 'password_hash': 'hash', 'rol': 'ADMIN', 'activo': True}
        user_id = self.db.create_user(user_data)
        self.assertTrue(self.db.update_user(user_id, {'nombre': 'Updated'}))
        loaded = self.db.get_user_by_email('update@test.com')
        self.assertEqual(loaded['nombre'], 'Updated')
        self.assertTrue(self.db.delete_user(user_id))
        loaded = self.db.get_user_by_email('update@test.com')
        self.assertFalse(loaded['activo'])

if __name__ == '__main__':
    unittest.main()
    