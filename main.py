from random import randint

Z = ["Z1", "Z2", "Z3", "Z4"]  # N ZONAS
TZ = ["A" , "A" , "P" , "G"] # TIPO DE ZONA

# M CARROR EN SOLICITUD DE ESTACIONAMIENTO EN UN TIEMPO DETERMINADO
C = ["C1", "C2", "C3", "C4", "C5"]
TC = ["P" , "A" , "A" , "G", "A"] # TIPO DE CARRO

D = [[0.24, 0.48, 0.20, 0.18],  # MATRIZ DE DISTANCIAS DE LOS CARROS HACIA LAS ZONAS DE ESTACIONAMIENTO
     [0.16, 0.13, 0.02, 0.26],
     [0.15, 0.61, 0.01, 0.52],
     [0.19, 0.54, 0.23, 0.45],
     [0.23, 0.73, 0.33, 0.31]
     ]

T = [[10, 3, 1, 5],  # MATRIZ DE TIEMPO QUE TOMA A CADA CARRO LLEGAR A LAS ZONAS EN MINUTOS
     [7, 8, 2, 5],
     [2, 7, 2, 2],
     [6, 3, 8, 3],
     [2, 8, 1, 8]
     ]


FS = [39, 18, 51, 63]  # CANTIDAD DE SPOTS LIBRES POR ZONA

WR = [[0.02, 0.78, 0.02, 0.18],
      [0.03, 0.43, 0.32, 0.83],
      [0.05, 0.43, 0.74, 0.72],
      [0.06, 0.13, 0.23, 0.16],
      [0.03, 0.64, 0.32, 0.67]
      ]

apha = [0, 0.25, 0.75, 0.35, 0.15]
beta = [1, 0.75, 0.25, 0.65, 0.85]

A = []  # A = (aij)M×N

for m in range(len(C)):  # CREAR MATRIZ DE ASIGNACION EN BLANCO
    fila = []
    for n in range(len(Z)):
        fila.append(0)
    A.append(fila)

def clone(array):
    a = []
    for e in array:
        a.append(e)
    return a

def get_positions(array, original):
    v = []
    for a in array:
        i = original.index(a)
        v.append(i)
    return v

def get_slice_array(array, indexs):
    v = []
    for i in indexs:
        v.append(array[i])
    return v

def get_not_zonas_type(type):
    zn = []
    for i,z in enumerate(Z):
        if type != TZ[i]:
            zn.append(i)
    return zn

def is_available(zona):
    if FS[zona] > 0:
        return True
    else:
        return False

def update_fs(fs):
    #ASUMIR QUE EL TIEMPO QUE LE FALTA A LOS CARROS ESTACIONADOS PARA IRSE RANDOM
    for c in range(len(C)):
        for z in range(len(Z)):
            leave = randint(0, 20)
            t = T[c][z]
            if leave < t:
                fs[z] += 1
    return fs

def take_spot(zona,fs):
    fs[zona] -= 1
    return fs

def get_ideal_v1(zonas, skip=[]):
    z = -1
    indexs = sorted(range(len(zonas)), key=zonas.__getitem__)
    for i in indexs:
        if i not in skip:
            if is_available(i):
                z = i
                break
    return z

def get_ideal_v2(zonas, carro, skip=[]):
    zn = -1
    v = []
    for i, z in enumerate(zonas):
        s = z*apha[carro] + beta[carro]*WR[carro][i]
        v.append(s)
    indexs = sorted(range(len(v)), key=v.__getitem__)
    for i in indexs:
        if i not in skip:
            if v.count(v[i]) > 1:
                f = list(filter((v[i]).__ne__, v))
                zn = get_ideal_v1(zonas, get_positions(f, v) + skip)
                break
            if is_available(i):
                zn = i
                break
    return zn

def get_ideal_v3(zonas,carro):
    z = -1
    tc = TC[carro]
    skip = get_not_zonas_type(tc)
    z = get_ideal_v2(zonas, carro, skip)
    return z

def get_ideal_v4(zonas,carro):
    z = get_ideal_v3(zonas, carro)
    return z

def run_example_v1():
    fs = clone(FS)
    print("Cantidad de espacios libres  iniciales  : {}".format(fs))
    for i,c in enumerate(C):
        ideal = get_ideal_v1(D[i])
        take_spot(ideal,fs)
        print("La  mejor zona para el carro {} es => {}".format(i,ideal))
    print("Cantidad de espacios libres  restantes  : {}".format(fs))

def run_example_v2():
    fs = clone(FS)
    print("Cantidad de espacios libres  iniciales  : {}".format(fs))
    for i,c in enumerate(C):
        ideal = get_ideal_v2(D[i],i)
        print(ideal)
        take_spot(ideal,fs)
        print("La  mejor zona para el carro {} es => {}".format(i,ideal))
    print("Cantidad de espacios libres  restantes  : {}".format(fs))

def run_example_v3():
    fs = clone(FS)
    print("Cantidad de espacios libres  iniciales  : {}".format(fs))
    for i,c in enumerate(C):
        ideal = get_ideal_v3(D[i],i)
        take_spot(ideal,fs)
        print("La  mejor zona para el carro {} es => {}".format(i,ideal))
    print("Cantidad de espacios libres  restantes  : {}".format(fs))

def run_example_v4():
    fs = clone(FS)
    print("Cantidad de espacios libres  iniciales  : {}".format(fs))
    fs = update_fs(fs)
    print("Cantidad de espacios libres  actualizados  : {}".format(fs))
    for i,c in enumerate(C):
        ideal = get_ideal_v4(D[i],i)
        take_spot(ideal,fs)
        print("La  mejor zona para el carro {} es => {}".format(i,ideal))
    print("Cantidad de espacios libres  restantes  : {}".format(fs))

run_example_v4()
