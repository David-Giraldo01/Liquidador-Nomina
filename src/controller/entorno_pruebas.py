from uuid import uuid4

from psycopg2 import sql

from src.controller.nomina_controller import NominaController


class EntornoPruebasNomina:
    """Administra un esquema temporal separado de los datos reales."""

    def __init__(self):
        self.esquema = "test_nomina_" + uuid4().hex
        self.conectar_original = NominaController.conectar

    def crear(self):
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

    def conectar(self):
        conexion = self.conectar_original()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    # Solo el esquema de prueba: sin fallback a public.
                    cursor.execute(
                        sql.SQL("SET search_path TO {}").format(
                            sql.Identifier(self.esquema)
                        )
                    )

            return conexion

        except Exception:
            conexion.close()
            raise

    def eliminar(self):
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