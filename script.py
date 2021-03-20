# -*- coding: utf-8 -*-
# -- Librerías necesarias --
import pandas as pd
import json
import xlsxwriter
from io import open
import re
from time import time

# Función que permite validar el formato de un json.
# Entrada: string que se validará.
# Salida: booleano indicando si es válido o no.
def esValidoJson(jsonString):
    try:
        json.loads(jsonString)
        return True
    except ValueError:
        return False

# Permite crear un diccionario de categorías, en donde se indica la categoría
# original y retorna la categoría definitiva, reduciendo así, las 56 categor-
# ías a solo 5.
def create_category_dictionary():
    category_dictionary = {}

    category = "Construcción"
    category_dictionary["Artículos para estructuras obras y construcciones"] = category
    category_dictionary["Maquinaria para construcción y edificación"] = category
    category_dictionary["Servicios de construcción y mantenimiento"] = category

    category = "Salud, farmacéutica y laboratorio"
    category_dictionary["Equipamiento para laboratorios"] = category
    category_dictionary["Equipamiento y suministros médicos"] = category
    category_dictionary["Medicamentos y productos farmacéuticos"] = category
    category_dictionary["Salud servicios sanitarios y alimentación"] = category

    category = "Servicios y equipamiento industrial"
    category_dictionary["Artículos de fabricación y producción"] = category
    category_dictionary["Combustibles lubricantes y anticorrosivos"] = category
    category_dictionary["Equipamiento para el acondicionamiento distribución y filtrado de fluidos"] = category
    category_dictionary["Equipamiento para manejo y estiba de materiales"] = category
    category_dictionary["Herramientas y maquinaria en general"] = category
    category_dictionary["Maquinaria para fabricación y transformación industrial"] = category
    category_dictionary["Maquinaria para minería y perforación"] = category
    category_dictionary["Maquinarias equipos y suministros para la industria de servicios"] = category
    category_dictionary["Productos químicos industriales"] = category
    category_dictionary["Resinas cauchos espumas y elastómeros"] = category
    category_dictionary["Servicios de limpieza industrial"] = category
    category_dictionary["Servicios de perforación de minería petróleo y gas"] = category
    category_dictionary["Servicios de producción y fabricación industrial"] = category
    category_dictionary["Servicios de transporte almacenaje y correo"] = category
    category_dictionary["Vehículos y equipamiento en general"] = category

    category = "Servicios administrativos, financieros y electrónica"
    category_dictionary["Consultoria"] = category
    category_dictionary["Equipos accesorios y suministros de oficina"] = category
    category_dictionary["Organizaciones y consultorías políticas demográficas económicas sociales y de administración pública"] = category
    category_dictionary["Productos de papel"] = category
    category_dictionary["Productos impresos y publicaciones"] = category
    category_dictionary["Servicios financieros pensiones y seguros"] = category
    category_dictionary["Servicios profesionales administrativos y consultorías de gestión empresarial"] = category
    category_dictionary["Artículos de electrónica"] = category
    category_dictionary["Artículos eléctricos y de iluminación"] = category
    category_dictionary["Equipos y suministros de imprenta fotográficos y audiovisuales"] = category
    category_dictionary["Maquinaria para generación y distribución de energía"] = category
    category_dictionary["Muebles accesorios electrodomésticos y productos electrónicos"] = category
    category_dictionary["Servicios basados en ingeniería ciencias sociales y tecnología de la información"] = category
    category_dictionary["Servicios editoriales de diseño publicidad gráficos y artistas"] = category
    category_dictionary["Tecnologías de la información telecomunicaciones y radiodifusión"] = category

    category = "Otros"
    category_dictionary["Alimentos bebidas y tabaco"] = category
    category_dictionary["Artículos para plantas y animales"] = category
    category_dictionary["Educación formación entrenamiento y capacitación"] = category
    category_dictionary["Equipos suministros y accesorios deportivos y recreativos"] = category
    category_dictionary["Equipos y suministros de defensa orden público protección y seguridad"] = category
    category_dictionary["Equipos y suministros de limpieza"] = category
    category_dictionary["Instrumentos musicales juegos juguetes artesanías y materiales educativos"] = category
    category_dictionary["Maquinaria para agricultura pesca y silvicultura"] = category
    category_dictionary["Muebles y mobiliario"] = category
    category_dictionary["Organizaciones sociales laborales y clubes"] = category
    category_dictionary["Productos derivados de minerales plantas y animales"] = category
    category_dictionary["Productos para relojería joyería y gemas"] = category
    category_dictionary["Ropa maletas y productos de aseo personal"] = category
    category_dictionary["Servicios agrícolas pesqueros forestales y relacionados con la fauna"] = category
    category_dictionary["Servicios básicos y de información pública"] = category
    category_dictionary["Servicios de cuidado personal y domésticos"] = category
    category_dictionary["Servicios de defensa nacional orden público y seguridad"] = category
    category_dictionary["Servicios de Viajes alimentación alojamiento y entretenimiento"] = category
    category_dictionary["Servicios medioambientales"] = category

    return category_dictionary


