# Teoría de Canales Estocásticos: Análisis Matemático e Implementación

## 📚 Introducción Conceptual

Un **canal estocástico** (o canal ruidoso) es un modelo probabilístico que describe la transmisión de información a través de un medio que puede introducir perturbaciones, errores o corrupción de datos.

### Definición Formal

Un canal discreto sin memoria (DMC - Discrete Memoryless Channel) se define como una tupla $\mathcal{C} = (X, Y, p_{Y|X})$ donde:

- $X = \{x_1, x_2, \ldots, x_m\}$ es el **alfabeto de entrada** (símbolos transmitidos)
- $Y = \{y_1, y_2, \ldots, y_n\}$ es el **alfabeto de salida** (símbolos recibidos)
- $p_{Y|X}(y_j | x_i)$ es la **matriz de transición** que define las probabilidades condicionales de recibir $y_j$ dado que se transmitió $x_i$

Este código implementa herramientas para **análisis riguroso** de canales, cálculo de capacidad, información mutua y probabilidades de error.

---

## 🔧 FUNCIONES DE CONSTRUCCIÓN DE MATRICES

### 1. `generar_matriz_canal(cadena_sin_codificar, cadena_salida)`

**Descripción:**
Construye la **matriz de transición del canal** (matriz de probabilidades condicionales) a partir de dos cadenas empíricas: una de entrada observada y una de salida observada.

**Proceso Matemático:**

$$P(y_j | x_i) = \frac{\text{Número de veces que } y_j \text{ se observa cuando se transmitió } x_i}{\text{Número total de veces que se transmitió } x_i}$$

**Algoritmo:**
1. Extraer alfabetos únicos de ambas cadenas (ordenados alfabéticamente)
2. Crear matriz de conteos: $C[i][j]$ = número de pares $(x_i, y_j)$ observados
3. Normalizar por filas: dividir cada elemento $C[i][j]$ por $\sum_j C[i][j]$ (suma de la fila)
4. Redondear a 3 decimales para precisión

**Ejemplo:**
```python
entrada = "abcacaabbcacaabcacaaabcaca"
salida = "01010110011001000100010011"

# Resultado: matriz 3×2 donde:
# Filas: a, b, c (entrada)
# Columnas: 0, 1 (salida)
# Valores: P(salida | entrada)
```

**Interpretación:**
Cada fila representa la distribución de probabilidad sobre las salidas posibles condicionada a una entrada específica.

---

### 2. `a_priori(cadena)`

**Descripción:**
Calcula la **distribución de probabilidades a priori** (distribución marginal de entrada) a partir de una cadena observada.

**Fórmula:**
$$P(x_i) = \frac{\text{Ocurrencias de } x_i}{|\text{cadena}|}$$

**Retorno:**
Lista de probabilidades ordenadas alfabéticamente, paralela a las filas de la matriz del canal.

**Relación con la Matriz del Canal:**
```
Estructura de datos:
P_priori = [P(a), P(b), P(c)]  ← paralela a filas

Matriz =  [[P(y1|a), P(y2|a)],
           [P(y1|b), P(y2|b)],
           [P(y1|c), P(y2|c)]]
```

---

## 📊 MATRICES DERIVADAS DEL CANAL

### 3. `generar_probs_salida(probs_priori, matriz_canal)`

**Definición Matemática (Probabilidades Marginales de Salida):**

$$P(y_j) = \sum_{i=1}^{m} P(x_i) \cdot P(y_j | x_i)$$

**Descripción:**
Calcula la **distribución de probabilidades de salida** (marginales), aplicando el teorema de la probabilidad total sobre todas las posibles entradas.

**Interpretación:**
La probabilidad de observar un símbolo en la salida del canal es la suma ponderada de todas las formas posibles en que ese símbolo puede ser generado desde las entradas.

**Ejemplo:**
```python
P_entrada = [0.3, 0.3, 0.4]
P_salida = generar_probs_salida(P_entrada, matriz_3x2)
# Resultado: [P(y1), P(y2)] distribución marginal de salida
```

---

### 4. `generar_matriz_eventos_simultaneos(probs_priori, matriz_canal)`

**Definición Matemática (Probabilidades Conjuntas):**

$$P(x_i, y_j) = P(x_i) \cdot P(y_j | x_i)$$

**Descripción:**
Genera la **matriz de probabilidades conjuntas** $P(X, Y)$, que representa la probabilidad de que simultáneamente se transmita $x_i$ y se reciba $y_j$.

