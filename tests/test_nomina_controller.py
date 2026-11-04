import unittest
from unittest.mock import patch
from uuid import UUID, uuid4

from src.controller.entorno_pruebas import EntornoPruebasNomina
from src.controller.nomina_controller import NominaController
from src.model.datos_nomina import DatosNomina
from src.model.errores import (
    ErrorDatosNominaInvalidos,
    ErrorIdNominaInvalido,
    ErrorNominaDuplicada,
    ErrorNominaNoEncontrada,
    ErrorTablaNominaExistente,
    ErrorTablaNominaNoExiste,
)


class TestNominaController(unittest.TestCase):

    def setUp(self):
        """Fixture: prepara una tabla aislada antes de cada prueba."""
        self.entorno = EntornoPruebasNomina()
        self.entorno.crear()

        # Los cleanups se ejecutan en orden inverso:
        # primero termina el parche y luego elimina el esquema.
        self.addCleanup(self.entorno.eliminar)

        parche = patch.object(
            NominaController,
            "conectar",
            side_effect=self.entorno.conectar,
        )
        parche.start()
        self.addCleanup(parche.stop)

        NominaController.crear_tablas()

    @staticmethod
    def nueva_nomina(**cambios):
        datos = {
            "salario": 3000000,
            "dias": 30,
            "bonificacion": 200000,
            "comision": 100000,
            "descuentos": 50000,
        }
        datos.update(cambios)
        return DatosNomina(**datos)

    # INSERTAR Y BUSCAR: CASOS NORMALES

    def test_insertar_y_buscar_nomina(self):
        nomina = self.nueva_nomina()
        id_original = nomina.id_nomina

        self.assertIsInstance(id_original, str)
        self.assertEqual(UUID(id_original).version, 4)

        id_guardado = NominaController.insertar(nomina)

        self.assertEqual(id_guardado, id_original)

        # Insertar cierra su conexión. Buscar abre otra:
        # esto comprueba que el registro quedó confirmado.
        encontrada = NominaController.buscar(id_guardado)

        self.assertIsInstance(encontrada, DatosNomina)
        self.assertEqual(encontrada, nomina)

    def test_insertar_nomina_con_centavos(self):
        nomina = self.nueva_nomina(
            salario=2500000.75,
            bonificacion=150000.25,
            comision=0,
            descuentos=10000.50,
        )

        id_guardado = NominaController.insertar(nomina)
        encontrada = NominaController.buscar(id_guardado)

        self.assertEqual(encontrada, nomina)

    def test_buscar_nomina_correcta_entre_varias(self):
        primera = self.nueva_nomina(salario=2000000)
        segunda = self.nueva_nomina(salario=4000000)

        NominaController.insertar(primera)
        NominaController.insertar(segunda)

        encontrada = NominaController.buscar(segunda.id_nomina)

        self.assertEqual(encontrada, segunda)
        self.assertNotEqual(encontrada.id_nomina, primera.id_nomina)

    # INSERTAR Y BUSCAR: CASOS DE ERROR

    def test_insertar_salario_negativo(self):
        nomina = self.nueva_nomina(salario=-100)

        with self.assertRaises(ErrorDatosNominaInvalidos):
            NominaController.insertar(nomina)

        # El registro rechazado no debe quedar guardado.
        with self.assertRaises(ErrorNominaNoEncontrada):
            NominaController.buscar(nomina.id_nomina)

    def test_insertar_dias_fuera_de_rango(self):
        nomina = self.nueva_nomina(dias=31)

        with self.assertRaises(ErrorDatosNominaInvalidos):
            NominaController.insertar(nomina)

        with self.assertRaises(ErrorNominaNoEncontrada):
            NominaController.buscar(nomina.id_nomina)

    def test_insertar_id_duplicado(self):
        original = self.nueva_nomina()
        NominaController.insertar(original)

        duplicada = self.nueva_nomina(
            id_nomina=original.id_nomina,
            salario=5000000,
        )

        with self.assertRaises(ErrorNominaDuplicada):
            NominaController.insertar(duplicada)

        # El intento fallido no debe modificar el registro original.
        encontrada = NominaController.buscar(original.id_nomina)
        self.assertEqual(encontrada, original)

    def test_buscar_nomina_inexistente(self):
        with self.assertRaises(ErrorNominaNoEncontrada):
            NominaController.buscar(str(uuid4()))

    def test_buscar_id_con_formato_invalido(self):
        with self.assertRaises(ErrorIdNominaInvalido):
            NominaController.buscar("esto-no-es-un-uuid")

    # CREAR TABLAS: CASO NORMAL Y DE ERROR

    def test_crear_tablas(self):
        NominaController.borrar_tablas()
        NominaController.crear_tablas()

        nomina = self.nueva_nomina()
        NominaController.insertar(nomina)

        encontrada = NominaController.buscar(nomina.id_nomina)
        self.assertEqual(encontrada, nomina)

    def test_crear_tablas_existentes(self):
        with self.assertRaises(ErrorTablaNominaExistente):
            NominaController.crear_tablas()

        # La tabla existente debe seguir siendo utilizable.
        nomina = self.nueva_nomina()
        NominaController.insertar(nomina)

        self.assertEqual(
            NominaController.buscar(nomina.id_nomina),

            nomina,
        )


    # BORRAR TABLAS: CASO NORMAL Y DE ERROR

    def test_borrar_tablas(self):
        nomina = self.nueva_nomina()
        NominaController.insertar(nomina)

        NominaController.borrar_tablas()
        


        with self.assertRaises(ErrorTablaNominaNoExiste):
            NominaController.buscar(nomina.id_nomina)

    def test_borrar_tablas_inexistentes(self):
        NominaController.borrar_tablas()

        with self.assertRaises(ErrorTablaNominaNoExiste):
            NominaController.borrar_tablas()


if __name__ == "__main__":
    unittest.main()