# Liquidador de Nómina

## Integrantes

- Yeisner Giraldo
- Samuel Garcia
- Sebastian Leal
- David Rios

## Descripción

Aplicación desarrollada en Python para calcular el neto a pagar de una nómina a partir del salario básico, los días trabajados, las bonificaciones, las comisiones y otros descuentos.

La aplicación permite:

- Calcular el neto a pagar.
- Validar los datos ingresados.
- Guardar nóminas en PostgreSQL.
- Buscar nóminas mediante su identificador UUID.
- Crear y eliminar la tabla de nóminas desde el controlador.
- Interactuar mediante una interfaz gráfica desarrollada con Kivy.

También conserva una interfaz de consola para realizar el cálculo de nómina.

## Entrega 4: persistencia en PostgreSQL

La persistencia sigue el modelo ORM manual trabajado en clase: los datos se representan mediante objetos de Python y el controlador realiza su correspondencia con las filas de PostgreSQL utilizando `psycopg2`.

La implementación incluye:

- Una clase de modelo para representar la nómina.
- Un controlador para conectar, insertar, buscar, crear y borrar tablas.
- Consultas SQL parametrizadas.
- Identificadores UUID generados en Python.
- Configuración privada de conexión separada del código.
- Pruebas automatizadas con fixtures.
- Funciones de guardar y buscar desde la interfaz gráfica.

## Entradas y resultado

### Entradas

| Campo | Descripción |
|---|---|
| Salario básico | Salario mensual del empleado. |
| Días trabajados | Número entero entre 0 y 30. |
| Bonificación | Valor de las bonificaciones. |
| Comisión | Valor de las comisiones. |
| Otros descuentos | Descuentos adicionales. |

Los valores monetarios deben ser numéricos y no negativos. Para escribir decimales se utiliza punto.

### Procesamiento

1. Validar los datos.
2. Calcular el salario proporcional a los días trabajados.
3. Incorporar bonificaciones y comisiones.
4. Calcular las deducciones de salud y pensión.
5. Aplicar los otros descuentos.
6. Obtener el neto a pagar.

### Resultado

La interfaz muestra el neto a pagar con formato monetario. Al guardar, también muestra el UUID que permite recuperar la nómina posteriormente.

## Organización del proyecto

| Ruta | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada de la interfaz gráfica. |
| `src/model/datos_nomina.py` | Clase `DatosNomina` e identificador UUID. |
| `src/model/constantes.py` | Constantes utilizadas en el cálculo. |
| `src/model/errores.py` | Errores personalizados de la aplicación. |
| `src/model/validacion.py` | Validación de las reglas de negocio. |
| `src/model/logica_nomina.py` | Funciones de cálculo de nómina. |
| `src/controller/nomina_controller.py` | Conexión y operaciones con PostgreSQL. |
| `src/view/Gui/liquidador.py` | Interfaz gráfica en Kivy. |
| `src/view/console/consola.py` | Interfaz de consola para calcular. |
| `sql/crear_tablas.sql` | Definición de la tabla `nominas`. |
| `tests/tests_nomina.py` | Pruebas de la lógica de negocio. |
| `tests/test_nomina_controller.py` | Pruebas de persistencia y fixtures. |
| `secret_config_sample.py` | Plantilla de configuración sin credenciales privadas. |
| `secret_config.py` | Configuración privada local, excluida de Git. |
| `requirements.txt` | Dependencias de Python. |
| `migrar_uuid.py` | Migración de la tabla anterior con ID entero a UUID. |
| `docs/` | Evidencias y documentación. |
| `README.md` | Instrucciones de instalación, configuración y ejecución. |

## Requisitos

- Python 3.12 o superior.
- PostgreSQL local o un servicio PostgreSQL remoto.
- Acceso a una base de datos y sus credenciales.
- Kivy.
- `psycopg2-binary`.
- Conexión a Internet si la base de datos está alojada en un servidor remoto.

Las instrucciones siguientes están preparadas para Windows y PowerShell.

## Instalación

### 1. Obtener el proyecto

```powershell
git clone https://github.com/David-Giraldo01/Liquidador-Nomina.git
cd Liquidador-Nomina
```

Si ya tienes el proyecto, abre una terminal en su carpeta principal.

### 2. Crear el entorno virtual

```powershell
py -m venv .venv
```

### 3. Instalar las dependencias

El archivo `requirements.txt` debe incluir:

```text
kivy
psycopg2-binary
```

