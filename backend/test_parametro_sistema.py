import unittest
from models import ParametroSistema

class TestParametroSistema(unittest.TestCase):
    def setUp(self):
        """Cleanup tabla 'parametros' antes de cada test (aisla estado)."""
        ParametroSistema._db.data['parametros'] = []  # Reset in-memory
        # Nota: En real, usa temp dir o rollback, pero simple para dev

    def test_creacion_valida(self):
        """HU19: Crea con clave única."""
        valor = {"periodo": "2025", "dias": ["Lun-Vie"]}
        param = ParametroSistema.create("periodo_academico", valor, "global")
        self.assertIsNotNone(param)
        self.assertEqual(param.clave, "periodo_academico")
        self.assertTrue(param.es_activo())

    def test_creacion_invalida(self):
        """HU19: Falla sin clave."""
        param = ParametroSistema.create("", {})  # Dummy valor para test inválido (empty clave)
        self.assertIsNone(param)

    def test_desactivar(self):
        """HU19: Desactiva persistente."""
        valor = {"horas": "8-18"}
        param = ParametroSistema.create("horas_laborables", valor)
        self.assertIsNotNone(param)
        self.assertTrue(param.delete())
        loaded = ParametroSistema.get_by_id(param.id)
        self.assertIsNotNone(loaded)
        self.assertFalse(loaded.es_activo())

if __name__ == '__main__':
    unittest.main()
