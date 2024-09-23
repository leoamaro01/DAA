# Problema

Rodrigo es el maestro de una academia de magia y debe organizar y clasificar sus ingredientes mágicos. Son tan mágicos que, consumidos de la forma adecuada, te permiten ver criaturas fantásticas y luces de colores, dejando poca resaca (Rodrigo no los consume pues es un maestro sano). Tiene dos estantes mágicos, uno llamado "a" y otro llamado "b", ambos con $n$ frascos de pociones, cada uno etiquetado con un número del 1 al $n$. Cada frasco está en un lugar aleatorio en los estantes, pero el número en cada frasco es único en cada estante.

Tu tarea es ayudar a Rodrigo a organizar ambos estantes en el orden correcto, de modo que los números en los frascos estén en orden ascendente de izquierda a derecha en ambos estantes. Sin embargo, estos estantes mágicos sólo se pueden mover siguiendo unas reglas:

1. Puedes elegir cualquier número $i$ entre 1 y $n$;
2. Encuentra el frasco en el estante "a" que tiene el número $i$ y cambia su posición con el frasco en la posición $i$;
3. Luego, encuentra el frasco en el estante "b" que tiene el número $i$ y cambia su posición con el frasco en la posición $i$.

Tu objetivo es organizar ambos estantes con el menor número de movimientos posible, asegurándote de que todos los frascos en ambos estantes estén en el orden correcto al finalizar la tarea.

# Solución

Para solucionar el problema utilizamos programación dinámica, dado que para lograr la cantidad de pasos óptimos es debido tener en cuenta ramificaciones que pueden ocurrir hasta $n - 2$ pasos después de realizar un movimiento, lo cuál hace imposible lograr un algoritmo que lo resuelva sin probar todas (o casi todas) las soluciones posibles.

Intentamos utilizar un algoritmo greedy, que en cada paso analizaba todos los posibles movimientos y escogía el que más pociones ordenaba a la vez, y este funcionaba en casos aleatorios más de un 90% de las veces y en $O(n^2)$, pero cometía errores ya que podían ocurrir algunas estructuras en las que tomar una decisión que arreglaba menos pociones, permitía arreglar más en el paso próximo, o en 2 pasos más adelante, y así sucesivamente.

En este punto también notamos que en el árbol de estados de los arrays, muchos estados se repetían, en particular cuando se seleccionaba un número $i$ y después otro $j$, se obtenía siempre el mismo resultado si escojías $j$ y después $i$ (lo cual se demostrará mas adelante para la complejidad temporal).

Entonces queda programación dinámica como última (y bastante buena) opción, la cual implementaríamos utilizando memoización. Pero hay un problema. 

El código

```python
def dynamic_potion_sort_aux(A: list[int], B: list[int], moves: dict[str, list[int]]):
    if (A, B) in moves:
        return moves[(A, B)]
```

sería una implementación típica de memoización en $O(1)$, donde los estados que ya se calcularon devuelven su resultado inmediatamente.

Sin embargo `A` y `B` son listas, las cuales son mutables, y los objetos mutables no son hasheables, por tanto no pueden ser utilizados como llave de diccionarios (al menos no en $O(1)$), por lo que tuvimos que recurrir a

```python
def dynamic_potion_sort_aux(A: list[int], B: list[int], moves: dict[str, list[int]]):
    list_repr = (tuple(A), tuple(B))
    if list_repr in moves:
        return moves[list_repr]
```

Que realiza $O(2n)$ operaciones en simplemente comprobar si ya se calculó ese estado. Por lo tanto encontramos una manera de representar las listas usando números binarios, aprovechandonos de que python tiene ints de tamaño arbitrario, no necesitamos utilizar arrays de bytes ni nada por el estilo.

Sea la lista:

$[5, 3, 1, 2, 4]$

una lista válida para el problema, bien podría tomar el lugar de A o de B, ¿cómo podemos representarla en binario?

Sea $c = ceil(log2(n))$ (en este caso $n = 5$, $c = 3$) el exponente mas pequeño tal que $2^c > n$, también conocido como la cantidad mínima de bits con la que podemos representar cualquier número entre $1$ y $n$, podemos representar la lista anterior de la siguiente manera (en `big endian`):

