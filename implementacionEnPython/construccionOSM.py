import sqlite3 as sql

# CONFIG DBS DIRECTORY AND NAME

dbDirectory = 'dbs/'
dbName = 'data'
db = f'{dbDirectory}{dbName}.sqlite'
conn = sql.connect(db)
cur = conn.cursor()

# Get Main columns

kmlDataTableInfo = cur.execute("PRAGMA TABLE_INFO(kmlData)")
kmlDataTableInfo = kmlDataTableInfo.fetchall()

columns = list()
if len(kmlDataTableInfo):
    for d in kmlDataTableInfo:
        columns.append((d[0], d[1]))
else:
    print(f'No se econtraron columnas disponibles en la base de datos')
    print(f'Directorio BD {dbDirectory} :: Nombre de la base {dbName}')

tipoCruce = {
    "Paso peatonal": {"railway": "crossing"},
    "Paso a nivel": {"railway": "level_crossing"},
    "Paso sobre nivel": {"bridge": "structure", "bridge:name": "name"},
    "Viaducto": {"tunnel": "yes", "tunnel:name": "name"},
    "Paso bajo nivel": {"tunnel": "yes", "tunnel:name": "name"}
}

# Diccionario de tablas y datos para mapear
# Esto viene de aca <ExtendedData><Data name="Línea"> <value>Belgrano Norte</value></ExtendedData>
# Dato en el tag Data me va a decir en tabla inserto el valor

tables = ["Linea", "Ramal", "Servicio", "Actualidad", "TipoObra"]
tablesIdsDict = {"line_id": "Linea", "ramal_id": "Ramal", "actualidad_id": "Actualidad"}
kmlDataColumnsSelection = ['placeName', 'lat', 'lon', ]

allData = list()
data = dict()
queryElementsAcumulator = list()
queryFinal = [0, 0, 0, 0, 0, 0]
queryFinal[0] = 'SELECT'

for c in columns:
    if c[1] in tablesIdsDict:
        queryElementsAcumulator.append(f'{tablesIdsDict[c[1]]}.name AS {tablesIdsDict[c[1]]}')
    if c[1] in kmlDataColumnsSelection:
        queryElementsAcumulator.append(f'kmlData.{c[1]}')

queryVar = ' , '.join([x for x in queryElementsAcumulator])
print(f'queryElementsAcumulator, primera parte \n{queryVar}')
queryElementsAcumulator.clear()

queryFinal[1] = f'{queryVar}'
queryFinal[2] = 'FROM kmlData'

for c in columns:
    if c[1] in tablesIdsDict:
        queryElementsAcumulator.append(f'JOIN {tablesIdsDict[c[1]]}')

# Entre los JOINS de la query Sql no van comas, la concatenacion en el join (python), es por espacio en blanco
queryVar = ' '.join([x for x in queryElementsAcumulator])
print(f'queryElementsAcumulator, Segunda parte \n{queryVar}')
queryElementsAcumulator.clear()

queryFinal[3] = f'{queryVar}'
queryFinal[4] = 'ON'

for c in columns:
    if c[1] in tablesIdsDict:
        queryElementsAcumulator.append(f'kmlData.{c[1]} = {tablesIdsDict[c[1]]}.id')

# Se agrega el keyWord AND como separador en el join
queryVar = ' AND '.join([x for x in queryElementsAcumulator])
print(f'queryElementsAcumulator, Segunda parte \n{queryVar}')
queryElementsAcumulator.clear()

queryFinal[5] = f'{queryVar}'
queryFinal = ' '.join([x for x in queryFinal]).strip()

cur.execute(queryFinal)
results = cur.fetchall()
toDay = 'toBeDefine'
data = dict()
nodeId = 1
for row in results:
    placeName = row[0]
    lon, lat = row[1], row[2]
    node = f'<node id="{nodeId}" lat="{lat}" lon="{lon}" version="1" timestamp="{toDay}" changeset="0">'
    nodeId += 1
    # Getting info
    # Voy a setear un valor por default de exD[k] por que hay algunos errores de tipeo que generar error de
    # claves cuando buscan el dato en el diccionario "tipo de cruce"
    extendedData = list()
    tipoCruceActual = row[5]
    if not (tipoCruceActual in list(tipoCruce.keys())):
        tipoCruceActual = "Paso a nivel"
        # Agrego este tag para hacer seguimientos de posibles errores o inconsistencia en los datos
        extendedData.append(f'<tag k="valorPorDefault" v="yes"/>')
    if len(list(tipoCruce[tipoCruceActual].keys())) > 1:
        k0 = list(tipoCruce[tipoCruceActual].keys())[0]
        k1 = list(tipoCruce[tipoCruceActual].keys())[1]
        tpCruce, tpCruceVal = k0, tipoCruce[tipoCruceActual][k0]
        cruceName, cruceNameVal = k1, f'{placeName}-{row[3]}-{row[4]}'
        tag1 = f'<tag k="{tpCruce}" v="{tpCruceVal}"/'
        tag2 = f'<tag k="{cruceName}" v="{cruceNameVal}"/>'
        extendedData.extend([tag1, tag2])
    else:
        k0 = list(tipoCruce[tipoCruceActual].keys())[0]
        tpCruce, tpCruceVal = k0, tipoCruce[tipoCruceActual][k0]
        tag1 = f'<tag k="{tpCruce}" v="{tpCruceVal}"/>'
        extendedData.append(tag1)
    # Finalmente agergo el bloque de datos a una lista y preparado para generar el archivo OSM
    allData.append({"placeName":placeName, "node":node ,"extendedData":extendedData})

#<----- HASTA AQUI ACTUALIZADO ----->

# ----> OSM out
with open("data/migrationFromDb.txt", "w") as osmFile:
    osmFile.write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<osmChange version="0.6" generator="CGImap 0.8.1 (9148 thorn-01.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">\n')
    for d in allData:
        osmFile.write(f'\t<create>\n\t\t{d["node"]}\n')
        for t in d["extendedData"]:
            osmFile.write(f'\t\t{t}\n')
        osmFile.write(f'\t\t</node>\n\t</create>\n')
    osmFile.write(f'</osm>')



