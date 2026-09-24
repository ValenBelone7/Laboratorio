"""
Lección 03: Módulos, paquetes, entornos virtuales, uv y APIs con requests
==========================================================================

EJERCICIO 1 (setup): antes de escribir una línea de código, dejá el
proyecto andando. Desde la RAÍZ del laboratorio (~/dev/laboratorio-dev):

    uv init --bare
    uv add requests

Eso te crea pyproject.toml, uv.lock y .venv/. Después, ejecutá SIEMPRE
esta lección así (fijate que es "uv run", no "python" a secas):

    uv run python fase-1-python/leccion-03-modulos-paquetes-apis/ejercicios.py

Reglas de siempre:
1. Reemplazá cada `raise NotImplementedError` por tu código. SIN IA.
   Los ejercicios 2, 3 y 4 están en indices/bcra.py
   Los ejercicios 5a y 5b están en indices/contratos.py
   El ejercicio 6 está en indices/__init__.py
2. ✅ = correcto   ❌ = incorrecto   ⏳ = todavía no lo hiciste
3. No modifiques los datos ni la función verificar().
"""

import sys

try:
    import requests
except ModuleNotFoundError:
    print("❌ No encuentro el paquete 'requests' en este entorno.")
    print()
    print("   Eso es el Ejercicio 1. Desde la raíz del laboratorio:")
    print("       uv init --bare")
    print("       uv add requests")
    print()
    print("   Y después ejecutá esta lección con:")
    print("       uv run python fase-1-python/leccion-03-modulos-paquetes-apis/ejercicios.py")
    print()
    print("   (Si corrés 'python' a secas en vez de 'uv run python', Python usa")
    print("    el intérprete del sistema y no ve el .venv del proyecto.)")
    sys.exit(1)


# ===============================================================
# Ejercicio 1 (segunda parte): los imports del paquete
# ===============================================================
# Escribí acá abajo los imports del paquete "indices". Necesitás traer,
# con imports ABSOLUTOS (no relativos):
#
#   de indices.bcra       -> extraer_valores, ultimo_valor, obtener_serie_icl
#   de indices.contratos  -> aplicar_ajuste_icl, actualizar_contratos
#
# Acordate del orden que manda PEP 8: estándar, terceros, y recién
# después tu propio código (por eso van acá abajo y no arriba de todo).

# TODO: tus imports acá

from indices.bcra import extraer_valores, ultimo_valor, obtener_serie_icl
from indices.contratos import aplicar_ajuste_icl,actualizar_contratos

# ===============================================================
# Datos de prueba (no los toques)
# ===============================================================

# Respuesta real de:
# https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/40?desde=2026-09-01&hasta=2026-09-05
RESPUESTA_BCRA = {
    "status": 200,
    "metadata": {"resultset": {"count": 5, "offset": 0, "limit": 1000}},
    "results": [
        {
            "idVariable": 40,
            "detalle": [
                {"fecha": "2026-09-05", "valor": 35.87},
                {"fecha": "2026-09-04", "valor": 35.83},
                {"fecha": "2026-09-03", "valor": 35.8},
                {"fecha": "2026-09-02", "valor": 35.77},
                {"fecha": "2026-09-01", "valor": 35.74},
            ],
        }
    ],
}

# La misma serie pero desordenada, para chequear que no te apoyes en el orden
RESPUESTA_DESORDENADA = {
    "status": 200,
    "metadata": {"resultset": {"count": 3, "offset": 0, "limit": 1000}},
    "results": [
        {
            "idVariable": 40,
            "detalle": [
                {"fecha": "2026-09-02", "valor": 35.77},
                {"fecha": "2026-09-05", "valor": 35.87},
                {"fecha": "2026-09-01", "valor": 35.74},
            ],
        }
    ],
}

RESPUESTA_VACIA = {
    "status": 200,
    "metadata": {"resultset": {"count": 0, "offset": 0, "limit": 1000}},
    "results": [],
}

