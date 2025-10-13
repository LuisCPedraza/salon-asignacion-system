import unittest
from models import Grupo

class TestGrupo(unittest.TestCase):
    def test_creacion_valida(self):
        """HU3: Crea con num_estudiantes >0."""
        group = Grupo.create("Grupo A", "Primaria", 25, "Especial")
        self.assertIsNotNone(group)
        self.assertEqual(group.nombre, "Grupo A")
        self.assertTrue(group.es_activo())

    def test_creacion_invalida(self):
        """HU3: Falla num_estudiantes <=0."""
        group = Grupo.create("Grupo B", "Secundaria", 0)
        self.assertIsNone(group)

    def test_desactivar(self):
            """HU4: Desactiva persistente."""
            group = Grupo.create("Grupo C", "Bachillerato", 30)
            self.assertIsNotNone(group)
            self.assertTrue(group.delete())
            loaded = Grupo.get_by_id(group.id)
            self.assertIsNotNone(loaded)
            self.assertFalse(loaded.es_activo())

if __name__ == '__main__':
    unittest.main()
