"""
Lección 02: Manejo de errores, archivos y JSON
================================================
Instrucciones:
1. Leé teoria.md antes de empezar.
2. Reemplazá cada `raise NotImplementedError` por tu código. SIN IA.
3. Ejecutá:  python ejercicios.py
   ✅ = correcto   ❌ = incorrecto   ⏳ = todavía no lo hiciste
4. No modifiques los datos ni la función verificar().
"""

import json
import os
import tempfile

STOCK_KIOSCO = {
    "Alfajor": 40,
    "Coca 500ml": 15,
    "Chocolate": 8,
}


# ---------------------------------------------------------------
# Ejercicio 1: Excepciones específicas
# ---------------------------------------------------------------
def calcular_cuota_mensual(monto_total, cantidad_cuotas):
    """
    Devolvé monto_total / cantidad_cuotas, redondeado a 2 decimales.

    - Si cantidad_cuotas es 0, capturá el ZeroDivisionError y devolvé None.
    - Si alguno de los dos argumentos no es un número (por ejemplo, llega
      como string), capturá el TypeError y devolvé None.
    - No uses "if cantidad_cuotas == 0" a mano: dejá que la división
      lance la excepción y capturala. El objetivo del ejercicio es
      practicar except, no evitarlo con un if.
    """

    try:
        resultado = monto_total / cantidad_cuotas
    except (TypeError, ZeroDivisionError):
        return None
    else:
        return round(resultado,2)

# ---------------------------------------------------------------
# Ejercicio 2: try / except / else
# ---------------------------------------------------------------
def convertir_a_entero(texto):
    """
    Intentá convertir "texto" a int con int(texto).

    - Si falla (ValueError), devolvé None.
    - Si funciona, devolvé el valor convertido, pero el return del caso
      exitoso tiene que ir en el bloque "else", no dentro del "try".
    """

    try:
        numero = int(texto)
    except ValueError:
        return None
    else:
        return numero


# ---------------------------------------------------------------
# Ejercicio 3: finally
# ---------------------------------------------------------------
def actualizar_stock(stock, producto, cantidad, intentos):
    """
    stock: dict {producto: cantidad_actual} (lo vas a MODIFICAR in-place).
    intentos: lista vacía o con elementos previos.

    - Sumale "cantidad" al stock actual de "producto" (cantidad puede ser
      negativa, por ejemplo una venta) y guardá el resultado en stock[producto].
      Devolvé ese nuevo valor.
    - Si "producto" no existe en stock, capturá el KeyError y devolvé None
      (no modifiques stock en ese caso).
    - Sin importar qué pase (haya salido bien o mal), agregá el string
      "intento" a la lista "intentos". Usá un bloque finally para esto,
      no lo repitas en cada rama.
    """

    try:
        stock[producto] += cantidad
    except KeyError:
        return None
    else:
        return stock[producto]
    finally:
        intentos.append('intento')


# ---------------------------------------------------------------
# Ejercicio 4: raise manual (validar una regla de negocio)
# ---------------------------------------------------------------
def validar_monto_alquiler(monto):
    """
    Si "monto" es menor o igual a 0, lanzá un ValueError con el mensaje
    "El monto tiene que ser positivo".
    Si es válido, devolvé el monto sin modificar.
    """
    if monto <= 0:
        raise ValueError('El monto debe ser positivo')
    else:
        return monto

# ---------------------------------------------------------------
# Ejercicio 5: excepción propia
# ---------------------------------------------------------------
class MoraExcesivaError(Exception):
    """
    Se lanza cuando la mora de un inquilino supera el límite permitido.

    Completá __init__ para que:
    - Reciba "inquilino" y "monto_mora" y los guarde como self.inquilino
      y self.monto_mora.
    - Llame a super().__init__(mensaje), con un mensaje armado por vos que
      incluya el nombre del inquilino y el monto de la mora.
    """

    def __init__(self, inquilino, monto_mora):
        self.inquilino = inquilino
        self.monto_mora = monto_mora
        super().__init__(f'El inquilino {self.inquilino} ha superado el limite de mora permitido: {self.monto_mora}')


def verificar_mora(inquilino, monto_mora, limite):
    """
    Si "monto_mora" es mayor que "limite", lanzá MoraExcesivaError(inquilino, monto_mora).
    Si no, devolvé el string "ok".
    """

    if monto_mora > limite:
        raise MoraExcesivaError(inquilino,monto_mora)
    else:
        return 'ok'

