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
    raise NotImplementedError


# ---------------------------------------------------------------
# Ejercicio 2: Acumular
# ---------------------------------------------------------------
def total_adeudado(contratos):
    """
    Devolvé la suma de los montos de los contratos "pendiente" o "vencido".
    """
    raise NotImplementedError


# ---------------------------------------------------------------
# Ejercicio 3: El patrón "agrupar"
# ---------------------------------------------------------------
def agrupar_por_indice(contratos):
    """
    Devolvé un diccionario donde la clave es el índice de aumento
    y el valor es una lista con los ids de los contratos que lo usan.

    Ejemplo de forma:  {"ICL": [1, 5], ...}
    """
    raise NotImplementedError


# ---------------------------------------------------------------
# Ejercicio 4: Tuplas y varios valores de retorno
# ---------------------------------------------------------------
def aplicar_aumento(monto, porcentaje):
    """
    Devolvé una TUPLA (monto_nuevo, diferencia), ambos redondeados
    a 2 decimales con round().

    Ejemplo: aplicar_aumento(200000, 10) -> (220000.0, 20000.0)
    """
    raise NotImplementedError


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
    raise NotImplementedError


# ---------------------------------------------------------------
# Ejercicio 6: Comprensiones
# ---------------------------------------------------------------
def montos_con_aumento(contratos, porcentaje):
    """
    Con UNA comprensión de lista, devolvé los montos con el aumento
    aplicado, redondeados a 2 decimales.
    """
    raise NotImplementedError


def indice_por_id(contratos):
    """
    Con UNA comprensión de diccionario, devolvé {id: indice}.
    """
    raise NotImplementedError


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
    raise NotImplementedError


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
