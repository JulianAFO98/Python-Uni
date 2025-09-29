# Dada una lista que representa una distribución de probabilidades de una fuente de
# memoria nula, desarrollar funciones en Python que resuelvan lo siguiente:
# a. generar otra lista con la cantidad de información en bits de cada símbolo (utilizar
# comprensión de listas).
# b. obtener la entropía de la fuente (utilizar la función anterior)

import math
def info(val,base): # preguntar
    if val == 0:
        return 0
    return -math.log(val,base)

#a
def generarListaInfo(lista,base):
    return [info(val,base) for val in lista]

#b
def calcularEntropia(listaP,base):
    return sum(p * info(p,base) for p in listaP)



def calcularEntropiaBinaria(w,base):
    return calcularEntropia([w,1-w],base)

"""
Desarrollar una función en Python que reciba: una lista con el alfabeto de una fuente, otra
con su distribución de probabilidades y un entero N. Esta función debe generar dos nuevas
listas con la extensión de orden N y su distribución de probabilidades.
"""
def generarListaExtension(alfabeto,probs,grado):
    cantFilas = len(alfabeto)**grado
    listaExtension = ["" for _ in range(cantFilas)]
    listaExtensionProb = [1 for _ in range(cantFilas)]
    
    for i in range(grado): # los n simbolos
        tamanioParticion = len(alfabeto)**(grado - (i+1))
        for j in range(cantFilas): # iterar sobre todas las filas
            elemIndex = (j // tamanioParticion) % len(alfabeto)
            listaExtension[j] += alfabeto[elemIndex]
            listaExtensionProb[j] *= probs[elemIndex]   
    return listaExtension,listaExtensionProb

"""
lista = [1/2,1/4,1/4]
print(generarListaInfo(lista,2))
print(calcularEntropia(lista,2))
print(calcularEntropiaBinaria(1/4,2))
"""



n=2
lista = [1/6]*6
listaExtension,listaExtensionProb = generarListaExtension(["D1","D2","D3","D4","D5","D6"],lista,n)
print(listaExtension)
print(listaExtensionProb)
print("Entropia de la lista de probabilidades extendida",calcularEntropia(listaExtensionProb,2))
print("n * H(S)",calcularEntropia(lista,2) * n)