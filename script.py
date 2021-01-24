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
    except ValueError:
        return False

# Función que permite reemplazar carácteres hasta ahora necesarios para la obtención de un json válido.
# Entrada: string del json que será reemplazado.
# Salida: el mismo string que se da por entrada, pero reemplazando los caracteres necesarios.
def limpiarJson(entrada):
    entrada = entrada.strip()
    entrada = entrada.strip()[1:][:-1].strip()
    entrada = entrada.replace("\"\"","\"")
    entrada = entrada.replace("\"  \"", "\", \"")
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

# Función que permite limpiar el link que viene en el CSV con caracteres válidos.
# Entrada: string del link que será limpiado.
# Salida: el mismo link pero sin caracteres inválidos.
def limpiarLink(entrada):
    entrada = entrada.strip()
    entrada = entrada.replace(" NaN", "")
    entrada = entrada.strip()
    return entrada

# Función que permite crear un CSV con cierta cantidad de líneas y obtener información relevante.
# Entrada: la ruta de acceso al histórico de licitaciones; y la cantidad de líneas que se quiere obtener.
# Salida: la creación de un CSV con información relevante del csv de entrada.
def ObtenerInformacionRelevante_resumen_xlsx(rutaHistorico, numero):
    numero = int(numero)                                        # Transformando el parámetro a número
    df = pd.read_csv(rutaHistorico, chunksize=1)                # Crear un dataframe a partir del CSV
    i = 0
    contador = 0
    libro = xlsxwriter.Workbook('licitaciones.xlsx')            # Se crea el excel
    hoja = libro.add_worksheet()                                # Se añade una hoja el excel
    centrar = libro.add_format({'align': 'center'})             # Se centran los títulos de las columnas

    hoja.write(0, 0, "ID", centrar)                             
    hoja.write(0, 1, "JSON", centrar)                           #-------------------------------------------
    hoja.write(0, 2, "LINK", centrar)                           #-------------------------------------------                
    hoja.write(0, 3, "VALIDO JSON", centrar)                    #-------------------------------------------                
    hoja.write(0, 5, "Categoría Item", centrar)                 # ----- Se crea la cabecera de la hoja -----                
    hoja.write(0, 6, "Descripción Item", centrar)               # ------------------------------------------
    hoja.write(0, 7, "Nombre Solicitud", centrar)               #-------------------------------------------
    hoja.write(0, 8, "Descripcion Solicitud", centrar)          #-------------------------------------------    
    hoja.write(0, 9, "Nombre unidad compradora", centrar)       
    hoja.write(0, 10, "Nombre organismo comprador", centrar)
    hoja.write(0, 11, "Monto estimado", centrar)
    hoja.write(0, 12, "Fecha", centrar)

                                                                # ------------------------------------------------------------------------
    for registro in df:                                         # ---  Por cada registro en el dataframe (CSV), arrojará esto: -----------
                                                                # ------------------------------------------------------------------------
                                                                # --------  "codigoexterno;detalleJson;urllicitacion  --------------------
                                                                # ----  '3021-124-L119';'{listado: {...';'https://mercado'"  -------------
                                                                # ------------------------------------------------------------------------

        registroString = registro.to_string()                   # Aquí se tiene lo anteriormente mencionado pero como string

        listadoRegistroString = registroString.split('\n')      # Como están separados por un salto de línea, interesa sólo
                                                                # el segundo elemento, que es el que tiene la información


        registroInformacion = listadoRegistroString[1]          # Aquí se tiene sólo la parte "3021-124-L119;{listado: {...;https://mercado..."
        listadoInformacion = registroInformacion.split(';')     # Aquí se separa lo anterior por ; para tener un listado.
        
        largoListadoInfo = len(listadoInformacion)              # Aquí se tiene el largo de lo anterior, ya que puede darse el caso
                                                                # que dentro del json (texto) tenga puntoycoma, o también puede darse el caso
                                                                # que no contenga el link de acceso a información complementaria.
        
        idLicitacion = ""
        jsonLicitacion = ""
        linkLicitacion = ""

        if (largoListadoInfo == 2):                              # Si tiene largo 2, quiere decir que no viene con el link
            idLicitacion = listadoInformacion[0].strip()

            jsonLicitacion = listadoInformacion[1]                   
            jsonLicitacion = limpiarJson(jsonLicitacion)           
            
            linkLicitacion = "http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=" + idLicitacion

        if(largoListadoInfo > 2):                              # Si tiene largo 3 o mayor
            idLicitacion = listadoInformacion[0].strip()

            # Ver si el último item tiene un "http:" al principio, eso quiere decir que tiene link
            if(listadoInformacion[largoListadoInfo - 1][0:4] == "http"):
                for j in range(1, largoListadoInfo - 1):
                    jsonLicitacion = jsonLicitacion + listadoInformacion[j]
                jsonLicitacion = limpiarJson(jsonLicitacion)

                linkLicitacion = listadoInformacion[largoListadoInfo - 1]
                linkLicitacion = limpiarLink(linkLicitacion)
            else:
                for j in range(1, largoListadoInfo):
                    jsonLicitacion = jsonLicitacion + listadoInformacion[j]
                jsonLicitacion = limpiarJson(jsonLicitacion)

                linkLicitacion = "http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=" + idLicitacion
            
        
        
        if(esValidoJson(jsonLicitacion)):
            hoja.write(contador + 1, 0, idLicitacion)
            hoja.write(contador + 1, 1, jsonLicitacion)  
            hoja.write(contador + 1, 2, linkLicitacion)             
            hoja.write(contador + 1, 3, esValidoJson(jsonLicitacion))
            jsonDatos = json.loads(jsonLicitacion)

            cantidadItems = int(jsonDatos['Listado'][0]['Items']['Cantidad'])

            categoriaItem = ""
            descripcionItem = ""
            for k in range(cantidadItems):
                if(k > 0):
                    categoriaItem = categoriaItem + "#*#*#*#*#*#*#*#*#*#*"
                    descripcionItem = descripcionItem + "#*#*#*#*#*#*#*#*#*#*"
                categoriaItem = categoriaItem + jsonDatos['Listado'][0]['Items']['Listado'][k]['Categoria']
                descripcionItem = descripcionItem + jsonDatos['Listado'][0]['Items']['Listado'][k]['Descripcion']
                
            hoja.write(contador + 1, 5, categoriaItem)
            hoja.write(contador + 1, 6, descripcionItem)
            hoja.write(contador + 1, 7, jsonDatos['Listado'][0]['Nombre'])
            hoja.write(contador + 1, 8, jsonDatos['Listado'][0]['Descripcion'])
            hoja.write(contador + 1, 9, jsonDatos['Listado'][0]['Comprador']['NombreUnidad'])
            hoja.write(contador + 1, 10, jsonDatos['Listado'][0]['Comprador']['NombreOrganismo'])
            contador = contador + 1

        if(i == numero):
            break
        i = i + 1
        print("analizando la licitación " + str(i))
    libro.close()

