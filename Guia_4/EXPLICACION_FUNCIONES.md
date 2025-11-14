# Explicación de Funciones - Codificación y Teoría de la Información

## 📚 Introducción

Este código implementa conceptos fundamentales de **Teoría de la Información** desarrollados por Claude Shannon, abarcando:

- **Compresión de Datos**: Algoritmos óptimos de codificación (Huffman, Shannon-Fano)
- **Teoría de Códigos**: Análisis de entropía, eficiencia y redundancia
- **Detección y Corrección de Errores**: Técnicas de control de integridad en transmisiones
- **Verificación de Teoremas**: Validación del Primer Teorema de Shannon

La complejidad de este código radica en la implementación rigurosa de conceptos matemáticos que subyacen en tecnologías modernas como compresión de datos, comunicaciones confiables y almacenamiento eficiente.

---

## 🔧 FUNCIONES BÁSICAS

### 1. `info(val, base)`

**Definición Matemática:**

$$I(x) = -\log_b(p(x))$$

donde $p(x)$ es la probabilidad de un símbolo y $b$ es la base logarítmica (base del alfabeto código).

**Descripción:**
Calcula la **autoinformación** o **contenido de información** de un símbolo individual. Esta es una medida fundamental en teoría de la información que cuantifica cuánta información (en bits) proporciona la ocurrencia de un evento con probabilidad $p$.

**Interpretación:**
- Un evento con alta probabilidad (cercano a 1) tiene baja autoinformación
- Un evento con baja probabilidad (cercano a 0) tiene alta autoinformación
- Un evento seguro (probabilidad 1) tiene autoinformación 0

**Ejemplos:**
```python
info(0.5, 2) = -log₂(0.5) = 1 bit      # Evento con 50% de probabilidad
info(0.25, 2) = -log₂(0.25) = 2 bits   # Evento con 25% de probabilidad
info(1.0, 2) = -log₂(1.0) = 0 bits     # Evento seguro (no aporta información)
```

**Caso especial:** Si `val == 0`, la función devuelve 0 (ya que el límite de $-p\log(p)$ cuando $p \to 0$ es 0).

---

### 2. `generarListaInfo(lista, base)`

**Descripción:**
Aplica la función de autoinformación a todos los elementos de una lista mediante una comprensión de lista (list comprehension).

**Fórmula:**
$$I = [I(p_i) : \forall p_i \in \text{lista}]$$

**Funcionalidad:**
Genera el vector de autoinformación para un conjunto de probabilidades, permitiendo análisis estadísticos posteriores de la fuente.

```python
generarListaInfo([0.5, 0.25, 0.125], 2)
# Resultado: [1.0, 2.0, 3.0]  (autoinformación de cada símbolo)
```

---

### 3. `generar_lista_longitudes(palabras)`

**Descripción:**
Obtiene la longitud (número de caracteres o símbolos) de cada palabra código en una secuencia.

**Fórmula:**
$$L = [|w_i| : \forall w_i \in \text{palabras}]$$

donde $|w_i|$ es la cardinalidad (longitud) de la palabra código $w_i$.

**Propósito:**
Permite calcular posteriormente la longitud media del código, un parámetro crítico para evaluar la eficiencia de esquemas de codificación.

```python
generar_lista_longitudes(["0", "10", "110"])
# Resultado: [1, 2, 3]  (longitudes de cada código)
```

---

### 4. `calcular_longitud_media_codigo(palabras_codigo, probabilidades)`

**Definición Matemática:**

$$L = \sum_{i=0}^{n-1} p_i \cdot |c_i|$$

donde:
- $p_i$ es la probabilidad del símbolo $i$
- $|c_i|$ es la longitud del código asignado al símbolo $i$
- $n$ es la cardinalidad del alfabeto fuente

**Descripción:**
Calcula la **longitud media de código** (average code length), que representa el número esperado de símbolos binarios requeridos por cada símbolo de la fuente.

**Significado:**
Es una métrica fundamental para evaluar la eficiencia de un código. El Primer Teorema de Shannon establece que:

$$H(S) \leq L < H(S) + 1$$

donde $H(S)$ es la entropía de la fuente.

**Ejemplo:**
```python
# Códigos: ["0", "10", "110"]
# Probabilidades: [0.5, 0.3, 0.2]
L = 0.5×1 + 0.3×2 + 0.2×3 = 1.7 bits por símbolo
```

