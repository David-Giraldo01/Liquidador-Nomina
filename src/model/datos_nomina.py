from dataclasses import dataclass


@dataclass
class DatosNomina:
    salario: float
    dias: int
    bonificacion: float
    comision: float
    descuentos: float
