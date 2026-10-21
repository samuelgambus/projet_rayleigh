import matplotlib.pyplot as plt
import numpy as np


#on suppose X(t) = X0 constant
#on définit ici les fonction u et v avec X0 constant

def u(x,z,q, X0):
    return X0*np.pi*np.sin(np.pi*z)*np.sin(q*x)

def v(x,z,q,X0):
    return X0*q*np.cos(np.pi*z)*np.cos(q*x)


#cherchons à afficher ce champ de vecteurs 
q=np.pi /np.sqrt(2) #donné dans le sujet 
X0=1 #on choisit une constante, on verra après comment la choisir

X=np.linspace(0,10,1)
Z=np.linspace(0,10,1)

def afficher(X,Z,U,V):
    plt.figure()
    plt.quiver(X,Z,U,V)
    plt.pcolormesh(X,Z,vort(X,Z,q,X0))
    plt.show()

def vort(x,z,q,X0):
    return np.pi**2*X0*np.cos(np.pi*z)*np.sin(q*x)+q**2*X0*np.cos(np.pi*z)*np.sin(q*x)

def temp(x,z, q, Y, Z):
    return Y*np.cos(np.pi*z)*np.cos(q*x)+Z*np.sin(2*np.pi*z)













