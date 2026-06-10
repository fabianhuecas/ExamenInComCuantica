#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


def Bits_entero(N): #verified

    #Funcion que devuelve la secuencia de asociada a un entero

    if(N==0):

        return '0'

    #Primer termino 
    secuencia_bit = ""
    sumando = 0
    
    n = np.log2(N)

    
    secuencia_bit += "1"
    n = int(np.log2(N))
    sumando += 2**n
    
    for k in range(n-1,-1,-1):

        if(sumando+(2**(k))>N):

            secuencia_bit += "0"

        else:

            sumando += (2**(k))
            secuencia_bit += "1"
            

    return secuencia_bit


# In[26]:


def inicio(N):

    archivo_txt = "DatosEjercicio6.txt"

    #Captamos los datos del archivo txt 
    with open(archivo_txt,"r") as archivo:
    
        contenido = archivo.read().splitlines()
    
    indices = []
    coefs = [] #Este es el vector de coeficientes
    
    for linea in contenido[2:]:
    
        partes_linea = linea.split()
    
        indices.append(partes_linea[0])
        coefs.append(float(partes_linea[1]))

    #print(indices)
    secuencias = [Bits_entero(int(i)).zfill(N) for i in indices]
        
    #secuencias = [secuencia[:-1] for secuencia in lista_secuencias] #lista con todas las secuencias tipo '00000000' de 8 digitos
    #esto identifica un elemento de base de 8 qubits con un indice. secuencias[i] ---- i

    #Aqui creamos los BLOQUES, no en un orden especifico pero esto nos dice que qubits cuenta el bloque
    #cada bloque es una lista de elementos, el elemento iesimo representa el qubit iesimo
    #si elemento es 1 sí lo considera, con -1 no lo considera

    bloques = [[oc1,oc2,oc3,oc4,oc5,oc6,oc7,oc8,oc9,oc10,oc11,oc12] for oc1 in [-1,1] for oc2 in [-1,1] for oc3 in [-1,1] for oc4 in [-1,1] for oc5 in [-1,1] for oc6 in [-1,1] for oc7 in [-1,1] for oc8 in [-1,1] for oc9 in [-1,1] for oc10 in [-1,1] for oc11 in [-1,1] for oc12 in [-1,1]]
    
    return secuencias, coefs, bloques
    


# In[4]:


def identificacion_fermions(bloque):

    #Dentro de un bloque nos quedamos con las posiciones que sí son consideradas
    #Ejemplo bloque = [-1,1,-1,1,-1,-1,-1,-1]
    #Entonces su identificador es [1,3]

    identificador = [i for i,i_qubit in enumerate(bloque) if i_qubit == 1]

    return identificador


# In[5]:


def index_secuencia(secuencia, secuencias): #verified

    #Esta funcion nos permite obtener el indice entre 0 y 255 incluidos asociado a un elemento de base

    pos = secuencias.index(secuencia)

    return pos


# In[6]:


def complementario(bloque): #verified

    #Crea el bloque complementario

    bloque_comple = [-1*oc2 for oc2 in bloque]

    return bloque_comple


# In[7]:


def num_qubits(bloque): #verified

    #Es el numero de qubits considerados en un bloque
    #Por ejemplo, A = {1,-1,-1,-1,-1,-1,-1,-1}

    num = 0

    for oc_qubit in bloque:

        if(oc_qubit==+1):

            num += 1

    return num


# In[8]:




# In[9]:


