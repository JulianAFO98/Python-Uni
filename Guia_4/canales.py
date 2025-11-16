import math

"""
Medio por el que se transmite la información desde la fuente de información al destino. 
La señal se codifica antes de ingresar al canal y se decodifica a la salida del canal.
Un canal puede introducir errores en la transmisión de la información debido a ruido, interferencias u otras
imperfecciones.
P(bj/ai) = probabilidad de que se reciba el símbolo bi dado que se envió el símbolo aj.
Matriz de canal: filas representan los simbolos de salida, columnas los simbolos de entrada.
Como se lee ? Probabilidad de recibir bj dado que se envió ai.
"""
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

"""
Que significado tienen las probabilidades a priori? H(A)
Son las probabilidades de que se envíe cada símbolo de entrada antes de observar cualquier símbolo de salida.
Estas probabilidades reflejan la distribución de probabilidad de los símbolos de entrada en la fuente de información.
Una entropia a priori alta indica una mayor incertidumbre sobre qué símbolo se enviará, mientras que una entropía baja indica
menos incertidumbre.
"""
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

"""
Que son las probabilidades de salida?
Son las probabilidades marginales de recibir cada símbolo de salida, independientemente de qué símbolo de entrada se haya enviado.
Se calculan sumando las probabilidades conjuntas P(ai, bj) sobre todas las posibles entradas ai para cada salida bj.
Estas probabilidades reflejan la distribución de probabilidad de los símbolos de salida en el canal. Es decir,
la probabilidad de observar cada símbolo de salida visto desde la perspectiva del receptor, sin conocimiento previo de qué símbolo de entrada se envió.
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

"""
Que son las probabilidades conjuntas?
Son las probabilidades de que ocurra un par específico de eventos, es decir, la probabilidad de que se envíe
un símbolo de entrada ai y se reciba un símbolo de salida bj simultáneamente.
Basicamente es P(ai,bj) = P(ai) * P(bj/ai)
A mayor cantidad de probabilidad conjunta, mayor es la probabilidad de que ocurra ese par específico de eventos.
"""

def generar_matriz_eventos_simultaneos(probs_priori, matriz_canal):
    matriz_simultaneos = []
    for i in range(len(probs_priori)):
        fila = []
        for j in range(len(matriz_canal[i])):
            fila.append(probs_priori[i] * matriz_canal[i][j])
        matriz_simultaneos.append(fila)
    
    return matriz_simultaneos

"""
Que son las probabilidades a posteriori ?P(ai/bj) = P(ai,bj) / P(bj)
Son las probabilidades condicionales de que se haya enviado un símbolo de entrada ai dado que se ha recibido un símbolo de salida bj.
Estas probabilidades sirven para actualizar lo que creemos sobre cuál fue la entrada después de observar la salida.
A mayor probabilidad a posteriori, mayor es la confianza de que se envió ese símbolo de entrada específico dado el símbolo de salida observado.
Por lo tanto a mayor probabilidad a posteriori, mayor seguridad sobre el símbolo de entrada enviado.
Por eso, es mejor que, para un símbolo de salida dado, alguna probabilidad a posteriori sea alta: indica mayor seguridad al inferir qué símbolo se envió.
"""

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


"""
Entropia a priori H(A)
Que es la entropía a priori?
Es una medida de la incertidumbre asociada a la fuente de información antes de observar cualquier símbolo de salida.
Que significa una entropía a priori alta?
Una entropía a priori alta indica una mayor incertidumbre sobre qué símbolo se enviará, lo que implica que la fuente de información es más impredecible.
Que significa una entropía a priori baja?
Una entropía a priori baja indica menos incertidumbre, lo que implica que la fuente de información es más predecible.
Para que sirve la entropía a priori?
La entropía a priori sirve para cuantificar la cantidad de información promedio que se espera recibir de la fuente de información antes de observar cualquier salida del canal.

