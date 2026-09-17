"""
Lección 01: Colecciones
=======================
Instrucciones:
1. Leé teoria.md antes de empezar.
2. Reemplazá cada `raise NotImplementedError` por tu código. SIN IA.
3. Ejecutá:  python ejercicios.py
   ✅ = correcto   ❌ = incorrecto   ⏳ = todavía no lo hiciste
4. No modifiques los datos ni la función verificar().
"""

CONTRATOS = [
    {"id": 1, "inquilino": "Lucía Gómez", "monto": 250000, "indice": "ICL", "estado": "pagado"},
    {"id": 2, "inquilino": "Martín Pérez", "monto": 180000, "indice": "IPC", "estado": "pendiente"},
    {"id": 3, "inquilino": "Sofía Ruiz", "monto": 320000, "indice": "IPC", "estado": "pendiente"},
    {"id": 4, "inquilino": "Diego Torres", "monto": 150000, "indice": "Casa Propia", "estado": "pagado"},
    {"id": 5, "inquilino": "Ana Castro", "monto": 210000, "indice": "ICL", "estado": "vencido"},
]

TRADES = [
    ("BTCUSDT", 120.5),
    ("ETHUSDT", -40.0),
    ("BTCUSDT", -15.0),
    ("SOLUSDT", 60.0),
    ("BTCUSDT", 80.0),
]


# ---------------------------------------------------------------
# Ejercicio 1: Diccionarios básicos
# ---------------------------------------------------------------
def inquilinos_con_deuda(contratos):
    """
    Devolvé una LISTA con los nombres de los inquilinos cuyo estado
    sea "pendiente" o "vencido", en el mismo orden en que aparecen.
    Usá un for normal (todavía sin comprensión).
    """

    inquilinos_deudores = []

    for c in contratos:
        if c["estado"] == "pendiente" or c["estado"] == "vencido":
            # 💡 más idiomático: c["estado"] in ("pendiente", "vencido")
            # evita repetir c["estado"] dos veces. Mismo caso en total_adeudado, abajo.
            inquilinos_deudores.append(c["inquilino"])

    return inquilinos_deudores


# ---------------------------------------------------------------
# Ejercicio 2: Acumular
# ---------------------------------------------------------------
def total_adeudado(contratos):
    """
    Devolvé la suma de los montos de los contratos "pendiente" o "vencido".
    """

    montos_sumados = 0

    for c in contratos:
        if c["estado"] == "pendiente" or c["estado"] == "vencido":
            montos_sumados += c['monto']

    return montos_sumados
# ---------------------------------------------------------------
# Ejercicio 3: El patrón "agrupar"
# ---------------------------------------------------------------
def agrupar_por_indice(contratos):
    """
    Devolvé un diccionario donde la clave es el índice de aumento
    y el valor es una lista con los ids de los contratos que lo usan.

    Ejemplo de forma:  {"ICL": [1, 5], ...}
    """

    ids_por_indice = {}

    for c in contratos:
        clave = c["indice"]              # "ICL", "IPC" o "Casa Propia"

        if clave not in ids_por_indice:
            ids_por_indice[clave] = []  # ← ¿con qué arranca la clave la primera vez?

        ids_por_indice[clave].append(c["id"])  # ← ¿qué método de lista agrega UN elemento al final?

    return ids_por_indice


# ---------------------------------------------------------------
# Ejercicio 4: Tuplas y varios valores de retorno
# ---------------------------------------------------------------
def aplicar_aumento(monto, porcentaje):
    """
    Devolvé una TUPLA (monto_nuevo, diferencia), ambos redondeados
    a 2 decimales con round().

    Ejemplo: aplicar_aumento(200000, 10) -> (220000.0, 20000.0)
    """

    nuevo_monto = monto * (1 + porcentaje / 100)
    diferencia = nuevo_monto - monto
    return round(nuevo_monto), round(diferencia)
    # ⚠️ falta el segundo parámetro de round() (ndigits=2) → así redondea a ENTERO.
    # Con estos números da igual porque el resultado cae redondo, pero con
    # decimales reales (ej: aplicar_aumento(100000, 7.3)) perdés precisión
    # sin que salte ningún error. Debería ser: round(nuevo_monto, 2), round(diferencia, 2)

