# Tesoro pirata
En una isla desierta, un grupo de piratas ha trazado un mapa lleno de senderos secretos. Cada sendero tiene un tesoro escondido en alguna parte de su trayecto. Los piratas de la tripulación del infame capitán Jack Amarow quieren esconderse en las intersecciones de los senderos para vigilar sus tesoros. En una intersección se pueden cruzar dos senderos o más. Todas las intersecciones tienen unas palmeras a las que los piratas se pueden encaramar. Mientras más alta la palmera, más difícil es subirse y por tanto más costo tiene.

Tu misión es ayudar a los piratas a encontrar el conjunto mínimo de intersecciones donde deben esconderse para poder vigilar todos los senderos que llevan a sus tesoros y que el costo de subirse en las palmas sea mínimo.


## Resumen

Se tiene un grafo G(V,E) no dirigido donde cada vértice tiene un costo de seleccionarlo (la altura de la palmera).
Se necesita seleccionar un conjunto $V' \subseteq V$ donde se cumple que G'(V',E') donde $E'={<v,e> \in E | v,e \in V'}$ de forma que se cumpla que G'es el cunbimiento menor tal que $E' = E$ y que el costo de seleccionar $V'$ sea mínimo. Llamaremos a este problema Cobertura Mínima de Aristas con Costo Mínimo (CMACM)


## Solución fuerza bruta
El algoritmo usa un acercamiento recursivo para explorar todos los cubrimientos de vértices posibles, apuntando a encontrar el que tiene el menor costo. Mantiene la mejor cobertura encontrada hasta el momento comparando la cantidad de nodos y el costo de cada cubrimiento potencial. Este es un método de fuerza bruta y puede que no sea eficiente con grafos grandes, pero garantiza que encuentra la solución óptima.

### Correctitud

Probar la correctitud de este algoritmo es bastante sencillo, ya que genera todas las combinaciones posibles y devuelve la mejor.

### Complejidad temporal

La complejidad temporal del código dado se puede analizar examinando la función recursiva find_min_cover_aux:

- **Llamadas Recursivas:** La función realiza una llamada recursiva para cada vértice que no está en la cobertura actual. En el peor de los casos, esto significa explorar todos los subconjuntos de vértices.

- **Exploración de Subconjuntos:** Para un grafo con $n$ vértices, hay $2^n$ subconjuntos posibles. La función explora cada subconjunto para encontrar la cobertura mínima.

- **Cálculo de Costos:** Para cada subconjunto, la función calcula el costo y verifica si el subconjunto cubre el grafo. Esto implica verificar la cobertura y actualizar la mejor cobertura y el costo.

- **Caso Base:** El caso base verifica si la cobertura actual cubre el grafo, lo cual toma $O(n)$ tiempo en el peor de los casos (asumiendo que el método is_covered verifica todos los vértices).

Combinando estos factores, la complejidad temporal está dominada por el número de subconjuntos explorados, que es $O(2^n)$. Por lo tanto, la complejidad temporal general del código es:
$O(2^n * n)$

## NP-Completitud

Por la descripción del problema se puede pensar que el problema tiene características donde coincide con el problema Vertex-Cover.

Primero debemos convertir nuestro problema a un problema de decisión, para luego demostrar que este problema de decisión asociado a nuestro problema, es NP-Completo.

### Problema de decisión:
Dada la misma entrada del problema original, junto a 2 valores enteros $k$ y $n$, devuelve verdadero en caso de que exista un subconjunto de vértices de tamaño $n$ con costo $k$ del grafo G, falso en otro caso. Nombremos este problema Cobertura Limitada de Aristas con Costo Limitado de Decisión ($CLACD$).
    
1. Probar que $CLACD \in NP$

    Para esto vamos a partir del concepto de cuando un problema es NP. Un problema P es NP si para cada instancia x del problema que devuelve true, existe un certificado $y$ con $|y|=O(|x|^c)$ para alguna $c$ constante y existe un algoritmo A que toma a $x$ y $y$ como entrada y cumple que $A(x,y) = 1$


    El certificado que vamos a utilizar es un conjunto de vértices, que al ser verificados, cumplen con las condiciones.
    
    $|y|=k$, es el máximo tamaño que puede tener un conjunto de vértices pertenecientes a un grafo G, con $V \in G$. La entrada del problema es $(G(V,E),n,k)$ con un coste en cada vértice, con lo cual $|x| = O(|V|+|E|)$

    $|y|=O(|x|^c) \rightarrow k = O((|V|+|E|)^c)$ para $c=1$ se cumple que $k=O(|V|+|E|)$


2. Seleccionar un porblema de $NPC$ conocido:
    El problema que vamos a utilizar es el problema **Vertex Cover**.

