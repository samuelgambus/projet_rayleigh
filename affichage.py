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
        # Maintenant, on crée la figure avec 3 sous-graphiques 3D côte à côte
fig = plt.figure(figsize=(15, 5))

for i, r in enumerate(valeurs_r):
    # Création de l'axe 3D pour la i-ème position (1 ligne, 3 colonnes, indice i+1)
    ax = fig.add_subplot(1, 3, i + 1, projection='3d')
    
    # On récupère la trajectoire correspondante dans T
    traj = T[i]
    
    # Tracé de la courbe (en gérant le format de traj selon ce que renvoie votre fonction 'integration')
    # Si 'integration' renvoie un tableau numpy avec les colonnes X, Y, Z :
    ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], label=f'r = {r}', color='blue', linewidth=0.7)
    
    # (Alternative si votre fonction renvoie une liste de tuples/listes au lieu de colonnes numpy :)
    # ax.plot([t[0] for t in traj], [t[1] for t in traj], [t[2] for t in traj], label=f'r = {r}', color='blue', linewidth=0.7)
    
    ax.set_title(f'Attracteur de Lorenz (r = {r})')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

plt.tight_layout()
plt.show()    
    
    plt.show()











