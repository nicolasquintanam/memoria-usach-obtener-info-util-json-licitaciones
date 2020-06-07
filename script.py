# -*- coding: utf-8 -*-
import pandas as pd



size = 1
df = pd.read_csv("c:/personal/historicoJsonLicitaciones.csv", chunksize=size)

for linea in df:
    dataframe1 = linea
    break

# En la variable dataframe1 queda el primer dataframe 
dfString = dataframe1.to_string()
# Ahora en dfString queda el primer dataframe como string
listadoLineasPrimerDF = dfString.split('\n')
# Ahora se tiene un listado de dos líneas en listadoLineasPrimerDF
# listadoLineasPrimerDF[0] = id;detalleJson;link
# listadoLineasPrimerDF[1] = idLicitacion1;detalleJson1;linkLicitacion1
listadoColumnasPrimerDF = listadoLineasPrimerDF[1].strip().split(';')
# Ahora se debería tener en listadoColumnasPrimerDF
# listadoColumnasPrimerDF[0] = ID de la licitación 1
# listadoColumnasPrimerDF[1] = Detalle Json Licitación 1
# listadoColumnasPrimerDF[2] = Link de la licitación
#print("ID DE LICITACIÓN 1")
#print(listadoColumnasPrimerDF[0].strip())
#print("JSON DE LICITACIÓN 1")
#print(listadoColumnasPrimerDF[1].strip())
#print("LINK DE LICITACIÓN 1")
#print(listadoColumnasPrimerDF[2].strip())

#Nos concentraremos en print(listadoColumnasPrimerDF[1].strip()) que tiene el json de la licitación
# Como el detalle del json está entre comillas, se sacará el primer y último caracter
jsonPelado = listadoColumnasPrimerDF[1].strip()[1:][:-1].strip()
# También se reemplazará las dobledoble comilla por doble comilla    Ejemplo ""Nombre"": ""Nicolas Quintana"" ---> "Nombre": "Nicolas Quintana"
jsonPelado = jsonPelado.replace("\"\"","\"")
# Parte del json está de la siguiente manera:
# "Obras": "0"  "Estado": "Adjudicada"  "Etapas": 1
# --> lo cual debería estar así
# "Obras": "0", "Estado": "Adjudicada", "Etapas": 1
# Por lo tanto, se reemplazará '"  "' por '", "'
jsonPelado = jsonPelado.replace("\"  \"", "\", \"")
# Ahora está el inconveniente, que aveces hay en vez de que haya:
# "Obras": "0"  "Estado": "Adjudicada"  "Etapas": 1
# Hay:
# "Obras": 0  "Estado": "Adjudicada"  "Etapas": 1
# Por lo tanto, ya no sirve el reemplazar "  " por ", "
# Se hará un método para reemplazar un número (del 0 al 9) que después tenga dos espacios y una comilla doble, por el número + "," + " " + comilla doble
print(jsonPelado)