3. Describir un algortimo que compute una función $f$ la cual debe mapear para cada instancia $x$ de **Vertex Cover** a una instancia $f(x)$ de $CLACD$.
    Necesitamos demostrar la existencia de un algoritmo que convierta la entrada del problema **Vertex Cover** a la entrada de nuestro problema y uno que transforme la salida de nuestro problema en la salida del **Vertex Cover**, y que esto ocurra en tiempo polinomial, pudiéramos representar este proceso de la siguiente manera:

    $Input(Vertex Cover) \rightarrow Input(CLACD) \Longrightarrow S \Longrightarrow Output(CLACD) \rightarrow Output(Vertex Cover)$

    Donde S es un algoritmo que resuelve CLACD. La entrada del algoritmo **Vertex Cover** es un grafo G(V,E) y un entero positivo $k$ que representa el tamaño máximo del conjunto de cobertura de vértices que se busca. Un algoritmo que mapee el grafo G en otro G'(V',E) donde &V'={v \in V}& y a cada nodo se le adiciona un costo, el cual es 0; además el número de costo $k$ es 0. Resta entonces convertir la salida de nuestro algoritmo a la salida del **Vertex Cover**. En caso que CLACD de verdadero la salida del **Vertex Cover** es verdadera, de igual forma si da falso.

4. Probar que este algoritmo que computa $f$ se resuelve en tiempo polinomial.

    `Complejidad temporal:`
    *$Input(Vertex Cover) \rightarrow Input(CLACD)$*
    
    Sea la entrada G(V,E), por cada $v \in V$ se crea v' igual a v pero con la adición de un valor de coste igual a 0, esto se realiza $|V|$ veces. Luego por cada par $<v,w> \in E$ se crea el par correspondiente $<v',w'>$ de forma que $<v',w'> \in E'$, esto se realiza $|E|$ veces. Por tanto la complejidad temporal de la conversión es $O(|V|+|E|)$
    $Output(CLACD) \rightarrow Output(Vertex Cover)$

    Ocurre homologamente en sentido contrario, siendo evidente que la complejidad temporal es $O(|V|+|E|)$

    Luego el algoritmo que computa $f$ se hace en tiempo polinomial.


## NP-hard

Vamos a demostrar ahora que el problema $CMACM \in$ **NP-hard**. Para esto nos basaremos en que $CLACD \in NPC$, se puede reducir en $CMACM$. Para esto, al igual que en el caso anterior, vamos a hacer una reducción. Ya seleccionamos un problema que pertenece a $NPC$. Debemos describir un algoritmo que compute $f$, convertir las entradas de $CLACD$ a $CMACM$, es muy sencillo pues ambos algoritmos reciven un grafo, la diferencia es que $CMACM$ irá probando diferentes valores de $k$ y $n$ hasta encontrar los mínimos de ambos valores mientras que $CLACD$ solo recibirá el grafo. Para el caso de convertir la salida de $CMACM$ en la salida de $CLACD$, si la salida del primero es un conjunto vacío de vértices, entonces la salida es -1; sino es vacío, se verifica si la cardinalidad de la salida es menor o igual a $n$ y que el costo es menor o igual a $k$

`Complejidad temporal:`

Convertir las entradas de los algoritmos es $O(1)$ pues estos algoritmos utilizan el mismo grafo de entrada pero con enteros de parámetros que son desechados. Para el caso de las salidas se computa en $O(|V|)$ ya que revisa cada vértice devuelto, siendo la cantidad máxima posible $|V|$, y a la misma vez que se cuenta la cantidad de vértices, se suma el costo total, siendo $O(1)$ para cada vértice.

Hemos demostrado que nuestro problema es **NP-hard**, por tanto es tan difícil como cualquier problema **NP-completo**, para los cuales hasta la fecha no existe solución en tiempo polinomial, por eso brindamos ahora nuestra solución para resolverlo de forma aproximada.

## Solución:

La función `find_min_cover_approx` es un algoritmo greedy de aproximación para encontrar el menor cubrimiento de vértices en un grafo.

- **Emparejamiento Maximal:** El algoritmo comienza encontrando un emparejamiento maximal en el grafo. Un emparejamiento es un conjunto de aristas tal que no hay dos aristas que compartan un vértice común. Un emparejamiento maximal es un emparejamiento que no puede ser extendido añadiendo otra arista.

- **Cobertura de vértices a partir de un emparejamiento:** Una vez que se encuentra un emparejamiento máximo, el conjunto de todos los extremos de las aristas en este emparejamiento forma una cobertura de vértices. Esto se debe a que cada arista en el emparejamiento está cubierta por sus extremos, y dado que el emparejamiento es máximo, cualquier arista que no esté en el emparejamiento debe compartir un vértice con una arista en el emparejamiento.

- **Ratio de Aproximación:** Este enfoque garantiza una aproximación de 2. Esto significa que el tamaño de la cobertura de vértices encontrada es como máximo el doble del tamaño de la cobertura de vértices mínima. Esto se debe a que el tamaño de la cobertura de vértices mínima es al menos el tamaño del emparejamiento máximo, y la cobertura de vértices encontrada por este método es como máximo el doble del tamaño del emparejamiento máximo.