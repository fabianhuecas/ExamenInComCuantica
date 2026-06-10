import numpy as np


def evolucion_montecarlo(Psi_inicial,G,gamma,T,M):

    #Evolucion Monte Carlo para una trayectoria
    #Psi_inicial: estado inicial, array de dos elementos.
    #G: parametro del hamiltoniano, Gamma
    #gamma: probabilidad por unidad de tiempo de decaimiento
    #T: periodo temporal total considerado
    #M: numero de puntos temporales

    #Psis: se devuelve lista con el estado(array de dos elementos) en cada punto temporal
    
    rng = np.random.default_rng() #generamos semilla para los numeros aleatorios

    dt = T/(M-1)
    t = np.linspace(dt,T,M-1)
    alpha = Psi_inicial[0]
    beta = Psi_inicial[1]
    dp = gamma*(np.abs(beta)**2)*dt
    #print('dp',dp)
    #norm = np.sqrt(1-dp)

    Psis = [Psi_inicial]

    for i,t_i in enumerate(t):

        epsilon = rng.random() #se toman los elementos independientes de la matriz segun distribucion uniforme (0,1)

        #print('epsilon ',epsilon)

        if(epsilon<dp): #SALTO

            alpha = 1
            beta = 0

            Psi = np.array((alpha,beta))

            for k in range(len(t)-i):

                Psis.append(Psi)

            break

        else: # EVOLUCION TEMPORAL SEGUN HAMILTONIANO EFECTIVO

            alpha = alpha*(1+0.5*1j*G*dt)
            #alpha /= norm
            beta = beta*(1-0.5*1j*G*dt-(gamma/2)*dt)
            #beta /= norm

            #print('beta: ',beta)

            Psi = np.array((alpha,beta))

            norma = np.linalg.norm(Psi)

            Psi/=norma

            Psis.append(Psi)

            alpha /= norma
            beta /= norma

        dp = gamma*(np.abs(beta)**2)*dt #actualizamos probabilidad de salto en intervalo temporal
        #norm = np.sqrt(1-dp)


    return Psis 


# In[23]:


def fidelidad_st(psi_ref, conjunto_psis):

    '''
    Probabilidades asociada a psi_ref dado el conjunto de soluciones en el mallado temporal

    '''

    f = []

    for psi in conjunto_psis:

        solapamiento = np.vdot(psi_ref,psi)

        f.append((np.abs(solapamiento))**2)

    return f


# In[24]:


def todas_trayectorias_Monte_Carlo_opt(alpha, beta,G,gamma,T,M,N):

    #alpha: coeficiente del estado fundamental en el estado incial
    #beta: coeficiente del estado excitado en el estado incial

    Psi_i = np.array((alpha, beta))
    Psi_ref = np.array((1, 0))

    t = np.linspace(0,T,M)

    f_acumulado = np.zeros(M)

    for n in range(N):
        Psis = evolucion_montecarlo(Psi_i, G, gamma, T, M)
        f = fidelidad_st(Psi_ref, Psis)

        f_acumulado += np.asarray(f)

    #Promedio sobre todas las trayectorias
    f_med = f_acumulado / N

    return f_med, t


# In[27]:


def main_Montecarlo():

    #alpha: coeficiente asociado al estado fundamental
    #beta: coeficiente asociado al estado excitado
    #IMPORTANTE: use valores reales
    print("Programa que desarrolla la evolucion temporal del sistema de un spin con hamiltoniano H = G sigma_z y una propabilidad de decaimiento por segundo gamma por medio de simulación Monte Carlo.")
    G = float(input("Introduzca el valor G de intensidad del hamiltoniano: "))
    gamma = float(input("Introduzca el valor de la propabilidad de decaimiento por unidad de tiempo gamma: "))
    T = float(input("Introduza el tiempo total de evolucion: "))
    M = int(input("Introduzca el numero de puntos temporales: "))
    N = int(input("Introduzca el numero de trayectorias: "))
    print("El estado inicial se debe escoger modificando la funcion main_lindblad por medio de los coeficientes alpha y beta.")

    alpha = 1/np.sqrt(2)
    beta = 1/np.sqrt(2)

    f, t = todas_trayectorias_Monte_Carlo_opt(alpha, beta,G,gamma,T,M,N)
    print("\n")
    print("Los valores de fidelidad con respecto al estado fundamental se guardaron en el archivo fidelidadMonteCarlo.txt")

    with open('fidelidadMonteCarlo.txt','w') as archivo:

        archivo.write("# t    |      f")
        archivo.write("\n")
        for t_i, f_i in zip(t,f):

            archivo.write(str(t_i)+'    '+str(f_i))
            archivo.write("\n")

    return


# In[28]:


main_Montecarlo()