def lista_estados(bloque,N): #verified

    #Nos apaorta toda la lista de elementos de base asociado a un determinado bloque
    #Por ejemplo, A = {1,-1,-1,-1,-1,-1,-1,-1}
    # Los estados seria [0]_1 y [1]_1 pero los devolvemos en secuencias de string donde
    #en la posicion iesima se establece si el qubit es 0, 1 o 2 si directamente no forma parte
    # con lo que en el ejemplo tendriamos estados '02222222' y '12222222'

    n_qubits = num_qubits(bloque) #num qubits considerados

    num_estados = 2**n_qubits #numero de estados asociados al bloque

    list_estados = [] #lista donde se incorporan todos los estados
    secuencias_estados = [] #lista con todas las secuencias

    posiciones = [] #posiciones/indices que sí son consideradas

    for index_qubit in range(N):

        if(bloque[index_qubit]==+1): #si el qubit es considerado en el bloque se añade su posicion

            posiciones.append(index_qubit)

    for i_estado in range(num_estados):

        #creamos secuencias para todos los estados 
        secuencia = Bits_entero(i_estado) #a cada estado le asociamos una secuencia
        secuencia = secuencia.zfill(n_qubits) #rellenamos hasta nqubits añadiendo ceros si es necesario
        secuencias_estados.append(secuencia) #añadimos todas las secuencias (todas tienen tamaño de nqubits)
    
    for i_estado in range(num_estados):

        estado = [] #inicializamos estado

        pos_secuencia = 0 #posicion asociada en la secuencia de nqubits
        for index in range(N):

            if(index in posiciones): #si el indice coincide con posicion considerada tomo lo que haya en la secuencia asociada

                estado.append(secuencias_estados[i_estado][pos_secuencia])

                pos_secuencia += 1 #muevo  posicion en su secuencia asociada

            else:

                estado.append('2') #si no, es que no es considerada y lo marco con 2

        list_estados.append(estado)

    return list_estados

            

            


# In[10]:


def crea_secuencia_bloques(elemento_A, elemento_A_c,N): #verified

    #En esta funcion creamos una secuencia asociada a un elemento de base a partir de dos estados asociados 
    #con dos bloques que deben ser complementarios y que deben ser construidos por medio
    #de la funcion lista_estados

    secuencia = []
    for i in range(N):
        if(elemento_A[i] == '2' and elemento_A_c[i] == '2'): #si esta todo bien esto no se deberia dar
            print('Error ambos no consideran este qubit')
            return None
        if(elemento_A[i] != '2' and elemento_A_c[i] != '2'): #si esta todo bien esto no se deberia dar
            print('Error ambos consideran este qubit')
            return None

        if(elemento_A[i]=='2'): #si el qubit no esta considerado en A, lo esta en A_c, y se crea la secuencia segun este
            if(elemento_A_c[i]=='1'):
                secuencia.append('1')
            elif(elemento_A_c[i]=='0'):
                secuencia.append('0')
            else: #no se deberia dar nunca
                print('Error')

        if(elemento_A_c[i]=='2'): #si el qubit no esta considerado en A, lo esta en A_c, y se crea la secuencia segun este
            if(elemento_A[i]=='1'):
                secuencia.append('1')
            elif(elemento_A[i]=='0'):
                secuencia.append('0')
            else: #no se deberia dar nunca
                print('Error')

    resultado = ''.join(secuencia)
    return resultado
        
                


# In[11]:


def matriz_M(bloque, coefs,secuencias,N):

    #se genera la matriz M que sirve para generar la matriz densidad
    #esta se compone de tantas filas como elementos tiene el bloque
    #y de tantas columnas como elementos tiene el bloque complementario
    #en la fila i columna j, se tiene el coeficiente c asociado al elemento de base 
    #que forma el elemento i del bloque y el elemento j del bloque complementario

    bloque_C = complementario(bloque)
    estados_bloque = lista_estados(bloque,N)
    estados_bloque_C = lista_estados(bloque_C,N)

    num_fil = len(estados_bloque)
    num_col = len(estados_bloque_C)

    M = np.zeros((num_fil,num_col)) #incializa la matriz en ceros

    for fil in range(num_fil):
        for col in range(num_col):
            estado_bloque = estados_bloque[fil] #recoge un estado del bloque
            estado_bloque_C = estados_bloque_C[col] #recoge un estado del complementario

            #se unen para formar un elemento de base en forma de secuencia
            secuencia = crea_secuencia_bloques(estado_bloque, estado_bloque_C, N) 

            #obtenemos el indice asociado 
            index = index_secuencia(secuencia,secuencias)

            #se llena con el coeficiente correspondiente
            M[fil][col] = coefs[index]

    return M


