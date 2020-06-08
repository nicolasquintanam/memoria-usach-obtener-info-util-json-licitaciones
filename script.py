# -*- coding: utf-8 -*-
# -- Librerías necesarias --
import pandas as pd
import json

# Función que permite validar el formato de un json.
# Entrada: string que se validará.
# Salida: booleano indicando si es válido o no.
def esValidoJson(jsonString):
    try:
        json.loads(jsonString)
        return True
    except ValueError as error:
        return False

# Función que permite reemplazar carácteres hasta ahora necesarios para la obtención de un json válido.
# Entrada: string del json que será reemplazado.
# Salida: el mismo string que se da por entrada, pero reemplazando los caracteres necesarios.
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

# Función que permite obtener el json a partir de la ruta donde se encuentra el CSV y el json que se quiere obtener.
# Entrada: un string que indica la ruta donde se encuentra el csv y el número de json que se quiere obtener.
# Salida: un string con el json obtenido.
def obtenerJson(rutaHistorico, numero):
    numero = int(numero)
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
    jsonPelado = reemplazoAux(jsonPelado)
    return jsonPelado



#ruta = input("Por favor ingresar la ruta donde se encuentra el CSV\nRuta: ")
ruta = "C:/personal/historicoJsonLicitaciones.csv"
lineaQueSeQuiereObtener = input("Ingresar json que se quiere obtener.\nNúmero: ")

jsonObtenido = obtenerJson(ruta, lineaQueSeQuiereObtener)
print(jsonObtenido)

print("El json mostrado tiene un formato válido" if esValidoJson(jsonObtenido) else "El json mostrado no tiene un formato válido")