# ---------------------------------------------------------------
# Ejercicio 6: archivos con with (escribir JSON)
# ---------------------------------------------------------------
def guardar_resumen_stock(ruta, resumen):
    """
    Escribí el diccionario "resumen" en el archivo "ruta" como JSON.

    Usá with open(...) y json.dump(). Configuralo con indent=2 y
    ensure_ascii=False para que quede legible y con tildes correctas.
    No necesitás devolver nada.
    """

    with open(ruta,'w',encoding='utf-8') as f:
        json.dump(resumen, f, indent=2 ,ensure_ascii=False)
# ---------------------------------------------------------------
# Ejercicio 7: archivos con with (leer JSON con manejo de errores)
# ---------------------------------------------------------------
def cargar_contratos(ruta):
    """
    Abrí "ruta", leé su contenido como JSON y devolvelo.

    - Si el archivo no existe, capturá FileNotFoundError y devolvé [].
    - Si el archivo existe pero su contenido no es JSON válido, capturá
      json.JSONDecodeError y devolvé [].
    - Si todo sale bien, devolvé lo que devuelva json.load().
    """

    try:
        with open(ruta,'r',encoding='utf-8') as f:
            texto = json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        return []
    else:
        return texto

# ---------------------------------------------------------------
# Ejercicio 8 (desafío): procesar un archivo con registros inválidos
# ---------------------------------------------------------------
def procesar_lote_trades(ruta):
    """
    "ruta" apunta a un archivo JSON con una LISTA de trades, cada uno
    con la forma {"par": "BTCUSDT", "resultado": 45.0}. Algunos
    registros pueden venir rotos: sin la clave "resultado", o con
    "resultado" como string en vez de número.

    Devolvé un diccionario {"procesados": N, "invalidos": M}:
    - "procesados": cantidad de trades que pudiste leer y sumar bien
      (no importa si ganaron o perdieron, solo que el dato era válido).
      Para saber si "resultado" es válido, sumale 0.0 (float(resultado) + 0.0
      o simplemente usalo en una cuenta): si el registro no tiene la clave
      ("resultado") vas a tener un KeyError, y si el valor no es numérico
      vas a tener un TypeError. Un registro roto NO tiene que frenar el
      procesamiento de los demás.
    - "invalidos": cantidad de registros que fallaron por cualquiera de
      esos dos motivos.

    Si "ruta" no existe o no es JSON válido, devolvé
    {"procesados": 0, "invalidos": 0} directamente (sin abrir nada más).
    """

    resultado = {
        'procesados':0,
        'invalidos':0
    }


    try:
        with open(ruta,'r',encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return resultado
    else:
        for t in data:
            try:
                float(t['resultado']) + 0.0
            except (KeyError,TypeError,ValueError):
                resultado["invalidos"] += 1
            else:
                resultado["procesados"] += 1

        return resultado

# ===============================================================
# Verificación: no hace falta que entiendas este código todavía
# (lo vas a entender en las lecciones 03 y 07).
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


def _probar_excepcion(nombre, funcion, tipo_esperado, chequeo_extra, correctos):
    try:
        obtenido = funcion()
    except NotImplementedError:
        print(f"⏳ {nombre}: sin resolver")
        return correctos
    except tipo_esperado as e:
        if chequeo_extra is not None and not chequeo_extra(e):
            print(f"❌ {nombre}: lanzó {type(e).__name__} pero con datos incorrectos")
            return correctos
        print(f"✅ {nombre}")
        return correctos + 1
    except Exception as e:
        print(f"❌ {nombre}: esperaba {tipo_esperado.__name__}, lanzó {type(e).__name__}: {e}")
        return correctos
    else:
        print(f"❌ {nombre}: no lanzó ninguna excepción (devolvió {obtenido!r})")
        return correctos


def verificar():
    correctos = 0
    total = 17

    casos_valor = [
        ("1a. calcular_cuota_mensual - caso normal", lambda: calcular_cuota_mensual(300000, 3), 100000.0),
        ("1b. calcular_cuota_mensual - cero cuotas", lambda: calcular_cuota_mensual(300000, 0), None),
        ("1c. calcular_cuota_mensual - tipo inválido", lambda: calcular_cuota_mensual("300000", 3), None),
        ("2a. convertir_a_entero - texto válido", lambda: convertir_a_entero("42"), 42),
        ("2b. convertir_a_entero - texto inválido", lambda: convertir_a_entero("cuarenta"), None),
        ("4a. validar_monto_alquiler - monto válido", lambda: validar_monto_alquiler(250000), 250000),
    ]
    for nombre, funcion, esperado in casos_valor:
        correctos = _probar_valor(nombre, funcion, esperado, correctos)

    # Ejercicio 3: dos llamadas sobre el mismo stock/intentos
    stock = dict(STOCK_KIOSCO)
    intentos = []
    correctos = _probar_valor(
        "3a. actualizar_stock - producto existente",
        lambda: actualizar_stock(stock, "Alfajor", -5, intentos),
        35,
        correctos,
    )
    correctos = _probar_valor(
        "3b. actualizar_stock - producto inexistente",
        lambda: actualizar_stock(stock, "Fanta", 10, intentos),
        None,
        correctos,
    )
    correctos = _probar_valor(
        "3c. actualizar_stock - finally corrió las dos veces",
        lambda: intentos,
        ["intento", "intento"],
        correctos,
    )

    correctos = _probar_excepcion(
        "4b. validar_monto_alquiler - monto inválido",
        lambda: validar_monto_alquiler(-100),
        ValueError,
        None,
        correctos,
    )

    correctos = _probar_valor(
        "5a. verificar_mora - dentro del límite",
        lambda: verificar_mora("Bruno Sosa", 20000, 50000),
        "ok",
        correctos,
    )
    correctos = _probar_excepcion(
        "5b. verificar_mora - supera el límite",
        lambda: verificar_mora("Carla Nieva", 80000, 50000),
        MoraExcesivaError,
        lambda e: e.inquilino == "Carla Nieva" and e.monto_mora == 80000,
        correctos,
    )

    # Ejercicios 6, 7 y 8: usan archivos reales en un directorio temporal
    with tempfile.TemporaryDirectory() as carpeta:
        ruta_resumen = os.path.join(carpeta, "resumen.json")
        try:
            guardar_resumen_stock(ruta_resumen, {"Alfajor": 35, "Chocolate": 8})
            with open(ruta_resumen, encoding="utf-8") as f:
                contenido = json.load(f)
            if contenido == {"Alfajor": 35, "Chocolate": 8}:
                print("✅ 6. guardar_resumen_stock")
                correctos += 1
            else:
                print(f"❌ 6. guardar_resumen_stock: contenido incorrecto -> {contenido}")
        except NotImplementedError:
            print("⏳ 6. guardar_resumen_stock: sin resolver")
        except Exception as e:
            print(f"❌ 6. guardar_resumen_stock: error {type(e).__name__}: {e}")

        ruta_valida = os.path.join(carpeta, "contratos_ok.json")
        with open(ruta_valida, "w", encoding="utf-8") as f:
            json.dump([{"id": 1, "inquilino": "Lucía Gómez"}], f)

        ruta_corrupta = os.path.join(carpeta, "contratos_corrupto.json")
        with open(ruta_corrupta, "w", encoding="utf-8") as f:
            f.write("{esto no es json valido,,,")

        ruta_inexistente = os.path.join(carpeta, "no_existe.json")

        correctos = _probar_valor(
            "7a. cargar_contratos - archivo válido",
            lambda: cargar_contratos(ruta_valida),
            [{"id": 1, "inquilino": "Lucía Gómez"}],
            correctos,
        )
        correctos = _probar_valor(
            "7b. cargar_contratos - archivo inexistente",
            lambda: cargar_contratos(ruta_inexistente),
            [],
            correctos,
        )
        correctos = _probar_valor(
            "7c. cargar_contratos - archivo corrupto",
            lambda: cargar_contratos(ruta_corrupta),
            [],
            correctos,
        )

        ruta_trades = os.path.join(carpeta, "trades.json")
        with open(ruta_trades, "w", encoding="utf-8") as f:
            json.dump(
                [
                    {"par": "BTCUSDT", "resultado": 45.0},
                    {"par": "ETHUSDT", "resultado": -12.0},
                    {"par": "SOLUSDT"},
                    {"par": "BTCUSDT", "resultado": "no es un número"},
                ],
                f,
            )
        correctos = _probar_valor(
            "8. procesar_lote_trades",
            lambda: procesar_lote_trades(ruta_trades),
            {"procesados": 2, "invalidos": 2},
            correctos,
        )

    print(f"\n{correctos}/{total} correctos")
    if correctos == total:
        print("¡Muy bien! Escribí tus notas y pedile a Claude la autoevaluación.")


if __name__ == "__main__":
    verificar()
