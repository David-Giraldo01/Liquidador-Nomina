from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class DatosNomina:
    salario: float
    dias: int
    bonificacion: float
    comision: float
    descuentos: float
    id_nomina: str = field(default_factory=lambda: str(uuid4()))
