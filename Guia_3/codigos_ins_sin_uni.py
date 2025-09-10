"""
Desarrollar funciones booleaneas en Python que reciban como parámetro una lista con
palabras código y verifiquen si el código es:
a. no singular
b. instantáneo
c. unívocamente decodificable
"""


def es_singular(list):
    s = set(list)
    return len(s) == len(list)

def es_instantaneo(codigo):
    for i, palabra in enumerate(codigo):
        for j, otra in enumerate(codigo):
            if i != j and otra.startswith(palabra):
                return False
    return True

def es_univoco(codigo):
    es_univoco = True
    codigo_set = set(codigo)
    sufijos_a_revisar = codigo_set.copy()
    
    while es_univoco and sufijos_a_revisar:
        nuevos_sufijos = set()
        
        for x in sufijos_a_revisar:
            for y in codigo_set:
                if y.startswith(x) and y != x:
                    suf = y[len(x):]
                    if suf in codigo_set:
                        es_univoco = False
                    nuevos_sufijos.add(suf)
        
        if es_univoco:
            sufijos_a_revisar = nuevos_sufijos
        else:
            sufijos_a_revisar = set()
    
    return es_univoco

list = ["1110","0","110","1101","1011","10"]

print(es_singular(list))
print(es_instantaneo(list))
print(es_univoco(list))
