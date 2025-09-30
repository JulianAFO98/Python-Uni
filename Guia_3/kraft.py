"""
 Dada una lista que contiene las palabras código de una codificación, implementar
funciones en Python que resuelvan lo siguiente:
a. obtener una cadena de caracteres con el alfabeto código.
b. generar otra lista con las longitudes de las palabras (utilizar comprensión de listas).
c. calcular la sumatoria de la inecuación de Kraft (utilizar las funciones anteriores).

Dadas dos listas paralelas que contengan las palabras código de una codificación y sus
respectivas probabilidades, codificar funciones en Python que calculen:
a. la entropía de la fuente
b. la longitud media del código

"""
import math
import random
def obtener_cadena_alfabeto_codigo(palabras):
    cadena = ""
    for palabra in palabras:
        for letra in palabra:
            if letra not in cadena:
                cadena += letra
    return cadena

def generar_lista_longitudes(palabras):
    lista_longitudes = [len(palabra) for palabra in palabras]
    return lista_longitudes

def calcular_inecuacion_kraft(cadena_codigo,lista_longitudes):
    suma = 0
    r = len(cadena_codigo)
    for i in range(len(lista_longitudes)):
        suma+=r ** (-lista_longitudes[i])
    return suma

"""
AUXILIARES
"""
def es_instantaneo(codigo):
    for i, palabra in enumerate(codigo):
        for j, otra in enumerate(codigo):
            if i != j and otra.startswith(palabra):
                return False
    return True

def info(val,base): 
    if val == 0:
        return 0
    return -math.log(val,base)

def generarListaInfo(lista,base):
    return [info(val,base) for val in lista]

"""
AUXILIARES
"""

def calcular_entropia_fuente_codigo(palabras_codigo,probabilidades):
    simbolos_distintos = obtener_cadena_alfabeto_codigo(palabras_codigo)
    base = len(simbolos_distintos)
    return sum(p * info(p,base) for p in probabilidades)

def calcular_entropia_fuente_codigo_con_techo(palabras_codigo,probabilidades):
    simbolos_distintos = obtener_cadena_alfabeto_codigo(palabras_codigo)
    base = len(simbolos_distintos)
    return sum(p * math.ceil(abs(info(p,base))) for p in probabilidades)

def informaciones(palabras_codigo,probabilidades):
    simbolos_distintos = obtener_cadena_alfabeto_codigo(palabras_codigo)
    base = len(simbolos_distintos)
    print("Informaciones")
    for i in range(len(probabilidades)):
        print(abs(info(i,base))); 


def calcular_longitud_media_codigo(palabras_codigo,probabilidades):
    lista_longitudes = generar_lista_longitudes(palabras_codigo)
    return sum(probabilidades[i] * lista_longitudes[i] for i in range(len(palabras_codigo)))

def es_codigo_compacto(codigo,probs):
    suma_kraft = calcular_inecuacion_kraft(obtener_cadena_alfabeto_codigo(codigo),generar_lista_longitudes(codigo))

    if suma_kraft > 1:
        return False 

    entropia = calcular_entropia_fuente_codigo_con_techo(codigo,probs)
    L = calcular_longitud_media_codigo(codigo,probs)
    if(not es_instantaneo(codigo)):
        return False
    
    return L<=entropia

def generar_mensaje(N, codigos, probs):
 
    mensaje = ""
    for _ in range(N):
        palabra = random.choices(codigos, weights=probs, k=1)[0]
        mensaje += palabra
    return mensaje



"""
lista = [".,",";",",,",":","...",",:;"]
print(calcular_inecuacion_kraft(obtener_cadena_alfabeto_codigo(lista),generar_lista_longitudes(lista)))
"""
"""
13)
["0","10","110","111"]
["00","11","10","01"]
lista = ["1","2","31","32"]
probs = [0.5,0.25,0.125,0.125]
lista = ["1","2","31","32"]
probs = [1/3,1/3,1/6,1/6]
preguntar
lista = ["11","12","21","22"] 
probs = [0.5,0.25,0.125,0.125]
lista = ["1","2","31","32"] 
probs = [1/3,1/3,1/6,1/6]

lista = ["1","2","31","32"]
probs = [0.5,0.25,0.125,0.125]
print("Kraft: ",calcular_inecuacion_kraft(obtener_cadena_alfabeto_codigo(lista),generar_lista_longitudes(lista)))
print("Entropia: ",calcular_entropia_fuente_codigo(lista,probs))
print("Entropia con techo: ",calcular_entropia_fuente_codigo_con_techo(lista,probs))
print("Longitud media: ",calcular_longitud_media_codigo(lista,probs))
informaciones(lista,probs)
"""

"""

15)
"""
"""
probs = [0.1, 0.5, 0.1, 0.2,0.05,0.05]

lista = ["==","<","<=",">",">=","<>"]
print(es_codigo_compacto(lista,probs))
lista = [")","[]","]]","([","[()]","([)]"]
print(es_codigo_compacto(lista,probs))
lista = ["/","*","-","*","++","+-"]
print(es_codigo_compacto(lista,probs))
lista = [".,",";",",,",":","...",",:;"]
print(es_codigo_compacto(lista,probs))
"""
probs = [0.13, 0.34, 0.37, 0.12,0.04]
lista = ["BA","CCB","AC","C","BAC"]
print(es_codigo_compacto(lista,probs))
lista = ["B","CB","A","CC","CA"]
print(es_codigo_compacto(lista,probs))
lista = ["AA","C","B","AB","ACB"]
print(es_codigo_compacto(lista,probs))
lista = ["BC","A","C","BA","BB"]
print(es_codigo_compacto(lista,probs))

"""
codigos = ["0", "10", "110", "111"]
probs = [0.5, 0.25, 0.125, 0.125]

mensaje = generar_mensaje(5, codigos, probs)
print(mensaje)  # Ejemplo de salida: "0110110110"
"""