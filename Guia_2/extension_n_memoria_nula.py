import entropia_info_mejorada

def generarListaExtension(alfabeto,probs,grado):
    cantFilas = len(alfabeto)**grado
    listaExtension = ["" for _ in range(cantFilas)]
    listaExtensionProb = [1 for _ in range(cantFilas)]
    
    for i in range(grado): # los n simbolos
        tamanioParticion = len(alfabeto)**(grado - (i+1))
        for j in range(cantFilas): # iterar sobre todas las filas
            elemIndex = (j // tamanioParticion) % len(alfabeto)
            listaExtension[j] += alfabeto[elemIndex]
            listaExtensionProb[j] *= probs[elemIndex]   
    return listaExtension,listaExtensionProb

n=2
lista = [1/6]*6
listaExtension,listaExtensionProb = generarListaExtension(["D1","D2","D3","D4","D5","D6"],lista,n)
print("Entropia de la lista de probabilidades extendida",entropia_info_mejorada.calcularEntropia(listaExtensionProb))
print("n * H(S)",entropia_info_mejorada.calcularEntropia(lista) * n)

n=3
lista = [1/6]*6

listaExtension,listaExtensionProb = generarListaExtension(["D1","D2","D3","D4","D5","D6"],lista,n)
print("Entropia de la lista de probabilidades extendida",entropia_info_mejorada.calcularEntropia(listaExtensionProb))
print("n * H(S)",entropia_info_mejorada.calcularEntropia(lista) * n)


n=2
lista = [1/9,1/6,1/9,1/9,1/6,1/3]
listaExtension,listaExtensionProb = generarListaExtension(["D1","D2","D3","D4","D5","D6"],lista,n)
print("Entropia de la lista de probabilidades extendida",entropia_info_mejorada.calcularEntropia(listaExtensionProb))
print("n * H(S)",entropia_info_mejorada.calcularEntropia(lista) * n)


n=3
lista = [1/9,1/6,1/9,1/9,1/6,1/3]
listaExtension,listaExtensionProb = generarListaExtension(["D1","D2","D3","D4","D5","D6"],lista,n)
print("Entropia de la lista de probabilidades extendida",entropia_info_mejorada.calcularEntropia(listaExtensionProb))
print("n * H(S)",entropia_info_mejorada.calcularEntropia(lista) * n)