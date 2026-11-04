from math import isfinite

from flask import Blueprint, redirect, render_template, request, url_for

from src.controller.nomina_controller import NominaController
from src.model.datos_nomina import DatosNomina
from src.model.errores import (
    ErrorConexionBD,
    ErrorNomina,
    ErrorNominaNoEncontrada,
    ErrorOperacionBD,
    ErrorTablaNominaExistente,
    ErrorTablaNominaNoExiste,
)
from src.model.logica_nomina import calcular_nomina


vista = Blueprint("nomina", __name__)


def error_formulario(motivo):
    return ErrorNomina(
        "No fue posible interpretar los datos del formulario.",
        motivo,
        "Formulario web de liquidación de nómina.",
        "Completa todos los campos con números finitos, usa punto "
        "para los decimales y escribe los días como un número entero.",
    )


def leer_datos(valores):
    try:
        salario = float(valores.get("salario", ""))
        dias = int(valores.get("dias", ""))
        bonificacion = float(valores.get("bonificacion", ""))
        comision = float(valores.get("comision", ""))
        descuentos = float(valores.get("descuentos", ""))

    except (ValueError, TypeError):
        raise error_formulario(
            "Hay campos vacíos o valores con un formato incorrecto."
        ) from None

    importes = (salario, bonificacion, comision, descuentos)

    if not all(isfinite(valor) for valor in importes):
        raise error_formulario(
            "Los importes contienen valores que no son finitos."
        )

    if bonificacion < 0 or comision < 0:
        raise ErrorNomina(
            "La bonificación o la comisión es negativa.",
            "Estos importes deben ser mayores o iguales a cero.",
            "Formulario web de liquidación de nómina.",
            "Corrige la bonificación y la comisión.",
        )

    return DatosNomina(
        salario=salario,
        dias=dias,
        bonificacion=bonificacion,
        comision=comision,
        descuentos=descuentos,
    )


def mostrar_error(error, **contexto):
    """Presenta los errores conocidos sin mostrar detalles privados."""
    codigo = 400

    if isinstance(error, ErrorNominaNoEncontrada):
        codigo = 404

    elif isinstance(
        error,
        (ErrorConexionBD, ErrorOperacionBD, ErrorTablaNominaNoExiste),
    ):
        codigo = 503

    return render_template(
        "nomina.html",
        error=str(error),
        **contexto,
    ), codigo


@vista.route("/")
def inicio():
    return render_template("inicio.html")


@vista.route("/calcular", methods=["GET", "POST"])
def calcular():
    if request.method == "GET":
        return render_template("nomina.html", valores={})

    valores = request.form.to_dict()

    try:
        datos = leer_datos(valores)
        neto = calcular_nomina(datos)

    except ErrorNomina as error:
        return mostrar_error(error, valores=valores)

    return render_template(
        "nomina.html",
        valores=valores,
        resultado=f"$ {neto:,.2f}",
    )


@vista.route("/guardar", methods=["POST"])
def guardar():
    valores = request.form.to_dict()

    try:
        datos = leer_datos(valores)

        # Valida la nómina antes de guardarla.
        calcular_nomina(datos)

        id_guardado = NominaController.insertar(datos)

    except ErrorNomina as error:
        return mostrar_error(error, valores=valores)

    # Redirigir evita repetir el INSERT al actualizar el resultado.
    return redirect(
        url_for("nomina.ver_nomina", id_nomina=id_guardado),
        code=303,
    )


@vista.route("/buscar", methods=["GET"])
def buscar():
    # Al entrar desde el menú, muestra el formulario sin error.
    if "id_nomina" not in request.args:
        return render_template("nomina.html", valores={})

    id_ingresado = request.args.get("id_nomina", "").strip()

    try:
        id_validado = NominaController.validar_id(id_ingresado)

    except ErrorNomina as error:
        return mostrar_error(
            error,
            valores={},
            id_busqueda=id_ingresado,
        )

    return redirect(
        url_for("nomina.ver_nomina", id_nomina=id_validado)
    )


@vista.route("/nomina/<id_nomina>")
def ver_nomina(id_nomina):
    try:
        datos = NominaController.buscar(id_nomina)
        neto = calcular_nomina(datos)

    except ErrorNomina as error:
        return mostrar_error(
            error,
            valores={},
            id_busqueda=id_nomina,
        )

    valores = {
        "salario": datos.salario,
        "dias": datos.dias,
        "bonificacion": datos.bonificacion,
        "comision": datos.comision,
        "descuentos": datos.descuentos,
    }

    return render_template(
        "nomina.html",
        valores=valores,
        resultado=f"$ {neto:,.2f}",
        id_guardado=datos.id_nomina,
        id_busqueda=datos.id_nomina,
    )


@vista.route("/crear-tablas", methods=["GET", "POST"])
def crear_tablas():
    if request.method == "GET":
        return render_template("crear_tablas.html")

    try:
        NominaController.crear_tablas()

    except ErrorTablaNominaExistente:
        return render_template(
            "crear_tablas.html",
            mensaje=(
                "La tabla de nóminas ya existe. "
                "Puedes continuar usando la aplicación. "
                "Los datos existentes se conservaron."
            ),
        )

    except ErrorNomina as error:
        return render_template(
            "crear_tablas.html",
            error=str(error),
        ), 503

    return render_template(
        "crear_tablas.html",
        mensaje="La tabla de nóminas se creó correctamente.",
    )