#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np


# In[4]:


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


# In[5]:


def preparacion_sistema(N):

    #Obtencion de todas las secuencias del sistema con N particulas y dos posibles estados
    #cada secuencia representa un elemento de base 
    #cada secuencia es "i1i2i3....iN" si i = 0, representa el estado spin +1/2 y si i=+1, representa el estado spin -1/2

    num_secuencias = 2**N

    secuencias = [Bits_entero(i_sec).zfill(N) for i_sec in range(num_secuencias)]

    return secuencias


# In[6]:


def num_spins_coincidentes(sec1,sec2):

    #numero de estados de spins coincidentes entre dos elementos de base sec1 y sec2
    #se comparan estados monoparticulares

    N1 = len(sec1)
    N2 = len(sec2)

    if(N1!=N2): return 
    else:
        n_coincidentes = 0
        for i_sec in range(N1):

            if(sec1[i_sec]==sec2[i_sec]):

                n_coincidentes += 1

    return n_coincidentes


# In[7]:


def matriz_H0(N, secuencias):

    #N numero de particulas
    #secuencias: elementos de base identificados en secuencias

    num_elem = 2**N #al haber dos estados monoparticulares (spin) la dimension del hamiltoniano 2**N x 2**N

    H0 = np.zeros((num_elem,num_elem))

    for i in range(num_elem):
        sec_i = secuencias[i]
        for j in range(num_elem):

            sec_j = secuencias[j]

            num_spins_coin = num_spins_coincidentes(sec_i,sec_j)

            if((N-num_spins_coin==1)): #si se diferencian en un spin los estados se acoplan

                H0[i][j] = +1.0  
    return H0


# In[8]:


def generar_matriz_J(N):

    #Genera una matriz J NxN siguiendo una distribucion uniforme

    num_elem_indp = int((N*(N-1))/2) #numero de elementos independientes de una matriz simetrica sin considerar la diagonal

    J = np.zeros((N,N)) #matriz J NxN

    rng = np.random.default_rng() #generamos semilla

    elementos = rng.random(size=num_elem_indp)#se toman los elementos independientes de la matriz segun distribucion uniforme con intervalo (0,1)

    #se llena la matriz teniendo en cuenta que es simetrica
    n = 0

    for fil in range(N):
        J[fil][fil]=0
        for col in range(fil):

            J[fil][col] = elementos[n]
            J[col][fil] = elementos[n]
            n+=1

    return J


# In[9]:


def matriz_H1(N,secuencias):

    #N numero de particulas
    #secuencias: elementos de base identificados en secuencias

    num_elem = 2**N

    H1 = np.zeros((num_elem,num_elem))

    J = generar_matriz_J(N) #matriz de enlaces

    for fil in range(num_elem): #H1 solo acopla un estado consigo mismo, es diagonal en esta base
        sec = secuencias[fil]
        elemento = 0
        #ahora vamos sumando el termino kJ_{ij}
        for i in range(N):
            for j in range(N):
                if(sec[i]==sec[j]):
                    k = 1 #si tienen mismos spines
                else:
                    k = -1 #si tienen spines opuestos

                elemento += k*J[i][j]

        H1[fil][fil] = -1*elemento

    return H1


# In[10]:


def matriz_H(N,secuencias,Gamma):

    #hamiltoniano total como: H = (1-lambda)H_0 + lambda*H_1

    H0 = matriz_H0(N,secuencias)
    H1 = matriz_H1(N,secuencias)

    H = Gamma*H0 + H1

    return H


# In[11]:


def index_secuencia(secuencia, secuencias): #verified

    #Esta funcion nos permite obtener el indice entre 0 y 255 incluidos asociado a un elemento de base

    pos = secuencias.index(secuencia)

    return pos


# In[6]:


def complementario(bloque): #verified

    #Crea el bloque complementario

    bloque_comple = [-1*oc2 for oc2 in bloque]

    return bloque_comple


# In[12]:


def num_qubits(bloque): #verified

    #Es el numero de qubits considerados en un bloque
    #Por ejemplo, A = {1,-1,-1,-1,-1,-1,-1,-1}

    num = 0

    for oc_qubit in bloque:

        if(oc_qubit==+1):

            num += 1

    return num


# In[13]:


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


# In[14]:


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


# In[15]:


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


# In[16]:


def matriz_densidad(bloque,coefs,secuencias,N):

    #Dado un bloque generamos su matriz densidad. Bloque A ---> rho_A

    M = matriz_M(bloque,coefs,secuencias,N) #se halla la matriz M

    MT = M.T #se halla su transpuesta

    rho = M @ MT #se obtiene la matriz densidad, esta forma de proceder asegura que es simetrica EXACTAMENTE

    return rho


# In[17]:


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


# In[18]:


def obtencion_entropias(Gamma, N, N_tray):

    secuencias = preparacion_sistema(N)

    bloque = [1,1,1,1,-1,-1,-1,-1]

    lista_S = -1*np.ones(N_tray)

    for n in range(N_tray):

        H = matriz_H(N,secuencias,Gamma) 
    
        autovalores, auto_estados = np.linalg.eigh(H)
    
        psi0 = auto_estados[:,0]
    
        S = entropia(bloque, psi0, secuencias,N)

        lista_S[n] = S

    media_S = np.mean(lista_S)
    
    desviacion_S = np.std(lista_S, ddof=1)
    
    return lista_S, media_S, desviacion_S
    
    


# In[19]:


def valores_mediod_dif_gamma(G_values,N,N_tray):

    medias_S = []
    stds_S = []
    for G in G_values:
        
        Ss, med_S, std_S = obtencion_entropias(G,N,N_tray)

        medias_S.append(med_S)
        stds_S.append(std_S)

    return medias_S, stds_S


# In[32]:


def main():

    print("Programa que calcula la entropia del bloque de los primeros N/2 spines para un hamiltoniano con termino de interaccion y flip de spines. ")
    print("La intensidad de las interacciones viene dada por una matriz de enlaces J cuyos elementos se generan aleatoreamente. Se realizan un cierto número de realizaciones escogido por el usuario. ")
    print("Se debe seleccionar la intensidad del término de flip, Gamma.")
    print("\n")
    G = float(input("Introduzca el valor de Gamma: "))
    M = int(input("Introduzca el numero de realizaciones: "))

    N = 8 #Numero de spines
    
    Ss, med_S, std_S = obtencion_entropias(G,N,M)
    print("\n")
    print("El valor medio <S_A> es: ", med_S)
    print("La desviación típica std(S_A) es: ", std_S)
    print("\n")
    print("Los valores de entropia para las diferentes realizaciones se guardaron en el archivo Entropias_S_A.txt")

    with open('Entropias_S_A.txt','w') as archivo:

        archivo.write("# Realizacion    |      S_A")
        archivo.write("\n")
        for i,s in enumerate(Ss):

            archivo.write(str(i)+'    '+str(s))
            archivo.write("\n")


# In[29]:


main()

