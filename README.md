# geo_google_kml_a_osm
## Migracion de datos de Google Maps a OpenStreet Maps

El objetivo de este proyecto es extraer datos de archivos tipo KML y migrarlos a otro tipo de archivos con extension osc. Estos utlimos representan informacion que puede ser leida en la plataforma OpenStreet Maps y es apta para la integracion en los mapas publicos del mimso web site. 

GM nos permite exportar y descargar los datos de los mapas en un archivo tipo KML. Este archivo contiene toda la imformacion sobre puntos, lineas y  poligonos  y los metadatos asociados a dichos elementos, por ejemplo, Nombre del punto, tipo, icono, descripcion, etc.

Ejemplo de algunos tags en el KML:

    <Document>
    <name>Este es el nombre del mapa</name>
    <description>Esto es una descripcion del mapa</description>
    <Folder>
      <name>Capa sin nombre</name>
      <Placemark>
        <name>Esto es un punto</name>
        <description>Esta es la descripcion del punto</description>
        <styleUrl>#icon-1899-0288D1</styleUrl>
        <Point>
          <coordinates>
            101.6758908,3.1504205,0
          </coordinates>
        </Point>
      </Placemark>
    </Folder>
    </document>
    
 >Este formato NO es soportado por OpenStreet Maps. Por ello nos propusimos migrar la informacion contenida en el KML a un archivo compatible.
 
 El archivo resultante de la trasnformacion (KML -> OSM ), debe tener una pinta parecida a lo siguiente:
 
    <osmChange version="0.6" generator="iD">
    <create>
        <node id="-99" lon="-59.44866421556385" lat="-34.450778315051785" version="0"/>
        <way id="-10" version="0">
            <nd ref="-99"/>
            <tag k="building" v="house"/>
            <tag k="name" v="Este es el nombre"/>
            <tag k="building:levels" v="2"/>
            <tag k="building:material" v="brick"/>
            <tag k="description" v="Esta es una descripcion del feature"/>
        </way>
    </create>
    <modify/>
    <delete if-unused="true"/>
    </osmChange>
 
>  This is the changeset to modify that single node.
 
