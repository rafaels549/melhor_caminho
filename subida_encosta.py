from ast import While
import numpy as np
import random as rd

def GerarProblema(n,min1,max1):    
    mat  = np.random.randint(min1,max1,(n,n))
    return mat

def Avalia(n,mat,sol):
    v = 0   
    for i in range(n-1):
        v += mat[sol[i]][sol[i+1]]
    v += mat[sol[n-1]][sol[0]]    
    return v


def SolucaoInicial(n):
    return np.random.permutation(n)


def Vizinho(sol):
    n = len(sol)
    i, j = rd.sample(range(n), 2)
    viz = sol.copy()
    viz[i], viz[j] = viz[j], viz[i]
    return viz


def SubidaEncostaLimite(n, mat, max_iter=1000):
    sol_inicial = SolucaoInicial(n)
    custo_inicial = Avalia(n, mat, sol_inicial)

    sol = sol_inicial
    custo_sol = custo_inicial
    
    for _ in range(max_iter):
        viz = Vizinho(sol)
        custo_viz = Avalia(n, mat, viz)
    
        if custo_viz > custo_sol:
            sol = viz
            custo_sol = custo_viz
    
    return sol, custo_sol, sol_inicial, custo_inicial
def SubidaEncosta(n, mat):
    sol_inicial = SolucaoInicial(n)
    custo_inicial = Avalia(n, mat, sol_inicial)

    sol = sol_inicial
    custo_sol = custo_inicial

    while True:
        viz = Vizinho(sol)
        custo_viz = Avalia(n, mat, viz)
        if custo_viz > custo_sol:
            sol = viz
            custo_sol = custo_viz
        else:
            break
    
    
    return sol, custo_sol, sol_inicial, custo_inicial


N = 30
MIN1 = 10
MAX1 = 100


mat = GerarProblema(N, MIN1, MAX1)
sol, valor, sol_inicial, custo_inicial = SubidaEncostaLimite(N, mat, max_iter=1000)

print("Solução encontrada:", sol)
print("Valor:", valor)


