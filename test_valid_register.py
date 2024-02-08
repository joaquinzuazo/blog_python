import unittest
from unittest.mock import patch, MagicMock

from valid_register import valid_form

class TestValidFormRegister(unittest.TestCase):
    def test_valid_form_user_exist(self):
        mock_respuesta = MagicMock()
        mock_respuesta.get_user_by_username.return_value = True
        orm_mock = mock_respuesta
        result, mensaje = valid_form(
            orm_mock,
            username="Juan",
            password="123456"
        )
        self.assertFalse(result)
        self.assertEqual(mensaje, "El username ya existe")

    def test_valid_form_user_not_exist(self):
        mock_respuesta = MagicMock()
        mock_respuesta.get_user_by_username.return_value = False
        orm_mock = mock_respuesta
        result, mensaje = valid_form(
            orm_mock,
            username="Juan",
            password="123456"
        )
        self.assertTrue(result)
        self.assertEqual(mensaje, "Formulario valido")