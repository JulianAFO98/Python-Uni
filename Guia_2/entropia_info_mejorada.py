# Dada una lista que representa una distribución de probabilidades de una fuente de
# memoria nula, desarrollar funciones en Python que resuelvan lo siguiente:
# a. generar otra lista con la cantidad de información en bits de cada símbolo (utilizar
# comprensión de listas).
# b. obtener la entropía de la fuente (utilizar la función anterior)

import math
import cadenas
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
    return calcularEntropia([w,1-w])



