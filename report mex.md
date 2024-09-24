## MEX subsecuencia

### Solución Implementada:

Para la solución de este problema implementamos un algoritmo de ventana deslizante que itera por el array y encuentra los bloques MEX (definición 1.1) del mismo. Cada vez que se encuentra uno de estos bloques MEX se calculan las diferentes divisiones que contienen a este bloque MEX en conjunto con los descubiertos anteriormente. Al terminar la iteración por el array y encontrar todos los bloques MEX Se suma el valor calculado para cada bloque MEX dando como resultado final todas las divisiones validas posibes.

A continuación daremos la información necesaria para entender el funcionamiento y la correctitud de nuestro algoritmo $ \dots $

#### Teorema (1.1):
En un array $A$, una división es válida con el MEX de todos sus subarrays $ = m $ si y solo si $ MEX(A) = m $

En otras palabras: todos los subarrays de una división válida tienen un MEX igual al MEX del array completo.

##### Demostración:
(=>)

Tomemos una división $A1, A2, \dots , An$ válida con $MEX$ de sus subarrays $m$. $ \forall i \in [1, n], MEX(Ai)= m $.

 => $ \forall k \in [0,m], k \in Ai$ (De lo contrario k seria el MEX de Ai) => $\forall k \in [0,m], k \in A$. => $MEX(A) \geq m $MEX(A) \geq m$.

Si $MEX(A) > m$: => $m \in A$ => $ \exist i : m \in Ai$ => $MEX(Ai) \neq m$. CONTRADICCION. => $MEX(A) = m$.

(<=)

Sea $MEX(A) = m$ tomemos una división válida $A1, A2, \dots , An$. Donde $\forall i \in [1,n], MEX(Ai) = \mu $.

Si $ \mu < m $: $\forall i \in [1,n], \mu \notin Ai $ => $ \mu \notin A $ => $MEX(A) = \mu < m$. CONTRADICCION. $ \mu \geq m $.

Si $ \mu > m $: => $\forall i \in [1,n], m \in Ai $ => $ m \in A$ => $MEX(A) \neq m $. CONTRADICCION. $\mu = m$.♠

Sabiendo esto pasemos a una definición importante para la solución del ejercicio.

#### Definición (1.1):
En un array A un bloque MEX es un subarray minimal de A tal que su $MEX$ es igual a $MEX(A)$.

#### Teorema (1.2):
Todo subarray de una división válida de A contiene un bloque MEX.

No consideramos necesaria la demostración de este teorema pero si nos pareció importante mencionarlo.

#### Teorema (1.3):
Sea A un array y Ak un subarray de A, Ak es un bloque MEX si y solo si $ \forall i \in [0,MEX(A)), i \in Ak$ $ \land $ $Ak[0], Ak[len -1] < MEX(A) \land Ak[0],Ak[len -1] \neq Ak[i] \forall i \in (0, len-1)$.

##### Demostración: 
(=>)

$ MEX(Ak) = MEX(A) = m $. Si $\exist i: 0 \leq i < m; i \notin Ak $ => $ MEX(Ak) = i < m $. CONTRADICCION. => $ \forall i \in [0,MEX(A)), i \in Ak $.

Si $ Ak[0] > m $ => Sea $Ak1$ subarray de $Ak$ de $Ak[1] a Ak[len -1]$ => $ MEX[Ak1] = m $ => $Ak$ no es minimal. CONTRADICCION. => $ Ak[0] \leq m $.

Si $Ak[0] = m$. CONTRADICCION TRIVIAL. => $Ak[0] < m$.

(La misma demostración se aplica para $Ak[len -1]$.)

Si $\exist i; Ak[i] = Ak[0]$ => Sea $Ak1$ subarray de $Ak$ de $Ak[1] a Ak[len -1]$ => $ MEX[Ak1] = m $ => $Ak$ no es minimal. CONTRADICCION. => Ak[0] \neq Ak[i] \forall i \in (0, len-1]$.

(La misma demostración se aplica para $Ak[len -1]$.)

(<=)

Al ser Ak un subarray de A, si todos los números mayores o iguales que 0 y menores que $MEX(A)$ pertenecen a Ak => $MEX(Ak)$ es igual a $MEX(A)$. Si los bordes de Ak contienen números únicos menores que $MEX(A)$ => al reducir el tamaño de alguno de los bordes el $MEX(AK)$ sería igual al valor de ese borde que es menor que $MEX(A)$ => Ak es minimal => Ak es un bloque MEX.♠

#### Definición (1.2):
Sea A un array y Ak un subarray de una división válida de A, se le llama $ Bloque $ $ Característico $ de Ak al bloque MEX contenido en Ak cuya posición inicial es más cercana a la posición inicial de Ak.

Conociendo este podemos concretar acerca del funcionamiento de nuestro algoritmo el cual primeramente calcula el MEX del array de entrada. Con este valor calculado el algoritmo busca todos los bloques MEX del array basandose en el Teorema 1.3. Cada vez que encontramos un nuevo bloque MEX añadimos los casos resultantes de las divisiones donde solo él y los bloques previamente descubiertos son bloques característicos. De esta forma al encontrar el último bloque tenemos previamente todos los casos donde él no es bloque característico y añadimos todos donde el si lo es, teniendo para ese momento el total de divisiones válidas del array.

