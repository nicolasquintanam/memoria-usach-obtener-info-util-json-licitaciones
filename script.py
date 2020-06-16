# -*- coding: utf-8 -*-
# -- Librerías necesarias --
import pandas as pd
import json
import xlsxwriter

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
    print("JSON DE LICITACIÓN 1")
    print(str(len(listadoColumnasPrimerDF[1].strip())))
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

def ObtenerPrimerosJson(rutaHistorico, numero):
    libro = xlsxwriter.Workbook('licitaciones.xlsx')
    hoja = libro.add_worksheet()
    numero = int(numero)
    df = pd.read_csv(rutaHistorico, chunksize=1)
    i = 0
    hoja.write(0, 0, "ID")
    hoja.write(0, 1, "JSON")
    hoja.write(0, 2, "LINK")
    hoja.write(0, 3, "VALIDO JSON")
    for linea in df:
        dataframe1 = linea
        if(i == numero):
            break
        else:
            dfString = dataframe1.to_string()
            listadoLineasPrimerDF = dfString.split('\n')
            listadoColumnasPrimerDF = listadoLineasPrimerDF[1].strip().split(';')
            print(i)
            idLicitacion = listadoColumnasPrimerDF[0].strip()
            hoja.write(i+1, 0, idLicitacion)

            jsonPelado = listadoColumnasPrimerDF[1].strip()[1:][:-1].strip()
            jsonPelado = jsonPelado.replace("\"\"","\"")
            jsonPelado = jsonPelado.replace("\"  \"", "\", \"")
            jsonPelado = reemplazoAux(jsonPelado)
            try:
                if(not(esValidoJson(jsonPelado))):
                    jsonPelado = jsonPelado + listadoColumnasPrimerDF[2].strip()
                    jsonPelado = jsonPelado.replace("\"\"","\"")
                    jsonPelado = jsonPelado.replace("\"  \"", "\", \"")
                    jsonPelado = reemplazoAux(jsonPelado)
            except:
                j = 2
            hoja.write(i+1, 1, jsonPelado)
            try:
                link = listadoColumnasPrimerDF[2].strip()
                link = link.replace(" NaN", "")
                link = link.strip()
                hoja.write(i+1, 2, link)
            except:
                link = "http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=" + idLicitacion
                hoja.write(i+1, 2, link)
            hoja.write(i+1, 3, esValidoJson(jsonPelado))
        i = i + 1
    libro.close()

