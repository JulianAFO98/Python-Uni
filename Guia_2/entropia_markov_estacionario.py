import math

def verificar_error(v1,v2,tol):
    for a, b in zip(v1, v2):
        if abs(a - b) > tol:
            return True
    return False

def generar_nuevo_vector_ideal(matriz,vector):
    nuevo_vector = []
    for i in range(len(matriz)):
        suma = 0
        for j in range(len(matriz[i])):
            suma += matriz[i][j] * vector[j]
        nuevo_vector.append(suma)
    return nuevo_vector

def generar_vector_estacionario(matriz,tol):
    valores_ideales = [1/len(matriz)] * len(matriz)
    nuevo_vector_ideal = [2] * len(matriz) #caso imposible que de perfecto
    
    while(verificar_error(valores_ideales,nuevo_vector_ideal,tol)):
        valores_ideales = nuevo_vector_ideal
        nuevo_vector_ideal = generar_nuevo_vector_ideal(matriz,valores_ideales)
        total = sum(nuevo_vector_ideal)
        if total != 0:
            nuevo_vector_ideal = [x / total for x in nuevo_vector_ideal]
   
    
    return nuevo_vector_ideal

def calcular_entropia_fuente(matriz,vector_estacionario):
    vector_entropias = []
    h=0
    for i in range(len(matriz)):
        suma = 0
        for j in range(len(matriz[i])):
            if matriz[j][i] != 0:
                suma+= matriz[j][i] * math.log2(matriz[j][i])
        vector_entropias.append(suma * -1)
    for a, b in zip(vector_estacionario, vector_entropias):
        h+= a*b
    return h




#17
matrizb= [[1/2,0,0,1/2],
          [1/2,0,0,0],
          [0,1/2,0,0],
          [0,1/2,1,1/2]]
vector_estacionario = generar_vector_estacionario(matrizb,0.01)
print(vector_estacionario)
print(calcular_entropia_fuente(matrizb,vector_estacionario))

matrizc= [[1/3,0,1,1/2,0],
          [1/3,0,0,0,0],
          [0,1,0,0,0],
          [1/3,0,0,0,1/2],
          [0,0,0,1/2,1/2]]
vector_estacionario = generar_vector_estacionario(matrizc,0.01)
print(vector_estacionario)
print(calcular_entropia_fuente(matrizc,vector_estacionario))