$100$ $010$ $001$ $011$ $101$

Esto se puede calcular para ambas listas en $O(n)$ una sola vez en todo el algoritmo, luego solo es cuestión de mantener estos identificadores actualizados cuando se hagan swaps. Para hacer un swap utilizaremos las operaciones bit a bit de OR `|`, XOR `^`, y shifting `<<`, de manera tal que sí queremos cambiar el elemento en la $i$-esima posición de valor $r$ a valor $k$, hacemos:

```python
identificador ^= r << (i * c) # Esto convierte la í-esima sección a ceros
identificador |= k << (i * c) # Esto hace que el valor de la sección sea k
```

Entonces hacemos eso para las dos secciones que se quieran intercambiar, y así se mantiene actualizada la representación de las listas en $O(1)$ (aunque con una constante bastante grande, más sobre esto después) cada vez que se hace un swap.

## Código final

```python

def dynamic_potion_sort(A: list[int], B: list[int]):
    moves = {}
    n = len(A)

    indexes_A = [-1] * n
    indexes_B = [-1] * n

    for i in range(n):
        indexes_A[A[i] - 1] = i
        indexes_B[B[i] - 1] = i

    bits_per_item = int(ceil(log2(n)))

    initial_identifier_A = A[n - 1]
    initial_identifier_B = B[n - 1]

    for i in range(n - 2, -1, -1):
        initial_identifier_A <<= bits_per_item
        initial_identifier_A |= A[i]

        initial_identifier_B <<= bits_per_item
        initial_identifier_B |= B[i]

    return dynamic_potion_sort_aux(
        A,
        B,
        moves,
        indexes_A,
        indexes_B,
        (initial_identifier_A, initial_identifier_B),
        bits_per_item,
    )


def dynamic_potion_sort_aux(
    A: list[int],
    B: list[int],
    moves: dict[tuple[int, int], list[int]],
    indexes_A: list[int],
    indexes_B: list[int],
    lists_repr: tuple[int, int],
    bits_per_item: int,
) -> list[int]:
    if lists_repr in moves:
        return moves[lists_repr]

    n = len(A)

    best_swaps_count = -1
    best_swaps = []
    best_swap_elem = -1
    for i in range(n):
        elem = i + 1

        # skip item if correct
        if A[i] == elem and B[i] == elem:
            continue

        A_item_at_i = A[i]
        B_item_at_i = B[i]

        i_index_A = indexes_A[i]
        i_index_B = indexes_B[i]

        # swap potions
        swap_items(A, i, i_index_A)
        swap_items(B, i, i_index_B)

        # update indexes array
        swap_items(indexes_A, A_item_at_i - 1, i)
        swap_items(indexes_B, B_item_at_i - 1, i)

        # update lists representation
        new_A_repr = (lists_repr[0] ^ (A_item_at_i << (bits_per_item * i))) ^ (
            (i + 1) << (bits_per_item * i_index_A)
        )
        new_A_repr |= (A_item_at_i << (bits_per_item * i_index_A)) | (
            (i + 1) << (bits_per_item * i)
        )

        new_B_repr = (lists_repr[1] ^ (B_item_at_i << (bits_per_item * i))) ^ (
            (i + 1) << (bits_per_item * i_index_B)
        )
        new_B_repr |= (B_item_at_i << (bits_per_item * i_index_B)) | (
            (i + 1) << (bits_per_item * i)
        )

        swaps = dynamic_potion_sort_aux(
            A,
            B,
            moves,
            indexes_A,
            indexes_B,
            (new_A_repr, new_B_repr),
            bits_per_item,
        )

        # revert swap
        swap_items(A, i, i_index_A)
        swap_items(B, i, i_index_B)

        # revert indexes array update
        swap_items(indexes_A, A_item_at_i - 1, i)
        swap_items(indexes_B, B_item_at_i - 1, i)

        if best_swaps_count == -1 or len(swaps) < best_swaps_count:
            best_swaps = swaps
            best_swaps_count = len(swaps)
            best_swap_elem = elem

    if best_swaps_count == -1:
        return []

    result = [best_swap_elem, *best_swaps]

    moves[lists_repr] = result

    return result


def swap_items(A: list[int], index1: int, index2: int):
    temp = A[index1]
    A[index1] = A[index2]
    A[index2] = temp

```