Entropía a posteriori H(A|bj)
Que es la entropía a posteriori?
Es una medida de la incertidumbre restante sobre el símbolo de entrada ai después de observar un símbolo de salida específico bj.
Que significa una entropía a posteriori alta?
Una entropía a posteriori alta indica que, incluso después de observar la salida bj, todavía hay mucha incertidumbre sobre qué símbolo de entrada se envió.
Que significa una entropía a posteriori baja?
Una entropía a posteriori baja indica que la observación de la salida bj ha reducido significativamente la incertidumbre sobre el símbolo de entrada enviado.
Para que sirve la entropía a posteriori?
La entropía a posteriori sirve para cuantificar la cantidad de incertidumbre que queda sobre el símbolo de entrada después de observar una salida específica del canal.

Como se interpretan juntas?
La comparación entre la entropía a priori y la entropía a posteriori permite evaluar la eficacia del canal en términos de reducción de incertidumbre.
Un canal eficiente es aquel en el que la entropía a posteriori H(A|B) es significativamente menor que la entropía a priori H(A). Esto indica que la observación del 
símbolo de salida reduce fuertemente la incertidumbre acerca del símbolo de entrada, proporcionando información valiosa sobre lo que fue transmitido.
"""

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

"""
H(A|B) = equivocation o ruido
Que es la equivocación H(A|B)?
Es una medida de la incertidumbre restante sobre el símbolo de entrada A después de observar el símbolo de salida B.
-Mide la información que queda en A después de observar B.
-Pérdida de información sobre A causada por el canal.
-Cantidad de información sobre A que no deja pasar el canal

Que significa una equivocación alta?
Una equivocación alta indica que, incluso después de observar la salida B, todavía hay mucha incertidumbre sobre qué símbolo de entrada se envió.
Que significa una equivocación baja?
Una equivocación baja indica que la observación de la salida B ha reducido significativamente la incertidumbre sobre el símbolo de entrada enviado.
Para que sirve la equivocación?
La equivocación sirve para cuantificar la cantidad de incertidumbre que queda sobre el símbolo de entrada después de observar la salida del canal.

H(B|A) = perdida
Que es la pérdida H(B|A)?
Es una medida de la incertidumbre sobre el símbolo de salida B dado que se conoce el símbolo de entrada A.
Que significa una pérdida alta?
Una pérdida alta indica que, incluso conociendo el símbolo de entrada A, todavía hay mucha incertidumbre sobre qué símbolo de salida se recibirá.
Que significa una pérdida baja?
Una pérdida baja indica que conocer el símbolo de entrada A reduce significativamente la incertidumbre sobre el símbolo de salida recibido.
Para que sirve la pérdida?
La pérdida sirve para cuantificar la cantidad de incertidumbre sobre el símbolo de salida del canal dado que se conoce el símbolo de entrada.
Como se interpretan juntas?
La comparación entre la equivocación H(A|B) y la pérdida H(B|A) permite evaluar la eficacia del canal en términos de transmisión de información.


H(A|B) te dice qué tan difícil es adivinar el input a partir del output.
H(B|A) te dice qué tan impredecible es la salida a partir del input.

