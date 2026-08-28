from src.model.constantes import (
    DIAS_MES,
    TASA_DESCUENTO_PENSION,
    TASA_DESCUENTO_SALUD,
)
from src.model.validacion import ValidadorNomina


def calcular_salario_proporcional(salario, dias):
    return salario / DIAS_MES * dias


def calcular_total_devengado(salario_proporcional, bonificacion, comision):
    return salario_proporcional + bonificacion + comision


def calcular_total_deducciones(total_devengado, descuentos):
    descuento_salud = total_devengado * TASA_DESCUENTO_SALUD
    descuento_pension = total_devengado * TASA_DESCUENTO_PENSION
    return descuento_salud + descuento_pension + descuentos


def calcular_neto_pagar(total_devengado, total_deducciones):
    return total_devengado - total_deducciones


def calcular_nomina(salario, dias, bonificacion, comision, descuentos):
    ValidadorNomina(salario, dias, descuentos).validar()

    salario_proporcional = calcular_salario_proporcional(salario, dias)
    total_devengado = calcular_total_devengado(
        salario_proporcional,
        bonificacion,
        comision,
    )
    total_deducciones = calcular_total_deducciones(total_devengado, descuentos)
    return calcular_neto_pagar(total_devengado, total_deducciones)