Instala las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Los comandos de este documento utilizan directamente el intérprete del entorno virtual, por lo que no es necesario activarlo.

## Crear la base de datos

La base de datos debe existir antes de ejecutar las operaciones del controlador.

### Opción A: PostgreSQL local

1. Instala PostgreSQL.
2. Conéctate al servidor desde pgAdmin u otro cliente PostgreSQL.
3. Abre una ventana de consultas sobre una base existente, por ejemplo `postgres`.
4. Ejecuta esta instrucción por separado, fuera de una transacción explícita:

```sql
CREATE DATABASE nomina_db;
```

El usuario que ejecute la instrucción debe tener permiso para crear bases de datos.

Después, utiliza `nomina_db` como nombre de la base de datos en la configuración del proyecto.

### Opción B: PostgreSQL remoto

Si utilizas un servicio como Render:

1. Crea una instancia PostgreSQL en tu cuenta.
2. Obtén el host externo, el puerto, el nombre de la base de datos, el usuario y la contraseña.
3. Verifica que el servicio permita conexiones desde tu equipo.
4. Registra esos datos únicamente en tu archivo local `secret_config.py`.

Si el proveedor ya creó la base de datos, no es necesario ejecutar `CREATE DATABASE`.

## Configurar la conexión

### 1. Crear el archivo privado

Si todavía no existe `secret_config.py`, copia la plantilla desde el explorador de archivos o ejecuta:

```powershell
Copy-Item secret_config_sample.py secret_config.py
```

No ejecutes este comando sobre una configuración existente que quieras conservar.

### 2. Completar la configuración

Edita `secret_config.py` con tus propios datos:

```python
HOST = "localhost"
PORT = 5432
DATABASE = "nomina_db"
USER = "tu_usuario"
PASSWORD = "tu_contrasena"
SSLMODE = "prefer"
```

Para una conexión remota que requiera SSL, utiliza:

```python
SSLMODE = "require"
```

En ese caso, también debes sustituir `HOST`, `DATABASE`, `USER` y `PASSWORD` por los valores proporcionados por el servicio.

`secret_config_sample.py` debe conservar solamente valores de ejemplo e instrucciones para copiarlo y completar la configuración.

### 3. Proteger las credenciales

El archivo `.gitignore` debe incluir:

```gitignore
secret_config.py
.venv/
__pycache__/
*.pyc
```

Para comprobar que la configuración privada está ignorada:

```powershell
git check-ignore -v secret_config.py
```

Para comprobar que no está siendo rastreada por Git:

```powershell
git ls-files secret_config.py
```

Este último comando no debe mostrar ninguna ruta.

No publiques contraseñas, cadenas de conexión privadas ni capturas que las contengan.

### 4. Verificar la conexión

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); from controller.nomina_controller import NominaController; c = NominaController.conectar(); print('Conexion correcta'); c.close()"
```

El resultado esperado es:

```text
Conexion correcta
```

## Crear la tabla de nóminas

Con la base de datos creada y la conexión configurada, ejecuta:

```powershell
.\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); from controller.nomina_controller import NominaController; NominaController.crear_tablas(); print('Tabla creada correctamente')"
```

El controlador lee y ejecuta `sql/crear_tablas.sql`.

La tabla tiene esta estructura:

```sql
CREATE TABLE nominas (
    id_nomina UUID PRIMARY KEY,
    salario NUMERIC(15, 2) NOT NULL CHECK (salario >= 0),
    dias INTEGER NOT NULL CHECK (dias BETWEEN 0 AND 30),
    bonificacion NUMERIC(15, 2) NOT NULL CHECK (bonificacion >= 0),
    comision NUMERIC(15, 2) NOT NULL CHECK (comision >= 0),
    descuentos NUMERIC(15, 2) NOT NULL CHECK (descuentos >= 0)
);
```

Si la tabla ya existe, la creación genera un error de tabla duplicada. Este comportamiento está contemplado en las pruebas automatizadas.

No es necesario crear la tabla cada vez que se ejecuta la aplicación.

## Modelo e identificadores UUID

La clase `DatosNomina` representa los datos de una nómina:

- `salario`
- `dias`
- `bonificacion`
- `comision`
- `descuentos`
- `id_nomina`

Cada objeto nuevo recibe por defecto un identificador generado en Python mediante:

```python
str(uuid4())
```

PostgreSQL almacena ese identificador en una columna de tipo `UUID`.

El identificador no es autoincremental. Para consultar una nómina debe utilizarse su UUID completo.

## Operaciones del controlador

La clase `NominaController` implementa:

| Método | Función |
|---|---|
| `conectar()` | Abre una conexión utilizando `secret_config.py`. |
| `validar_id(id_nomina)` | Verifica y normaliza el formato del UUID. |
| `insertar(nomina)` | Ejecuta `INSERT INTO` y devuelve el identificador guardado. |
| `buscar(id_nomina)` | Ejecuta `SELECT` y reconstruye un objeto `DatosNomina`. |
| `crear_tablas()` | Ejecuta el archivo SQL de creación. |
| `borrar_tablas()` | Elimina la tabla `nominas`. |

Las inserciones y búsquedas utilizan parámetros `%s` de `psycopg2` para enviar los valores por separado de las instrucciones SQL.

Las operaciones cierran sus conexiones al terminar. Los bloques transaccionales confirman los cambios cuando la operación finaliza correctamente y los revierten si ocurre un error.

## Ejecutar la interfaz gráfica

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe main.py
```

