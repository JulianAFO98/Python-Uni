
import math

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


def cumple_primer_teorema_shannon(probs_fuente, palabras_codigo, n):

    listaExtension,probsExtension = generarListaExtension(palabras_codigo, probs_fuente, n)
    L_n = calcular_longitud_media_codigo(listaExtension, probsExtension)
    print("Longitud ",L_n)
    H_r_S = calcular_entropia_fuente_codigo(listaExtension, probsExtension)/n
    print("Entropia r ",H_r_S)
    return (H_r_S) <= (L_n/n)  and  (L_n/n)  < ((H_r_S) + (1 / n))

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
    return round(R,3), round(eficiencia,3)


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
    
    probabilidades = [round(val/len(cadena),2) for val in contApariciones]
    return letras,probabilidades
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

letras,probs = generarListaParalelas("ABCDABCBDCBAAABBBCBCBABADBCBABCBDBCCCAAABB")
print("Letras ",letras) 
print("Probs ",probs)
letras,probs = generarListaParalelas("AOEAOEOOOOEOAOEOOEOOEOAOAOEOEUUUIEOEOEO")
print("Letras ",letras) 
print("Probs ",probs)