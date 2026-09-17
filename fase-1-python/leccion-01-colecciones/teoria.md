# Lección 01: Colecciones (diccionarios, tuplas, sets y comprensiones)

## Por qué importa

Ya sabés usar listas. Pero en el trabajo real casi todos los datos llegan como **diccionarios**:

- Una respuesta de la API de Binance es un diccionario (JSON).
- Una fila de una base de datos se parece a un diccionario: columna → valor.
- En Django, `request.POST`, `request.GET` y `QuerySet.values()` se usan como diccionarios.

Si dominás las cuatro colecciones de esta lección, vas a poder leer y transformar datos sin depender de la IA.

---

## 1. Diccionarios (`dict`)

Guardan pares **clave → valor**. No se accede por posición sino por nombre.

```python
contrato = {
    "id": 1,
    "inquilino": "Lucía Gómez",
    "monto": 250000,
    "indice": "ICL",
    "estado": "pendiente",
}
```

### Leer valores

```python
contrato["monto"]            # 250000
contrato["garante"]          # KeyError: la clave no existe
contrato.get("garante")      # None, no rompe
contrato.get("garante", "Sin garante")  # valor por defecto
```

Regla práctica: usá `[]` cuando la clave **tiene** que existir, y `.get()` cuando puede faltar (por ejemplo, datos que vienen de una API).

### Modificar, agregar y eliminar

```python
contrato["estado"] = "pagado"      # modifica valor (la clave ya existía)
contrato["mora"] = 1500            # agrega clave y valor (la clave no existía)
eliminado = contrato.pop("mora")   # elimina y devuelve el valor
del contrato["indice"]             # elimina sin devolver
```

### Preguntar si existe una clave

```python
if "garante" in contrato:
    print("Tiene garante")
```

`in` busca en las **claves**, no en los valores.

### Recorrer

```python
for clave in contrato:                  # recorre claves
    print(clave)

for valor in contrato.values():         # recorre valores
    print(valor)

for clave, valor in contrato.items():   # recorre ambos (el más usado)
    print(f"{clave}: {valor}")
```

### Diccionarios anidados

Así se ven las respuestas reales de las APIs:

```python
respuesta = {
    "symbol": "BTCUSDT",
    "precio": 97000.5,
    "exchange": {"nombre": "Binance", "pais": "Global"},
}
respuesta["exchange"]["nombre"]   # "Binance"
```

### Lista de diccionarios: el formato más común

```python
contratos = [
    {"id": 1, "inquilino": "Lucía", "monto": 250000},
    {"id": 2, "inquilino": "Martín", "monto": 180000},
]
for c in contratos:
    print(c["inquilino"], c["monto"])
```

Esto es básicamente **una tabla**: cada diccionario es una fila. Lo vas a ver en JSON, en Supabase y en Django.

### El patrón "agrupar"

Construir un diccionario mientras recorrés. Es muy común.

```python
ventas = [("coca", 2), ("alfajor", 5), ("coca", 3)]
total_por_producto = {}
for producto, cantidad in ventas:
    if producto not in total_por_producto:
        total_por_producto[producto] = 0
    total_por_producto[producto] += cantidad
# {"coca": 5, "alfajor": 5}
```

Una forma más corta de hacer lo mismo:

```python
total_por_producto[producto] = total_por_producto.get(producto, 0) + cantidad
```

### Reglas de las claves

- Las claves son **únicas**. Si repetís una, se pisa el valor anterior.
- Tienen que ser inmutables: `str`, `int`, `tuple` sirven; una `list` no.
- Desde Python 3.7, el diccionario **mantiene el orden** de inserción.

---

## 2. Tuplas (`tuple`)

Son como listas, pero **no se pueden modificar** (son inmutables).

```python
coordenadas = (-33.12, -64.35)   # Río Cuarto
coordenadas[0]                   # -33.12
coordenadas[0] = 0               # TypeError: no se puede modificar
```

### ¿Para qué sirven si son "listas limitadas"?

1. **Datos que no deberían cambiar**: una coordenada, un par (fecha, valor), una configuración.
2. **Devolver varios valores desde una función**:

```python
def aplicar_aumento(monto, porcentaje):
    nuevo = monto * (1 + porcentaje / 100)
    return nuevo, nuevo - monto          # devuelve una tupla

nuevo_monto, diferencia = aplicar_aumento(100000, 10)
```

3. **Como clave de diccionario** (las listas no pueden serlo):

```python
precios = {("BTC", "Binance"): 97000, ("BTC", "Bybit"): 97010}
```

### Desempaquetado

Asignar cada elemento a una variable en una sola línea:

```python
par, ganancia = ("BTCUSDT", 120.5)

trades = [("BTCUSDT", 120.5), ("ETHUSDT", -40.0)]
for par, ganancia in trades:          # desempaquetado dentro del for
    print(par, ganancia)
```

Es lo mismo que hacés con `.items()` en los diccionarios: cada item es una tupla `(clave, valor)`.

Detalle: una tupla de un solo elemento lleva coma, `("BTC",)`. Sin la coma, `("BTC")` es solo un string entre paréntesis.

---

## 3. Sets (`set`)

Colección **sin elementos repetidos** y **sin orden**.

