# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 20:07:46 2020

@author: Yo Mero
"""

import NumP as n
#import socket
import random as r
from AlGen import AlGen 
import PPros as p

def main():
    tweets = int(input("Número de tweets a procesar: "))
    tareas = []
    numT = 1
    while tweets != 0:
        tamT = r.randint(20, 40)
        tareas.append([numT,tamT])
        tweets -= tamT
        numT += 1
        if tweets <= 40 and tweets > 0:
            tareas.append([numT,tweets])
            tweets = 0
    ex_load = []
    for s in range(n.numP):
        ex_load.append(r.randint(10, 30))
    
    a = AlGen()
    tareas = a.AlgoritmoGenetico(tareas,ex_load)
    rep = int(len(tareas)/n.numP)
    sobra = len(tareas)%n.numP
    cont = 0
    suma = 0
    tweets = []
    for s in range(n.numP):
        for j in range(rep):
            suma += tareas[cont][1]
            cont += 1
        if sobra > 0:
            suma += tareas[cont][1]
            cont += 1
            sobra -= 1
        tweets.append(suma)
        suma = 0
    numT = max(tweets)
    p.PreprocesarTweets(numT,0,"paralelo")
        
main()
