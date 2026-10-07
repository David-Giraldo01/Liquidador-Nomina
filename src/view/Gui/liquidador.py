from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from src.model.datos_nomina import DatosNomina
from src.model.errores import ErrorNomina
from src.model.logica_nomina import calcular_nomina

if platform not in ("android", "ios"):
    Window.size = (480, 440)
    
TITULO_ERROR_VALIDACION = "Error de validación"
TITULO_ERROR_DATOS = "Datos inválidos"
TITULO_ERROR_INESPERADO = "Error inesperado"
TEXTO_RESULTADO_INICIAL = "$ 0.00"


class LiquidadorNominaApp(App):
    title = "Liquidador de Nómina"

    def build(self) -> BoxLayout:
        raiz = BoxLayout(orientation="vertical", padding=20, spacing=15)

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

        formulario = GridLayout(cols=2, spacing=10, size_hint=(1, 0.55))

        self.input_salario = self._agregar_campo(formulario, "Salario básico:")
        self.input_dias = self._agregar_campo(formulario, "Días trabajados:")
        self.input_bonificacion = self._agregar_campo(formulario, "Bonificación:")
        self.input_comision = self._agregar_campo(formulario, "Comisión:")
        self.input_descuentos = self._agregar_campo(formulario, "Otros descuentos:")

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

        return raiz

    @staticmethod
    def _ajustar_texto(label: Label) -> None:
        label.bind(
            size=lambda widget, tamanio: setattr(widget, "text_size", tamanio)
        )

    @staticmethod
    def _agregar_campo(contenedor: GridLayout, texto: str) -> TextInput:
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
            self._mostrar_error(TITULO_ERROR_VALIDACION, str(error))

        except ValueError as error:
            mensaje = (
                f"Qué sucedió: no fue posible interpretar un valor ingresado ({error}).\n"
                "Por qué: uno o más campos están vacíos, contienen texto no numérico "
                "o los días trabajados no son un número entero.\n"
                "Dónde: formulario del Liquidador de Nómina.\n"
                "Cómo se soluciona: ingrese solo números en todos los campos, use "
                "punto para los decimales y escriba los días como un número entero."
            )
            self._mostrar_error(TITULO_ERROR_DATOS, mensaje)

        except Exception as error:
            mensaje = (
                f"Qué sucedió: ocurrió un error inesperado ({error}).\n"
                "Por qué: no se identificó una causa específica dentro de la aplicación.\n"
                "Dónde: Liquidador de Nómina (interfaz gráfica).\n"
                "Cómo se soluciona: verifique los datos ingresados e intente "
                "nuevamente; si el error persiste, reporte el detalle al desarrollador."
            )
            self._mostrar_error(TITULO_ERROR_INESPERADO, mensaje)

    def limpiar_formulario(self, instance: Button) -> None:
        campos = (
            self.input_salario,
            self.input_dias,
            self.input_bonificacion,
            self.input_comision,
            self.input_descuentos,
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
            raise ValueError("Los días trabajados deben ser un número entero.")

        return int(dias)

    def _mostrar_resultado(self, neto: float) -> None:
        self.label_resultado.text = f"$ {neto:,.2f}"

    def _mostrar_error(self, titulo: str, mensaje: str) -> None:
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

        boton_cerrar = Button(text="Cerrar", size_hint=(1, 0.25))
        contenido.add_widget(boton_cerrar)

        popup = Popup(
            title=titulo,
            content=contenido,
            size_hint=(0.85, 0.6),
        )
        boton_cerrar.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    LiquidadorNominaApp().run()