### Calcular

1. Completa los cinco campos.
2. Presiona **Calcular**.
3. Consulta el valor mostrado en **Neto a pagar**.

### Guardar una nómina

1. Ingresa los datos.
2. Presiona **Guardar nómina en la base de datos**.
3. La aplicación valida la información y calcula el resultado.
4. Si la inserción tiene éxito, muestra una confirmación.
5. Copia el UUID que aparece en el campo de búsqueda.

Cada nueva operación de guardado genera un registro con un UUID nuevo.

### Buscar una nómina

1. Pega el UUID completo en el campo inferior.
2. Presiona **Buscar por ID**.
3. La aplicación consulta PostgreSQL.
4. Si encuentra el registro, carga sus datos en el formulario y calcula el neto a pagar.

### Limpiar

Presiona **Limpiar** para vaciar los campos y restablecer el resultado.

Limpiar el formulario no elimina las nóminas guardadas en PostgreSQL.

### Manejo de errores

La interfaz presenta mensajes cuando:

- Los campos no contienen datos válidos.
- Se incumplen las reglas de negocio.
- El UUID tiene un formato incorrecto.
- No existe una nómina con el UUID consultado.
- Ocurre un problema de conexión u operación con PostgreSQL.

## Ejemplo de uso

Ingresa:

| Campo | Valor |
|---|---:|
| Salario básico | 3000000 |
| Días trabajados | 30 |
| Bonificación | 0 |
| Comisión | 0 |
| Otros descuentos | 0 |

El resultado esperado es:

```text
Neto a pagar: $ 2,760,000.00
```

Para comprobar la persistencia:

1. Guarda la nómina.
2. Copia su UUID.
3. Limpia el formulario.
4. Pega el UUID y realiza la búsqueda.
5. Comprueba que se recuperan los mismos datos y el mismo resultado.

Para comprobar la validación del identificador, escribe `abc` y presiona **Buscar por ID**.

La aplicación debe mostrar:

```text
El ID debe tener un formato UUID válido.
Copia el identificador completo de una nómina guardada.
```