```python
monedas = {"BTC", "ETH", "BTC", "SOL"}
print(monedas)      # {"BTC", "ETH", "SOL"}  (el orden puede variar)
vacio = set()       # ojo: {} crea un diccionario vacío, no un set
```

### Usos típicos

**Eliminar duplicados:**

```python
indices = ["IPC", "ICL", "IPC", "IPC"]
unicos = set(indices)     # {"IPC", "ICL"}
```

**Operaciones de conjuntos** (lo que viste en Matemática y Lógica):

```python
binance = {"BTC", "ETH", "SOL", "ADA"}
bybit   = {"BTC", "ETH", "XRP"}

binance & bybit    # intersección: {"BTC", "ETH"}  (en ambos)
binance | bybit    # unión: todas sin repetir
binance - bybit    # diferencia: {"SOL", "ADA"}  (solo en Binance)
```

**Buscar rápido:** `"BTC" in monedas` es muchísimo más rápido en un set que en una lista cuando hay miles de elementos. La lista revisa uno por uno; el set va directo.

### Limitaciones

- No se puede hacer `monedas[0]`, porque no tiene posiciones.
- Si el orden importa, no uses set.
- Agregar y quitar: `.add("DOGE")`, `.discard("DOGE")` (no falla si no existe).

---

## 4. Comprensiones

Una forma corta de **crear** una colección a partir de otra.

### De listas

```python
montos = [100000, 200000, 300000]

# Forma larga
con_aumento = []
for m in montos:
    con_aumento.append(m * 1.1)

# Comprensión: mismo resultado
con_aumento = [m * 1.1 for m in montos]
```

Se lee así: "**qué** guardo, **para cada** elemento, **de dónde**".

### Con filtro

```python
caros = [m for m in montos if m > 150000]
pendientes = [c["inquilino"] for c in contratos if c["estado"] == "pendiente"]
```

### De diccionarios y sets

```python
# dict: {clave: valor for ...}
monto_por_id = {c["id"]: c["monto"] for c in contratos}

# set: {valor for ...}
indices_usados = {c["indice"] for c in contratos}
```

### Cuándo NO usarlas

Si necesitás varias líneas de lógica, un `if/elif/else` complejo o prints en el medio, usá un `for` normal. **Una comprensión que no se entiende a primera vista es peor que un for.**

---

## Errores comunes

| Error                                          | Causa                                          | Solución                      |
| ---------------------------------------------- | ---------------------------------------------- | ----------------------------- |
| `KeyError: 'garante'`                          | La clave no existe                             | `.get()` o verificar con `in` |
| `TypeError: unhashable type: 'list'`           | Usaste una lista como clave o dentro de un set | Usá una tupla                 |
| `{}` no se comporta como set                   | `{}` es un dict vacío                          | `set()`                       |
| Modificar un dict "copiado" cambia el original | `b = a` no copia, apunta al mismo objeto       | `b = a.copy()`                |
| Recorrer un dict y borrar claves a la vez      | `RuntimeError`                                 | Recorré `list(d.keys())`      |

Sobre el penúltimo error:

```python
original = {"monto": 100}
copia = original          # NO es una copia
copia["monto"] = 999
print(original["monto"])  # 999
```

---

## Conexión con lo que viene

- **Django:** `Contrato.objects.values("id", "monto")` devuelve algo que se recorre como una lista de diccionarios. `request.POST.get("monto")` funciona igual que `.get()`.
- **PostgreSQL:** un `GROUP BY` hace lo mismo que el patrón "agrupar" que viste arriba.
- **IA:** las APIs de modelos reciben y devuelven diccionarios (`{"role": "user", "content": "..."}`).

---

## Resumen

| Colección | Sintaxis   | Ordenada | Modificable | Repetidos | Uso principal                |
| --------- | ---------- | -------- | ----------- | --------- | ---------------------------- |
| list      | `[1, 2]`   | Sí       | Sí          | Sí        | Secuencias de cosas          |
| dict      | `{"a": 1}` | Sí       | Sí          | Claves no | Datos con nombre             |
| tuple     | `(1, 2)`   | Sí       | No          | Sí        | Datos fijos, varios retornos |
| set       | `{1, 2}`   | No       | Sí          | No        | Únicos, comparar grupos      |

---

## Autoevaluación

Respondé sin mirar la teoría:

1. ¿Qué diferencia hay entre `contrato["garante"]` y `contrato.get("garante")`? ¿Cuándo usarías cada uno?
   La diferencia entre contrato[garante] y el get() es que el primero se utiliza en una clave que debe o sabes que esta y el get() se utiliza en claves que vos no tenes confirmadas que estan, por ejemplo cuando se le pega a una API

2. Tenés las monedas de Binance y las de OKX. ¿Qué operación usás para saber cuáles están en Binance pero no en OKX?

Se utiliza un set y el metodo de de diferencia

3. ¿Por qué una tupla puede ser clave de un diccionario y una lista no?

Las tuplas son inmutables y las claves de un dict tambien deben serlo

4. Escribí de memoria una comprensión que devuelva los nombres de los inquilinos con monto mayor a 200000.

inquilinos_comprension = [c['inquilino'] for c in contratos if c['monto'] > 200000]

return inquilinos_comprension

5. ¿Qué pasa si hacés `b = a` con un diccionario y después modificás `b`?

Se actualiza el valor del diccionario ya que no es una copia, sino que sigue apuntando al dict original
