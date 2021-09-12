# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:23:25 2020

@author: Yo Mero
"""

#import Prepro as p
import pandas as pd
from time import time
import Sentiment as s
import KNN as knn
import Preprocess as p

def PreprocesarTweets(limS,limI,string):
    csv = []
    tiempoI = time()
    #Se abre el dataset con los tweets en ingles, se preprocesa el texto y se hace un análisis de sentimiento
    df = pd.read_csv("RecoleccionTweetsEs(1).csv",encoding='utf-16',engine='python',sep='\t')
    print(df)
    tweets = df['text'].iloc[limI:limS]
    cont = limI
    #Para cada tweet se clasifica el sentimiento y se agrega el número de palabras en el WordCloud
    for text in tweets:
        #Se aplica el analisis de sentimiento al texto contenido en tweet
        fila = s.AnalisisSentimiento(text)
        #Se aplica la fase 2 de preprocesamiento de texto para calcular el numero de palabras en el wordcloud de cada tweet
        fila.append(p.Preprocesamiento(df.loc[cont, 'text']))
        csv.append(fila)
        cont += 1
    if limS == -1:
        limS = 100000
    #Se guardan los resultados en otro DataSet que contendrá la polaridad, la clasificación del sentimiento, la subjetividasd y el número de palanras en el wordcloud
    dw = pd.DataFrame(csv)
    dw.to_csv("Dataset.csv", header = ['Polaridad','Clasificacion','Subjetividad','WordCloud'])
    glob,mconf = knn.MachineLearning()
    tiempoF = time() - tiempoI
    #Se guarda el tiempo de ejecución el el archivo txt tiempoE.txt, además de la matriz de confusión, calificación global del modelo y la razón de error
    f = open ('tiempoE.txt','a')
    f.write(str(limS-limI) + " tweets en : %0.5f segundos. " % tiempoF+"("+string+")\n")
    f.write("Matriz de confusión : \n")
    f.write(str(mconf))
    f.write("\nCalificación global : %0.3f" % glob)
    f.write("\nRazón de Error : %0.3f \n\n" % (1-glob))
    f.close()
    f.close()
    print("Tiempo de ejecución: %0.5f segundos. " % tiempoF)
    
