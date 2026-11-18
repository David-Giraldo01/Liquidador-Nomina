from src.model.datos_nomina import DatosNomina
from src.model.logica_nomina import calcular_detalle

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

        detalle = calcular_detalle(datos)

        print("\n=== RESULTADO ===")
        print(f"Salario básico: ${detalle.salario:,.2f}")

        if detalle.aplica_auxilio_transporte:
            print(
                "Auxilio de transporte: "
                f"${detalle.auxilio_transporte:,.2f}"
            )
        else:
            print("Auxilio de transporte: No aplica")

        print(f"Total devengado: ${detalle.total_devengado:,.2f}")
        print(f"Total deducciones: ${detalle.total_deducciones:,.2f}")
        print(f"Neto a pagar: ${detalle.neto_pagar:,.2f}")

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()