# In[12]:


def matriz_densidad(bloque,coefs,secuencias,N):

    #Dado un bloque generamos su matriz densidad. Bloque A ---> rho_A

    M = matriz_M(bloque,coefs,secuencias,N) #se halla la matriz M

    MT = M.T #se halla su transpuesta

    rho = M @ MT #se obtiene la matriz densidad, esta forma de proceder asegura que es simetrica EXACTAMENTE

    return rho
    


# In[13]:


def entropia(bloque, coefs, secuencias,N):

    #Calculo de la entropia segun S_A = -Tr_A(rho_A log rho_A) = -lambda_i log_2(lambda_i)

    rho = matriz_densidad(bloque,coefs,secuencias,N)

    autovalores = np.linalg.eigvalsh(rho)

    S = 0
    tol = 1e-12

    for autovalor in autovalores:

        if autovalor>tol:
            
            S += -autovalor*np.log2(autovalor) 

    return S


# In[14]:


def lista_entropias(coefs, bloques,secuencias,N):

    #Hallamos las entropias de todos los bloques y las metemos en una lista
    S = []
    for i in range(2**N):

        bloque = bloques[i]
        S.append(entropia(bloque,coefs,secuencias,N))

    return S


# In[15]:


def obtencion_J(coefs, bloques,secuencias,N):

    #Este programa ofrece la matriz de adyacencia directamente

    tol = 1e-10

    S = lista_entropias(coefs, bloques,secuencias,N) #Obtencion de todas las entropias

    #Se eliminan todas las entropias menores que la tolerancia
    for i,s in enumerate(S):
        if(abs(s)<tol):
            S[i]=0

    J, n_iter = matriz_adyacencia(S,bloques,N) #Se halla matriz de adyacencia J

    return J


# In[16]:


def identificacion(N):

    #identificacion uno a uno con un indice que empieza en cero con una lista [i,j] donde j va de 0 a N-1 e i desde 0 a j
    #Necesario para el sistema lineal aproximado

    lista_i_j = []

    for j in range(N):
        for i in range(j):
            lista_i_j.append([i,j])

    return lista_i_j

    


# In[17]:


def creacion_sistema_lineal(S,bloques,N):

    #Se crea el sistema lineal aproximado, la matriz de coeficientes de variables, que es la matriz A_T*A
    #Y el vector de coeficientes libres que se calcula con el valor de las entropias de todos los bloques

    N_p = int(N*(N-1)/2) #numero de parametros independientes

    #contruccion matriz_coeficientes_variables

    matriz_A_T_A = np.ones((N_p,N_p))

    for i in range(N_p):

        matriz_A_T_A[i][i] = 2

    matriz_A_T_A = (2**(N-2))*matriz_A_T_A #verified

    #construccion matriz A

    A = np.zeros((2**N,N_p))

    i_j_values = identificacion(N)

    for k in range(2**N):
        for l in range(N_p):

            i = i_j_values[l][0]
            j = i_j_values[l][1]
        
            if((bloques[k][i]==1 and bloques[k][j]==-1)or(bloques[k][i]==-1 and bloques[k][j]==1)):

                A[k][l] = 1

    #construccion del vector columna independiente

    b = np.zeros(N_p)

    for l in range(N_p):

        for i_bloque in range(2**N):

            b[l] += A[i_bloque][l]*S[i_bloque]

    return matriz_A_T_A, b
    


# In[18]:


