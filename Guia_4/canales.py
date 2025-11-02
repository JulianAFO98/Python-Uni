import math

def generar_matriz_canal(cadena_sin_codificar,cadena_salida):
    lista_letras = []
    cantidad_elementos = len(cadena_sin_codificar)
    for c in cadena_sin_codificar:
        if c not in lista_letras:
            lista_letras.append(c)
    lista_letras = sorted(lista_letras)

    lista_letras_salida = []
    for c in cadena_salida:
        if c not in lista_letras_salida:
            lista_letras_salida.append(c)
    lista_letras_salida = sorted(lista_letras_salida)

    matriz = [[0 for _ in range(len(lista_letras_salida))]  for _ in range(len(lista_letras))]

    for i in range(cantidad_elementos):
        indexi = lista_letras.index(cadena_sin_codificar[i])
        indexj = lista_letras_salida.index(cadena_salida[i])
        matriz[indexi][indexj]+=1
    
    for i in range(len(matriz)):
        fila_sum = sum(matriz[i])
        if fila_sum != 0:  # evitar división por cero
            matriz[i] = [round(x / fila_sum,3) for x in matriz[i]]

       
    for c in lista_letras_salida:
        print(f"{c:>6}", end="")  # ancho fijo de 6 espacios
    print()

# Imprimir filas con índice a la izquierda
    for i, fila in enumerate(matriz):
        print(f"{lista_letras[i]:>2}", end=" ")  # letra de entrada
        for x in fila:
            print(f"{x:6.3f}", end="")  # 3 decimales, ancho fijo
        print()



    return matriz


def a_priori(cadena):
    total = len(cadena)
    contador = {}

    # Contar ocurrencias de cada carácter
    for c in cadena:
        contador[c] = contador.get(c, 0) + 1

    # Calcular probabilidades ordenadas por carácter
    probabilidades = [contador[c] / total for c in sorted(contador)]

    return probabilidades

#La lista de probs priori es paralela a las filas de la matriz(hacia abajo)
"""
l   1   2   3
a   x   x   x
b   y   y   y
c   z   z   z
"""
#retorna una lista paralela a las columnas, con las probabilidades
"""
   1   2   3
   x   x   x
   y   y   y
   z   z   z
l  p1  p2  p3 
"""
def generar_probs_salida(probs_priori, matriz_canal):
    num_salidas = len(matriz_canal[0])  # cantidad de columnas
    lista_salida = [0 for _ in range(num_salidas)]
    
    for j in range(num_salidas):  # recorro cada salida
        sum_prob = 0
        for i in range(len(probs_priori)):  # recorro cada entrada
            sum_prob += probs_priori[i] * matriz_canal[i][j]
        lista_salida[j] = round(sum_prob, 3)
    
    return lista_salida

def generar_matriz_eventos_simultaneos(probs_priori, matriz_canal):
    matriz_simultaneos = []
    for i in range(len(probs_priori)):
        fila = []
        for j in range(len(matriz_canal[i])):
            fila.append(probs_priori[i] * matriz_canal[i][j])
        matriz_simultaneos.append(fila)
    
    return matriz_simultaneos

def generar_matriz_posteriori(probs_priori,matriz_canal):
    probs_salida = generar_probs_salida(probs_priori,matriz_canal)
    matriz_simultaneos = generar_matriz_eventos_simultaneos(probs_priori,matriz_canal)
    matriz_posteriori = []
    for i in range(len(matriz_canal)):
        fila = []
        for j in range(len(matriz_canal[i])):
            fila.append(matriz_simultaneos[i][j]/probs_salida[j] if probs_salida[j] != 0 else 0) 
        matriz_posteriori.append(fila)
    return matriz_posteriori

def mostrar_matriz_encuadrada(matriz, etiquetas_filas=None, etiquetas_columnas=None):
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0

    # Si no se pasan etiquetas, se usan índices
    if etiquetas_filas is None:
        etiquetas_filas = [str(i) for i in range(filas)]
    if etiquetas_columnas is None:
        etiquetas_columnas = [str(j) for j in range(columnas)]

    # Mostrar encabezado de columnas
    print("     ", end="")
    for col in etiquetas_columnas:
        print(f"{col:8}", end="")
    print("\n" + "    " + "--------" * columnas)

    # Mostrar cada fila con su etiqueta
    for i, fila in enumerate(matriz):
        print(f"{etiquetas_filas[i]:4} |", end="")
        for valor in fila:
            print(f"{valor:8.4f}", end="")
        print()

