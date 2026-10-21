import matplotlib.pyplot as plt
import numpy as np


#on suppose X(t) = X0 constant
#on définit ici les fonction u et v avec X0 constant

def u(x,z,q, X0):
    return X0*np.pi*np.sin(np.pi*z)*np.sin(q*x)

def v(x,z,q,X0):
    return X0*q*np.cos(np.pi*z)*np.cos(q*x)

def V(x,z,q,X0):
    return np.array(u(x,z,q,X0),v(x,z,q,X0))

#cherchons à afficher ce champ de vecteurs 
q=np.pi /np.sqrt(2) #donné dans le sujet 
X0=1 #on choisit une constante, on verra après comment la choisir

X=np.linspace(0,10,1)
Z=np.linspace(0,10,1)

plt.figure()
plt.quiver(X,Z, u(X,Z,q,X0),v(X,Z,q,X0))
plt.show()