def ObtenerPrimerosJson2(rutaHistorico, numero):
    numero = int(numero)                            # Transformando el parámetro a número
    df = pd.read_csv(rutaHistorico, chunksize=1)    # Crear un dataframe a partir del CSV
    i = 0
    libro = xlsxwriter.Workbook('licitaciones.xlsx')   # Se crea el excel
    hoja = libro.add_worksheet()                       # Se añade una hoja el excel
    negrita = libro.add_format({'bold': True})
    centrar = libro.add_format({'align': 'center'})

    hoja.write(0, 0, "ID", centrar)
    hoja.write(0, 1, "JSON", centrar)                           # ---- Se crea la cabecera de la hoja --
    hoja.write(0, 2, "LINK", centrar)                           # --------------------------------------
    hoja.write(0, 3, "VALIDO JSON", centrar)                    #---------------------------------------
    hoja.write(0, 5, "Categoría Item", centrar)
    hoja.write(0, 6, "Descripción Item", centrar)
    hoja.write(0, 7, "Nombre Solicitud", centrar)
    hoja.write(0, 8, "Descripcion Solicitud", centrar)
    hoja.write(0, 9, "Nombre unidad compradora", centrar)
    hoja.write(0, 10, "Nombre organismo comprador", centrar)
    hoja.write(0, 11, "Monto estimado", centrar)

    for registro in df:                                # Por cada registro en el dataframe (CSV), arrojará esto:
                                                       # ------------------------------------------------------------------------
                                                       # ---------  "idLicitacion;json;linkJson  --------------------------------
                                                       # ---------  3021-124-L119;{listado: {...;https://mercado"  --------------
                                                       # ------------------------------------------------------------------------

        registroString = registro.to_string()                       # Aquí se tiene lo anteriormente mencionado pero como string
        listadoRegistroString = registroString.split('\n')          # Como están separados por un salto de línea, interesa sólo
                                                                    # el segundo elemento, que es el que tiene la información
        registroInformacion = listadoRegistroString[1].strip()  # Aquí se tiene sólo la parte "3021-124-L119;{listado: {...;https://mercado..."
        listadoInformacion = registroInformacion.split(';')     # Aquí se separa lo anterior por ; para tener un listado.
        largoListadoInfo = len(listadoInformacion)              # Aquí se tiene el largo de lo anterior, ya que puede darse el caso
                                                                # que dentro del json (texto) tenga puntoycoma, o también puede darse el caso
                                                                # que no contenga el link de acceso a información complementaria.

        idLicitacion = listadoInformacion[0].strip()            # Si o si tiene el id de la licitación, por lo tanto,
        hoja.write(i + 1, 0, idLicitacion)                      # se inserta en el excel
        jsonLicitacion = ""
        if(largoListadoInfo == 2):                              # Si tiene largo 2, quiere decir que no viene con el link
            jsonLicitacion = listadoInformacion[1].strip()
            # -----------------------------------------
            # ----- PROCESO DE LIMPIEZA DE JSON -------
            # -----------------------------------------
            jsonLicitacion = jsonLicitacion[1:][:-1].strip()
            jsonLicitacion = jsonLicitacion.replace("\"\"","\"")
            jsonLicitacion = jsonLicitacion.replace("\"  \"", "\", \"")
            jsonLicitacion = reemplazoAux(jsonLicitacion)
            # -----------------------------------------
            # ---- FIN PROCESO DE LIMPIEZA DE JSON ----
            # -----------------------------------------
            hoja.write(i + 1, 1, jsonLicitacion)                # Se inserta el json limpio en el excel
            link = "http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=" + idLicitacion
            hoja.write(i + 1, 2, link)

        if(largoListadoInfo == 3):                              # Si tiene largo 3, quiere decir que está en lo correcto
            jsonLicitacion = listadoInformacion[1].strip()
            # -----------------------------------------
            # ----- PROCESO DE LIMPIEZA DE JSON -------
            # -----------------------------------------
            jsonLicitacion = jsonLicitacion[1:][:-1].strip()
            jsonLicitacion = jsonLicitacion.replace("\"\"","\"")
            jsonLicitacion = jsonLicitacion.replace("\"  \"", "\", \"")
            jsonLicitacion = reemplazoAux(jsonLicitacion)
            # -----------------------------------------
            # ---- FIN PROCESO DE LIMPIEZA DE JSON ----
            # -----------------------------------------
            hoja.write(i + 1, 1, jsonLicitacion)                # Se inserta el json limpio en el excel
            link = listadoInformacion[2].strip()
            link = link.replace(" NaN", "")
            link = link.strip()
            hoja.write(i + 1, 2, link)

        if(largoListadoInfo == 4):                              # Si tiene largo 4, quiere decir que el texto tiene un puntoycoma
            jsonLicitacion = listadoInformacion[1] + listadoInformacion[2]
            jsonLicitacion = jsonLicitacion.strip()
            # -----------------------------------------
            # ----- PROCESO DE LIMPIEZA DE JSON -------
            # -----------------------------------------
            jsonLicitacion = jsonLicitacion[1:][:-1].strip()
            jsonLicitacion = jsonLicitacion.replace("\"\"","\"")
            jsonLicitacion = jsonLicitacion.replace("\"  \"", "\", \"")
            jsonLicitacion = reemplazoAux(jsonLicitacion)
            # -----------------------------------------
            # ---- FIN PROCESO DE LIMPIEZA DE JSON ----
            # -----------------------------------------
            hoja.write(i + 1, 1, jsonLicitacion)                # Se inserta el json limpio en el excel
            link = listadoInformacion[3].strip()
            link = link.replace(" NaN", "")
            link = link.strip()
            hoja.write(i + 1, 2, link)
        
        hoja.write(i + 1, 3, esValidoJson(jsonLicitacion))
        if(esValidoJson(jsonLicitacion)):
            jsonDatos = json.loads(jsonLicitacion)
            hoja.write(i + 1, 5, jsonDatos['Listado'][0]['Items']['Listado'][0]['Categoria'])
            hoja.write(i + 1, 6, jsonDatos['Listado'][0]['Items']['Listado'][0]['Descripcion'])
            hoja.write(i + 1, 7, jsonDatos['Listado'][0]['Nombre'])
            hoja.write(i + 1, 8, jsonDatos['Listado'][0]['Descripcion'])
            hoja.write(i + 1, 9, jsonDatos['Listado'][0]['Comprador']['NombreUnidad'])
            hoja.write(i + 1, 10, jsonDatos['Listado'][0]['Comprador']['NombreOrganismo'])
            hoja.write(i + 1, 11, jsonDatos['Listado'][0]['MontoEstimado'])

        if(i == numero):
            break
        i = i + 1
        print(i)
    libro.close()

#ruta = input("Por favor ingresar la ruta donde se encuentra el CSV\nRuta: ")
ruta = "C:/personal/historicoJsonLicitaciones.csv"
lineaQueSeQuiereObtener = input("Ingresar json que se quiere obtener.\nNúmero: ")





#jsonObtenido = obtenerJson(ruta, lineaQueSeQuiereObtener)
#print(jsonObtenido)
#print("El json mostrado tiene un formato válido" if esValidoJson(jsonObtenido) else "El json mostrado no tiene un formato válido")
#print("largo del json: " + str(len(jsonObtenido)))

ObtenerPrimerosJson2(ruta, lineaQueSeQuiereObtener)
