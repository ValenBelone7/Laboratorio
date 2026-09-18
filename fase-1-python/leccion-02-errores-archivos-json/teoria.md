# Lección 02: Manejo de errores, archivos y JSON

## Por qué importa

Hasta ahora tus programas asumían que todo sale bien: el archivo existe, el dato que llega es del tipo que esperás, la cuenta nunca se divide por cero. En el trabajo real eso no pasa nunca:

- Un inquilino escribe "diez mil" en un campo que esperaba un número.
- La API de Binance está caída y tu request no devuelve nada.
- El archivo `contratos.json` de un cliente viejo tiene un typo y no es JSON válido.
- Django, cuando buscás un objeto que no existe (`Contrato.objects.get(id=999)`), no devuelve `None`: **lanza una excepción** (`DoesNotExist`).

Un programa que no maneja esto no "no anda": explota en producción, con un cliente mirando, en el peor momento. Esta lección es sobre eso: anticipar lo que puede salir mal y decidir con precisión qué hacer en cada caso, en vez de dejar que el programa se caiga o, peor, tragarse el error en silencio.

---

## 1. Excepciones específicas

Cuando algo sale mal, Python no sigue ejecutando: **lanza (raise) una excepción**, y si nadie la atrapa, el programa se cae mostrando un traceback.

```python
def calcular_cuota(monto_total, cantidad_cuotas):
    return monto_total / cantidad_cuotas

calcular_cuota(300000, 0)
# ZeroDivisionError: division by zero
```

Para no dejar que se caiga, usás `try`/`except`, indicando **qué excepción esperás**:

```python
try:
    cuota = monto_total / cantidad_cuotas
except ZeroDivisionError:
    print("No se puede dividir en 0 cuotas")
```

### La regla de oro: nunca atrapes lo que no esperás

```python
# ❌ MAL: "except" pelado (bare except) o except Exception genérico
try:
    cuota = monto_total / cantidad_cuotas
except:
    print("algo salió mal")
```