**Interpretación:** En promedio, cada símbolo de la fuente requiere 1.7 bits para ser codificado.

---

### 5. `obtener_cadena_alfabeto_codigo(palabras)`

**Descripción:**
Extrae el conjunto de símbolos distintos (alfabeto código) utilizados en una lista de palabras código.

**Fórmula:**
$$\Sigma = \{c : c \in w_i, \forall w_i \in \text{palabras}\}$$

**Funcionalidad:**
Determina la cardinalidad del alfabeto código (número de símbolos distintos), parámetro esencial para:
- Calcular la base del logaritmo en la entropía
- Verificar que sea un alfabeto binario (base 2) u otro

```python
obtener_cadena_alfabeto_codigo(["0011", "101", "10"])
# Resultado: "01"  (alfabeto binario)

obtener_cadena_alfabeto_codigo(["ABC", "BAC", "CA"])
# Resultado: "ABC"  (alfabeto ternario)
```

---

### 6. `calcular_entropia_fuente_codigo(palabras_codigo, probabilidades)`

**Definición Matemática (Entropía de Shannon):**

$$H_r(S) = -\sum_{i=0}^{n-1} p_i \log_r(p_i)$$

donde:
- $r = |\Sigma|$ es la cardinalidad del alfabeto código
- $p_i$ es la probabilidad del símbolo $i$
- $\log_r$ es el logaritmo en base $r$

**Descripción:**
Calcula la **entropía de la fuente en base $r$**, que representa la cantidad mínima de información (medida en símbolos de base $r$) necesaria en promedio para codificar un símbolo de la fuente.

**Propiedades Fundamentales:**
1. Es una medida de la incertidumbre o aleatoriedad de la fuente
2. Establece un **límite inferior teórico** para la longitud media de cualquier código
3. La entropía es máxima cuando todos los símbolos tienen equiprobabilidad

**Teorema de Shannon (Primer Teorema):**

$$H_r(S) \leq L < H_r(S) + 1$$

Esto implica que no existe código cuya longitud media sea menor que la entropía.

**Ejemplo:**
```python
# Probabilidades: [0.5, 0.3, 0.2]
# Alfabeto binario (r=2)
H = -[0.5×log₂(0.5) + 0.3×log₂(0.3) + 0.2×log₂(0.2)]
  = -[0.5×(-1) + 0.3×(-1.737) + 0.2×(-2.322)]
  ≈ 1.486 bits
```

**Interpretación:** Un código óptimo para esta fuente debe tener longitud media mínimo de 1.486 bits por símbolo.

---

### 7. `generarListaExtension(alfabeto, probs, grado)`

**Concepto de Extensión de Fuente:**

Una extensión de grado $n$ de una fuente $S$ es una nueva fuente $S^n$ cuyos símbolos son $n$-tuplas de símbolos de $S$.

**Descripción:**
Genera todas las $|\Sigma|^n$ posibles secuencias de longitud $n$ tomadas del alfabeto fuente, junto con sus probabilidades (asumiendo independencia estadística).

**Algoritmo:**
1. Crea $|\Sigma|^n$ posiciones para almacenar secuencias
2. Para cada posición, construye la secuencia correspondiente usando aritmética modular
3. Calcula la probabilidad conjunta $P(w_i) = \prod_{j} p_{ij}$ para cada secuencia

**Ejemplo de Extensión de Grado 2:**
```python
generarListaExtension(["A", "B"], [0.6, 0.4], 2)
# Resultado:
# Secuencias: ["AA", "AB", "BA", "BB"]
# Probabilidades: [0.36, 0.24, 0.24, 0.16]
# (porque 0.6²=0.36, 0.6×0.4=0.24, etc.)
```

**Propiedades de la Extensión:**
- La suma de probabilidades sigue siendo 1
- La entropía de $S^n$ es $n \times H(S)$
- Cumple el teorema: $H(S^n) = n \times H(S)$

**Aplicación:**
Es esencial para verificar el Primer Teorema de Shannon, ya que permite evaluar si un código cumple la desigualdad de Shannon en diferentes grados de extensión.

---

### 8. `cumple_primer_teorema_shannon(probs_fuente, palabras_codigo, n)`

**Primer Teorema de Shannon (Teorema Fundamental de la Codificación):**

