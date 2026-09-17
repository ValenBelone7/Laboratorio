"""
Repaso de la Lección 01: Colecciones
=====================================
No es una lección nueva, es una vuelta más sobre lo mismo con datos distintos.
Apunta especialmente a lo que costó la primera vez:
  - desempaquetar tuplas de MÁS de 2 elementos en un for
  - en una comprensión, no confundir la colección completa con la variable
    de cada vuelta
  - el patrón "agrupar" en variantes nuevas (acumular un número, no una lista;
    y un diccionario anidado con una tupla de 3 elementos)

Mismas reglas que siempre:
1. Reemplazá cada `raise NotImplementedError` por tu código. SIN IA.
2. Ejecutá:  python repaso.py
3. No modifiques los datos ni verificar().
"""

STOCK_KIOSCO = [
    {"producto": "Alfajor", "categoria": "golosinas", "stock": 40, "precio": 900},
    {"producto": "Coca 500ml", "categoria": "bebidas", "stock": 15, "precio": 1500},
    {"producto": "Sprite 500ml", "categoria": "bebidas", "stock": 0, "precio": 1500},
    {"producto": "Chocolate", "categoria": "golosinas", "stock": 8, "precio": 2200},
    {"producto": "Agua 500ml", "categoria": "bebidas", "stock": 22, "precio": 1000},
]

VENTAS = [
    ("Alfajor", 3, 900),
    ("Coca 500ml", 2, 1500),
    ("Alfajor", 5, 900),
    ("Agua 500ml", 1, 1000),
    ("Coca 500ml", 4, 1500),
]

ALQUILERES = [
    {"id": 1, "inquilino": "Bruno Sosa", "barrio": "Alberdi", "monto": 240000, "indice": "ICL", "mora": 0},
    {"id": 2, "inquilino": "Carla Nieva", "barrio": "Centro", "monto": 310000, "indice": "IPC", "mora": 15000},
    {"id": 3, "inquilino": "Franco Díaz", "barrio": "Alberdi", "monto": 190000, "indice": "IPC", "mora": 0},
    {"id": 4, "inquilino": "Melina Ríos", "barrio": "Banda Norte", "monto": 275000, "indice": "ICL", "mora": 32000},
    {"id": 5, "inquilino": "Ezequiel Paz", "barrio": "Centro", "monto": 200000, "indice": "Casa Propia", "mora": 8000},
]

TRADES_EXCHANGE = [
    ("Binance", "BTCUSDT", 45.0),
    ("Bybit", "ETHUSDT", -12.0),
    ("Binance", "ETHUSDT", 30.0),
    ("Binance", "BTCUSDT", -20.0),
    ("Bybit", "BTCUSDT", 18.0),
    ("Bybit", "ETHUSDT", -5.0),
]

SUCURSAL_CENTRO = {"Alfajor", "Coca 500ml", "Chocolate", "Agua 500ml"}
SUCURSAL_NORTE = {"Alfajor", "Sprite 500ml", "Chocolate", "Gomitas"}


# ---------------------------------------------------------------
# 1. Desempaquetar una tupla de 3 elementos + acumular un número
# ---------------------------------------------------------------
def total_facturado_por_producto(ventas):
    """
    VENTAS es una lista de tuplas (producto, cantidad, precio_unitario).
    Devolvé un diccionario {producto: monto_total_facturado}.

    A diferencia del ejemplo de teoria.md (que acumulaba cantidad),
    acá cada vuelta tenés que CALCULAR cantidad * precio_unitario
    antes de sumarlo. Usá un for normal, con desempaquetado de los
    3 valores directo en el "for".

    Ejemplo de forma: {"Alfajor": 7200, "Coca 500ml": 9000, ...}
    """

    montototal_por_producto = {}

    for producto,cantidad,precio_unitario in ventas:
        if producto not in montototal_por_producto:
            montototal_por_producto[producto] = 0

        montototal_por_producto[producto] += cantidad * precio_unitario

    return montototal_por_producto

# ---------------------------------------------------------------
# 2. Calentamiento: for simple sobre lista de diccionarios
# ---------------------------------------------------------------
def productos_agotados(stock):
    """
    Devolvé una LISTA con los nombres ("producto") de los ítems
    cuyo "stock" sea igual a 0.
    """

    productos_sin_stock = []

    for s in stock:
        if s['stock'] == 0:
            productos_sin_stock.append(s['producto'])

    return productos_sin_stock

# ---------------------------------------------------------------
# 3. Comprensión: ojo con "la colección completa" vs "cada vuelta"
# ---------------------------------------------------------------
def deudores_con_mora(alquileres):
    """
    Con UNA comprensión de lista, devolvé los nombres ("inquilino")
    de los contratos cuya "mora" sea mayor a 0.

    Antes de escribirla, contestate (no hace falta escribirlo, pero
    pensalo): ¿cuál es "la colección de donde vengo" acá? ¿Y cuál es
    el nombre que le doy a cada elemento dentro del for?
    """

    inquilinos_mora = [a['inquilino'] for a in alquileres if a['mora'] > 0]

    return inquilinos_mora

# ---------------------------------------------------------------
# 4. Patrón "agrupar" de nuevo, con otros datos
# ---------------------------------------------------------------
def productos_por_categoria(stock):
    """
    Devolvé un diccionario {categoria: [nombres_de_productos]}.

    Es el mismo patrón que agrupar_por_indice de ejercicios.py:
    inicializar la clave la primera vez, después ir agregando.

    Ejemplo de forma: {"golosinas": ["Alfajor", "Chocolate"], "bebidas": [...]}
    """

    productos_categoria = {}

    for s in stock:
        categoria = s['categoria']

        if categoria not in productos_categoria:
            productos_categoria[categoria] = []

        productos_categoria[categoria].append(s['producto'])

    return productos_categoria

