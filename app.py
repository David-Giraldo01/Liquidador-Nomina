from math import isfinite

import psycopg2
from flask import Flask, redirect, render_template, request, url_for

from src.controller.nomina_controller import NominaController
from src.model.datos_nomina import DatosNomina
from src.model.errores import ErrorNomina
from src.model.logica_nomina import calcular_nomina


app = Flask(__name__)


def leer_datos(valores):
    try:
        salario = float(valores.get("salario", ""))
        dias = int(valores.get("dias", ""))
        bonificacion = float(valores.get("bonificacion", ""))
        comision = float(valores.get("comision", ""))
        descuentos = float(valores.get("descuentos", ""))

    except ValueError:
        raise ValueError(
            "Completa todos los campos con números válidos. "
            "Los días deben ser un número entero."
        ) from None

    importes = (salario, bonificacion, comision, descuentos)

    if not all(isfinite(valor) for valor in importes):
        raise ValueError("Los importes deben ser números finitos.")

    if bonificacion < 0 or comision < 0:
        raise ValueError(
            "La bonificación y la comisión no pueden ser negativas."
        )

    return DatosNomina(
        salario=salario,
        dias=dias,
        bonificacion=bonificacion,
        comision=comision,
        descuentos=descuentos,
    )


@app.route("/")
def inicio():
    return render_template("index.html", valores={})


@app.route("/calcular", methods=["POST"])
def calcular():
    valores = request.form.to_dict()

    try:
        datos = leer_datos(valores)
        neto = calcular_nomina(datos)

        return render_template(
            "index.html",
            valores=valores,
            resultado=f"$ {neto:,.2f}",
        )

    except (ErrorNomina, ValueError) as error:
        return render_template(
            "index.html",
            valores=valores,
            error=str(error),
        ), 400


@app.route("/guardar", methods=["POST"])
def guardar():
    valores = request.form.to_dict()

    try:
        datos = leer_datos(valores)

        # Valida las reglas del cálculo antes de insertar.
        calcular_nomina(datos)

        id_guardado = NominaController.insertar(datos)

    except (ErrorNomina, ValueError) as error:
        return render_template(
            "index.html",
            valores=valores,
            error=str(error),
        ), 400

    except psycopg2.Error:
        return render_template(
            "index.html",
            valores=valores,
            error=(
                "No fue posible guardar la nómina. "
                "Verifica la conexión con PostgreSQL, la configuración "
                "y que la tabla nominas esté creada."
            ),
        ), 503

    # Al actualizar la página de resultado no se repite el INSERT.
    return redirect(
        url_for("ver_nomina", id_nomina=id_guardado),
        code=303,
    )


@app.route("/buscar", methods=["GET"])
def buscar():
    id_ingresado = request.args.get("id_nomina", "").strip()

    try:
        id_validado = NominaController.validar_id(id_ingresado)

    except ValueError as error:
        return render_template(
            "index.html",
            valores={},
            id_busqueda=id_ingresado,
            error=str(error),
        ), 400

    return redirect(
        url_for("ver_nomina", id_nomina=id_validado)
    )


@app.route("/nomina/<id_nomina>")
def ver_nomina(id_nomina):
    try:
        datos = NominaController.buscar(id_nomina)
        neto = calcular_nomina(datos)

        valores = {
            "salario": datos.salario,
            "dias": datos.dias,
            "bonificacion": datos.bonificacion,
            "comision": datos.comision,
            "descuentos": datos.descuentos,
        }

        return render_template(
            "index.html",
            valores=valores,
            resultado=f"$ {neto:,.2f}",
            id_guardado=datos.id_nomina,
            id_busqueda=datos.id_nomina,
            mensaje="Esta nómina está guardada en la base de datos.",
        )

    except (ErrorNomina, ValueError) as error:
        return render_template(
            "index.html",
            valores={},
            id_busqueda=id_nomina,
            error=str(error),
        ), 400

    except psycopg2.Error:
        return render_template(
            "index.html",
            valores={},
            id_busqueda=id_nomina,
            error=(
                "No fue posible consultar la nómina. "
                "Verifica la conexión con PostgreSQL e intenta nuevamente."
            ),
        ), 503


if __name__ == "__main__":
    app.run()