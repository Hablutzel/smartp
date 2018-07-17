from random import randint
import random
import statistics

Z = ["Z1", "Z2", "Z3", "Z4","Z5", "Z6", "Z7", "Z8","Z9"]  # N ZONAS
TZ = ["A" , "A" , "P" , "G", "P" , "A" , "A" , "A","A"] # TIPO DE ZONA

# M CARROR EN SOLICITUD DE ESTACIONAMIENTO EN UN TIEMPO DETERMINADO
C = ["C1", "C2", "C3", "C4", "C5"]
TC = ["P" , "A" , "A" , "G", "A"] # TIPO DE CARRO

D = [[0.24, 0.48, 0.20, 0.18,0.64, 0.25, 0.82, 0.91, 0.85],  # MATRIZ DE DISTANCIAS DE LOS CARROS HACIA LAS ZONAS DE ESTACIONAMIENTO
     [0.16, 0.13, 0.02, 0.26,0.98, 0.93, 0.40, 0.84, 0.82],
     [0.15, 0.61, 0.01, 0.52,0.29, 0.97, 0.95, 0.39, 1.83],
     [0.19, 0.54, 0.23, 0.45,0.35, 0.69, 1.52, 1.18, 2.33],
     [0.23, 0.73, 0.33, 0.31,0.92, 0.92, 0.92, 1.57, 1.23]
     ]

T = [[10, 3, 1, 5,6,2,6,7,2],  # MATRIZ DE TIEMPO QUE TOMA A CADA CARRO LLEGAR A LAS ZONAS EN MINUTOS
     [7, 8, 2, 5],
     [2, 7, 2, 2],
     [6, 3, 8, 3],
     [2, 8, 1, 8]
     ]


FS = [13, 21, 43, 31, 41, 24, 23, 23 , 12]  # CANTIDAD DE SPOTS LIBRES POR ZONA

WR = [[0.02, 0.78, 0.02, 0.18, 0.22, 0.74, 0.34, 0.93, 0.13],
      [0.03, 0.43, 0.32, 0.83, 0.62, 0.45, 0.44, 0.35, 0.35],
      [0.05, 0.43, 0.74, 0.72, 0.14, 0.63, 0.14, 0.14, 0.63],
      [0.06, 0.13, 0.23, 0.16, 0.14, 0.24, 0.46, 0.22, 0.15],
      [0.03, 0.64, 0.32, 0.67, 0.12, 0.13, 0.24, 0.33, 0.64]
      ]

apha = [0.3, 0.25, 0.75, 0.35, 0.15]
beta = [0.7, 0.75, 0.25, 0.65, 0.85]

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

# Random : Random asignment
def Random():
    solution_matrix = []
    for c in range(len(C)):
        r = randint(0, 3)
        v = [0 for x in range(len(Z))]
        v[r] = 1
        solution_matrix.append(v)
    weight = evaluateMatrix(solution_matrix)
    # print("(RANDOM) Best solution : {}".format(weight))
    return weight

# Gready
def Gready():
    fs = clone(FS)
    solution_matrix = []
    for i,c in enumerate(C):
        ideal = get_ideal_v3(D[i],i)
        take_spot(ideal,fs)
        v = [0 for x in range(len(Z))]
        v[ideal] = 1
        solution_matrix.append(v)
    weight = evaluateMatrix(solution_matrix)
    # print("(GREEADY) Best solution : {}".format(weight))
    return weight

# GRASP : Greedy randomized adaptative search procedure
def getOptionsVectors():
    result = []
    for i,z in enumerate(Z):
        v = [0 for x in range(len(Z))]
        v[i] = 1
        result.append(v)
    return result

def getCostByCard(zonas , carro):
    s = 0
    for i,z in enumerate(zonas):
        s += z*D[carro][i]*apha[carro] + z*beta[carro]*WR[carro][i]
    return s

def evaluateMatrix(matrix):
    cost = 0
    for i,m in enumerate(matrix):
        cost += getCostByCard(m,i)
    return cost

def RandomGreedy(count):
    population = []
    weights = []
    for cont in range(count):
        solution_matrix = []
        for car in range(len(C)):
            vectors = getOptionsVectors()
            costs = []
            for i,v in enumerate(vectors):
                c = getCostByCard(v,car)
                costs.append(c)
            indexs = sorted(range(len(costs)), key=costs.__getitem__)
            r = randint(0, 2)
            pos = indexs[r]
            select = vectors[pos]
            solution_matrix.append(select)
        population.append(solution_matrix)
        weight = evaluateMatrix(solution_matrix)
        weights.append(weight)
        # print("Add chromosome : {} , Weight : {}".format(cont+1,weight))
    indexs = sorted(range(len(weights)), key=weights.__getitem__)
    best_solution = population[indexs[0]]
    weight = weights[indexs[0]]
    # print("(GRASP) Best solution : {}".format(weight))
    return weight

