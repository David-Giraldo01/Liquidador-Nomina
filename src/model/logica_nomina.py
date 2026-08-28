from src.model.constantes import (
    DIAS_MES,
    TASA_DESCUENTO_PENSION,
    TASA_DESCUENTO_SALUD,
)
from src.model.validacion import ValidadorNomina
from src.model.datos_nomina import DatosNomina

def calcular_salario_proporcional(salario: float, dias: int )-> float:
    return salario / DIAS_MES * dias


def calcular_total_devengado(salario_proporcional: float, bonificacion: float, comision: float)-> float:
    return salario_proporcional + bonificacion + comision


def calcular_total_deducciones(total_devengado: float, descuentos: float)-> float:
    descuento_salud = total_devengado * TASA_DESCUENTO_SALUD
    descuento_pension = total_devengado * TASA_DESCUENTO_PENSION
    return descuento_salud + descuento_pension + descuentos


def calcular_neto_pagar(total_devengado: float , total_deducciones: float)-> float:
    return total_devengado - total_deducciones


def calcular_nomina(datos: DatosNomina) -> float:
    ValidadorNomina(
        datos.salario,
        datos.dias,
        datos.descuentos
    ).validar()

    salario_proporcional = calcular_salario_proporcional(
        datos.salario,
        datos.dias
    )

    total_devengado = calcular_total_devengado(
        salario_proporcional,
        datos.bonificacion,
        datos.comision,
    )

    total_deducciones = calcular_total_deducciones(
        total_devengado,
        datos.descuentos
    )

    return calcular_neto_pagar(
        total_devengado,
        total_deducciones
    )