Para verificar el teorema de Shannon se parte de las probabilidades de la fuente original y las palabras del código (debe ser un código para la fuente original). Se genera la extensión de grado $n$ de la fuente y se calcula la entropía $H_r$ y la longitud media del código para la extensión. Luego se verifica que se cumpla la desigualdad:

$$H_r(S) \leq \frac{L_n}{n} < H_r(S) + \frac{1}{n}$$

donde:
- $H_r(S)$ es la entropía de la fuente en base $r$ ($r$ es la cantidad de símbolos distintos en el alfabeto del código)
- $L_n$ es la longitud media del código para la extensión de grado $n$
- La división por $n$ normaliza la longitud media al símbolo original

**Descripción:**
Implementa la verificación rigurosa del Primer Teorema de Shannon. Esta es la verificación **teórica fundamental** que garantiza la optimalidad de un código.

**Algoritmo:**
1. Genera la extensión de grado $n$ de la fuente
2. Calcula $L_n$ (longitud media normalizada de la extensión)
3. Calcula $H_r(S)$ (entropía normalizada por $n$)
4. Verifica la doble desigualdad

**Conclusión del Teorema:**
Si se cumple la desigualdad para la extensión de grado $n$, entonces el código cumple el Primer Teorema de Shannon, siendo este un **código sin ruido** (noiseless code) que satisface las condiciones de optimalidad de Shannon.

**Interpretación Práctica:**
- Si el código es **óptimo**, la desigualdad se cumple y $\frac{L_n}{n}$ se aproxima a $H_r(S)$ cuando $n \to \infty$
- Si el código **no es óptimo**, $\frac{L_n}{n}$ será significativamente mayor que $H_r(S)$

**Ejemplo de Verificación:**
```python
P = [0.5, 0.3, 0.2]
C = ["0", "10", "11"]  # Código de Huffman (óptimo)

# Para n=1:
# L = 0.5×1 + 0.3×2 + 0.2×2 = 1.5
# H = -[0.5×log₂(0.5) + 0.3×log₂(0.3) + 0.2×log₂(0.2)] ≈ 1.486
# Verifica: 1.486 ≤ 1.5 < 1.486 + 1 ✓

cumple_primer_teorema_shannon(P, C, 1)  # Devuelve True
```

---

### 9. `calcularRedundanciaYEficiencia(probs_extension, palabras_codigo)`

**Definiciones Matemáticas:**

**Eficiencia del Código:**
$$\eta = \frac{H(S)}{L}$$

**Redundancia del Código:**
$$R = 1 - \eta = 1 - \frac{H(S)}{L}$$

donde:
- $H(S)$ es la entropía de la fuente (límite inferior teórico)
- $L$ es la longitud media del código

**Descripción:**
Calcula dos métricas fundamentales para evaluar la calidad de un esquema de codificación:

1. **Eficiencia** ($0 \leq \eta \leq 1$): Indica qué proporción de los bits transmitidos contienen información útil
2. **Redundancia** ($0 \leq R \leq 1$): Indica qué proporción de bits se utiliza para "llenar" sin aportar información

**Interpretación:**
- $\eta = 1$ y $R = 0$: Código **perfecto/óptimo** (nunca alcanzable en la práctica)
- $\eta = 0.95$: El 95% de los bits son información, 5% es redundancia
- $\eta < 0.90$: El código es **ineficiente** y debería mejorarse

**Ejemplo Comparativo:**
```python
# Código 1 (Huffman - Óptimo):
P = [0.5, 0.3, 0.2]
C1 = ["0", "10", "11"]
# L = 1.5, H ≈ 1.486
# η ≈ 0.9907, R ≈ 0.0093  (excelente)

# Código 2 (No óptimo):
C2 = ["00", "01", "10"]
# L = 2.0, H ≈ 1.486
# η ≈ 0.7430, R ≈ 0.2570  (deficiente)

calcularRedundanciaYEficiencia(P, C1)  # (0.0093, 0.9907)
calcularRedundanciaYEficiencia(P, C2)  # (0.2570, 0.7430)
```

**Aplicación Práctica:**
Estas métricas son críticas en diseño de sistemas de comunicación, compresión de datos y almacenamiento, donde la eficiencia se traduce directamente en ahorro de ancho de banda o espacio de almacenamiento.

---

### 10. `generarListaParalelasCadenaCaracteresYProbs(cadena)`