CONTRATOS = [
    {"id": 1, "inquilino": "Lucía Gómez", "monto_original": 250000, "icl_inicio": 20.0},
    {"id": 2, "inquilino": "Martín Pérez", "monto_original": 180000, "icl_inicio": 25.0},
    {"id": 3, "inquilino": "Sofía Ruiz", "monto_original": 320000, "icl_inicio": 0},
]


# ===============================================================
# Verificación: no hace falta que entiendas este código todavía
# ===============================================================
class RespuestaFalsa:
    """Imita lo mínimo de un objeto Response de requests, sin red."""

    def __init__(self, datos, status_code=200):
        self._datos = datos
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"{self.status_code} Error")

    def json(self):
        return self._datos


class ClienteFalso:
    """Imita requests (solo .get()) y anota con qué lo llamaron."""

    def __init__(self, respuesta=None, excepcion=None):
        self.respuesta = respuesta
        self.excepcion = excepcion
        self.url_usada = None
        self.params_usados = None
        self.timeout_usado = None

    def get(self, url, params=None, timeout=None):
        self.url_usada = url
        self.params_usados = params
        self.timeout_usado = timeout
        if self.excepcion is not None:
            raise self.excepcion
        return self.respuesta


def _probar_valor(nombre, funcion, esperado, correctos):
    try:
        obtenido = funcion()
    except NotImplementedError:
        print(f"⏳ {nombre}: sin resolver")
        return correctos
    except Exception as e:
        print(f"❌ {nombre}: error {type(e).__name__}: {e}")
        return correctos
    if obtenido == esperado:
        print(f"✅ {nombre}")
        return correctos + 1
    print(f"❌ {nombre}\n   esperado: {esperado}\n   obtenido: {obtenido}")
    return correctos


def _probar_excepcion(nombre, funcion, tipo_esperado, correctos):
    try:
        obtenido = funcion()
    except NotImplementedError:
        print(f"⏳ {nombre}: sin resolver")
        return correctos
    except tipo_esperado:
        print(f"✅ {nombre}")
        return correctos + 1
    except Exception as e:
        print(f"❌ {nombre}: esperaba {tipo_esperado.__name__}, salió {type(e).__name__}: {e}")
        return correctos
    else:
        print(f"❌ {nombre}: no lanzó ninguna excepción (devolvió {obtenido!r})")
        return correctos


