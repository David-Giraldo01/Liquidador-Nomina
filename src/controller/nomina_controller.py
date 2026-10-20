from pathlib import Path
from uuid import UUID

import psycopg2
import secret_config

from model.datos_nomina import DatosNomina


class NominaController:

    @staticmethod
    def conectar():
        return psycopg2.connect(
            host=secret_config.HOST,
            port=secret_config.PORT,
            database=secret_config.DATABASE,
            user=secret_config.USER,
            password=secret_config.PASSWORD,
            sslmode=secret_config.SSLMODE,
            connect_timeout=10,
        )

    @staticmethod
    def validar_id(id_nomina: str) -> str:
        try:
            return str(UUID(str(id_nomina).strip()))
        except (ValueError, TypeError, AttributeError):
            raise ValueError(
                "El ID debe tener un formato UUID válido. "
                "Copia el identificador completo de una nómina guardada."
            ) from None

    @staticmethod
    def insertar(nomina: DatosNomina) -> str:
        id_nomina = NominaController.validar_id(nomina.id_nomina)
        conexion = NominaController.conectar()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO nominas (
                            id_nomina,
                            salario,
                            dias,
                            bonificacion,
                            comision,
                            descuentos
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id_nomina;
                        """,
                        (
                            id_nomina,
                            nomina.salario,
                            nomina.dias,
                            nomina.bonificacion,
                            nomina.comision,
                            nomina.descuentos,
                        ),
                    )

                    id_guardado = str(cursor.fetchone()[0])

            return id_guardado
        finally:
            conexion.close()

    @staticmethod
    def buscar(id_nomina: str) -> DatosNomina:
        id_validado = NominaController.validar_id(id_nomina)
        conexion = NominaController.conectar()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT
                            id_nomina,
                            salario,
                            dias,
                            bonificacion,
                            comision,
                            descuentos
                        FROM nominas
                        WHERE id_nomina = %s;
                        """,
                        (id_validado,),
                    )

                    fila = cursor.fetchone()

            if fila is None:
                raise ValueError(
                    f"No existe una nómina con el ID {id_validado}."
                )

            return DatosNomina(
                id_nomina=str(fila[0]),
                salario=float(fila[1]),
                dias=fila[2],
                bonificacion=float(fila[3]),
                comision=float(fila[4]),
                descuentos=float(fila[5]),
            )
        finally:
            conexion.close()

    @staticmethod
    def crear_tablas():
        ruta_sql = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "crear_tablas.sql"
        )

        sentencia = ruta_sql.read_text(encoding="utf-8")
        conexion = NominaController.conectar()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(sentencia)
        finally:
            conexion.close()

    @staticmethod
    def borrar_tablas():
        conexion = NominaController.conectar()

        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("DROP TABLE nominas;")
        finally:
            conexion.close()