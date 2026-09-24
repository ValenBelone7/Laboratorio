# Lección 03: Módulos, paquetes, entornos virtuales, `uv` y APIs con `requests`

## Por qué importa

Hasta acá todo tu código vivió en **un solo archivo**, con lo que Python trae de fábrica. Ningún sistema real funciona así.

Pensá en tu inmobiliaria: los contratos se ajustan por ICL, y el ICL lo publica el Banco Central todos los días. Hoy eso lo hacés a mano (o alguien lo carga a mano). Lo que querés es un programa que:

1. Le pregunte al BCRA cuánto vale el ICL hoy → **consumir una API** (`requests`).
2. Calcule el monto actualizado de cada contrato → **lógica de negocio en su propio módulo**.
3. No se rompa cuando la API esté caída → lo que aprendiste en la lección 02.
4. Funcione igual en tu máquina, en la del cliente y en el servidor → **entorno virtual + dependencias fijadas**.

Los puntos 1, 2 y 4 son esta lección. Y hay algo más de fondo: cuando trabajás con "vibe coding", la IA te dice `pip install tal cosa` y vos lo corrés sin saber **dónde** se instaló ni **por qué** después otro proyecto dejó de andar. Al terminar esta lección eso se te termina.

---

## 1. Módulos: un archivo `.py` es un módulo

Un **módulo** es, literalmente, un archivo `.py`. Si tenés `calculos.py`, ya tenés un módulo llamado `calculos`.

```python
# calculos.py
IVA = 0.21

def aplicar_aumento(monto, porcentaje):
    return monto * (1 + porcentaje / 100)
```

```python
# main.py
import calculos

print(calculos.IVA)
print(calculos.aplicar_aumento(250000, 10))
```

### Las formas de importar

```python
import calculos                              # todo el módulo, se usa calculos.algo
import calculos as calc                       # con alias
from calculos import aplicar_aumento          # solo una cosa, se usa directo
from calculos import aplicar_aumento, IVA     # varias
from calculos import *                        # ❌ NUNCA hagas esto
```

¿Por qué `import *` es malo? Porque trae todos los nombres del módulo al tuyo, sin que vos sepas cuáles. Si `calculos` define una función `round()`, te acaba de pisar la `round()` de Python y no vas a entender por qué tu código hace cosas raras. **Explícito es mejor que implícito** (esto es literalmente una línea del Zen de Python, escribí `import this` en la terminal y leelo).

### Qué pasa cuando importás

Al hacer `import calculos`, Python **ejecuta el archivo entero** de arriba a abajo, una sola vez, y guarda el resultado. Por eso esto es un problema:

```python
# calculos.py
def aplicar_aumento(monto, porcentaje):
    return monto * (1 + porcentaje / 100)

print(aplicar_aumento(100, 10))    # ⚠️ esto se ejecuta al importar el módulo
```

Cada vez que alguien haga `import calculos`, va a aparecer ese `print` de la nada.

### `if __name__ == "__main__":`

Esta es la solución, y es esa línea que venís copiando desde la lección 01 sin saber qué hace.

Python le pone a cada módulo una variable automática llamada `__name__`:

- Si el archivo **se está ejecutando directamente** (`python calculos.py`), `__name__` vale `"__main__"`.
- Si el archivo **fue importado** por otro, `__name__` vale el nombre del módulo (`"calculos"`).

```python
# calculos.py
def aplicar_aumento(monto, porcentaje):
    return monto * (1 + porcentaje / 100)

if __name__ == "__main__":
    # esto SOLO corre con: python calculos.py
    # NO corre cuando otro archivo hace: import calculos
    print(aplicar_aumento(100, 10))
```

Traducción: _"si me están corriendo a mí directamente, hacé esto; si me están importando, no hagas nada, solo ofrecé mis funciones"_. Por eso tus `ejercicios.py` terminan con `if __name__ == "__main__": verificar()`.

### Cómo encuentra Python los módulos

Cuando escribís `import requests`, Python busca en este orden:

1. Módulos built-in (los que vienen compilados con Python).
2. La carpeta desde donde ejecutaste el script.
3. Las rutas en `sys.path` (que incluyen el `site-packages` del entorno virtual activo).

```python
import sys
print(sys.path)   # probalo en la terminal, es una lista de carpetas
```

