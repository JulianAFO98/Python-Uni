# Dada una lista que representa una distribución de probabilidades de una fuente de
# memoria nula, desarrollar funciones en Python que resuelvan lo siguiente:
# a. generar otra lista con la cantidad de información en bits de cada símbolo (utilizar
# comprensión de listas).
# b. obtener la entropía de la fuente (utilizar la función anterior)

import math
import cadenas

def info(val): # preguntar
    if val == 0:
        return 0
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

def calcularEntropiaBinaria(w):
    listaBinaria = [w,1-w]
    listaInfoBinaria = generarListaInfo(listaBinaria)
    return calcularEntropia(listaBinaria,listaInfoBinaria)

"""
# 3
lista = [0.166,0.166,0.166,0.166,0.166,0.166]
listaInformacion = generarListaInfo(lista)

print(calcularEntropia(lista,listaInformacion))


lista = [0.111,0.166,0.111,0.111,0.166,0.333]
listaInformacion = generarListaInfo(lista)

print(calcularEntropia(lista,listaInformacion))
"""
"""
#4
lista = [0.5,0.1,0.4]
listaInformacion = generarListaInfo(lista)
print(listaInformacion)
print(calcularEntropia(lista,listaInformacion))

lista = [0.5,0.5]
listaInformacion = generarListaInfo(lista)
print(listaInformacion)
print(calcularEntropia(lista,listaInformacion))

lista = [0.1,0.3,0.4,0.2]
listaInformacion = generarListaInfo(lista)
print(listaInformacion)
print(calcularEntropia(lista,listaInformacion))

"""
"""
#5

letras,probabilidades = cadenas.generarListaParalelas("ABDAACAABACADAABDAADABDAAABDCDCDCDC")
print(probabilidades)
listaInformacion = generarListaInfo(probabilidades)
print(calcularEntropia(probabilidades,listaInformacion))

"""
"""
#6
S = [1]
listaInformacion = generarListaInfo(S)
print(listaInformacion)
print(calcularEntropia(S,listaInformacion))
#Un evento que siempre ocurre no brinda informacion
"""
"""
#7
S = [0.25,0.25,0.25,0.25]
listaInformacion = generarListaInfo(S)
print(listaInformacion)
print(calcularEntropia(S,listaInformacion))
# Maximo valor posible = 2
# Para que ocurra esto cada elemento debe tener la misma probabilidad, a mayor probabilidad
# de un suceso, "mas normal" se vuelve y baja la incertidumbre
"""

#9
print(calcularEntropiaBinaria(0.25))
print(calcularEntropiaBinaria(0.75))
print(calcularEntropiaBinaria(0.5))
print(calcularEntropiaBinaria(0))
print(calcularEntropiaBinaria(1))
