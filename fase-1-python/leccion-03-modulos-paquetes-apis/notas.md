# Mis notas: Lección 03

(Escribí acá, con tus palabras, qué entendiste de cada tema. Sin copiar la teoría.)

## Módulos e imports

Los modulos son todos los archivos terminados en .py, estos modulos se pueden importar en otro modulos y usar su contenido. Hay distintas formas de importarlos, pueden ser mas especificos o mas generales o con mas o menos cosas. Es importante que el import se haga conscientemente de las cosas que necesitas en nuestro modulo.

## `if __name__ == "__main__":` (ahora sí, explicado por vos)

Es una condicion que le dice al modulo que ejecutar en un entorno donde es el propiamente el ejecutado directamente y que NO ejecutar en un entorno donde el modulo en ejecucion es otro importando lo que necesita del modulo. El nombre del modulo cambia dependiendo que modulo se ejecute, si es el modulo ejecutado es main, sino toma el nombre del archivo

## Paquetes y `__init__.py`

Los paquetes son cantidades de modulos hecho por terceros, un indicio de un paquete y que viene normalmente vacio es el archivo init.py . Estos paquetes son instalados por gestores de paquetes como uv, se encargan de instalar sus diferentes versiones dentro de un entorno aislado para no afectar a tu maquina local, sino que todo en ese ambiente sea con las versiones que deben.

## Entornos virtuales: qué problema resuelven

El problema que solucionan los entornos virtuales son el afectar las distintas versiones de los paquetes o sistemas, envolviendolos en un entorno independiente al local. Esto hace que cualquiera que tenga el entorno configurado como dicen los diferentes archivos como puede ser un uv.lock o un requirements.txt hace que la ejecucion sea la misma en distintos dispositivos.

## uv: pyproject.toml, uv.lock, .venv

el pyproject.toml son los requisitos para que funcione el proyecto, el uv.lock son exactamente las versiones que se setearon en el proyecto y el .venv es el entorno completo que contiene todas las dependencias instaladas.

## requests: GET, params, timeout, raise_for_status

Los requests son peticiones de respuesta de un servidor, se utiliza el metodo GET para recibir la respuesta del servidor. Esa peticion eleva tambien diferentes parametros que queremos que tenga en cuenta para su respuesta, ademas de que lleva el mas importante que es el timeout, cierra la conexion despues del tiempo que se le especifica para que no quede colgado a recibir algo muerto, o que simplemente no gaste recursos del sistema en esa conexion que no llefa. La respuesta llega en formato JSON y tambien tiene excepciones como vimos en la leccion 02. El raise_for_status lanza una excepcion de HTTP Code que nos dice dependiendo del numero el resultado de la respuesta

## Las excepciones de requests

Las excepciones de requests son algunas de las que dije en mi anterior respuesta, tenemos excepciones para el tiempo de conexion, si directamente no tiene conexion, si no entrega un json que se puede decodificar.

## Por qué un 200 no garantiza que los datos sean los que pediste

Es el valor de como respondio el servidor, no si entendio lo que quisimos o esperamos como respuesta

## Dudas que me quedaron
