# Liquidador de Nómina

## Integrantes

- Sebastián Velásquez

## Descripción

Aplicación desarrollada en Python que permite calcular la liquidación de nómina de un empleado teniendo en cuenta el salario básico, los días trabajados, las bonificaciones, las comisiones y otros descuentos.

El sistema calcula las deducciones correspondientes a salud y pensión y obtiene el valor neto a pagar.

El proyecto incluye una interfaz de consola y una interfaz gráfica experimental desarrollada con Kivy. También incluye pruebas unitarias desarrolladas con `unittest` para validar el correcto funcionamiento de la lógica del sistema.

> La interfaz gráfica con Kivy se encuentra en desarrollo experimental y fue incorporada como parte de la implementación del Tema 3: Interfaz de Usuario Gráfica.

## Entradas

- Salario básico.
- Días trabajados.
- Bonificación.
- Comisión.
- Otros descuentos.

## Procesos

- Validar los datos ingresados.
- Calcular el salario proporcional según los días trabajados.
- Sumar bonificaciones y comisiones.
- Obtener el total devengado.
- Calcular el descuento de salud.
- Calcular el descuento de pensión.
- Calcular el total de deducciones.
- Obtener el neto a pagar.
- Mostrar el resultado mediante la interfaz de consola o la interfaz gráfica.

## Salidas

- Total devengado.
- Total de deducciones.
- Neto a pagar.

## Interfaces disponibles

El proyecto ofrece dos formas de interacción:

- **Interfaz de consola:** solicita los datos desde la terminal y muestra el neto a pagar.
- **Interfaz gráfica experimental:** desarrollada con Kivy; presenta un formulario para ingresar los valores, botones para calcular o limpiar el formulario, un área para visualizar el neto a pagar y ventanas emergentes con mensajes claros cuando ocurre un error de validación, de formato de datos o un error inesperado.

La interfaz gráfica permite ingresar el salario básico, los días trabajados, la bonificación, la comisión y otros descuentos.

- Al presionar **Calcular**, muestra el valor neto a pagar con formato monetario.
- Al presionar **Limpiar**, elimina los valores ingresados y restablece el resultado inicial. Esta opción constituye una funcionalidad adicional de la interfaz.
- Si hay un error en la información ingresada, la aplicación presenta un mensaje amigable que explica qué ocurrió y cómo solucionarlo.

## Arquitectura del proyecto

El proyecto está organizado por capas: la lógica de negocio en `src/model`, las interfaces en `src/view` y las pruebas en `tests`.

```text
Liquidador-Nomina/
├── main.py
├── src/
│   ├── model/
│   │   ├── constantes.py
│   │   ├── errores.py
│   │   ├── datos_nomina.py
│   │   ├── logica_nomina.py
│   │   └── validacion.py
│   └── view/
│       ├── console/
│       │   └── consola.py
│       └── Gui/
│           └── liquidador.py
├── tests/
│   └── tests_nomina.py
├── docs/
├── .gitignore
└── README.md
```

## Descripción de los archivos

- `main.py`: punto de entrada principal para ejecutar la interfaz gráfica y para compilar la aplicación Android con Buildozer.
- `src/model/constantes.py`: contiene las constantes del cálculo, como los días del mes y las tasas de descuento.
- `src/model/datos_nomina.py`: contiene la estructura de datos que representa la información necesaria para liquidar la nómina.
- `src/model/errores.py`: contiene los errores personalizados e indica qué sucedió, por qué, dónde y cómo se soluciona.
- `src/model/logica_nomina.py`: contiene la lógica principal de cálculo dividida en funciones con responsabilidades específicas.
- `src/model/validacion.py`: contiene la clase que valida las entradas antes de calcular.
- `src/view/console/consola.py`: contiene la interfaz de consola para ingresar los datos y mostrar el resultado.
- `src/view/Gui/liquidador.py`: contiene la interfaz gráfica experimental en Kivy para ingresar datos, calcular el neto, limpiar el formulario y presentar mensajes de error amigables.
- `tests/tests_nomina.py`: contiene las pruebas unitarias desarrolladas con `unittest`.
- `docs/`: contiene la matriz de casos de prueba y demás documentación del proyecto.
- `README.md`: contiene la descripción general del proyecto y las instrucciones para su ejecución.

