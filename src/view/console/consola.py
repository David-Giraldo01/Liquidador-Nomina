from src.model.datos_nomina import DatosNomina
from src.model.logica_nomina import calcular_nomina

def main():
    print("=== LIQUIDADOR DE NÓMINA ===")

    try:
        salario = float(input("Ingrese el salario básico: "))
        dias = int(input("Ingrese los días trabajados: "))
        bonificacion = float(input("Ingrese la bonificación: "))
        comision = float(input("Ingrese la comisión: "))
        descuentos = float(input("Ingrese otros descuentos: "))

        datos = DatosNomina(
            salario=salario,
            dias=dias,
            bonificacion=bonificacion,
            comision=comision,
            descuentos=descuentos,
        )

        neto = calcular_nomina(datos)

        print("\n=== RESULTADO ===")
        print(f"Neto a pagar: ${neto:,.2f}")

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()