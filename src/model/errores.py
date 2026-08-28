class ErrorNomina(ValueError):
    """Error base de la liquidación.

    Cada error indica qué sucedió, por qué, dónde y cómo se soluciona.
    """

    def __init__(self, que_sucedio, por_que, donde, como_solucionar):
        super().__init__(que_sucedio)
        self.que_sucedio = que_sucedio
        self.por_que = por_que
        self.donde = donde
        self.como_solucionar = como_solucionar

    def __str__(self):
        return (
            f"Qué sucedió: {self.que_sucedio}\n"
            f"Por qué: {self.por_que}\n"
            f"Dónde: {self.donde}\n"
            f"Cómo se soluciona: {self.como_solucionar}"
        )


class ErrorDiasInvalidos(ErrorNomina):

    def __init__(self, dias):
        super().__init__(
            f"Los días trabajados ({dias}) deben estar entre 0 y 30.",
            "El número de días no está en el rango válido de un mes.",
            "src/model/validacion.py (_validar_dias).",
            "Ingrese un valor de días entre 0 y 30.",
        )


class ErrorSalarioNegativo(ErrorNomina):

    def __init__(self, salario):
        super().__init__(
            f"El salario no puede ser negativo ({salario}).",
            "Se ingresó un valor de salario menor que cero.",
            "src/model/validacion.py (_validar_salario).",
            "Ingrese un salario mayor o igual a cero.",
        )


class ErrorDescuentosNegativos(ErrorNomina):

    def __init__(self, descuentos):
        super().__init__(
            f"Los descuentos no pueden ser negativos ({descuentos}).",
            "Se ingresó un valor de descuentos menor que cero.",
            "src/model/validacion.py (_validar_descuentos).",
            "Ingrese un valor de descuentos mayor o igual a cero.",
        )