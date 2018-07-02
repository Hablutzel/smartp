
Z = ["Z1" , "Z2" , "Z3" , "Z4"] # N ZONAS

C = ["C1" , "C2" , "C3"] # M CARROR EN SOLICITUD DE ESTACIONAMIENTO EN UN TIEMPO DETERMINADO

D = [   [0.24 , 0.48 , 0.20 , 0.18 ], # MATRIZ DE DISTANCIAS DE LOS CARROS HACIA LAS ZONAS DE ESTACIONAMIENTO
        [0.16 , 0.13 , 0.02 , 0.26],
        [0.17 , 0.6 , 0.14 , 0.3]
    ]
D2 = [   [0.24 , 0.48 , 0.20 , 0.18 ], # MATRIZ DE DISTANCIAS DE LOS CARROS HACIA LAS ZONAS DE ESTACIONAMIENTO
        [0.16 , 0.13 , 0.02 , 0.26],
        [0.17 , 0.6 , 0.14 , 0.3]
    ]

FS1 = [3,1,0,6] # CANTIDAD DE SPOTS LIBRES POR ZONA
FS2 = [3,1,0,6]
FS3 = [3,1,0,6]

A1 = [] # A = (aij)M×N
A2 = [] # A = (aij)M×N
A3 = [] # A = (aij)M×N

for m in range(len(C)): # CREAR MATRIZ DE ASIGNACION EN BLANCO
    fila = []
    for n in range(len(Z)):
        fila.append(0)
    A1.append(fila)
    A2.append(fila)
    A3.append(fila)

def fs_availability(zona , fs):
    if fs[zona] > 0:
        fs[zona]= fs[zona] - 1
        return True
    else:
        return False

def calcular_menor_v1(carro):
    val = 0
    aux = D[carro].copy()
    D[carro].sort()
    find = False
    while not find:
        pos_min = aux.index(D[carro][val])
        if fs_availability(pos_min , FS1):
            find = True
            print("**Carro: {}, asignado a la zona : {}".format(carro,pos_min))
            A1[carro][pos_min] = 1 # ASIGNAR 1 A LA SELECCIONADA
            print(FS1)  
            return
        print("No hay spot disponible en la zona {}. Recalculando ...".format(pos_min))
        val+=1

def llenar_matriz_asignacion_v1():
    for c in range(len(C)):
        calcular_menor_v1(c)
    print(A1)

def funcion_costo_v1():
    suma = 0
    for m in range(len(C)):
        for n in range(len(Z)):
            suma += D2[m][n] * A1[m][n]
    print("\n F1) Valor minimo de la funcion costo : {}".format(suma))


llenar_matriz_asignacion_v1()

#********************************************

WR = [0.02 , 0.02 , 0.78 , 0.18]
apha = [0 , 0.25 , 0.75]
beta = [1 , 0.75 , 0.25]

def calcular_matriz_asignacion_v2(carro):
    aux = []
    suma = 0
    for n in range(len(Z)):
        suma = D2[carro][n] * apha[carro] + beta[carro] * WR[n]
        aux.append(suma)
    print(aux)
    print("Menor para el carro {} : {}".format(carro , min(aux)))

def consultar_matriz_v1(array , carro):
    for p in array:
        if A1[carro][p] == 1:
            return p

def funcion_costo_v2():
    suma = 0
    for m in range(len(C)):
        for n in range(len(Z)):
            suma += D2[m][n] * A2[m][n] * apha[m] + A2[m][n] * beta[m] * WR[n]
    print("\n F2) Valor minimo de la funcion costo : {}".format(suma))

calcular_matriz_asignacion_v2(0)