## Correctitud

La idea del algoritmo es particularmente simple, comienza con los arrays de pociones `A` y `B`, y prueba recursivamente todas las acciones posibles. Tras probar cada una devuelve la que llegó a la solución en menos pasos. No creemos que el backtracking requiera demostración formal alguna.

## Complejidad temporal

Para realizar el intercambio de pociones, según la descripción del problema, es necesario encontrar en que posición se encuentra la poción $i$, para poder intercambiar su lugar con la poción que está en la posición $i$ del array. Para acelerar estas búsquedas se crean dos arrays llamados `indexes_A` e `indexes_B`, donde el elemento $i$ del array contiene la posición en que se encuentra la poción $i$ en A o B correspondientemente, lo cual hace que la operación de swappeo sea $O(1)$ a costo de un paso que se ejecuta una sola vez en $O(n)$, y de mantenerlas actualizadas para cada llamada del array, lo cual se hace con un swappeo en $O(1)$.

```python
def swap_items(A: list[int], index1: int, index2: int):
    temp = A[index1]
    A[index1] = A[index2]
    A[index2] = temp
```

Al caso, la función `swap_items` intercambia dos elementos en un array en un evidente $O(1)$.

Entonces el método de preparación:

```python lineNumbers
1   def dynamic_potion_sort(A: list[int], B: list[int]):
2       moves = {}
3       n = len(A)
4   
5       indexes_A = [-1] * n
6       indexes_B = [-1] * n
7   
8       for i in range(n):
9           indexes_A[A[i] - 1] = i
10          indexes_B[B[i] - 1] = i
11  
12      bits_per_item = int(ceil(log2(n)))
13  
14      initial_identifier_A = A[n - 1]
15      initial_identifier_B = B[n - 1]
16
17      for i in range(n - 2, -1, -1):
18          initial_identifier_A <<= bits_per_item
19          initial_identifier_A |= A[i]
20  
21          initial_identifier_B <<= bits_per_item
22          initial_identifier_B |= B[i]
23  
24      return dynamic_potion_sort_aux(
25          A,
26          B,
27          moves,
28          indexes_A,
29          indexes_B,
30          (initial_identifier_A, initial_identifier_B),
31          bits_per_item,
32      )
```

En 5 y 6 se crean dos arrays en $O(n)$ cada uno, y el bucle de 8-10 los inicializa con las posiciones de los elementos de A y B en $O(n)$ también. La creación de los identificadores de las listas en 12-22 también se realiza en $O(n)$. Por tanto la complejidad temporal del método de inicialización es $O(n + n + n) = O(n)$.

En el método principal, la complejidad temporal de un algoritmo de programación dinamica es:

$O(cantidad$ $de$ $estados$ $únicos * complejidad$ $temporal$ $de$ $cada$ $uno)$

Analicemos entonces cada estado, para después calcular el total. Tomémoslo por secciones:

```python
1   def dynamic_potion_sort_aux(
2       A: list[int],
3       B: list[int],
4       moves: dict[tuple[int, int], list[int]],
5       indexes_A: list[int],
6       indexes_B: list[int],
7       lists_repr: tuple[int, int],
8       bits_per_item: int,
9   ) -> list[int]:
10      if lists_repr in moves:
11          return moves[lists_repr]
12  
13      n = len(A)
14  
15      best_swaps_count = -1
16      best_swaps = []
17      best_swap_elem = -1
```
En 10 se busca si este estado ya se ha calculado antes, lo cual es una operación de $O(1)$ típicamente, ya que `moves` es un diccionario.

Entre 13 y 17 se realizan otras inicializaciones miscelaneas también en $O(1)$.

Esta sección se llevó a cabo en $O(1)$.

