# Progreso

## Estado general
- Fase actual: 1 (Python)
- Lección actual: 02 (Manejo de errores, archivos y JSON) — cerrada, repaso hecho

## Registro

### Lección 01: Colecciones
- Inicio: 2026-09-16
- Fin: 2026-09-16
- Qué aprendí:
  - Diccionarios: acceso con `[]` vs `.get()`, CUD, recorrido con `.items()`, anidados y listas de diccionarios.
  - El patrón "agrupar" (inicializar clave la primera vez, después acumular) — lo aplicó solo, dos veces, en contextos distintos: `agrupar_por_indice` (valor = lista, con `.append()`) y `resumen_trades` (valor = diccionario anidado, con `+= 1`). Entendió por qué cada caso necesita una inicialización distinta y por qué `+=` sobre algo inexistente rompe.
  - Tuplas como retorno múltiple y para desempaquetar en `for` (`for par, resultado in trades`).
  - Sets y operadores de conjunto (`&`, `-`, `|`) aplicados a comparar exchanges.
  - Comprensiones de lista y de diccionario (`[... for ... if ...]`, `{clave: valor for ...}`).
  - `round(numero, ndigits)`: el segundo parámetro es necesario para redondear a decimales; sin él redondea a entero.
  - 8/8 ejercicios resueltos y verificados sin errores.
- Qué me costó:
  - El desempaquetado de tuplas dentro de un `for` (`for producto, cantidad in ventas`) — al principio intentó agregar un `for` anidado de más, pensando que hacía falta un paso previo de acceso a cada tupla.
  - Diferenciar, dentro de una función, la lista completa (`contratos`) de la variable de cada vuelta del `for` (`c`) — confundía ambas dentro de una misma comprensión (ejercicio 6a).
  - Errores de sintaxis finos al escribir Python a mano en Markdown (comillas y corchetes sin cerrar, `return` mezclado con `=`, nombre de variable con typo) — los fue encontrando solo con guía de "contá los corchetes/comillas", buena señal de lectura atenta del código.
- Pendientes / repasar:
  - Limpiar en `notas.md` (líneas 15-46) el bloque viejo de "No logro entender el ejemplo..." con el intento de `for` anidado — ya no refleja lo que entiende, quedó desactualizado.
  - Tener presente el hábito de `round(x, 2)` con el segundo parámetro siempre que el enunciado pida decimales, no solo cuando el test lo exige.

### Refuerzo (17-09-2026): `repaso.py`
Pidió una vuelta extra antes de pasar a la lección 02. Se armó `repaso.py`
con 7 ejercicios nuevos (otros datos: kiosco, alquileres, exchanges) apuntados
a los tres puntos débiles de arriba. Resultado: **7/7 correctos sin ayuda**,
incluida la corrección de `comparar_exchanges` (armar el dict final directo,
sin valores en 0 que se pisan) aplicada por su cuenta en `comparar_sucursales`
sin que se le pidiera de nuevo. Lección 01 cerrada de forma sólida — listo
para arrancar la lección 02 (manejo de errores, archivos con `with`, JSON).

### Lección 02: Manejo de errores, archivos y JSON
- Inicio: 2026-09-17
- Fin: 2026-09-18
- Qué aprendí:
  - Excepciones específicas: capturar `ValueError`/`TypeError`/`ZeroDivisionError`
    puntuales en vez de un `except` genérico, y combinar varias en una tupla
    (`except (TypeError, ZeroDivisionError):`) cuando el manejo es el mismo.
  - `try/except/else`: separar la línea riesgosa (en el `try`) del código que
    depende de que salió bien (en el `else`).
  - `finally` para garantizar un efecto (en este caso, `intentos.append(...)`)
    sin importar si hubo excepción o no.
  - `raise` manual para validar una regla de negocio (`validar_monto_alquiler`).
  - Excepción propia (`MoraExcesivaError`) con atributos guardados en
    `__init__`, para poder acceder a los datos estructurados en el `except`
    en vez de un mensaje de texto.
  - `with open(...)` + `json.dump`/`json.load` para escribir y leer archivos,
    incluyendo el manejo de `FileNotFoundError` y `json.JSONDecodeError`.
  - 17/17 ejercicios resueltos, con dos rondas de corrección.
  - Repaso (`repaso.py`, mismo día): 14/14 sin ayuda, incluyendo el ejercicio
    nuevo sobre `finally` con una excepción que se deja sin capturar.
- Qué me costó:
  - Ejercicio 7 (primera entrega): el `try` envolvía solo `json.load(f)`, pero
    el `with open(ruta, ...)` que puede lanzar `FileNotFoundError` estaba
    *fuera* del `try`. Lo corrigió solo moviendo el `with open(...)` adentro
    del `try`, después de que se le preguntó puntualmente por el alcance del
    bloque.
  - Matiz sobre `finally` vs. duplicar código en `try` y en `except`: en la
    autoevaluación dijo que daba "el mismo resultado", sin ver el caso de una
    excepción que no está capturada (ahí `finally` sigue corriendo antes de
    que la excepción se propague, pero un `append()` duplicado en `try`/`except`
    nunca correría). Se lo reforzó con el ejercicio 2 del repaso
    (`cerrar_posicion`, con un `ZeroDivisionError` sin capturar a propósito).
  - En el ejercicio 8 usó `float(t["resultado"])` en vez de `t["resultado"] + 0.0`
    como sugería el enunciado: pasa los tests, pero es más permisivo (acepta
    un número como string, ej. `"45.0"`, como válido). Quedó marcado como una
    decisión de diseño a tener presente, no como un error — se reforzó en el
    ejercicio 3 del repaso (`sumar_montos_validos`), donde el enunciado exige
    explícitamente `+ 0` en vez de `float(...)`.
- Pendientes / repasar:
  - Ninguno crítico. Tener presente el matiz de `finally` de arriba si en
    Fase 2 (Django) aparecen casos de limpieza de recursos con excepciones
    que se dejan propagar (por ejemplo, `transaction.atomic()`).
- Listo para arrancar la lección 03 (módulos, paquetes, entornos virtuales,
  `uv`, consumir APIs con `requests`).
