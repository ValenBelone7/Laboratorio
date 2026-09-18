"""
Repaso de la Lección 02: Manejo de errores, archivos y JSON
==============================================================
No es una lección nueva, es una vuelta más con datos distintos.
Apunta especialmente a lo que costó (o casi se escapó) la primera vez:
  - el alcance del try: proteger TODO lo riesgoso, no solo una parte
  - finally vs. duplicar código en try/except: no son lo mismo cuando
    hay una excepción que no capturás
  - validar tipos de verdad (no aceptar un string numérico como si
    fuera un número)

Mismas reglas que siempre:
1. Reemplazá cada `raise NotImplementedError` por tu código. SIN IA.
2. Ejecutá:  python repaso.py
3. No modifiques los datos ni verificar().
"""

import json
import os
import tempfile


# ---------------------------------------------------------------
# 1. El alcance del try (el bug del ejercicio 7, otra vez)
# ---------------------------------------------------------------
def obtener_precio_par(ruta, par):
    """
    "ruta" apunta a un archivo JSON con la forma {"BTCUSDT": 97000, ...}.
    Devolvé el precio de "par".

    Pensá TODO lo que puede fallar antes de escribir el try:
    - Que el archivo no exista.
    - Que el archivo exista pero no sea JSON válido.
    - Que "par" no esté en el diccionario.

    Las tres tienen que quedar protegidas por el MISMO try (varios
    except, uno por cada caso). Si alguna de esas tres cosas falla,
    devolvé None.
    """

    try:
        with open(ruta,'r',encoding='utf-8') as f:
            data = json.load(f)
        precio = data[par]
    except (FileNotFoundError, json.JSONDecodeError,KeyError,TypeError):
        return None
    else:
        return precio
# ---------------------------------------------------------------
# 2. finally vs. duplicar en try/except
# ---------------------------------------------------------------
def cerrar_posicion(posiciones, par, precio_actual, cierres):
    """
    posiciones: dict {par: precio_de_entrada}.
    Calculá el resultado en porcentaje:
        (precio_actual - posiciones[par]) / posiciones[par] * 100
    redondeado a 2 decimales con round().

    - Si "par" no existe en posiciones, capturá el KeyError y devolvé None.
    - NO captures ningún otro tipo de excepción. En particular, si
      posiciones[par] es 0, el ZeroDivisionError tiene que propagarse
      sin que lo atrapes (no le pongas un except).
    - Pase lo que pase —incluso si terminás dejando que una excepción
      se propague sin capturarla— agregá el string "cierre" a la lista
      "cierres". Usá finally para esto.
    """

    try:
        resultado = (precio_actual - posiciones[par]) / posiciones[par] * 100
    except KeyError:
        return None
    else:
        return round(resultado,2)
    finally:
        cierres.append('cierre')

# ---------------------------------------------------------------
# 3. Validar tipos de verdad (no con float())
# ---------------------------------------------------------------
def sumar_montos_validos(registros):
    """
    "registros" es una lista de dicts, cada uno debería tener una clave
    "monto". Devolvé una tupla (suma_total, cantidad_invalidos):

    - "suma_total": la suma de los "monto" que sean números de verdad
      (int o float).
    - "cantidad_invalidos": cuántos registros NO se pudieron sumar,
      ya sea porque no tienen la clave "monto" (KeyError) o porque
      "monto" no es un número, por ejemplo llega como string (TypeError).

    Importante: para decidir si "monto" es válido, usá
    `registro["monto"] + 0` (sumarle 0 directo). NO uses float(...):
    float("2000") funciona y convierte el string en 2000.0, que es
    justo lo que NO queremos aceptar acá — un monto que llegó como
    texto es un dato roto, no algo para "arreglar" en silencio.
    """
    suma_total = 0
    cantidad_invalidos = 0
    for r in registros:
        try:
            suma_total += r['monto'] + 0
        except (KeyError, TypeError):
            cantidad_invalidos += 1

    return suma_total,cantidad_invalidos
# ---------------------------------------------------------------
# 4. Excepción propia con varios atributos
# ---------------------------------------------------------------
class SaldoInsuficienteError(Exception):
    """
    Se lanza cuando se intenta retirar más de lo disponible en un exchange.

    Completá __init__ para que reciba "exchange", "monto_solicitado" y
    "saldo_disponible", los guarde como atributos (self.exchange,
    self.monto_solicitado, self.saldo_disponible) y llame a
    super().__init__() con un mensaje que incluya los tres datos.
    """

    def __init__(self, exchange, monto_solicitado, saldo_disponible):
        self.exchange = exchange
        self.monto_solicitado = monto_solicitado
        self.saldo_disponible = saldo_disponible
        super().__init__(f'{exchange} Error: Intenta retirar {monto_solicitado} y es mas del monto disponibl0e. Monto disponible: {saldo_disponible}')