# Permite estandarizar el texto antes de ser utilizado por las técnicas de preprocesamiento
# de texto. Esta estandarización consta de transformar el texto a minúsculas, eliminar pun-
# tos, comas y puntuaciones en general,  eliminar números y eliminar palabras que contienen 
# solo una letra.
def standardize(words):
    words = words.replace('\n', ' ')
    words = words.replace('\r', ' ')
    words = words.replace('\t', ' ')
    words = words.replace('_', ' ')
    words = words.replace('º', '')
    words = words.replace('à', 'a')
    words = words.replace('è', 'e')
    words = words.replace('ì', 'i')
    words = words.replace('ò', 'o')
    words = words.replace('ù', 'u')
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_number(words)
    words = remove_one_character_words(words)
    return words

# Transforma todo el texto a minúsculas.
def to_lowercase(words):
    return words.lower()

# Elimina puntuaciones de un texto.
def remove_punctuation(words):
    return re.sub(r'[^\w\s]','',words)

# Elimina los números de un texto.
def remove_number(words):
    return ''.join([i for i in words if not i.isdigit()])

# Elimina las palabras que tienen solo un caracter.
def remove_one_character_words(words):
    word_list = words.split(' ')
    return ' '.join([i for i in word_list if (len(i) > 1)])

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