**Propiedades:**
- Cada elemento está entre 0 y 1
- La suma de todos los elementos es 1 (forma una distribución de probabilidad)
- Es la información más completa sobre el comportamiento del canal con distribución de entrada conocida

**Relación Matemática:**
```
Sumando por filas: ∑_j P(x_i, y_j) = P(x_i)
Sumando por columnas: ∑_i P(x_i, y_j) = P(y_j)
Sumando todo: ∑_i ∑_j P(x_i, y_j) = 1
```

---

### 5. `generar_matriz_posteriori(probs_priori, matriz_canal)`

**Definición Matemática (Teorema de Bayes):**

$$P(x_i | y_j) = \frac{P(x_i, y_j)}{P(y_j)} = \frac{P(x_i) \cdot P(y_j | x_i)}{\sum_{i'} P(x_{i'}) \cdot P(y_j | x_{i'})}$$

**Descripción:**
Calcula la **matriz de probabilidades posteriori**, que representa la creencia sobre cuál entrada se transmitió **dado que** se observó una salida específica. Este es el cálculo fundamental para:
- **Demodulación y detección** en comunicaciones
- **Corrección de errores** en canales ruidosos
- **Toma de decisiones óptimas** en receptores

**Interpretación:**
Responde la pregunta: "Si observé $y_j$ a la salida del canal, ¿cuál es la probabilidad de que se haya transmitido cada $x_i$?"

**Caso Especial - División por Cero:**
Si $P(y_j) = 0$ (evento imposible), se asigna $P(x_i | y_j) = 0$ para evitar errores numéricos.

---

## 📈 FUNCIONES DE VISUALIZACIÓN Y UTILIDAD

### 6. `mostrar_matriz_encuadrada(matriz, etiquetas_filas, etiquetas_columnas)`

**Descripción:**
Imprime una matriz de forma elegante con:
- Etiquetas para filas y columnas
- Formato numérico consistente (4 decimales)
- Separadores visuales (líneas)
- Alineación clara

**Uso Típico:**
```python
mostrar_matriz_encuadrada(matriz_posteriori, 
                         etiquetas_filas=['A', 'B', 'C'],
                         etiquetas_columnas=['0', '1', '2'])
```

### 7. `info(num)`

**Definición:**
$$I(x) = -\log_2(x) \text{ si } x \neq 0, \quad \text{si no } 0$$

Función de autoinformación (en bits). Misma definición que en `shanon_huffman.py`.

---

## 🧮 FUNCIONES DE ENTROPÍA E INFORMACIÓN

### 8. `calcular_entropia_salida(probs_priori, matriz_canal)`

**Definición Matemática:**

$$H(Y) = -\sum_{j=1}^{n} P(y_j) \log_2 P(y_j)$$

**Descripción:**
Calcula la **entropía de la salida del canal**, que mide la incertidumbre en los símbolos observados a la salida.

**Propiedades:**
- Representa cuánta información (en bits) contiene en promedio cada símbolo de salida
- Depende tanto de la matriz del canal como de la distribución de entrada
- Máximo valor: $\log_2 n$ (cuando salidas equiprobables)

---

### 9. `lista_entropias(probs_priori, matriz_canal)`

**Retorna:**
Tupla $(H(X), [H(X|y_1), H(X|y_2), \ldots, H(X|y_n)])$

**Definiciones Matemáticas:**

**Entropía A Priori (entrada):**
$$H(X) = -\sum_{i=1}^{m} P(x_i) \log_2 P(x_i)$$

**Entropía Posteriori Condicional (dado cada símbolo de salida):**
$$H(X | y_j) = -\sum_{i=1}^{m} P(x_i | y_j) \log_2 P(x_i | y_j)$$

**Descripción:**
- $H(X)$ es la incertidumbre sobre la entrada **antes** de recibir nada
- $H(X|y_j)$ es la incertidumbre remanente sobre la entrada **después** de observar la salida $y_j$

**Interpretación:**
La reducción $H(X) - H(X|y_j)$ representa cuánta información sobre la entrada proporciona observar $y_j$.

---

### 10. `calcular_equivocacion(probs_priori, matriz_canal)`

**Definiciones Matemáticas:**

**Equivocación (Pérdida de Información - Confusión):**
$$H(X|Y) = \sum_{j=1}^{n} P(y_j) \cdot H(X|y_j)$$

Promedio ponderado de las entropías condicionales posteriori.

**Pérdida (Ruido):**
$$H(Y|X) = \sum_{i=1}^{m} P(x_i) \cdot H(Y|x_i)$$

donde $H(Y|x_i) = -\sum_{j} P(y_j|x_i) \log_2 P(y_j|x_i)$

**Descripción:**
- **$H(X|Y)$ (Equivocación):** Incertidumbre remanente sobre la entrada **después** de observar la salida. Representa el error potencial en la decodificación.
- **$H(Y|X)$ (Pérdida):** Entropía de la salida condicionada a la entrada. Representa cuánta información se pierde en la transmisión.

**Relación Fundamental:**
$$I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$$

---

### 11. `calcular_entropia_afin(probs_priori, matriz_canal)`

**Definición Matemática (Entropía Conjunta):**

$$H(X,Y) = -\sum_{i,j} P(x_i, y_j) \log_2 P(x_i, y_j)$$

**Descripción:**
Entropía del sistema conjunto $(X, Y)$. Mide la incertidumbre total en el par entrada-salida.

**Relación con otras Entropías:**
$$H(X,Y) = H(X) + H(Y|X) = H(Y) + H(X|Y)$$

---

### 12. `calcular_informacion_mutua(probs_priori, matriz_canal)`

**Definición Matemática (Información Mutua):**

$$I(X;Y) = \sum_{i,j} P(x_i, y_j) \log_2 \left( \frac{P(x_i, y_j)}{P(x_i) P(y_j)} \right)$$

**Descripción:**
Cuantifica la **cantidad de información compartida** entre entrada y salida del canal. Mide cuánta información sobre la entrada se puede obtener observando la salida.

**Propiedades Teóricas:**
- $I(X;Y) \geq 0$ (siempre no negativa)
- $I(X;Y) = 0$ si y solo si $X$ e $Y$ son independientes
- $I(X;Y) = H(X)$ si el canal es sin ruido (decodificación perfecta)
- $I(X;Y) = H(X) - H(X|Y)$ (información remanente después de la transmisión)

**Interpretación:**
Es el parámetro fundamental para la **Capacidad del Canal** (Shannon).

---

## 🔍 CLASIFICACIÓN DE CANALES

### 13. `es_sin_ruido(matriz_canal)`

**Definición:**
Un canal es **sin ruido** (noiseless) si cada columna contiene exactamente un elemento no nulo.

**Interpretación:**
Para cada salida $y_j$, existe exactamente una entrada $x_i$ que puede producirla. No hay ambigüedad: conocer la salida determina unívocamente la entrada.

**Propiedad Matemática:**
$$I(X;Y) = H(X)$$

(Toda la información de entrada se preserva en la salida)

---

### 14. `es_determinante(matriz_canal)`

**Definición:**
Un canal es **determinante** (deterministic) si cada fila contiene exactamente un elemento no nulo.

**Interpretación:**
Para cada entrada $x_i$, la salida $y_j$ está determinada de forma unívoca (no hay aleatoriedad en la transmisión desde el lado de entrada).

**Propiedad Matemática:**
$$H(Y|X) = 0$$

(No hay pérdida de información; el ruido viene de la ambigüedad en la decodificación)

---

### 15. `es_canal_uniforme(matriz_canal)`

**Definición:**
Un canal es **uniforme** si cada fila de la matriz de transición es una permutación de la primera fila.

**Interpretación:**
El comportamiento probabilístico es "simétrico" en todas las entradas: cambiar de entrada mantiene la distribución sobre salidas (solo cambia el orden).

**Propiedad Importante:**
$$H(Y|X) = \text{constante}$$

(Pérdida de información independiente de la entrada transmitida)

**Capacidad de Canal Uniforme:**
$$C = \log_2 m - H(Y|X)$$

---

## 🔗 OPERACIONES CON CANALES

### 16. `generar_matriz_compuesta(A, B)`

**Descripción:**
Multiplica dos matrices de transición de canales para obtener el canal **compuesto** o en **cascada**.

**Interpretación Física:**
Si $A$ representa un canal discreto y $B$ representa otro canal discreto, el producto $A \times B$ representa pasar la salida de $A$ como entrada a $B$.

**Matrices Requeridas:**
- Dimensiones: $A$ es $m \times n$, $B$ es $n \times p$
- Resultado: matriz $m \times p$ (canal compuesto)

**Fórmula:**
$$P(z_k|x_i) = \sum_{j=1}^{n} P(y_j|x_i) \cdot P(z_k|y_j)$$

---

### 17. `_verificar_proporcionalidad(matriz, col_a, col_b, tol)`

**Descripción:**
Verifica si dos columnas de una matriz son **proporcionales** (dentro de tolerancia numérica).

**Matemáticamente:**
Dos columnas son proporcionales si $\exists k : col_a[i] = k \cdot col_b[i] \; \forall i$

**Uso Interno:**
Paso intermedio para simplificar canales mediante reducción de columnas combinables.

---

### 18. `son_columnas_combinables(matriz, col1, col2)`

**Descripción:**
Determina si dos columnas pueden ser **combinadas** (fusionadas) sin perder información.

**Criterio:**
Dos columnas son combinables si son proporcionales en **cualquier dirección** (considerando ambas direcciones de proporcionalidad).

**Significado Teórico:**
Las salidas correspondientes a esas columnas son estadísticamente indistinguibles desde el receptor; combinarlas simplifica el canal sin cambiar sus propiedades esenciales.

---

### 19. `generar_matriz_determinante(matriz, col1, col2)`

**Descripción:**
Crea una **matriz de determinante** $D$ para combinar dos columnas especificadas en una sola.

**Operación:**
Genera una matriz que, multiplicada con la matriz del canal, produce una versión reducida combinando las dos columnas.

---

### 20. `generar_matriz_reducida(matriz_de_un_canal)`

**Descripción:**
Realiza **todas las reducciones posibles** de un canal combinando columnas proporcionales de forma iterativa.

**Algoritmo:**
```
MIENTRAS haya reducciones posibles:
    POR CADA par de columnas:
        SI son combinables:
            Crear matriz D
            Multiplicar canal × D
            Repetir desde inicio
```

**Resultado:**
Canal canónico o **forma reducida** equivalente, con número mínimo de salidas distinguibles.

---

## ⚡ CAPACIDAD DEL CANAL

### 21. `calcular_capacidad_canal(matriz_canal)`

**Definición Teórica (Capacidad de Shannon):**

$$C = \max_{P(X)} I(X;Y) \text{ (bits por símbolo)}$$

**Fórmulas por Tipo de Canal:**

**1. Canal Determinante** (deterministic):
$$C = \log_2 n \quad (n = \text{número de salidas})$$

**2. Canal Sin Ruido** (noiseless):
$$C = \log_2 m \quad (m = \text{número de entradas})$$

**3. Canal Uniforme:**
$$C = \log_2 m - H(Y|X)$$

donde $H(Y|X)$ es la entropía condicional (constante para canales uniformes).

**Descripción:**
La capacidad es la **tasa máxima de información** (en bits) que se puede transmitir por símbolo del canal de forma confiable.

**Teorema de Shannon:**
Para cualquier $R < C$ (tasa menor que capacidad), existe un código que permite transmitir con error arbitrariamente pequeño.

---

### 22. `estimar_capacidad_canal_binario(matriz_canal, paso)`

**Descripción:**
Estima la capacidad de un **canal binario** probando distribuciones de entrada uniformes según un paso especificado.

**Algoritmo:**
1. Para probabilidades a priori $p = 0, \text{paso}, 2 \cdot \text{paso}, \ldots, 1$:
   - Calcular información mutua $I(X;Y)$ para $P(x_1) = p, P(x_2) = 1-p$
2. Retornar el máximo de información mutua y su probabilidad asociada

**Retorna:**
- Capacidad estimada (máximo de $I(X;Y)$)
- Probabilidad a priori que produce ese máximo

**Precisión:**
Inversamente proporcional al `paso`: paso más pequeño → estimación más precisa (pero más cálculos).

**Ejemplo:**
```python
matriz_binaria = [[0.6, 0.4], [0.2, 0.8]]
capacidad, probs = estimar_capacidad_canal_binario(matriz_binaria, 0.001)
# paso=0.001 realiza 1001 iteraciones
```

---

## 🎯 PROBABILIDAD DE ERROR Y DECISIÓN

### 23. `calcular_probabilidad_error(probs_priori, matriz_canal)`

**Descripción:**
Calcula la **probabilidad de error mínima** usando la **regla de decisión ML (Maximum Likelihood)**.

**Algoritmo de Decisión:**

1. **Regla de decisión:** Para cada salida $y_j$, decidir que se transmitió:
   $$\hat{x}_j = \arg\max_i P(x_i | y_j)$$

2. **Probabilidad de acierto dado $x_i$ transmitido:**
   $$P(\text{acierto}|x_i) = \sum_{j: \hat{x}_j = x_i} P(y_j|x_i)$$

3. **Probabilidad de error dado $x_i$ transmitido:**
   $$P(\text{error}|x_i) = 1 - P(\text{acierto}|x_i)$$

4. **Probabilidad de error total:**
   $$P_e = \sum_{i=1}^{m} P(x_i) \cdot P(\text{error}|x_i)$$

**Interpretación:**
Es el error mínimo alcanzable con un decodificador óptimo (ML).

**Ejemplo:**
```python
matriz = [[0.6, 0.3, 0.1], 
          [0.1, 0.8, 0.1],
          [0.3, 0.3, 0.4]]
probs = [4/15, 3/15, 8/15]
Pe = calcular_probabilidad_error(probs, matriz)
# Resultado: probabilidad de error con decisión óptima
```

---

## 🎓 SÍNTESIS INTEGRAL: TEORÍA DE CANALES

### Conceptos Fundamentales

**1. Transmisión de Información:**
$$\text{Fuente} \xrightarrow{P(X)} \text{Canal} \xrightarrow{P(Y|X)} \text{Receptor}$$

**2. Medidas Clave:**
| Concepto | Símbolo | Significado |
|----------|---------|-----------|
| Entropía entrada | $H(X)$ | Incertidumbre sobre entrada |
| Entropía salida | $H(Y)$ | Incertidumbre sobre salida |
| Entropía conjunta | $H(X,Y)$ | Incertidumbre total |
| Equivocación | $H(X\|Y)$ | Incertidumbre remanente (error potencial) |
| Pérdida | $H(Y\|X)$ | Información perdida en el canal |
| Información mutua | $I(X;Y)$ | Información compartida |

**3. Relaciones Teóricas:**
$$H(X,Y) = H(X) + H(Y|X)$$
$$I(X;Y) = H(X) + H(Y) - H(X,Y)$$
$$I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$$

**4. Capacidad:**
$$C = \max_P I(X;Y)$$

Tasa máxima de transmisión confiable (en bits/símbolo).

### Clasificación de Canales

| Tipo | Propiedad | $I(X;Y)$ | $C$ |
|------|----------|---------|-----|
| **Sin Ruido** | Cada salida de 1 entrada | $H(X)$ | $\log_2 m$ |
| **Determinante** | Cada entrada → 1 salida | $H(Y)$ | $\log_2 n$ |
| **Uniforme** | Filas son permutaciones | Función de $P(X)$ | $\log_2 m - H_0$ |
| **General** | Ruido en ambas direcciones | $\leq \min(H(X), H(Y))$ | $\leq \min(H(X), H(Y))$ |

### Aplicaciones Prácticas

1. **Comunicaciones Digitales:** Diseño de moduladores/demoduladores
2. **Almacenamiento:** Códigos correctores de errores
3. **Redes:** Asignación óptima de potencia y recursos
4. **Criptografía:** Análisis de seguridad de canales
5. **Compresión:** Codificación de fuentes para canales ruidosos

---

## 📈 Ejemplo Completo de Análisis

```python
# Dados
entrada = "1101011001..."
salida = "1001111111..."

# Paso 1: Construir matriz del canal
matriz = generar_matriz_canal(entrada, salida)

# Paso 2: Obtener distribución de entrada
P_entrada = a_priori(entrada)

# Paso 3: Calcular derivadas
P_salida = generar_probs_salida(P_entrada, matriz)
P_simul = generar_matriz_eventos_simultaneos(P_entrada, matriz)
P_post = generar_matriz_posteriori(P_entrada, matriz)

# Paso 4: Analizar entropías
H_entrada, H_post_lista = lista_entropias(P_entrada, matriz)
H_eq, H_perd = calcular_equivocacion(P_entrada, matriz)

# Paso 5: Medir información
I_mutua = calcular_informacion_mutua(P_entrada, matriz)

# Paso 6: Clasificar canal
print(f"¿Sin ruido? {es_sin_ruido(matriz)}")
print(f"¿Determinante? {es_determinante(matriz)}")
print(f"¿Uniforme? {es_canal_uniforme(matriz)}")

# Paso 7: Capacidad y decisión
C = calcular_capacidad_canal(matriz)
P_error = calcular_probabilidad_error(P_entrada, matriz)
```

---

**Conclusión:** El análisis de canales estocásticos es la base teórica para toda comunicación digital confiable. Estos conceptos permiten diseñar sistemas óptimos que alcanzan los límites fundamentales establecidos por Shannon.

