def calcular_mcd(a, b):

    #funcion que halla el maximo comun divisor de dos numeros a y b
    while b != 0:
        a_org = a       
        a = b          
        b = a_org % b   
    return a

def llave_secreta(p,q):

    #Produccion de la llave secreta (d,N)
    # p y q deben ser numeros primos y N entero
    
    N = p*q

    aux = (p-1)*(q-1)

    for d in range(200,N): #aqui selecciono que sea uno mayor que 200 arbitrariamente
    
        mcd = calcular_mcd(d,aux)
    
        if(mcd==1):
    
            break

    return d

def llave_publica(p,q):
    
    #Produccion de la llave secreta (d,N)
    # p y q deben ser numeros primos y d entero
    
    d = llave_secreta(p, q)

    a = (p-1)*(q-1)

    e = 0
    mod = 0
    while(mod!=1):
    
        e+=1
        mod = (e*d)%a

    return e
#Numeros primos p y q
p = 179
q = 281
N = p*q
d = llave_secreta(p,q)
e = llave_publica(p,q)
#mensaje a enviar:
mensaje = [4, 9, 16, 20]
print("Mensaje seleccionado por emisor para enviar:", mensaje)
men_encript = [pow(m, e, N) for m in mensaje]
print("Mensaje encriptado por emisor con llave publica:", men_encript)
men_desci = [pow(c, d, N) for c in men_encript]
print("Mensaje descifrado por receptor con llave secreta:", men_desci)

