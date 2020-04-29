
Baso de datos creada con sqlite3

Esquema:

    CREATE TABLE kmlData (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        folder_id INTEGER,
        placeName TEXT,
        placeDescription TEXT,
        line_id INTEGER,
        ramal_id INTEGER,
        servicio_id INTEGER,
        actualidad_id INTEGER,
        nomAlt TEXT,
        obs TEXT,
        prev2019 TEXT,
        prev2023 TEXT,
        obra_id INTEGER,
        estado TEXT,
        progresiva TEXT,
        anoEstimadoDeObra TEXT,
        ultimaActualizacion TEXT
    );
    CREATE TABLE Folder (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE);
    CREATE TABLE Linea (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE);
    CREATE TABLE Ramal (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE);
    CREATE TABLE Servicio (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE);
    CREATE TABLE Actualidad (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE);
    CREATE TABLE TipoObra (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE); 
    ''')