"""

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

"""
Que es la entropía afín H(A,B)?
Es una medida de la incertidumbre conjunta sobre los símbolos de entrada A y salida B en un canal de comunicación.
Que significa una entropía afín alta?
Una entropía afín alta indica que hay mucha incertidumbre conjunta sobre los pares de símbolos (A, B), 
lo que implica que el canal introduce una gran cantidad de variabilidad en la transmisión.
Que significa una entropía afín baja?
Una entropía afín baja indica que hay menos incertidumbre conjunta sobre los pares de símbolos (A, B),
lo que implica que el canal es más predecible en su comportamiento.
Para que sirve la entropía afín?
La entropía afín sirve para cuantificar la cantidad total de incertidumbre en el sistema de comunicación,
incluyendo tanto la fuente de información como el canal.
"""

def calcular_entropia_afin(probs_priori, matriz_canal):
    probs_simultaneas = generar_matriz_eventos_simultaneos(probs_priori, matriz_canal)
    entropia_afin = 0
    for i in range(len(probs_simultaneas)):
        for j in range(len(probs_simultaneas[0])):
            entropia_afin+= probs_simultaneas[i][j] * info(probs_simultaneas[i][j])
    print("Entropia Afin: ",entropia_afin)
    return entropia_afin

"""
Que es la información mutua I(A;B)? H(A) - H(A|B)
Es una medida de la cantidad de información que el símbolo de salida B proporciona sobre el símbolo de entrada A en un canal de comunicación.
Es la cantidad de información sobre A, menos la cantidad de información que todavía hay en A después de observar la salida.
-Es la cantidad de información que se obtiene de A gracias al conocimiento de B.
-Es la incertidumbre sobre la entrada del canal que se resuelve observando la salida del canal.
-Es la cantidad de información sobre A que atraviesa el canal.
Que significa una información mutua alta?
Una información mutua alta indica que la salida B proporciona mucha información sobre la entrada A,
lo que implica que el canal es eficiente en la transmisión de información.
Que significa una información mutua baja?
Una información mutua baja indica que la salida B proporciona poca información sobre la entrada A,
lo que implica que el canal introduce mucha incertidumbre en la transmisión.
Para que sirve la información mutua?
La información mutua sirve para cuantificar la eficacia del canal en términos de transmisión de información,
permitiendo evaluar cuánto conocimiento sobre la entrada se puede obtener a partir de la salida observada.
"""

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


def es_sin_ruido(matriz_canal):
    n = len(matriz_canal)
    m = len(matriz_canal[0])
    for j in range(m):
        valores_no_nulos=0
        for i in range(n):
            if(matriz_canal[i][j]!=0):
                valores_no_nulos+=1
            if(valores_no_nulos>1):
                return False
    return True

def es_determinante(matriz_canal):
    n = len(matriz_canal)
    m = len(matriz_canal[0])
    for i in range(n):
        valores_no_nulos=0
        for j in range(m):
            if(matriz_canal[i][j]!=0):
                valores_no_nulos+=1
            if(valores_no_nulos>1):
                return False
    return True

def generar_matriz_compuesta(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Las matrices no se pueden multiplicar: dimensiones incompatibles")

    filas_A = len(A)
    columnas_B = len(B[0])
    columnas_A = len(A[0])  

    resultado = [[0 for _ in range(columnas_B)] for _ in range(filas_A)]

    for i in range(filas_A):
        for j in range(columnas_B):
            for k in range(columnas_A):
                resultado[i][j] += A[i][k] * B[k][j]

    return resultado

def _verificar_proporcionalidad(matriz, col_a, col_b, tol=1e-9):
    k = None  
    for i in range(len(matriz)):
        val_a = matriz[i][col_a]
        val_b = matriz[i][col_b]

        if abs(val_b) > tol:
            current_k = val_a / val_b
            if k is None:
                k = current_k
            elif abs(k - current_k) > tol:
                return False
        elif abs(val_a) > tol:
            return False
    return True

def son_columnas_combinables(matriz, col1, col2):
    TOL = 1e-9
    proporcional_dir1 = _verificar_proporcionalidad(matriz, col1, col2, TOL)
    proporcional_dir2 = _verificar_proporcionalidad(matriz, col2, col1, TOL)
    return proporcional_dir1 or proporcional_dir2

def generar_matriz_determinante(matriz, col1, col2):
    m = len(matriz[0])  # cantidad de columnas de la matriz original
    matriz_determinante = []

    if col1 > col2:
        col1, col2 = col2, col1

    for i in range(m):
        fila = [0] * (m - 1)
        if i == col1:
            fila[col1] = 1
        elif i == col2:
            fila[col1] = 1   
        elif i < col2:
            fila[i] = 1
        else:
            fila[i - 1] = 1
        matriz_determinante.append(fila)

    return matriz_determinante

"""
Realiza todas las reducciones suficientes posibles a la matriz del canal
utilizando las funciones de combinación de columnas.
"""
def generar_matriz_reducida(matriz_de_un_canal):
    matriz_actual = [fila[:] for fila in matriz_de_un_canal]
    while True:
        se_hizo_una_reduccion = False
        num_cols = len(matriz_actual[0])
        
        for i in range(num_cols):
            for j in range(i + 1, num_cols):
                if son_columnas_combinables(matriz_actual, i, j):
                    matriz_D = generar_matriz_determinante(matriz_actual, i, j)
                    matriz_actual = generar_matriz_compuesta(matriz_actual, matriz_D)
                    se_hizo_una_reduccion = True
                    break  
            if se_hizo_una_reduccion:
                break  
        if not se_hizo_una_reduccion:
            break
    return matriz_actual

"""
Un canal es uniforme si cada fila consiste en una permutación arbitraria de los términos de la primera fila. 
"""
def es_canal_uniforme(matriz_canal):
    num_filas = len(matriz_canal)

    primera_fila = sorted(matriz_canal[0])
    for i in range(1, num_filas):
        if sorted(matriz_canal[i]) != primera_fila:
            return False
    return True

def calcular_capacidad_canal(matriz_canal):
    if (es_determinante(matriz_canal)):
        capacidad = math.log2(len(matriz_canal[0]))
    elif(es_sin_ruido(matriz_canal)):
        capacidad = math.log2(len(matriz_canal))
    elif(es_canal_uniforme(matriz_canal)):
        fila = matriz_canal[0]
        entropia = 0
        for p in fila:
            entropia += p * info(p)
        capacidad = math.log2(len(matriz_canal)) - entropia
    print("Capacidad del canal: ",capacidad)
    return capacidad

"""
Realizar una función en Python que reciba como parámetros: 
la matriz de un canal binario y un valor de paso, y estime 
la capacidad del canal mediante el cálculo de la información
 mutua para un conjunto de probabilidades a priori distribuidas 
 uniformemente según el paso especificado. La función debe retornar 
 el valor de capacidad estimado, junto con su probabilidad asociada. 
