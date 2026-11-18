from dataclasses import dataclass

from src.model.constantes import (
    AUXILIO_TRANSPORTE,
    DIAS_MES,
    TASA_DESCUENTO_PENSION,
    TASA_DESCUENTO_SALUD,
    UMBRAL_AUXILIO_TRANSPORTE,
)
from src.model.validacion import ValidadorNomina
from src.model.datos_nomina import DatosNomina


@dataclass(frozen=True)
class DetalleNomina:
    """Desglose completo de una liquidación de nómina."""

    salario: float
    salario_proporcional: float
    dias: int
    auxilio_transporte: float
    bonificacion: float
    comision: float
    total_devengado: float
    descuento_salud: float
    descuento_pension: float
    otros_descuentos: float
    total_deducciones: float
    neto_pagar: float

    @property
    def aplica_auxilio_transporte(self) -> bool:
        return self.auxilio_transporte > 0


def calcular_salario_proporcional(salario: float, dias: int) -> float:
    return salario / DIAS_MES * dias


def calcular_auxilio_transporte(salario: float) -> float:
    """Devuelve el auxilio de transporte si el salario básico lo permite."""
    if salario < UMBRAL_AUXILIO_TRANSPORTE:
        return AUXILIO_TRANSPORTE
    return 0.0


def calcular_total_devengado(
    salario_proporcional: float,
    bonificacion: float,
    comision: float,
    auxilio_transporte: float = 0.0,
) -> float:
    return (
        salario_proporcional
        + bonificacion
        + comision
        + auxilio_transporte
    )


def calcular_descuento_salud(total_devengado: float) -> float:
    return total_devengado * TASA_DESCUENTO_SALUD


def calcular_descuento_pension(total_devengado: float) -> float:
    return total_devengado * TASA_DESCUENTO_PENSION


def calcular_total_deducciones(total_devengado: float, descuentos: float) -> float:
    return (
        calcular_descuento_salud(total_devengado)
        + calcular_descuento_pension(total_devengado)
        + descuentos
    )


def calcular_neto_pagar(total_devengado: float, total_deducciones: float) -> float:
    return total_devengado - total_deducciones


def calcular_detalle(datos: DatosNomina) -> DetalleNomina:
    ValidadorNomina(
        datos.salario,
        datos.dias,
        datos.descuentos
    ).validar()

    salario_proporcional = calcular_salario_proporcional(
        datos.salario,
        datos.dias
    )

    auxilio_transporte = calcular_auxilio_transporte(datos.salario)

    total_devengado = calcular_total_devengado(
        salario_proporcional,
        datos.bonificacion,
        datos.comision,
        auxilio_transporte,
    )

    descuento_salud = calcular_descuento_salud(total_devengado)
    descuento_pension = calcular_descuento_pension(total_devengado)
    total_deducciones = calcular_total_deducciones(
        total_devengado,
        datos.descuentos
    )

    return DetalleNomina(
        salario=datos.salario,
        salario_proporcional=salario_proporcional,
        dias=datos.dias,
        auxilio_transporte=auxilio_transporte,
        bonificacion=datos.bonificacion,
        comision=datos.comision,
        total_devengado=total_devengado,
        descuento_salud=descuento_salud,
        descuento_pension=descuento_pension,
        otros_descuentos=datos.descuentos,
        total_deducciones=total_deducciones,
        neto_pagar=calcular_neto_pagar(
            total_devengado,
            total_deducciones
        ),
    )


def calcular_nomina(datos: DatosNomina) -> float:
    return calcular_detalle(datos).neto_pagar