**Descripción:**
Realiza un **análisis de frecuencias** de una cadena de caracteres, computando la distribución empírica de probabilidades de los símbolos.

**Algoritmo:**
1. Recorre la cadena carácter por carácter
2. Mantiene un registro de símbolos únicos y sus ocurrencias
3. Calcula la probabilidad empírica como $p_i = \frac{\text{ocurrencias}_i}{|\text{cadena}|}$

**Salida:**
Tupla $(S, P)$ donde:
- $S$ es la lista de símbolos únicos (alfabeto observado)
- $P$ es la lista de probabilidades empíricas correspondientes

**Aplicación:**
Herramienta esencial para:
- Análisis estadístico de textos reales
- Estimar distribuciones de probabilidad de fuentes naturales
- Preparar datos para algoritmos de compresión basados en probabilidades (Huffman, Shannon-Fano)

**Ejemplo:**
```python
cadena = "AABBBC"
letras, probs = generarListaParalelasCadenaCaracteresYProbs(cadena)
# letras = ["A", "B", "C"]
# probs = [0.3333, 0.5, 0.1667]  (distribuidas proporcionalmente)
```

**Nota sobre Redondeo:**
Las probabilidades se redondean a 10 decimales para evitar errores de precisión en cálculos posteriores.

---

## 🗜️ ALGORITMOS ÓPTIMOS DE COMPRESIÓN

### 11. `algoritmo_huffman(probs)`

**Algoritmo de Codificación de Huffman:**

Inventado por David A. Huffman (1952), es un algoritmo **greedy** que genera códigos binarios **óptimos** para una distribución de probabilidades conocida.

**Propiedades Teóricas:**
- Genera un código **óptimo instantáneo** (sin prefijos)
- La longitud media se acerca a la entropía: $H(S) \leq L < H(S) + 1$
- Es **óptimo en el sentido de Shannon**

**Algoritmo (Construcción de Árbol de Huffman):**
1. Crear nodos hoja para cada símbolo con su probabilidad
2. Mientras haya más de un nodo:
   - Seleccionar los dos nodos con menor probabilidad
   - Crear nodo padre con probabilidad suma
   - Asignar "0" y "1" a las ramas hijo
3. Recorrer el árbol desde raíz a hojas para obtener códigos

**Estructura de Datos:**
Usa una lista de pares `[probabilidad, [índices]]` donde los índices rastrean qué símbolos originales corresponden a cada nodo.

**Ejemplo:**
```python
probs = [0.5, 0.3, 0.2]
tabla_huffman = algoritmo_huffman(probs)
# Resultado posible: ["0", "10", "11"]
# Símbolo 0 (prob 0.5) → "0" (1 bit)
# Símbolo 1 (prob 0.3) → "10" (2 bits)
# Símbolo 2 (prob 0.2) → "11" (2 bits)
# L = 0.5×1 + 0.3×2 + 0.2×2 = 1.5 bits
```

**Comparación con Shannon-Fano:**
- Huffman: Siempre genera código óptimo
- Shannon-Fano: A veces genera código subóptimo

**Aplicaciones Reales:**
- Compresión ZIP/GZIP
- Compresión JPEG (tabla de Huffman para DC/AC)
- Transmisión de datos en redes

---

### 12. `algoritmo_shanon_fano(probs)`

**Algoritmo de Codificación de Shannon-Fano:**

Propuesto por Claude Shannon y Robert Fano, es un método alternativo que genera códigos **casi óptimos** mediante un enfoque **divide y conquista** recursivo.

**Algoritmo (Construcción Recursiva):**
1. Ordenar símbolos por probabilidad (descendente)
2. Dividir el conjunto en dos subconjuntos cuyas probabilidades se aproximan a la mitad
3. Asignar "0" al primer subconjunto y "1" al segundo
4. Repetir recursivamente en cada subconjunto hasta que queden símbolos individuales

**Criterio de División:**
Para cada partición, busca el índice que minimice $|P_{\text{izq}} - P_{\text{der}}|$ donde:
- $P_{\text{izq}} = \sum p_i$ para el subconjunto izquierdo
- $P_{\text{der}} = \sum p_i$ para el subconjunto derecho

**Estructura Recursiva:**
```
def shanon_fano_recursivo(items, tabla_shanon_fano):
    if len(items) > 1:
        # Ordenar, particionar, asignar bits, recursar
```