"""

def estimar_capacidad_canal_binario(matriz_canal, paso):
    capacidades = []
    probabilidades_asociadas = []

    prob_actual = 0.0
    while prob_actual <= 1.0:
        probs_priori = [prob_actual, 1 - prob_actual]
        info_mutua = calcular_informacion_mutua(probs_priori, matriz_canal)
        capacidades.append(info_mutua)
        probabilidades_asociadas.append(probs_priori)
        prob_actual += paso

    capacidad_estimada = max(capacidades)
    indice_max = capacidades.index(capacidad_estimada)
    probabilidad_asociada = probabilidades_asociadas[indice_max]

    print("Capacidad estimada: ",capacidad_estimada)
    print("Probabilidad asociada: ",probabilidad_asociada)
    return capacidad_estimada, probabilidad_asociada

def calcular_probabilidad_error(probs_priori, matriz_canal):
    M = len(matriz_canal) 
    if M == 0:
        return 0.0
    N = len(matriz_canal[0])

    decision_rule = [0] * N 
    
    for j in range(N): 
        max_prob = -1.0
        indice_max = -1
        for i in range(M): 
            prob_actual = matriz_canal[i][j]
            if prob_actual > max_prob:
                max_prob = prob_actual
                indice_max = i
        decision_rule[j] = indice_max
    P_error_dado_x = [0.0] * M
    
    for i in range(M): 
        P_acierto_dado_x = 0.0
        for j in range(N):
            if decision_rule[j] == i:
                P_acierto_dado_x += matriz_canal[i][j]
        P_error_dado_x[i] = 1.0 - P_acierto_dado_x
    probabilidad_error_total = 0.0
    for i in range(M):
        probabilidad_error_total += P_error_dado_x[i] * probs_priori[i]
    return probabilidad_error_total


#print(generar_matriz_canal("abcacaabbcacaabcacaaabcaca","01010110011001000100010011"))

#Punto 3
"""
generar_matriz_canal("1101011001101010010101010100011111","1001111111100011101101010111110110")
print(a_priori("1101011001101010010101010100011111"))
generar_matriz_canal("110101100110101100110101100111110011","110021102110022010220121122100112011")
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
"""

"""

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

