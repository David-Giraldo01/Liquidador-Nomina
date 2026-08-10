def calcular_nomina(salario, dias, bonificacion, comision, descuentos):

    salario_proporcional = salario / 30 * dias

    total_devengado = (
        salario_proporcional
        + bonificacion
        + comision
    )

    descuento_salud = total_devengado * 0.04
    descuento_pension = total_devengado * 0.04

    total_deducciones = (
        descuento_salud
        + descuento_pension
        + descuentos
    )

    neto_pagar = total_devengado - total_deducciones

    return neto_pagar