**Ejemplo Comparativo:**
```python
probs = [0.4, 0.3, 0.2, 0.1]

# Shannon-Fano:
# Nivel 1: [0.4, 0.3] vs [0.2, 0.1]
# Nivel 2: [0.4] vs [0.3] y [0.2] vs [0.1]
# Códigos: ["0", "10", "110", "111"]
# L = 0.4×1 + 0.3×2 + 0.2×3 + 0.1×3 = 1.9 bits

# Huffman:
# Códigos: ["0", "10", "110", "111"]  o similar
# L ≈ 1.8 bits (mejor que Shannon-Fano en este caso)
```

**Comparación:**
| Propiedad | Huffman | Shannon-Fano |
|-----------|---------|--------------|
| Optimalidad | **Óptimo** | Casi óptimo |
| Complejidad | O(n log n) | O(n log n) |
| Simplicidad | Más complejo | Más intuitivo |
| Aplicaciones | ZIP, JPEG, MP3 | Educativo, histórico |

**Nota:** Aunque Shannon-Fano es más directo conceptualmente, Huffman es superior y es el estándar en compresión moderna.

---

## 🔐 FUNCIONES DE CODIFICACIÓN/DECODIFICACIÓN

### 13. `codificar_en_byteArray(mensaje_a_codificar, alfabeto_fuente, lista_cadena_caracteres)`
**¿Qué hace?**
Convierte un mensaje de texto en bytes usando un código personalizado.

**Explicación simple:**
Si le dices:
- Mensaje: "ABC"
- Alfabeto: ["A", "B", "C"]
- Códigos: ["00", "11", "10"]

Devuelve los bytes que representan "001110".

**Para qué sirve:** Guardar mensajes codificados en archivos.

---

### 14. `decodificar_de_byteArray(cadena_bits_byteArray, alfabeto_fuente, alfabeto_codigo)`
**¿Qué hace?**
Lo inverso del anterior: convierte bytes codificados de vuelta al texto original.

**Explicación simple:**
Si le das bytes que representan "001110" y el diccionario de códigos, recupera "ABC".

**Para qué sirve:** Leer mensajes codificados.

---

## 📦 COMPRESIÓN POR RUN-LENGTH ENCODING

### 15. `codificar_usando_RCL(cadena)`
**¿Qué hace?**
Implementa **RLE** (Run-Length Encoding), que almacena repeticiones de forma compacta.

**Explicación simple:**
"AAABBBCC" se guarda como:
- A, 3 veces
- B, 3 veces
- C, 2 veces

Es muy efectivo para imágenes con áreas de color sólido.

```python
codificar_usando_RCL("AAABBBCC")
# Resultado: bytearray(b'A\x03B\x03C\x02')
```

**Para qué sirve:** Comprimir imágenes simples, FAX, etc.

---

### 16. `calcular_comprension(cadena_alfabeto_fuente, byte_array)`
**¿Qué hace?**
Calcula cuántas veces se comprimió el archivo.

**Explicación simple:**
Si el original tenía 100 bytes y comprimido tiene 25, la compresión es 4 veces.

```python
calcular_comprension("AAABBBCC", byte_array)
# Resultado: 2.66 (se redujo a 37% del tamaño original)
```

---

## 🛡️ DETECCIÓN Y CORRECCIÓN DE ERRORES

### 17. `hamming(lista_palabras_codigo)`

**Distancia de Hamming:**

La distancia de Hamming entre dos palabras código de igual longitud es el número de posiciones en las cuales los símbolos correspondientes **difieren**.

$$d_H(c_i, c_j) = |\{k : c_i[k] \neq c_j[k]\}|$$

**Definición Operativa:**
```python
d_H("000", "111") = 3  (todas las posiciones difieren)
d_H("001", "011") = 1  (solo la primera posición difiere)
d_H("0000", "0000") = 0  (códigos idénticos)
```

**Descripción de la Función:**
Calcula la **distancia de Hamming mínima** de un código (mínima entre todos los pares de palabras) y determina:

1. **Distancia Mínima** ($d_{\min}$): El menor número de diferencias entre cualquier par de códigos
2. **Errores Detectables**: $t_d = d_{\min} - 1$
3. **Errores Corregibles**: $t_c = \lfloor \frac{d_{\min} - 1}{2} \rfloor$

