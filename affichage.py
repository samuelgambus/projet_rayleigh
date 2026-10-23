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
def papillons_r(valeurs_r):
    T=[]
    for r in valeurs_r:
        T.append(integration(X0,Y0,Z0,r))


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


valeurs_r = [0.5, 18, 350]

#papillons_r(valeurs_r)

r=28



def papillons_CI_comparaison(CI_initiale, r, temps_court_max=30.0):
    # Nombre de pas de temps pour la vue courte
    Nt_court = int(temps_court_max / h)
    temps_court = np.arange(Nt_court + 1) * h
    
    # 1. Calcul de la trajectoire de référence (sans perturbation)
    traj_ref = integration(CI_initiale[0], CI_initiale[1], CI_initiale[2], r)
    
    fig = plt.figure(figsize=(16, 10))
    noms = {0: 'X', 1: 'Y', 2: 'Z'}
    
    # Limite pour la référence sur le temps court
    limite_3d_ref = min(Nt_court + 1, len(traj_ref))
    x_ref_3d = [traj_ref[k][0] for k in range(limite_3d_ref)]
    y_ref_3d = [traj_ref[k][1] for k in range(limite_3d_ref)]
    z_ref_3d = [traj_ref[k][2] for k in range(limite_3d_ref)]
    
    for i in range(3):
        # Création d'une copie stricte et perturbation UNIQUE de la i-ème variable
        CI_pert = list(CI_initiale)
        CI_pert[i] += 1e-3  # Ajout de 10^-3 exactement sur la variable i
        
        # Calcul de la trajectoire perturbée
        traj_pert = integration(CI_pert[0], CI_pert[1], CI_pert[2], r)
        
        # --- LIGNE DU HAUT : 3D (Référence vs Perturbé sur le temps court) ---
        ax_3d = fig.add_subplot(2, 3, i + 1, projection='3d')
        
        limite_3d_pert = min(Nt_court + 1, len(traj_pert))
        x_p = [traj_pert[k][0] for k in range(limite_3d_pert)]
        y_p = [traj_pert[k][1] for k in range(limite_3d_pert)]
        z_p = [traj_pert[k][2] for k in range(limite_3d_pert)]
        
        # Tracé de la trajectoire de référence en 3D (ex: en gris/noir pointillé ou fin)
        ax_3d.plot(x_ref_3d, y_ref_3d, z_ref_3d, color='blue', linestyle='--', linewidth=0.4, label='réf')
        # Tracé de la trajectoire perturbée en 3D (en rouge ou bleu)
        ax_3d.plot(x_p, y_p, z_p, color='red', linewidth=0.5, alpha=0.8, label='perturbé')
        
        ax_3d.set_title(f'Espace des phases 3D\n(Perturbation sur {noms[i]})')
        ax_3d.set_xlabel('X')
        ax_3d.set_ylabel('Y')
        ax_3d.set_zlabel('Z')
        ax_3d.legend()
        
        # --- LIGNE DU BAS : Comparaison Référence vs Perturbé (Temps court) ---
        ax_2d = fig.add_subplot(2, 3, i + 4)
        
        # Extraction de la variable i sur le temps court
        var_ref = [traj_ref[k][i] for k in range(min(Nt_court + 1, len(traj_ref)))]
        var_pert = [traj_pert[k][i] for k in range(min(Nt_court + 1, len(traj_pert)))]
        t_reel = temps_court[:len(var_ref)]
        
        # Tracé avec des styles bien distincts pour les distinguer
        ax_2d.plot(t_reel, var_ref, color='blue', linestyle='--', linewidth=1.5, label=f'{noms[i]} (réf)')
        ax_2d.plot(t_reel, var_pert, color='red', linestyle='-', linewidth=1.0, alpha=0.8, label=f'{noms[i]} (perturbé)')
        
        ax_2d.set_title(f'Divergence de {noms[i]} (0 à {temps_court_max}s)')
        ax_2d.set_xlabel('Temps t')
        ax_2d.set_ylabel(noms[i])
        ax_2d.legend()

    plt.tight_layout()
    plt.show()

papillons_CI_comparaison([X0,Y0,Z0],r)


#REMARQUE ANALYSE: on remarque que perturbé ou non, c'est les memes trajectoires
#genre l'idée c'est que en régime chaotioque, dans tous les cas il vont explorer
#toutes les possibilités, donc la perturbation n'a pas tant d'impact
#en d'ailleurs si on teste avec r=18, ie pas de chaos, ça bifurque pas
#prcq 10e3 ça se voit pas quoi

















# --- Fonctions adaptées avec les valeurs à l'instant t ---
#def u(x,z,q, X0):
    #return X0*np.pi*np.sin(np.pi*z)*np.sin(q*x)

def u(x, z, q, X_t):
    return X_t * np.pi * np.sin(np.pi * z) * np.sin(q * x)

#def v(x,z,q,X0):
    #return X0*q*np.cos(np.pi*z)*np.cos(q*x)

def v(x, z, q, X_t):
    return X_t * q * np.cos(np.pi * z) * np.cos(q * x)

#def vort(x,z,q,X0):
    #return np.pi**2*X0*np.cos(np.pi*z)*np.sin(q*x)+q**2*X0*np.cos(np.pi*z)*np.sin(q*x)

def vort(x, z, q, X_t):
    return np.pi**2 * X_t * np.cos(np.pi * z) * np.sin(q * x) + q**2 * X_t * np.cos(np.pi * z) * np.sin(q * x)

