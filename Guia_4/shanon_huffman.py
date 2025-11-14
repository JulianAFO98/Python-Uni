
import math
from operator import itemgetter

def info(val,base): 
    if val == 0:
        return 0
    return -math.log(val,base)

def generarListaInfo(lista,base):
    return [info(val,base) for val in lista]


def generar_lista_longitudes(palabras):
    lista_longitudes = [len(palabra) for palabra in palabras]
    return lista_longitudes


def calcular_longitud_media_codigo(palabras_codigo,probabilidades):
    lista_longitudes = generar_lista_longitudes(palabras_codigo)
    return sum(probabilidades[i] * lista_longitudes[i] for i in range(len(palabras_codigo)))

def obtener_cadena_alfabeto_codigo(palabras):
    cadena = ""
    for palabra in palabras:
        for letra in palabra:
            if letra not in cadena:
                cadena += letra
    return cadena

def calcular_entropia_fuente_codigo(palabras_codigo,probabilidades):
    simbolos_distintos = obtener_cadena_alfabeto_codigo(palabras_codigo)
    base = len(simbolos_distintos)
    return sum(p * info(p,base) for p in probabilidades)

def generarListaExtension(alfabeto, probs, grado):
    cantFilas = len(alfabeto) ** grado
    listaExtension = ["" for _ in range(cantFilas)]
    listaExtensionProb = [1 for _ in range(cantFilas)]
    
    for i in range(grado):  # los n símbolos
        tamanioParticion = len(alfabeto) ** (grado - (i + 1))
        for j in range(cantFilas):  # iterar sobre todas las filas
            elemIndex = (j // tamanioParticion) % len(alfabeto)
            listaExtension[j] += alfabeto[elemIndex]
            listaExtensionProb[j] *= probs[elemIndex]
    
    # redondear probabilidades a 2 decimales
    listaExtensionProb = [round(p, 2) for p in listaExtensionProb]
    
    return listaExtension, listaExtensionProb


"""
Para verificar el teorema de shannon se  parte de las probabilidades de la fuente original y las palabras del código (debe ser un código
para la fuente original). Se genera la extensión de grado n de la fuente y se calcula la entropia r y la longitud media del código
para la extensión. Luego se verifica que se cumpla la desigualdad H_r(S) <= L_n/n < H_r(S) + 1/n
donde H_r(S) es la entropia de la fuente en base r (r es la cantidad de símbolos distintos en el alfabeto del codigo) y 
L_n es la longitud media del código para la extensión de grado n.

Conclusion: Si se cumple la desigualdad para la extensión de grado n, entonces el código cumple el primer teorema de Shannon, siendo este 
un codigo codigo optimo para la fuente original y sin ruido.
"""

def cumple_primer_teorema_shannon(probs_fuente, palabras_codigo, n):

    listaExtension,probsExtension = generarListaExtension(palabras_codigo, probs_fuente, n)
    L_n = calcular_longitud_media_codigo(listaExtension, probsExtension)
    print("Longitud ",L_n)
    H_r_S = calcular_entropia_fuente_codigo(listaExtension, probsExtension)/n
    print("Entropia r ",H_r_S)
    return (H_r_S) <= (L_n/n)  and  (L_n/n)  < ((H_r_S) + (1 / n))


"""
 Como obtener la redundancia y eficiencia de un código dado las probabilidades de la
 fuente y las palabras del código.
 Redundancia R = 1 - (H / L) siendo H la entropía de la fuente y L la longitud media del codigo.
 Eficiencia = H / L siendo H la entropía de la fuente y L la longitud media del codigo.
 Que es la entropia de la fuente?
    La entropía de la fuente es una medida de la incertidumbre o la cantidad promedio de informacion 
    que provee cada símbolo emitido por la fuente.
 Conclusion o significado de los valores:
 - Si la redundancia es 0, el código es óptimo (eficiencia 1).
 - Si la redundancia es mayor que 0, el código no es tan optimo (eficiencia menor que 1).
 - Si la eficiencia es 1, el código es óptimo (redundancia 0).
 - Si la eficiencia es menor que 1, el código no es tan optimo (redundancia mayor que 0).
 Estas medidas son utiles para evaluar la calidad del codigo en terminos de su capacidad 
 para representar la informacion de manera eficiente.
"""
def calcularRedundanciaYEficiencia(probs_extension, palabras_codigo):
    """
    probs_extension: lista de probabilidades de cada palabra (bloque) en la extensión
    palabras_codigo: lista de longitudes o códigos asociados a cada palabra
    """
    # Longitud media del código
    L = calcular_longitud_media_codigo(palabras_codigo, probs_extension)
    
    # Entropía de la fuente
    H = calcular_entropia_fuente_codigo(palabras_codigo, probs_extension)
    
    # Redundancia y eficiencia
    eficiencia = H / L if L != 0 else 0
    R = 1 - eficiencia
    return round(R,4), round(eficiencia,4)


def generarListaParalelasCadenaCaracteresYProbs(cadena):
    contApariciones = []
    letras = []
    for i in range(len(cadena)):
        if cadena[i] not in letras:
            letras.append(cadena[i])
            contApariciones.append(1)
        else:
            index = letras.index(cadena[i])
            contApariciones[index]+=1
    
    probabilidades = [round(val/len(cadena),10) for val in contApariciones]
    return letras,probabilidades

"""
Algoritmo de Huffman para generar el código óptimo basado en las probabilidades de los símbolos.
Que hace el algoritmo?
Construye un árbol binario donde los símbolos con mayor probabilidad tienen códigos más cortos,
y los símbolos con menor probabilidad tienen códigos más largos.
Es mas eficiente que otros métodos de codificación, como el código de Shannon-Fano,
ya que siempre produce un código óptimo.
"""
def algoritmo_huffman(probs):
    items = [[p, [i]] for i, p in enumerate(probs)]
    tabla_huffman = [""]*len(probs)
    while len(items) > 1:
        items = sorted(items, key=itemgetter(0),reverse=True)
        ultimoElemento = items.pop()
        penultimoElemento = items.pop()
        for indice in ultimoElemento[1]:
            tabla_huffman[indice] = "1" + tabla_huffman[indice]
        for indice in penultimoElemento[1]:
            tabla_huffman[indice] = "0" + tabla_huffman[indice]
        nuevoElemento = [ultimoElemento[0] + penultimoElemento[0], ultimoElemento[1] + penultimoElemento[1]]
        items.append(nuevoElemento)

    print("Tabla huffman final ",tabla_huffman)
    return tabla_huffman


def shanon_fano_recursivo(items,tabla_shanon_fano):
    if len(items) > 1:
        items = sorted(items, key=itemgetter(0),reverse=True) #ordeno de mayor a menor
        total = sum(item[0] for item in items) #sumo probabilidades
        acum = 0 #acumulador de probabilidades
        index_seccionado = 0 #indice donde se secciona la tabla
        for i, item in enumerate(items): #busco el indice donde secciono
            acum += item[0] 
            if acum >= total / 2: #si el acumulado es mayor o igual a la mitad del total
                if(i > 0 and (total/2 - (acum - item[0])) < (acum - total/2)):
                    index_seccionado = i
                else:
                    index_seccionado = i + 1
                break
        for indice in items[:index_seccionado]: #agrego 0 y 1 a los codigos basandome en la seccion
            for idx in indice[1]:
                tabla_shanon_fano[idx] += "0"
        for indice in items[index_seccionado:]:
            for idx in indice[1]:
                tabla_shanon_fano[idx] += "1"
        shanon_fano_recursivo(items[:index_seccionado],tabla_shanon_fano)
        shanon_fano_recursivo(items[index_seccionado:],tabla_shanon_fano)


"""
Algoritmo de Shannon-Fano para generar el código basado en las probabilidades de los simbolos.
Que hace el algoritmo?
Construye un árbol binario dividiendo recursivamente la lista de símbolos en dos partes
de manera que las probabilidades de ambas partes sean lo más equilibradas posible.
Es menos eficiente que el algoritmo de Huffman, ya que no siempre produce un código óptimo.
"""

def algoritmo_shanon_fano(probs):
    items = [[p, [i]] for i, p in enumerate(probs)]
    tabla_shanon_fano = [""]*len(probs)
    shanon_fano_recursivo(items,tabla_shanon_fano)
    print("Tabla shanon fano final ",tabla_shanon_fano)
    return tabla_shanon_fano

def codificar_en_byteArray(mensaje_a_codificar, alfabeto_fuente, lista_cadena_caracteres):
    relacion = {alfabeto_fuente[i]: lista_cadena_caracteres[i] for i in range(len(alfabeto_fuente))}

    cuerpo = ""
    for c in mensaje_a_codificar:
        if c in relacion:
            cuerpo += relacion[c]
        else:
            raise ValueError(f"El caracter '{c}' no está en el alfabeto fuente.")
    ceros_relleno = ( - (3 + len(cuerpo)) ) % 8 
   
   # Añadir  ceros al final del cuerpo
    cuerpo_padded = cuerpo + ("0" * ceros_relleno)
    # Encabezado de 3 bits con la cantidad de ceros
    encabezado = f"{ceros_relleno:03b}"
    cadena_final_bits = encabezado + cuerpo_padded
    # Ahora la longitud debe ser múltiplo de 8; convertir a bytearray

    if len(cadena_final_bits) % 8 != 0:
        raise RuntimeError("Longitud inesperada, no múltiplo de 8.")
    
    byte_array = bytearray(int(cadena_final_bits[i:i+8], 2) for i in range(0, len(cadena_final_bits), 8))
    cadena_bits = "".join(f"{b:08b}" for b in byte_array)
    return cadena_bits, byte_array


def decodificar_de_byteArray(cadena_bits_byteArray, alfabeto_fuente, alfabeto_codigo):
    if len(cadena_bits_byteArray) < 3:
        raise ValueError("Entrada demasiado corta para contener el encabezado.")
    ceros_relleno = int(cadena_bits_byteArray[:3], 2)
    cuerpo_bits = cadena_bits_byteArray[3:]
    if ceros_relleno:
        if ceros_relleno > len(cuerpo_bits):
            raise ValueError("Número de ceros de relleno inválido.")
        cuerpo_bits = cuerpo_bits[:-ceros_relleno]
    codigo_a_simbolo = {alfabeto_codigo[i]: alfabeto_fuente[i] for i in range(len(alfabeto_fuente))}
    # Decodificar
    cadena_decodificada = ""
    buffer = ""
    for bit in cuerpo_bits:
        buffer += bit
        if buffer in codigo_a_simbolo:
            cadena_decodificada += codigo_a_simbolo[buffer]
            buffer = ""
    # Si quedó buffer no vacío significa que los códigos no forman una partición válida
    if buffer != "":
        raise ValueError("Secuencia de bits restante no coincide con ningún código (buffer no vacío).")
    return cadena_decodificada



def codificar_usando_RCL(cadena):
    if not cadena:
        return bytearray()

    tabla_letras = []
    tabla_cantidad_apariciones = []

    char_anterior = cadena[0]
    cantidad = 1

    for i in range(1, len(cadena)):
        char_actual = cadena[i]

        if char_actual == char_anterior and cantidad < 255:
            cantidad += 1
        else:
            tabla_letras.append(char_anterior)
            tabla_cantidad_apariciones.append(cantidad)
            char_anterior = char_actual
            cantidad = 1

    tabla_letras.append(char_anterior)
    tabla_cantidad_apariciones.append(cantidad)

    print("Tabla letras:", tabla_letras)
    print("Tabla apariciones:", tabla_cantidad_apariciones)

    # crear el bytearray
    bytearray_cadena = bytearray()
    for letra, cantidad in zip(tabla_letras, tabla_cantidad_apariciones):
        bytearray_cadena.append(ord(letra))
        bytearray_cadena.append(cantidad)

    return bytearray_cadena


def calcular_comprension(cadena_alfabeto_fuente,byte_array):
    compresion = -1
    # Calcular el tamaño original en bits
    tamaño_original_bits = len(cadena_alfabeto_fuente) * 8  # Asumiendo 1 byte (8 bits) por carácter
    
    # Calcular el tamaño comprimido en bits
    tamaño_comprimido_bits = len(byte_array) * 8  # Cada byte tiene 8 bits
    
    # Calcular la compresión
    if tamaño_comprimido_bits != 0:
        compresion = tamaño_original_bits / tamaño_comprimido_bits
    print("La compresion es de: ",compresion," veces")
    return round(compresion,4)   

"""
Objetivos de la compresion de un archivo:
- Reducir el tamaño del archivo para ahorrar espacio de almacenamiento.
- Disminuir el tiempo de transferencia al enviar archivos a través de redes.
- Mejorar la eficiencia en la gestión de datos.
- Facilitar la transmisión de datos en entornos con ancho de banda limitado.
- Optimizar el rendimiento de aplicaciones que manejan grandes volúmenes de datos.
"""

"""
Metodos de compresion sin perdida:
Mantienen la integridad de la información (datos descomprimidos iguales a los datos originales). 
Usados para textos, base de datos, código fuente, imágenes críticas, etc.
La long. media de código es mayor o igual a la entropía : H <= L
Estatico:  -Requiere una sola pasada por los datos para codificar
           -La distribución de probabilidades es fija, puede diferir de los datos a codificar.
           -No se debe transmitir/almacenar la distribución de probabilidades al decodificador.
Semi-estatico:  -Requiere dos pasadas por los datos (una para analizar, otra para codificar).
                -La distribución de probabilidades se basa en los datos a codificar.
                - Se debe transmitir/almacenar la distribución de probabilidades al decodificador.
Dinamico:     -Requiere una sola pasada por los datos para codificar.
              -La distribución de probabilidades se actualiza dinámicamente durante la codificación.
              - No se debe transmitir/almacenar la distribución de probabilidades al decodificador.
              -Algoritmos mas complejos y lentos.

            
Los modelos estáticos y semi estáticos usan una única tabla de probabilidades y 
son del tipo Huffman. Serán estáticos si la distribución de probabilidades es
impuesta desde el exterior (por ejemplo la cantidad de e's en el alfabeto hispano,probabilidad ya conocida)
 y semi estática si dependen de los datos a comprimir.

Huffman no alcanza generalmente el limite H(S) porque no se permiten bits fraccionales ,
necesita al menos un bit por símbolo. 

Methodos de compresion con perdida:
Eliminan datos considerados menos importantes, lo que puede resultar en una pérdida de calidad.
Usados en imágenes, video, sonido (jpeg, mpeg, mp3, entre otros).
No tienen como límite la entropía: L<H

Los métodos de compresión con pérdida buscan comprimir pensando en la función del archivo a comprimir.
Por ejemplo si pretendemos comprimir imágenes o videos,
tratan de reducir la imágenes a zonas de color similar tomando una tolerancia y
juegan con la capacidad de diferenciación del ojo humano. Cuando se trata de sonido se 
refieren a la sensibilidad del oído humano. 
"""


"""
Distancia de Hamming entre palabras de código:
La distancia de Hamming entre dos palabras de codigo es el número de posiciones en las que difieren.
Es una medida de cuon diferentes son dos palabras de código.
La distancia minima de Hamming en un conjunto de palabras de código es la menor distancia de Hamming
entre cualquier par de palabras en el conjunto.
La distancia mínima de Hamming es importante porque determina la capacidad del codigo para detectar y corregir errores.
- Cantidad de errores detectables: Un código con distancia mínima d puede detectar hasta d-1 errores.
- Cantidad de errores corregibles: Un código con distancia mínima d puede corregir hasta (d-1)/2 errores.   
"""

def hamming(lista_palabras_codigo):
    distancias = []
    for i in range(len(lista_palabras_codigo)):
        for j in range(i + 1, len(lista_palabras_codigo)):
            palabra1 = lista_palabras_codigo[i]
            palabra2 = lista_palabras_codigo[j]
            # Asegurarse de que ambas palabras tengan la misma longitud
            if len(palabra1) != len(palabra2):
                raise ValueError("Las palabras deben tener la misma longitud para calcular la distancia de Hamming.")
            # Calcular la distancia de Hamming
            distancia = sum(c1 != c2 for c1, c2 in zip(palabra1, palabra2))
            distancias.append(distancia)
    # Calcular la distancia mínima, cantidad de errores detectables y corregibles
    distancia_minima = min(distancias) if distancias else 0
    cantidad_errores_detectables = distancia_minima - 1 if distancia_minima > 0 else 0
    cantidad_errores_correjibles = (distancia_minima - 1) // 2 if distancia_minima > 0 else 0

    return distancia_minima,cantidad_errores_detectables,cantidad_errores_correjibles

#tipo paridad -> 0 para par (default), 1 para paridad impar
def devolver_byte_con_paridad(byte,tipoParidad = 0):
    byte = ord(byte)
    contador_bits = 0
    for i in range(8):
        bit = (byte >> (7 - i)) & 1  # del bit más significativo al menos
        contador_bits+=bit
    if tipoParidad == 0: 
        paridad = 0 if contador_bits % 2 == 0 else 1
    else:  
        paridad = 1 if contador_bits % 2 == 0 else 0

    byte_con_paridad = (byte << 1) | paridad   

    return byte_con_paridad

def byte_tiene_errores(byte,tipoParidad=0):
    bit_paridad = byte & 1 # tomo el menos significativo
    byte = byte >> 1
    contador_bits = 0
    for i in range(8):
        bit = (byte >> (7 - i)) & 1  # del bit más significativo al menos
        contador_bits+=bit
    
    if tipoParidad == 0:  
        bit_esperado = 0 if contador_bits % 2 == 0 else 1
    else: 
        bit_esperado = 1 if contador_bits % 2 == 0 else 0
    
    return bit_paridad != bit_esperado


def codificar_con_paridades(cadena, tipoParidad=0):
    if not cadena:
        return bytearray()

    # convertir cada char en byte con paridad vertical
    bytes_con_paridad = [devolver_byte_con_paridad(c, tipoParidad) for c in cadena]

    # crear matriz de bits (cada fila = byte de 9 bits)
    matriz_bits = []
    for byte in bytes_con_paridad:
        fila = [(byte >> i) & 1 for i in range(8, -1, -1)]  # 9 bits (MSB -> LSB)
        matriz_bits.append(fila)

    filas = len(matriz_bits)
    columnas = len(matriz_bits[0])

    # calcular paridad longitudinal (columna por columna)
    paridad_longitudinal = []
    for col in range(columnas):
        suma = sum(matriz_bits[f][col] for f in range(filas))
        if tipoParidad == 0:  # paridad par
            paridad_longitudinal.append(suma % 2)
        else:  # impar
            paridad_longitudinal.append((suma + 1) % 2)

    #calcular paridad cruzada (bit total de todas las paridades longitudinales)
    suma_total = sum(paridad_longitudinal)
    if tipoParidad == 0:
        bit_cruzado = suma_total % 2
    else:
        bit_cruzado = (suma_total + 1) % 2

    # agregar las paridades como bytes finales
    # Convertir la paridad longitudinal (9 bits) en un byte
    byte_paridad_longitudinal = 0
    for bit in paridad_longitudinal:
        byte_paridad_longitudinal = (byte_paridad_longitudinal << 1) | bit

    # Agregar todo al bytearray
    resultado = bytearray(bytes_con_paridad)
    resultado.append(byte_paridad_longitudinal)
    resultado.append(bit_cruzado)

    return resultado



def decodificar_con_paridades(byte_seq, tipoParidad=0):
    if not byte_seq or len(byte_seq) < 3:
        return ""

    # Últimos dos bytes: longitudinal y cruzada
    bit_cruzado = byte_seq[-1]
    byte_paridad_longitudinal = byte_seq[-2]
    bytes_datos = byte_seq[:-2]

    # Verificar errores individuales (paridad vertical)
    errores = [byte_tiene_errores(b, tipoParidad) for b in bytes_datos]
    if any(errores):
        return ""

    # Reconstruir la matriz de bits para comprobar longitudinal y cruzada
    matriz_bits = []
    for byte in bytes_datos:
        fila = [(byte >> i) & 1 for i in range(8, -1, -1)]
        matriz_bits.append(fila)

    filas = len(matriz_bits)
    columnas = len(matriz_bits[0])

    # Calcular paridad longitudinal esperada
    paridad_longitudinal_esperada = []
    for col in range(columnas):
        suma = sum(matriz_bits[f][col] for f in range(filas))
        if tipoParidad == 0:
            paridad_longitudinal_esperada.append(suma % 2)
        else:
            paridad_longitudinal_esperada.append((suma + 1) % 2)

    # Comparar con la recibida
    for i in range(columnas):
        bit_recibido = (byte_paridad_longitudinal >> (columnas - 1 - i)) & 1
        if bit_recibido != paridad_longitudinal_esperada[i]:
            return ""

    # Verificar paridad cruzada
    suma_total = sum(paridad_longitudinal_esperada)
    bit_cruzado_esperado = suma_total % 2 if tipoParidad == 0 else (suma_total + 1) % 2
    if bit_cruzado != bit_cruzado_esperado:
        return ""

    # Todo correcto: reconstruir cadena
    mensaje = ""
    for byte in bytes_datos:
        ascii_byte = byte >> 1  # eliminar bit de paridad vertical
        mensaje += chr(ascii_byte)

    return mensaje




def mostrarListaConIndices(lista):
    for i in range(len(lista)):
        print(f"[{i}]={lista[i]}",end="  ")
    print()

"""
print(cumple_primer_teorema_shannon([0.3,0.1,0.4,0.2],["BA","CAB","A","CBA"],1))
print(cumple_primer_teorema_shannon([0.3,0.1,0.4,0.2],["BA","CAB","A","CBA"],2))

C1 = ["11", "010", "00"]
C2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]
P = [0.5, 0.2, 0.3]
P_2 = [P[i]*P[j] for i in range(len(P)) for j in range(len(P))]

print(cumple_primer_teorema_shannon(P, C1, 1))
print(cumple_primer_teorema_shannon(P_2, C2, 1))
"""
"""
P = [0.8,0.2]
listaExtension,listaExtensionProb = generarListaExtension(["0","1"],P,3)
print("Extension ",listaExtension)
print("Probs Extension ordenada ",sorted(listaExtensionProb,reverse=True))
print(cumple_primer_teorema_shannon(sorted(listaExtensionProb,reverse=True), ["0","100","101","110","11100","11101","11110","11111"], 3))

"""
"""
print(cumple_primer_teorema_shannon([0.49,0.21,0.21,0.09],["0","11","100","101"],2))
print(cumple_primer_teorema_shannon([0.49,0.21,0.21,0.09],["0","10","110","111"],2))
"""

"""
6

C1 = ["11", "010", "00"]
C2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]
P = [0.5, 0.2, 0.3]
P_2 = [P[i]*P[j] for i in range(len(P)) for j in range(len(P))]

print(calcularRedundanciaYEficiencia(P, C1))
print(calcularRedundanciaYEficiencia(P_2, C2))
"""
"""
P= [0.2,0.15,0.1,0.3,0.25]
C = ["01","111","110","101","100"]
print(calcularRedundanciaYEficiencia(P, C))
C2 = ["00","01","10","110","111"]
print(calcularRedundanciaYEficiencia(P, C2))
C3 = ["0110","010","0111","1","00"]
print(calcularRedundanciaYEficiencia(P, C3))
C4 = ["11","001","000","10","01"]
print(calcularRedundanciaYEficiencia(P, C4))
"""
"""
letras,probs = generarListaParalelas("ABCDABCBDCBAAABBBCBCBABADBCBABCBDBCCCAAABB")
print("Letras ",letras) 
print("Probs ",probs)
letras,probs = generarListaParalelas("AOEAOEOOOOEOAOEOOEOOEOAOAOEOEUUUIEOEOEO")
print("Letras ",letras) 
print("Probs ",probs)

"""
#Punto 12
#P = { 0.385, 0.154, 0.128, 0.154, 0.179 }
"""
P  = [0.385, 0.154, 0.128, 0.154, 0.179]
 # uso cualquier valor para palabras_codigo de 0 y 1 para obtener la entropia en base 2
print("Entropia ",calcular_entropia_fuente_codigo(["00","1","11","10","11"],P))
tabla_huffman = algoritmo_huffman(P) # OJO CON LOS INDICES posible trampa para el examen
tabla_shanon_fano = algoritmo_shanon_fano(P)
print(calcular_longitud_media_codigo(tabla_huffman,P))
print(calcular_longitud_media_codigo(tabla_shanon_fano,P))
print(calcularRedundanciaYEficiencia(P, tabla_huffman))
print(calcularRedundanciaYEficiencia(P, tabla_shanon_fano))
"""
"""
#Punto 13
letras,probs = generarListaParalelasCadenaCaracteresYProbs("58784784525368669895745123656253698989656452121702300223659")
mostrarListaConIndices(letras)
mostrarListaConIndices(probs)
tabla_huffman = algoritmo_huffman(probs) 
tabla_shanon_fano = algoritmo_shanon_fano(probs)
print(calcular_longitud_media_codigo(tabla_huffman,probs))
print(calcular_longitud_media_codigo(tabla_shanon_fano,probs))
print(calcularRedundanciaYEficiencia(probs, tabla_huffman))
print(calcularRedundanciaYEficiencia(probs, tabla_shanon_fano)) # preguntar
"""
#Punto 15


cadena_bits,byte_array = codificar_en_byteArray("DDDDDDDDDBBBBBBBBBBBBBBBBBBBBBBBBAAABBCD","ABCD",["00","11","10","01"]) # deberia devolver bytearray(b'\x00\x01\x02\x03\x00\x01\x02\x03')
print(cadena_bits)
print(byte_array)
cadena_decodificada = decodificar_de_byteArray(cadena_bits,"ABCD",["00","11","10","01"]) #Ojo con el orden de los alfabetos
print(cadena_decodificada)

#Punto 16

#print(calcular_comprension("DDDDDDDDDBBBBBBBBBBBBBBBBBBBBBBBBAAABBCD",byte_array))

#punto 17
"""


simbolos = [
    " ", ",", ".", ":", ";", "A", "B", "C",
    "D", "E", "F", "G", "H", "I", "J", "K",
    "L", "M", "N", "Ñ", "O", "P", "Q", "R",
    "S", "T", "U", "V", "W", "X", "Y", "Z"
]

probs = [
    0.175990, 0.014093, 0.015034, 0.000542, 0.002109, 0.111066, 0.015368, 0.030176,
    0.038747, 0.101604, 0.004873, 0.008762, 0.007953, 0.049740, 0.003706, 0.000034,
    0.048149, 0.021041, 0.050490, 0.002018, 0.073793, 0.019583, 0.010246, 0.051446,
    0.058406, 0.031093, 0.033240, 0.008930, 0.000012, 0.000076, 0.007851, 0.003199
]

tabla_huffman = algoritmo_huffman(probs)
cadena_bits,byte_array = codificar_en_byteArray("HOLA MUNDO"," ,.:;ABCDEFGHIJKLMNÑOPQRSTUVWXYZ",tabla_huffman)
print("Cadena bits ",cadena_bits)
print("Byte array ",byte_array)
print("Compresion ",calcular_comprension("HOLA MUNDO",byte_array))
print("redundancia y eficiencia ",calcularRedundanciaYEficiencia(probs, tabla_huffman))

cadena_decodificada = decodificar_de_byteArray(cadena_bits," ,.:;ABCDEFGHIJKLMNÑOPQRSTUVWXYZ",tabla_huffman)
print(cadena_decodificada)

"""
"""
bytearray_cadena = codificar_usando_RCL("XXXYZZZZ")
print("Compresion RCL ",calcular_comprension("XXXYZZZZ",bytearray_cadena))
bytearray_cadena = codificar_usando_RCL("AAAABBBCCDAA")
print("Compresion RCL ",calcular_comprension("AAAABBBCCDAA",bytearray_cadena))
bytearray_cadena = codificar_usando_RCL("UUOOOOAAAIEUUUU")
print("Compresion RCL ",calcular_comprension("UUOOOOAAAIEUUUU",bytearray_cadena))
"""
#punto 23
"""
C = ["0100100","0101000","0010010","0100000"]
distancia,errores_detectables,errores_corregibles = hamming(C)
print(distancia,errores_detectables,errores_corregibles)
C = ["0100100","0010010","0101000","0100001"]
distancia,errores_detectables,errores_corregibles = hamming(C)
print(distancia,errores_detectables,errores_corregibles)
C = ["0110000","0000011","0101101","0100110"]
distancia,errores_detectables,errores_corregibles = hamming(C)
print(distancia,errores_detectables,errores_corregibles)
"""
"""
print(devolver_byte_con_paridad("c"))
print(byte_tiene_errores(devolver_byte_con_paridad("c")))

mensaje = codificar_con_paridades("Hola")
print(mensaje)
mensajeDescifrado = decodificar_con_paridades(mensaje)
print(mensajeDescifrado)


"""