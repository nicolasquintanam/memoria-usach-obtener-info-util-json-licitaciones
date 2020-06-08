# -*- coding: utf-8 -*-
import pandas as pd

def reemplazoAux(entrada):
    entrada = entrada.replace("1  \"","1,  \"")
    entrada = entrada.replace("2  \"","2,  \"")
    entrada = entrada.replace("3  \"","3,  \"")
    entrada = entrada.replace("4  \"","4,  \"")
    entrada = entrada.replace("5  \"","5,  \"")
    entrada = entrada.replace("6  \"","6,  \"")
    entrada = entrada.replace("7  \"","7,  \"")
    entrada = entrada.replace("8  \"","8,  \"")
    entrada = entrada.replace("9  \"","9,  \"")
    entrada = entrada.replace("0  \"","0,  \"")
    entrada = entrada.replace("1   \"","1,  \"")
    entrada = entrada.replace("2   \"","2,  \"")
    entrada = entrada.replace("3   \"","3,  \"")
    entrada = entrada.replace("4   \"","4,  \"")
    entrada = entrada.replace("5   \"","5,  \"")
    entrada = entrada.replace("6   \"","6,  \"")
    entrada = entrada.replace("7   \"","7,  \"")
    entrada = entrada.replace("8   \"","8,  \"")
    entrada = entrada.replace("9   \"","9,  \"")
    entrada = entrada.replace("0   \"","0,  \"")
    entrada = entrada.replace("null  \"","null,  \"")
    entrada = entrada.replace("}  \"","},  \"")
    entrada = entrada.replace("]  \"","],  \"")
    entrada = entrada.replace("}  {","},  {")
    entrada = entrada.replace("\"       \"","\",       \"")
    return entrada

def obtenerJson(rutaHistorico, numero):
    size = 1
    df = pd.read_csv(rutaHistorico, chunksize=size)
    i = 0
    for linea in df:
        dataframe1 = linea
        if(i == numero):
            break
        i = i + 1
    # En la variable dataframe1 queda el primer dataframe
    dfString = dataframe1.to_string()
    #print("paso 1:\n")
    #print(dfString)
    # Ahora en dfString queda el primer dataframe como string

    listadoLineasPrimerDF = dfString.split('\n')
    #print("paso 2:\n")
    #print(listadoLineasPrimerDF)

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
    jsonPelado = reemplazoAux(jsonPelado)
    return jsonPelado

print(obtenerJson("c:/personal/historicoJsonLicitaciones.csv", 5))
