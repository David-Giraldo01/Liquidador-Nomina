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

class ErrorIdNominaInvalido(ErrorNomina):

    def __init__(self):
        super().__init__(
            "El identificador de la nómina no es válido.",
            "El texto ingresado no tiene formato UUID.",
            "Controlador de nómina: validación del identificador.",
            "Copie el ID completo de una nómina guardada.",
        )


class ErrorNominaNoEncontrada(ErrorNomina):

    def __init__(self, id_nomina):
        super().__init__(
            f"No existe una nómina con el ID {id_nomina}.",
            "No se encontró un registro con ese identificador.",
            "Controlador de nómina: búsqueda.",
            "Verifique el ID e intente consultar nuevamente.",
        )


class ErrorNominaDuplicada(ErrorNomina):

    def __init__(self, id_nomina):
        super().__init__(
            f"Ya existe una nómina con el ID {id_nomina}.",
            "Se intentó insertar un identificador que ya está registrado.",
            "Controlador de nómina: inserción.",
            "Consulte la nómina existente o cree una nueva con otro ID.",
        )


class ErrorDatosNominaInvalidos(ErrorNomina):

    def __init__(self):
        super().__init__(
            "Los datos de la nómina no cumplen las restricciones.",
            "Uno o más valores no son admitidos por la base de datos.",
            "Controlador de nómina: inserción.",
            "Use importes no negativos y días enteros entre 0 y 30.",
        )


class ErrorTablaNominaExistente(ErrorNomina):

    def __init__(self):
        super().__init__(
            "La tabla de nóminas ya existe.",
            "Se intentó crear una tabla que ya estaba creada.",
            "Controlador de nómina: creación de tablas.",
            "Utilice la tabla existente para guardar y consultar nóminas.",
        )


class ErrorTablaNominaNoExiste(ErrorNomina):

    def __init__(self):
        super().__init__(
            "La tabla de nóminas no existe.",
            "La base de datos todavía no contiene la tabla requerida.",
            "Controlador de nómina: operación sobre tablas.",
            "Cree la tabla antes de insertar, consultar o eliminarla.",
        )


class ErrorConexionBD(ErrorNomina):

    def __init__(self):
        super().__init__(
            "No fue posible establecer conexión con la base de datos.",
            "El servidor no está disponible o la configuración es incorrecta.",
            "Controlador de nómina: conexión con PostgreSQL.",
            "Verifique la conexión a Internet, el servidor y los datos "
            "de secret_config.py.",
        )


class ErrorOperacionBD(ErrorNomina):

    def __init__(self):
        super().__init__(
            "No fue posible completar la operación en la base de datos.",
            "PostgreSQL informó un error durante la operación.",
            "Controlador de nómina.",
            "Verifique la estructura de la tabla y los permisos "
            "del usuario de la base de datos.",
        )