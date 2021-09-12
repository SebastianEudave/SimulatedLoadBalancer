# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 18:03:33 2020

@author: Yo Mero
"""
import random as r
import NumP as n

class AlGen:
    def _init_(self):
        pass
        
    #Función que ejecuta el algoritmo genético para conseguir una solución óptima (tareas es la variable de la lista de tareas que entra, ex_load las cargas que ya estan en cada procesador, numP el numero de procesadores)
    def AlgoritmoGenetico(self,tareas,ex_load):
        #Se especifican el número de generaciones
        numG = 25
        #Se especifica el tamaño de las poblaciones
        tamP = 25
        #Valores de los limites superiro e inferior de las cargas antes de que un porcesador este demasiado cargado o muy poco cargado
        avgL = self.CargaPromedio( tareas, ex_load)
        limS = avgL * 1.2
        limI = avgL * 0.8
        #Se genera la poblacion inicial y se calcula su fitness
        poblacion = self.PoblacionInicial(tareas,tamP)
        fitness = self.CalcularFitness(poblacion,ex_load,limS,limI)
        #Se busca el mejor individuo de la generación
        posM = self.BuscarMejor(fitness)
        mejorS = poblacion[posM]
        mejorF = fitness[posM]
        self.ImprimirSol(mejorS, mejorF, 0, ex_load)
        #Se hacen las operaciones de selección, cruzamiento y mutación para cada generación
        for i in range(numG):
            poblacion = self.SeleccionRuleta(poblacion, fitness, tamP)
            poblacion = self.CruzamientoPob(poblacion, tamP)
            fitness = self.CalcularFitness(poblacion,ex_load,limS,limI)
            #Se busca el mejor individuo de la generación
            mejorS = poblacion[posM]
            mejorF = fitness[posM]
            self.ImprimirSol(mejorS, mejorF, i+1, ex_load)
        #Se devuelven las tareas que deberán ser asignadas a los procesadores y aquellas que deberán quedarse en la ventana
        return mejorS
    
    #Funcion que genera la poblacion inicial 
    def PoblacionInicial(self,tareas,tamP):
        #Se inicializa la lista de soluciones de la poblacón inicial y como primer solución se elige a la lista de tareas tal y como llego 
        poblacion = []
        poblacion.append(tareas)
        #Se generan soluciones aleatorias que revuelven el orden de las tareas
        for i in range(tamP-1):
            poblacion.append(r.sample(tareas,len(tareas)))
        #Se regresa la poblacion inicial
        return poblacion
    
    #Calculamos el fitness de una poblacion
    def CalcularFitness(self,poblacion,ex_load,limS,limI):
        #Se inicializa la lista de fitness
        fitness = []
        #Se calcula el fitness para cada solucion de la poblacion
        for i in range(len(poblacion)):
            maxPan,cargas = self.MaxPan(poblacion[i],ex_load)
            fitness.append((1/maxPan)*self.UsoPromedio(maxPan,cargas)*(self.QueuesAceptables(cargas,limS,limI)/n.numP))
        #Se regresa la lista de fitness
        return fitness
        
    #Se calcula el valor maximo de carga para los procesadores en una solución
    def MaxPan(self,sol,ex_load):
        #Se inicializa el valor de maxpan
        maxPan = 0
        #Se suman la carga actual de cada procesador con las nuevas cargas respectivamente
        cargas = self.CalcularCarga(sol,ex_load)
        for i in range(n.numP):
            #Si la suma de las cargas es más grande al valor actual más grande se asigna a la variable maxpan
            if cargas[i] > maxPan:
                maxPan = cargas[i]
        #Se regresa el valor del maxPan
        return maxPan,cargas
            
    #Calculamos el uso promedio de los procesadores
    def UsoPromedio(self,maxPan,cargas):
        promedio = 0
        #Se suman los usos de cada procesador a la variable promedio 
        for i in range(n.numP):
            promedio += cargas[i] / maxPan
        #para calcular el uso promedio se divide la suma total de usos entre el número de procesadores
        promedio /= n.numP
        return promedio
    
    #Se cuentabn el número de queues aceptables, es decir aquellas que no infringen los limites de carga anteriormente establecidos
    def QueuesAceptables(self,cargas,limS,limI):
        numQ = 0
        for i in range(n.numP):
            #Si la carga del procesador esta entre los limites actuales se suma 1 al numero de queues aceptables, si no no pasa nada
            if cargas[i] <= limS and cargas[i] >= limI:
                numQ +=1
        #Regresamos el número de queues aceptables
        return numQ
                
    #Calculamos la carga promedio que hay en el sistema
    def CargaPromedio(self,tareas,ex_load):
        #Se calcula la carga total que hay actualmente en el sistema
        sumaC = 0
        for i in range(n.numP):
            sumaC += ex_load[i]
        #Se calcula la carga total que entrarar en el sistema
        sumaT = 0
        for i in range(len(tareas)):
            sumaT += tareas[i][1]
        #Se regresa la carga promedio que es la suma de las cargas anteriormente sumadas entre el número de procesadores
        return (sumaC + sumaT) / n.numP
    
    #Funcion de seleccion 
    def SeleccionRuleta(self,poblacion,fitness,tamP):
        #Calculamos el fitness acumuladod e la población
        acumF = self.FitnessAcumulado(fitness)
        #Calculamos los espacios en la ruleta para cada solucion de acuierdo a su fitness y el fitness acumulado
        slot = self.Slots(acumF, fitness)
        poblacion2 = []
        #Se consigue un número aleatorio entre 0 y 1 ,y se selecciona la solucion donde el numero aleatorio haya caido en la ruleta
        for i in range(int(tamP / 2)):
            numA = r.random()
            poblacion2.append(self.ExtraccionSolucion(numA, poblacion, slot))
        #Se retorna la poblacion seleccionada
        return poblacion2
            
    #Se calcula el fitness acumulado de la poblacion
    def FitnessAcumulado(self,fitness):
        acumF = 0
        for i in range(len(fitness)):
            acumF += fitness[i]
        #Se regresa la sumatoria de fitness de la poblacion
        return acumF
    
    #Se generan cada uno de los pedazos de la ruleta
    def Slots(self,acumF,fitness):
        tempF = 0
        slot = []
        #Se calcula la probabilidad de supervivencia de cada solucion dividiendo el fitness de la solucion entre el fitness total de la poblacion, posteriormente se agrega el fitness acumulado hasta el momento del calculo 
        for i in range(len(fitness)):
            slot.append((fitness[i] / acumF) + tempF)
            tempF = slot[i]
        #Se retorna el espacio que ocupara cada solucion en la ruleta 
        return slot
            
    #Sacamos la solucion de acorde al numero aleatorio conseguido y a las probabilidades anteriormente calculadas para cada solucion
    def ExtraccionSolucion(self,numA,poblacion,slot):
        sumaF = 0
        #Se revisa si el espacio que ocupa cada solucion es mayor que el numero aleatorio conseguido, si es el caso se devuelve la solucion seleccionada
        for i in range(len(slot)):
            sumaF = slot[i]
            if sumaF >= numA:
                return poblacion[i]
            
    #Funcion de cruzamiento de una población
    def CruzamientoPob(self,poblacion,tamP):
        #Se cruzan los padres que fueron seleccionados por ruleta
        for i in range(int(tamP/2)):
            padre1 = poblacion[i]
            i += 1
            padre2 = poblacion[i]
            #Se reciben los hijos de los padres seleccionados y se agregan a la poblacion
            hijo1,hijo2 = self.Cruzamiento(padre1, padre2)
            poblacion.append(hijo1)
            poblacion.append(hijo2)
        #Se regresa la poblacion actualizada con los hijos
        return poblacion
        
    #Funcion que cruza dos padres y devuelve sus dos hijos
    def Cruzamiento(self,padre1,padre2):
        #Se elige una posicion aleatoria para empezar el cruzamiento
        numA = r.randint(0,len(padre1)-1)
        #Se inicializan los hijos con tuplas [0,0] para facilitar su escritura y la busqueda de espacios vacios
        hijo1 = []
        hijo2 = []
        for i in range(len(padre1)):
            hijo1.append([0,0])
            hijo2.append([0,0])
        hijo1[numA] = padre1[numA]
        hijo2[numA] = padre2[numA]
        inicio = hijo1[numA][0]
        temp = hijo2[numA][0]
        #Mientras que el primer elemento añadido al hijo1 no coincida con uno último del hijo2 se agregan los elementos donde el ultimo elemento añadido al hijo2 sea igual a un elemento del padre1
        while inicio != temp:
            numA = self.BuscarNumero(padre1, temp)
            hijo1[numA] = padre1[numA]
            hijo2[numA] = padre2[numA]
            temp = hijo2[numA][0]
        numA = self.BuscarNumero(hijo1, 0)
        #Para continuar el cruzamiento se intercambian las tareas que no fueron asignadas en el paso anterior minetras se encuenten elementos vacios o mejor dicho iguales a 0
        while numA != None:
            hijo2[numA] = padre1[numA]
            hijo1[numA] = padre2[numA]
            numA = self.BuscarNumero(hijo1, 0)
        #Se mutan los hijos generados
        hijo1 = self.Mutacion(hijo1)
        hijo2 = self.Mutacion(hijo2)
        #Se regresan los hijos
        return hijo1,hijo2
    
    #Buscamos un numero especifico temp en la solucion
    def BuscarNumero(self,sol,temp):
        #Cuando se encuentra el numero temp en alguna posicion de la solucion se devuelve dicha posicion
        for i in range(len(sol)):
            if temp == sol[i][0]:
                return i
        return None

    #Funcion para imprimir las soluciones de cada población y su fitness
    def ImprimirGeneracion(self,poblacion,fitness,numG):
        print("Generación: ",numG,"\n")
        for i in range(len(poblacion)):
            print(poblacion[i],fitness[i],"\n")
        print("\n")
        
    #Se busca la posicion de la mejor solución
    def BuscarMejor(self,fitness):
        mayor = 0
        posM = 0
        for i in range(len(fitness)):
            if fitness[i] > mayor:
                mayor = fitness[i]
                posM = i
        return posM
    
    #Funcion para imprimir una solucion
    def ImprimirSol(self,sol,fitness,numG,ex_load):
        cargas = self.CalcularCarga(sol,ex_load)
        print("Mejor solucion de la generación ",numG,"  fitness: ",fitness,"\n")
        cont = 0
        for c in cargas:
            print("Procesador ",cont+1,": ",c-ex_load[cont]," tweets\n")
            cont += 1
        
    #Funcion que muta una solucion generada anteriormente
    def Mutacion(self,sol):
        #Se eligen dos numers aleatorios para intercambiar tareas en una solucion
        numA = r.randint(0,len(sol)-1)
        numA2 = r.randint(0,len(sol)-1)
        #Se intercambian las dos tareas previamente escogidas
        temp = sol[numA]
        sol[numA] = sol[numA2]
        sol[numA2] = temp
        #Se regresa la solucion ya mutada
        return sol

    #Funcion que regresa la lista de tareas que si serán enviadas a los procesadores y cuales se quedarán en la lista de tareas
    def ListaTareas(self,sol,limS,limI,ex_load):
        cargas = self.CalcularCarga(sol, ex_load)
        tareasA = []
        tareasQ = []
        cont = 0
        rep = int(len(sol)/n.numP)
        sobra = len(sol)%n.numP
        #Se verifica eu la carga de cada procesador este dentro de los límites, si es el caso se agregan las tareas la lista de tareas que serán asignadas, si no se envían a la lista de tareas que se quedarán en la ventana
        for i in range(n.numP):
            if cargas[i] > limS or cargas[i] < limI:
                for j in range(rep):
                    tareasQ.append(sol[cont])
                    tareasA.append([0,0])
                    cont += 1
                if sobra > 0:
                    tareasQ.append(sol[cont])
                    tareasA.append([0,0])
                    cont += 1
                    sobra -= 1
            else:
                for j in range(rep):
                    tareasA.append(sol[cont])
                    tareasQ.append([0,0])
                    cont += 1
                if sobra > 0:
                    tareasA.append(sol[cont])
                    tareasQ.append([0,0])
                    cont += 1
                    sobra -= 1
        #Se regresan las dos listas de tareas, las que si serán asignadas y las que no
        return tareasA,tareasQ
        
    #Funcion que calcula la carga de cada procesador en una solucion
    def CalcularCarga(self,sol,ex_load):
        cargas = []
        cont = 0
        rep = int(len(sol)/n.numP)
        sobra = len(sol)%n.numP
        for i in range(n.numP):
            #Se suma la carga de cada procesador respectivamente en la variable suma
            suma = ex_load[i]
            #Cada procesador recibe un número de tareas equitativas a la de los demás
            for j in range(rep):
                suma += sol[cont][1]
                cont += 1
            if sobra > 0:
                suma += sol[cont][1]
                cont += 1
                sobra -= 1
            #Se añade la carga calculada a la lista de cargas
            cargas.append(suma)
        return cargas