## Aqui podras encontrar toda la implementacion en Pyhton

### El esquema de la base de datos, las queries y la construcciones de los archivos finales estan en fase Beta. Ninguno de los elementos anteriores es definitivo, todo es alterable.

El objetivo del proyecto es extraer los datos geograficos y descripcion de un archivo KML y guardarlos en una base de datos para posterior mente migrar dicha info a otro formato. En este caso el formato final buscado es uno compatible con Open Street Maps para generar los archivos osc que son destinados a agregar iformacion en las base de datos del web site. 

El proyecto se encuentra en la fase de finalizacion del diseño e implementacion para testeo

La implementacion en BeautifulSoup no se actualizara mas. En cambio, el proyecto tomo otro camino, se desarrollo sobre xml.etreeElementTree y se decidio usar uns base de datos sqlite.

Secuencia de ejecucion
- crud.py para crear la base de datos desde cero
- extraccion para sacar e insertar los datos en la base de datos
- construccionOSM para tomar los datos necesarios de la base y escribir el archivo final

