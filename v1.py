Z = ["Z1" , "Z2" , "Z3" , "Z4"] # N ZONAS

C = ["C1" , "C2" , "C3"] # M CARROR EN SOLICITUD DE ESTACIONAMIENTO EN UN TIEMPO DETERMINADO

D = [   [0.24 , 0.48 , 0.20 , 0.18 ], # MATRIZ DE DISTANCIAS DE LOS CARROS HACIA LAS ZONAS DE ESTACIONAMIENTO
        [0.16 , 0.13 , 0.02 , 0.26],
        [0.17 , 0.6 , 0.14 , 0.3]
    ]

FS = [3,1,0,6] # CANTIDAD DE SPOTS LIBRES POR ZONA

WR = [0.02 , 0.78, 0.02  , 0.18]
apha = [0 , 0.25 , 0.75]
beta = [1 , 0.75 , 0.25]

A = [] # A = (aij)M×N

for m in range(len(C)): # CREAR MATRIZ DE ASIGNACION EN BLANCO
    fila = []
    for n in range(len(Z)):
        fila.append(0)
    A.append(fila)

def clone(array):
    a = []
    for e in array:
        a.append(e)
    return a

def get_positions(array,original):
    v = []
    for a in array:
        i = original.index(a)
        v.append(i)
    return v

def get_slice_array(array, indexs):
    v =  []
    for i in indexs:
        v.append(array[i])
    return v

def is_available(zona):
    if FS[zona] > 0:
        return True
    else:
        return False

def take_spot(zona):
    FS[zona] -= 1

def get_ideal_v1(zonas, skip=[]):
    z = -1
    indexs = sorted(range(len(zonas)),key=zonas.__getitem__)
    for i in indexs:
        if i not in skip:
            if is_available(i):
                z = i
                break
    return z 
 
def get_ideal_v2(zonas,carro):
    z = -1
    v = []
    for i,z in enumerate(zonas):
        s = z*apha[carro] + beta[carro]*WR[i]
        v.append(s)
    indexs = sorted(range(len(v)),key=v.__getitem__)
    for i in indexs:
        if v.count(v[i]) > 1:
            f = list(filter((v[i]).__ne__, v))
            z = get_ideal_v1(zonas, get_positions(f,v))
            break
    return z

       

print("Ideal V2 : {}".format(get_ideal_v2(D[0],0)))