#def temp(x,z, q, Y, Z):
    #return Y*np.cos(np.pi*z)*np.cos(q*x)+Z*np.sin(2*np.pi*z)

def temp(x, z, q, Y_t, Z_t):
    return Y_t * np.cos(np.pi * z) * np.cos(q * x) + Z_t * np.sin(2 * np.pi * z)



def afficher_physique_instant(traj, n, q):
    # Récupération des valeurs de X, Y, Z à l'instant t_n
    X_n = traj[n][0]
    Y_n = traj[n][1]
    Z_n = traj[n][2]
    
    # Définition de l'espace physique (selon le sujet : x dans [-2*pi/q, 2*pi/q] et z dans [0, 1])
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 40)
    z_vals = np.linspace(0, 1, 40)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)
    
    # Calcul des champs sur la grille
    U = u(X_grid, Z_grid, q, X_n)
    V = v(X_grid, Z_grid, q, X_n)
    Vort_grid = vort(X_grid, Z_grid, q, X_n)
    Theta_grid = temp(X_grid, Z_grid, q, Y_n, Z_n)
    
    # --- Figure 1 : Vorticité et Champ de vitesse ---
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(X_grid, Z_grid, Vort_grid, shading='auto', cmap='coolwarm')
    plt.colorbar(label='Vorticité')
    plt.quiver(X_grid, Z_grid, U, V, color='black')
    plt.title(f"Vorticité et Vitesse (instant n={n})")
    plt.xlabel('x')
    plt.ylabel('z')
    plt.tight_layout()
    plt.show()
    
    # --- Figure 2 : Température et Champ de vitesse ---
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(X_grid, Z_grid, Theta_grid, shading='auto', cmap='inferno')
    plt.colorbar(label='Écart de température theta')
    plt.quiver(X_grid, Z_grid, U, V, color='white')
    plt.title(f"Température et Vitesse (instant n={n})")
    plt.xlabel('x')
    plt.ylabel('z')
    plt.tight_layout()
    plt.show()



# Paramètre du nombre d'onde q donné dans le sujet


# Condition initiale et paramètres
X0, Y0, Z0 = 1.0, 1.0, 1.0

# --- Cas r = 10 (Régime stable / stationnaire) ---
print("Calcul pour r = 10...")
traj_r10 = integration(X0, Y0, Z0, r=10)
# On prend un instant vers la fin de la simulation (ex: le dernier point -1)
afficher_physique_instant(traj_r10, -1, q)

# --- Cas r = 28 (Régime chaotique) ---
print("Calcul pour r = 28...")
traj_r28 = integration(X0, Y0, Z0, r=28)
# En régime chaotique, les mouvements changent tout le temps, vous pouvez tester différents indices n (ex: 100, 500, -1)
afficher_physique_instant(traj_r28, -1, q)




import matplotlib.pyplot as plt
import numpy as np
from constante import *
from integration import *

def comparer_r10_r28_instants(indices=[50, 200, 500]):
    q = np.pi / np.sqrt(2)
    X0, Y0, Z0 = 1.0, 1.0, 1.0
    
    # 1. Calcul des trajectoires pour r = 10 et r = 28
    print("Calcul des trajectoires...")
    traj_r10 = integration(X0, Y0, Z0, r=10)
    traj_r28 = integration(X0, Y0, Z0, r=28)
    
    # 2. Définition de la grille spatiale (x et z)
    x_vals = np.linspace(-2 * np.pi / q, 2 * np.pi / q, 30)
    z_vals = np.linspace(0, 1, 30)
    X_grid, Z_grid = np.meshgrid(x_vals, z_vals)
    
    # 3. Création de la figure 2x3
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    
    # --- LIGNE DU HAUT : r = 10 à 3 instants différents ---
    for j, n in enumerate(indices):
        X_n = traj_r10[n][0]
        
        # Calcul des champs
        Vort_grid = vort(X_grid, Z_grid, q, X_n)
        U = u(X_grid, Z_grid, q, X_n)
        V = v(X_grid, Z_grid, q, X_n)
        
        ax = axes[0, j]
        im = ax.pcolormesh(X_grid, Z_grid, Vort_grid, shading='auto', cmap='coolwarm')
        ax.quiver(X_grid, Z_grid, U, V, color='black', scale=400)
        ax.set_title(f"r = 10 (instant t_n, n={n})")
        ax.set_xlabel('x')
        ax.set_ylabel('z')

    # --- LIGNE DU BAS : r = 28 à 3 instants différents ---
    for j, n in enumerate(indices):
        X_n = traj_r28[n][0]
        
        # Calcul des champs
        Vort_grid = vort(X_grid, Z_grid, q, X_n)
        U = u(X_grid, Z_grid, q, X_n)
        V = v(X_grid, Z_grid, q, X_n)
        
        ax = axes[1, j]
        im = ax.pcolormesh(X_grid, Z_grid, Vort_grid, shading='auto', cmap='coolwarm')
        ax.quiver(X_grid, Z_grid, U, V, color='black', scale=400)
        ax.set_title(f"r = 28 (chaos, n={n})")
        ax.set_xlabel('x')
        ax.set_ylabel('z')

    plt.tight_layout()
    plt.show()

# Appel de la fonction (vous pouvez changer les indices selon votre nombre de pas Nt)
comparer_r10_r28_instants(indices=[50, 300, 900])