def info(num):
    return -math.log2(num)  if num !=0 else 0



def calcular_entropia_salida(probs_priori, matriz_canal):
    probs_priori = generar_probs_salida(probs_priori,matriz_canal)
    entropia_salida = 0
    for i in range(len(probs_priori)):
        entropia_salida += probs_priori[i]*info(probs_priori[i])
    print("Entropia de salida",round(entropia_salida,3))
    return round(entropia_salida,3)

def lista_entropias(probs_priori, matriz_canal):
    entropia_priori = 0
    lista_entropia_posteriori = []
    matriz_posteriori = generar_matriz_posteriori(probs_priori, matriz_canal)

    # Recorrer columnas (cada y_j)
    for j in range(len(matriz_posteriori[0])):  
        entropia = 0
        for i in range(len(matriz_posteriori)):  # recorrer filas (x_i)
            entropia += matriz_posteriori[i][j] * info(matriz_posteriori[i][j])
        lista_entropia_posteriori.append(round(entropia, 3))

    # Entropía a priori
    for i in range(len(probs_priori)):
        entropia_priori += probs_priori[i] * info(probs_priori[i])

    return round(entropia_priori, 3), lista_entropia_posteriori

def calcular_equivocacion(probs_priori, matriz_canal):
    # probs_priori = [P(a1), P(a2), ...]
    # matriz_canal = [[P(b1|a1), P(b2|a1), ...],
    #                 [P(b1|a2), P(b2|a2), ...], ...]

    entro_priori, entropia_post = lista_entropias(probs_priori, matriz_canal)
    probs_simultaneas = generar_matriz_eventos_simultaneos(probs_priori, matriz_canal)

    # Calcular P(b) sumando columnas de P(a,b)
    probs_b = [sum(col) for col in zip(*probs_simultaneas)]

    # H(A|B) = sum_b P(b) * H(A|b)
    H_A_dado_B = sum(pb * h for pb, h in zip(probs_b, entropia_post))

    # H(B|A) = sum_a P(a) * H(B|a)
    H_B_dado_A = 0
    for pa, fila in zip(probs_priori, matriz_canal):
        H_B_a = -sum(pba * math.log(pba, 2) for pba in fila if pba > 0)
        H_B_dado_A += pa * H_B_a

    
    print(f"H(A|B) (equivocacion o ruido): {H_A_dado_B:.4f}")
    print(f"H(B|A) (perdida): {H_B_dado_A:.4f}")

    
    return H_A_dado_B, H_B_dado_A # H(A|B) H(B|A)

def calcular_entropia_afin(probs_priori, matriz_canal):
    probs_simultaneas = generar_matriz_eventos_simultaneos(probs_priori, matriz_canal)
    entropia_afin = 0
    for i in range(len(probs_simultaneas)):
        for j in range(len(probs_simultaneas[0])):
            entropia_afin+= probs_simultaneas[i][j] * info(probs_simultaneas[i][j])
    print("Entropia Afin: ",entropia_afin)
    return entropia_afin

def calcular_informacion_mutua(probs_priori, matriz_canal):
    # probs_simultaneas[i][j] = P(A=i, B=j)
    probs_simultaneas = generar_matriz_eventos_simultaneos(probs_priori, matriz_canal)
    
    n = len(probs_simultaneas)
    m = len(probs_simultaneas[0])
    
    # Probabilidades marginales
    P_A = [sum(probs_simultaneas[i][j] for j in range(m)) for i in range(n)]
    P_B = [sum(probs_simultaneas[i][j] for i in range(n)) for j in range(m)]
    
    # Informacion mutua
    info_mutua = 0
    for i in range(n):
        for j in range(m):
            if probs_simultaneas[i][j] > 0: 
                info_mutua += probs_simultaneas[i][j] * math.log2(probs_simultaneas[i][j] / (P_A[i] * P_B[j]))
    print("Informacion mutua: ",info_mutua)
    return info_mutua



#print(generar_matriz_canal("abcacaabbcacaabcacaaabcaca","01010110011001000100010011"))

