import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from uuid import UUID, uuid4

import psycopg2
from psycopg2 import sql

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from model.datos_nomina import DatosNomina
from controller.nomina_controller import NominaController


class TestNominaController(unittest.TestCase):

    def setUp(self):
        self.esquema = "test_nomina_" + uuid4().hex
        self.conectar_original = NominaController.conectar

        conexion = self.conectar_original()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("CREATE SCHEMA {}").format(
                            sql.Identifier(self.esquema)
                        )
                    )
        finally:
            conexion.close()

        self.addCleanup(self.eliminar_esquema)

        parche = patch.object(
            NominaController,
            "conectar",
            side_effect=self.conectar_prueba,
        )
        parche.start()
        self.addCleanup(parche.stop)

        NominaController.crear_tablas()

    def conectar_prueba(self):
        conexion = self.conectar_original()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("SET search_path TO {}").format(
                            sql.Identifier(self.esquema)
                        )
                    )

            return conexion

        except Exception:
            conexion.close()
            raise

    def eliminar_esquema(self):
        conexion = self.conectar_original()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("DROP SCHEMA {} CASCADE").format(
                            sql.Identifier(self.esquema)
                        )
                    )
        finally:
            conexion.close()

    def nueva_nomina(self, **cambios):
        datos = {
            "salario": 3000000,
            "dias": 30,
            "bonificacion": 200000,
            "comision": 100000,
            "descuentos": 50000,
        }
        datos.update(cambios)
        return DatosNomina(**datos)

    def cantidad_registros(self):
        conexion = NominaController.conectar()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM nominas;"
                    )
                    return cursor.fetchone()[0]
        finally:
            conexion.close()

    # INSERTAR Y BUSCAR: CASOS NORMALES

    def test_insertar_y_buscar_nomina(self):
        nomina = self.nueva_nomina()

        # El identificador existe antes de insertar.
        id_original = nomina.id_nomina

        self.assertIsInstance(id_original, str)
        self.assertEqual(UUID(id_original).version, 4)

        id_guardado = NominaController.insertar(nomina)

        # La base de datos conserva el ID generado en Python.
        self.assertEqual(id_guardado, id_original)

        encontrada = NominaController.buscar(id_guardado)

        self.assertIsInstance(encontrada, DatosNomina)
        self.assertEqual(nomina, encontrada)

    def test_insertar_nomina_con_centavos(self):
        nomina = self.nueva_nomina(
            salario=2500000.75,
            bonificacion=150000.25,
            comision=0,
            descuentos=10000.50,
        )

        id_guardado = NominaController.insertar(nomina)
        encontrada = NominaController.buscar(id_guardado)

        self.assertEqual(nomina, encontrada)

    def test_buscar_nomina_correcta_entre_varias(self):
        primera = self.nueva_nomina(salario=2000000)
        segunda = self.nueva_nomina(salario=4000000)

        self.assertNotEqual(
            primera.id_nomina,
            segunda.id_nomina,
        )

        NominaController.insertar(primera)
        NominaController.insertar(segunda)

        encontrada = NominaController.buscar(
            segunda.id_nomina
        )

        self.assertEqual(segunda, encontrada)

    # INSERTAR Y BUSCAR: CASOS DE ERROR

    def test_insertar_salario_negativo(self):
        nomina = self.nueva_nomina(salario=-100)

        with self.assertRaises(
            psycopg2.errors.CheckViolation
        ):
            NominaController.insertar(nomina)

        self.assertEqual(self.cantidad_registros(), 0)

    def test_insertar_dias_fuera_de_rango(self):
        nomina = self.nueva_nomina(dias=31)

        with self.assertRaises(
            psycopg2.errors.CheckViolation
        ):
            NominaController.insertar(nomina)

        self.assertEqual(self.cantidad_registros(), 0)

    def test_insertar_id_duplicado(self):
        nomina = self.nueva_nomina()

        NominaController.insertar(nomina)

        with self.assertRaises(
            psycopg2.errors.UniqueViolation
        ):
            NominaController.insertar(nomina)

        self.assertEqual(self.cantidad_registros(), 1)
        self.assertEqual(
            NominaController.buscar(nomina.id_nomina),
            nomina,
        )

    def test_buscar_nomina_inexistente(self):
        id_inexistente = str(uuid4())

        with self.assertRaisesRegex(
            ValueError,
            "No existe una nómina",
        ):
            NominaController.buscar(id_inexistente)

    def test_buscar_id_con_formato_invalido(self):
        with self.assertRaisesRegex(
            ValueError,
            "formato UUID válido",
        ):
            NominaController.buscar("esto-no-es-un-uuid")

    # CREAR TABLAS: CASO NORMAL Y DE ERROR

    def test_crear_tablas(self):
        NominaController.borrar_tablas()
        NominaController.crear_tablas()

        self.assertEqual(self.cantidad_registros(), 0)

        nomina = self.nueva_nomina()
        NominaController.insertar(nomina)

        self.assertEqual(
            NominaController.buscar(nomina.id_nomina),
            nomina,
        )

    def test_crear_tablas_existentes(self):
        with self.assertRaises(
            psycopg2.errors.DuplicateTable
        ):
            NominaController.crear_tablas()

    # BORRAR TABLAS: CASO NORMAL Y DE ERROR

    def test_borrar_tablas(self):
        NominaController.borrar_tablas()

        with self.assertRaises(
            psycopg2.errors.UndefinedTable
        ):
            self.cantidad_registros()

    def test_borrar_tablas_inexistentes(self):
        NominaController.borrar_tablas()

        with self.assertRaises(
            psycopg2.errors.UndefinedTable
        ):
            NominaController.borrar_tablas()


if __name__ == "__main__":
    unittest.main()