def verificar():
    correctos = 0
    total = 18

    requeridos = [
        "extraer_valores",
        "ultimo_valor",
        "obtener_serie_icl",
        "aplicar_ajuste_icl",
        "actualizar_contratos",
    ]
    faltantes = [nombre for nombre in requeridos if nombre not in globals()]
    if faltantes:
        print("⏳ 1. imports: todavía falta traer -> " + ", ".join(faltantes))
        print("   Escribilos en la sección 'Ejercicio 1' y volvé a correr.")
        print(f"\n0/{total} correctos")
        return
    print("✅ 1. imports")
    correctos += 1

    # --- Ejercicio 2: extraer_valores ---
    correctos = _probar_valor(
        "2a. extraer_valores - respuesta real",
        lambda: extraer_valores(RESPUESTA_BCRA),
        {"2026-09-05": 35.87, "2026-09-04": 35.83, "2026-09-03": 35.8,
         "2026-09-02": 35.77, "2026-09-01": 35.74},
        correctos,
    )
    correctos = _probar_valor(
        "2b. extraer_valores - results vacío",
        lambda: extraer_valores(RESPUESTA_VACIA), {}, correctos,
    )
    correctos = _probar_valor(
        "2c. extraer_valores - sin la clave results",
        lambda: extraer_valores({"status": 200}), {}, correctos,
    )

    # --- Ejercicio 3: ultimo_valor ---
    correctos = _probar_valor(
        "3a. ultimo_valor - respuesta real",
        lambda: ultimo_valor(RESPUESTA_BCRA), ("2026-09-05", 35.87), correctos,
    )
    correctos = _probar_valor(
        "3b. ultimo_valor - serie desordenada",
        lambda: ultimo_valor(RESPUESTA_DESORDENADA), ("2026-09-05", 35.87), correctos,
    )
    correctos = _probar_valor(
        "3c. ultimo_valor - sin datos",
        lambda: ultimo_valor(RESPUESTA_VACIA), None, correctos,
    )

    # --- Ejercicio 4: obtener_serie_icl ---
    cliente_ok = ClienteFalso(respuesta=RespuestaFalsa(RESPUESTA_BCRA))
    correctos = _probar_valor(
        "4a. obtener_serie_icl - respuesta OK",
        lambda: obtener_serie_icl("2026-09-01", "2026-09-05", cliente_ok),
        RESPUESTA_BCRA,
        correctos,
    )
    correctos = _probar_valor(
        "4b. obtener_serie_icl - pasó los params correctos",
        lambda: cliente_ok.params_usados,
        {"desde": "2026-09-01", "hasta": "2026-09-05"},
        correctos,
    )
    nombre = "4c. obtener_serie_icl - pasó un timeout"
    if cliente_ok.timeout_usado is None:
        print(f"❌ {nombre}: llamaste a .get() sin timeout (o todavía no lo resolviste)")
    else:
        print(f"✅ {nombre}")
        correctos += 1

    cliente_timeout = ClienteFalso(excepcion=requests.exceptions.Timeout("tardó demasiado"))
    correctos = _probar_valor(
        "4d. obtener_serie_icl - timeout devuelve None",
        lambda: obtener_serie_icl("2026-09-01", "2026-09-05", cliente_timeout),
        None,
        correctos,
    )
    cliente_500 = ClienteFalso(respuesta=RespuestaFalsa({"error": "boom"}, status_code=500))
    correctos = _probar_valor(
        "4e. obtener_serie_icl - error 500 devuelve None",
        lambda: obtener_serie_icl("2026-09-01", "2026-09-05", cliente_500),
        None,
        correctos,
    )

    # --- Ejercicio 5a: aplicar_ajuste_icl ---
    correctos = _probar_valor(
        "5a. aplicar_ajuste_icl - caso normal",
        lambda: aplicar_ajuste_icl(250000, 20.0, 35.87), 448375.0, correctos,
    )
    correctos = _probar_valor(
        "5b. aplicar_ajuste_icl - otro contrato",
        lambda: aplicar_ajuste_icl(180000, 25.0, 35.87), 258264.0, correctos,
    )
    correctos = _probar_excepcion(
        "5c. aplicar_ajuste_icl - icl_inicio inválido",
        lambda: aplicar_ajuste_icl(250000, 0, 35.87), ValueError, correctos,
    )

    # --- Ejercicio 5b: actualizar_contratos ---
    esperado_lista = [
        {"id": 1, "inquilino": "Lucía Gómez", "monto_original": 250000,
         "icl_inicio": 20.0, "monto_actualizado": 448375.0},
        {"id": 2, "inquilino": "Martín Pérez", "monto_original": 180000,
         "icl_inicio": 25.0, "monto_actualizado": 258264.0},
        {"id": 3, "inquilino": "Sofía Ruiz", "monto_original": 320000,
         "icl_inicio": 0, "monto_actualizado": None},
    ]
    correctos = _probar_valor(
        "5d. actualizar_contratos",
        lambda: actualizar_contratos(CONTRATOS, 35.87),
        (esperado_lista, 1),
        correctos,
    )
    nombre = "5e. actualizar_contratos - no mutó los originales"
    if any("monto_actualizado" in c for c in CONTRATOS):
        print(f"❌ {nombre}: le agregaste la clave a los diccionarios originales")
    else:
        print(f"✅ {nombre}")
        correctos += 1

    # --- Ejercicio 6: __init__.py ---
    nombre = "6. indices/__init__.py re-exporta aplicar_ajuste_icl"
    import indices
    if hasattr(indices, "aplicar_ajuste_icl"):
        print(f"✅ {nombre}")
        correctos += 1
    else:
        print(f"⏳ {nombre}: sin resolver")

    print(f"\n{correctos}/{total} correctos")
    if correctos == total:
        print("¡Muy bien! Escribí tus notas y pedile a Claude la autoevaluación.")


if __name__ == "__main__":
    verificar()
