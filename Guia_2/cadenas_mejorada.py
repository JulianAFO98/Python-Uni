"""
Implementar funciones en Python que resuelvan lo siguiente:
a. Dada una cadena de caracteres que representa un mensaje emitido por una fuente
de memoria nula, devolver dos listas paralelas que contengan: el alfabeto de la
fuente y las probabilidades de cada símbolo.
b. Dada una lista que contenga el alfabeto de una fuente y otra con las probabilidades
de cada símbolo, simular la generación de una cadena de caracteres emitida por
esa fuente.

"""

import random

def generarListaParalelas(cadena):
    contApariciones = []
    letras = []
    for i in range(len(cadena)):
        if cadena[i] not in letras:
            letras.append(cadena[i])
            contApariciones.append(1)
        else:
            index = letras.index(cadena[i])
            contApariciones[index]+=1
    
    probabilidades = [val/len(cadena) for val in contApariciones]
    return letras,probabilidades

""" Forma complicada
def acumularProbabilidades(probabilidades):
    acumuladas = []
    total = 0
    for p in probabilidades:
        total += p
        acumuladas.append(total)
    return acumuladas

def simulacion(letras,probabilidades,limite = 10):
    probabilidadesAcum = acumularProbabilidades(probabilidades)
    resultado = []
    for _ in range(n):
        valAnterior = 0
        indexLetra = len(letras) - 1
        randomNum = random.random()
        for index,p in enumerate(probabilidadesAcum):
            if valAnterior<=randomNum and randomNum<p:
                indexLetra = index
            valAnterior = p
        resultado.append(letras[indexLetra])
    return "".join(resultado)
"""

def simulacion(letras,probabilidades,limite = 10):
    seleccion = random.choices(letras, weights=probabilidades, k=limite)
    return "".join(seleccion)



letras,probabilidades = generarListaParalelas("ABDAACAABACADAABDAADABDAAABDCDCDCDC")
print(letras,probabilidades)
print(simulacion(letras,probabilidades,10))
