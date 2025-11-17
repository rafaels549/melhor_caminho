import numpy as np
import random as rd
import math

def GerarProblema(n, min1, max1):    
    return np.random.randint(min1, max1, (n, n))

def Avalia(n, mat, sol):
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

def TemperaSimulada(n, mat, t_ini=1000, t_fim=0.001, fr=0.99):
    si = SolucaoInicial(n)
    vi = Avalia(n, mat, si)

    atual = si.copy()
    va = vi

    sf = atual.copy()
    vf = va

    t = t_ini

    while t > t_fim:
        novo = Vizinho(atual)
        vn = Avalia(n, mat, novo)

        deltaE = vn - va 

        if deltaE > 0:       
            atual = novo
            va = vn
        else:                
            prob = math.exp(deltaE / t)
            if rd.random() < prob:
                atual = novo
                va = vn

        
        if va > vf:
            sf = atual.copy()
            vf = va

        t = t * fr

    return si, vi, sf, vf