def obtener_numero_categoria_licitacion(category):
    if(category == 'Construcción'):
        return 1
    if(category == 'Salud, farmacéutica y laboratorio'):
        return 2
    if(category == 'Servicios y equipamiento industrial'):
        return 3
    if(category == 'Servicios administrativos, financieros y electrónica'):
        return 4
    else:
        return 5 #Categoría Otros

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
def ObtenerInformacionRelevante_resumen_xlsx(rutaHistorico, numero, dictionary):
    numero = int(numero)                                        # Transformando el parámetro a número
    df = pd.read_csv(rutaHistorico, chunksize=1)                # Crear un dataframe a partir del CSV
    i = 0
    contador = 0
    libro = xlsxwriter.Workbook('licitaciones.xlsx')            # Se crea el excel
    hoja = libro.add_worksheet()                                # Se añade una hoja el excel
    centrar = libro.add_format({'align': 'center'})             # Se centran los títulos de las columnas
    archivo = open('corpus.txt', 'w')
    archivo_no_c = open('corpus_no_considerado.txt', 'w')
    archivo_no_considerado_por_duplicidad = open('corpus_no_considerado_por_duplicidad.txt', 'w')
    archivo_licitaciones_corruptas = open('archivo_con_licitaciones_corruptas.txt', 'w')
    archivo_con_licitaciones_mas_de_un_item = open('archivo_licitaciones_mas_un_item.txt', 'w')
    licitaciones_no_consideradas = 0
    licitaciones_consideradas_en_corpus = []

    hoja.write(0, 0, "ID", centrar)                             
    hoja.write(0, 1, "JSON", centrar)                           #-------------------------------------------
    hoja.write(0, 2, "LINK", centrar)                           #-------------------------------------------                
    hoja.write(0, 3, "VALIDO JSON", centrar)                    #-------------------------------------------                
    hoja.write(0, 5, "Nombre Solicitud", centrar)               #-------------------------------------------
    hoja.write(0, 6, "Descripcion Solicitud", centrar)          #-------------------------------------------    
    hoja.write(0, 7, "Descripción Item", centrar)               # ------------------------------------------
    hoja.write(0, 8, "Categoría Item", centrar)                 # ----- Se crea la cabecera de la hoja -----                
    hoja.write(0, 9, "Nombre unidad compradora", centrar)       
    hoja.write(0, 10, "Nombre organismo comprador", centrar)
    hoja.write(0, 11, "Fecha", centrar)

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
            if(cantidadItems == 1):
                categoria_licitacion = jsonDatos['Listado'][0]['Items']['Listado'][0]['Categoria'].split(' / ')[0]
                categoria_licitacion = categoria_licitacion.replace('  ', ' ').strip()
                categoria_final = ''
                if(categoria_licitacion in dictionary):
                    categoria_final = dictionary[categoria_licitacion]
                    categoria_final = str(obtener_numero_categoria_licitacion(categoria_final))
                else:
                    print('no encontré la categoría para la licitación ' + i)
                    print(categoria_licitacion)
                


                texto_licitacion = jsonDatos['Listado'][0]['Nombre'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                texto_licitacion += ' '
                texto_licitacion += jsonDatos['Listado'][0]['Descripcion'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                texto_licitacion += ' '
                texto_licitacion += jsonDatos['Listado'][0]['Items']['Listado'][0]['Descripcion'].replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

                



                texto_reducido = standardize(texto_licitacion)
                listado_texto_reducido = texto_reducido.split(' ')
                nuevo_listado = []
                for palabra in listado_texto_reducido:
                    if(palabra not in nuevo_listado):
                        nuevo_listado.append(palabra)
                

                if(len(nuevo_listado) >= 3):
                    if(idLicitacion not in licitaciones_consideradas_en_corpus):
                        hoja.write(contador + 1, 0, idLicitacion)
                        hoja.write(contador + 1, 1, jsonLicitacion)  
                        hoja.write(contador + 1, 2, linkLicitacion)             
                        hoja.write(contador + 1, 3, esValidoJson(jsonLicitacion))
                        hoja.write(contador + 1, 5, jsonDatos['Listado'][0]['Nombre'])
                        hoja.write(contador + 1, 6, jsonDatos['Listado'][0]['Descripcion'])
                        hoja.write(contador + 1, 7, jsonDatos['Listado'][0]['Items']['Listado'][0]['Descripcion'])
                        hoja.write(contador + 1, 8, jsonDatos['Listado'][0]['Items']['Listado'][0]['Categoria'])
                        hoja.write(contador + 1, 9, jsonDatos['Listado'][0]['Comprador']['NombreUnidad'])
                        hoja.write(contador + 1, 10, jsonDatos['Listado'][0]['Comprador']['NombreOrganismo'])
                        hoja.write(contador + 1, 11, str(jsonDatos['Listado'][0]['Fechas']['FechaInicio'])[0:10])



                        archivo.write(idLicitacion)
                        archivo.write('####')
                        archivo.write(texto_reducido)
                        archivo.write('####')
                        archivo.write(categoria_final)
                        archivo.write('\n')
                        contador = contador + 1

                        licitaciones_consideradas_en_corpus.append(idLicitacion)
                    else:
                        archivo_no_considerado_por_duplicidad.write(idLicitacion)
                        archivo_no_considerado_por_duplicidad.write('\n')
                else:
                    archivo_no_c.write(texto_licitacion)
                    archivo_no_c.write('\n')
                    licitaciones_no_consideradas += 1
            else:
                archivo_con_licitaciones_mas_de_un_item.write(idLicitacion)
                archivo_con_licitaciones_mas_de_un_item.write('\n')
        else:
            archivo_licitaciones_corruptas.write(idLicitacion)
            archivo_licitaciones_corruptas.write('\n')
        if(i == numero):
            break
        i = i + 1
        print(i)
    print('no consideré ' + str(licitaciones_no_consideradas) + 'licitaciones')
    archivo.close()
    archivo_no_c.close()
    archivo_no_considerado_por_duplicidad.close()
    archivo_con_licitaciones_corruptas.close()
    archivo_con_licitaciones_mas_de_un_item.close()
    libro.close()


dictionary = create_category_dictionary()

#ruta = input("Por favor ingresar la ruta donde se encuentra el CSV\nRuta: ")
ruta = "/home/nicolasquintanam/Licitaciones/historicoJsonLicitaciones.csv"
#lineaQueSeQuiereObtener = input("Ingresar json que se quiere obtener.\nNúmero: ")
start_time = time()
ObtenerInformacionRelevante_resumen_xlsx(ruta, 100000, dictionary)
elapsed_time = time() - start_time
print("Tiempo utilizado: %.10f segundos." % elapsed_time)
