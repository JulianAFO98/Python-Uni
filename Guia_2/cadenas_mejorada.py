
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

def acumularProbabilidades(probabilidades):
    acumuladas = []
    total = 0
    for p in probabilidades:
        total += p
        acumuladas.append(total)
    return acumuladas

def simulacion(letras,probabilidades,len = 10):
    probabilidadesAcum = acumularProbabilidades(probabilidades)
    for _ in range(len):
        valAnterior = 0
        randomNum = random.random()
        for index,p in enumerate(probabilidadesAcum):
            if valAnterior<=randomNum and randomNum<p:
                indexLetra = index
            valAnterior = p
        print(letras[indexLetra])
