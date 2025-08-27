# Dada una lista que representa una distribución de probabilidades de una fuente de
# memoria nula, desarrollar funciones en Python que resuelvan lo siguiente:
# a. generar otra lista con la cantidad de información en bits de cada símbolo (utilizar
# comprensión de listas).
# b. obtener la entropía de la fuente (utilizar la función anterior)

import math

def info(val): # preguntar
    return -math.log(val,2)

#a
def generarListaInfo(lista):
    return [info(val) for val in lista]

#b
def calcularEntropia(listaP,listaI):
    H = 0
    for i in range(len(listaI)): #preguntar
        H += listaP[i] * listaI[i]
    return H


lista = [0.5,0.25,0.25]
lista2 = generarListaInfo(lista)

print(lista2)
print(calcularEntropia(lista,lista2))