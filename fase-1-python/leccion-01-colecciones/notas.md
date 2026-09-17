# Mis notas: Lección 01

(Escribí acá, con tus palabras, qué entendiste de cada tema. Sin copiar la teoría.)

## Diccionarios

Los diccionarios se confeccionan con Clave : Valor, se utilizan en los JSON, es decir que la respuesta de una API por ejemplo vendria en este formato.
Las claves deben ser unicas como en una base de datos, no deben pisarse e inmutables
Utilizo [] cuando se que la clave debe estar, en caso de no saber si esta utilizo .get()
Accedo a ellos mediante el nombre, es decir si el dict se llama contratos, debo acceder contratos[clave] y me retornaria el valor.
Puedo hacer CUD sobre ellos, sobreescribiendo el acceso a ellos seguido de "=" valor nuevo.
La forma en que puedo constatar el contenido de un dict puede ser mediante un bucle for, sea para buscar si existe tal clave, tal valor o mostrar ambas.
Existen los diccionarios anidados que son comunes dentro de una llamada a la API. Como por ejemplo un dict(contrato) puede tener como clave garantes y dentro de esa clave tener la clave del nombre del garante y su valor + clave de telefono del garante y su valor. A su vez puede ser una lista de diccionarios, ya que son varios garantes.
Y comunmente llegan como JSON listas de diccionarios. Por ejemplo contratos es la lista del diccionario contrato que dentro tiene id,nombre,monto,propietario, etc.
No logro entender el ejemplo:

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

Ya que al ser una lista de tuplas, porque se asigna el contenido de cada tupla a la variable de producto y cantidad. Es decir, no deberia haber un paso previo de acceso a cada tupla y ahi si los dos elementos que tiene asignarlos a esa variable? Algo como esto:

ventas = [("coca", 2), ("alfajor", 5), ("coca", 3)]
total_por_producto = {}

for venta in ventas:
for producto, cantidad in venta:
if producto not in total_por_producto:
total_por_producto[producto] = 0
total_por_producto[producto] += cantidad

## Tuplas

Las tuplas sirven como constantes, por eso en elementos que deben ser fijos se utilizan
Sirven para los JSON a diferencia de las listas, ya que las claves deben ser inmutables

## Sets

El set se utiliza para elementos que no deban repetirse y tampoco seguir un orden
La teoria de conjuntos a los sets es con los operadores correspondientes utilizados para cada set. Es decir, lleva la teoria de diferencia, interseccion y union a operadores para comparar ambos sets

## Comprensiones

Cuando se quiere comprimir una lista o diccionario se utiliza los siguientes parametros mentales: Primero lo que quiero guardar, luego se hace el bucle y se le agrega, si la hay, una condicion.

## Dudas que me quedaron