# Genetic algorithm
def getRandomSolutionMatrix(count):
    population = []
    for i in range(count):
        solution_matrix = []
        for c in range(len(C)):
            r = randint(0, 3)
            v = [0 for x in range(len(Z))]
            v[r] = 1
            solution_matrix.append(v)
        population.append(solution_matrix)
    return population
    
def getRandomElements(k , len):
    find = False
    while not find:
        find = True
        randoms = []
        for i in range(k):
            randoms.append(randint(0, len-1))
        for r in randoms:
            if(randoms.count(r) > 1):
                find = False
                break

    return randoms

def battle(randoms , weigths):
    b1 = weigths[randoms[0]]
    b2 = weigths[randoms[1]]
    if b1 >= b2:
        return randoms[0]
    else:
        return randoms[1]

def isFinishBattle(table):
    s = 0
    for t in table:
        s += t[2]
    if (s==len(table)):
        return True
    else:
        return False

def findMax(table):
    values = [x[1] for x in table]
    indexs = sorted(range(len(values)), key=values.__getitem__,reverse=True)
    return indexs[0],indexs[1]

def swap(vector):
    r = getRandomElements(2,len(vector))
    v1 = vector[r[0]]
    v2 = vector[r[1]]
    vector[r[0]] = v2
    vector[r[1]] = v1
    return vector

def Mutation(matrix,pocentaje):
    for m in matrix:
        r = randint(1, 100)
        if (r > 5):
            m = swap(m)
    return matrix

def TournamentSelection(k,pop_weigths ):
    table = []
    for i,w in enumerate(pop_weigths):
        table.append([i,0,0])
    while(not isFinishBattle(table)):
        randoms = getRandomElements(k,len(pop_weigths))
        win = battle(randoms, pop_weigths)
        table[randoms[0]][2] = 1
        table[randoms[1]][2] = 1
        table[win][1] += table[win][1] + 1
    return findMax(table)
    
def croosOverSinglePoint(m1, m2):
    s1 = m1[0:3] + m2[3:5]
    s2 = m2[0:3] + m1[3:5]
    return s1,s2

def GeneticAlgorithm(num_population, iterations):

    random_solutions = getRandomSolutionMatrix(num_population)
    weigths = []
    best_matrix = 0
    for i,r in enumerate(random_solutions):
        weigths.append(evaluateMatrix(r))
    
    for i in range(iterations):
        w1,w2 = TournamentSelection(2,weigths)
        m1 = random_solutions[w1]
        m2 = random_solutions[w2]
        s1,s2 = croosOverSinglePoint(m1,m2)
        s1 = Mutation(s1,5)
        s2 = Mutation(s2,5)
        p1 = evaluateMatrix(s1)
        p2 = evaluateMatrix(s2)
        min_index = weigths.index(min(weigths))
        if(p1>=p2):
            random_solutions[min_index] = s1
            weigths[min_index] = p1
            best_matrix = s1
        else:
            random_solutions[min_index] = s2
            weigths[min_index] = p2
            best_matrix = s2
# HGRASH 

def getGreedyMatrix(count):
    population = []
    for cont in range(count):
        solution_matrix = []
        for car in range(len(C)):
            vectors = getOptionsVectors()
            costs = []
            for i,v in enumerate(vectors):
                c = getCostByCard(v,car)
                costs.append(c)
            indexs = sorted(range(len(costs)), key=costs.__getitem__)
            r = randint(0, 2)
            pos = indexs[r]
            select = vectors[pos]
            solution_matrix.append(select)
        population.append(solution_matrix)
    return population

def croosOverMXP(m1, m2):
    s1 = m1[0:2] + m2[2:5]
    s2 = m2[0:2] + m1[2:5]
    return s1,s2

def Hgrasp(num_population, iterations):
    random_solutions = getGreedyMatrix(num_population)
    weigths = []
    best_matrix = 0
    for i,r in enumerate(random_solutions):
        weigths.append(evaluateMatrix(r))
    
    for i in range(iterations):
        w1,w2 = TournamentSelection(2,weigths)
        m1 = random_solutions[w1]
        m2 = random_solutions[w2]
        s1,s2 = croosOverMXP(m1,m2)
        s1 = Mutation(s1,5)
        s2 = Mutation(s2,5)
        p1 = evaluateMatrix(s1)
        p2 = evaluateMatrix(s2)
        min_index = weigths.index(min(weigths))
        if(p1>=p2):
            random_solutions[min_index] = s1
            weigths[min_index] = p1
            best_matrix = s1
        else:
            random_solutions[min_index] = s2
            weigths[min_index] = p2
            best_matrix = s2

    
    
        
Hgrasp(20,20)






