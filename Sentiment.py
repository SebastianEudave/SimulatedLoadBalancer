# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:23:21 2020

@author: Yo Mero
"""

from textblob import TextBlob


#Analisis de sentimiento del tweet
def AnalisisSentimiento(text):
    fila = []
    simple_text = TextBlob(text)
    #Se agrega a la fila el número de palabras del wordCloud
    #fila.append(len(word_list))
    #Se obtiene la polaridad y subjetividad del tweet
    polaridad,subjetividad = ObtenerPyS(simple_text)
    #Se agrega a la fila la polaridad
    fila.append(polaridad)
    #Se agrega a la fila la clasificación de la polaridad
    fila.append(ClasificarPolaridad(polaridad))
    #Se agrega a la fila la subjetividad
    fila.append(subjetividad)
    #Se regresa la fila
    return fila
    
#Obtenemos la polaridad y subjetividad del texto
def ObtenerPyS(simple_text):
    return simple_text.sentiment

#Clasificamos la polaridad del tweet
def ClasificarPolaridad(polaridad):
    if polaridad < 0.6:
        if polaridad <= 0:
            if polaridad == 0:
                #Si es 0 es neutral
                return "NT"
            elif polaridad > -0.6:
                #Si es mayor a -0.6 y menor a 0 es negativo
                return "N"
            else:
                #Si es menor a 0.6 es muy negativo
                return "MN"
        else:
            #Si esta entre 0.6 y 0.3 es positivo
            return "P"
    else:
        #Si es mayor a 0.6 es muy positivo
        return "MP"