Esto explica el error más común del principiante: `ModuleNotFoundError: No module named 'requests'` no significa "no existe requests en el mundo", significa **"no lo encontré en NINGUNA de estas carpetas"** — casi siempre porque lo instalaste en otro entorno.

---

## 2. Paquetes: una carpeta de módulos

Un **paquete** es una carpeta que contiene módulos y un archivo `__init__.py`.

```
indices/
├── __init__.py
├── bcra.py
└── contratos.py
```

```python
from indices import bcra                    # importa el módulo bcra del paquete indices
from indices.bcra import obtener_serie_icl  # importa una función puntual
from indices.contratos import aplicar_ajuste_icl
```

### ¿Qué es `__init__.py`?

Es el archivo que se ejecuta cuando alguien importa el paquete. Puede estar **vacío** (y muchas veces lo está: solo marca "esta carpeta es un paquete"). También sirve para exponer una API pública más cómoda:

```python
# indices/__init__.py
from indices.bcra import obtener_serie_icl
from indices.contratos import aplicar_ajuste_icl
```

Con eso, quien use tu paquete puede escribir `from indices import aplicar_ajuste_icl` sin saber en qué archivo interno vive.

> Desde Python 3.3 existen los _namespace packages_, que funcionan sin `__init__.py`. Igual, para un paquete común y corriente, **ponelo**: es explícito y evita comportamientos raros.

### Imports absolutos vs relativos

```python
# absoluto: desde la raíz del proyecto (RECOMENDADO)
from indices.bcra import obtener_serie_icl

# relativo: desde el módulo actual
from .bcra import obtener_serie_icl      # . = mismo paquete
from ..otros import algo                 # .. = paquete padre
```

