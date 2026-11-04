from math import isfinite
from pathlib import Path
from uuid import UUID

import psycopg2
import secret_config

from src.model.datos_nomina import DatosNomina
from src.model.errores import (
    ErrorConexionBD,
    ErrorDatosNominaInvalidos,
    ErrorIdNominaInvalido,
    ErrorNominaDuplicada,
    ErrorNominaNoEncontrada,
    ErrorOperacionBD,
    ErrorTablaNominaExistente,
    ErrorTablaNominaNoExiste,
)


class NominaController:

    @staticmethod
    def conectar():
        try:
            return psycopg2.connect(
                host=secret_config.HOST,
                port=secret_config.PORT,
                database=secret_config.DATABASE,
                user=secret_config.USER,
                password=secret_config.PASSWORD,
                sslmode=secret_config.SSLMODE,
                connect_timeout=10,
            )
        except psycopg2.Error:
            raise ErrorConexionBD() from None

    @staticmethod
    def validar_id(id_nomina: str) -> str:
        try:
            return str(UUID(str(id_nomina).strip()))
        except (ValueError, TypeError, AttributeError):
            raise ErrorIdNominaInvalido() from None

    @staticmethod
    def _validar_datos(nomina: DatosNomina) -> None:
        importes = (
            nomina.salario,
            nomina.bonificacion,
            nomina.comision,
            nomina.descuentos,
        )

        try:
            importes_validos = all(
                not isinstance(valor, bool)
                and isfinite(valor)
                and valor >= 0
                for valor in importes
            )

            dias_validos = (
                isinstance(nomina.dias, int)
                and not isinstance(nomina.dias, bool)
                and 0 <= nomina.dias <= 30
            )

        except (TypeError, ValueError, OverflowError):
            raise ErrorDatosNominaInvalidos() from None

        if not importes_validos or not dias_validos:
            raise ErrorDatosNominaInvalidos()

    @staticmethod
    def _ejecutar(
        sentencia,
        parametros=None,
        devolver_fila=False,
        id_nomina=None,
    ):
        """Ejecuta SQL y administra la transacción y la conexión."""
        conexion = NominaController.conectar()

        try:
            with conexion.cursor() as cursor:
                cursor.execute(sentencia, parametros)

                fila = (
                    cursor.fetchone()
                    if devolver_fila
                    else None
                )

            conexion.commit()
            return fila

        except psycopg2.Error as error:
            # Si la conexión se perdió, rollback también puede fallar.
            # Conservamos el error original para traducirlo.
            try:
                conexion.rollback()
            except psycopg2.Error:
                pass

            if isinstance(error, psycopg2.errors.UniqueViolation):
                raise ErrorNominaDuplicada(id_nomina) from None

            if isinstance(
                error,
                (
                    psycopg2.errors.CheckViolation,
                    psycopg2.errors.NotNullViolation,
                    psycopg2.DataError,
                ),
            ):
                raise ErrorDatosNominaInvalidos() from None

            if isinstance(error, psycopg2.errors.DuplicateTable):
                raise ErrorTablaNominaExistente() from None

            if isinstance(error, psycopg2.errors.UndefinedTable):
                raise ErrorTablaNominaNoExiste() from None

            raise ErrorOperacionBD() from None

        finally:
            conexion.close()

    @staticmethod
    def insertar(nomina: DatosNomina) -> str:
        id_validado = NominaController.validar_id(
            nomina.id_nomina
        )
        NominaController._validar_datos(nomina)

        fila = NominaController._ejecutar(
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
            parametros=(
                id_validado,
                nomina.salario,
                nomina.dias,
                nomina.bonificacion,
                nomina.comision,
                nomina.descuentos,
            ),
            devolver_fila=True,
            id_nomina=id_validado,
        )

        return str(fila[0])

    @staticmethod
    def buscar(id_nomina: str) -> DatosNomina:
        id_validado = NominaController.validar_id(id_nomina)

        fila = NominaController._ejecutar(
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
            parametros=(id_validado,),
            devolver_fila=True,
        )

        if fila is None:
            raise ErrorNominaNoEncontrada(id_validado)

        return DatosNomina(
            id_nomina=str(fila[0]),
            salario=float(fila[1]),
            dias=fila[2],
            bonificacion=float(fila[3]),
            comision=float(fila[4]),
            descuentos=float(fila[5]),
        )

    @staticmethod
    def crear_tablas():
        ruta_sql = (
            Path(__file__).resolve().parents[2]
            / "sql"
            / "crear_tablas.sql"
        )

        try:
            sentencia = ruta_sql.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            raise ErrorOperacionBD() from None

        NominaController._ejecutar(sentencia)

    @staticmethod
    def borrar_tablas():
        NominaController._ejecutar(
            "DROP TABLE nominas;"
        )   