def retirar_fondos(saldos, exchange, monto):
    """
    saldos: dict {exchange: saldo_disponible} (lo vas a MODIFICAR in-place).

    - Si "monto" es mayor al saldo disponible de "exchange" (usá
      saldos.get(exchange, 0)), lanzá
      SaldoInsuficienteError(exchange, monto, saldo_disponible).
    - Si no, restale "monto" al saldo de ese exchange, guardá el
      resultado y devolvelo.
    """

    if monto > saldos.get(exchange,0):
        raise SaldoInsuficienteError(exchange,monto,saldos[exchange])
    else:
        resultado = saldos[exchange] - monto

    return resultado
# ---------------------------------------------------------------
# 5. with + JSON de escritura, transformando los datos antes
# ---------------------------------------------------------------
def guardar_historial_trades(ruta, trades):
    """
    "trades" es una lista de tuplas (par, resultado), igual que en la
    lección 01. Guardá en "ruta" un JSON con esta forma:

        {
          "total_trades": 2,
          "trades": [
            {"par": "BTCUSDT", "resultado": 45.0},
            {"par": "ETHUSDT", "resultado": -12.0}
          ]
        }

    Tenés que transformar la lista de tuplas en la lista de diccionarios
    ANTES de escribirla. Usá with + json.dump, con indent=2.
    """
    diccionario_trades = {'total_trades':0,'trades':[]}
    for par, resultado in trades:
        diccionario_trades["total_trades"] += 1
        diccionario_trades['trades'].append({"par":par,"resultado":resultado})
    
    try:
        with open(ruta,'w',encoding='utf-8') as f:
            json.dump(diccionario_trades,f,ensure_ascii=False,indent=2)
    except (json.JSONDecodeError, FileNotFoundError):
        return None