## Requisitos

- Python 3.12 o superior.
- Kivy, únicamente para ejecutar la interfaz gráfica experimental.

Para instalar Kivy, desde la carpeta principal del proyecto ejecuta:

```bash
py -m pip install kivy
```

En Linux o macOS, puede utilizarse:

```bash
python3 -m pip install kivy
```

## Ejecución de las pruebas unitarias

Para ejecutar las pruebas unitarias, ubícate desde la terminal en la carpeta principal del proyecto y ejecuta:

```bash
py -m unittest tests.tests_nomina
```

Actualmente el proyecto cuenta con 10 pruebas unitarias:

- 3 casos normales.
- 3 casos extraordinarios.
- 4 casos de error.

Si todas las pruebas se ejecutan correctamente, la terminal mostrará un resultado similar a:

```text
..........
Ran 10 tests in ...

OK
```

## Ejecución de la interfaz de consola

Para ejecutar la interfaz de consola, ubícate desde la terminal en la carpeta principal del proyecto y ejecuta:

```bash
py -m src.view.console.consola
```

La aplicación solicitará los siguientes datos:

- Salario básico.
- Días trabajados.
- Bonificación.
- Comisión.
- Otros descuentos.

Después de ingresar los datos, el programa calculará y mostrará el neto a pagar.

## Ejecución de la interfaz gráfica

Primero instala Kivy si todavía no está disponible en tu entorno:

```bash
py -m pip install kivy
```

Después, desde la carpeta principal del proyecto, ejecuta:

```bash
py -m src.view.Gui.liquidador
```

También puede ejecutarse mediante el punto de entrada principal:

```bash
py main.py
```

Se abrirá una ventana titulada **Liquidador de Nómina** con campos para ingresar el salario básico, los días trabajados, la bonificación, la comisión y otros descuentos.

- Presiona **Calcular** para obtener el neto a pagar.
- Presiona **Limpiar** para borrar todos los campos y restablecer el resultado a `$ 0.00`.

Todos los campos deben contener valores numéricos. Para los valores decimales, usa punto (`.`), por ejemplo: `2500000.50`. Si se ingresa información vacía, texto no numérico o valores que no cumplen las reglas de negocio, la aplicación mostrará una ventana con la explicación del error y una sugerencia para corregirlo.

## Ejemplo de ejecución en consola

```text
=== LIQUIDADOR DE NÓMINA ===
Ingrese el salario básico: 3000000
Ingrese los días trabajados: 30
Ingrese la bonificación: 0
Ingrese la comisión: 0
Ingrese otros descuentos: 0

=== RESULTADO ===
Neto a pagar: $2,760,000.00
```

## Ejemplo de uso de la interfaz gráfica

Ingresa los siguientes valores en el formulario:

- Salario básico: `3000000`
- Días trabajados: `30`
- Bonificación: `0`
- Comisión: `0`
- Otros descuentos: `0`

Al presionar **Calcular**, la interfaz mostrará:

```text
Neto a pagar: $ 2,760,000.00
```

Al presionar **Limpiar**, todos los campos quedarán vacíos y el resultado se restablecerá a:

```text
$ 0.00
```

## Generación del ejecutable para Windows

El proyecto cuenta con un ejecutable para Windows publicado en GitHub Releases.

Para generar localmente un ejecutable con PyInstaller, desde la raíz del proyecto puede utilizarse:

```bash
py -m PyInstaller -F --paths=src main.py
```

El ejecutable generado se ubicará en la carpeta `dist/`.

## Generación del APK para Android

La aplicación puede empaquetarse como APK Android utilizando Kivy y Buildozer en Ubuntu 22.04 o WSL.

El archivo principal debe llamarse `main.py` y estar ubicado en la raíz del repositorio. La configuración de compilación se define en el archivo `buildozer.spec`.

Después de configurar Buildozer, desde la raíz del proyecto se ejecuta:

```bash
buildozer -v android debug
```

El APK generado queda disponible en la carpeta `bin/`. El archivo APK se publica como un Asset en GitHub Releases.

> En Windows, se recomienda compilar desde Ubuntu 22.04 en WSL y clonar el repositorio dentro del sistema de archivos Linux, no dentro de `/mnt/c/`.
