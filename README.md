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
python -m pytest --cov=avistamientos --cov=app --cov=validador --cov-report=term-missing
```

En el informe se muestran las instrucciones ejecutadas, las que quedaron sin cubrir y el porcentaje de cobertura de cada archivo.

### Últimos resultados obtenidos

| Archivo o módulo | Cobertura |
|---|---:|
| `app.py` | 88 % |
| Rutas web | 100 % |
| Casos de uso | 100 % |
| Entidad y validador del dominio | 100 % |
| Repositorio SQLite | 100 % |
| Contrato del repositorio | 0 % |
| **Cobertura total** | **98 %** |

Estos resultados corresponden a la ejecución posterior al refactor en la rama `taller5-clean-architecture`, con Python 3.14.6, pytest 9.2.0 y pytest-cov 7.1.0. Se analizaron 182 sentencias y quedaron 4 sin cubrir. El porcentaje del contrato del repositorio es 0 % porque su archivo declara una interfaz/protocolo y no contiene lógica de ejecución que las pruebas necesiten invocar.

## Estructura del proyecto

En la rama `taller5-clean-architecture`, la API está organizada con Clean Architecture:

```text
api-avistamientos/
├── app.py
├── database.py
├── validador.py
├── avistamientos/
│   ├── domain/
│   │   ├── entities/avistamiento.py
│   │   └── services/validador.py
│   ├── application/
│   │   ├── ports/avistamiento_repository.py
│   │   └── use_cases/avistamientos.py
│   ├── adapters/web/routes.py
│   └── infrastructure/persistence/sqlite_avistamiento_repository.py
├── docs/
│   └── taller5_clean_architecture.md
└── tests/
    ├── test_api.py
    └── test_validador.py
```

### Descripción de los archivos y capas

- `app.py`: crea Flask y conecta los componentes.
- `database.py`: conserva la conexión y creación de la tabla SQLite.
- `avistamientos/domain`: contiene la entidad y las reglas de validación.
- `avistamientos/application`: define el contrato del repositorio y coordina los casos de uso.
- `avistamientos/adapters/web`: recibe las solicitudes HTTP mediante Flask.
- `avistamientos/infrastructure/persistence`: implementa las operaciones de persistencia con SQLite.
- `validador.py`: mantiene compatibilidad con las pruebas y código que importan el validador desde el módulo raíz.
- `tests`: contiene las pruebas de integración de la API y las pruebas unitarias del validador.
- `docs/taller5_clean_architecture.md`: contiene la investigación y el informe del taller.

## Repositorio

El código fuente del proyecto se encuentra disponible en GitHub:

https://github.com/lunaa06/api-avistamientos

## IA utilizada

Para el desarrollo de este proyecto se utilizaron ChatGPT y Gemini como herramientas de apoyo para comprender conceptos, estructurar el código, preparar pruebas y solucionar errores durante el desarrollo.

Las herramientas de inteligencia artificial se utilizaron como apoyo al proceso de aprendizaje, revisando y verificando el funcionamiento del código implementado.

## Autora

**Ana Luna**

Proyecto realizado para la asignatura de Ingeniería de Software 2.
