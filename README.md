# ExamenInComCuantica

En el archivo Problema6.py se encuentra el programa correspondiente a este problema.



## Problema 6

Programa para hallar matriz de enlaces de entrelazamiento de dos estados puros caracterizados en wavefunction_1.txt y wavefunction_2.txt. El programa pide seleccionar el estado, así la opción 1 se corresponde al primer archivo de datos y la opción 2 al segundo.

Además, se hallan los contornos de entrelazamiento para un bloque seleccionado y se muestran los contornos de entrelazamiento propios de estado rainbow y dimer de fermiones libres según la opción escogida.

El bloque tiene formato [q1 q2 q3 q4 q5 q6 q7 q8], donde cada qi debe ser 1 o -1, 1 si el qubit se considera y -1 si no es el caso.

La matriz de enlaces de entrelazamiento se genera en el archivo MatrizEnlaces.txt y la matriz distancia en el archivo distancia.txt.


## Problema 9

### Ecuación Lindblad

En el archivo Problema9-1.py se encuentra el programa correspondiente a este problema.

Este programa que desarrolla la evolucion temporal del sistema de un spin con hamiltoniano H = G sigma_z y una propabilidad de decaimiento por segundo gamma según la ecuación de Lindblad. Este programa pide al usuario por pantalla:

- G: intensidad del hamiltoniano.
- gamma: valor de la propabilidad de decaimiento por unidad de tiempo.
- T: tiempo total de evolucion.
- M: número de puntos temporales en el mallado.

El estado inicial se debe escoger modificando la funcion main_lindblad por medio de los coeficientes alpha y beta. El valor actual es de 1/sqrt(2) para ambos.

Los valores de fidelidad con respecto al estado fundamental se guardaron en el archivo fidelidadLindblad.txt.

### Simulación Monte Carlo

En el archivo Problema9-2.py se encuentra el programa correspondiente a este problema.

Este programa desarrolla la evolucion temporal del sistema de un spin con hamiltoniano H = G sigma_z y una propabilidad de decaimiento por segundo gamma por medio de simulación Monte Carlo.

- G: intensidad del hamiltoniano.
- gamma: valor de la propabilidad de decaimiento por unidad de tiempo.
- T: tiempo total de evolucion.
- M: número de puntos temporales en el mallado.
- N: número de trayectorias.

El estado inicial se debe escoger modificando la funcion main_lindblad por medio de los coeficientes alpha y beta. El valor actual es de 1/sqrt(2) para ambos.

Los valores de fidelidad con respecto al estado fundamental se guardaron en el archivo fidelidadMonteCarlo.txt.

## Problema 10

En el archivo Problema10.py se encuentra el programa correspondiente a este problema.

Este programa que calcula la entropia del bloque de los primeros N/2 spines para un hamiltoniano con termino de interaccion y flip de spines. La intensidad de las interacciones viene dada por una matriz de enlaces J cuyos elementos se generan aleatoreamente. Se realizan un cierto número de realizaciones escogido por el usuario. Se debe seleccionar la intensidad del término de sigma_x, Gamma.

Por pantalla se muestra el valor medio de S_A y su desviacion típica. En el archivo Entropias_S_A.txt se escriben todos los valores de S_A obtenidos para las 
distintas realizaciones.
