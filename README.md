# API REST de Avistamientos de Aves

## Descripción

Se creó una API REST que permite registrar y consultar avistamientos de aves.

Cada avistamiento contiene la siguiente información:

- ID
- Especie
- Lugar
- Fecha
- Observador

El proyecto fue desarrollado utilizando Python, Flask y SQLite.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- JSON
- REST API

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

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 5. Instalar Flask

```bash
pip install flask
```

### 6. Ejecutar la API

```bash
python app.py
```

La API quedará disponible en:

```text
http://127.0.0.1:5000
```

## Base de datos

El proyecto utiliza SQLite para almacenar los avistamientos.

La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.

El archivo utilizado es:

```text
avistamientos.db
```

La tabla principal se llama:

```text
avistamientos
```

Y contiene los siguientes campos:

- `id`
- `especie`
- `lugar`
- `fecha`
- `observador`

## Endpoints

### GET /avistamientos

Obtiene todos los avistamientos registrados.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl.exe http://127.0.0.1:5000/avistamientos
```

Respuesta:

```json
[
    {
        "id": 1,
        "especie": "Colibrí",
        "lugar": "Parque El Virrey",
        "fecha": "2026-10-06",
        "observador": "Ana"
    }
]
```

### GET /avistamientos/{id}

Obtiene un avistamiento específico utilizando su ID.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl.exe http://127.0.0.1:5000/avistamientos/1
```

Si el avistamiento no existe:

**Respuesta:** `404 Not Found`

```json
{
    "error": "Avistamiento no encontrado"
}
```

### POST /avistamientos

Permite registrar un nuevo avistamiento.

Los campos requeridos son:

- `especie`
- `lugar`
- `fecha`
- `observador`

**Respuesta:** `201 Created`

Ejemplo:

```bash
curl.exe -X POST http://127.0.0.1:5000/avistamientos -H "Content-Type: application/json" --data "{\"especie\":\"Colibrí\",\"lugar\":\"Parque El Virrey\",\"fecha\":\"2026-10-06\",\"observador\":\"Ana\"}"
```

Respuesta:

```json
{
    "id": 1,
    "especie": "Colibrí",
    "lugar": "Parque El Virrey",
    "fecha": "2026-10-06",
    "observador": "Ana"
}
```

Si falta alguno de los campos requeridos:

**Respuesta:** `400 Bad Request`

Ejemplo:

```json
{
    "error": "Falta el campo: especie"
}
```

### PUT /avistamientos/{id}

Permite actualizar un avistamiento existente.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl.exe -X PUT http://127.0.0.1:5000/avistamientos/1 -H "Content-Type: application/json" --data "{\"especie\":\"Colibrí\",\"lugar\":\"Jardín Botánico\",\"fecha\":\"2026-10-07\",\"observador\":\"Ana\"}"
```

Respuesta:

```json
{
    "id": 1,
    "especie": "Colibrí",
    "lugar": "Jardín Botánico",
    "fecha": "2026-10-07",
    "observador": "Ana"
}
```

Si el ID no existe:

**Respuesta:** `404 Not Found`

```json
{
    "error": "Avistamiento no encontrado"
}
```

### DELETE /avistamientos/{id}

Permite eliminar un avistamiento utilizando su ID.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl.exe -X DELETE http://127.0.0.1:5000/avistamientos/1
```

Respuesta:

```json
{
    "mensaje": "Avistamiento eliminado correctamente"
}
```

Si el ID no existe:

**Respuesta:** `404 Not Found`

```json
{
    "error": "Avistamiento no encontrado"
}
```

## Endpoint adicional: Resumen

### GET /avistamientos/resumen

Muestra la cantidad de avistamientos registrados por cada especie.

**Respuesta:** `200 OK`

Ejemplo:

```bash
curl.exe http://127.0.0.1:5000/avistamientos/resumen
```

Respuesta:

```json
[
    {
        "cantidad": 1,
        "especie": "Águila"
    },
    {
        "cantidad": 1,
        "especie": "Colibrí"
    }
]
```

## Estructura del proyecto

```text
api-avistamientos/
│
├── app.py
├── database.py
├── avistamientos.db
├── README.md
├── .gitignore
└── .venv/
```

### Descripción de los archivos

- `app.py`: contiene la aplicación Flask y los endpoints de la API.
- `database.py`: contiene la conexión y creación de la base de datos SQLite.
- `avistamientos.db`: almacena los datos de los avistamientos.
- `README.md`: contiene la documentación del proyecto.
- `.gitignore`: indica los archivos y carpetas que Git no debe subir al repositorio.
- `.venv/`: contiene el entorno virtual de Python.

## Repositorio

El código fuente del proyecto se encuentra disponible en GitHub:

https://github.com/lunaa06/api-avistamientos

## IA utilizada

Para el desarrollo de este proyecto se utilizó Chat gpt y Gemini como herramientas de apoyo para comprender conceptos, estructurar el código, realizar pruebas y solucionar errores durante el desarrollo.

La herramienta de IA fue utilizada como apoyo, comprendiendo y verificando el funcionamiento del código implementado.

## Autora

**Ana Luna**

Proyecto realizado para la asignatura de Ingeniería de Software 2.