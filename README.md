# API REST de Avistamientos de Aves

## Descripción

Se creó una API REST que permite registrar, consultar, actualizar y eliminar avistamientos de aves, además de consultar un resumen de los registros por especie.

Cada avistamiento contiene la siguiente información:

- ID
- Especie
- Lugar
- Fecha
- Observador

El proyecto fue desarrollado utilizando Python, Flask y SQLite. También cuenta con un validador que comprueba los datos antes de crear o actualizar un registro.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- JSON
- REST API
- Pytest
- pytest-cov

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/lunaa06/api-avistamientos.git
```

### 2. Entrar a la carpeta del proyecto

```bash
cd api-avistamientos
```

### 3. Crear el entorno virtual

En Windows:

```powershell
python -m venv .venv
```

En macOS o Linux:

```bash
python3 -m venv .venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

En Windows CMD:

```cmd
.venv\Scripts\activate
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

### 5. Instalar las dependencias

```bash
python -m pip install Flask pytest pytest-cov
```

### 6. Ejecutar la API

```bash
python app.py
```

En macOS o Linux, si es necesario:

```bash
python3 app.py
```

La API quedará disponible en:

```text
http://127.0.0.1:5000
```

## Base de datos

El proyecto utiliza SQLite para almacenar los avistamientos.

La tabla se crea automáticamente al ejecutar la aplicación directamente con `python app.py`.

El archivo utilizado es:

```text
avistamientos.db
```

La tabla principal se llama `avistamientos` y contiene los siguientes campos:

- `id`
- `especie`
- `lugar`
- `fecha`
- `observador`

## Validación de datos

Antes de crear o actualizar un avistamiento, la API comprueba que los datos cumplan las siguientes reglas:

- La especie debe tener entre 3 y 50 caracteres.
- La fecha debe tener el formato `AAAA-MM-DD`.
- La fecha debe ser válida y no puede ser posterior al día actual.
- El lugar no puede estar vacío.
- El observador no puede estar vacío.
- El cuerpo recibido debe tener una estructura de datos válida.

Cuando los datos no cumplen las reglas, la API responde con el código HTTP `400` y un mensaje que explica el error.

## Endpoints

### GET `/`

Comprueba que la API esté funcionando.

**Respuesta:** `200 OK`

```json
{
  "mensaje": "API de avistamientos funcionando"
}
```

### GET `/avistamientos`

Obtiene todos los avistamientos registrados.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl http://127.0.0.1:5000/avistamientos
```

### GET `/avistamientos/{id}`

Obtiene un avistamiento específico utilizando su ID.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl http://127.0.0.1:5000/avistamientos/1
```

Si el avistamiento no existe, responde `404 Not Found`:

```json
{
  "error": "Avistamiento no encontrado"
}
```

### POST `/avistamientos`

Permite registrar un nuevo avistamiento.

Los campos requeridos son `especie`, `lugar`, `fecha` y `observador`.

**Respuesta:** `201 Created`

Ejemplo:

```bash
curl -X POST http://127.0.0.1:5000/avistamientos -H "Content-Type: application/json" -d "{\"especie\":\"Colibrí\",\"lugar\":\"Parque El Virrey\",\"fecha\":\"2026-10-21\",\"observador\":\"Ana\"}"
```

La respuesta contiene el registro creado, incluido su identificador.

Si los datos no cumplen las reglas de validación, responde `400 Bad Request`.

### PUT `/avistamientos/{id}`

Permite actualizar un avistamiento existente. Se deben enviar los campos requeridos y sus valores válidos.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl -X PUT http://127.0.0.1:5000/avistamientos/1 -H "Content-Type: application/json" -d "{\"especie\":\"Colibrí\",\"lugar\":\"Jardín Botánico\",\"fecha\":\"2026-10-21\",\"observador\":\"Ana\"}"
```

Si los datos son inválidos, responde `400 Bad Request`. Si el ID no existe, responde `404 Not Found`.

### DELETE `/avistamientos/{id}`

Elimina un avistamiento utilizando su ID.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl -X DELETE http://127.0.0.1:5000/avistamientos/1
```

Respuesta:

```json
{
  "mensaje": "Avistamiento eliminado correctamente"
}
```

Si el ID no existe, responde `404 Not Found`.

### GET `/avistamientos/resumen`

Muestra la cantidad de avistamientos registrados por cada especie.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl http://127.0.0.1:5000/avistamientos/resumen
```

La respuesta es una lista con la especie y la cantidad de registros encontrados.

## Pruebas automatizadas

Para verificar el funcionamiento del proyecto se utilizaron Pytest y el cliente de pruebas de Flask.

Las pruebas están organizadas en la carpeta `tests`:

- `test_validador.py`: contiene las pruebas unitarias para comprobar las reglas de validación de los datos.
- `test_api.py`: contiene las pruebas de integración para verificar los endpoints, sus códigos de respuesta y las operaciones sobre los registros.

### Ejecutar todas las pruebas

Desde la carpeta principal del proyecto, ejecuta:

```powershell
python -m pytest -v
```

### Resultado de las pruebas

En la última ejecución se obtuvieron los siguientes resultados:

- Pruebas aprobadas: **24 de 24**.
- No se registraron pruebas fallidas.

## Cobertura del código

Para medir la cobertura de las pruebas se utilizó pytest-cov.

Ejecuta el siguiente comando:

```powershell
python -m pytest --cov=app --cov=validador --cov-report=term-missing
```

En el informe se muestran las instrucciones ejecutadas, las que quedaron sin cubrir y el porcentaje de cobertura de cada archivo.

### Últimos resultados obtenidos

| Archivo | Cobertura |
|---|---:|
| `app.py` | 97 % |
| `validador.py` | 100 % |
| **Cobertura total** | **98 %** |

Las dos líneas que quedaron sin cubrir corresponden al bloque que crea la tabla e inicia el servidor cuando `app.py` se ejecuta directamente. Las pruebas de los endpoints utilizan el cliente de pruebas de Flask y no necesitan iniciar el servidor real.

## Estructura del proyecto

```text
api-avistamientos/
├── app.py
├── database.py
├── validador.py
├── avistamientos.db
├── README.md
├── .gitignore
└── tests/
    ├── test_api.py
    └── test_validador.py
```

### Descripción de los archivos

- `app.py`: contiene la aplicación Flask y los endpoints de la API.
- `database.py`: contiene la conexión y la creación de la tabla de SQLite.
- `validador.py`: contiene las reglas para validar los datos de los avistamientos.
- `avistamientos.db`: almacena los registros de la base de datos.
- `tests/test_api.py`: contiene las pruebas de integración de la API.
- `tests/test_validador.py`: contiene las pruebas unitarias del validador.
- `README.md`: contiene la documentación del proyecto.
- `.gitignore`: indica los archivos y carpetas que Git no debe subir al repositorio.

## Repositorio

El código fuente del proyecto se encuentra disponible en GitHub:

https://github.com/lunaa06/api-avistamientos

## IA utilizada

Para el desarrollo de este proyecto se utilizaron ChatGPT y Gemini como herramientas de apoyo para comprender conceptos, estructurar el código, preparar pruebas y solucionar errores durante el desarrollo.

Las herramientas de inteligencia artificial se utilizaron como apoyo al proceso de aprendizaje, revisando y verificando el funcionamiento del código implementado.

## Autora

**Ana Luna**

Proyecto realizado para la asignatura de Ingeniería de Software 2.
