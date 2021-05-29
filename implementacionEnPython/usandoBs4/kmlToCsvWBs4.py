# Datos sobre cruces ferroviarios
# Tipos de cruce
tipoCruce = {
    "Paso peatonal":{"railway":"crossing"},
    "Paso a nivel":{"railway":"level_crossing"},
    "Paso sobre nivel":{"bridge":"structure", "bridge:name":"name"},
    "Viaducto":{"tunnel":"yes", "tunnel:name":"name"},
    "Paso bajo nivel":{"tunnel":"yes", "tunnel:name":"name"}
}

from bs4 import BeautifulSoup
from datetime import date

# ----> Kml in
with open("data/cruces.kml", "r") as kFile:
    soup = BeautifulSoup(kFile.read(), "xml")
    kFile.close()

# cooking kml ---->
toDay = f'{date.today()}'
nodeId = 1

# folder seria como categoria 1
folders = soup.find_all("Folder")
count = 0
allData = list()
for f in [folders[0]]:
    data = dict()
    folderName = f.find("name").text.strip()
    placeList = f.find_all("Placemark")
    for p in placeList:
        placeName = p.find("name").text.strip()
        placeDescription = p.find("description").text.strip()
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
        haveDescription = False
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
                if not haveDescription:
                    haveDescription = True
                    description = f'{k} : {exD[k]}'
                else:
                    description = ' '.join([description, f'{k} : {exD[k]}]')
        if haveDescription:
            tag1 = f'<tag k="description" v="{description}"/>'
            extendedData.append(tag1)
        # Finalmente agergo el bloque de datos a una lista y preparado para generar el archivo OSM
        allData.append({"placeName":placeName, "placeDescription":placeDescription, "node":node ,"extendedData":extendedData})

# ----> OSM out
with open("data/migration.txt", "w") as osmFile:
    osmFile.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<osmChange version="0.6" generator="CGImap 0.8.1 (9148 thorn-01.openstreetmap.org)" copyright="OpenStreetMap and contributors" attribution="http://www.openstreetmap.org/copyright" license="http://opendatacommons.org/licenses/odbl/1-0/">\n')
    for d in allData:
        osmFile.write(f'\t<create>\n\t\t{d["node"]}')
        for t in d["extendedData"]:
            osmFile.write(f'\t\t{t}\n')
        osmFile.write(f'\t\t</node>\n\t</create>\n')
    osmFile.write(f'</osm>')