La guía de estilo oficial ([PEP 8](https://peps.python.org/pep-0008/#imports)) recomienda **absolutos**: se leen mejor y no se rompen si movés el archivo. Los relativos se usan sobre todo _dentro_ de un paquete grande.

### Orden de los imports (PEP 8)

Tres bloques, separados por una línea en blanco:

```python
import json                    # 1. librería estándar
import os

import requests                # 2. paquetes de terceros
from django.db import models

from indices.bcra import ultimo_valor   # 3. tu propio código
```

Es una convención, no una regla del lenguaje — pero en cualquier equipo profesional te la van a pedir (y herramientas como `ruff` te la ordenan solas).

---

## 3. Entornos virtuales: por qué existen

Imaginate que tenés dos proyectos:

- La inmobiliaria en producción, con **Django 4.2**.
- El laboratorio nuevo, donde querés probar **Django 6.0**.

Si instalás los paquetes "en la computadora" (global), los dos comparten la misma carpeta de librerías. Instalás Django 6.0 para el laboratorio y **acabás de romper el sistema en producción**. Esto se llama _dependency hell_ y es una de las formas más comunes de arruinar un viernes.

Un **entorno virtual** es una carpeta (`.venv/`) con su propio Python y su propio `site-packages`. Cada proyecto tiene el suyo, aislado de los demás.

```bash
python -m venv .venv          # crear (forma clásica)
source .venv/bin/activate     # activar (Linux/macOS)
deactivate                    # salir
```

Cuando el entorno está activo, `python` y `pip` apuntan a los de esa carpeta, no a los del sistema. Ese es todo el truco.

Regla de oro: **el `.venv/` NUNCA va a git**. Es pesado, es específico de tu máquina y se regenera en segundos. Lo que va a git es la _lista_ de lo que hay que instalar. Fijate que tu [.gitignore](.gitignore) ya lo excluye.

---

## 4. `uv`: la herramienta actual

Históricamente esto requería juntar cuatro o cinco herramientas: `pip` (instalar), `venv` (aislar), `pyenv` (versiones de Python), `pip-tools`/`poetry` (fijar versiones), `pipx` (herramientas globales).

**`uv`**, de Astral (los mismos de `ruff`), hace todo eso en un solo binario escrito en Rust, y es entre 10 y 100 veces más rápido que `pip`. Al día de hoy es el estándar de facto en proyectos Python nuevos. Ya lo tenés instalado (`uv 0.12.5`).

### El flujo completo

```bash
uv init --bare              # crea el pyproject.toml del proyecto
uv add requests             # agrega una dependencia (crea .venv y uv.lock solos)
uv add --dev pytest         # dependencia solo de desarrollo (no va a producción)
uv remove requests          # saca una dependencia
uv run python archivo.py    # ejecuta DENTRO del entorno, sin activarlo a mano
uv sync                     # recrea el entorno exacto a partir del lockfile
uv lock --upgrade           # actualiza las versiones fijadas
```

Lo importante: con `uv run` **no necesitás activar nada**. uv se fija que el entorno esté al día con el lockfile y recién ahí ejecuta tu comando.

### Los archivos que aparecen

| Archivo           | Qué es                                                                            | ¿Va a git? |
| ----------------- | --------------------------------------------------------------------------------- | ---------- |
| `pyproject.toml`  | Qué necesita tu proyecto (`requests>=2.32`), a grandes rasgos                     | ✅ Sí      |
| `uv.lock`         | Las versiones **exactas** de todo, incluidas las dependencias de tus dependencias | ✅ Sí      |
| `.venv/`          | El entorno real, con los paquetes instalados                                      | ❌ No      |
| `.python-version` | Qué versión de Python usa este proyecto                                           | ✅ Sí      |

Un `pyproject.toml` típico:

```toml
[project]
name = "laboratorio-dev"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.32.0",
]
```

### Por qué el lockfile importa tanto

`pyproject.toml` dice "quiero requests 2.32 o mayor". Eso el mes que viene puede resolverse a una versión distinta. `uv.lock` dice "requests 2.32.3, urllib3 2.2.1, certifi 2024.7.4, …" — **exactamente** lo mismo en tu máquina, en la de un compañero, en CI y en producción. Es la diferencia entre "en mi máquina anda" y un sistema reproducible.

En un servidor o en CI se usa `uv sync --locked`: si el lockfile quedó desactualizado respecto del `pyproject.toml`, falla ruidosamente en vez de instalar cualquier cosa.

---

## 5. `requests`: hablar con una API

Una API REST es un servidor al que le hacés un pedido HTTP y te contesta, casi siempre en JSON — el mismo JSON de la lección 02.

```python
import requests

respuesta = requests.get("https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias", timeout=10)
print(respuesta.status_code)   # 200
datos = respuesta.json()       # dict de Python
```

### Las partes de un request

```python
respuesta = requests.get(
    "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/40",
    params={"desde": "2026-09-01", "hasta": "2026-09-05"},   # va a la URL como ?desde=...&hasta=...
    headers={"User-Agent": "laboratorio-dev/0.1"},           # metadatos del pedido
    timeout=10,                                              # ⚠️ SIEMPRE
)
```

**El `timeout` no es opcional.** Sin él, `requests` espera **para siempre**. La documentación oficial lo dice con todas las letras: _"nearly all production code should use this parameter in nearly all requests"_. Un servidor que no contesta y un request sin timeout es un proceso colgado que nadie mata.

### Códigos de estado

| Código                        | Significa                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------- |
| 2xx (200, 201, 204)           | Salió bien                                                                               |
| 4xx (400, 401, 403, 404, 429) | **Vos** hiciste algo mal: parámetro inválido, sin permiso, no existe, demasiados pedidos |
| 5xx (500, 502, 503)           | **El servidor** falló                                                                    |

```python
respuesta.raise_for_status()   # lanza HTTPError si el código es 4xx o 5xx
```

Sin `raise_for_status()`, un 500 te devuelve un objeto `Response` normal, y tu código sigue como si nada hasta reventar más adelante en un lugar que no tiene nada que ver.

### Las excepciones de `requests`

Todas heredan de `requests.exceptions.RequestException`:

```
RequestException
├── ConnectionError      → no hay internet, DNS falla, servidor caído
│   └── Timeout          → tardó más que el timeout que pusiste
├── HTTPError            → lo lanza raise_for_status() ante 4xx/5xx
├── TooManyRedirects
└── JSONDecodeError      → la respuesta no era JSON válido
```

El patrón completo, juntando todo lo de la lección 02:

```python
import requests

def obtener_icl(desde, hasta):
    try:
        respuesta = requests.get(
            "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/40",
            params={"desde": desde, "hasta": hasta},
            timeout=10,
        )
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.Timeout:
        print("el BCRA tardó demasiado")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"el BCRA respondió con error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        # el comodín, pero acotado a errores de requests (no a cualquier bug)
        print(f"falló la conexión: {e}")
        return None
```

Fijate el orden: `Timeout` es subclase de `ConnectionError`, que es subclase de `RequestException`. Lo específico arriba, lo general abajo — la regla de la lección 02, aplicada a una jerarquía real.

### `requests` vs `httpx`

`httpx` es la alternativa moderna: API casi idéntica, pero además soporta `async/await` y HTTP/2. La recomendación actual: **`requests` para scripts, herramientas y llamadas sincrónicas** (es lo que vas a ver en el 90% del código Django existente); `httpx` cuando necesites concurrencia de verdad. Aprendé `requests` primero: lo que sabés se traslada casi línea por línea.

---

## 6. Caso real: el ICL del Banco Central

Esto no es un ejemplo inventado. El BCRA publica una API **pública y sin API key**:

**Base:** `https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias`

La variable **40** es _"Índice para Contratos de Locación (base 30.6.20=1)"_ — el ICL con el que se ajustan los alquileres.

```bash
curl "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/40?desde=2026-09-01&hasta=2026-09-05"
```

Respuesta real (recortada):

```json
{
  "status": 200,
  "metadata": { "resultset": { "count": 5, "offset": 0, "limit": 1000 } },
  "results": [
    {
      "idVariable": 40,
      "detalle": [
        { "fecha": "2026-09-05", "valor": 35.87 },
        { "fecha": "2026-09-04", "valor": 35.83 },
        { "fecha": "2026-09-03", "valor": 35.8 },
        { "fecha": "2026-09-02", "valor": 35.77 },
        { "fecha": "2026-09-01", "valor": 35.74 }
      ]
    }
  ]
}
```

Mirá la estructura: un dict, con una clave `"results"` que es una **lista**, cuyo primer elemento es un dict con la clave `"detalle"`, que es otra lista de dicts. Para llegar al primer valor:

```python
datos["results"][0]["detalle"][0]["valor"]    # 35.87
```

Esto es exactamente la lección 01 (diccionarios anidados y listas de diccionarios), pero con datos que vienen de afuera. Por eso las dos lecciones anteriores eran la base de esta.

### Cómo se usa el ICL en un contrato

El ICL es un índice acumulado: el ajuste es la **razón** entre el valor de hoy y el del inicio del contrato.

```
monto_actualizado = monto_original × (ICL_de_hoy / ICL_al_inicio)
```

Si un alquiler arrancó en $250.000 cuando el ICL valía 20.00, y hoy el ICL vale 35.87:

```
250000 × (35.87 / 20.00) = $448.375
```

### ⚠️ La trampa que solo se aprende quemándose

Probé esto contra la API real mientras armaba la lección. Si mandás la fecha mal formada (`01-09-2026` en vez de `2026-09-01`):

- La API **no** devuelve un error.
- Devuelve **HTTP 200**, ignora tu parámetro y te manda **240 registros** en vez de 5.

Es decir: `raise_for_status()` no salta, `.json()` funciona perfecto, y tu programa procesa datos que no pediste, convencido de que todo salió bien.

**Moraleja:** `status_code == 200` significa _"el servidor te respondió"_, no _"el servidor entendió lo que querías"_. En código serio, además de manejar excepciones, se **valida la forma de la respuesta**: ¿vino la cantidad de registros que esperaba? ¿están las claves que necesito? ¿las fechas caen en el rango que pedí? Esto es exactamente lo que en Django terminás haciendo con serializers.

---

## Errores comunes

| Error                                             | Causa                                                                           | Solución                                                 |
| ------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'requests'` | No está instalado **en el entorno activo**                                      | `uv add requests` y ejecutar con `uv run`                |
| `ImportError: cannot import name 'X' from 'Y'`    | El nombre no existe en ese módulo (typo, o está en otro archivo)                | Revisar el nombre exacto y el módulo correcto            |
| `ModuleNotFoundError` con tu propio paquete       | Estás ejecutando desde otra carpeta; la raíz del proyecto no está en `sys.path` | Ejecutar desde la raíz del proyecto                      |
| El programa queda colgado para siempre            | `requests.get()` sin `timeout`                                                  | Poner `timeout` siempre                                  |
| Procesás basura sin enterarte                     | Confiar en `status_code == 200`                                                 | `raise_for_status()` **y** validar la forma de los datos |
| Instalaste algo y "desapareció"                   | Lo instalaste en otro entorno (o global)                                        | Un `.venv` por proyecto, siempre                         |
| `from modulo import *`                            | Trae nombres invisibles y pisa los tuyos                                        | Imports explícitos                                       |
| El `.venv/` en el repo                            | No se ignoró                                                                    | `.gitignore` (el tuyo ya lo tiene)                       |

---

## Conexión con lo que viene

- **Django (Fase 2):** un proyecto Django _es_ un paquete de paquetes — cada "app" es un paquete con `__init__.py`, `models.py`, `views.py`. `settings.py` es un módulo que Django importa. Y `pip install django` dentro de un `.venv` va a ser el primer comando de la fase.
- **PostgreSQL (Fase 3):** el driver (`psycopg`) es una dependencia más en tu `pyproject.toml`; el lockfile es lo que garantiza que la versión del driver sea la misma en tu máquina y en el servidor.
- **IA (Fase 4):** el SDK de Claude (`anthropic`) se instala igual y se usa igual: un cliente HTTP con timeout, manejo de errores por tipo (rate limit, sobrecarga) y JSON de ida y de vuelta. Lo que aprendas acá con `requests` se traslada tal cual.
- **Tareas periódicas:** "actualizar el ICL todos los días a las 9" (que está en la hoja de ruta de la Fase 2) es esta lección + un scheduler.

---

## Resumen

| Concepto                 | Qué es                                     | Comando / sintaxis                     |
| ------------------------ | ------------------------------------------ | -------------------------------------- |
| Módulo                   | Un archivo `.py`                           | `import calculos`                      |
| Paquete                  | Carpeta con `__init__.py`                  | `from indices.bcra import ...`         |
| `__name__ == "__main__"` | "Solo si me ejecutan directo"              | `if __name__ == "__main__":`           |
| Entorno virtual          | Carpeta con Python y paquetes propios      | `.venv/`, nunca a git                  |
| `uv init --bare`         | Crea el `pyproject.toml`                   | —                                      |
| `uv add X`               | Instala y anota la dependencia             | crea `.venv` y `uv.lock`               |
| `uv run`                 | Ejecuta dentro del entorno                 | `uv run python x.py`                   |
| `uv sync`                | Recrea el entorno desde el lock            | `--locked` en CI                       |
| GET con `requests`       | Pedido HTTP                                | `requests.get(url, params=, timeout=)` |
| `raise_for_status()`     | Convierte 4xx/5xx en excepción             | dentro de un `try`                     |
| `RequestException`       | Padre de todas las excepciones de requests | específicas primero                    |

---

## Autoevaluación

Respondé sin mirar la teoría:

1. ¿Qué diferencia hay entre un módulo y un paquete? ¿Qué archivo convierte una carpeta en paquete?

La diferencia entre un modulo y un paquete, es que el modulo es un archivo .py que puede ser creado por mi e importado dentro de mi proyecto, en cambio un paquete es de un tercero con muchos modulos, se usa un gestor de paquetes para su instalacion dentro de un ambiente aislado del sistema general. El archivo init.py es el que da como indicio que es un paquete

2. Venís copiando `if __name__ == "__main__":` desde la lección 01. Ahora explicalo: ¿qué vale `__name__` en cada caso y qué problema evita esa línea?

Esa condicion le dice al modulo que si lo estan ejecutando directamente a el, realice las operaciones que hay debajo de la condicion. Pero que si lo estan importando, toma el nombre del modulo.py y no ejecuta lo que hay debajo de esa condicion. Evita que una importacion de un modulo realice operaciones o pise demas cosas del modulo main que se esta ejecutando directamente

3. ¿Por qué `uv.lock` va a git pero `.venv/` no, si los dos describen "lo que está instalado"?

El uv.lock contiene las versiones de las dependencias, mientras que .venv es muy pesado y contiene demas cosas

4. ¿Qué pasa si hacés `requests.get(url)` sin `timeout` y el servidor nunca responde?

Quedaria la conexion colgada infinitamente y crearia un trafico que consuma recursos en algo que esta muerto.

5. Una API te devuelve `200 OK`. ¿Podés asumir que los datos que te llegaron son los que pediste? Justificá con el caso del BCRA.

El HTTP Code no refiere a que la API o el pedido fue entendido como tu querias, sino que resuelve si el servidor te envio o no la respuesta. Puede enviar un 200 y que se salte parametros que tu le mandaste.
