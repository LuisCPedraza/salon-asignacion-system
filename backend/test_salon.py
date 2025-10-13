import unittest
from models import Salon

class TestSalon(unittest.TestCase):
    def test_creacion_valida(self):
        """HU5: Crea con capacidad >0, codigo único."""
        salon = Salon.create("S101", 30, "Edificio A")
        self.assertIsNotNone(salon)
        self.assertEqual(salon.codigo, "S101")
        self.assertTrue(salon.es_activo())

    def test_creacion_invalida(self):
        """HU5: Falla capacidad <=0."""
        salon = Salon.create("S102", 0, "Edificio B")
        self.assertIsNone(salon)

    def test_desactivar(self):
        """HU6: Desactiva persistente."""
        salon = Salon.create("S103", 40, "Edificio C")
        self.assertIsNotNone(salon)
        self.assertTrue(salon.delete())
        loaded = Salon.get_by_id(salon.id)
        self.assertIsNotNone(loaded)
        self.assertFalse(loaded.es_activo())

if __name__ == '__main__':
    unittest.main()