def ObtenerInformacionRelevante_corpus_txt(rutaHistorico, numero):
    numero = int(numero)                                        # Transformando el parámetro a número
    df = pd.read_csv(rutaHistorico, chunksize=1)                # Crear un dataframe a partir del CSV
    i = 0
    contador = 0
    archivo = open('corpus.txt', 'w')

                                                                # ------------------------------------------------------------------------
    for registro in df:                                         # ---  Por cada registro en el dataframe (CSV), arrojará esto: -----------
                                                                # ------------------------------------------------------------------------
                                                                # --------  "codigoexterno;detalleJson;urllicitacion  --------------------
                                                                # ----  '3021-124-L119';'{listado: {...';'https://mercado'"  -------------
                                                                # ------------------------------------------------------------------------

        registroString = registro.to_string()                   # Aquí se tiene lo anteriormente mencionado pero como string

        listadoRegistroString = registroString.split('\n')      # Como están separados por un salto de línea, interesa sólo
                                                                # el segundo elemento, que es el que tiene la información


        registroInformacion = listadoRegistroString[1]          # Aquí se tiene sólo la parte "3021-124-L119;{listado: {...;https://mercado..."
        listadoInformacion = registroInformacion.split(';')     # Aquí se separa lo anterior por ; para tener un listado.
        
        largoListadoInfo = len(listadoInformacion)              # Aquí se tiene el largo de lo anterior, ya que puede darse el caso
                                                                # que dentro del json (texto) tenga puntoycoma, o también puede darse el caso
                                                                # que no contenga el link de acceso a información complementaria.
        
        idLicitacion = ""
        jsonLicitacion = ""
        linkLicitacion = ""

        if (largoListadoInfo == 2):                              # Si tiene largo 2, quiere decir que no viene con el link
            idLicitacion = listadoInformacion[0].strip()

            jsonLicitacion = listadoInformacion[1]                   
            jsonLicitacion = limpiarJson(jsonLicitacion)           
            
            linkLicitacion = "http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=" + idLicitacion

        if(largoListadoInfo > 2):                              # Si tiene largo 3 o mayor
            idLicitacion = listadoInformacion[0].strip()

            # Ver si el último item tiene un "http:" al principio, eso quiere decir que tiene link
            if(listadoInformacion[largoListadoInfo - 1][0:4] == "http"):
                for j in range(1, largoListadoInfo - 1):
                    jsonLicitacion = jsonLicitacion + listadoInformacion[j]
                jsonLicitacion = limpiarJson(jsonLicitacion)

                linkLicitacion = listadoInformacion[largoListadoInfo - 1]
                linkLicitacion = limpiarLink(linkLicitacion)
            else:
                for j in range(1, largoListadoInfo):
                    jsonLicitacion = jsonLicitacion + listadoInformacion[j]
                jsonLicitacion = limpiarJson(jsonLicitacion)

                linkLicitacion = "http://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?idlicitacion=" + idLicitacion
            
        
        
        if(esValidoJson(jsonLicitacion)):
            jsonDatos = json.loads(jsonLicitacion)
            cantidadItems = int(jsonDatos['Listado'][0]['Items']['Cantidad'])
            categoriaItem = ""
            descripcionItem = ""
            for k in range(cantidadItems):
                if(k > 0):
                    categoriaItem = categoriaItem + "#*#*#*#*#*#*#*#*#*#*"
                    descripcionItem = descripcionItem + "#*#*#*#*#*#*#*#*#*#*"
                categoriaItem = categoriaItem + jsonDatos['Listado'][0]['Items']['Listado'][k]['Categoria']
                descripcionItem = descripcionItem + jsonDatos['Listado'][0]['Items']['Listado'][k]['Descripcion']
            

            archivo.write(idLicitacion)
            archivo.write('####')
            archivo.write(jsonDatos['Listado'][0]['Nombre'].replace('\n', ' . ').replace('\r', ' . '))
            archivo.write(' . ')
            archivo.write(jsonDatos['Listado'][0]['Descripcion'].replace('\n', ' . ').replace('\r', ' . '))
            archivo.write(' . ')
            archivo.write(jsonDatos['Listado'][0]['Comprador']['NombreUnidad'].replace('\n', ' . ').replace('\r', ' . '))
            archivo.write(' . ')
            archivo.write(jsonDatos['Listado'][0]['Comprador']['NombreOrganismo'].replace('\n', ' . ').replace('\r', ' . '))
            archivo.write('####')
            archivo.write(jsonDatos['Listado'][0]['Items']['Listado'][0]['Categoria'].split(' / ')[0])
            archivo.write('\n')
            contador = contador + 1

        if(i == numero):
            break
        i = i + 1
        print("analizando la licitación " + str(i))
    archivo.close()

#ruta = input("Por favor ingresar la ruta donde se encuentra el CSV\nRuta: ")
ruta = "/home/nicolasquintanam/Licitaciones/historicoJsonLicitaciones.csv"
lineaQueSeQuiereObtener = input("Ingresar json que se quiere obtener.\nNúmero: ")

ObtenerInformacionRelevante_corpus_txt(ruta, lineaQueSeQuiereObtener)
