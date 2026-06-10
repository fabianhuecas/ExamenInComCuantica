#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np


# # ECUACION LINDBLAD

# In[15]:


def matriz_inicial(alpha, beta):

    #Recibe alpha y beta reales para formar la matriz densidad inicial

    rho = np.zeros((2,2))

    rho[0,0] = np.abs(alpha)**2
    rho[1,0] = alpha*beta
    rho[0,1] = alpha*beta
    rho[1,1] = np.abs(beta)**2

    return rho


# In[16]:


def rho_Lindbland(rho_0,G,gamma,t):

    #Soluciones ecuacion Lindblad
    #rho_0: matriz inicial
    #G: parametro Gamma del hamiltoniano
    #gamma: probabilidad por unidad de tiempo del decaimiento
    #t: tiempo

    rho = np.zeros((2,2),dtype=complex)

    rho[0,0] = rho_0[0,0] + rho_0[1,1]*(1-np.exp(-gamma*t))
    rho[1,0] = rho_0[0,1]*np.exp((1j*G-gamma/2)*t)
    rho[0,1] = rho_0[1,0]*np.exp(-(1j*G+gamma/2)*t)
    rho[1,1] = rho_0[1,1]*np.exp(-gamma*t)

    return rho


# In[17]:


def fidelidad(rho, rho_ref):

    #fidelidad segun matrices densidad entre un estado referencia y otro estado rho

    producto = rho @ rho_ref

    f = producto[0,0]+producto[1,1] #Traza de la matriz producto

    return f


# In[29]:


def evolucion_Lindbland(alpha,beta,G,gamma,T,M):

    #alpha: coeficiente asociado al estado fundamental
    #beta: coeficiente asociado al estado excitado

    #devuelve la fidelidad para todos los puntos temporales considerados
    t = np.linspace(0,T,M)
    rho_menos = np.zeros((2,2))
    rho_menos[0,0] = 1.0 

    rho_0 = matriz_inicial(alpha, beta)

    f = []

    for t_i in t:
        
        rho = rho_Lindbland(rho_0,G,gamma,t_i)
        f_i = fidelidad(rho, rho_menos)
        f.append(f_i.real)

    return f, t


# In[30]:


def main_lindblad():

    #alpha: coeficiente asociado al estado fundamental
    #beta: coeficiente asociado al estado excitado
    #IMPORTANTE: use valores reales

    print("Programa que desarrolla la evolucion temporal del sistema de un spin con hamiltoniano H = G sigma_z y una propabilidad de decaimiento por segundo gamma según la ec. de Lindblad.")
    G = float(input("Introduzca el valor G de intensidad del hamiltoniano: "))
    gamma = float(input("Introduzca el valor de la propabilidad de decaimiento por unidad de tiempo gamma: "))
    T = float(input("Introduza el tiempo total de evolucion: "))
    M = int(input("Introduzca el numero de puntos temporales: "))
    print("El estado inicial se debe escoger modificando la funcion main_lindblad por medio de los coeficientes alpha y beta.")
    
    alpha = 1/np.sqrt(2)
    beta = 1/np.sqrt(2)

    f, t = evolucion_Lindbland(alpha,beta,G,gamma,T,M)

    print("\n")

    with open('fidelidadLindblad.txt','w') as archivo:

        archivo.write("# t    |      f")
        archivo.write("\n")

        for t_i, f_i in zip(t,f):

            archivo.write(str(t_i)+'    '+str(f_i))
            archivo.write("\n")

    print("Los valores de fidelidad con respecto al estado fundamental se guardaron en el archivo fidelidadLindblad.txt")

    return


# In[31]:


main_lindblad()





