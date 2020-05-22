### Detalles sobre la base de datos

Decidi usar una base de datos como punto de transcicion entre la extraccion de los datos del Kml y la creacion del Archivo OSM change. Las razones son las siguientes.

1) Separa el problema de migracion de datos en varias partes.
2) Conservar una copia de todos los datos extraidos del KML en crudo.
3) Facilitar el analisis de los datos extraidos.
4) Permitir a futuro la migracion de datos a otras plataformas sin necesidad de extraer nuevamente informacion del KML.
5) Agilizar la escritura del OSM change y poner a disposicion todos los datos extraidos pudiendo tomar solo los de interes.

Implemente la API de sqlite3 ya que para la cantidad de datos y la modalidad de uso es la herramienta que tiene mejor performance. Implementacion rapida, interfaz simple, navegador grafico, rapides y documentacion.

El esquema de la base se puede encontrar en esta misma carpeta.

El encoding de los datos es un tema pendiente.
