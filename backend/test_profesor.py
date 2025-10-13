import unittest
from models import Profesor

class TestProfesor(unittest.TestCase):
    def test_creacion_valida(self):
        """HU7: Crea con usuario_id válido."""
        profesor = Profesor.create("test-uuid", "Matemáticas", "https://hoja-vida.com")
        self.assertIsNotNone(profesor)
        self.assertEqual(profesor.usuario_id, "test-uuid")
        self.assertTrue(profesor.es_activo())

    def test_creacion_invalida(self):
        """HU7: Falla sin usuario_id."""
        profesor = Profesor.create("")
        self.assertIsNone(profesor)

    def test_desactivar(self):
        """HU8: Desactiva persistente."""
        profesor = Profesor.create("test-uuid2", "Historia")
        self.assertIsNotNone(profesor)
        self.assertTrue(profesor.delete())
        loaded = Profesor.get_by_id(profesor.id)
        self.assertIsNotNone(loaded)
        self.assertFalse(loaded.es_activo())

if __name__ == '__main__':
    unittest.main()
