"""
Codificar funciones en Python que resuelvan los siguiente:
a. Dada una cadena de caracteres que representa un mensaje emitido por una fuente,
devolver una lista con su alfabeto y su matriz de transición.
b. Dada una lista que contenga el alfabeto de una fuente y su matriz de transición,
simular la generación de una cadena de caracteres emitida por esa fuente.
c. Dada una matriz de transición y una tolerancia máxima, determinar si se trata de
una fuente de memoria nula o una fuente con memoria
"""
import random
import entropia_markov_estacionario
def obtener_alfabeto_y_matriz_transicion(cadena):
    alfabeto = []
    cantidad_apariciones_alfabeto = []
    for i in cadena:
        if i not in alfabeto:
            alfabeto.append(i)
            cantidad_apariciones_alfabeto.append(1)
        else:
            index_letra = alfabeto.index(i)
            cantidad_apariciones_alfabeto[index_letra]+=1
    n = len(alfabeto)
    matriz = [[0]*n for _ in range(n)]
    for i in range(len(cadena)):
        if i==0:
            continue
        index_letra = alfabeto.index(cadena[i])
        index_letra_anterior = alfabeto.index(cadena[i-1])
        matriz[index_letra][index_letra_anterior] +=1
    
    for i in range(n):
        suma_columna = sum(matriz[j][i] for j in range(n))
        if suma_columna != 0:
            for j in range(n):
                matriz[j][i] /= suma_columna
    return alfabeto,matriz

def mostrar_matriz(matriz):
    for i in range(len(matriz)):
        print(matriz[i])


def simulacion_markov(alfabeto, matriz, largo):

    posibles_iniciales = [i for i, fila in enumerate(matriz) if sum(fila) > 0]
    simbolo_actual = alfabeto[random.choice(posibles_iniciales)]
    
    cadena = simbolo_actual
    
    while len(cadena) < largo:
        idx = alfabeto.index(simbolo_actual)
        probabilidades = matriz[idx]
        
        if sum(probabilidades) == 0:

            simbolo_actual = alfabeto[random.choice(posibles_iniciales)]
        else:
            simbolo_actual = random.choices(alfabeto, weights=probabilidades, k=1)[0]
        
        cadena += simbolo_actual
        
    return cadena

def es_fuente_de_memoria_nula(matriz,tolerancia=0.1):
    for i in range(len(matriz)):
        maximo = max(matriz[i])
        minimo = min(matriz[i])
        if maximo-minimo>tolerancia:
            return False
    return True

"""
alfabeto,matriz = obtener_alfabeto_y_matriz_transicion("hola mundo")
print(simulacion_markov(alfabeto,matriz,15))
matriz = [[0.46,0.43,0.44],
          [0.23,0.29,0.22],
          [0.31,0.29,0.33]]
print(es_fuente_de_memoria_nula(matriz))
matriz = [[0.58,0.43,0.3],
          [0.17,0.43,0.1],
          [0.25,0.14,0.6]]
print(es_fuente_de_memoria_nula(matriz))
"""


#16
#CAAACCAABAACBBCABACCAAABCBBACC
alfabeto,matriz = obtener_alfabeto_y_matriz_transicion("CAAACCAABAACBBCABACCAAABCBBACC")
print(es_fuente_de_memoria_nula(matriz))
vector_estacionario = entropia_markov_estacionario.generar_vector_estacionario(matriz,0.01)
print(entropia_markov_estacionario.calcular_entropia_fuente(matriz,vector_estacionario))

#BBAAACCAAABCCCAACCCBBACCAABBAA
alfabeto,matriz = obtener_alfabeto_y_matriz_transicion("BBAAACCAAABCCCAACCCBBACCAABBAA")
print(es_fuente_de_memoria_nula(matriz))
vector_estacionario = entropia_markov_estacionario.generar_vector_estacionario(matriz,0.01)
print(entropia_markov_estacionario.calcular_entropia_fuente(matriz,vector_estacionario))




 