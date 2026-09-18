# Mis notas: Lección 02

(Escribí acá, con tus palabras, qué entendiste de cada tema. Sin copiar la teoría.)

## Excepciones específicas (except puntual vs genérico)

Las excepciones deben realizarse con el objetivo de atrapar algo concreto, esas excepciones son lanzadas por Python y debemos guardarlas para resolver el error especifico el cual esperamos. Si se hace un except generico (Se puede hacer como comodin a modo de error inesperado pero no es recomendado) agarra errores que nosotros quiza no contemplamos y tampoco con ese except nos aseguramos de saber especificamente que es lo que fallo

## try / except / else

El try debe contener unicamente la linea o lineas que esperamos un fallo o no del sistema, pueden ocurrir varios errores distintos en la linea, algunos Python ya los maneja con excepciones del mismo lenguaje, estas excepciones deben ser especificas como dije antes, los except se leen de arriba abajo, deben colocarse los especificos arriba, ya que el error cae en la primer coincidencia. Y el else se utiliza para manejar las acciones cuando el sistema realiza la operacion esperada, es decir, cuando sale bien.
Lei esto de la teoria y me parecio importante que no dije sin leer\*: Para capturar el objeto del error se utiliza as e para ver el traceback. Imagino que viendo logs esto nos sirve para identificar mejor y mas claro el error

## finally

El finally le da un cierre obligatorio a todo, salga como salga. Es para limpieza, por ejemplo: Falla una conexion a un endpoint de la API donde intenta recibir o enviar datos, esa conexion no se cerraria nunca y generaria trafico. Con finally le damos un cierre obligatorio a esa conexion

## raise y raise ... from ...

El raise se utiliza para lanzar una excepcion para que el usuario sea el encargado de manejar el error. Si el usuario esta mandando un email en un campo donde va el numero de telefono, podemos lanzar la excepcion con el raise y que el se encargue de que el error deje de existir. El raise ... from ... se utiliza para relacionar la expecion con la funcion que fallo

## Excepciones propias

Crear excepciones propias con clases para capturar datos y errores especificos, como diseño del sistema o reglas de negocio

## Archivos con with

El with ejecuta la misma operacion/funcion o comportamiento que el finally pero especifico de archivos. Obliga a que si se abre un archivo este sea cerrado para que no ocupe recursos del sistema. Se utiliza as f para capturar ese file.

## JSON (dump/load vs dumps/loads)

Los archivos JSON se pueden leer o escribir, como si fuera un GET o un POST donde vos podes convertirlos al formato que quiera, dump/load se utiliza para pasar de strings a un archivo JSON, se utilizaria como en el metodo POST, y dumps/loads se utiliza para convertir el archivo JSON a str. Dump es para enviar, load para leer. Ya que el lenguaje universal es JSON y debemos enviar los datos en ese formato, los recibimos en ese formato y podemos formatearlo para utilizarlo nosotros por ejemplo en un dict de python.

## Dudas que me quedaron