```python
1   for i in range(n):
2       elem = i + 1
3   
4       # skip item if correct
5       if A[i] == elem and B[i] == elem:
6           continue
7   
8       A_item_at_i = A[i]
9       B_item_at_i = B[i]
10  
11      i_index_A = indexes_A[i]
12      i_index_B = indexes_B[i]
13  
14      # swap potions
15      swap_items(A, i, i_index_A)
16      swap_items(B, i, i_index_B)
17  
18      # update indexes array
19      swap_items(indexes_A, A_item_at_i - 1, i)
20      swap_items(indexes_B, B_item_at_i - 1, i)
```

La línea 5 comprueba si en el elemento $i$ no es necesario hacer ningún swap, saltándose los índices que ya están ordenados. Esto es en $O(1)$.

En 8-12 se inicializan variables con las posiciones del elemento $i$ en A y B, así como el valor del elemento que se encuentra en la posición $i$ en A y B. Todo en $O(1)$.

En 15-12 se realizan las operaciones de swappeo, mostrado anteriormente que es en $O(1)$.

Esta sección también se ejecutó en $O(1)$.

```python
1   # update lists representation
2   new_A_repr = (lists_repr[0] ^ (A_item_at_i << (bits_per_item * i))) ^ (
3       (i + 1) << (bits_per_item * i_index_A)
4   )
5   new_A_repr |= (A_item_at_i << (bits_per_item * i_index_A)) | (
6       (i + 1) << (bits_per_item * i)
7   )
8   
9   new_B_repr = (lists_repr[1] ^ (B_item_at_i << (bits_per_item * i))) ^ (
10      (i + 1) << (bits_per_item * i_index_B)
11  )
12  new_B_repr |= (B_item_at_i << (bits_per_item * i_index_B)) | (
13      (i + 1) << (bits_per_item * i)
14  )
```

Un montón de operaciones de bits, pero todo en $O(1)$, aunque introduce una constante bastante grande, cuyas consecuencias veremos más tardes.

```python
1   swaps = dynamic_potion_sort_aux(
2       A,
3       B,
4       moves,
5       indexes_A,
6       indexes_B,
7       (new_A_repr, new_B_repr),
8       bits_per_item,
9   )
10  
11  # revert swap
12  swap_items(A, i, i_index_A)
13  swap_items(B, i, i_index_B)
14  
15  # revert indexes array update
16  swap_items(indexes_A, A_item_at_i - 1, i)
17  swap_items(indexes_B, B_item_at_i - 1, i)
18  
19  if best_swaps_count == -1 or len(swaps) < best_swaps_count:
20      best_swaps = swaps
21      best_swaps_count = len(swaps)
22      best_swap_elem = elem
```

En 1 está la llamada recursiva, el efecto de esta se verá al calcular la cantidad de estados únicos, ya que como vimos antes, si un estado ya fue calculado el método devuelve instantaneamente.

En 12-17 se revierten los swaps hechos antes de la llamada recursiva, todo nuevamente en $O(1)$.

En 19-22 se comprueba si encontramos un nuevo mejor swap, o si es el primero. $O(1)$.

El bucle entero corre $n$ veces y sus operaciones interiores se realizan en $O(1)$, por tanto la ejecución del bucle es $O(n)$.

```python
1   if best_swaps_count == -1:
2       return []
3   
4   result = [best_swap_elem, *best_swaps]
5   
6   moves[lists_repr] = result
7   
8   return result
```

El paso de finalización, en 1 si no se realizó ningún swap, se devuelve el array vacío. $O(1)$.

En otro caso se construye un array con mejor swap, y los swaps definidos recursivamente, en $O(n)$ por la deconstrucción de la lista `best_swaps`.

En 6 se guarda el resultado de este estado para la memoización. $O(1)$ típicamente.

Entonces en general, la ejecución de cada estado del problema es $O(n + n) = O(n)$.

Ahora, determinemos la cantidad máxima de estados que puede tener el problema.

No se 👉👈

Asumamos peor caso $O(n!^2)$ estados (que no es, son muchos menos, pero esta parte de la demostración la dejamos a medias por _skill issue_), la complejidad temporal sería $O(n*n!^2)$