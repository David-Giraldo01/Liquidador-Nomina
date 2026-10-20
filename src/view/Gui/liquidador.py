import psycopg2

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from src.controller.nomina_controller import NominaController
from src.model.datos_nomina import DatosNomina
from src.model.errores import ErrorNomina
from src.model.logica_nomina import calcular_nomina


if platform not in ("android", "ios"):
    Window.size = (560, 620)


TITULO_ERROR_VALIDACION = "Error de validación"
TITULO_ERROR_DATOS = "Datos inválidos"
TITULO_ERROR_INESPERADO = "Error inesperado"
TEXTO_RESULTADO_INICIAL = "$ 0.00"


class LiquidadorNominaApp(App):
    title = "Liquidador de Nómina"

    def build(self) -> BoxLayout:
        raiz = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15,
        )

        encabezado = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.15),
        )

        titulo = Label(
            text="LIQUIDADOR DE NÓMINA",
            font_size=20,
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(0.6, 1),
        )
        self._ajustar_texto(titulo)

        instruccion = Label(
            text="Ingresa los datos a continuación:",
            font_size=14,
            halign="left",
            valign="middle",
            size_hint=(0.4, 1),
        )
        self._ajustar_texto(instruccion)

        encabezado.add_widget(titulo)
        encabezado.add_widget(instruccion)
        raiz.add_widget(encabezado)

        formulario = GridLayout(
            cols=2,
            spacing=10,
            size_hint=(1, 0.55),
        )

        self.input_salario = self._agregar_campo(
            formulario, "Salario básico:"
        )
        self.input_dias = self._agregar_campo(
            formulario, "Días trabajados:"
        )
        self.input_bonificacion = self._agregar_campo(
            formulario, "Bonificación:"
        )
        self.input_comision = self._agregar_campo(
            formulario, "Comisión:"
        )
        self.input_descuentos = self._agregar_campo(
            formulario, "Otros descuentos:"
        )

        raiz.add_widget(formulario)

        fila_botones = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, 0.12),
        )

        boton_calcular = Button(text="Calcular")
        boton_calcular.bind(on_press=self.calcular)

        boton_limpiar = Button(text="Limpiar")
        boton_limpiar.bind(on_press=self.limpiar_formulario)

        fila_botones.add_widget(boton_calcular)
        fila_botones.add_widget(boton_limpiar)
        raiz.add_widget(fila_botones)

        fila_resultado = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.18),
        )

        etiqueta_resultado = Label(
            text="Neto a pagar:",
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(0.45, 1),
        )
        self._ajustar_texto(etiqueta_resultado)

        self.label_resultado = Label(
            text=TEXTO_RESULTADO_INICIAL,
            bold=True,
            font_size=20,
            halign="right",
            valign="middle",
            size_hint=(0.55, 1),
        )
        self._ajustar_texto(self.label_resultado)

        fila_resultado.add_widget(etiqueta_resultado)
        fila_resultado.add_widget(self.label_resultado)
        raiz.add_widget(fila_resultado)

        boton_guardar = Button(
            text="Guardar nómina en la base de datos",
            size_hint=(1, None),
            height=45,
        )
        boton_guardar.bind(on_press=self.guardar_nomina)
        raiz.add_widget(boton_guardar)

        fila_busqueda = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint=(1, None),
            height=45,
        )

        self.input_id = TextInput(
            hint_text="Pega el UUID de la nómina",
            multiline=False,
            size_hint=(0.6, 1),
        )

        boton_buscar = Button(
            text="Buscar por ID",
            size_hint=(0.4, 1),
        )
        boton_buscar.bind(on_press=self.buscar_nomina)

        fila_busqueda.add_widget(self.input_id)
        fila_busqueda.add_widget(boton_buscar)
        raiz.add_widget(fila_busqueda)

        return raiz

    @staticmethod
    def _ajustar_texto(label: Label) -> None:
        label.bind(
            size=lambda widget, tamanio: setattr(
                widget, "text_size", tamanio
            )
        )

    @staticmethod
    def _agregar_campo(
        contenedor: GridLayout,
        texto: str,
    ) -> TextInput:
        contenedor.add_widget(Label(text=texto))

        campo = TextInput(
            multiline=False,
            font_size=18,
        )
        contenedor.add_widget(campo)
        return campo

    def calcular(self, instance: Button) -> None:
        try:
            datos = self._leer_datos()
            neto = calcular_nomina(datos)
            self._mostrar_resultado(neto)

        except ErrorNomina as error:
            self._mostrar_mensaje(
                TITULO_ERROR_VALIDACION,
                str(error),
            )

        except ValueError:
            self._mostrar_mensaje(
                TITULO_ERROR_DATOS,
                "Completa todos los campos con números.\n\n"
                "Usa punto para los decimales y escribe los días "
                "como un número entero.",
            )

        except Exception:
            self._mostrar_mensaje(
                TITULO_ERROR_INESPERADO,
                "No fue posible calcular la nómina.\n\n"
                "Verifica los datos e intenta nuevamente.",
            )

    def guardar_nomina(self, instance: Button) -> None:
        try:
            datos = self._leer_datos()

            # Aplicar las validaciones del modelo antes de guardar.
            neto = calcular_nomina(datos)

            id_generado = NominaController.insertar(datos)

            self.input_id.text = str(id_generado)
            self._mostrar_resultado(neto)

            self._mostrar_mensaje(
                "Nómina guardada",
                "La nómina se guardó correctamente.\n\n"
                f"ID asignado: {id_generado}\n\n"
                "Conserva este número para consultar la nómina.",
            )

        except ErrorNomina as error:
            self._mostrar_mensaje(
                TITULO_ERROR_VALIDACION,
                str(error),
            )

        except ValueError:
            self._mostrar_mensaje(
                TITULO_ERROR_DATOS,
                "Completa todos los campos con números.\n\n"
                "Usa punto para los decimales y escribe los días "
                "como un número entero.",
            )

        except psycopg2.IntegrityError:
            self._mostrar_mensaje(
                "Datos rechazados",
                "La base de datos rechazó los valores.\n\n"
                "Revisa que los importes no sean negativos "
                "y que los días estén entre 0 y 30.",
            )

        except psycopg2.Error:
            self._mostrar_mensaje(
                "Error de base de datos",
                "No se pudo completar el guardado.\n\n"
                "Revisa la conexión a Internet, la configuración "
                "de PostgreSQL y que la tabla nominas exista.",
            )

    def buscar_nomina(self, instance: Button) -> None:
        try:
            id_nomina = self.input_id.text.strip()

            if not id_nomina:
                raise ValueError(
                    "Pega el UUID completo de la nómina "
                    "que deseas buscar."
                )

            datos = NominaController.buscar(id_nomina)
            neto = calcular_nomina(datos)

            self.input_salario.text = f"{datos.salario:.2f}"
            self.input_dias.text = str(datos.dias)
            self.input_bonificacion.text = (
                f"{datos.bonificacion:.2f}"
            )
            self.input_comision.text = f"{datos.comision:.2f}"
            self.input_descuentos.text = f"{datos.descuentos:.2f}"
            self.input_id.text = datos.id_nomina

            self._mostrar_resultado(neto)

            self._mostrar_mensaje(
                "Nómina encontrada",
                "Se cargaron correctamente los datos "
                "de la nómina consultada.",
            )

        except ErrorNomina as error:
            self._mostrar_mensaje(
                TITULO_ERROR_VALIDACION,
                str(error),
            )

        except ValueError as error:
            self._mostrar_mensaje(
                "No se pudo consultar",
                str(error),
            )

        except psycopg2.Error:
            self._mostrar_mensaje(
                "Error de base de datos",
                "No se pudo completar la consulta.\n\n"
                "Revisa la conexión a Internet, la configuración "
                "de PostgreSQL y que la tabla nominas exista.",
            )

    def limpiar_formulario(self, instance: Button) -> None:
        campos = (
            self.input_salario,
            self.input_dias,
            self.input_bonificacion,
            self.input_comision,
            self.input_descuentos,
            self.input_id,
        )

        for campo in campos:
            campo.text = ""

        self.label_resultado.text = TEXTO_RESULTADO_INICIAL

    def _leer_datos(self) -> DatosNomina:
        salario = float(self.input_salario.text)
        dias = self._leer_dias_enteros()
        bonificacion = float(self.input_bonificacion.text)
        comision = float(self.input_comision.text)
        descuentos = float(self.input_descuentos.text)

        return DatosNomina(
            salario=salario,
            dias=dias,
            bonificacion=bonificacion,
            comision=comision,
            descuentos=descuentos,
        )

    def _leer_dias_enteros(self) -> int:
        dias = float(self.input_dias.text.strip())

        if not dias.is_integer():
            raise ValueError(
                "Los días trabajados deben ser un número entero."
            )

        return int(dias)

    def _mostrar_resultado(self, neto: float) -> None:
        self.label_resultado.text = f"$ {neto:,.2f}"

    def _mostrar_mensaje(self, titulo: str, mensaje: str) -> None:
        contenido = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10,
        )

        etiqueta = Label(
            text=mensaje,
            halign="left",
            valign="top",
        )
        self._ajustar_texto(etiqueta)
        contenido.add_widget(etiqueta)

        boton_cerrar = Button(
            text="Cerrar",
            size_hint=(1, None),
            height=45,
        )
        contenido.add_widget(boton_cerrar)

        popup = Popup(
            title=titulo,
            content=contenido,
            size_hint=(0.9, 0.65),
        )
        boton_cerrar.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    LiquidadorNominaApp().run()