**Teoremas Fundamentales:**
- **Detección:** Un código puede detectar hasta $t_d$ errores si $d_{\min} \geq t_d + 1$
- **Corrección:** Un código puede corregir hasta $t_c$ errores si $d_{\min} \geq 2t_c + 1$

**Ejemplo:**
```python
C = ["000", "011", "101", "110"]
hamming(C)
# Distancias: (000,011)→2, (000,101)→2, (000,110)→2, ...
# d_min = 2
# Errores detectables = 1
# Errores corregibles = 0

# Un error de 1 bit se DETECTA pero NO se CORRIGE

C2 = ["0000000", "1111111"]
hamming(C2)
# d_min = 7
# Errores detectables = 6
# Errores corregibles = 3

# Hasta 3 errores se CORRIGEN automáticamente
```

**Aplicación en Sistemas Reales:**
- **Comunicaciones Espaciales:** NASA usa códigos con $d_{\min}$ muy alto
- **QR Codes:** Contienen redundancia para recuperarse de daño
- **Memoria DRAM:** Usa ECC (Error Correcting Code)

---

### 18. `devolver_byte_con_paridad(byte, tipoParidad=0)`

**Bit de Paridad (Parity Bit):**

Un bit adicional anexado a una palabra código que indica si la cantidad de 1s es **par** o **impar**.

**Tipos de Paridad:**
1. **Paridad Par** (Even Parity, `tipoParidad=0`): El bit de paridad es 1 si hay un número impar de 1s (para hacer el total par)
2. **Paridad Impar** (Odd Parity, `tipoParidad=1`): El bit de paridad es 1 si hay un número par de 1s (para hacer el total impar)

**Algoritmo:**
1. Contar los 1s en el byte original (8 bits)
2. Computar el bit de paridad según el tipo
3. Desplazar el byte original a la izquierda 1 posición
4. Insertar el bit de paridad como el LSB (Least Significant Bit)

**Ejemplo:**
```python
byte_original = "A" = 01000001 (ASCII 65)
Conteo de 1s: 2 (número par)

# Paridad par (tipoParidad=0):
Bit de paridad = 0 (ya hay número par de 1s)
Resultado: 010000010 = 130 en decimal

# Paridad impar (tipoParidad=1):
Bit de paridad = 1 (para hacer el total impar)
Resultado: 010000011 = 131 en decimal
```

**Estructura del Byte con Paridad:**
```
Bit:     8 7 6 5 4 3 2 1 (0=LSB)
Original: 0 1 0 0 0 0 0 1  (= "A")
Resultado: 0 1 0 0 0 0 1 p  (p = bit de paridad)
```

**Limitaciones:**
- Solo detecta errores **simples** (1 bit)
- No puede corregir errores
- No detecta errores en número par de bits

**Aplicación:**
Usada en transmisiones serie de bajo nivel, sistemas legados, UART (Universal Asynchronous Receiver-Transmitter)

---

### 19. `byte_tiene_errores(byte, tipoParidad=0)`

**Verificación de Bit de Paridad:**

Función que **verifica** si el bit de paridad de un byte es correcto (o si hay error en la transmisión).

**Algoritmo:**
1. Extraer el bit de paridad (LSB)
2. Extraer el byte de datos (primeros 8 bits más significativos)
3. Contar los 1s en el byte de datos
4. Calcular el bit de paridad esperado
5. Comparar bit recibido vs. bit esperado

**Detección:**
- Si `bit_paridad == bit_esperado`: **Sin error** → devuelve `False`
- Si `bit_paridad ≠ bit_esperado`: **Error detectado** → devuelve `True`

**Ejemplo:**
```python
# Transmisión correcta:
byte_correcto = devolver_byte_con_paridad("A", tipoParidad=0)
byte_tiene_errores(byte_correcto, tipoParidad=0)  # False

# Transmisión con error (flip de 1 bit):
byte_con_error = byte_correcto ^ 0x0100  # Flip un bit
byte_tiene_errores(byte_con_error, tipoParidad=0)  # True
```

**Limitaciones de Detección Simple:**
- Detecta cambios en número **impar** de bits
- **No detecta** cambios en número **par** de bits (error no detectado)
- Por ejemplo, si se invierten 2 bits en la transmisión, el error puede no ser detectado

**Nota:** Es por esto que se necesitan esquemas más robustos como paridad bidimensional (vertical + horizontal)

