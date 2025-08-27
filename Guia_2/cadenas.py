
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
    valAnterior = 0
    for i in range(len(probabilidades)):
        probabilidades[i]+=valAnterior
        valAnterior=probabilidades[i]
    return probabilidades

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
letras,probabilidades = generarListaParalelas("alado")
print(letras)
print(probabilidades)
simulacion(letras,probabilidades)