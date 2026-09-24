"""
Módulo contratos: la lógica de negocio del ajuste por ICL.

Fijate que este módulo NO importa requests ni sabe nada de la API.
Eso es a propósito: separar "de dónde vienen los datos" de "qué hago
con los datos" es una de las decisiones de diseño más importantes que
vas a tomar en cualquier sistema. Te permite testear los cálculos sin
internet, y cambiar la fuente de datos sin tocar los cálculos.
"""


# ---------------------------------------------------------------
# Ejercicio 5a: el cálculo del ajuste
# ---------------------------------------------------------------
def aplicar_ajuste_icl(monto_original, icl_inicio, icl_actual):
    """
    El ICL es un índice acumulado. El monto actualizado es:

        monto_original * (icl_actual / icl_inicio)

    Devolvelo redondeado a 2 decimales.

    Ejemplo: aplicar_ajuste_icl(250000, 20.0, 35.87) -> 448375.0

    - Si "icl_inicio" es 0 o negativo, lanzá un ValueError con el
      mensaje "El ICL inicial tiene que ser mayor a 0". No devuelvas
      None: un índice inválido es un dato roto, y quien llame a esta
      función tiene que enterarse.
    """
    try:
      monto_actualizado = monto_original * (icl_actual / icl_inicio)
    except (ValueError,ZeroDivisionError):
       print("El ICL inicial tiene que ser mayor a 0")
    else:
       return round(monto_actualizado,2)

# ---------------------------------------------------------------
# Ejercicio 5b: aplicarlo a una cartera de contratos
# ---------------------------------------------------------------
def actualizar_contratos(contratos, icl_actual):
    """
    "contratos" es una lista de diccionarios, cada uno con al menos
    "monto_original" e "icl_inicio".

    Devolvé una TUPLA (lista_actualizada, cantidad_con_error):

    - "lista_actualizada": una lista NUEVA de diccionarios. Cada uno es
      una COPIA del original (usá .copy(), como viste en la lección 01)
      más una clave "monto_actualizado" con el resultado de
      aplicar_ajuste_icl().
    - Si aplicar_ajuste_icl() lanza ValueError para un contrato, ese
      contrato igual entra en la lista, pero con "monto_actualizado"
      en None. Un contrato roto NO tiene que frenar el procesamiento
      de los demás (mismo patrón que el lote de trades de la lección 02).
    - "cantidad_con_error": cuántos contratos fallaron.

    No modifiques los diccionarios originales.
    """

    raise NotImplementedError
