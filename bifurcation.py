from constante import *
from integration import *

def bifurcation_stable(N,X0,Y0,Z0):
    points = []
    for r in np.linspace(1,30,100):
        T = integration(X0,Y0,Z0,r)
        points.append(T[-N:])
    return points

def maxima_locaux(Z): #garde les maximas locaux d'une liste
    Z_max = []
    for i in range(1,len(Z) - 1):
        if Z[i]>Z[i-1] and Z[i]>Z[i+1]:
            Z_max.append(Z[i])
    return Z_max

def bifurcation_chaos(Np,X0,Y0,Z0):
    maximas = []
    for r in np.linspace(30,350,100):
        Z = integration(X0,Y0,Z0,r)[2]
        Z_max = maxima_locaux([z - r for z in Z])
        maximas.append(Z_max[-Np:])
    return maximas