#Punto 3
"""
print(generar_matriz_canal("1101011001101010010101010100011111","1001111111100011101101010111110110"))
print(a_priori("1101011001101010010101010100011111"))
print(generar_matriz_canal("110101100110101100110101100111110011","110021102110022010220121122100112011"))
print(a_priori("110101100110101100110101100111110011"))

"""
"""
print(generar_probs_salida([0.3,0.3,0.4],[[0.4,0.4,0.2],
                                          [0.3,0.2,0.5],
                                          [0.3,0.4,0.3]]))
mat_eventos = generar_matriz_eventos_simultaneos([0.3,0.3,0.4],[[0.4,0.4,0.2],
                                                                [0.3,0.2,0.5],
                                                                [0.3,0.4,0.3]])
mostrar_matriz_encuadrada(mat_eventos)

mat_posteriori = generar_matriz_posteriori([0.3,0.3,0.4],[[0.4,0.4,0.2],
                                                          [0.3,0.2,0.5],
                                                          [0.3,0.4,0.3]])

mostrar_matriz_encuadrada(mat_posteriori)
"""
"""

mat_canal = generar_matriz_canal("110101100110101100110101100111110011","110021102110022010220121122100112011")
mat_posteriori = generar_matriz_posteriori(a_priori("110101100110101100110101100111110011"),mat_canal)
mat_simultaneos = generar_matriz_eventos_simultaneos(a_priori("110101100110101100110101100111110011"),mat_canal)
mostrar_matriz_encuadrada(mat_posteriori)
mostrar_matriz_encuadrada(mat_simultaneos)


"""
"""

mat_canal = generar_matriz_canal("abcacaabbcacaabcacaaabcaca","01010110011001000100010011")
entropia_priori,entropia_posteriori = lista_entropias(a_priori("abcacaabbcacaabcacaaabcaca"),mat_canal)

print(entropia_priori)
print(entropia_posteriori)
mat_canal = generar_matriz_canal("1101011001101010010101010100011111","1001111111100011101101010111110110")
entropia_priori,entropia_posteriori = lista_entropias(a_priori("1101011001101010010101010100011111"),mat_canal)

print(entropia_priori)
print(entropia_posteriori)

mat_canal = generar_matriz_canal("110101100110101100110101100111110011","110021102110022010220121122100112011")
entropia_priori,entropia_posteriori = lista_entropias(a_priori("110101100110101100110101100111110011"),mat_canal)

print(entropia_priori)
print(entropia_posteriori)
entropia_priori,entropia_posteriori = lista_entropias([0.3,0.3,0.4],[[0.4,0.4,0.2],[0.3,0.2,0.5],[0.3,0.4,0.3]])

print(entropia_priori)
print(entropia_posteriori)
"""
"""
entropia_priori,entropia_posteriori = lista_entropias([0.14,0.52,0.34],[[0.5,0.3,0.2],[0,0.4,0.6],[0.2,0.8,0]])
entropia_priori,entropia_posteriori = lista_entropias([0.25,0.25,0.5],[[0.25,0.25,0.25,0.25],[0.25,0.25,0,0.5],[0.5,0,0.5,0]])
entropia_priori,entropia_posteriori = lista_entropias([0.12,0.24,0.14,0.5],[[0.25,0.15,0.3,0.3],[0.23,0.27,0.25,0.25],[0.1,0.4,0.25,0.25],[0.34,0.26,0.2,0.2]])


print(entropia_priori)
print(entropia_posteriori)

"""

entro_priori,entro_posteriori = lista_entropias([0.14,0.52,0.34],[[0.5,0.3,0.2],[0,0.4,0.6],[0.2,0.8,0]])
print(entro_priori)
calcular_entropia_salida([0.14,0.52,0.34],[[0.5,0.3,0.2],[0,0.4,0.6],[0.2,0.8,0]])
calcular_equivocacion([0.14,0.52,0.34],[[0.5,0.3,0.2],[0,0.4,0.6],[0.2,0.8,0]])
calcular_entropia_afin([0.14,0.52,0.34],[[0.5,0.3,0.2],[0,0.4,0.6],[0.2,0.8,0]])
calcular_informacion_mutua([0.14,0.52,0.34],[[0.5,0.3,0.2],[0,0.4,0.6],[0.2,0.8,0]])