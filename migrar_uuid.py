import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from controller.nomina_controller import NominaController


def migrar():
    conexion = NominaController.conectar()
    equivalencias = []

    try:
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SET LOCAL lock_timeout = '10s';")
                cursor.execute(
                    "LOCK TABLE public.nominas IN ACCESS EXCLUSIVE MODE;"
                )

                cursor.execute("""
                    SELECT data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = 'nominas'
                      AND column_name = 'id_nomina';
                """)
                resultado = cursor.fetchone()

                if resultado and resultado[0] == "uuid":
                    print("La tabla ya usa UUID. No se realizaron cambios.")
                    return

                if not resultado or resultado[0] != "integer":
                    raise ValueError("La columna no tiene el tipo esperado.")

                # No sobrescribe un respaldo que ya exista.
                cursor.execute("""
                    CREATE TABLE public.nominas_respaldo_enteros AS
                    SELECT * FROM public.nominas;
                """)
                cursor.execute("""
                    ALTER TABLE public.nominas_respaldo_enteros
                    ADD COLUMN nuevo_uuid UUID;
                """)
                cursor.execute("""
                    ALTER TABLE public.nominas
                    ADD COLUMN uuid_temporal UUID;
                """)

                cursor.execute(
                    "SELECT id_nomina FROM public.nominas ORDER BY id_nomina;"
                )
                ids_anteriores = [fila[0] for fila in cursor.fetchall()]

                for id_anterior in ids_anteriores:
                    nuevo_id = str(uuid4())

                    cursor.execute("""
                        UPDATE public.nominas
                        SET uuid_temporal = %s
                        WHERE id_nomina = %s;
                    """, (nuevo_id, id_anterior))

                    cursor.execute("""
                        UPDATE public.nominas_respaldo_enteros
                        SET nuevo_uuid = %s
                        WHERE id_nomina = %s;
                    """, (nuevo_id, id_anterior))

                    equivalencias.append((id_anterior, nuevo_id))

                cursor.execute("""
                    ALTER TABLE public.nominas
                    ALTER COLUMN id_nomina DROP IDENTITY IF EXISTS;
                """)
                cursor.execute("""
                    ALTER TABLE public.nominas
                    ALTER COLUMN id_nomina DROP DEFAULT;
                """)
                cursor.execute("""
                    ALTER TABLE public.nominas
                    ALTER COLUMN id_nomina TYPE UUID
                    USING uuid_temporal;
                """)
                cursor.execute("""
                    ALTER TABLE public.nominas
                    DROP COLUMN uuid_temporal;
                """)

                # Comprueba que se conservaron los registros y sus valores.
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM public.nominas AS n
                    JOIN public.nominas_respaldo_enteros AS r
                      ON n.id_nomina = r.nuevo_uuid
                    WHERE ROW(
                        n.salario, n.dias, n.bonificacion,
                        n.comision, n.descuentos
                    ) IS NOT DISTINCT FROM ROW(
                        r.salario, r.dias, r.bonificacion,
                        r.comision, r.descuentos
                    );
                """)

                if cursor.fetchone()[0] != len(ids_anteriores):
                    raise RuntimeError(
                        "La verificación de los registros no fue satisfactoria."
                    )

        print("Migración completada correctamente.")
        print(f"Nóminas conservadas: {len(equivalencias)}")
        print("Respaldo: public.nominas_respaldo_enteros")
        print("\nIdentificadores anteriores y nuevos:")

        for anterior, nuevo in equivalencias:
            print(f"{anterior} -> {nuevo}")

    finally:
        conexion.close()


if __name__ == "__main__":
    migrar()