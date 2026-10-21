import matplotlib.pyplot as plt
import numpy as np
from constante import *
from integration import * 

#on suppose X(t) = X0 constant
#on définit ici les fonction u et v avec X0 constant

def u(x,z,q, X0):
    return X0*np.pi*np.sin(np.pi*z)*np.sin(q*x)

def v(x,z,q,X0):
    return X0*q*np.cos(np.pi*z)*np.cos(q*x)


#cherchons à afficher ce champ de vecteurs 
X0=1 #on choisit une constante, on verra après comment la choisir
Y0,Z0=1,1
"""
X=np.linspace(0,10,1)
Z=np.linspace(0,10,1)
"""
def afficher_vort_et_vitesse(X,Z,U,V):
    plt.figure()
    plt.pcolormesh(X,Z,vort(X,Z,q,X0))
    plt.quiver(X,Z,U,V)
    
    plt.show()

def afficher_theta_et_vitesse(X,Z,U,V):
    plt.figure()
    plt.pcolormesh(X,Z,temp(X,Z,q,Y0,Z0))   
    plt.quiver(X,Z,U,V)
    plt.show()

def vort(x,z,q,X0):
    return np.pi**2*X0*np.cos(np.pi*z)*np.sin(q*x)+q**2*X0*np.cos(np.pi*z)*np.sin(q*x)

def temp(x,z, q, Y, Z):
    return Y*np.cos(np.pi*z)*np.cos(q*x)+Z*np.sin(2*np.pi*z)
T=[]
valeurs_r = [0.5, 18, 28]
for r in valeurs_r:
    T.append(integration(X0,Y0,Z0,r))

def papillon(T):
    """
    fig, axes = plt.subplots(1, 3, figsize=(8, 6))
    axes[0] = fig.add_subplot(projection='3d')
    axes[0].plot([t[0] for t in T],[t[1] for t in T],[t[2] for t in T], label='Courbe papillon r=0.5', markersize=5, color='blue')
    axes[1] = fig.add_subplot(projection='3d')
    axes[0].plot([t[0] for t in T],[t[1] for t in T],[t[2] for t in T], label='Courbe papillon r=18', markersize=5, color='blue')
    axes[0] = fig.add_subplot(projection='3d')
    axes[0].plot([t[0] for t in T],[t[1] for t in T],[t[2] for t in T], label='Courbe papillon r=28', markersize=5, color='blue')
    """
    fig = plt.figure(figsize=(15, 5))
    for i, r in enumerate(valeurs_r):
    # Création du sous-graphique 3D
        ax = fig.add_subplot(1, 3, i + 1, projection='3d')
    
    # Récupération de la trajectoire pour le r courant
        traj = T[i]
    
    # Comme 'traj' est une liste de listes [ [X,Y,Z], [X,Y,Z], ... ], 
    # on extrait chaque coordonnée avec une liste en compréhension :
        x_vals = [point[0] for point in traj]
        y_vals = [point[1] for point in traj]
        z_vals = [point[2] for point in traj]
    
    # Tracé de la courbe
        ax.plot(x_vals, y_vals, z_vals, label=f'r = {r}', color='blue', linewidth=0.6)
    
        ax.set_title(f'Système de Lorenz (r = {r})')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()

    plt.tight_layout()
    plt.show()


papillon(T)








