import unittest
from calculadora import suma, dividir

class TestSuma(unittest.TestCase):
    def test_suma_sucess(self):
        self.assertEqual(suma(5,5),10,"Error en test")
        self.assertEqual(suma(1,15),16,"Error en test")
        # assertEqual => assert suma(1,15)==16

    def test_suma_failed(self):
        self.assertNotEqual(suma(1,15),20,"Error de test")
        # assertNotEqual => assert suma(1,15) != 20

class TestDividir(unittest.TestCase):
    def test_dividir_sucess(self):
        self.assertEqual(dividir(15,3),5,"Error en test")

    def test_exception_sucess(self):
        with self.assertRaises(ZeroDivisionError):
            dividir(10, 0)