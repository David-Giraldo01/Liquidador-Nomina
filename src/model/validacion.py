from src.model.constantes import DIAS_MES
from src.model.errores import (
    ErrorDescuentosNegativos,
    ErrorDiasInvalidos,
    ErrorSalarioNegativo,
)


class ValidadorNomina:
    """Valida las entradas de la liquidación antes de calcular."""

    def __init__(self, salario, dias, descuentos):
        self.salario = salario
        self.dias = dias
        self.descuentos = descuentos

    def validar(self):
        self._validar_dias()
        self._validar_salario()
        self._validar_descuentos()

    def _validar_dias(self):
        if self.dias < 0 or self.dias > DIAS_MES:
            raise ErrorDiasInvalidos(self.dias)

    def _validar_salario(self):
        if self.salario < 0:
            raise ErrorSalarioNegativo(self.salario)

    def _validar_descuentos(self):
        if self.descuentos < 0:
            raise ErrorDescuentosNegativos(self.descuentos)