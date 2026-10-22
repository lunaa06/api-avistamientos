\# Justificación de las pruebas de la API de avistamientos



\*\*Proyecto:\*\* API REST de avistamientos de aves  

\*\*Lenguaje:\*\* Python  

\*\*Herramientas:\*\* Flask, pytest y pytest-cov



\## 1. Qué cambió en el código y por qué



Se separó la validación de los datos en el archivo `validador.py` para que las reglas de negocio no quedaran mezcladas con las rutas de la API. El validador comprueba que la especie tenga entre 3 y 50 caracteres, que la fecha use el formato `AAAA-MM-DD`, que sea una fecha existente y que no sea posterior al día actual. También revisa que el lugar y el observador no estén vacíos y que los datos tengan la estructura esperada.



Esta separación permite probar la lógica de validación sin enviar solicitudes HTTP ni depender de la base de datos. Las rutas de `app.py` se prueban por separado para comprobar el comportamiento de la API.



También se encapsuló la fecha actual mediante `Reloj`. En las pruebas se usa `RelojFijo`, que devuelve el 21 de octubre de 2026. Así, los casos de la fecha de hoy y de mañana son repetibles y no dependen del día en que se ejecute la prueba.



\## 2. Tabla de casos de prueba unitarios



Se aplicó \*\*partición de equivalencia\*\* para separar entradas válidas e inválidas y \*\*análisis de valores límite\*\* para probar los extremos de las reglas. La especie debe tener entre 3 y 50 caracteres.



| Campo | Valor o condición | Tipo de caso | Resultado esperado y justificación |

|---|---|---|---|

| Especie | `Águila` | Representativo válido | Se acepta porque está dentro del rango permitido. |

| Especie | Texto de 2 caracteres | Límite inválido | Se rechaza por estar por debajo del mínimo de 3. |

| Especie | Texto de 3 caracteres | Límite válido | Se acepta porque alcanza el mínimo. |

| Especie | Texto de 50 caracteres | Límite válido | Se acepta porque coincide con el máximo. |

| Especie | Texto de 51 caracteres | Límite inválido | Se rechaza porque supera el máximo de 50. |

| Fecha | `2026-10-21` | Límite válido | Se acepta porque es la fecha fijada por `RelojFijo`. |

| Fecha | `2026-10-22` | Límite inválido | Se rechaza porque es el día siguiente. |

| Fecha | `21/10/2026` | Inválido | Se rechaza porque no cumple el formato `AAAA-MM-DD`. |

| Fecha | `2026-02-30` | Inválido | Se rechaza porque esa fecha no existe. |

| Lugar | Cadena vacía o espacios | Inválido | Se rechaza porque el lugar debe contener información. |

| Observador | Cadena vacía o espacios | Inválido | Se rechaza porque el observador debe contener información. |

| Datos recibidos | Valor que no sea un diccionario | Inválido | Se rechaza porque la estructura no es la esperada. |



Los casos de 2, 3, 50 y 51 caracteres comprueban ambos lados de los límites. Para la fecha, se distinguen el formato incorrecto, la fecha inexistente y la fecha futura porque son motivos de rechazo diferentes.



\## 3. Por qué usamos cada nivel de prueba



Las \*\*pruebas unitarias\*\* de `tests/test\_validador.py` comprueban la lógica de validación de forma aislada. Por ejemplo, una prueba con una especie de 2 caracteres verifica el límite mínimo sin necesitar que Flask atienda una petición ni que exista un registro en la base de datos.



Las \*\*pruebas de integración\*\* de `tests/test\_api.py` usan el cliente de pruebas de Flask para enviar solicitudes a las rutas. Comprueban la interacción entre la ruta, la validación, el acceso a los datos y las respuestas HTTP. Una prueba unitaria del validador no detectaría, por ejemplo, que una ruta no invoque el validador o construya una respuesta HTTP incorrecta.



Las pruebas de integración usan una base SQLite en memoria mediante una sustitución de la conexión empleada por la aplicación. Esto mantiene los datos aislados y evita depender de una base persistente o del orden de ejecución de las pruebas.



\## 4. Dobles de prueba utilizados



`RelojFijo` es un \*\*stub\*\*: devuelve una respuesta predeterminada, la fecha 21 de octubre de 2026, cuando el validador necesita conocer el día actual. Solo proporciona el dato necesario para la prueba.



Sin este stub, el resultado de la prueba de la fecha de mañana dependería del reloj del computador y podría dejar de ser válido con el paso del tiempo. El stub hace que la prueba sea repetible.



En las pruebas de integración también se reemplaza la conexión por una base SQLite en memoria, para mantener los datos de cada prueba aislados de la base real.



\## 5. Lo que decidimos no probar



1\. \*\*No se probó el arranque de un servidor real.\*\* Las pruebas usan el cliente de Flask, que permite comprobar las rutas sin abrir un servidor en un puerto. El bloque de ejecución directa de `app.py` no es necesario para verificar las respuestas HTTP de los endpoints.



2\. \*\*No se probaron servicios externos reales.\*\* La API no necesita llamar a un servicio externo para validar y gestionar avistamientos. Añadir llamadas externas introduciría dependencias que no hacen parte del comportamiento evaluado.



Estas decisiones delimitan el alcance: se priorizan las reglas de negocio y el comportamiento HTTP de la API, manteniendo las pruebas rápidas y repetibles.



\## 6. Lectura de la cobertura



El comando utilizado para obtener la cobertura fue:



```powershell

python -m pytest --cov=app --cov=validador --cov-report=term-missing

```



El resultado obtenido fue:



| Archivo | Sentencias | Sin cubrir | Cobertura |

|---|---:|---:|---:|

| `app.py` | 74 | 2 | 97 % |

| `validador.py` | 30 | 0 | 100 % |

| \*\*Total\*\* | \*\*104\*\* | \*\*2\*\* | \*\*98 %\*\* |



Las 24 pruebas finalizaron correctamente. `validador.py` tiene cobertura del 100 %; en `app.py` quedaron sin cubrir las líneas 175–176, correspondientes al bloque de ejecución directa que inicia la aplicación. Las pruebas usan el cliente de Flask y no necesitan arrancar el servidor real, por lo que no se considera necesario cubrir ese bloque en las pruebas de endpoints.



La cobertura muestra qué partes del código se ejecutaron, pero por sí sola no demuestra que todos los comportamientos estén bien comprobados. Por eso se combinó el reporte con pruebas de límites, entradas inválidas y pruebas de integración.



\## Comandos para ejecutar las pruebas



Para ejecutar todas las pruebas:



```powershell

python -m pytest -v

```



Para ejecutar las pruebas y mostrar la cobertura:



```powershell

python -m pytest --cov=app --cov=validador --cov-report=term-missing

```

