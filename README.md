# Liquidador de Nómina

## Integrantes

- Yeisner Giraldo
- Samuel García
- Juan Sebastian Leal

## Descripción

Aplicación desarrollada en Python que permite calcular la liquidación de nómina de un empleado teniendo en cuenta el salario básico, los días trabajados, las bonificaciones, las comisiones y otros descuentos.

El sistema calcula las deducciones correspondientes a salud y pensión y obtiene el valor neto a pagar.

El proyecto incluye pruebas unitarias desarrolladas con `unittest` para validar el correcto funcionamiento de la lógica del sistema.

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

## Salidas

- Total devengado.
- Total de deducciones.
- Neto a pagar.

## Arquitectura del proyecto

El proyecto está organizado de forma simple para facilitar la ejecución de la lógica, la interfaz de consola y las pruebas unitarias.

```text
Liquidador-Nomina/
├── docs/
├── consola.py
├── logica_nomina.py
├── tests_nomina.py
├── .gitignore
└── README.md
```

## Descripción de los archivos

- `logica_nomina.py`: contiene la lógica principal para realizar el cálculo de la nómina.
- `consola.py`: contiene la interfaz de consola para ingresar los datos y mostrar el resultado.
- `tests_nomina.py`: contiene las pruebas unitarias desarrolladas con `unittest`.
- `docs/`: contiene la matriz de casos de prueba y demás documentación del proyecto.
- `README.md`: contiene la descripción general del proyecto y las instrucciones para su ejecución.

## Ejecución de las pruebas unitarias

Para ejecutar las pruebas unitarias, ubicarse desde la terminal en la carpeta principal del proyecto y ejecutar:

```bash
py -m unittest tests_nomina
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

Para ejecutar la interfaz de consola, ubicarse desde la terminal en la carpeta principal del proyecto y ejecutar:

```bash
python consola.py
```

La aplicación solicitará los siguientes datos:

- Salario básico.
- Días trabajados.
- Bonificación.
- Comisión.
- Otros descuentos.

Después de ingresar los datos, el programa calculará y mostrará el neto a pagar.

## Ejemplo de ejecución

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
