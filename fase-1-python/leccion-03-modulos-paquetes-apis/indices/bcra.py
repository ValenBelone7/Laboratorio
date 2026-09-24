"""
Módulo bcra: consultar la API pública del Banco Central.

La variable 40 es el "Índice para Contratos de Locación (base 30.6.20=1)",
o sea el ICL con el que se ajustan los alquileres.

Documentación y estructura real de la respuesta: ver teoria.md, sección 6.
"""

import requests

URL_ICL = "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/40"


# ---------------------------------------------------------------
# Ejercicio 2: navegar la respuesta real de la API
# ---------------------------------------------------------------
def extraer_valores(respuesta_json):
    """
    Recibe el JSON tal cual lo devuelve el BCRA:

        {
          "status": 200,
          "metadata": {...},
          "results": [
            {"idVariable": 40, "detalle": [
                {"fecha": "2026-09-05", "valor": 35.87},
                {"fecha": "2026-09-04", "valor": 35.83}
            ]}
          ]
        }

    Devolvé un diccionario plano {fecha: valor}:

        {"2026-09-05": 35.87, "2026-09-04": 35.83}

    - Si "results" está vacío, o si no existe alguna de las claves que
      necesitás, devolvé un diccionario vacío {} en vez de romper.
      (Acordate: la API puede responder 200 y aun así no traer lo que
      esperabas.)
    """

    valor_por_fecha = {}

    try:
        for d in respuesta_json.get("results",[])[0]["detalle"]:
            valor_por_fecha[d["fecha"]] = d["valor"]
    except (IndexError,KeyError):
        return {}
    else:
        return valor_por_fecha

# ---------------------------------------------------------------
# Ejercicio 3: encontrar el valor más reciente
# ---------------------------------------------------------------
def ultimo_valor(respuesta_json):
    """
    Devolvé una TUPLA (fecha, valor) correspondiente a la fecha MÁS
    RECIENTE de la serie. Si no hay datos, devolvé None.

    Ojo: hoy el BCRA devuelve la lista ordenada de más nueva a más vieja,
    pero NO te apoyes en ese orden — una API puede cambiarlo sin avisar.
    Buscá explícitamente la fecha mayor.

    Pista: las fechas vienen como "AAAA-MM-DD", y en ese formato comparar
    strings alfabéticamente da el mismo resultado que comparar fechas.
    Podés reutilizar extraer_valores().
    """

    valores_por_fecha = extraer_valores(respuesta_json)
    fecha_mas_reciente = None
    ultimo_indice = 0

    if valores_por_fecha == {}:
        return None
    
    for clave in valores_por_fecha:
        if fecha_mas_reciente == None or fecha_mas_reciente < clave:
            fecha_mas_reciente = clave
            ultimo_indice = valores_por_fecha[clave]

    return fecha_mas_reciente,ultimo_indice

# ---------------------------------------------------------------
# Ejercicio 4: el request de verdad, con manejo de errores
# ---------------------------------------------------------------
def obtener_serie_icl(desde, hasta, cliente=requests):
    """
    Pedile a la API del BCRA la serie del ICL entre dos fechas
    (formato "AAAA-MM-DD") y devolvé el JSON ya parseado.

    Tenés que:
    1. Hacer cliente.get(URL_ICL, params=..., timeout=...) pasando
       "desde" y "hasta" como params y un timeout de 10 segundos.
       ⚠️ El timeout NO es opcional: sin él, el programa puede quedar
       colgado para siempre.
    2. Llamar a .raise_for_status() sobre la respuesta, para que un
       4xx o 5xx se convierta en excepción.
    3. Devolver respuesta.json().
    4. Si algo falla en la conexión (timeout, servidor caído, 4xx/5xx),
       capturar la excepción y devolver None. Usá excepciones de
       requests.exceptions, de la más específica a la más general.

    Sobre el parámetro "cliente": por defecto es el módulo requests, así
    que en la vida real llamás obtener_serie_icl("2026-09-01", "2026-09-05")
    y habla con internet. Los tests, en cambio, le pasan un cliente falso
    para no depender de la conexión. Esto se llama "inyección de
    dependencias" y es lo que hace que el código sea testeable.
    """
    try:
        respuesta = cliente.get(URL_ICL, params={"desde":desde,"hasta":hasta},timeout=10,)
        respuesta.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout,requests.exceptions.HTTPError):
        return None
    else:
        return respuesta.json()