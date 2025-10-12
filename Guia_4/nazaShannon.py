
import math

def obtenerAlfabetoOrd(codigos):
    """Devuelve el alfabeto ordenado de una lista de códigos."""
    return sorted(set("".join(codigos)))

def entropia(codigos, probabilidades):
    """Calcula la entropía de un código dado su alfabeto y probabilidades."""
    r = len(obtenerAlfabetoOrd(codigos))
    h = 0.0
    for p in probabilidades:
        if p > 0:
            h += p * math.log(1/p, r)
    return h

def longitudMedia(codigos, probabilidades):
    """Calcula la longitud media de un código ponderada por probabilidades."""
    l = 0.0
    for i in range(len(codigos)):
        l += probabilidades[i] * len(codigos[i])
    return l


def cumplePrimerTeorema(probabilidades, codigos, N):
    """
    Verifica si un código para la extensión de orden N cumple el Primer Teorema de Shannon.
    
    probabilidades: lista con la distribución de la fuente original
    codigos: lista de palabras código asignadas a la extensión de orden N
    N: orden de la extensión
    """
    # Entropía de la fuente original
    H = entropia(codigos, probabilidades)/N #divido por N porque puede calcular la entropia de la extension y para el return uso H/N
    print("Entropia ",H)
    # Longitud media de la extensión
    L = longitudMedia(codigos, probabilidades)
    print("Longitud media ",L)
    # Primer Teorema: H <= L_n/N < H + 1/N
    return H <= L/N < H + 1/N

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
    listaExtensionProb = [round(p, 2) for p in listaExtensionProb]
    
    return listaExtension, listaExtensionProb        
print(cumplePrimerTeorema([0.3,0.1,0.4,0.2],["BA","CAB","A","CBA"],1))
print(cumplePrimerTeorema([0.3,0.1,0.4,0.2],["BA","CAB","A","CBA"],2))

C1 = ["11", "010", "00"]
C2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]
P = [0.5, 0.2, 0.3]
P_2 = [P[i]*P[j] for i in range(len(P)) for j in range(len(P))]

ext_cod, ext_p = generarListaExtension(C1, P, 1)
print("n =", 1, "H(S) =", entropia(C1, P), "L1 =", longitudMedia(C1, P), "cumple?", cumplePrimerTeorema(P, C1, 1), "\n")

ext_cod, ext_p = generarListaExtension(C1, P, 2)
print("n =", 2, "H(S) =", entropia(C2, P), "L2 =", longitudMedia(C2, ext_p), "cumple?", cumplePrimerTeorema(ext_p, C2, 2), "\n")