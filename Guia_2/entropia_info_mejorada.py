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
def calcularEntropia(listaP):
    return sum(p * info(p) for p in listaP)



def calcularEntropiaBinaria(w):
    return calcularEntropia([w,1-w])



