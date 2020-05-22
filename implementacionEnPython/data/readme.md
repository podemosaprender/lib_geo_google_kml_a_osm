#### Geo Data 
- KML, OSM, GeoJson, Shapes, todos estos archivos son de tipo etiquetados y en el caso de GeoJson un objeto. Aunque varian en su forma todos tienen el mismo proposito o casi el mismo. Fueron creados para trabajar con datos que estan geograficamente referenciados, ya sea con puntos como por ejemplo el par (latitud, longitud), con poligonos contruidos a partir de las rectas surgidas de unir los puntos anteriores, lineas divisorias entre dos puntos, etc. En general estas caracteristicas estan acompañadas por sus meta datos, nombre, descripcion y angunos detalles mas especificos de cada punto, poligono o linea. Si es una linea pude ser una ruta y en su metadata encontraras el nombre, numero, si es nacional o provincial y quiza tambien el estado general del asfalto.


#### Datos en formato xlmns o Espacio de nombre xml, en español
>Un espacio de nombres XML es una recomendación W3C para proporcionar elementos y atributos con nombre único en un archivo XML. Un archivo XML puede contener nombres de elementos o atributos procedentes de más de un vocabulario XML. Si a cada uno de estos vocabularios se le da un espacio de nombres, un ámbito semántico propio, referenciado a una URI donde se listen los términos que incluye, se resuelve la ambigüedad existente entre elementos o atributos que se llamen igual, la homonimia. Los nombres de elementos dentro de cada espacio de nombres deben ser únicos.

#### Archivos KML
>KML (del acrónimo en inglés Keyhole Markup Language) es un lenguaje de marcado basado en XML para representar datos geográficos en tres dimensiones. Fue desarrollado para ser manejado con Keyhole LT, precursor de Google Earth (Google adquirió Keyhole LT en octubre de 2004 tras lanzar su versión LT 2). Su gramática contiene muchas similitudes con la de GML. 

#### OSM change files o archivos de Cambio
>osmChange is the file format used by osmosis (and osmconvert) to describe differences between two dumps of OSM data. However, it can also be used as the basis for anything that needs to represent changes. For example, bulk uploads/deletes/changes are also changesets and they can also be described using this format. We also offer Planet.osm/diffs downloads in this format.
> En pocas palabras mas arriba dice que este tipo de archivos sirven para describir diferencias entre dos grupos de datos geograficos de OpenStreetMaps. En nuestro caso, si queremos subir algun agregado al mapa de OpenStreetMap, lo tenemos que poponer usando este tipo archivo OSM change. Ya que OpenStreetMaps es una gran base de datos deberemos proponer nunestro trabajo para que sea incluido en la base.

### Los datos fueron extraidos de Google Maps usando la opcion de exportar a KML a partir de un mapa generado por un usuario.

> ESTE ARCHIVO FUE PARCIALMENTE MODIFICADO !!!

1) Los textos anidados en la eltiqueta <data name=""><values></values></data> que empiezan con numero, fueron cambiados a prev..n°
2) Los datos que fueron incluidos en el mapa no presentan un patron de caracteristicas o atributos. Esto quieres decir que no todos tiene los mismos atributos, por lo tanto, para evitar errores y simplificar el parseo del archivo, normalice los atributos dandole la misma forma a todos. Para el caso donde los atributos necesarios no estaban presentes, se los agrego y se seteo su valor a NONE.