# ---------------------------------------------------------------
# 6. Lectura de JSON con un default que viene por parámetro
# ---------------------------------------------------------------
def cargar_configuracion(ruta, valores_default):
    """
    Leé el JSON en "ruta" y devolvelo.

    - Si el archivo no existe o no es JSON válido, devolvé
      "valores_default" tal cual te lo pasaron (no un [] fijo:
      en este ejercicio el default lo decide quien llama a la función).
    """

    try:
        with open(ruta,'r',encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return valores_default
    else:
        return data

# ===============================================================
# Verificación
# ===============================================================
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


def verificar():
    correctos = 0
    total = 14

    with tempfile.TemporaryDirectory() as carpeta:
        # --- Ejercicio 1 ---
        ruta_precios = os.path.join(carpeta, "precios.json")
        with open(ruta_precios, "w", encoding="utf-8") as f:
            json.dump({"BTCUSDT": 97000, "ETHUSDT": 3500}, f)
        ruta_corrupta = os.path.join(carpeta, "precios_corrupto.json")
        with open(ruta_corrupta, "w", encoding="utf-8") as f:
            f.write("{esto no es json,,,")
        ruta_inexistente = os.path.join(carpeta, "no_existe.json")

        correctos = _probar_valor("1a. obtener_precio_par - par existente",
                                   lambda: obtener_precio_par(ruta_precios, "BTCUSDT"), 97000, correctos)
        correctos = _probar_valor("1b. obtener_precio_par - par inexistente",
                                   lambda: obtener_precio_par(ruta_precios, "SOLUSDT"), None, correctos)
        correctos = _probar_valor("1c. obtener_precio_par - archivo inexistente",
                                   lambda: obtener_precio_par(ruta_inexistente, "BTCUSDT"), None, correctos)
        correctos = _probar_valor("1d. obtener_precio_par - archivo corrupto",
                                   lambda: obtener_precio_par(ruta_corrupta, "BTCUSDT"), None, correctos)

        # --- Ejercicio 2 ---
        posiciones = {"BTCUSDT": 90000, "ETHUSDT": 0}
        cierres = []
        correctos = _probar_valor("2a. cerrar_posicion - ganancia",
                                   lambda: cerrar_posicion(posiciones, "BTCUSDT", 97000, cierres), 7.78, correctos)
        correctos = _probar_valor("2b. cerrar_posicion - par inexistente",
                                   lambda: cerrar_posicion(posiciones, "SOLUSDT", 100, cierres), None, correctos)

        nombre = "2c. cerrar_posicion - excepción no capturada + finally"
        try:
            cerrar_posicion(posiciones, "ETHUSDT", 100, cierres)
        except NotImplementedError:
            print(f"⏳ {nombre}: sin resolver")
        except ZeroDivisionError:
            if len(cierres) == 3:
                print(f"✅ {nombre}")
                correctos += 1
            else:
                print(f"❌ {nombre}: el finally no corrió (cierres={cierres})")
        except Exception as e:
            print(f"❌ {nombre}: esperaba ZeroDivisionError sin capturar, salió {type(e).__name__}: {e}")
        else:
            print(f"❌ {nombre}: no debía capturar el ZeroDivisionError, pero la función devolvió un valor")

        # --- Ejercicio 3 ---
        registros = [{"monto": 1000}, {"monto": "2000"}, {"monto": 1500.5}, {"otro": 1}]
        correctos = _probar_valor("3. sumar_montos_validos",
                                   lambda: sumar_montos_validos(registros), (2500.5, 2), correctos)

        # --- Ejercicio 4 ---
        saldos = {"Binance": 50000, "Bybit": 10000}
        correctos = _probar_valor("4a. retirar_fondos - saldo suficiente",
                                   lambda: retirar_fondos(saldos, "Binance", 20000), 30000, correctos)

        nombre = "4b. retirar_fondos - saldo insuficiente"
        try:
            retirar_fondos(saldos, "Bybit", 15000)
            print(f"❌ {nombre}: no lanzó SaldoInsuficienteError")
        except NotImplementedError:
            print(f"⏳ {nombre}: sin resolver")
        except SaldoInsuficienteError as e:
            if e.exchange == "Bybit" and e.monto_solicitado == 15000 and e.saldo_disponible == 10000:
                print(f"✅ {nombre}")
                correctos += 1
            else:
                print(f"❌ {nombre}: lanzó SaldoInsuficienteError pero con datos incorrectos")
        except Exception as e:
            print(f"❌ {nombre}: esperaba SaldoInsuficienteError, salió {type(e).__name__}: {e}")

        # --- Ejercicio 5 ---
        ruta_historial = os.path.join(carpeta, "historial.json")
        try:
            guardar_historial_trades(ruta_historial, [("BTCUSDT", 45.0), ("ETHUSDT", -12.0)])
            with open(ruta_historial, encoding="utf-8") as f:
                contenido = json.load(f)
            esperado = {"total_trades": 2, "trades": [
                {"par": "BTCUSDT", "resultado": 45.0}, {"par": "ETHUSDT", "resultado": -12.0}]}
            if contenido == esperado:
                print("✅ 5. guardar_historial_trades")
                correctos += 1
            else:
                print(f"❌ 5. guardar_historial_trades: contenido incorrecto -> {contenido}")
        except NotImplementedError:
            print("⏳ 5. guardar_historial_trades: sin resolver")
        except Exception as e:
            print(f"❌ 5. guardar_historial_trades: error {type(e).__name__}: {e}")

        # --- Ejercicio 6 ---
        default = {"modo": "conservador", "apalancamiento": 1}
        ruta_config_valida = os.path.join(carpeta, "config.json")
        with open(ruta_config_valida, "w", encoding="utf-8") as f:
            json.dump({"modo": "agresivo", "apalancamiento": 5}, f)
        ruta_config_corrupta = os.path.join(carpeta, "config_corrupta.json")
        with open(ruta_config_corrupta, "w", encoding="utf-8") as f:
            f.write("{no es json,,,")
        ruta_config_inexistente = os.path.join(carpeta, "no_existe_config.json")

        correctos = _probar_valor("6a. cargar_configuracion - archivo válido",
                                   lambda: cargar_configuracion(ruta_config_valida, default),
                                   {"modo": "agresivo", "apalancamiento": 5}, correctos)
        correctos = _probar_valor("6b. cargar_configuracion - archivo inexistente",
                                   lambda: cargar_configuracion(ruta_config_inexistente, default),
                                   default, correctos)
        correctos = _probar_valor("6c. cargar_configuracion - archivo corrupto",
                                   lambda: cargar_configuracion(ruta_config_corrupta, default),
                                   default, correctos)

    print(f"\n{correctos}/{total} correctos")
    if correctos == total:
        print("¡Muy bien! Esta lección quedó afianzada.")


if __name__ == "__main__":
    verificar()