def metodo_Gauss_Seidel(A,b,n,tol,max_iter,par_lambda):

    '''

    Funcion que aplica el metodo Gauss-Seidel sobre el sistema de ecuaciones lineal Ax=b

    Argumentos:

    -A: matriz con los coeficientes de variables
    -b: matriz con los coeficientes libres
    -n: numero de ecuaciones/incognitas del sistema
    -tol: tolerancia
    -max_iter: maximo numero de iteraciones
    -par_lambda: valor para la sobrerelajacion, con lambda=1 se tiene el metodo Gauss-Seidel sin relajacion.

    Output:

    -x: soluciones
    -iter: numero de iteraciones

    '''

    #x = -1*np.ones(n)
    x = np.zeros(n)
    tol_alcanzada = False
    n_iter = 0

    while((n_iter<max_iter)and(tol_alcanzada==False)):

        tol_alcanzada = True

        for i_x in range(n):

            x_prev = x[i_x]
            x[i_x] = b[i_x]

            for col in range(n):

                if(col != i_x):

                    x[i_x] = x[i_x] - A[i_x][col]*x[col]

            x[i_x] = x[i_x]/A[i_x][i_x]

            x[i_x] = par_lambda*x[i_x] + (1.0-par_lambda)*x_prev

            if(tol_alcanzada):

                error = abs(x[i_x]-x_prev)
                
                if(tol<error):
                    
                    tol_alcanzada = False

        n_iter+=1

    if(tol_alcanzada):
        print("La tolerancia ha sido alcanzada. ")
    else:
        
        print("Maximo numero de iteraciones alcanzado sin que la tolerancia fuese alcanzada. ")

    return x,n_iter
        

    


# In[19]:


def matriz_adyacencia(S,bloques,N):

    #Creacion de la matriz de adyacencia por medio del sistema lineal aproximado
    #Se debe proveer la entropia de todos los bloques

    n = int(N*(N-1)/2) #numero de ecuaciones e incognitas (los elementos independientes de J)

    A, b = creacion_sistema_lineal(S,bloques,N) #Obtenemos matriz de coeficientes de variables y vector de coeficientes libres

    tol = 1e-11

    max_iter = 10000

    par_lambda = 1.0

    x, n_iter = metodo_Gauss_Seidel(A,b,n,tol,max_iter,par_lambda) #soluciones x y el numero de iteraciones realizadas

    lista_i_j = identificacion(N) #la lista que nos identifica el indice de las soluciones con los valores i,j

    J = -1*np.ones((N,N)) #Inicializamos en un valor que no debria suceder

    for l in range(n):

        i = lista_i_j[l][0]
        j = lista_i_j[l][1]
        J[i][j] = x[l]
        J[j][i] = J[i][j] #Por definicion, simetrica

    for i in range(N):

        J[i][i] = 0 #Por definicion, la diagonal es cero

    return J, n_iter


# In[20]:


def entropia_matriz_adyacencia(bloque, J,N):

    #Entropia de un bloque calculada desde el conocimiento de la matriz de adyacencia

    bloque_C = complementario(bloque)

    S = 0

    for i in range(N):
        for j in range(N):
            if(bloque[i]==+1 and bloque_C[j]==+1): #solo suma si i es del bloque y j del complementario

                S += J[i][j]

    return S


# In[21]:


    


# In[32]:


def main():

    N = 12
    
    secuencias, coefs, bloques = inicio(N)

    #valores_entropia = lista_entropias(coefs,bloques,secuencias,N)

    J = obtencion_J(coefs,bloques,secuencias,N)

    with open("MatrizEnlaces.txt", "w") as archivo:

        for fila in range(len(J)):
            for col in range(len(J)):
                archivo.write(str(J[fila][col]))
                archivo.write("  ")

            archivo.write("\n")
            
    print("La matriz de enlaces asociadas al estado puro insertado fue escrita en el archivo MatrizEnlaces.txt.")

    #print("Tamaño J: ",len(J))

    return None


# In[ ]:


main()

print('Calculos finalizados')