### Complejidad Temporal:

Primeramente tenemos el calcualo del MEX, este se realiza una sola vez por ejecución, al inicio del algoritmo. Aquí tenemos un primer ciclo que intera por el grafo rellenando un diccionario de hallazgos; este primer ciclo realiza n iteraciones y en cada una sus acciones tienen tiempo constante, por lo que su comprejidad es $O(n)$. Luego de este hay un segundo ciclo que itera por todos los números desde 0 hasta el máximo del algoritmo y en cada iteración busca si ese elemento está en el diccionario de hallazgos. Buscar en el diccionario se realiza en tiempo constante y aunque el ciclo se realiza por los números menores al máximo del array este ciclo termina al encontrar el primer valor que no pertenece al array, por lo que no realizará más de n iteraciones, siendo n el tamaño del array; por lo que este ciclo también tiene complejidad de $O(n)$ al igual que el método entero.

Luego de calculado el MEX se hace una iteración por el array. Dentro de esta iteración la mayoría de las operaciónes se realizan en tiempo constante, a exepción de dos ciclos independientes. El primero de estos sucede cuando se encuentra un bloque, para obtenerer el valor del inicio de ese bloque se recorre un array del tamaño del MEX previamente calculado; este valor es siempre menor o igual a n+1 por lo que el ciclo tiene complejidad $O(n)$. El otro ciclo ocurre justo después, donde se recorren todos los bloques ya encontrados para calcular los casos que añade este nuevo bloque; El número de bloques en el array es siempre menor o igual que n, por lo que este ciclo es también $O(n)$. Por lo tanto la complejidad final del ciclo entero sería de $O(n^{2})$.

Hay un último ciclo que itera por los bloques para sacar la suma que devuelve el algoritmo como resultado final; al igual que en el analis anterior, este ciclo es en $O(n)$.

Por lo tanto la complejidad temporal de nuestro algoritmo general será de $O(n)$. Aunque he de mencionar que tanto el MEX como el número de bloques, a pesar de tener valores máximos de $n+1$ y $n$ respectivamente, suelen tener valores bastante menores por lo que los tiempos del algoritmo en muchos de los casos tienen valores cercanos a los de un algoritmo lineal. 


### Línea de Pensamiento:

Para la solución de este ejercicio primeramente analizamos las especificaciones del problema y las propiedades que podían tener las soluciones. En este análisis construimos el Teorema 1.1. Teniendo una idea general del problema escribimos un código de "fuerza bruta" para comprobar con ejemplos la posible correctitud de futuros algoritmos.

Con la intención de llegar a alguna solución "decente" intentamos buscar cotas para las soluciones válidas, con la esperanza de poder reducir los casos a probar. La única cota rescatable de entre las que encontramos fue que: el número de subarrays de una división válida es debe ser menor o igual al número de veces que aparece el número menor al MEX que menos aparece en el array. Esta cota no tuvo mucha utilidad práctica pero pensamos que pudo ser la idea inicial para la futura definición de los bloques MEX.

Una vez saliendo de la pura teoría y entrando más en las técnicas para abordar el ejercicio, nuestros pensamientos estaban más encaminados en buscar una forma de "picar" el problema para trabajar con subproblemas más pequeños. Ideas como picar a la mitad, o picar por el mayor o menor elemento no dieron ningún resultado relevante, la primera idea decente surge junto con la idea de los bloques MEX. La idea era buscar el primer y el último de estos bloques y llamar recursivo al subarray que quedara en medio de estos. Esta posible solución no fue viable ya que en el subarray podían surgir multiples casos distnintos (un solo bloque dentro, dos bloques que se interceptan, bloques que se interceptan con los extremos, etc...) y no había una forma concreta de calcular las divisiones totales de manera recursiva.

En ese momento pasamos a un  enfoque más iterativo, continuando con la idea de los bloques MEX. Intentamos una primera iteración para encontrar todos los bloques y luego relacionarlos entre ellos para calcular las divisiones totales, pero la fórmula al calcular la interacción entre estos era compleja y crecía con cada nuevo caso que encontrabamos, por lo que en el caso de encontrar finalmente una fórmula que abarcara todos los casos, esta sería muy compleja y la demostración de su correctitud lo sería aún más.

Fue entonces cuando decidimos utilizar el enfoque de contar los casos a medida que encontrabamos los bloques de forma tal que no contaramos ninguno de esos casos dos veces. Esta idea prometía ser, no solo más ordenada y sencilla, también era más eficiente que todas las anteriores que habiamos pensado. De esta forma, luego de afinar la manera de añadir los casos nuevos para que fuera lo más "limpio" posible, se finalizó la creación de nuestro algoritmo de ventana deslizante que da solución a nuestro problema de manera eficiente.