## Ejecutar la interfaz de consola

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m src.view.console.consola
```

La interfaz de consola solicita los datos y muestra el resultado del cálculo.

Las funciones de guardar y buscar nóminas de esta entrega se utilizan desde la interfaz gráfica.

## Eliminar la tabla

**Esta operación elimina la tabla `nominas` y todos sus registros. Úsala únicamente cuando quieras borrar esos datos.**

```powershell
.\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); from controller.nomina_controller import NominaController; NominaController.borrar_tablas(); print('Tabla eliminada')"
```

Después de eliminarla, puedes crear nuevamente una tabla vacía utilizando el comando de creación.

Si la tabla no existe, la eliminación genera un error. Este caso está incluido en las pruebas.

## Pruebas automatizadas

El proyecto cuenta con **22 pruebas automatizadas**:

- **10 pruebas de la lógica de negocio.**
- **12 pruebas del controlador de base de datos.**

### Fixtures de base de datos

Cada prueba del controlador:

1. Crea un esquema de prueba con un nombre único.
2. Configura sus conexiones para utilizar exclusivamente ese esquema.
3. Crea la tabla mediante el controlador.
4. Ejecuta el caso de prueba.
5. Elimina el esquema y sus tablas al finalizar.

De esta manera, las pruebas no borran ni modifican las nóminas de la tabla principal.

El usuario de PostgreSQL debe tener permiso para crear esquemas en la base de datos configurada.

### Casos del controlador

| N.º | Caso | Resultado esperado |
|---|---|---|
| 1 | Insertar una nómina válida y buscarla | Recupera los mismos datos y el UUID generado. |
| 2 | Insertar y buscar valores con centavos | Conserva los valores monetarios. |
| 3 | Buscar una nómina entre varios registros | Devuelve el registro correspondiente al UUID. |
| 4 | Insertar salario negativo | Rechaza el registro y no lo guarda. |
| 5 | Insertar más de 30 días | Rechaza el registro y no lo guarda. |
| 6 | Insertar un UUID duplicado | Rechaza el duplicado y conserva el original. |
| 7 | Buscar un UUID inexistente | Informa que no existe la nómina. |
| 8 | Buscar con un UUID inválido | Rechaza el formato del identificador. |
| 9 | Crear la tabla después de eliminarla | Permite insertar y consultar nuevamente. |
| 10 | Crear una tabla que ya existe | Genera el error esperado. |
| 11 | Eliminar una tabla existente | La tabla deja de estar disponible. |
| 12 | Eliminar una tabla que no existe | Genera el error esperado. |

Los casos cubren comportamientos normales y de error para insertar, buscar, crear y eliminar tablas.

### Ejecutar las pruebas de lógica

```powershell
.\.venv\Scripts\python.exe -m unittest tests.tests_nomina -v
```

### Ejecutar las pruebas del controlador

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_nomina_controller -v
```

Estas pruebas necesitan una conexión válida a PostgreSQL.

### Ejecutar todas las pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest tests.tests_nomina tests.test_nomina_controller -v
```

En la ejecución verificada se obtuvo:

```text
Ran 22 tests in ...

OK
```

El tiempo de ejecución depende del equipo y de la conexión con PostgreSQL.

## Migración de la versión anterior a UUID

Esta sección aplica únicamente a una base de datos anterior cuya columna `id_nomina` sea de tipo `INTEGER`.

Las instalaciones nuevas crean directamente la tabla con UUID y no necesitan ejecutar la migración.

El archivo `migrar_uuid.py`:

1. Comprueba el tipo del identificador.
2. Crea la tabla de respaldo `public.nominas_respaldo_enteros`.
3. Genera UUID en Python para los registros existentes.
4. Conserva en el respaldo la relación entre el ID anterior y el UUID nuevo.
5. Cambia la columna principal a tipo UUID.
6. Verifica que se conservaron los datos antes de confirmar los cambios.

Para ejecutar la migración:

```powershell
.\.venv\Scripts\python.exe migrar_uuid.py
```

Si la tabla ya utiliza UUID, el script informa que no se necesitan cambios.

El respaldo no se sobrescribe si ya existe. Si ocurre un error antes de confirmar la transacción, los cambios de esa ejecución se revierten.

## Evidencias

### Consulta de una nómina por UUID

![Consulta de nómina por UUID](docs/consulta_nomina.png)

### Validación de un identificador incorrecto

![Mensaje de UUID inválido](docs/error_consulta_nomina.png)

## Solución de problemas

| Problema | Qué revisar |
|---|---|
| No se encuentra `secret_config` | Copiar la plantilla a `secret_config.py` en la raíz del proyecto. |
| Error de autenticación | Verificar usuario, contraseña y nombre de la base de datos. |
| No se puede conectar al servidor | Revisar host, puerto, disponibilidad del servidor, acceso de red y SSL. |
| La tabla `nominas` no existe | Ejecutar la creación de tablas. |
| La tabla `nominas` ya existe | No repetir la creación; continuar con la aplicación. |
| El UUID es inválido | Copiar el identificador completo de una nómina guardada. |
| No existe la nómina consultada | Comprobar el UUID y que se esté usando la base de datos correcta. |
| No se encuentra Kivy o psycopg2 | Instalar `requirements.txt` con el intérprete de `.venv`. |
| Las pruebas no pueden crear esquemas | Revisar los permisos del usuario de PostgreSQL. |

## Alcance de la entrega

Esta entrega incorpora persistencia en PostgreSQL, operaciones del controlador, pruebas automatizadas y funciones de guardar y buscar desde Kivy.

Las instrucciones de este documento corresponden a la ejecución desde el código fuente. Los ejecutables o APK de versiones anteriores no garantizan incluir estas funcionalidades.