# ---------------------------------------------------------------
# 5. Diccionario anidado con tupla de 3 elementos
# ---------------------------------------------------------------
def resumen_por_exchange(trades_exchange):
    """
    TRADES_EXCHANGE es una lista de tuplas (exchange, par, resultado).
    Un resultado > 0 es un trade ganado; < 0, perdido. El "par" no lo
    necesitás para este ejercicio (lo desempaquetás igual, aunque no
    lo uses después).

    Devolvé un diccionario anidado, igual que resumen_trades pero
    agrupando por exchange en vez de por par:
      {"Binance": {"ganados": N, "perdidos": M}, "Bybit": {...}}
    """

    resultados_exchanges = {}

    for exchange,par,resultado in trades_exchange:
        if exchange not in resultados_exchanges:
            resultados_exchanges[exchange] = {'ganados':0,'perdidos':0}

        if resultado > 0:
            resultados_exchanges[exchange]['ganados'] += 1
        else:
            resultados_exchanges[exchange]['perdidos'] += 1

    return resultados_exchanges



# ---------------------------------------------------------------
# 6. Sets
# ---------------------------------------------------------------
def comparar_sucursales(productos_a, productos_b):
    """
    Recibe dos sets de nombres de productos. Devolvé un diccionario
    con 4 claves, cada valor un set:
      "en_ambas":  productos que están en las dos sucursales
      "solo_a":    productos que están solo en la primera
      "solo_b":    productos que están solo en la segunda
      "todas":     todos los productos sin repetir
    Usá operadores de conjuntos, no for.
    """

    conjuntos = {
        "en_ambas": productos_a & productos_b,
        "solo_a":productos_a - productos_b,
        "solo_b":productos_b - productos_a,
        "todas":productos_a | productos_b
    }

    return conjuntos
# ---------------------------------------------------------------
# 7 (desafío): combinar agrupar + acumular en el mismo ejercicio
# ---------------------------------------------------------------
def valor_total_stock_por_categoria(stock):
    """
    Devolvé un diccionario {categoria: valor_total}, donde valor_total
    es la suma de (stock * precio) de todos los productos de esa
    categoría.

    Es la fusión de los ejercicios 1 y 4 de este repaso: agrupás por
    categoria (como en 4), pero en vez de una lista de nombres vas
    acumulando un número calculado (como en 1).
    """

    valor_total_stock = {}

    for s in stock:
        if s['categoria'] not in valor_total_stock:
            valor_total_stock[s['categoria']] = 0

        valor_total_stock[s['categoria']] += s["stock"] * s["precio"]

    return valor_total_stock

# ===============================================================
# Verificación
# ===============================================================
def verificar():
    casos = [
        ("1. total_facturado_por_producto",
         lambda: total_facturado_por_producto(VENTAS),
         {"Alfajor": 7200, "Coca 500ml": 9000, "Agua 500ml": 1000}),
        ("2. productos_agotados",
         lambda: productos_agotados(STOCK_KIOSCO),
         ["Sprite 500ml"]),
        ("3. deudores_con_mora",
         lambda: deudores_con_mora(ALQUILERES),
         ["Carla Nieva", "Melina Ríos", "Ezequiel Paz"]),
        ("4. productos_por_categoria",
         lambda: productos_por_categoria(STOCK_KIOSCO),
         {"golosinas": ["Alfajor", "Chocolate"],
          "bebidas": ["Coca 500ml", "Sprite 500ml", "Agua 500ml"]}),
        ("5. resumen_por_exchange",
         lambda: resumen_por_exchange(TRADES_EXCHANGE),
         {"Binance": {"ganados": 2, "perdidos": 1},
          "Bybit": {"ganados": 1, "perdidos": 2}}),
        ("6. comparar_sucursales",
         lambda: comparar_sucursales(SUCURSAL_CENTRO, SUCURSAL_NORTE),
         {"en_ambas": {"Alfajor", "Chocolate"},
          "solo_a": {"Coca 500ml", "Agua 500ml"},
          "solo_b": {"Sprite 500ml", "Gomitas"},
          "todas": {"Alfajor", "Chocolate", "Coca 500ml", "Agua 500ml", "Sprite 500ml", "Gomitas"}}),
        ("7. valor_total_stock_por_categoria",
         lambda: valor_total_stock_por_categoria(STOCK_KIOSCO),
         {"golosinas": 53600, "bebidas": 44500}),
    ]

    correctos = 0
    for nombre, funcion, esperado in casos:
        try:
            obtenido = funcion()
        except NotImplementedError:
            print(f"⏳ {nombre}: sin resolver")
            continue
        except Exception as e:
            print(f"❌ {nombre}: error {type(e).__name__}: {e}")
            continue
        if obtenido == esperado:
            print(f"✅ {nombre}")
            correctos += 1
        else:
            print(f"❌ {nombre}\n   esperado: {esperado}\n   obtenido: {obtenido}")

    print(f"\n{correctos}/{len(casos)} correctos")
    if correctos == len(casos):
        print("¡Muy bien! Esta lección quedó afianzada.")


if __name__ == "__main__":
    verificar()
