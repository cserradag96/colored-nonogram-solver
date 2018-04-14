# Colored Nonograma Solver

Se desarrolló un programa en python que resuelve nonogramas de colores. A partir de un archivo `.cnon` como especificación de una partida, la misma se codifica en formato CNF y mediante un SAT Solver de codigo abierto, llamado MiniSAT, se obtiene, en caso de que exista, una evaluación que la haga verdadera, de lo contrario se indica que es insatisfacible.

Un problema SAT busca determinar si existe una evaluación que satisfaga una formula booleana. Por ejemplo, consideremos la formula: "a AND NOT b" es satisfacible porque existen los valores a = True y b = False que cuales hacen cierta dicha expresion. MiniSAT es un SAT solver que recibe un conjunto de terminos, clausulas y expresiones. MiniSAT requiere un input especificado en una version simplificada de CNF llamada "DIMACS CNF". Un archivo de entrada para MiniSAT podría ser como el siguiente:

    p cnf 5 3
    1 -5 4 0
    -1 5 3 4 0
    -3 -4 0
Que coresponde a la siguiente formula:

    (x1 ∨-x5 ∨ x4) ∧ (-x1 ∨ x5 ∨ x3 ∨ x4) ∧ (-x3 ∨ x4).

## Extensión `.cnon`

Se diseño un formato para representar facilmente la especificación de un nonograma de color. El formato consiste en una primera linea con tres números representando la cantidad de colores C, el ancho W y el alto H del tablero respectivamente. A continuación se presentan C lineas con el nombre del color y su valor en hexadecimal separados por un espacio.  Luego H lineas con los bloques presentes en cada fila, separados por espacios. Analogamente las siguiente W lineas contienen los bloques presentes en cada columna. Los bloques son especificados mediante un número que indica la cantidad de celdas que componen el bloque, seguido por el nombre del color del bloque, separados mediante dos puntos.

## Instalación

- Instalar svgwrite

```
pip install svgwrite
```

- Compilar MiniSAT

```
cd minisat
export MROOT=$(pwd)
cd core
sudo apt-get install libghc-zlib-dev
make
```

## Ejecución

```
python3 solver.py <file.cnon>
```

## Codificación

Para representar los nonogramas como CFN consideramos dos tipos de términos:

- **cell** para indicar si una casilla es negra o no (e.g. r3c3: la celda de la fila 3 y columna 3 es negra).
- **group-start** para indicar si un bloque específico empieza en una posición especifica (e.g. r2b0s2: el primero bloque de la fila 2 empieza en la segunda casilla de la fila).

Además, tenemos las siguientes clausulas:

- **Block-starts-somewhere**
Esta clausura  asegura que cada bloque tenga al menos una posición. Por ejemplo, el bloque 2 de la fila 3 tiene la clausura:

    r3b2s0 ∨ r3b2s1 ∨ r3b2s2 ∨ r3b2s3

- **Block-doesn't-duplicate**
Utilizamos esta clausula para evitar que a un bloque se le establezca más de una celda de inicio:

    ¬r3b2s0 ∨ ¬r3b2s1
    ¬r3b2s0 ∨ ¬r3b2s2
    ¬r3b2s0 ∨ ¬r3b2s3
    ¬r3b2s1 ∨ ¬r3b2s2
    ¬r3b2s1 ∨ ¬r3b2s3
    ¬r3b2s2 ∨ ¬r3b2s3

- **Block-to-cell**
Esta clausula sirve para representar la relación entre las celdas y los bloques. Por ejemplo, si un bloque de longtud 2 empieza en el índice 3, entonces hay dos celdas negras:

    ¬r0b0s3 ∨ r0s3
    ¬r0b0s3 ∨ r0s4


- **CellToBlock**
Esta clausula asegura que una celda es negra solamente si existe un bloque que cubra esa posicion. Por ejemplo, si la celda (0, 1) es negra entonces un bloque debe iniciar en la primero o en la segunda posicion de esa fila:

     ¬r0c1 ∨ r0b0c0 ∨ r0b0c1


- **Block-order**
Esta clausula obliga a que el orden de los bloques sea como aparece en el puzzle. Son solo relevante en las filas/columnas con más de un bloque. Si un bloque 0 de una fila 0 tiene longitud 2, la clausula sería:

      ¬r0b0c1 ∨ ¬r0b1c0
      ¬r0b0c1 ∨ ¬r0b1c1
      ¬r0b0c1 ∨ ¬r0b1c2
      ¬r0b0c1 ∨ ¬r0b1c3

Finalmente para la construcción de la entrada para miniSAT, cada uno de estos nombres es traducido a un id único\
 mediante la utilización de un mapa que se va llenando a medida que los terminos son generados, tomando los nombres\
 como las claves y el contador de terminos generados como valor.

## Minisat

Luego de generar la entrada para miniSAT, se guarda en un archivo llamado "input.txt", el cual se crea en la misma\
ubicación del programa. Después se ejecuta miniSAT con el archivo creado directamente desde el script mediante un\
pipe provisto por el lenguaje. La salida estandar de miniSAT es mostrada tambien en pantalla. Y por último, la\
salida correspondiente a la solución encontrada por miniSAT es guardada en el archivo "output.txt".
** Se debe compilar miniSAT con antelación o el programa fallará al intentar ejecutarlo **

## Decodificación

En este caso se lee el archivo de salida de miniSAT y en caso de haber encontrado solución, se crea un arreglo de\
booleanos asignando True a toda variable positiva y False en caso contrario. Luego se construye un segundo mapa con\
la lista de identificadores de cada termino y el arreglo de booleanos. Finalmente de esta estructura se extraen las\
variables que representan celdas del puzzle y se construye una matriz de boolenos que representa la solución.

## Generación de la imagen

Con la matriz resultado de la decodificación de la solución y la información almacenada del problema (vaor de los colores), se renderiza la solución como una imagen vectorial con formato `.svg` mediante la libreria `svgwrite`.

## Estado del proyecto

No siempre encuentra la solución correcta. Faltan agregar y reforzar las reglas.

- `0.cnon` (solución correcta)

<img src="https://raw.githubusercontent.com/cserradag96/colored-nonogram-solver/master/solutions/0.svg?sanitize=true" width="500" height="270"/>

-`yoshi.cnon` (solución incorrecta)

<img src="https://raw.githubusercontent.com/cserradag96/colored-nonogram-solver/master/solutions/yoshi.svg?sanitize=true" width="500" height="650"/>
