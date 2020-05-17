import sqlite3 as sql

# CONFIG DBS DIRECTORY AND NAME

dbDirectory = 'dbs/'
dbName = 'data'
db = f'{dbDirectory}{dbName}.sqlite'
conn = sql.connect(db)
cur = conn.cursor()

# Get Main columns

mc = cur.execute("PRAGMA TABLE_INFO(kmlData)")
mc = mc.fetchall()

if len(mc):
    columns = list()
    for d in mc:
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
tablesIdsDict = {"line_id":"Linea", "ramal_id":"Ramal", "servicio_id":"Servicio", "actualidad_id":"Actualidad", "obra_id":"TipoObra"}
#reverseTablesIdsDict = funciones.reverseDict(tablesIdsDict)

'''
SELECT * FROM kmlData as a
JOIN Linea as b JOIN Ramal as c JOIN Servicio as d JOIN Actualidad as e JOIN TipoObra as f
ON a.linea_id = b.id and a.ramal_id = c.id and a.servicio_id = d.id and a.actualidad_id = e.id and a.obra_id = f.id
'''
allData = list()
data = dict()
queryElementsAcumulator = list()
queryFinal = [0, 0, 0, 0, 0, 0]
queryFinal[0] = 'SELECT'

for c in columns:
    if not c[1] in tablesIdsDict:
        # falta crear el node, que antes no lo habia guardado en la base de datos
        queryElementsAcumulator.append(f'kmlData.{c[1]}')
    else:
        queryElementsAcumulator.append(f'{tablesIdsDict[c[1]]}.name')

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
result = cur.fetchone()

print(f'Resultado de la queryElementsAcumulator \n{result}')

# <----- HASTA AQUI ACTUALIZADO ----->

data = dict()
folderName = f.find("name").text.strip() # <----  REEMPLAZAR :: foreing key folder_id FROM Folder
placeList = f.find_all("Placemark")
for p in placeList:
    placeName = p.find("name").text.strip() # <----  REEMPLAZAR :: CAMPO placeName FROM kmlData
    placeDescription = p.find("description").text.strip() # <----  REEMPLAZAR :: CAMPO placeDescription FROM kmlData
    extendedData = p.find("ExtendedData").find_all("Data")
    if len(extendedData):
        exD = dict()
        for d in extendedData:
            dataName = d["name"]
            dataValue = d.value.text.strip()
            exD.update({dataName:dataValue})
    lon, lat, z = p.find("Point").find("coordinates").text.strip().split(",")
    #print(f'Folder Name : {folderName} \nPlace Name : {placeName} \nlat : {lat} , lon : {lon}')
    node = f'<node id="{nodeId}" lat="{lat}" lon="{lon}" version="1" timestamp="{toDay}" changeset="0">'
    nodeId += 1
    # Lista de tags en <ExtendedData>
    extendedData = list()
    # Getting info
    for k in exD.keys():
        if k == "Actualidad":
            # Voy a setear un valor por default de exD[k] por que hay algunos errores de tipeo que generar error de
            # claves cuando buscan el dato en el diccionario "tipo de cruce"
            if not (exD[k] in list(tipoCruce.keys())):
                exD.update({"Actualidad":"Paso a nivel"})
                # Agrego este tag para hacer seguimientos de posibles errores o inconsistencia en los datos
                extendedData.append(f'<tag k="valorPorDefault" v="yes"/>')
            if len(list(tipoCruce[exD[k]].keys())) > 1:
                k0 = list(tipoCruce[exD[k]].keys())[0]
                k1 = list(tipoCruce[exD[k]].keys())[1]
                tpCruce, tpCruceVal = k0, tipoCruce[exD[k]][k0]
                cruceName, cruceNameVal = k1, exD["Nom. Alt."]
                tag1 = f'<tag k="{tpCruce}" v="{tpCruceVal}"/'
                tag2 = f'<tag k="{cruceName}" v="{cruceNameVal}"/>'
                extendedData.extend([tag1, tag2])
            else:
                k0 = list(tipoCruce[exD[k]].keys())[0]
                tpCruce, tpCruceVal = k0, tipoCruce[exD[k]][k0]
                tag1 = f'<tag k="{tpCruce}" v="{tpCruceVal}"/>'
                extendedData.append(tag1)
        else:
            tag1 = f'<tag k="{k}" v="{exD[k]}"/>'
            extendedData.append(tag1)
    # Finalmente agergo el bloque de datos a una lista y preparado para generar el archivo OSM
    allData.append({"placeName":placeName, "placeDescription":placeDescription, "node":node ,"extendedData":extendedData})



# ----> OSM out
with open("data/migrationFromDb.txt", "w") as osmFile:
    osmFile.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<osmChange version="0.6" generator="CGImap 0.8.1 (9148 thorn-01.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">\n')
    for d in allData:
        osmFile.write(f'\t<create>\n\t\t{d["node"]}')
        for t in d["extendedData"]:
            osmFile.write(f'\t\t{t}\n')
        osmFile.write(f'\t\t</node>\n\t</create>\n')
    osmFile.write(f'</osm>')



