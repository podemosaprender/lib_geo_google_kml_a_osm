## Aqui podras encontrar toda la implementacion en Pyhton

### El esquema de la base de datos, las queries y la construcciones de los archivos finales estan en fase Beta. Ninguno de los elementos anteriores es definitivo, todo es alterable.

El objetivo del proyecto es extraer los datos geograficos y descripcion de un archivo KML y guardarlos en una base de datos para posterior mente migrar dicha info a otro formato. En este caso el formato final buscado es uno compatible con Open Street Maps para generar los archivos osc que son destinados a agregar iformacion en las base de datos del web site. 

El proyecto se encuentra en la fase de finalizacion del diseño e implementacion para testeo

La implementacion en BeautifulSoup no se actualizara mas. En cambio, el proyecto tomo otro camino, se desarrollo sobre xml.etreeElementTree y se decidio usar uns base de datos sqlite.

Secuencia de ejecucion
- crud.py para crear la base de datos desde cero
- extraccion para sacar e insertar los datos en la base de datos
- construccionOSM para tomar los datos necesarios de la base y escribir el archivo final

### extraccionDeDatos.py
En este archivo econtramos lo siguiente:
- Se importa lee y parsea el KML
- Se crea y conecta a la base de datos
- Se insertan los registros

Los registros se insertan en la base de datos uno por uno inmediatamente despues de extraer el dato

### crud.py
Este archivo contiene el esquema para crear la base de datos

### funciones.py
En este archivo se encuentran dos funciones.

#### 1 Funcion de comprobacion y transformacion de texto : transform(word=None, upFLetter=None, isCamel=None)
- Toma tres parametros string, upFLetter, isCamel.
- EL primero input word = string, upFLetter = Bool , isCamel = Bool
- Devuelve un string quitando acentos y espacios
- Si upFLetter = True devuelve un string con la primera letra en mayuscula. NO ES CAPITALIZE
- Si isCamel = True conbierte el string a tipo de tipeo camello

#### 2 Funcion para invertir diccionario reverseDict(d = None, retRep = False):
- Toma dos parametros d y retRep
- Inputs d = dict , retRep = Bool
- Devuelve un diccionario
- Devuelve el diccionario de entrada pero invertido, las valores como clave y las claves (keys), como valor
- Si retRep = True la funcion devuelve una tupla donde el valor [1] es una lista con los pares clave:valor donde el valor se repite.