# ---------------------------------------------------------------
# Ejercicio 5: Sets
# ---------------------------------------------------------------
def comparar_exchanges(monedas_a, monedas_b):
    """
    Recibe dos sets de monedas. Devolvé un diccionario con 4 claves:
      "en_ambos": monedas que están en los dos
      "solo_a":   monedas que están solo en A
      "solo_b":   monedas que están solo en B
      "todas":    todas las monedas sin repetir
    Cada valor tiene que ser un set. Usá operadores de conjuntos, no for.
    """

    conjuntos = {
        'en_ambos':0,
        'solo_a':0,
        'solo_b':0,
        'todas':0
    }
    # 👆 estos 4 valores en 0 nunca se leen: las 4 líneas de abajo los pisan sin
    # ninguna condición. Un dev que revise esto se pregunta "¿para qué inicializo
    # algo que siempre se sobreescribe?". Se puede ir directo al resultado final:
    #   return {
    #       "en_ambos": monedas_a & monedas_b,
    #       "solo_a": monedas_a - monedas_b,
    #       "solo_b": monedas_b - monedas_a,
    #       "todas": monedas_a | monedas_b,
    #   }

    conjuntos['en_ambos'] = monedas_a & monedas_b
    conjuntos['solo_a'] = monedas_a - monedas_b
    conjuntos['solo_b'] = monedas_b - monedas_a
    conjuntos["todas"] = monedas_a | monedas_b

    return conjuntos


# ---------------------------------------------------------------
# Ejercicio 6: Comprensiones
# ---------------------------------------------------------------
def montos_con_aumento(contratos, porcentaje):
    """
    Con UNA comprensión de lista, devolvé los montos con el aumento
    aplicado, redondeados a 2 decimales.
    """

    con_aumento = [round(c['monto'] * (1 + porcentaje / 100)) for c in contratos]
    # ⚠️ mismo problema que en aplicar_aumento: falta el ndigits=2 → round(..., 2)

    return con_aumento


def indice_por_id(contratos):
    """
    Con UNA comprensión de diccionario, devolvé {id: indice}.
    """

    id_indice = {c['id']:c['indice'] for c in contratos}

    return id_indice

# ---------------------------------------------------------------
# Ejercicio 7 (desafío): Resumen de trades
# ---------------------------------------------------------------
def resumen_trades(trades):
    """
    Recibe una lista de tuplas (par, resultado).
    Un resultado > 0 es un trade ganado; < 0, perdido.
    Devolvé un diccionario anidado:
      {"BTCUSDT": {"ganados": 2, "perdidos": 1}, ...}
    Todos los pares tienen que tener ambas claves, aunque valgan 0.
    """

    resumen = {}

    for par, resultado in trades:
        if par not in resumen:
            resumen[par] = {'ganados':0,'perdidos':0}              # (1) ¿qué diccionario "vacío" necesito acá?

        if resultado > 0:
            resumen[par]["ganados"] +=1     # (2)
        else:
            resumen[par]["perdidos"] += 1    # (2)

    return resumen

        


# ===============================================================
# Verificación: no hace falta que entiendas este código todavía
# (lo vas a entender en las lecciones 02 y 07).
# ===============================================================
def verificar():
    casos = [
        ("1. inquilinos_con_deuda",
         lambda: inquilinos_con_deuda(CONTRATOS),
         ["Martín Pérez", "Sofía Ruiz", "Ana Castro"]),
        ("2. total_adeudado",
         lambda: total_adeudado(CONTRATOS),
         710000),
        ("3. agrupar_por_indice",
         lambda: agrupar_por_indice(CONTRATOS),
         {"ICL": [1, 5], "IPC": [2, 3], "Casa Propia": [4]}),
        ("4. aplicar_aumento",
         lambda: aplicar_aumento(200000, 10),
         (220000.0, 20000.0)),
        ("5. comparar_exchanges",
         lambda: comparar_exchanges({"BTC", "ETH", "SOL", "ADA"}, {"BTC", "ETH", "XRP", "SOL"}),
         {"en_ambos": {"BTC", "ETH", "SOL"}, "solo_a": {"ADA"},
          "solo_b": {"XRP"}, "todas": {"BTC", "ETH", "SOL", "ADA", "XRP"}}),
        ("6a. montos_con_aumento",
         lambda: montos_con_aumento(CONTRATOS, 5),
         [262500.0, 189000.0, 336000.0, 157500.0, 220500.0]),
        ("6b. indice_por_id",
         lambda: indice_por_id(CONTRATOS),
         {1: "ICL", 2: "IPC", 3: "IPC", 4: "Casa Propia", 5: "ICL"}),
        ("7. resumen_trades",
         lambda: resumen_trades(TRADES),
         {"BTCUSDT": {"ganados": 2, "perdidos": 1},
          "ETHUSDT": {"ganados": 0, "perdidos": 1},
          "SOLUSDT": {"ganados": 1, "perdidos": 0}}),
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
        print("¡Muy bien! Escribí tus notas y pedile a Claude la autoevaluación.")


if __name__ == "__main__":
    verificar()