#calcular_equivocacion([0.25,0.25,0.25,0.25],[[0,1,0],[0,0,1],[0,1,0],[1,0,0]])
#calcular_informacion_mutua([0.25,0.25,0.25,0.25],[[0,1,0],[0,0,1],[0,1,0],[1,0,0]])

#calcular_equivocacion([1/3,1/3,1/3],[[1,0,0,0],[0,0.2,0,0.8],[0,0,1,0]])
#calcular_informacion_mutua([1/3,1/3,1/3],[[1,0,0,0],[0,0.2,0,0.8],[0,0,1,0]])

#print(es_sin_ruido([[0,1,0],[0,0,1],[0,1,0],[1,0,0]]))
#print(es_sin_ruido([[1,0,0,0],[0,0.2,0,0.8],[0,0,1,0]]))
#print(es_sin_ruido([[0.3,0.5,0.2],[0.2,0.3,0.5],[0.5,0.2,0.3]]))
#print(es_sin_ruido([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]))

#print(es_determinante([[0,1,0],[0,0,1],[0,1,0],[1,0,0]]))
#print(es_determinante([[1,0,0,0],[0,0.2,0,0.8],[0,0,1,0]]))
#print(es_determinante([[0.3,0.5,0.2],[0.2,0.3,0.5],[0.5,0.2,0.3]]))
#print(es_determinante([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]))

#calcular_equivocacion([1/2,1/2],[[0.7,0,0.3,0],[0.2,0.6,0,0.2]])
#calcular_informacion_mutua([1/2,1/2],[[0.7,0,0.3,0],[0.2,0.6,0,0.2]])
"""
matriz_mult = generar_matriz_compuesta(
    [[0.7,0,0.3,0],[0.2,0.6,0,0.2]],
    [[0.9,0,0.1],[0,1,0],[0.1,0.1,0.8],[0,0.5,0.5]]
)
mostrar_matriz_encuadrada(matriz_mult)
calcular_equivocacion([1/2,1/2],matriz_mult)
calcular_informacion_mutua([1/2,1/2],matriz_mult)
"""


#calcular_capacidad_canal([[0.0,1.0,0.0],[0,0,1],[0.0,1,0],[1.0,0.0,0.0]])
#calcular_capacidad_canal([[1,0,0,0],[0,0.2,0,0.8],[0,0,1,0]])
#calcular_capacidad_canal([[0.3,0.5,0.2],[0.2,0.3,0.5],[0.5,0.2,0.3]])
#calcular_capacidad_canal([[0,0,0,1],[1,0,0,0],[0,1,0,0],[0,0,1,0]])

#estimar_capacidad_canal_binario([[0.6,0.4],[0.2,0.8]],0.001)
#estimar_capacidad_canal_binario([[0.25,0.75],[0.9,0.1]],0.001)
#estimar_capacidad_canal_binario([[0.51,0.49],[0.72,0.28]],0.001)
#estimar_capacidad_canal_binario([[0.77,0.23],[0.2,0.8]],0.0001)
"""

matriz_ejemplo = [[0.6, 0.3,0.1], [0.1, 0.8,0.1],[0.3,0.3,0.4]]
probs_priori_uniforme = [4/15, 3/15, 8/15]

prob_error_calculada = calcular_probabilidad_error(probs_priori_uniforme, matriz_ejemplo)
print("Probabilidad de error calculada:", prob_error_calculada)
"""