import unittest
from models import Asignacion

class TestAsignacion(unittest.TestCase):
    def test_creacion_valida(self):
        """HU11: Crea con IDs FKs."""
        asignacion = Asignacion.create("grupo-uuid", "salon-uuid", "prof-uuid", "bloque-uuid", "periodo-uuid", 'Manual', "user-uuid")
        self.assertIsNotNone(asignacion)
        self.assertEqual(asignacion.origen, 'Manual')
        self.assertTrue(asignacion.es_activo())

    def test_creacion_invalida(self):
        """HU11: Falla sin FKs."""
        asignacion = Asignacion.create("", "", "", "", "")
        self.assertIsNone(asignacion)

    def test_desactivar(self):
        """HU12: Desactiva persistente."""
        asignacion = Asignacion.create("g1", "s1", "p1", "b1", "per1", 'Manual')
        self.assertIsNotNone(asignacion)
        self.assertTrue(asignacion.delete())
        loaded = Asignacion.get_by_id(asignacion.id)
        self.assertIsNotNone(loaded)
        self.assertFalse(loaded.es_activo())

if __name__ == '__main__':
    unittest.main()
