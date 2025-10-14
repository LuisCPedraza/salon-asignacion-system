import unittest
from models import Asignacion, Grupo, Salon, Profesor

class TestAsignacionAuto(unittest.TestCase):
    def setUp(self):
        # Cleanup tablas para test
        Asignacion._db.data['asignaciones'] = []
        Grupo._db.data['grupos'] = []
        Salon._db.data['salones'] = []
        Profesor._db.data['profesores'] = []

        # Dummy data for test
        Grupo.create("G1", "Primaria", 20)
        Salon.create("S1", 30, "A")
        Profesor.create("U1", "Matemáticas")

    def test_auto_assign_basico(self):
        """HU9: Auto-assign stub crea asignaciones random con score."""
        ids = Asignacion.auto_assign()
        self.assertGreater(len(ids), 0)  # Al menos 1 asignación
        self.assertIsInstance(ids[0], str)  # ID UUID

        # Check created in DB
        all_asign = Asignacion.get_all()
        self.assertEqual(len(all_asign), len(ids))
        self.assertEqual(all_asign[0].origen, 'Automática')
        self.assertGreaterEqual(all_asign[0].score, 0)

    def test_auto_assign_con_prioridades(self):
        """HU10: Usa parametros_prioridades para score."""
        priors = {"prioridad_cap": 0.8}
        ids = Asignacion.auto_assign(priors)
        self.assertGreater(len(ids), 0)
        all_asign = Asignacion.get_all()
        self.assertGreater(all_asign[0].score, 0)  # Score >0 con prioridad

if __name__ == '__main__':
    unittest.main()