El problema: esto también atrapa un `KeyboardInterrupt` (Ctrl+C), un `NameError` por una variable mal escrita, o cualquier bug tuyo. Vas a estar buscando un error durante horas porque el programa "no rompe", solo hace algo raro y sigue. La [documentación oficial de Python](https://docs.python.org/3/tutorial/errors.html) es explícita: atrapá la excepción concreta que podés manejar, y dejá que las demás se propaguen.

```python
# ✅ BIEN: específico, y si no sé qué es, la relanzo
try:
    cuota = monto_total / cantidad_cuotas
except ZeroDivisionError:
    print("No se puede dividir en 0 cuotas")
except TypeError:
    print("monto_total y cantidad_cuotas tienen que ser números")
```

### Varios `except`: el orden importa

Podés encadenar varios `except`. Python revisa de arriba hacia abajo y ejecuta el **primero que coincida**. Si tenés excepciones que heredan una de otra, la más específica (la subclase) tiene que ir **primero**, porque un `except` de la clase base también atrapa a sus subclases:

```python
try:
    valor = int(texto)
except ValueError:      # más específico: subclase de Exception
    print("no es un número")
except Exception:       # comodín, va al final
    print("error inesperado")
```

Si pusieras `except Exception` primero, nunca llegarías a leer el `except ValueError`: el genérico se lo come todo.

### Capturar el objeto de la excepción

`as e` te da acceso al objeto, con el mensaje y los datos del error:

```python
try:
    edad = int("veinte")
except ValueError as e:
    print(f"Error: {e}")   # Error: invalid literal for int() with base 10: 'veinte'
```

---

## 2. El bloque `else`: separar el éxito del fracaso

`else` en un `try` se ejecuta **solo si NO hubo excepción**. Sirve para separar "lo que puede fallar" de "lo que hago cuando salió bien", así el `except` no atrapa por error algo que no tenía que atrapar.

```python
try:
    cuota = monto_total / cantidad_cuotas
except ZeroDivisionError:
    print("no se puede dividir en 0 cuotas")
else:
    print(f"cada cuota es de ${cuota:.2f}")
```

Compará con la versión sin `else`, donde metés todo dentro del `try`:

```python
# funciona, pero si el print() de acá abajo tuviera un bug,
# ese error también caería (por error) en el except de arriba
try:
    cuota = monto_total / cantidad_cuotas
    print(f"cada cuota es de ${cuota:.2f}")
except ZeroDivisionError:
    print("no se puede dividir en 0 cuotas")
```

Regla práctica: en el `try` va **solo** la línea que puede fallar. Todo lo que depende de que haya salido bien va en `else`.

---

## 3. `finally`: lo que se ejecuta siempre

`finally` corre **sí o sí**: haya excepción, no la haya, o esté capturada. Se usa para limpieza de recursos: cerrar un archivo, cerrar una conexión a la base, liberar un lock.

```python
try:
    conexion = abrir_conexion_exchange()
    hacer_operacion(conexion)
except ConexionError:
    print("no se pudo conectar")
finally:
    cerrar_conexion(conexion)   # se ejecuta pase lo que pase
```

Detalle importante: si tenés un `return` dentro de un `try` **y** dentro de un `finally`, gana el del `finally` — pisa el otro. Es una fuente de bugs silenciosos, así que evitá poner `return` en un `finally`.

---

## 4. `raise`: lanzar excepciones a propósito

Hasta ahora viste excepciones que lanza Python solo (`ZeroDivisionError`, `ValueError`). Pero también podés lanzar una vos, cuando detectás una regla de negocio violada:

```python
def validar_monto(monto):
    if monto <= 0:
        raise ValueError("El monto tiene que ser positivo")
    return monto
```

Esto es distinto de devolver `None` o imprimir un error: `raise` **corta la ejecución ahí mismo** y obliga a quien llamó a la función a lidiar con el problema (con un `try/except`, o dejando que se propague). Es la forma correcta de decir "esto no es un dato válido, no sigas como si lo fuera".

### Re-lanzar (`raise` solo)

Dentro de un `except`, `raise` sin argumentos relanza la misma excepción que atrapaste. Útil cuando querés loguear o hacer algo puntual, pero sin ocultar el error:

```python
try:
    procesar_archivo(ruta)
except FileNotFoundError:
    print(f"no encontré {ruta}, lo registro y sigo fallando")
    raise
```

### Encadenar con `raise ... from ...`

Cuando atrapás una excepción y lanzás **otra** distinta, Python te muestra ambas en el traceback, pero sin `from` no queda claro que una causó la otra. `raise NuevaExcepcion(...) from excepcion_original` deja la relación explícita:

```python
try:
    contrato = obtener_contrato(id)
except KeyError as e:
    raise ValueError(f"no existe el contrato {id}") from e
```

---

## 5. Excepciones propias

Cuando una regla de negocio no encaja en ningún error de Python (`ValueError`, `KeyError`, etc.), definís tu propia excepción heredando de `Exception`. Por convención, el nombre termina en `Error`:

```python
class MoraExcesivaError(Exception):
    """Se lanza cuando la mora de un inquilino supera el límite permitido."""

    def __init__(self, inquilino, monto_mora):
        self.inquilino = inquilino
        self.monto_mora = monto_mora
        super().__init__(f"{inquilino} tiene una mora de ${monto_mora}, supera el límite")
```

`super().__init__(mensaje)` es lo que hace que `str(excepcion)` y el traceback muestren ese mensaje. Guardar `self.inquilino` y `self.monto_mora` además del mensaje te permite, en el `except`, acceder a los datos concretos (no solo al texto):

```python
try:
    verificar_mora(inquilino, monto_mora, limite=50000)
except MoraExcesivaError as e:
    enviar_alerta(e.inquilino, e.monto_mora)   # datos, no un string a parsear
```

¿Por qué no alcanza con `raise ValueError("mora excesiva")`? Porque quien atrapa el error necesita **distinguir este caso de cualquier otro `ValueError`** del programa, y necesita los datos estructurados, no un mensaje de texto para parsear con substring.

---

## 6. Archivos con `with`

Abrir un archivo reserva un recurso del sistema operativo. Si no lo cerrás, en scripts cortos "no se nota", pero en un programa que corre server-side (como Django) vas acumulando archivos abiertos hasta romper algo.

```python
# ❌ Riesgoso: si algo entre open() y close() lanza una excepción,
# close() nunca se ejecuta y el archivo queda abierto.
f = open("stock.txt", encoding="utf-8")
contenido = f.read()
f.close()

# ✅ with: cierra el archivo SIEMPRE, incluso si hay una excepción adentro
with open("stock.txt", encoding="utf-8") as f:
    contenido = f.read()
```

`with` es, en el fondo, un `try/finally` que Python te escribe por vos. Es el mismo patrón que vas a ver en Django con transacciones (`with transaction.atomic():`) y en bases de datos con conexiones.

### Modos de apertura

| Modo  | Qué hace                                                                           |
| ----- | ---------------------------------------------------------------------------------- |
| `"r"` | Lectura (por defecto). Si el archivo no existe: `FileNotFoundError`.               |
| `"w"` | Escritura. Si el archivo existe, **lo pisa entero**. Si no existe, lo crea.        |
| `"a"` | Append: agrega al final, sin borrar lo que había.                                  |
| `"x"` | Crea el archivo, pero falla con `FileExistsError` si ya existe.                    |
| `"b"` | Se combina con los anteriores (`"rb"`, `"wb"`) para modo binario (imágenes, PDFs). |

Siempre especificá `encoding="utf-8"` al trabajar con texto. Si no lo hacés, Python usa la codificación por defecto del sistema operativo, que puede variar entre tu máquina, un servidor Linux y la de un compañero — y ahí aparecen los acentos rotos.

---

## 7. JSON: el formato de intercambio universal

JSON es el formato en el que llegan casi todas las respuestas de APIs (Binance, cualquier backend REST) y en el que Django/DRF serializa sus respuestas. La buena noticia: un JSON es, ni más ni menos, la misma estructura de diccionarios y listas que ya conocés de la lección 01.

```python
import json

contrato = {"id": 1, "inquilino": "Lucía Gómez", "monto": 250000, "activo": True}

# dict de Python -> string JSON
texto = json.dumps(contrato)          # '{"id": 1, "inquilino": "Lucía Gómez", ...}'

# string JSON -> dict de Python
de_vuelta = json.loads(texto)
```

Para trabajar con archivos, `dump`/`load` (sin la "s") leen y escriben directo, combinados con `with`:

```python
# Escribir
with open("contratos.json", "w", encoding="utf-8") as f:
    json.dump(contrato, f, indent=2, ensure_ascii=False)

# Leer
with open("contratos.json", "r", encoding="utf-8") as f:
    contrato = json.load(f)
```

- `indent=2`: lo escribe legible, con sangría (si no, queda todo en una línea).
- `ensure_ascii=False`: para que "Lucía" se guarde como "Lucía" y no como `"Lucía"`.

Truco para no confundirte entre `dump`/`dumps` y `load`/`loads`: **la que tiene "s" trabaja con `strings`**; la que no tiene "s" trabaja con **archivos** (`f`).

### Qué se puede guardar en JSON y qué no

| Python                   | JSON                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| `dict`                   | objeto `{}`                                                                                |
| `list`, `tuple`          | array `[]` (¡la tupla se guarda como lista, y al leerla vuelve como lista, no como tupla!) |
| `str`                    | string                                                                                     |
| `int`, `float`           | number                                                                                     |
| `True`/`False`           | `true`/`false`                                                                             |
| `None`                   | `null`                                                                                     |
| objeto de una clase tuya | ❌ `TypeError: Object of type X is not JSON serializable`                                  |

### Los dos errores que vas a ver todo el tiempo

```python
# 1. El archivo no existe
with open("no_existe.json") as f:
    datos = json.load(f)
# FileNotFoundError: [Errno 2] No such file or directory: 'no_existe.json'

# 2. El archivo existe, pero el contenido no es JSON válido
# (una coma de más, comillas simples en vez de dobles, un archivo vacío...)
json.loads("{'id': 1}")   # comillas simples: no es JSON válido
# json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes
```

Ambas son excepciones normales, atrapables con `except FileNotFoundError` y `except json.JSONDecodeError`. En un programa real, casi siempre querés capturarlas: un archivo de configuración corrupto no debería tirar abajo todo el sistema.

---

## Errores comunes

| Error                                                         | Causa                                                                  | Solución                                       |
| ------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------- |
| `except:` pelado, o `except Exception` como wildcard          | Atrapa todo, oculta bugs propios                                       | Capturá la excepción específica                |
| Excepción base antes que la derivada en la cadena de `except` | La base también atrapa a la subclase, el bloque específico nunca corre | Subclases primero, genéricas al final          |
| `return` dentro de un `finally`                               | Pisa silenciosamente el `return` del `try`                             | Evitá `return` en `finally`                    |
| Perder el archivo abierto si algo falla en el medio           | Usar `open()`/`close()` manual                                         | Usar siempre `with open(...)`                  |
| `json.dump(objeto_de_clase_propia, f)`                        | JSON no sabe serializar objetos arbitrarios                            | Convertí a `dict` antes (`vars(obj)` o a mano) |
| No poner `encoding="utf-8"`                                   | Rompe acentos en otro sistema operativo                                | Siempre explícito en `open()`                  |
| Usar `raise ValueError("texto")` para todo                    | Quien atrapa no puede distinguir un caso de negocio de otro            | Excepción propia cuando el caso lo justifica   |

---

## Conexión con lo que viene

- **Django:** `Modelo.objects.get(id=x)` lanza `Modelo.DoesNotExist` si no existe (y `MultipleObjectsReturned` si hay más de uno) — son excepciones específicas por modelo, mismo patrón que viste acá. Las vistas de DRF devuelven errores HTTP a partir de excepciones capturadas.
- **PostgreSQL:** una transacción que falla en el medio necesita revertirse (`ROLLBACK`) — es un `finally`/`with` a nivel de base de datos, lo vas a ver en la Fase 3 con `with transaction.atomic():`.
- **IA:** llamar a la API de Claude o de OpenAI puede fallar por timeout, rate limit o respuesta mal formada; siempre se envuelve en `try/except` con excepciones específicas del SDK, y la respuesta casi siempre es JSON.

---

## Resumen

| Herramienta                             | Para qué sirve                                      |
| --------------------------------------- | --------------------------------------------------- |
| `except ExcepcionEspecifica`            | Atrapar solo lo que sabés manejar                   |
| `else` (en try)                         | Código que corre solo si no hubo excepción          |
| `finally`                               | Limpieza que corre siempre                          |
| `raise Excepcion(...)`                  | Lanzar un error a propósito ante una regla violada  |
| `raise` (solo)                          | Re-lanzar la excepción atrapada, sin ocultarla      |
| `raise X from e`                        | Encadenar: "X pasó a causa de e"                    |
| Excepción propia (`class X(Exception)`) | Errores de negocio que Python no tiene predefinidos |
| `with open(...)`                        | Abrir un archivo garantizando que se cierre         |
| `json.dump`/`load`                      | JSON ↔ archivo                                      |
| `json.dumps`/`loads`                    | JSON ↔ string                                       |

---

## Autoevaluación

Respondé sin mirar la teoría:

1. ¿Por qué `except:` pelado (o `except Exception` como comodín) se considera mala práctica? Dame un ejemplo de un bug que se te escaparía por usarlo.

Un except: pelado puede generar una excepcion no deseada, general, o simplemente un bug por error del codigo que yo mismo escribi. Me imagino en un entorno de deploy y logs de mi backend, donde este buscando un error de algo especifico y al tener una exception: pelado ese bug seria silenciosamente atrapado por ese except y no me daria la informacion necesaria para corregir eso. El except Exception se utiliza como error general, va a lo ultimo de los excepts, se implementa con un else

2. Tenés `try: algo() except A: ... except B: ...`, donde `B` es la clase base de `A`. ¿Qué pasa si invertís el orden de los `except`? ¿Por qué?

La clase del except B pisaria a la subclase del except A, por ende el error especifico que queria capturar la subclase quedaria generalizada por la clase base de la excepcion B. Esto pasa porque en python las excepciones se leen de arriba a abajo y se toma la primera que coincide con el error, por eso siempre se debe poner la subclase o except mas especifico arriba de los except generales o clases base

3. ¿Cuál es la diferencia entre poner una línea dentro del `try` y ponerla en el `else`?

Esta respuesta tuve que volver a leer la explicacion que hay en este archivo\*: La diferencia que hay es que al poner todo en un try puede caer dentro del except un error como un bug en el print(), en cambio con el else le da la directiva al sistema de que hacer cuando sale todo bien.

4. ¿Cuándo conviene crear una excepción propia en vez de usar `raise ValueError(...)`?

Conviene crear una excepcion propia cuando Python no tiene excepciones especificas para el error que queres capturar, ese error puede ser una limitacion que quieras imponer como regla del sistema o negocio.

5. ¿Qué ventaja tiene `with open(...)` sobre `open()` + `close()` manual?

el with le agrega un cierre al archivo obligatorio, ya que en un sistema/servidor como Django sin el with podria haber una excepcion entre el open() y el close() y no se cerraria el archivo, quedaria abierto durante todo el tiempo. Con with esto no pasa, se encarga de que se cierre obligatoriamente el archivo
