def calcular_nomina(salario, dias, bonificacion, comision, descuentos):

    if dias < 0 or dias > 30:
     raise ValueError("Los dias deben estar entre 0 y 30")

    if salario < 0:
     raise ValueError("El salario no puede ser negativo")

    if descuentos < 0:
     raise ValueError("Los descuentos no pueden ser negativos")

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