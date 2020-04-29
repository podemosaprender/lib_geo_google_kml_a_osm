# Aqui podras encontrar toda la implementacion en Pyhton

## Tanto el esquema de la base de datos como las queries apenas funcionan y aun no me he preocupado por la eficienda de la BD.

El objetivo del proyecto es extraer los datos geograficos y descripcion de un archivo KML y guardarlos en una base de datos para posterior mente migrar dicha info a otro formato. En este caso el formato final buscado es uno compatible con Open Street Maps para generar los archivos osc que son destinados a agregar iformacion en las base de datos del web site. 

El desarrollo del proyecto esta apenas en la primera fase de experimentacion y testeos. Los scripts que podes encontra aca estan funcinando con los datos que tambien estan publicados en este repo. 

En primer lugar se puede encontrar una implementacion usando BeautifulSoup, en ese files se ejecutan todas las intrucciones para realizar la migracion pero no se creo la base de datos.

En segundo lugar y ya un poco mas desarrollado podes encontrar varios archivos donde comenze con el uso de otroa libreria para parsear el KML, xml.etreeElementTree. Tambien se implemento la base de datos, por ahora solo en la extraccion de la info.

