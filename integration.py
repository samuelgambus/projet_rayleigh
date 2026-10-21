import numpy as np
from constante import *

def f(X,Y,Z):
    return (Pr*(Y-X),-X*Z + r*X - Y,X*Y - b*Z)

def runge_kutta(X,Y,Z):
    k1 = f(X,Y,Z)

    k2 = f(X + (h/2)*k1[0],Y + (h/2)*k1[1],Z+ (h/2)*k1[2])

    k3 = f(X + (h/2)*k2[0],Y + (h/2)*k2[1],Z+ (h/2)*k2[2])

    k4 = f(X + h*k3[0],Y + h*k3[1],Z+ h*k3[2])

    return (X + (h/6)*(k1[0]+2*k2[0]+2*k3[0]+k4[0]), Y + (h/6)*(k1[1]+2*k2[1]+2*k3[1]+k4[1]), Z + (h/6)*(k1[2]+2*k2[2]+2*k3[2]+k4[2]))


def integration(X0,Y0,Z0):
    tab=[[X0,Y0,Z0]]
    for i in range(Nt):
        tab.append(runge_kutta(tab[i]))
    return tab

        









