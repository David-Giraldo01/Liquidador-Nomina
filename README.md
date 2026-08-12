# Liquidador de Nómina

## Integrantes

- Yeisner Giraldo
- Samuel García 
- Juan Sebastian Leal

## Descripción

Aplicación desarrollada en Python que permite calcular la liquidación de nómina de un empleado teniendo en cuenta los valores devengados y las deducciones de ley. El proyecto incluye pruebas unitarias para validar el correcto funcionamiento del sistema.

## Entradas

- Salario básico
- Días trabajados
- Bonificaciones
- Comisiones
- Otros Descuentos
- Porcentaje de salud
- Porcentaje de pensión

## Procesos

- Calcular salario proporcional.
- Calcular horas dominicales.
- Calcular bonificaciones y comisiones.
- Obtener el total devengado.
- Calcular descuentos por salud y pensión.
- Calcular deducciones.
- Obtener el neto a pagar.

## Salidas

- Total devengado.
- Descuento por salud.
- Descuento por pensión.
- Total deducciones.
- Neto a pagar.

## Arquitectura del proyecto

El proyecto está organizado en carpetas para separar la lógica del programa, las pruebas y la documentación.

```text
Liquidador-Nomina/
├── docs/
│   ├── AUDIO EXPLICACION.ogg
│   ├── PRUEBAS UNITARIAS CORREGIDAS Y REAL.xlsx
│   └── Pruebas_Unitarias_Liquidador_Nomina.xlsx
├── src/
│   ├── logica_nomina.py
│   └── consola.py
├── test/
│   └── tests_nomina.py
├── .gitignore
└── README.md
### Descripción de las carpetas

- `src/`: contiene la lógica principal para realizar el cálculo de la nómina.
- `test/`: contiene las pruebas unitarias desarrolladas con `unittest`.
- `docs/`: contiene la matriz original de casos de prueba de la primera entrega, la matriz actualizada de pruebas unitarias y el archivo de explicación del proyecto.
- `README.md`: contiene la descripción general del proyecto y las instrucciones para su ejecución.

## Ejecución de las pruebas unitarias

Para ejecutar las pruebas unitarias, ubicarse desde la terminal en la carpeta principal del proyecto y ejecutar:

```bash
python -m unittest test.tests_nomina
```

Actualmente el proyecto cuenta con 10 pruebas unitarias:

- 3 casos normales.
- 3 casos extraordinarios.
- 4 casos de error.

Si todas las pruebas se ejecutan correctamente, la terminal mostrará un resultado similar a:

```text
Ran 10 tests in ...
OK
```

## Ejecución de la interfaz de consola

Para ejecutar la interfaz de consola, ubicarse desde la terminal en la carpeta principal del proyecto y ejecutar:

```bash
python src/consola.py
```

La aplicación solicitará los siguientes datos:

- Salario básico.
- Días trabajados.
- Bonificación.
- Comisión.
- Otros descuentos.

Después de ingresar los datos, el programa calculará y mostrará el neto a pagar.

Ejemplo:

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