---

### 20. `codificar_con_paridades(cadena, tipoParidad=0)`

**Esquema de Paridad Bidimensional (2D Parity Check):**

Extensión sofisticada de paridad que detecta **y corrige** errores simples mediante redundancia en dos dimensiones.

**Componentes del Esquema:**
1. **Paridad Vertical**: 1 bit de paridad por cada byte de datos
2. **Paridad Horizontal (Longitudinal)**: 1 bit de paridad por cada columna
3. **Paridad Cruzada**: 1 bit de paridad del total de paridades longitudinales

**Estructura de Datos:**
```
Datos originales (3 bytes):
      Bit:  8 7 6 5 4 3 2 1 
Byte1:      c₁₈ c₁₇ ... c₁₁ | p₁_v  (paridad vertical)
Byte2:      c₂₈ c₂₇ ... c₂₁ | p₂_v
Byte3:      c₃₈ c₃₇ ... c₃₁ | p₃_v
            ---|---|---|---|---|--+
Paridades h: p_h8 p_h7 ... p_h1 | p_c  (paridad cruzada)
            (longitudinal)        
```

**Capacidades Teóricas:**
- Detecta: **Cualquier número de errores** (si el patrón es diferente)
- Corrige: **Un error simple** en posición conocida
- Localiza: Exactamente dónde está el error (intersección de fila+columna con error)

**Algoritmo de Codificación:**
1. Para cada carácter:
   - Calcular paridad vertical
   - Crear byte de 9 bits: 8 de datos + 1 de paridad vertical
2. Para cada columna de la matriz:
   - Calcular paridad horizontal de los 9 bits
3. Calcular paridad cruzada (XOR de todas las paridades horizontales)
4. Retornar: datos con paridades + byte de paridades horizontales + byte de paridad cruzada

**Ejemplo:**
```python
mensaje = "ABC"
resultado = codificar_con_paridades(mensaje, tipoParidad=0)
# Estructura interna (simplificada):
# [A_con_pv, B_con_pv, C_con_pv, paridades_longitudinales, paridad_cruzada]
# Ejemplo: bytearray(b'...')  # Tamaño = 3 + 2 bytes = 5 bytes

# Con bytes simples sería: 3 bytes
# Con paridad: 5 bytes (67% overhead pero detecta y corrige errores)
```

**Ventajas sobre Paridad Simple:**
- Localiza el error exactamente
- Puede corregir 1 error automáticamente
- Detecta patrones de errores múltiples

**Aplicaciones:**
- Transmisión de datos de larga distancia
- Almacenamiento en cintas magnéticas de datos sensibles
- Sistemas aeroespaciales y críticos para seguridad
- RAID (Redundant Array of Independent Disks) - análogo bidimensional

---

### 21. `decodificar_con_paridades(byte_seq, tipoParidad=0)`
**¿Qué hace?**
Lo inverso: verifica todas las paridades y recupera el mensaje original si no hay errores.

---

## 🎯 FUNCIÓN AUXILIAR

### 22. `mostrarListaConIndices(lista)`
**¿Qué hace?**
Solo imprime una lista con su índice de forma bonita.

```python
mostrarListaConIndices(["a", "b", "c"])
# Imprime: [0]=a  [1]=b  [2]=c
```

---

---

# 📝 CONCLUSIÓN: ¿QUÉ ES Y PARA QUÉ SIRVE TODO ESTO?

## El Propósito General

Este código implementa **Teoría de la Información**, una rama de la matemática que responde preguntas como:
- ¿Cuál es la mejor forma de comprimir un mensaje?
- ¿Cómo detectamos si hay errores en una transmisión?
- ¿Cuántos bits necesitamos mínimo para codificar información?

## Las 3 Pilares Principales

### 1️⃣ **COMPRESIÓN DE DATOS** 
Usa algoritmos como Huffman y Shannon-Fano para:
- Hacer archivos más pequeños
- Usados en: ZIP, JPEG, MP3, videos

**Ejemplo real:** Una película de 2GB se comprime a 500MB

---

### 2️⃣ **DETECCIÓN Y CORRECCIÓN DE ERRORES**
Usa técnicas como paridad y distancia de Hamming para:
- Detectar si datos se corrumpieron
- Corregir algunos errores automáticamente
- Usados en: comunicaciones espaciales, QR codes, transmisiones 4G/5G

