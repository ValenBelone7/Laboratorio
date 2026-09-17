# Progreso

## Estado general
- Fase actual: 1 (Python)
- Lección actual: 01 (Colecciones)

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