**Ejemplo real:** El Rover de Marte envía datos a través del espacio; si se pierden bits, la NASA puede recuperarlos

---

### 3️⃣ **ANÁLISIS Y OPTIMIZACIÓN DE CÓDIGOS**
Usa entropía de Shannon y teoremas para:
- Saber si un código es óptimo
- Calcular la eficiencia
- Medir redundancia

**Ejemplo real:** Netflix usa estos conceptos para transmitir video sin buffering

---

## Aplicaciones Prácticas

| Aplicación | Qué Usa |
|-----------|---------|
| **Compresión ZIP** | Huffman + RLE |
| **Imágenes JPEG** | Compresión + Huffman |
| **Códigos QR** | Corrección de errores |
| **Transmisiones 5G** | Paridad + Hamming |
| **Streaming de Video** | Compresión + análisis de entropía |
| **Sistemas Satelitales** | Corrección de errores avanzada |

---

## 🎯 SÍNTESIS INTEGRAL

Este código es una implementación **rigurosa y educativa** de los pilares fundamentales de la Teoría de la Información de Shannon:

### Tres Dominios Principales

**1. COMPRESIÓN (Entropía y Códigos Óptimos)**
- Cuantificación matemática de información mediante entropía
- Algoritmos de codificación óptima (Huffman, Shannon-Fano)
- Verificación del Primer Teorema de Shannon
- Aplicaciones: ZIP, JPEG, MPEG, WebP

**2. DETECCIÓN Y CORRECCIÓN DE ERRORES (Robustez)**
- Técnicas de control de integridad (paridad, Hamming)
- Localización y corrección automática de errores
- Teoremas de detectabilidad y corregibilidad
- Aplicaciones: QR codes, transmisiones satelitales, 5G, RAID

**3. ANÁLISIS Y OPTIMIZACIÓN (Teoría de Códigos)**
- Métricas de eficiencia y redundancia
- Distribuciones de probabilidad empíricas
- Extensiones de fuentes y análisis de grado-n

### Relaciones Matemáticas Clave

```
Entropía H(S) ← Límite inferior fundamental
                      ↓
              Longitud Media L
                      ↓
Eficiencia η = H/L, Redundancia R = 1-η
                      ↓
            Desigualdad de Shannon
        H(S) ≤ L < H(S) + 1
                      ↓
              Óptimalidad del código
```

### Flujo de Aplicación Típica

```
1. Análisis: generarListaParalelasCadenaCaracteresYProbs()
                        ↓
2. Compresión: algoritmo_huffman() o algoritmo_shanon_fano()
                        ↓
3. Validación: cumple_primer_teorema_shannon()
                        ↓
4. Evaluación: calcularRedundanciaYEficiencia()
                        ↓
5. Protección: codificar_con_paridades()
                        ↓
6. Transmisión: codificar_en_byteArray()
```

## 📊 Tabla Comparativa de Métodos

| Técnica | Optimalidad | Corrección | Overhead | Uso |
|---------|------------|-----------|----------|-----|
| Huffman | ✅ Óptimo | ❌ No | Bajo | Compresión |
| Shannon-Fano | ⚠️ Casi óptimo | ❌ No | Bajo | Educativo |
| Paridad Simple | ❌ No | ❌ No | Mínimo | Detección |
| Paridad 2D | ✅ Óptimo (1 error) | ✅ Sí (1 error) | 67% | Crítico |
| Hamming | ✅ Óptimo | ✅ Sí | Moderado | Memoria |

## 🌐 Contexto Histórico

- **Claude Shannon** (1948): Funda la Teoría de la Información
- **David Huffman** (1952): Desarrolla algoritmo de codificación óptima
- **Richard Hamming** (1950): Introduce códigos detectores/correctores
- **Modern Era**: Aplicación universal en todas las comunicaciones digitales

---

**Conclusión:** Cuando usas internet, streaming de video, compresión de archivos, comunicaciones 4G/5G, satélites GPS o escaneas un código QR, **estás usando directamente estos principios y algoritmos de Teoría de la Información**.

Este código es una **encarnación del conocimiento fundamental** que hace funcionar la era digital moderna.

---

**Escrito para:** Estudiantes de Ingeniería en Sistemas, Telecomunicaciones, Informática | **Nivel Académico:** Teoría de la Información (Pregrado Avanzado/Postgrado)
